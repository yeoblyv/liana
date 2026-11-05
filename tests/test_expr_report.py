# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Expression builders, outlines and the texts shown to the user."""

from __future__ import annotations

import math
import re
from typing import Any

import pytest

from Liana.core.expr import diff, holder_hole_exprs, member_coords, neg, nut_seat, pitch_expr, sgn
from Liana.core.params import make_params
from Liana.core.report import BuildLog, log_text, result_message, summary_html
from Liana.core.settings import Settings, defaults, from_mapping


def settings(**changes: Any) -> Settings:
    """Return the defaults with some values changed."""
    return from_mapping({**defaults(), **changes})


def evaluator(s: Settings) -> Any:
    """Return a function that evaluates expressions against the parameters of ``s``."""
    names: dict[str, Any] = {"sqrt": math.sqrt}
    unit = re.compile(r"\b(mm|deg)\b")
    for name, expr, _ in make_params(s):
        names[name] = float(eval(unit.sub("", expr), {"__builtins__": {}}, names))

    def ev(expr: str) -> float:
        return float(eval(unit.sub("", expr), {"__builtins__": {}}, names))

    return ev


def test_small_builders() -> None:
    assert neg("A") == "-(A)"
    assert sgn(1, "A") == "A" and sgn(-1, "A") == "-(A)"
    assert diff("A", "B") == "(A) - (B)"
    assert pitch_expr(0.0) == "0 mm"
    assert pitch_expr(-1.5) == "-1.5 * NOTCH_PITCH"


@pytest.mark.parametrize("side", [True, False])
def test_nut_seats_mirror_and_end_in_a_half_hexagon(side: bool) -> None:
    ev = evaluator(defaults())
    right = [(ev(u), ev(v)) for u, v in nut_seat(1, side)]
    left = [(ev(u), ev(v)) for u, v in nut_seat(-1, side)]
    assert len(right) == 9
    assert [c for p in left for c in p] == pytest.approx([c for x, z in right for c in (-x, z)])
    m3_x, af = ev("M3_X"), ev("NUT_AF")
    # the tip of the half hexagon sits one circumradius from the screw axis
    tip = (m3_x, af / math.sqrt(3)) if side else (m3_x - af / math.sqrt(3), 0.0)
    assert right[5] == pytest.approx(tip)


def test_member_coords_of_opposite_sides_mirror() -> None:
    ev = evaluator(defaults())
    s_rect = [ev(e) for e in member_coords("S", "BEAM_W", "HALF_OUT")]
    n_rect = [ev(e) for e in member_coords("N", "BEAM_W", "HALF_OUT")]
    e_rect = [ev(e) for e in member_coords("E", "BEAM_W", "HALF_OUT")]
    assert s_rect[1] < s_rect[3] and n_rect[1] < n_rect[3]
    assert n_rect[1] == pytest.approx(-s_rect[3])
    assert e_rect == pytest.approx([s_rect[1], s_rect[0], s_rect[3], s_rect[2]])


def test_holder_holes_include_mirrored_side_screws_once() -> None:
    ev = evaluator(settings(cradles=5))
    holes = holder_hole_exprs(True, ev)
    values = [round(ev(h), 6) for h in holes]
    assert len(values) == len(set(values)) == 6
    assert holder_hole_exprs(False, ev) == ["EAR_X", "-EAR_X"]
    even = evaluator(defaults())
    assert len(holder_hole_exprs(True, even)) == 4  # mirrored screws coincide


def test_summary_for_defaults() -> None:
    html = summary_html(defaults(), [], editing=False)
    assert html.startswith("<b>10 cradles</b> for 10.0 mm cables, pitch 12.0 mm")
    assert "T-pin at the center, 4 table screws" in html
    assert "2 x M3x12 DIN 965" in html
    assert "use longer screws" not in html


def test_summary_marks_editing_short_screws_thin_teeth_and_problems() -> None:
    s = settings(cradles=1, screw_len=12.0, cable_d=25.0, tooth_w=2.0)
    html = summary_html(s, ["choose at least one part"], editing=True)
    assert html.startswith("<b>Editing the system in this design.</b>")
    assert "<b>1 cradle</b>" in html and "no T-pin, 2 table screws" in html
    assert "use longer screws" in html
    assert "Note: teeth are thin" in html
    assert html.endswith("<b>! choose at least one part</b>")
    assert "Editing" not in summary_html(settings(new_design=True), [], editing=True)


def test_summary_without_holder_or_with_odd_pin() -> None:
    html = summary_html(settings(make_holder=False, make_frame=False), [], editing=False)
    assert "Hardware - tie mount: 1 screw" in html and "Screw in the wood" not in html
    assert "tooth next to the center" in summary_html(settings(cradles=5), [], editing=False)


def test_log_text_lists_every_section() -> None:
    log = BuildLog(hard=["Rail:\nboom"], soft=["Rail: x"], dims=["d"], aligned=["a", "b"])
    text = log_text("built in this design", defaults(), log)
    assert text.splitlines()[:3] == [
        "Liana build log",
        "mode: built in this design",
        "cradles=10 cable=10.0 pitch=12.0 pin=True side_screws=True",
    ]
    assert "ERRORS (part not finished): 1\nRail:\nboom\n" in text
    assert "explicit constraint): 2\na\nb\n" in text
    assert text.endswith("\n")


def test_result_message() -> None:
    clean = result_message("built in this design", BuildLog(), "/tmp/log.txt")
    assert clean.startswith("Liana: system built in this design.\n\nSizes stay editable")
    log = BuildLog(hard=["Rail:\nTraceback\nRuntimeError: no"], soft=["x"])
    msg = result_message("rebuilt in this design", log, "/tmp/log.txt")
    assert "Parts not finished: 1\nSkipped features: 1\nSkipped sketch dimensions: 0" in msg
    assert "\n\nRuntimeError: no\n\nLog: /tmp/log.txt" in msg
    assert "Log:" not in result_message("x", log, "")


def test_build_log_clear() -> None:
    log = BuildLog(hard=["a"], soft=["b"], dims=["c"], aligned=["d"])
    assert log.has_problems
    log.clear()
    assert log == BuildLog() and not log.has_problems
