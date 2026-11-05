# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Build, update or rebuild a whole Liana system in a design."""

from __future__ import annotations

import math
import traceback
from collections.abc import Callable
from typing import Any

import adsk.core
import adsk.fusion

from ..core.layout import topology
from ..core.report import BuildLog
from ..core.settings import MOUNT_SIDES, Settings, Side
from .api import API_ERRORS, MM, Application, Component, Design, Occurrence, UserInterface
from .appearance import paint_parts
from .comb import build_comb
from .context import BuildContext
from .design import (
    ATTR_GROUP,
    find_system,
    is_empty,
    is_hybrid,
    load_design_settings,
    new_comp,
    new_design,
    save_design_settings,
    tag,
    upsert_params,
)
from .frame import build_frame
from .rail import build_rail
from .tie_mount import build_tie

SYSTEM_NAME = "Liana"
"""Name of the top component of a system."""

TITLE = "Liana"
"""Title of the progress dialog."""

PartBuilder = Callable[[BuildContext, Component, Settings], None]
"""Function that models one part into an empty component."""

_SEAT_ANGLE: dict[Side, float] = {"S": 0, "E": 90, "N": 180, "W": 270}


class Progress:
    """Progress dialog for builds.

    One dialog is kept for the whole session: Fusion does not destroy a
    dialog it created, so a new one per build would pile up hidden windows.
    """

    def __init__(self, ui: UserInterface | None) -> None:
        """Create the reporter; the dialog itself is created on first use.

        Args:
            ui: Fusion user interface, or None to report nothing.
        """
        self._ui = ui
        self._dialog: Any = None
        self._active = False
        self._step = 0

    def start(self, total: int) -> None:
        """Show the dialog for a build of ``total`` steps."""
        self._step = 0
        self._active = False
        if self._ui is None:
            return
        try:
            if self._dialog is None:
                dialog = self._ui.createProgressDialog()
                dialog.isCancelButtonShown = False
                self._dialog = dialog
            self._dialog.show(TITLE, "Building...", 0, total, 0)
            self._active = True
        except API_ERRORS:
            self._active = False  # build without progress feedback

    def step(self, message: str) -> None:
        """Advance by one step and show what is being built."""
        self._step += 1
        if not self._active:
            return
        try:
            self._dialog.message = message
            self._dialog.progressValue = self._step
            adsk.doEvents()
        except API_ERRORS:
            pass  # progress feedback is cosmetic

    def close(self) -> None:
        """Hide the dialog."""
        if not self._active:
            return
        self._active = False
        try:
            self._dialog.hide()
        except API_ERRORS:
            pass  # a dialog left open closes with the next build


def _matrix(angle_deg: float, tx: float, ty: float, tz: float) -> object:
    """Return a rotation about +Y followed by a translation in mm."""
    m = adsk.core.Matrix3D.create()
    if angle_deg:
        m.setToRotation(
            math.radians(angle_deg),
            adsk.core.Vector3D.create(0, 1, 0),
            adsk.core.Point3D.create(0, 0, 0),
        )
    m.translation = adsk.core.Vector3D.create(tx * MM, ty * MM, tz * MM)
    return m


def seat_matrix(ctx: BuildContext, side: Side) -> object:
    """Return the transform that puts a holder under one side of the frame."""
    a, ft, fz = ctx.ev("FRAME_A"), ctx.ev("FRAME_T"), ctx.ev("FRAME_Z")
    offsets: dict[Side, tuple[float, float]] = {
        "S": (0.0, a),
        "E": (a, 0.0),
        "N": (0.0, -a),
        "W": (-a, 0.0),
    }
    tx, tz = offsets[side]
    return _matrix(_SEAT_ANGLE[side], tx, -ft, fz + tz)


def seat_holders(ctx: BuildContext, system: Component, holder: Component, s: Settings) -> None:
    """Show the holder on the frame sides chosen in the settings.

    Each copy is inserted straight at its final position; moving occurrences
    afterwards would rely on position snapshots that do not survive recompute.
    """
    if not (s["make_frame"] and s["make_holder"]):
        return
    for side in MOUNT_SIDES.get(s["mount"], ()):
        occ = system.occurrences.addExistingComponent(holder, seat_matrix(ctx, side))
        tag(occ, "seat:" + side)


