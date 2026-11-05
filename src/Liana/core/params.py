# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""User Parameters that drive every sketch dimension of a Liana system."""

from __future__ import annotations

from typing import NamedTuple

from .layout import layout
from .settings import NUT_H, Settings


class ParamSpec(NamedTuple):
    """One User Parameter.

    Attributes:
        name: Parameter name.
        expression: Fusion expression, with units.
        comment: Comment shown in Change Parameters.
    """

    name: str
    expression: str
    comment: str


ANGLE_PARAMS = frozenset({"CSK_ANGLE"})
"""Parameters measured in degrees; all others are lengths in mm."""


def fmt(value: float) -> str:
    """Format a length in mm as a Fusion expression, e.g. ``"4.2 mm"``."""
    return "%g mm" % round(float(value), 4)


def make_params(s: Settings) -> list[ParamSpec]:
    """Return the User Parameters for the settings, in dependency order.

    Values the dialog sets become plain lengths; everything else is an
    expression of other parameters, so a size changed later in Change
    Parameters propagates through the whole design.

    Args:
        s: Settings.

    Returns:
        Parameters; each one refers only to parameters listed before it.
    """
    lay = layout(s)
    n = lay.n
    return [
        # cables
        ParamSpec("CABLE_D", fmt(s["cable_d"]), "Cable diameter = cradle diameter"),
        ParamSpec("NOTCH_R", "CABLE_D / 2", "(derived) cradle radius"),
        ParamSpec("FIN_W", fmt(s["tooth_w"]), "Tooth width between cradles"),
        ParamSpec("NOTCH_PITCH", "CABLE_D + FIN_W", "(derived) cradle pitch"),
        ParamSpec("FIN_H", "NOTCH_R", "Tooth height above the cable axis"),
        ParamSpec("FIN_TIP_R", fmt(min(0.9, s["tooth_w"] / 2.0 - 0.1)), "Tooth tip round"),
        # holder body
        ParamSpec("DEPTH", fmt(s["depth"]), "Holder depth along the cable"),
        ParamSpec("PLATE_T", "3 mm", "Rail plate thickness"),
        ParamSpec("PAD_T", "4 mm", "Thickness under the screw heads"),
        ParamSpec("CEIL_GAP", "3 mm", "Gap from the cable top to the rail plate"),
        ParamSpec(
            "CABLE_Y",
            "PLATE_T + CEIL_GAP + NOTCH_R",
            "(derived) cable axis = rail/comb joint, from the table",
        ),
        ParamSpec("END_W", "10 mm", "End block width"),
        ParamSpec(
            "END_X0",
            "%g * NOTCH_PITCH + NOTCH_R" % ((n - 1) / 2.0),
            "(derived) end block inner face (%d cradles)" % n,
        ),
        ParamSpec("END_X1", "END_X0 + END_W", "(derived) end block outer face"),
        ParamSpec("EAR_X", "END_X1 + 5.5 mm", "(derived) ear screws, +-X"),
        ParamSpec("END_R", "3 mm", "Plan rounding of the ends"),
        ParamSpec("CAV_R", fmt(lay.cav_r), "Cavity upper corner round"),
        # screws
        ParamSpec("WS_D", fmt(s["screw_d"]), "Wood screw clearance hole"),
        ParamSpec("WS_CSK", fmt(s["screw_csk"]), "Wood screw countersink diameter"),
        ParamSpec("CSK_ANGLE", "90 deg", "Countersink angle"),
        ParamSpec(
            "M3_X",
            "(END_X0 + END_X1) / 2" if lay.nut_side else "(END_X0 + END_X1) / 2 + 1 mm",
            "(derived) M3 rail-to-comb screws, +-X (centered when the nut enters from the side)",
        ),
        ParamSpec("M3_D", fmt(s["m3_d"]), "M3 clearance hole"),
        ParamSpec("M3_CSK", "7 mm", "Countersink for M3 DIN 965"),
        ParamSpec("NUT_AF", fmt(s["nut_af"]), "M3 nut seat across flats (5.5 mm nut + clearance)"),
        ParamSpec(
            "NUT_Y0",
            fmt(lay.nut_y0),
            "Nut slot bottom above the joint (kept inside the end block)",
        ),
        ParamSpec("NUT_H", fmt(NUT_H), "Nut slot height (2.4 mm nut + clearance)"),
        ParamSpec("NUT_FLARE", "0.5 mm", "Nut slot mouth: extra width per side for an easy start"),
        ParamSpec("M3_CH_GAP", "1 mm", "M3 channel stops this far from the table"),
        # center T-pin
        ParamSpec("STEM_HW", fmt(lay.stem_hw), "Pin stem half-width"),
        ParamSpec("CB_HW", "STEM_HW + 1.7 mm", "(derived) pin crossbar half-width"),
        ParamSpec("CB_T", "1.9 mm", "Crossbar thickness"),
        ParamSpec("CLR_X", fmt(s["clr"]), "Slot side clearance per side"),
        ParamSpec("CLR_Y", "0.15 mm", "Slot vertical clearance"),
        ParamSpec(
            "LIP_Y0", "NOTCH_R + 0.3 mm", "(derived) slot lip underside above the cable axis"
        ),
        ParamSpec("LIP_T", "1.5 mm", "Slot lip thickness"),
        ParamSpec("NECK_HW", "STEM_HW + CLR_X", "(derived) slot neck half-width"),
        ParamSpec("HEAD_HW", "CB_HW + CLR_X", "(derived) slot head half-width"),
        ParamSpec("BOSS_HW", "HEAD_HW + 2 mm", "(derived) slot boss half-width"),
        ParamSpec("CB_Y0", "LIP_Y0 + LIP_T + CLR_Y", "(derived) crossbar bottom above the axis"),
        ParamSpec("CB_Y1", "CB_Y0 + CB_T", "(derived) crossbar top above the axis"),
        ParamSpec("SLOT_CEIL", "CB_Y1 + CLR_Y", "(derived) slot ceiling above the axis"),
        ParamSpec(
            "PIN_X",
            "0 mm" if n % 2 == 0 else "NOTCH_PITCH / 2",
            "Pin position (half a pitch off center for odd counts)",
        ),
        ParamSpec(
            "SIDE_SCREW_X", "BOSS_HW + WS_CSK / 2 + 2.6 mm", "(derived) side screws from the pin"
        ),
        ParamSpec(
            "CENTER_BLOCK_HX",
            "SIDE_SCREW_X + WS_CSK / 2 + 1.3 mm",
            "(derived) center block half-width",
        ),
        # comb
        ParamSpec(
            "COMB_END_BOT",
            "NOTCH_R" if lay.r >= 4.0 else "4 mm",
            "Comb end blocks below the cable axis",
        ),
        ParamSpec("COMB_BOT", "COMB_END_BOT + 2 mm", "(derived) comb bottom below the cable axis"),
        ParamSpec("COMB_BAR_X", "END_X0 + 2 mm", "(derived) comb bar half-length"),
        # rounds
        ParamSpec("COMB_STEP_R", "0.9 mm", "Comb step rounds"),
        ParamSpec("BOSS_R", "1 mm", "Boss bottom round"),
        ParamSpec("BOSS_ROOT_R", "1.2 mm", "Boss root round"),
        ParamSpec("BLOCK_R", "0.8 mm", "Center block rounds"),
        ParamSpec("LIP_CH", "0.5 mm", "Lip edge chamfer"),
        ParamSpec("LEAD_IN", "0.5 mm", "Slot lead-in chamfer"),
        ParamSpec("CB_FILLET", "0.4 mm", "Stem-to-crossbar round"),
        ParamSpec("CB_EDGE_R", "0.3 mm", "Crossbar corner round"),
        # X-frame
        ParamSpec("FRAME_T", fmt(s["frame_t"]), "Frame thickness"),
        ParamSpec(
            "FRAME_A", "EAR_X + DEPTH + 1.5 mm", "(derived) half-distance between opposite holders"
        ),
        ParamSpec(
            "BEAM_W", fmt(lay.bw), "Frame beam width (at least holder depth + 4.5 mm for the ribs)"
        ),
        ParamSpec("HALF_OUT", "FRAME_A + BEAM_W / 2", "(derived) half of the frame outer size"),
        ParamSpec("RIB_H", "1.5 mm", "Locating rib height"),
        ParamSpec("RIB_W", "2 mm", "Locating rib width"),
        ParamSpec("RIB_GAP", "0.25 mm", "Rib-to-holder clearance"),
        ParamSpec("RIB_LEN", "EAR_X - 2.5 mm", "(derived) half-length of the ribs"),
        ParamSpec("GUSSET", fmt(lay.gusset), "Inner corner gusset leg"),
        ParamSpec("CORNER_R", "6 mm", "Frame outer corner round"),
        ParamSpec("FRAME_Z", "300 mm", "Frame position in the design (layout only)"),
        # tie mount
        ParamSpec("TM_L", fmt(s["tm_l"]), "Tie mount: length"),
        ParamSpec("TM_W", fmt(s["tm_w"]), "Tie mount: width"),
        ParamSpec("TM_H", fmt(s["tm_h"]), "Tie mount: height"),
        ParamSpec("TIE_SLOT_W", fmt(s["tie_w"]), "Tie tunnel width"),
        ParamSpec("TIE_SLOT_T", "2 mm", "Tie tunnel height"),
        ParamSpec("TUNNEL_X", "TM_L / 2 - 7 mm", "(derived) tie tunnels at +-X"),
        ParamSpec("TUNNEL_Y0", "1.6 mm", "Tunnel wall on the table side"),
        ParamSpec("TM_EDGE_R", "1.5 mm", "Round of the edges the strap wraps around"),
        ParamSpec("TM_CORNER_R", "TM_W / 2 - 3 mm", "(derived) tie mount corner round"),
        ParamSpec("TIE_Z", "-60 mm", "Tie mount position in the design (layout only)"),
    ]
