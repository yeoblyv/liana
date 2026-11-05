# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Layout arithmetic shared by the dialog and the builders; no Fusion calls.

Every value mirrors a User Parameter expression in :mod:`.params`, so the
dialog can report sizes and printer-bed fit before anything is built.
Coordinates: table face at Y = 0, parts hang below it (-Y), X along the
holder, Z along the cable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import NamedTuple

from .settings import MAX_CRADLES, NUT_H, Mount, Settings

END_W = 10.0
"""End block width in mm (``END_W`` parameter)."""

EAR_OFFSET = 5.5
"""Ear screw distance from the end block outer face in mm."""

PLATE_T = 3.0
"""Rail plate thickness in mm."""

CEIL_GAP = 3.0
"""Gap from the cable top to the rail plate in mm."""

PAD_T = 4.0
"""Rail thickness under the screw heads in mm."""

STANDARD_M3_LENGTHS = (6, 8, 10, 12, 14, 16, 18, 20, 25, 30)
"""Stock lengths of M3 DIN 965 countersunk screws in mm."""


@dataclass(frozen=True)
class Layout:
    """Sizes derived from the settings, in millimetres.

    Attributes:
        n: Cradles per holder.
        r: Cradle radius.
        p: Cradle pitch (cable diameter + tooth width).
        end_x0: Inner face of the end blocks (+-X).
        end_x1: Outer face of the end blocks.
        ear_x: Ear screws (+-X).
        stem_hw: Half-width of the T-pin stem.
        boss_hw: Half-width of the rail boss around the T-slot.
        side_x: Side screws, measured from the pin.
        block_hx: Half-width of the rail centre block.
        pin: Whether the comb has a centre T-pin.
        pin_x: X of the pin (half a pitch off centre for odd counts).
        side: Whether the side screws next to the pin fit.
        cav_r: Round of the rail cavity upper corners.
        a: Half-distance between opposite holders on the frame.
        bw: Frame beam width (widened when the holder needs it).
        m3_x: Rail-to-comb M3 screws (+-X).
        frame_out: Outer size of the square frame.
        holder_len: Overall rail length.
        comb_len: Overall comb length.
        cable_y: Depth of the cable axis (rail/comb joint) below the table.
        comb_end_bot: Comb end blocks below the cable axis.
        bite_holder: Wood screw engagement in the table, holder alone.
        nut_y0: Nut slot bottom above the joint.
        nut_side: Whether the nut enters from the side (low end blocks).
        bite_frame: Wood screw engagement, holder on the frame.
        m3_len: Stock M3 length that fits, or None.
        teeth: Raised teeth positions in pitches from the centre.
        gusset: Leg of the frame inner corner gussets.
    """

    n: int
    r: float
    p: float
    end_x0: float
    end_x1: float
    ear_x: float
    stem_hw: float
    boss_hw: float
    side_x: float
    block_hx: float
    pin: bool
    pin_x: float
    side: bool
    cav_r: float
    a: float
    bw: float
    m3_x: float
    frame_out: float
    holder_len: float
    comb_len: float
    cable_y: float
    comb_end_bot: float
    bite_holder: float
    nut_y0: float
    nut_side: bool
    bite_frame: float
    m3_len: int | None
    teeth: tuple[float, ...]
    gusset: float


