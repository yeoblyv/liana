# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Design-level helpers: documents, components, attributes and parameters."""

from __future__ import annotations

import json

import adsk.core
import adsk.fusion

from ..core.params import ANGLE_PARAMS, make_params
from ..core.settings import Settings, from_mapping, migrate
from .api import API_ERRORS, Application, Component, Design, Occurrence, value

ATTR_GROUP = "Liana"
"""Attribute group of everything Liana stores in a design."""

_LOAD_ERRORS: tuple[type[Exception], ...] = (*API_ERRORS, ValueError)  # ValueError: malformed JSON


def tag(occ: Occurrence, place: str) -> None:
    """Mark an occurrence with its role, e.g. ``"seat:S"``."""
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
    """Return the Liana system occurrence of a design, if there is one."""
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
    return from_mapping(migrate(raw))


def save_design_settings(design: Design, s: Settings) -> None:
    """Store the settings in the design, so running Liana again edits it."""
    try:
        design.attributes.add(ATTR_GROUP, "settings", json.dumps(s))
    except API_ERRORS:
        pass  # without them the next run starts from the last dialog values


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
    """Return whether a design can hold several components (hybrid intent)."""
    try:
        return bool(design.designIntent == adsk.fusion.DesignIntentTypes.HybridDesignIntentType)
    except AttributeError:
        return True  # Fusion before design intents: every design is hybrid


def is_empty(design: Design) -> bool:
    """Return whether the root component has no occurrences, bodies or sketches."""
    root = design.rootComponent
    return not (root.occurrences.count or root.bRepBodies.count or root.sketches.count)


def new_design(app: Application) -> Design:
    """Open a new hybrid design document and return its design."""
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(doc.products.itemByProductType("DesignProductType"))
    try:
        design.designIntent = adsk.fusion.DesignIntentTypes.HybridDesignIntentType
    except API_ERRORS:
        pass  # Fusion before design intents
    return design
