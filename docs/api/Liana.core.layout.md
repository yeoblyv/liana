# `Liana.core.layout`

Layout arithmetic shared by the dialog and the builders; no Fusion calls.

Every value mirrors a User Parameter expression in :mod:`.params`, so the
dialog can report sizes and printer-bed fit before anything is built.
Coordinates: table face at Y = 0, parts hang below it (-Y), X along the
holder, Z along the cable.

## Constants

### `END_W`

End block width in mm (``END_W`` parameter).

### `EAR_OFFSET`

Ear screw distance from the end block outer face in mm.

### `PLATE_T`

Rail plate thickness in mm.

### `CEIL_GAP`

Gap from the cable top to the rail plate in mm.

### `PAD_T`

Rail thickness under the screw heads in mm.

### `STANDARD_M3_LENGTHS`

Stock lengths of M3 DIN 965 countersunk screws in mm.

### `Topology`

Everything that changes the feature tree, as opposed to sizes.

## Classes

### `Layout`

```text
Sizes derived from the settings, in millimeters.

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
    block_hx: Half-width of the rail center block.
    pin: Whether the comb has a center T-pin.
    pin_x: X of the pin (half a pitch off center for odd counts).
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
    teeth: Raised teeth positions in pitches from the center.
    gusset: Leg of the frame inner corner gussets.
```

### `FitReport(NamedTuple)`

```text
Printer bed check.

Attributes:
    ok: Whether every enabled part fits.
    lines: One summary line per part.
    max_cradles: Largest cradle count that still fits (0 if none).
```

## Functions

### `layout(s: Settings) -> Layout`

```text
Compute the layout for a set of settings.

Args:
    s: Settings; lengths in mm.

Returns:
    The derived sizes.
```

### `fit_report(s: Settings) -> FitReport`

```text
Check the enabled parts against the printer bed.

The rail may lie diagonally; the frame is square and must fit the short
side of the bed.

Args:
    s: Settings including the bed size and margin.

Returns:
    The fit report.
```

### `topology(s: Settings) -> Topology`

```text
Return the settings that decide which features exist.

Two settings with the same topology produce the same timeline, so the
parameters of an existing design can be updated in place.

Args:
    s: Settings.

Returns:
    A comparable tuple.
```
