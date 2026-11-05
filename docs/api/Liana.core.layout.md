---
id: api.liana.core.layout
title: Liana.core.layout
slug: /api/Liana.core.layout
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.core.layout`

# `Liana.core.layout`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Layout arithmetic shared by the dialog and the builders; no Fusion calls.

Every value mirrors a User Parameter expression in `params`, so the
dialog can report sizes and printer-bed fit before anything is built.
Coordinates: table face at Y = 0, parts hang below it (-Y), X along the
holder, Z along the cable.

## On this page

- [Constants](#constants)
  - [`END_W`](#liana-core-layout-const-end-w)
  - [`EAR_OFFSET`](#liana-core-layout-const-ear-offset)
  - [`PLATE_T`](#liana-core-layout-const-plate-t)
  - [`CEIL_GAP`](#liana-core-layout-const-ceil-gap)
  - [`PAD_T`](#liana-core-layout-const-pad-t)
  - [`STANDARD_M3_LENGTHS`](#liana-core-layout-const-standard-m3-lengths)
  - [`Topology`](#liana-core-layout-const-topology)
- [Classes](#classes)
  - [`Layout`](#liana-core-layout-class-layout)
  - [`FitReport`](#liana-core-layout-class-fitreport)
- [Functions](#functions)
  - [`layout`](#liana-core-layout-layout)
  - [`fit_report`](#liana-core-layout-fit-report)
  - [`topology`](#liana-core-layout-topology)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `END_W` {#liana-core-layout-const-end-w}

End block width in mm (`END_W` parameter).

**Since** 1.0.0

### `EAR_OFFSET` {#liana-core-layout-const-ear-offset}

Ear screw distance from the end block outer face in mm.

**Since** 1.0.0

### `PLATE_T` {#liana-core-layout-const-plate-t}

Rail plate thickness in mm.

**Since** 1.0.0

### `CEIL_GAP` {#liana-core-layout-const-ceil-gap}

Gap from the cable top to the rail plate in mm.

**Since** 1.0.0

### `PAD_T` {#liana-core-layout-const-pad-t}

Rail thickness under the screw heads in mm.

**Since** 1.0.0

### `STANDARD_M3_LENGTHS` {#liana-core-layout-const-standard-m3-lengths}

Stock lengths of M3 DIN 965 countersunk screws in mm.

**Since** 1.0.0

### `Topology` {#liana-core-layout-const-topology}

Everything that changes the feature tree, as opposed to sizes.

**Since** 1.0.0

## Classes

### `Layout` {#liana-core-layout-class-layout}

Sizes derived from the settings, in millimeters.

| Attribute | Description |
|---|---|
| `n` | Cradles per holder. |
| `r` | Cradle radius. |
| `p` | Cradle pitch (cable diameter + tooth width). |
| `end_x0` | Inner face of the end blocks (+-X). |
| `end_x1` | Outer face of the end blocks. |
| `ear_x` | Ear screws (+-X). |
| `stem_hw` | Half-width of the T-pin stem. |
| `boss_hw` | Half-width of the rail boss around the T-slot. |
| `side_x` | Side screws, measured from the pin. |
| `block_hx` | Half-width of the rail center block. |
| `pin` | Whether the comb has a center T-pin. |
| `pin_x` | X of the pin (half a pitch off center for odd counts). |
| `side` | Whether the side screws next to the pin fit. |
| `cav_r` | Round of the rail cavity upper corners. |
| `a` | Half-distance between opposite holders on the frame. |
| `bw` | Frame beam width (widened when the holder needs it). |
| `m3_x` | Rail-to-comb M3 screws (+-X). |
| `frame_out` | Outer size of the square frame. |
| `holder_len` | Overall rail length. |
| `comb_len` | Overall comb length. |
| `cable_y` | Depth of the cable axis (rail/comb joint) below the table. |
| `comb_end_bot` | Comb end blocks below the cable axis. |
| `bite_holder` | Wood screw engagement in the table, holder alone. |
| `nut_y0` | Nut slot bottom above the joint. |
| `nut_side` | Whether the nut enters from the side (low end blocks). |
| `bite_frame` | Wood screw engagement, holder on the frame. |
| `m3_len` | Stock M3 length that fits, or None. |
| `teeth` | Raised teeth positions in pitches from the center. |
| `gusset` | Leg of the frame inner corner gussets. |

**Since** 1.0.0

### `FitReport(NamedTuple)` {#liana-core-layout-class-fitreport}

Printer bed check.

| Attribute | Description |
|---|---|
| `ok` | Whether every enabled part fits. |
| `lines` | One summary line per part. |
| `max_cradles` | Largest cradle count that still fits (0 if none). |

**Since** 1.0.0

## Functions

### `layout(s: Settings) -> Layout` {#liana-core-layout-layout}

Compute the layout for a set of settings.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings; lengths in mm. |

**Returns** `Layout` - The derived sizes.  
**Since** 1.0.0

### `fit_report(s: Settings) -> FitReport` {#liana-core-layout-fit-report}

Check the enabled parts against the printer bed.

The rail may lie diagonally; the frame is square and must fit the short
side of the bed.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings including the bed size and margin. |

**Returns** `FitReport` - The fit report.  
**Since** 1.0.0

### `topology(s: Settings) -> Topology` {#liana-core-layout-topology}

Return the settings that decide which features exist.

Two settings with the same topology produce the same timeline, so the
parameters of an existing design can be updated in place.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings. |

**Returns** `Topology` - A comparable tuple.  
**Since** 1.0.0

## See also

- [`Liana.core`](Liana.core.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
