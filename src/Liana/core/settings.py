# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Dialog settings: defaults, limits, validation and loading from untrusted JSON."""

from __future__ import annotations

import math
from typing import Any, Literal, TypedDict, cast, get_args

Mount = Literal["none", "straight", "L", "T", "X"]
"""Which frame sides show a holder in the design preview."""

Side = Literal["S", "E", "N", "W"]
"""Frame side: south, east, north, west."""


class Settings(TypedDict):
    """Everything the dialog sets; lengths in millimeters."""

    cradles: int
    cable_d: float
    tooth_w: float
    raised_teeth: bool
    center_pin: bool
    depth: float
    screw_d: float
    screw_csk: float
    screw_len: float
    m3_d: float
    nut_af: float
    clr: float
    frame_t: float
    beam_w: float
    tm_l: float
    tm_w: float
    tm_h: float
    tie_w: float
    make_holder: bool
    make_frame: bool
    make_tie: bool
    mount: Mount
    bed_x: float
    bed_y: float
    margin: float
    new_design: bool
    ver: int


SETTINGS_VERSION = 2
"""Version written with saved settings; older files are migrated on load."""

NUT_H = 3.0
"""M3 nut slot height in mm: a 2.4 mm nut plus room for a sagging bridge."""

SIDES: tuple[Side, ...] = ("S", "E", "N", "W")
"""Frame sides in build order."""

MOUNTS: tuple[tuple[Mount, str, tuple[Side, ...]], ...] = (
    ("none", "No holders on the frame", ()),
    ("straight", "Straight run (2 opposite sides)", ("S", "N")),
    ("L", "L - turn (2 sides)", ("S", "E")),
    ("T", "T - branch (3 sides)", ("W", "S", "E")),
    ("X", "X - cross (4 sides)", ("S", "E", "N", "W")),
)
"""Mount options: key, dialog label, frame sides that get a holder."""

MOUNT_SIDES: dict[Mount, tuple[Side, ...]] = {key: sides for key, _, sides in MOUNTS}
"""Frame sides for each mount option."""

DEFAULTS: Settings = {
    "cradles": 10,
    "cable_d": 10.0,
    "tooth_w": 2.0,
    "raised_teeth": True,
    "center_pin": True,
    "depth": 12.0,
    "screw_d": 4.2,
    "screw_csk": 8.4,
    "screw_len": 20.0,
    "m3_d": 3.4,
    "nut_af": 6.0,
    "clr": 0.2,
    "frame_t": 4.0,
    "beam_w": 18.0,
    "tm_l": 36.0,
    "tm_w": 14.0,
    "tm_h": 6.5,
    "tie_w": 5.2,
    "make_holder": True,
    "make_frame": True,
    "make_tie": True,
    "mount": "X",
    "bed_x": 256.0,
    "bed_y": 256.0,
    "margin": 5.0,
    "new_design": False,
    "ver": SETTINGS_VERSION,
}
"""Settings of a fresh install."""

LIMITS: dict[str, tuple[float, float]] = {
    "cradles": (1, 15),
    "cable_d": (3.0, 25.0),
    "tooth_w": (1.2, 10.0),
    "depth": (8.0, 40.0),
    "screw_d": (2.0, 8.0),
    "screw_csk": (4.0, 16.0),
    "screw_len": (10.0, 60.0),
    "m3_d": (2.5, 5.0),
    "nut_af": (4.0, 9.0),
    "clr": (0.0, 1.0),
    "frame_t": (2.0, 12.0),
    "beam_w": (10.0, 40.0),
    "tm_l": (20.0, 80.0),
    "tm_w": (8.0, 40.0),
    "tm_h": (4.0, 20.0),
    "tie_w": (2.0, 12.0),
    "bed_x": (50.0, 1000.0),
    "bed_y": (50.0, 1000.0),
    "margin": (0.0, 30.0),
}
"""Allowed range (inclusive) of every numeric setting."""

MAX_CRADLES = int(LIMITS["cradles"][1])
"""Largest cradle count the dialog offers."""