def reseat_holders(ctx: BuildContext, system_occ: Occurrence, s: Settings) -> None:
    """Replace the holder copies on the frame after a size change."""
    system = system_occ.component
    holder = None
    seats = []
    for i in range(system.occurrences.count):
        occ = system.occurrences.item(i)
        attr = occ.attributes.itemByName(ATTR_GROUP, "place")
        if not attr:
            continue
        if attr.value == "holder:":
            holder = occ.component
        elif attr.value.startswith("seat:"):
            seats.append(occ)
    for occ in seats:
        occ.deleteMe()
    if holder is not None:
        seat_holders(ctx, system, holder, s)


def _build_part(
    ctx: BuildContext, name: str, builder: PartBuilder, comp: Component, s: Settings
) -> None:
    """Build one part; a failure is logged and the other parts still get built.

    Fusion can fail a feature for reasons that depend on the geometry, so any
    error is caught here and reported with its traceback.
    """
    try:
        builder(ctx, comp, s)
    except Exception:  # one broken part must not stop the others
        ctx.log.hard.append("%s:\n%s" % (name, traceback.format_exc(limit=3)))


def build_system(ctx: BuildContext, s: Settings, progress: Progress) -> Occurrence:
    """Build every enabled part into the design of ``ctx``.

    Args:
        ctx: Build context.
        s: Settings.
        progress: Progress reporter.

    Returns:
        The system occurrence.
    """
    design = ctx.design
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    upsert_params(design, s)
    root = design.rootComponent
    steps = 1 + (2 if s["make_holder"] else 0) + int(s["make_frame"]) + int(s["make_tie"])
    progress.start(steps)
    try:
        system_occ = new_comp(root, SYSTEM_NAME)
        system_occ.attributes.add(ATTR_GROUP, "system", "1")
        system = system_occ.component
        holder = None
        if s["make_holder"]:
            holder = new_comp(system, "Holder %d" % int(s["cradles"]), "holder:").component
            rail = new_comp(holder, "Rail").component
            comb = new_comp(holder, "Comb").component
            progress.step("Rail")
            _build_part(ctx, "Rail", build_rail, rail, s)
            progress.step("Comb")
            _build_part(ctx, "Comb", build_comb, comb, s)
        if s["make_frame"]:
            progress.step("X-frame")
            frame = new_comp(system, "X-Frame", "frame:").component
            _build_part(ctx, "X-Frame", build_frame, frame, s)
        if s["make_tie"]:
            progress.step("Tie mount")
            tie = new_comp(system, "Tie Mount", "tie:").component
            _build_part(ctx, "Tie Mount", build_tie, tie, s)
        progress.step("Holders on the frame")
        if holder is not None:
            seat_holders(ctx, system, holder, s)
        ctx.soft("Part colours", lambda: paint_parts(ctx.app, design))
        save_design_settings(design, s)
        try:
            design.computeAll()
        except API_ERRORS:
            pass  # Fusion recomputes on the next change anyway
        return system_occ
    finally:
        progress.close()


def generate(app: Application, s: Settings, progress: Progress) -> tuple[str, BuildLog]:
    """Apply the dialog settings to the active design.

    - A design that already holds a system with the same layout gets its
      parameters updated in place.
    - A different layout is rebuilt in the same design.
    - Otherwise the system is built into the active design when it is an
      empty hybrid design, or into a new design.

    Args:
        app: Fusion application.
        s: Settings.
        progress: Progress reporter.

    Returns:
        How the system was built, and the problems recorded.
    """
    log = BuildLog()
    design: Design | None = adsk.fusion.Design.cast(app.activeProduct)
    system_occ = find_system(design) if design else None
    if design is not None and system_occ is not None and not s["new_design"]:
        ctx = BuildContext(app, design, log)
        old = load_design_settings(design)
        if old is not None and topology(old) == topology(s):
            n = upsert_params(design, s)
            reseat_holders(ctx, system_occ, s)
            ctx.soft("Part colours", lambda: paint_parts(app, design))
            save_design_settings(design, s)
            return "updated in place (%d parameter%s changed)" % (n, "" if n == 1 else "s"), log
        try:
            system_occ.deleteMe()
            build_system(ctx, s, progress)
            return "rebuilt in this design", log
        except Exception:  # fall back to a clean document rather than leave the user with nothing
            log.hard.append(
                "in-place rebuild failed, built in a new design:\n" + traceback.format_exc(limit=2)
            )
            build_system(BuildContext(app, new_design(app), log), s, progress)
            return "built in a new design", log
    if design is None or s["new_design"] or not is_hybrid(design) or not is_empty(design):
        design = new_design(app)
        mode = "built in a new design"
    else:
        mode = "built in this design"
    build_system(BuildContext(app, design, log), s, progress)
    return mode, log
