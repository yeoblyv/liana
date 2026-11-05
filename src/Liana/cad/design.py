# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Design-level helpers: documents, components, attributes and parameters."""

from __future__ import annotations

import json

import adsk.core
import adsk.fusion

from ..core.layout import layout
from ..core.params import ANGLE_PARAMS, make_params
from ..core.settings import Settings, from_mapping, in_limits, migrate
from .api import API_ERRORS, MM, Application, Component, Design, Occurrence, value

ATTR_GROUP = "Liana"
"""Attribute group of everything Liana stores in a design."""

_LOAD_ERRORS: tuple[type[Exception], ...] = (*API_ERRORS, ValueError)  # ValueError: malformed JSON


def tag(occ: Occurrence, place: str) -> None:
    """Mark an occurrence with its role, e.g. ``"seat:S"``.

    Args:
        occ: Occurrence to mark.
        place: Role, e.g. ``"holder:"`` or ``"seat:S"``.
    """
    occ.attributes.add(ATTR_GROUP, "place", place)


def new_comp(parent: Component, name: str, place: str | None = None) -> Occurrence:
    """Add a new component at identity under ``parent``.

    Args:
        parent: Parent component.
        name: Component name.
        place: Optional role tag (see :func:`tag`).

    Returns:
        The new occurrence.
    """
    occ = parent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    if place:
        tag(occ, place)
    return occ


def find_system(design: Design | None) -> Occurrence | None:
    """Return the Liana system occurrence of a design, if there is one.

    Args:
        design: Design to search, or None.
    """
    if not design:
        return None
    root = design.rootComponent
    for i in range(root.occurrences.count):
        occ = root.occurrences.item(i)
        if occ.attributes.itemByName(ATTR_GROUP, "system"):
            return occ
    return None


def load_design_settings(design: Design) -> Settings | None:
    """Return the settings stored in a design, or None if there are none.

    The stored JSON is untrusted: the design may come from anyone.

    Args:
        design: Design that may hold a system.
    """
    try:
        attr = design.attributes.itemByName(ATTR_GROUP, "settings")
        if not attr:
            return None
        raw = json.loads(attr.value)
    except _LOAD_ERRORS:
        return None
    if not isinstance(raw, dict):
        return None
    return from_mapping(migrate(raw), within_limits=True)


def save_design_settings(design: Design, s: Settings) -> None:
    """Store the settings in the design, so running Liana again edits it.

    Args:
        design: Design that holds the system.
        s: Settings of the system.
    """
    try:
        design.attributes.add(ATTR_GROUP, "settings", json.dumps(s))
    except API_ERRORS:
        pass  # without them the next run starts from the last dialog values


SETTING_PARAMETERS: dict[str, str] = {
    "cable_d": "CABLE_D",
    "tooth_w": "FIN_W",
    "depth": "DEPTH",
    "screw_d": "WS_D",
    "screw_csk": "WS_CSK",
    "m3_d": "M3_D",
    "nut_af": "NUT_AF",
    "clr": "CLR_X",
    "frame_t": "FRAME_T",
    "tm_l": "TM_L",
    "tm_w": "TM_W",
    "tm_h": "TM_H",
    "tie_w": "TIE_SLOT_W",
}
"""Dialog settings that are User Parameters of their own, by parameter name."""


def _parameter_mm(design: Design, name: str) -> float | None:
    try:
        param = design.userParameters.itemByName(name)
        return None if param is None else round(float(param.value) / MM, 4)
    except API_ERRORS:
        return None


def with_parameter_values(design: Design, s: Settings) -> Settings:
    """Return the settings with the sizes the design's User Parameters hold now.

    A size changed in Change Parameters is not in the settings stored with
    the system; without this the next Generate would set it back.

    Args:
        design: Design with a Liana system.
        s: Settings stored with the system.

    Returns:
        The settings, with every in-range parameter value taken over.
    """
    values: dict[str, object] = dict(s)
    for key, name in SETTING_PARAMETERS.items():
        mm = _parameter_mm(design, name)
        if mm is not None and in_limits(key, mm):
            values[key] = mm
    # BEAM_W holds the beam actually built, which may be widened for the holder;
    # a value other than the one Liana computed was set by hand
    beam = _parameter_mm(design, "BEAM_W")
    if beam is not None and abs(beam - layout(s).bw) > 1e-6 and in_limits("beam_w", beam):
        values["beam_w"] = beam
    return from_mapping(values)


def upsert_params(design: Design, s: Settings) -> int:
    """Create missing User Parameters and update the ones that differ.

    Changed parameters are set in one call, so the design recomputes once.

    Args:
        design: Design to update.
        s: Settings.

    Returns:
        Number of parameters whose expression changed.
    """
    changed, values = [], []
    for name, expr, comment in make_params(s):
        param = design.userParameters.itemByName(name)
        if param is None:
            units = "deg" if name in ANGLE_PARAMS else "mm"
            design.userParameters.add(name, value(expr), units, comment)
            continue
        try:
            param.comment = comment
        except API_ERRORS:
            pass  # a stale comment is cosmetic
        if param.expression.replace(" ", "") != expr.replace(" ", ""):
            changed.append(param)
            values.append(value(expr))
    if not changed:
        return 0
    try:
        design.modifyParameters(changed, values)
    except API_ERRORS:  # Fusion before modifyParameters
        for param, val in zip(changed, values):
            param.expression = val.stringValue
    return len(changed)


def is_hybrid(design: Design) -> bool:
    """Return whether a design can hold several components (hybrid intent).

    Args:
        design: Design to check.
    """
    try:
        return bool(design.designIntent == adsk.fusion.DesignIntentTypes.HybridDesignIntentType)
    except AttributeError:
        return True  # Fusion before design intents: every design is hybrid


def is_empty(design: Design) -> bool:
    """Return whether the root component has no occurrences, bodies or sketches.

    Args:
        design: Design to check.
    """
    root = design.rootComponent
    return not (root.occurrences.count or root.bRepBodies.count or root.sketches.count)


def new_design(app: Application) -> Design:
    """Open a new hybrid design document and return its design.

    Args:
        app: Fusion application.
    """
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(doc.products.itemByProductType("DesignProductType"))
    try:
        design.designIntent = adsk.fusion.DesignIntentTypes.HybridDesignIntentType
    except API_ERRORS:
        pass  # Fusion before design intents
    return design
