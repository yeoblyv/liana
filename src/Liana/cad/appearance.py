# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Part colors, so the rail, comb, frame and tie mount stay apart visually."""

from __future__ import annotations

from typing import Any

import adsk.core

from .api import API_ERRORS, Application, Design

APPEARANCE_LIBRARY_ID = "BA5EE55E-9982-449B-9D66-9F036540E140"
"""Id of the Fusion Appearance Library."""

BASE_APPEARANCES = (
    "Plastic - Matte (Yellow)",
    "Plastic - Glossy (Yellow)",
    "Plastic - Matte (Red)",
    "Plastic - Glossy (Red)",
)
"""Library appearances to copy, in order of preference."""

PART_COLORS: dict[str, tuple[str, tuple[int, int, int]]] = {
    "Rail": ("Liana Red", (220, 45, 45)),
    "Comb": ("Liana Green", (40, 170, 70)),
    "X-Frame": ("Liana Blue", (40, 95, 230)),
    "Tie Mount": ("Liana Green", (40, 170, 70)),
}
"""Component name to appearance name and RGB color."""

_COLOR_PROPERTY_IDS = ("opaque_albedo", "generic_diffuse")


def _appearance_library(app: Application) -> Any:
    libs = app.materialLibraries
    try:
        lib = libs.itemById(APPEARANCE_LIBRARY_ID)
    except API_ERRORS:
        lib = None
    if lib is None:
        for i in range(libs.count):
            if "appearance" in libs.item(i).name.lower():
                return libs.item(i)
    return lib


def _base_appearance(lib: Any) -> Any:
    for name in BASE_APPEARANCES:
        try:
            base = lib.appearances.itemByName(name)
        except API_ERRORS:
            base = None
        if base is not None:
            return base
    for i in range(lib.appearances.count):
        if lib.appearances.item(i).name.lower().startswith("plastic"):
            return lib.appearances.item(i)
    return None


def part_appearance(app: Application, design: Design, name: str, rgb: tuple[int, int, int]) -> Any:
    """Return the named appearance of the design, creating it on first use.

    A plastic appearance from the Fusion library is copied into the design and
    its color property is set.

    Args:
        app: Fusion application.
        design: Design that owns the appearance.
        name: Appearance name.
        rgb: Color.

    Returns:
        The appearance.

    Raises:
        RuntimeError: The copied appearance has no color property.
    """
    existing = design.appearances.itemByName(name)
    if existing is not None:
        return existing
    base = _base_appearance(_appearance_library(app))
    appearance = design.appearances.addByCopy(base, name)
    done = False
    for i in range(appearance.appearanceProperties.count):
        prop = adsk.core.ColorProperty.cast(appearance.appearanceProperties.item(i))
        if prop is None:
            continue
        if prop.id in _COLOR_PROPERTY_IDS or prop.name.lower() == "color":
            prop.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 0)
            done = True
    if not done:
        raise RuntimeError("no color property in appearance %s" % base.name)
    return appearance


def paint_parts(app: Application, design: Design) -> None:
    """Color every Liana part of the design: rail red, comb green, frame blue.

    Args:
        app: Fusion application.
        design: Design with the Liana parts.
    """
    for i in range(design.allComponents.count):
        comp = design.allComponents.item(i)
        if comp.name in PART_COLORS and comp.bRepBodies.count:
            name, rgb = PART_COLORS[comp.name]
            appearance = part_appearance(app, design, name, rgb)
            for j in range(comp.bRepBodies.count):
                comp.bRepBodies.item(j).appearance = appearance
