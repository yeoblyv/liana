# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Layout arithmetic and the User Parameters that mirror it."""

from __future__ import annotations

import math
import re
from typing import Any

import pytest

from Liana.core.layout import fit_report, layout, topology
from Liana.core.params import ANGLE_PARAMS, fmt, make_params
from Liana.core.settings import Settings, defaults, from_mapping

_NAME = re.compile(r"\b[A-Z][A-Z0-9_]*\b")


def settings(**changes: Any) -> Settings:
    """Return the defaults with some values changed."""
    return from_mapping({**defaults(), **changes})


def evaluate_params(s: Settings) -> dict[str, float]:
    """Evaluate the parameter expressions the way Fusion does (mm and deg)."""
    values: dict[str, Any] = {"sqrt": math.sqrt}
    for name, expr, _ in make_params(s):
        values[name] = float(eval(re.sub(r"\b(mm|deg)\b", "", expr), {"__builtins__": {}}, values))
    del values["sqrt"]
    return values


def test_default_layout() -> None:
    lay = layout(defaults())
    assert (lay.n, lay.r, lay.p) == (10, 5.0, 12.0)
    assert lay.end_x0 == pytest.approx(59.0)
    assert lay.ear_x == pytest.approx(74.5)
    assert lay.pin and lay.side and lay.pin_x == 0.0
    assert not lay.nut_side
    assert lay.m3_len == 12
    assert lay.holder_len == pytest.approx(161.0)
    assert lay.bw == 18.0
    assert lay.teeth == (-4.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 4.0)


def test_small_cables_enter_the_nut_from_the_side() -> None:
    assert layout(settings(cable_d=3.0)).nut_side
    assert not layout(settings(cable_d=25.0)).nut_side


def test_odd_counts_put_the_pin_next_to_the_centre() -> None:
    lay = layout(settings(cradles=5))
    assert lay.pin and lay.pin_x == pytest.approx(lay.p / 2)
    assert all(abs(t * lay.p - lay.pin_x) > 1e-6 for t in lay.teeth)


def test_no_pin_below_four_cradles_and_one_cradle_has_no_teeth() -> None:
    assert not layout(settings(cradles=3)).pin
    assert layout(settings(cradles=1)).teeth == ()


def test_beam_widens_for_deep_holders() -> None:
    s = settings(depth=20.0)
    assert layout(s).bw == pytest.approx(24.5)
    assert "Beam widened to 24.5 mm" in fit_report(s).lines[-1]


def test_fit_report_on_a_small_bed() -> None:
    s = settings(bed_x=120.0, bed_y=120.0)
    report = fit_report(s)
    assert not report.ok
    assert report.lines[0].endswith("DOES NOT FIT")
    assert 0 < report.max_cradles < 10
    assert fit_report(settings(bed_x=50.0, bed_y=50.0)).max_cradles == 0


def test_long_rail_fits_diagonally() -> None:
    s = settings(cradles=12, make_frame=False, bed_x=170.0, bed_y=170.0)
    report = fit_report(s)
    assert report.ok
    assert report.lines == ["Holder rail: %.0f x 12 mm - fits diagonally" % layout(s).holder_len]


def test_topology_ignores_sizes_but_not_layout() -> None:
    base = topology(defaults())
    assert topology(settings(cable_d=11.0, depth=14.0)) == base
    assert topology(settings(cradles=6)) != base
    assert topology(settings(mount="T")) != base
    assert topology(settings(mount="T", make_frame=False))[-1] == "none"


def test_fmt() -> None:
    assert fmt(4.2) == "4.2 mm"
    assert fmt(6) == "6 mm"
    assert fmt(1 / 3) == "0.3333 mm"


@pytest.mark.parametrize("cradles", [1, 2, 4, 5, 10, 15])
@pytest.mark.parametrize("cable_d", [3.0, 10.0, 25.0])
def test_parameters_are_in_dependency_order(cradles: int, cable_d: float) -> None:
    seen: set[str] = set()
    for name, expr, comment in make_params(settings(cradles=cradles, cable_d=cable_d)):
        refs = set(_NAME.findall(expr))
        assert refs <= seen, "%s uses %s before it exists" % (name, refs - seen)
        assert comment
        seen.add(name)
    assert ANGLE_PARAMS <= seen


@pytest.mark.parametrize("cradles", [1, 5, 10, 15])
@pytest.mark.parametrize("cable_d", [3.0, 10.0, 25.0])
def test_parameters_match_the_layout(cradles: int, cable_d: float) -> None:
    s = settings(cradles=cradles, cable_d=cable_d)
    lay = layout(s)
    v = evaluate_params(s)
    assert v["END_X0"] == pytest.approx(lay.end_x0)
    assert v["END_X1"] == pytest.approx(lay.end_x1)
    assert v["EAR_X"] == pytest.approx(lay.ear_x)
    assert v["CABLE_Y"] == pytest.approx(lay.cable_y)
    assert v["M3_X"] == pytest.approx(lay.m3_x)
    assert v["PIN_X"] == pytest.approx(lay.pin_x)
    assert v["BOSS_HW"] == pytest.approx(lay.boss_hw)
    assert v["SIDE_SCREW_X"] == pytest.approx(lay.side_x)
    assert v["CENTER_BLOCK_HX"] == pytest.approx(lay.block_hx)
    assert v["FRAME_A"] == pytest.approx(lay.a)
    assert v["COMB_END_BOT"] == pytest.approx(lay.comb_end_bot)
    assert 2 * v["HALF_OUT"] == pytest.approx(lay.frame_out)
