---
id: api.liana.core.expr
title: Liana.core.expr
slug: /api/Liana.core.expr
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.core.expr`

# `Liana.core.expr`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Builders for Fusion parameter expressions and the outlines drawn with them.

Every sketch coordinate is an expression of User Parameters rather than a
number, so the design follows a parameter change without running Liana again.

## On this page

- [Constants](#constants)
  - [`Outline`](#liana-core-expr-const-outline)
- [Functions](#functions)
  - [`neg`](#liana-core-expr-neg)
  - [`sgn`](#liana-core-expr-sgn)
  - [`diff`](#liana-core-expr-diff)
  - [`pitch_expr`](#liana-core-expr-pitch-expr)
  - [`nut_seat`](#liana-core-expr-nut-seat)
  - [`member_coords`](#liana-core-expr-member-coords)
  - [`holder_hole_exprs`](#liana-core-expr-holder-hole-exprs)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `Outline` {#liana-core-expr-const-outline}

Closed polygon as `(u, v)` expression pairs.

**Since** 1.0.0

## Functions

### `neg(e: str) -> str` {#liana-core-expr-neg}

Return the negated expression.

| Parameter | Type | Description |
|---|---|---|
| `e` | `str` | Expression. |

**Returns** `str`  
**Since** 1.0.0

### `sgn(sign: int, e: str) -> str` {#liana-core-expr-sgn}

Return `e` for a positive sign and its negation otherwise.

| Parameter | Type | Description |
|---|---|---|
| `sign` | `int` | Positive keeps `e`, anything else negates it. |
| `e` | `str` | Expression. |

**Returns** `str`  
**Since** 1.0.0

### `diff(a: str, b: str) -> str` {#liana-core-expr-diff}

Return the expression `a - b`.

| Parameter | Type | Description |
|---|---|---|
| `a` | `str` | Minuend. |
| `b` | `str` | Subtrahend. |

**Returns** `str`  
**Since** 1.0.0

### `pitch_expr(t: float) -> str` {#liana-core-expr-pitch-expr}

Return `t` cradle pitches from the center as an expression.

| Parameter | Type | Description |
|---|---|---|
| `t` | `float` | Offset in pitches; may be fractional. |

**Returns** `str` - `"0 mm"` for zero, otherwise `"<t> * NOTCH_PITCH"`.  
**Since** 1.0.0

### `nut_seat(sx: int, side: bool) -> Outline` {#liana-core-expr-nut-seat}

Return the outline of one M3 nut seat at `x = sx * M3_X`.

The seat is an entry slot with a flared mouth that ends in a half hexagon
centered on the screw, so the nut slides in by hand, stops on the screw
axis and cannot turn.

| Parameter | Type | Description |
|---|---|---|
| `sx` | `int` | `1` for the seat at +X, `-1` for the one at -X. |
| `side` | `bool` | The slot opens to the -Z face (low end blocks) when true, otherwise to the end face at +-X. |

**Returns** `Outline` - Vertices with `u` along X and `v` along Z.  
**Since** 1.0.0

### `member_coords(side: Side, width: str, half_len: str) -> tuple[str, str, str, str]` {#liana-core-expr-member-coords}

Return the rectangle of one frame beam as `(u0, v0, u1, v1)`.

| Parameter | Type | Description |
|---|---|---|
| `side` | `Side` | Frame side; S and N beams run along X, E and W along Z. |
| `width` | `str` | Beam width expression. |
| `half_len` | `str` | Half of the beam length. |

**Returns** `tuple[str, str, str, str]` - Opposite corners with `u` along X and `v` along Z, relative to the frame center.  
**Since** 1.0.0

### `holder_hole_exprs(side_screws: bool, ev: Callable[[str], float]) -> list[str]` {#liana-core-expr-holder-hole-exprs}

Return the holder screw positions along the holder axis.

The frame gets a hole under every holder screw for both orientations of
the holder, so the side screws are mirrored; mirrored positions that
coincide with an existing hole are dropped.

| Parameter | Type | Description |
|---|---|---|
| `side_screws` | `bool` | Whether the holder has side screws next to the pin. |
| `ev` | `Callable[[str], float]` | Evaluates an expression to millimeters. |

**Returns** `list[str]` - X expressions of the holes.  
**Since** 1.0.0

## See also

- [`Liana.core`](Liana.core.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
