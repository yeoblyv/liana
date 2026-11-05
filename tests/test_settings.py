# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Settings: defaults, migration, loading untrusted data and validation."""

from __future__ import annotations

from typing import Any

import pytest

from Liana.core.layout import fit_report
from Liana.core.settings import (
    DEFAULTS,
    LIMITS,
    MOUNT_SIDES,
    MOUNTS,
    SETTINGS_VERSION,
    defaults,
    from_mapping,
    migrate,
    problems,
)


def test_defaults_are_a_copy() -> None:
    s = defaults()
    s["cradles"] = 3
    assert DEFAULTS["cradles"] == 10


def test_defaults_are_within_limits_and_build() -> None:
    s = defaults()
    assert problems(s, fit_report(s).ok) == []


def test_every_mount_has_sides() -> None:
    assert [m for m, _, _ in MOUNTS] == list(MOUNT_SIDES)
    assert MOUNT_SIDES["X"] == ("S", "E", "N", "W")
    assert MOUNT_SIDES["none"] == ()


def test_migrate_lifts_old_tight_nut_slot() -> None:
    raw: dict[str, Any] = {"nut_af": 5.8}
    assert migrate(raw) == {"nut_af": DEFAULTS["nut_af"], "ver": SETTINGS_VERSION}


def test_migrate_keeps_custom_nut_slot_and_current_files() -> None:
    assert migrate({"nut_af": 6.3, "ver": 1})["nut_af"] == 6.3
    assert migrate({"nut_af": 5.8, "ver": 2})["nut_af"] == 5.8


def test_migrate_ignores_non_numeric_values() -> None:
    raw: dict[str, Any] = {"nut_af": "5.8", "ver": "old"}
    assert migrate(raw) == {"nut_af": "5.8", "ver": SETTINGS_VERSION}


def test_from_mapping_rejects_non_objects() -> None:
    assert from_mapping([1, 2]) == DEFAULTS
    assert from_mapping(None) == DEFAULTS


def test_from_mapping_keeps_known_well_typed_values_in_default_order() -> None:
    s = from_mapping({"mount": "T", "cradles": 4, "cable_d": 6, "make_tie": False, "extra": 1})
    assert list(s) == list(DEFAULTS)
    assert s["mount"] == "T"
    assert s["cradles"] == 4
    assert s["cable_d"] == 6.0 and isinstance(s["cable_d"], float)
    assert s["make_tie"] is False
    assert "extra" not in s


@pytest.mark.parametrize(
    "key, bad",
    [
        ("cradles", True),
        ("cradles", 4.5),
        ("cable_d", "10"),
        ("cable_d", False),
        ("make_tie", 1),
        ("mount", "Y"),
        ("mount", 3),
    ],
)
def test_from_mapping_drops_wrong_types(key: str, bad: object) -> None:
    assert from_mapping({key: bad}) == DEFAULTS


def test_problems_report_limits_and_rules() -> None:
    s = defaults()
    s["cradles"] = 16
    s["cable_d"] = 2.0
    s["screw_csk"] = s["screw_d"] + 0.5
    s["make_holder"] = s["make_frame"] = s["make_tie"] = False
    found = problems(s, fits_bed=False)
    assert found == [
        "cradles must be 1...15",
        "cable d must be 3...25",
        "countersink must be larger than the screw hole",
        "choose at least one part",
        "a part does not fit on the printer bed",
    ]


def test_limits_cover_every_numeric_setting() -> None:
    numeric = {
        k for k, v in DEFAULTS.items() if isinstance(v, (int, float)) and not isinstance(v, bool)
    } - {"ver"}
    assert numeric == set(LIMITS)


@pytest.mark.parametrize("bad", [10**400, float("nan"), float("inf"), -float("inf")])
def test_numbers_must_be_finite(bad: object) -> None:
    assert from_mapping({"nut_af": bad, "cable_d": bad}) == DEFAULTS
    assert migrate({"nut_af": bad, "ver": 1})["nut_af"] is bad
    assert migrate({"nut_af": 5.8, "ver": bad})["nut_af"] == 5.8


def test_values_read_back_must_be_within_limits() -> None:
    raw = {"cradles": 10**9, "cable_d": 40.0, "depth": 14.0}
    assert from_mapping(raw)["cradles"] == 10**9  # the dialog reports it
    checked = from_mapping(raw, within_limits=True)
    assert checked["cradles"] == DEFAULTS["cradles"]
    assert checked["cable_d"] == DEFAULTS["cable_d"]
    assert checked["depth"] == 14.0
    assert from_mapping({"ver": 7}, within_limits=True)["ver"] == 7


def test_problems_catch_nan() -> None:
    s = defaults()
    s["depth"] = float("nan")
    assert problems(s, fits_bed=True) == ["depth must be 8...40"]
