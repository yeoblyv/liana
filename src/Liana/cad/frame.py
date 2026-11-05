# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""X-frame: a square frame that carries holders on up to four sides.

The frame is modelled around ``(0, 0, FRAME_Z)`` in its own component with
the occurrence at identity, so no frame feature can reach the holder or the
tie mount, at build time or on any later recompute.
"""

from __future__ import annotations

from ..core.expr import holder_hole_exprs, member_coords, sgn
from ..core.layout import layout
from ..core.settings import SIDES, Settings
from .api import CUT, JOIN, NEW_BODY, Component, bodies
from .context import BuildContext
from .features import Vec3, csk_holes, ext_one, fillet, y_edges
from .sketch import ParamSketch, plane_y


def _z(e: str) -> str:
    """Shift a Z expression into the frame's region of the design."""
    return "(%s) + FRAME_Z" % e


def build_frame(ctx: BuildContext, comp: Component, s: Settings) -> None:
    """Model the frame in ``comp``.

    Args:
        ctx: Build context; the parameters already exist.
        comp: Empty component that receives the frame.
        s: Settings.
    """
    ev = ctx.ev
    xz = comp.xZConstructionPlane
    ft = ev("FRAME_T")
    fz = ev("FRAME_Z")
    first = True

    def extrude(sk: ParamSketch, probe: Vec3) -> None:
        # the first member makes the body, the others join it
        nonlocal first
        ext_one(ctx, comp, sk, NEW_BODY if first else JOIN, "FRAME_T", -1, probe)
        first = False

    for side in SIDES:
        u0, v0, u1, v1 = member_coords(side, "BEAM_W", "HALF_OUT")
        probe = ((ev(u0) + ev(u1)) / 2, -ft / 2, fz + (ev(v0) + ev(v1)) / 2)
        sk = ParamSketch(ctx, comp, xz, "Frame beam " + side, 0, 2)
        sk.rect(u0, _z(v0), u1, _z(v1))
        extrude(sk, probe)

    for sx in (1, -1):
        for sz in (1, -1):
            uc = sgn(sx, "FRAME_A - BEAM_W / 2")
            vc = sgn(sz, "FRAME_A - BEAM_W / 2")
            ue = sgn(sx, "FRAME_A - BEAM_W / 2 - GUSSET")
            ve = sgn(sz, "FRAME_A - BEAM_W / 2 - GUSSET")
            probe = ((2 * ev(uc) + ev(ue)) / 3, -ft / 2, fz + (2 * ev(vc) + ev(ve)) / 3)
            sk = ParamSketch(ctx, comp, xz, "Frame gusset", 0, 2)
            sk.right_triangle(uc, _z(vc), ue, _z(ve))
            extrude(sk, probe)

    half = ev("HALF_OUT")
    outer = [(sx * half, fz + sz * half) for sx in (1, -1) for sz in (1, -1)]
    ctx.soft(
        "Frame: outer corners",
        lambda: fillet(comp, y_edges(bodies(comp), outer), "CORNER_R"),
    )

    _ribs(ctx, comp, ft, fz)

    # through holes for the holder screws on every side (the screw goes holder,
    # frame, table); exactly the frame thickness deep, so they never touch a
    # holder mounted under the frame
    sk = ParamSketch(ctx, comp, xz, "Frame holder screw holes", 0, 2)
    holes = holder_hole_exprs(layout(s).side, ev)
    for side in SIDES:
        k = 1 if side in ("S", "E") else -1
        line = sgn(k, "FRAME_A")
        for pos in holes:
            if side in ("S", "N"):
                sk.circle(pos, _z(line), "WS_D")
            else:
                sk.circle(line, _z(pos), "WS_D")
    ext_one(ctx, comp, sk, CUT, "FRAME_T", -1, (ev("EAR_X"), -ft / 2, fz + ev("FRAME_A")))

    pts = [(sgn(sx, "FRAME_A"), _z(sgn(sz, "FRAME_A"))) for sx in (1, -1) for sz in (1, -1)]
    csk_holes(
        ctx,
        comp,
        "-FRAME_T",
        pts,
        "WS_D",
        "WS_CSK",
        "CSK_ANGLE",
        "FRAME_T + 1 mm",
        "Frame corner screws",
    )


def _ribs(ctx: BuildContext, comp: Component, ft: float, fz: float) -> None:
    """Add the locating ribs that keep a holder square under every side."""
    ev = ctx.ev
    sk = ParamSketch(ctx, comp, plane_y(ctx, comp, "-FRAME_T"), "Frame ribs", 0, 2)
    near, far = "(DEPTH) / 2 + RIB_GAP", "(DEPTH) / 2 + RIB_GAP + RIB_W"
    probe: Vec3 | None = None
    for side in SIDES:
        k = 1 if side in ("S", "E") else -1
        for b0, b1 in (
            ("(FRAME_A) + (%s)" % near, "(FRAME_A) + (%s)" % far),
            ("(FRAME_A) - (%s)" % far, "(FRAME_A) - (%s)" % near),
        ):
            c0, c1 = sgn(k, b0), sgn(k, b1)
            lo, hi = (c0, c1) if ev(c0) < ev(c1) else (c1, c0)
            mid = (ev(lo) + ev(hi)) / 2
            if side in ("S", "N"):
                sk.rect("-RIB_LEN", _z(lo), "RIB_LEN", _z(hi))
                rib_probe = (0.0, -ft - ev("RIB_H") / 2, fz + mid)
            else:
                sk.rect(lo, _z("-RIB_LEN"), hi, _z("RIB_LEN"))
                rib_probe = (mid, -ft - ev("RIB_H") / 2, fz)
            probe = probe or rib_probe
    assert probe is not None  # SIDES is never empty
    ext_one(ctx, comp, sk, JOIN, "RIB_H", -1, probe)
