# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Comb: the lower half of the holder with the cable cradles.

The comb is a bar with end blocks that meet the rail at the cable axis,
optional raised teeth between the cradles and an optional T-pin that hooks
into the rail's slot so a long comb cannot sag in the middle.
"""

from __future__ import annotations

from ..core.expr import neg, pitch_expr
from ..core.layout import layout
from ..core.settings import Settings
from .api import CUT, JOIN, NEW_BODY, Component, Feature, bodies
from .context import BuildContext
from .features import combine, corners, csk_holes, ext_sym, fillet, sym, y_edges, z_edges
from .sketch import ParamSketch


def build_comb(ctx: BuildContext, comp: Component, s: Settings) -> None:
    """Model the comb in ``comp``.

    Args:
        ctx: Build context; the parameters already exist.
        comp: Empty component that receives the comb.
        s: Settings.
    """
    lay = layout(s)
    ev = ctx.ev
    xy = comp.xYConstructionPlane
    sk = ParamSketch(ctx, comp, xy, "Comb bar", 0, 1)
    sk.rect("-COMB_BAR_X", neg("CABLE_Y + COMB_BOT"), "COMB_BAR_X", "-CABLE_Y")
    ext_sym(comp, sk, NEW_BODY, "DEPTH")

    sk = ParamSketch(ctx, comp, xy, "Comb end blocks", 0, 1)
    sk.rect("END_X0", neg("CABLE_Y + COMB_END_BOT"), "END_X1", "-CABLE_Y")
    sk.rect("-END_X1", neg("CABLE_Y + COMB_END_BOT"), "-END_X0", "-CABLE_Y")
    ends_feature = ext_sym(comp, sk, NEW_BODY, "DEPTH")
    ends = [ends_feature.bodies.item(i) for i in range(ends_feature.bodies.count)]
    ctx.soft(
        "Comb: end rounding",
        lambda: fillet(comp, y_edges(ends, corners(ev("END_X1"), ev("DEPTH") / 2)), "END_R"),
    )
    combine(comp, (0, -ev("CABLE_Y") - ev("COMB_BOT") / 2, 0))

    ybot = -(ev("CABLE_Y") + ev("COMB_BOT"))
    yend = -(ev("CABLE_Y") + ev("COMB_END_BOT"))
    ctx.soft(
        "Comb: step outer",
        lambda: fillet(comp, z_edges(bodies(comp), sym(ev("COMB_BAR_X"), ybot)), "COMB_STEP_R"),
    )
    ctx.soft(
        "Comb: step inner",
        lambda: fillet(comp, z_edges(bodies(comp), sym(ev("COMB_BAR_X"), yend)), "COMB_STEP_R"),
    )

    cy = ev("CABLE_Y")
    px = ev("PIN_X")
    if lay.pin:
        sk = ParamSketch(ctx, comp, xy, "Comb T-pin", 0, 1)
        sk.rect(
            "PIN_X - STEM_HW",
            neg("CABLE_Y + 1 mm"),
            "PIN_X + STEM_HW",
            neg("CABLE_Y - CB_Y0 - 0.5 mm"),
        )
        sk.rect("PIN_X - CB_HW", neg("CABLE_Y - CB_Y0"), "PIN_X + CB_HW", neg("CABLE_Y - CB_Y1"))
        ext_sym(comp, sk, JOIN, "DEPTH")

    teeth = s["raised_teeth"] and bool(lay.teeth)
    if teeth:
        sk = ParamSketch(ctx, comp, xy, "Comb teeth", 0, 1)
        for t in lay.teeth:
            center = pitch_expr(t)
            sk.rect(
                "(%s) - FIN_W / 2" % center,
                neg("CABLE_Y + 1 mm"),
                "(%s) + FIN_W / 2" % center,
                neg("CABLE_Y - FIN_H"),
            )
        ext_sym(comp, sk, JOIN, "DEPTH")

    sk = ParamSketch(ctx, comp, xy, "Comb cradles", 0, 1)
    for k in range(lay.n):
        sk.circle(pitch_expr(k - (lay.n - 1) / 2.0), "-CABLE_Y", "2 * NOTCH_R")
    ext_sym(comp, sk, CUT, "DEPTH + 2 mm")

    if lay.pin:
        sh, ch = ev("STEM_HW"), ev("CB_HW")
        y0, y1 = -(cy - ev("CB_Y0")), -(cy - ev("CB_Y1"))
        ctx.soft(
            "Comb: stem fillet",
            lambda: fillet(
                comp, z_edges(bodies(comp), [(px - sh, y0), (px + sh, y0)]), "CB_FILLET"
            ),
        )
        ctx.soft(
            "Comb: crossbar corners",
            lambda: fillet(
                comp,
                z_edges(
                    bodies(comp), [(px - ch, y0), (px + ch, y0), (px - ch, y1), (px + ch, y1)]
                ),
                "CB_EDGE_R",
            ),
        )

    if teeth:

        def tips() -> Feature:
            pitch, width, yt = ev("NOTCH_PITCH"), ev("FIN_W"), -(cy - ev("FIN_H"))
            pts = []
            for t in lay.teeth:
                pts += [(t * pitch - width / 2, yt), (t * pitch + width / 2, yt)]
            return fillet(comp, z_edges(bodies(comp), pts), "FIN_TIP_R")

        ctx.soft("Comb: teeth tips", tips)

    csk_holes(
        ctx,
        comp,
        neg("CABLE_Y + COMB_END_BOT"),
        [("M3_X", "0 mm"), ("-M3_X", "0 mm")],
        "M3_D",
        "M3_CSK",
        "CSK_ANGLE",
        "COMB_END_BOT",
        "Comb M3 holes",
    )
