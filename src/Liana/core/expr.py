# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Builders for Fusion parameter expressions and the outlines drawn with them.

Every sketch coordinate is an expression of User Parameters rather than a
number, so the design follows a parameter change without running Liana again.
"""

from __future__ import annotations

from collections.abc import Callable

from .settings import Side

Outline = list[tuple[str, str]]
"""Closed polygon as ``(u, v)`` expression pairs."""


def neg(e: str) -> str:
    """Return the negated expression."""
    return "-(%s)" % e


def sgn(sign: int, e: str) -> str:
    """Return ``e`` for a positive sign and its negation otherwise."""
    return e if sign > 0 else neg(e)


def diff(a: str, b: str) -> str:
    """Return the expression ``a - b``."""
    return "(%s) - (%s)" % (a, b)


def pitch_expr(t: float) -> str:
    """Return ``t`` cradle pitches from the center as an expression.

    Args:
        t: Offset in pitches; may be fractional.

    Returns:
        ``"0 mm"`` for zero, otherwise ``"<t> * NOTCH_PITCH"``.
    """
    if abs(t) < 1e-9:
        return "0 mm"
    return "%g * NOTCH_PITCH" % t


def nut_seat(sx: int, side: bool) -> Outline:
    """Return the outline of one M3 nut seat at ``x = sx * M3_X``.

    The seat is an entry slot with a flared mouth that ends in a half hexagon
    centered on the screw, so the nut slides in by hand, stops on the screw
    axis and cannot turn.

    Args:
        sx: ``1`` for the seat at +X, ``-1`` for the one at -X.
        side: The slot opens to the -Z face (low end blocks) when true,
            otherwise to the end face at +-X.

    Returns:
        Vertices with ``u`` along X and ``v`` along Z.
    """

    def x(e: str) -> str:
        return "(%s)" % e if sx > 0 else "-(%s)" % e

    c, w, f = "M3_X", "NUT_AF / 2", "NUT_AF / 2 + NUT_FLARE"
    # half hexagon: where the flanks start, and the tip
    h1, h2 = "NUT_AF / (2 * sqrt(3))", "NUT_AF / sqrt(3)"
    if side:
        out, face = "-(DEPTH / 2 + 2 mm)", "-(DEPTH / 2)"
        inner = "-(DEPTH / 2) + 1.5 mm"
        pts = [
            ("%s - (%s)" % (c, f), out),
            ("%s + %s" % (c, f), out),
            ("%s + %s" % (c, f), face),
            ("%s + %s" % (c, w), inner),
            ("%s + %s" % (c, w), h1),
            (c, h2),
            ("%s - (%s)" % (c, w), h1),
            ("%s - (%s)" % (c, w), inner),
            ("%s - (%s)" % (c, f), face),
        ]
        return [(x(u), v) for u, v in pts]
    # slot along X towards the end face: flats on the +-Z walls, half hexagon towards the center
    out, face, inner = "END_X1 + 2 mm", "END_X1", "END_X1 - 1.5 mm"
    pts = [
        (out, "-(%s)" % f),
        (out, f),
        (face, f),
        (inner, w),
        ("%s - %s" % (c, h1), w),
        ("%s - %s" % (c, h2), "0 mm"),
        ("%s - %s" % (c, h1), "-(%s)" % w),
        (inner, "-(%s)" % w),
        (face, "-(%s)" % f),
    ]
    return [(x(u), v) for u, v in pts]


def member_coords(side: Side, width: str, half_len: str) -> tuple[str, str, str, str]:
    """Return the rectangle of one frame beam as ``(u0, v0, u1, v1)``.

    Args:
        side: Frame side; S and N beams run along X, E and W along Z.
        width: Beam width expression.
        half_len: Half of the beam length.

    Returns:
        Opposite corners with ``u`` along X and ``v`` along Z, relative to
        the frame center.
    """
    a_expr = "FRAME_A"
    w2 = "(%s) / 2" % width
    k = 1 if side in ("S", "E") else -1
    a, b = sgn(k, diff(a_expr, w2)), sgn(k, "(%s) + (%s)" % (a_expr, w2))
    lo, hi = (a, b) if k > 0 else (b, a)
    if side in ("S", "N"):
        return neg(half_len), lo, half_len, hi
    return lo, neg(half_len), hi, half_len


def holder_hole_exprs(side_screws: bool, ev: Callable[[str], float]) -> list[str]:
    """Return the holder screw positions along the holder axis.

    The frame gets a hole under every holder screw for both orientations of
    the holder, so the side screws are mirrored; mirrored positions that
    coincide with an existing hole are dropped.

    Args:
        side_screws: Whether the holder has side screws next to the pin.
        ev: Evaluates an expression to millimeters.

    Returns:
        X expressions of the holes.
    """
    out = [("EAR_X", ev("EAR_X")), ("-EAR_X", -ev("EAR_X"))]
    if side_screws:
        for e in (
            "PIN_X + SIDE_SCREW_X",
            "PIN_X - SIDE_SCREW_X",
            "-(PIN_X + SIDE_SCREW_X)",
            "-(PIN_X - SIDE_SCREW_X)",
        ):
            v = ev(e)
            if all(abs(v - w) > 0.01 for _, w in out):
                out.append((e, v))
    return [e for e, _ in out]
