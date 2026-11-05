# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Tie mount: a small pad with two zip-tie tunnels and one screw.

The tie mount is modelled around ``(0, 0, TIE_Z)`` in its own component with
the occurrence at identity, so its tunnels can never cut the holder or the
frame.
"""

from __future__ import annotations

from ..core.expr import neg
from ..core.settings import Settings
from .api import CUT, NEW_BODY, Component, bodies
from .context import BuildContext
from .features import chamfer, csk_holes, ext_one, ext_sym, face_edges_at_y, fillet, y_edges
from .sketch import ParamSketch, plane_z


def _z(e: str) -> str:
    """Shift a Z expression into the tie mount's region of the design."""
    return "(%s) + TIE_Z" % e


def build_tie(ctx: BuildContext, comp: Component, s: Settings) -> None:
    """Model the tie mount in ``comp``.

    Args:
        ctx: Build context; the parameters already exist.
        comp: Empty component that receives the tie mount.
        s: Settings (the sizes come from the parameters).
    """
    ev = ctx.ev
    tz = ev("TIE_Z")
    l2, w2 = ev("TM_L") / 2, ev("TM_W") / 2
    sk = ParamSketch(ctx, comp, comp.xZConstructionPlane, "Tie mount base", 0, 2)
    sk.rect("-TM_L / 2", _z("-TM_W / 2"), "TM_L / 2", _z("TM_W / 2"))
    ext_one(ctx, comp, sk, NEW_BODY, "TM_H", -1, (l2 - 2, -ev("TM_H") / 2, tz))
    outer = [(sx * l2, tz + sz * w2) for sx in (1, -1) for sz in (1, -1)]
    ctx.soft("Tie: corners", lambda: fillet(comp, y_edges(bodies(comp), outer), "TM_CORNER_R"))
    ctx.soft(
        "Tie: strap edges",
        lambda: fillet(comp, face_edges_at_y(bodies(comp), -ev("TM_H")), "TM_EDGE_R"),
    )
    # a small chamfer on the bed side compensates the first-layer squish
    ctx.soft(
        "Tie: elephant foot",
        lambda: chamfer(comp, face_edges_at_y(bodies(comp), 0.0), "0.4 mm"),
    )

    sk = ParamSketch(ctx, comp, plane_z(comp, "TIE_Z"), "Tie tunnels", 0, 1)
    for sign in (1, -1):
        a, b = "TUNNEL_X - TIE_SLOT_W / 2", "TUNNEL_X + TIE_SLOT_W / 2"
        u0, u1 = (a, b) if sign > 0 else (neg(b), neg(a))
        sk.rect(u0, neg("TUNNEL_Y0 + TIE_SLOT_T"), u1, "-TUNNEL_Y0")
    ext_sym(comp, sk, CUT, "TM_W + 2 mm")

    csk_holes(
        ctx,
        comp,
        "-TM_H",
        [("0 mm", "TIE_Z")],
        "WS_D",
        "WS_CSK",
        "CSK_ANGLE",
        "TM_H + 1 mm",
        "Tie mount screw",
    )
