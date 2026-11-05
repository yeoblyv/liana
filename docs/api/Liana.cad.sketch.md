---
id: api.liana.cad.sketch
title: Liana.cad.sketch
slug: /api/Liana.cad.sketch
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.sketch`

# `Liana.cad.sketch`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Sketches whose every coordinate is driven by a parameter expression.

## On this page

- [Classes](#classes)
  - [`ParamSketch`](#liana-cad-sketch-class-paramsketch)
    - [`ParamSketch.__init__`](#liana-cad-sketch-class-paramsketch-init)
    - [`ParamSketch.name`](#liana-cad-sketch-class-paramsketch-name)
    - [`ParamSketch.dim_coord`](#liana-cad-sketch-class-paramsketch-dim-coord)
    - [`ParamSketch.dim_between`](#liana-cad-sketch-class-paramsketch-dim-between)
    - [`ParamSketch.rect`](#liana-cad-sketch-class-paramsketch-rect)
    - [`ParamSketch.right_triangle`](#liana-cad-sketch-class-paramsketch-right-triangle)
    - [`ParamSketch.circle`](#liana-cad-sketch-class-paramsketch-circle)
    - [`ParamSketch.polygon`](#liana-cad-sketch-class-paramsketch-polygon)
    - [`ParamSketch.point`](#liana-cad-sketch-class-paramsketch-point)
    - [`ParamSketch.profiles`](#liana-cad-sketch-class-paramsketch-profiles)
    - [`ParamSketch.normal`](#liana-cad-sketch-class-paramsketch-normal)
- [Functions](#functions)
  - [`plane_y`](#liana-cad-sketch-plane-y)
  - [`plane_z`](#liana-cad-sketch-plane-z)
- [See also](#see-also)
- [Changelog](#changelog)

## Classes

### `ParamSketch` {#liana-cad-sketch-class-paramsketch}

A sketch on a plane, drawn in model coordinates given as expressions.

Geometry is placed at the current parameter values and then dimensioned
with the same expressions, so the sketch follows any later parameter
change.

| Attribute | Description |
|---|---|
| `ctx` | Build context. |
| `comp` | Component that owns the sketch. |
| `iu` | Model axis (0 = X, 1 = Y, 2 = Z) of the first in-plane coordinate. |
| `iv` | Model axis of the second in-plane coordinate. |
| `sk` | The Fusion sketch. |

**Since** 1.0.0

#### `ParamSketch.__init__(self, ctx: BuildContext, comp: Component, plane: ConstructionPlane, name: str, iu: int, iv: int) -> None` {#liana-cad-sketch-class-paramsketch-init}

Create the sketch.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context. |
| `comp` | `Component` | Component that receives the sketch. |
| `plane` | `ConstructionPlane` | Sketch plane. |
| `name` | `str` | Sketch name shown in the browser. |
| `iu` | `int` | Model axis of the first in-plane coordinate. |
| `iv` | `int` | Model axis of the second in-plane coordinate. |

**Since** 1.0.0

#### `ParamSketch.name(self) -> str` {#liana-cad-sketch-class-paramsketch-name}

Sketch name.

**Returns** `str`  
**Since** 1.0.0

#### `ParamSketch.dim_coord(self, pt: SketchPoint, axis: int, expr: str) -> None` {#liana-cad-sketch-class-paramsketch-dim-coord}

Drive one model coordinate of a sketch point by an expression.

Fusion refuses a second origin dimension for a point that sits on the
same coordinate as a point already dimensioned (an over-constraint
error) without tying the two points together. Such a point would stay
behind when the parameter changes, so it is aligned to the first point
with an explicit constraint instead.

| Parameter | Type | Description |
|---|---|---|
| `pt` | `SketchPoint` | Sketch point. |
| `axis` | `int` | Model axis of the coordinate. |
| `expr` | `str` | Expression of the coordinate. |

**Since** 1.0.0

#### `ParamSketch.dim_between(self, a: SketchPoint, b: SketchPoint, axis: int, expr: str) -> None` {#liana-cad-sketch-class-paramsketch-dim-between}

Drive the distance between two points along a model axis.

| Parameter | Type | Description |
|---|---|---|
| `a` | `SketchPoint` | First point. |
| `b` | `SketchPoint` | Second point. |
| `axis` | `int` | Model axis of the distance. |
| `expr` | `str` | Distance expression; a negative value is driven by its negation. |

**Since** 1.0.0

#### `ParamSketch.rect(self, u0: str, v0: str, u1: str, v1: str) -> None` {#liana-cad-sketch-class-paramsketch-rect}

Draw an axis-aligned rectangle between two opposite corners.

| Parameter | Type | Description |
|---|---|---|
| `u0` | `str` | First corner, first coordinate. |
| `v0` | `str` | First corner, second coordinate. |
| `u1` | `str` | Opposite corner, first coordinate. |
| `v1` | `str` | Opposite corner, second coordinate. |

**Since** 1.0.0

#### `ParamSketch.right_triangle(self, uc: str, vc: str, ue: str, ve: str) -> None` {#liana-cad-sketch-class-paramsketch-right-triangle}

Draw a right triangle with the corner at `(uc, vc)`.

The legs end at `(ue, vc)` and `(uc, ve)`.

| Parameter | Type | Description |
|---|---|---|
| `uc` | `str` | Corner, first coordinate. |
| `vc` | `str` | Corner, second coordinate. |
| `ue` | `str` | End of the first leg. |
| `ve` | `str` | End of the second leg. |

**Since** 1.0.0

#### `ParamSketch.circle(self, uc: str, vc: str, dia: str) -> SketchCircle` {#liana-cad-sketch-class-paramsketch-circle}

Draw a circle with a driven center and diameter.

| Parameter | Type | Description |
|---|---|---|
| `uc` | `str` | Center, first coordinate. |
| `vc` | `str` | Center, second coordinate. |
| `dia` | `str` | Diameter expression. |

**Returns** `SketchCircle`  
**Since** 1.0.0

#### `ParamSketch.polygon(self, pts: Outline) -> list[SketchLine]` {#liana-cad-sketch-class-paramsketch-polygon}

Draw a closed polygon; every vertex is dimensioned.

| Parameter | Type | Description |
|---|---|---|
| `pts` | `Outline` | Vertices in order; the polygon is closed automatically. |

**Returns** `list[SketchLine]`  
**Since** 1.0.0

#### `ParamSketch.point(self, u: str, v: str) -> SketchPoint` {#liana-cad-sketch-class-paramsketch-point}

Add a driven sketch point.

| Parameter | Type | Description |
|---|---|---|
| `u` | `str` | First coordinate. |
| `v` | `str` | Second coordinate. |

**Returns** `SketchPoint`  
**Since** 1.0.0

#### `ParamSketch.profiles(self) -> Any` {#liana-cad-sketch-class-paramsketch-profiles}

Return every profile of the sketch as an `ObjectCollection`.

**Returns** `Any`  
**Since** 1.0.0

#### `ParamSketch.normal(self) -> Any` {#liana-cad-sketch-class-paramsketch-normal}

Return the sketch normal as a `Vector3D`.

**Returns** `Any`  
**Since** 1.0.0

## Functions

### `plane_y(ctx: BuildContext, comp: Component, y_expr: str) -> ConstructionPlane` {#liana-cad-sketch-plane-y}

Return a plane parallel to XZ at `Y = y_expr`.

The XZ plane itself is returned for a zero offset; any other plane is a
hidden offset construction plane driven by the expression.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context. |
| `comp` | `Component` | Component that owns the plane. |
| `y_expr` | `str` | Height of the plane. |

**Returns** `ConstructionPlane`  
**Since** 1.0.0

### `plane_z(comp: Component, z_expr: str) -> ConstructionPlane` {#liana-cad-sketch-plane-z}

Return a hidden plane parallel to XY at `Z = z_expr`.

| Parameter | Type | Description |
|---|---|---|
| `comp` | `Component` | Component that owns the plane. |
| `z_expr` | `str` | Position of the plane along Z. |

**Returns** `ConstructionPlane`  
**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