_OLD_DEFAULT_NUT_AF = 5.8


def defaults() -> Settings:
    """Return a fresh copy of the default settings."""
    return DEFAULTS.copy()


def finite_number(value: object) -> float | None:
    """Return ``value`` as a finite float, or None.

    Booleans, strings, NaN, infinities and integers too large for a float
    are rejected, so untrusted JSON cannot smuggle them into the arithmetic.

    Args:
        value: Value from JSON.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    try:
        number = float(value)
    except OverflowError:
        return None
    return number if math.isfinite(number) else None


def migrate(raw: dict[str, Any]) -> dict[str, Any]:
    """Upgrade settings saved by an older version, in place.

    Version 1 used a 5.8 mm nut slot that is too tight for printed parts; a
    stored value equal to that old default is raised to the current one.

    Args:
        raw: Settings as read from JSON.

    Returns:
        The same dictionary, tagged with :data:`SETTINGS_VERSION`.
    """
    old_version = finite_number(raw.get("ver", 1))
    if old_version is not None and old_version < 2:
        nut_af = finite_number(raw.get("nut_af"))
        if nut_af is not None and abs(nut_af - _OLD_DEFAULT_NUT_AF) < 1e-6:
            raw["nut_af"] = DEFAULTS["nut_af"]
    raw["ver"] = SETTINGS_VERSION
    return raw


def from_mapping(raw: object, within_limits: bool = False) -> Settings:
    """Build settings from data of unknown quality, keeping well-typed known keys.

    Unknown keys are dropped and every value is checked against the type of
    its default; numbers must be finite.

    Values read back from files, designs or events pass ``within_limits``,
    so an out-of-range value (a cradle count of a billion, say) is replaced
    by the default before any arithmetic runs on it. The dialog leaves it
    off: there an out-of-range value must stay visible and be reported by
    :func:`problems`.

    Args:
        raw: Parsed JSON; anything that is not an object yields the defaults.
        within_limits: Also drop numbers outside :data:`LIMITS`.

    Returns:
        Complete settings.
    """
    result = defaults()
    if not isinstance(raw, dict):
        return result
    merged: dict[str, object] = dict(result)
    for key, default in DEFAULTS.items():
        if key not in raw:
            continue
        value = raw[key]
        if isinstance(default, bool):
            if isinstance(value, bool):
                merged[key] = value
        elif isinstance(default, int):
            if isinstance(value, int) and not isinstance(value, bool):
                if not within_limits or in_limits(key, value):
                    merged[key] = value
        elif isinstance(default, float):
            number = finite_number(value)
            if number is not None and (not within_limits or in_limits(key, number)):
                merged[key] = number
        elif key == "mount":
            if value in get_args(Mount):
                merged[key] = value
    return cast(Settings, merged)


def in_limits(key: str, value: float) -> bool:
    """Return whether a value is inside the dialog limits of its setting.

    Args:
        key: Settings key.
        value: Value to check.
    """
    if key not in LIMITS:
        return True
    lo, hi = LIMITS[key]
    return lo - 1e-9 <= value <= hi + 1e-9


def problems(s: Settings, fits_bed: bool) -> list[str]:
    """List what is wrong with the settings, in dialog wording.

    Args:
        s: Settings to check.
        fits_bed: Whether every part fits on the printer bed.

    Returns:
        Problems; empty when the settings can be built.
    """
    found = []
    values: dict[str, object] = dict(s)
    for key, (lo, hi) in LIMITS.items():
        value = values[key]
        if not isinstance(value, (int, float)):
            continue
        if not lo - 1e-9 <= value <= hi + 1e-9:  # also true for NaN
            found.append("%s must be %g...%g" % (key.replace("_", " "), lo, hi))
    if s["screw_csk"] <= s["screw_d"] + 0.5:
        found.append("countersink must be larger than the screw hole")
    if not (s["make_holder"] or s["make_frame"] or s["make_tie"]):
        found.append("choose at least one part")
    if not fits_bed:
        found.append("a part does not fit on the printer bed")
    return found
