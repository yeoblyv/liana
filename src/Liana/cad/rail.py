# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Rail: the upper half of the holder, screwed to the table.

The rail is a plate with ears for the wood screws, end blocks that meet the
comb at the cable axis, an optional boss with a T-slot for the comb's centre
pin, M3 channels and nut seats that pull the comb up.
"""

from __future__ import annotations

from ..core.expr import neg, nut_seat
from ..core.layout import layout
from ..core.settings import Settings
from .api import CUT, JOIN, NEW_BODY, Component, bodies
from .context import BuildContext
from .features import (
    chamfer,
    combine,
    corners,
    csk_holes,
    end_face_edges,
    ext_one,
    ext_sym,
    fillet,
    sym,
    y_edges,
    z_edges,
)
from .sketch import ParamSketch, plane_y


def build_rail(ctx: BuildContext, comp: Component, s: Settings) -> None:
    """Model the rail in ``comp``.

    Args:
        ctx: Build context; the parameters already exist.
        comp: Empty component that receives the rail.
        s: Settings.
    """
    lay = layout(s)
    ev = ctx.ev
    xy = comp.xYConstructionPlane
    sk = ParamSketch(ctx, comp, xy, "Rail plate", 0, 1)
    sk.rect("-EAR_X", "-PLATE_T", "EAR_X", "0 mm")
    ext_sym(comp, sk, NEW_BODY, "DEPTH")

    sk = ParamSketch(ctx, comp, comp.xZConstructionPlane, "Rail ears", 0, 2)
    sk.circle("EAR_X", "0 mm", "DEPTH")
    sk.circle("-EAR_X", "0 mm", "DEPTH")
    ext_one(
        ctx,
        comp,
        sk,
        JOIN,
        "PAD_T",
        -1,
        (ev("EAR_X") + ev("DEPTH") / 2 - 0.5, -ev("PAD_T") / 2, 0),
    )

    # the pads start inside the end blocks, so they also fill the rounded
    # end-block corners; otherwise a notch is left between the round and the ear
    sk = ParamSketch(ctx, comp, xy, "Rail pads", 0, 1)
    sk.rect("END_X1 - END_R - 1 mm", "-PAD_T", "EAR_X", "-PLATE_T")
    sk.rect("-EAR_X", "-PAD_T", "-(END_X1 - END_R - 1 mm)", "-PLATE_T")
    if lay.side:
        sk.rect("PIN_X - CENTER_BLOCK_HX", "-PAD_T", "PIN_X + CENTER_BLOCK_HX", "-PLATE_T")
    ext_sym(comp, sk, JOIN, "DEPTH")

    boss_top = "-PAD_T" if lay.side else "-PLATE_T"
    if lay.pin:
        sk = ParamSketch(ctx, comp, xy, "Rail T-boss", 0, 1)
        sk.rect("PIN_X - BOSS_HW", neg("CABLE_Y - LIP_Y0"), "PIN_X + BOSS_HW", boss_top)
        ext_sym(comp, sk, JOIN, "DEPTH")

    sk = ParamSketch(ctx, comp, xy, "Rail end blocks", 0, 1)
    sk.rect("END_X0", "-CABLE_Y", "END_X1", "-PLATE_T")
    sk.rect("-END_X1", "-CABLE_Y", "-END_X0", "-PLATE_T")
    ends_feature = ext_sym(comp, sk, NEW_BODY, "DEPTH")
    ends = [ends_feature.bodies.item(i) for i in range(ends_feature.bodies.count)]
    ctx.soft(
        "Rail: end rounding",
        lambda: fillet(comp, y_edges(ends, corners(ev("END_X1"), ev("DEPTH") / 2)), "END_R"),
    )
    combine(comp, (0, -ev("PLATE_T") / 2, 0))

    px = ev("PIN_X")
    yb = -(ev("CABLE_Y") - ev("LIP_Y0"))
    if lay.pin:
        bh = ev("BOSS_HW")
        ctx.soft(
            "Rail: boss bottom",
            lambda: fillet(comp, z_edges(bodies(comp), [(px - bh, yb), (px + bh, yb)]), "BOSS_R"),
        )
        yr = -ev("PAD_T") if lay.side else -ev("PLATE_T")
        ctx.soft(
            "Rail: boss root",
            lambda: fillet(
                comp, z_edges(bodies(comp), [(px - bh, yr), (px + bh, yr)]), "BOSS_ROOT_R"
            ),
        )
    if lay.side:
        bx = ev("CENTER_BLOCK_HX")
        ctx.soft(
            "Rail: center block",
            lambda: fillet(
                comp,
                z_edges(bodies(comp), [(px - bx, -ev("PAD_T")), (px + bx, -ev("PAD_T"))]),
                "BLOCK_R",
            ),
        )
        ctx.soft(
            "Rail: center block root",
            lambda: fillet(
                comp,
                z_edges(bodies(comp), [(px - bx, -ev("PLATE_T")), (px + bx, -ev("PLATE_T"))]),
                "BLOCK_R",
            ),
        )
    ctx.soft(
        "Rail: cavity corners",
        lambda: fillet(comp, z_edges(bodies(comp), sym(ev("END_X0"), -ev("PLATE_T"))), "CAV_R"),
    )

    if lay.pin:
        _t_slot(ctx, comp, px, yb)

    pts = [("EAR_X", "0 mm"), ("-EAR_X", "0 mm")]
    if lay.side:
        pts += [("PIN_X + SIDE_SCREW_X", "0 mm"), ("PIN_X - SIDE_SCREW_X", "0 mm")]
    csk_holes(
        ctx, comp, "-PAD_T", pts, "WS_D", "WS_CSK", "CSK_ANGLE", "PAD_T + 1 mm", "Rail screw holes"
    )

    sk = ParamSketch(ctx, comp, plane_y(ctx, comp, "-CABLE_Y"), "Rail M3 channel", 0, 2)
    sk.circle("M3_X", "0 mm", "M3_D")
    sk.circle("-M3_X", "0 mm", "M3_D")
    ext_one(ctx, comp, sk, CUT, "CABLE_Y - M3_CH_GAP", 1, (ev("M3_X"), -ev("CABLE_Y") + 0.5, 0))

    # nut seats: an entry slot with a flared mouth that ends in a half hexagon
    # centred on the screw, so the nut slides in by hand and stops on the axis
    sk = ParamSketch(
        ctx, comp, plane_y(ctx, comp, neg("CABLE_Y - NUT_Y0")), "Rail nut seats", 0, 2
    )
    for sx in (1, -1):
        sk.polygon(nut_seat(sx, lay.nut_side))
    yp = -(ev("CABLE_Y") - ev("NUT_Y0")) + ev("NUT_H") / 2
    # probe inside the seat but clear of the M3 hole, which is already empty
    probe = (ev("M3_X"), yp, -2.4) if lay.nut_side else (ev("M3_X") + 2.4, yp, 0)
    ext_one(ctx, comp, sk, CUT, "NUT_H", 1, probe)


def _t_slot(ctx: BuildContext, comp: Component, px: float, yb: float) -> None:
    """Cut the T-slot for the comb pin and chamfer its lip and mouth.

    Args:
        ctx: Build context.
        comp: Rail component.
        px: X of the pin in mm.
        yb: Y of the lip underside in mm.
    """
    ev = ctx.ev
    # neck and head; the neck reaches 0.5 mm into the head to avoid collinear edges
    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "Rail T-slot", 0, 1)
    sk.rect(
        "PIN_X - NECK_HW",
        neg("CABLE_Y - LIP_Y0 + 1 mm"),
        "PIN_X + NECK_HW",
        neg("CABLE_Y - LIP_Y0 - LIP_T - 0.5 mm"),
    )
    sk.rect(
        "PIN_X - HEAD_HW",
        neg("CABLE_Y - LIP_Y0 - LIP_T"),
        "PIN_X + HEAD_HW",
        neg("CABLE_Y - SLOT_CEIL"),
    )
    ext_sym(comp, sk, CUT, "DEPTH + 2 mm")
    yl1 = -(ev("CABLE_Y") - ev("LIP_Y0") - ev("LIP_T"))
    yce = -(ev("CABLE_Y") - ev("SLOT_CEIL"))
    nh = ev("NECK_HW")
    ctx.soft(
        "Rail: lip chamfer",
        lambda: chamfer(comp, z_edges(bodies(comp), [(px - nh, yl1), (px + nh, yl1)]), "LIP_CH"),
    )
    ctx.soft(
        "Rail: lip lead-in",
        lambda: chamfer(comp, z_edges(bodies(comp), [(px - nh, yb), (px + nh, yb)]), "0.3 mm"),
    )

    # the mouth of the slot on both end faces, so the pin finds its way in
    ctx.soft(
        "Rail: slot lead-in",
        lambda: chamfer(
            comp,
            end_face_edges(bodies(comp), ev("DEPTH") / 2, px, ev("HEAD_HW") + 0.01, yl1, yce),
            "LEAD_IN",
        ),
    )