def layout(s: Settings) -> Layout:
    """Compute the layout for a set of settings.

    Args:
        s: Settings; lengths in mm.

    Returns:
        The derived sizes.
    """
    n = int(s["cradles"])
    r = s["cable_d"] / 2.0
    p = s["cable_d"] + s["tooth_w"]
    end_x0 = (n - 1) / 2.0 * p + r
    end_x1 = end_x0 + END_W
    ear_x = end_x1 + EAR_OFFSET
    stem_hw = max(1.3, s["tooth_w"] / 2.0 + 0.3)
    head_hw = stem_hw + 1.7 + s["clr"]
    boss_hw = head_hw + 2.0
    side_x = boss_hw + s["screw_csk"] / 2.0 + 2.6
    block_hx = side_x + s["screw_csk"] / 2.0 + 1.3
    pin = bool(s["center_pin"]) and n >= 4
    pin_x = 0.0 if n % 2 == 0 else p / 2.0
    side = pin and abs(pin_x) + block_hx <= end_x0 - 6.0
    used = (abs(pin_x) + boss_hw) if pin else 0.0
    cable_y = PLATE_T + CEIL_GAP + r
    block_h = PLATE_T + r  # rail end block height: joint plane to plate underside
    cav_r = max(1.0, min(6.0, (end_x0 - used) * 0.45, (block_h - 0.5) * 0.8))
    # the nut slot stays inside the end block, 0.6 mm under the plate
    nut_y0 = max(1.0, min(2.8, block_h - 0.6 - NUT_H))
    # the slot opens to the end face only if it passes under the ear pad,
    # otherwise the nut goes in from the side
    nut_side = (cable_y - nut_y0 - NUT_H) < PAD_T + 0.4
    # a side-entry seat needs walls on both sides; an end-entry one sits nearer the end face
    m3_x = (end_x0 + end_x1) / 2.0 + (0.0 if nut_side else 1.0)
    a = ear_x + s["depth"] + 1.5
    # the beam carries the holder plus a locating rib (0.25 mm gap + 2 mm) on each side
    bw = max(s["beam_w"], s["depth"] + 2.0 * (0.25 + 2.0))
    comb_end_bot = r if r >= 4.0 else 4.0
    head_sink = (s["screw_csk"] - 7.0) / 2.0 if s["screw_csk"] > 7.0 else 0.0
    bite_holder = s["screw_len"] - (PAD_T - head_sink)
    # M3: from a flush head at the comb end bottom to past the nut, short of the table
    m3_min = comb_end_bot + nut_y0 + 2.4 + 0.5
    m3_max = comb_end_bot + cable_y - 1.0
    teeth = [(k - (n - 2) / 2.0) for k in range(n - 1)] if n >= 2 else []
    if pin:
        teeth = [t for t in teeth if abs(t * p - pin_x) > 1e-6]
    return Layout(
        n=n,
        r=r,
        p=p,
        end_x0=end_x0,
        end_x1=end_x1,
        ear_x=ear_x,
        stem_hw=stem_hw,
        boss_hw=boss_hw,
        side_x=side_x,
        block_hx=block_hx,
        pin=pin,
        pin_x=pin_x,
        side=side,
        cav_r=cav_r,
        a=a,
        bw=bw,
        m3_x=m3_x,
        frame_out=2.0 * (a + bw / 2.0),
        holder_len=2.0 * (ear_x + s["depth"] / 2.0),
        comb_len=2.0 * end_x1,
        cable_y=cable_y,
        comb_end_bot=comb_end_bot,
        bite_holder=bite_holder,
        nut_y0=nut_y0,
        nut_side=nut_side,
        bite_frame=bite_holder - s["frame_t"],
        m3_len=next((L for L in STANDARD_M3_LENGTHS if m3_min <= L <= m3_max), None),
        teeth=tuple(teeth),
        gusset=min(16.0, (a - bw / 2.0) * 0.6),
    )


class FitReport(NamedTuple):
    """Printer bed check.

    Attributes:
        ok: Whether every enabled part fits.
        lines: One summary line per part.
        max_cradles: Largest cradle count that still fits (0 if none).
    """

    ok: bool
    lines: list[str]
    max_cradles: int


def fit_report(s: Settings) -> FitReport:
    """Check the enabled parts against the printer bed.

    The rail may lie diagonally; the frame is square and must fit the short
    side of the bed.

    Args:
        s: Settings including the bed size and margin.

    Returns:
        The fit report.
    """
    lay = layout(s)
    bx, by, margin = s["bed_x"], s["bed_y"], s["margin"]
    usable_min = min(bx, by) - 2 * margin
    usable_max = max(bx, by) - 2 * margin
    diag = math.hypot(bx - 2 * margin, by - 2 * margin)
    ok = True
    lines = []
    if s["make_holder"]:
        fits = lay.holder_len <= usable_max
        fits_diag = lay.holder_len <= diag - 2 * s["depth"]
        verdict = "fits" if fits else ("fits diagonally" if fits_diag else "DOES NOT FIT")
        ok = ok and (fits or fits_diag)
        lines.append("Holder rail: %.0f x %.0f mm - %s" % (lay.holder_len, s["depth"], verdict))
    if s["make_frame"]:
        fits = lay.frame_out <= usable_min
        ok = ok and fits
        lines.append(
            "X-frame: %.0f x %.0f mm - %s"
            % (lay.frame_out, lay.frame_out, "fits" if fits else "DOES NOT FIT")
        )
        if lay.bw > s["beam_w"] + 1e-6:
            lines.append(
                "Beam widened to %.1f mm to fit the holder and its locating ribs" % lay.bw
            )
    max_n = 0
    for n in range(MAX_CRADLES, 0, -1):
        trial = s.copy()
        trial["cradles"] = n
        tl = layout(trial)
        good = True
        if s["make_frame"] and tl.frame_out > usable_min:
            good = False
        if s["make_holder"] and tl.holder_len > max(usable_max, diag - 2 * s["depth"]):
            good = False
        if good:
            max_n = n
            break
    return FitReport(ok, lines, max_n)


Topology = tuple[int, bool, bool, bool, bool, bool, bool, bool, Mount]
"""Everything that changes the feature tree, as opposed to sizes."""


def topology(s: Settings) -> Topology:
    """Return the settings that decide which features exist.

    Two settings with the same topology produce the same timeline, so the
    parameters of an existing design can be updated in place.

    Args:
        s: Settings.

    Returns:
        A comparable tuple.
    """
    lay = layout(s)
    mount: Mount = s["mount"] if s["make_frame"] and s["make_holder"] else "none"
    return (
        lay.n,
        lay.pin,
        lay.side,
        lay.nut_side,
        bool(s["raised_teeth"]),
        bool(s["make_holder"]),
        bool(s["make_frame"]),
        bool(s["make_tie"]),
        mount,
    )
