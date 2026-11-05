# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Build scenarios whose Fusion API traces are pinned by golden files.

Each case names the settings to apply on top of the defaults, the switches of
the fake API, and a scenario:

- ``build``: generate into an empty hybrid design.
- ``part_active``: the active design is a Part design, so a new one is made.
- ``busy_active``: the active design already holds a sketch.
- ``update``: build, then generate again with ``second`` settings on the same
  design (same layout, so parameters are updated in place).
- ``rebuild``: as ``update`` but the layout changes, so the system is rebuilt.
- ``new_flag``: build, then generate again with ``new_design`` set.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Case:
    """One golden scenario."""

    name: str
    settings: dict[str, Any] = field(default_factory=dict)
    scenario: str = "build"
    second: dict[str, Any] = field(default_factory=dict)
    fail_first_direction: bool = False
    point_constraints: bool = True
    hole_feature_broken: bool = False


def _cases() -> list[Case]:
    cases = [Case("n%02d" % n, {"cradles": n}) for n in range(1, 16)]
    cases += [Case("n%02d_no_pin" % n, {"cradles": n, "center_pin": False}) for n in (4, 5, 9)]
    cases += [
        Case("cable6_n7", {"cable_d": 6.0, "tooth_w": 1.6, "cradles": 7}),
        Case("cable16_n5_t", {"cable_d": 16.0, "cradles": 5, "mount": "T"}),
        Case("cable3_n15", {"cable_d": 3.0, "cradles": 15}),
        Case("cable25_n2", {"cable_d": 25.0, "cradles": 2}),
        Case("cable6_n1", {"cable_d": 6.0, "cradles": 1}),
        Case("flat_teeth", {"raised_teeth": False}),
        Case("no_frame", {"make_frame": False}),
        Case("no_holder", {"make_holder": False}),
        Case("no_tie", {"make_tie": False}),
        Case("mount_none", {"mount": "none"}),
        Case("mount_straight", {"mount": "straight"}),
        Case("mount_l", {"mount": "L"}),
        Case("depth14", {"depth": 14.0}),
        Case("wide_teeth", {"tooth_w": 4.0, "cradles": 6}),
        Case("fail_first", {}, fail_first_direction=True),
        Case("fail_first_cable6_n1", {"cable_d": 6.0, "cradles": 1}, fail_first_direction=True),
        Case("hole_fallback", {}, hole_feature_broken=True),
        Case("no_point_constraints", {}, point_constraints=False),
        Case("part_active", {}, scenario="part_active"),
        Case("busy_active", {}, scenario="busy_active"),
        Case("update", {}, scenario="update", second={"cable_d": 11.0, "depth": 14.0}),
        Case(
            "update_cable6_n1",
            {"cable_d": 6.0, "cradles": 1},
            scenario="update",
            second={"cable_d": 7.0},
        ),
        Case("rebuild", {}, scenario="rebuild", second={"cradles": 6}),
        Case("new_flag", {}, scenario="new_flag", second={"new_design": True}),
    ]
    return cases


CASES = _cases()
