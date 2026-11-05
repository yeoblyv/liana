---
id: api.liana.cad.features
title: Liana.cad.features
slug: /api/Liana.cad.features
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.features`

# `Liana.cad.features`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Extrudes, combines, rounds and countersunk holes with checked directions.

## On this page

- [Constants](#constants)
  - [`Vec3`](#liana-cad-features-const-vec3)
  - [`Pt2`](#liana-cad-features-const-pt2)
- [Functions](#functions)
  - [`ext_sym`](#liana-cad-features-ext-sym)
  - [`ext_one`](#liana-cad-features-ext-one)
  - [`combine`](#liana-cad-features-combine)
  - [`line_edges`](#liana-cad-features-line-edges)
  - [`z_edges`](#liana-cad-features-z-edges)
  - [`y_edges`](#liana-cad-features-y-edges)
  - [`face_edges_at_y`](#liana-cad-features-face-edges-at-y)
  - [`end_face_edges`](#liana-cad-features-end-face-edges)
  - [`sym`](#liana-cad-features-sym)
  - [`corners`](#liana-cad-features-corners)
  - [`fillet`](#liana-cad-features-fillet)
  - [`chamfer`](#liana-cad-features-chamfer)
  - [`csk_holes`](#liana-cad-features-csk-holes)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `Vec3` {#liana-cad-features-const-vec3}

Model point in millimeters.

**Since** 1.0.0

### `Pt2` {#liana-cad-features-const-pt2}

Pair of model coordinates in millimeters.

**Since** 1.0.0

## Functions

### `ext_sym(comp: Component, sketch: ParamSketch, op: object, dist: str) -> Feature` {#liana-cad-features-ext-sym}

Extrude every profile of a sketch symmetrically, `dist` in total.

Cuts use a bounded distance rather than "All", so they stay inside the
part's own bodies.

| Parameter | Type | Description |
|---|---|---|
| `comp` | `Component` | Component of the sketch. |
| `sketch` | `ParamSketch` | Sketch with the profiles. |
| `op` | `object` | Feature operation (new body, join or cut). |
| `dist` | `str` | Total distance expression. |

**Returns** `Feature`  
**Since** 1.0.0

### `ext_one(ctx: BuildContext, comp: Component, sketch: ParamSketch, op: object, dist: str, want_y: int, probe: Vec3, taper: str | None=None, wrong_probe: Vec3 | None=None) -> Feature` {#liana-cad-features-ext-one}

Extrude one-sided toward +Y or -Y, checking the result with probe points.

Which extent direction points toward the wanted side depends on the plane
normal Fusion picked, so the likely direction is tried first and the
result is checked: after a cut the probe must be empty, after a join or
new body it must be filled. A wrong result is deleted and the other
direction is tried.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context. |
| `comp` | `Component` | Component of the sketch. |
| `sketch` | `ParamSketch` | Sketch with the profiles. |
| `op` | `object` | Feature operation. |
| `dist` | `str` | Distance expression. |
| `want_y` | `int` | `1` to extrude toward +Y, `-1` toward -Y. |
| `probe` | `Vec3` | Point that tells whether the extrude went the right way. |
| `taper` | `str \| None` | Optional taper angle expression. |
| `wrong_probe` | `Vec3 \| None` | Optional point that must stay filled; it catches a taper with the wrong sign. |

**Returns** `Feature` - The feature.  
**Raises** `RuntimeError` - Neither direction gave the expected result.  
**Since** 1.0.0

### `combine(comp: Component, probe: Vec3) -> Feature | None` {#liana-cad-features-combine}

Join every body of a component into the one that contains `probe`.

| Parameter | Type | Description |
|---|---|---|
| `comp` | `Component` | Component with the bodies. |
| `probe` | `Vec3` | Point in mm inside the body that receives the others. |

**Returns** `Feature | None` - The combine feature, or None when there is only one body.  
**Since** 1.0.0

### `line_edges(bs: Sequence[BRepBody]) -> Iterator[tuple[BRepEdge, Point, Point]]` {#liana-cad-features-line-edges}

Yield the straight edges of some bodies with their end points.

| Parameter | Type | Description |
|---|---|---|
| `bs` | `Sequence[BRepBody]` | Bodies to search. |

**Returns** `Iterator[tuple[BRepEdge, Point, Point]]`  
**Since** 1.0.0

### `z_edges(bs: Sequence[BRepBody], pts: Sequence[Pt2], tol: float=0.02) -> list[BRepEdge]` {#liana-cad-features-z-edges}

Return the straight edges parallel to Z that pass through given `(x, y)`.

| Parameter | Type | Description |
|---|---|---|
| `bs` | `Sequence[BRepBody]` | Bodies to search. |
| `pts` | `Sequence[Pt2]` | `(x, y)` in mm. |
| `tol` | `float` | Match tolerance in mm. |

**Returns** `list[BRepEdge]`  
**Since** 1.0.0

### `y_edges(bs: Sequence[BRepBody], pts: Sequence[Pt2], tol: float=0.02) -> list[BRepEdge]` {#liana-cad-features-y-edges}

Return the straight edges parallel to Y that pass through given `(x, z)`.

| Parameter | Type | Description |
|---|---|---|
| `bs` | `Sequence[BRepBody]` | Bodies to search. |
| `pts` | `Sequence[Pt2]` | `(x, z)` in mm. |
| `tol` | `float` | Match tolerance in mm. |

**Returns** `list[BRepEdge]`  
**Since** 1.0.0

### `face_edges_at_y(bs: Sequence[BRepBody], y: float, tol: float=0.01) -> list[BRepEdge]` {#liana-cad-features-face-edges-at-y}

Return every edge, straight or curved, that lies in the plane `Y = y` (mm).

| Parameter | Type | Description |
|---|---|---|
| `bs` | `Sequence[BRepBody]` | Bodies to search. |
| `y` | `float` | Height of the plane in mm. |
| `tol` | `float` | Match tolerance in mm. |

**Returns** `list[BRepEdge]`  
**Since** 1.0.0

### `end_face_edges(bs: Sequence[BRepBody], dz: float, x: float, half_width: float, y0: float, y1: float) -> list[BRepEdge]` {#liana-cad-features-end-face-edges}

Return the straight edges on the end faces `Z = +-dz` inside a window.

| Parameter | Type | Description |
|---|---|---|
| `bs` | `Sequence[BRepBody]` | Bodies to search. |
| `dz` | `float` | Distance of the end faces from Z = 0, in mm. |
| `x` | `float` | Center of the window along X, in mm. |
| `half_width` | `float` | Half-width of the window along X, in mm. |
| `y0` | `float` | Bottom of the window, in mm. |
| `y1` | `float` | Top of the window, in mm. |

**Returns** `list[BRepEdge]`  
**Since** 1.0.0

### `sym(x: float, y: float) -> list[Pt2]` {#liana-cad-features-sym}

Return a point and its mirror image across X = 0.

| Parameter | Type | Description |
|---|---|---|
| `x` | `float` | X in mm. |
| `y` | `float` | Second coordinate in mm. |

**Returns** `list[Pt2]`  
**Since** 1.0.0

### `corners(x: float, z: float) -> list[Pt2]` {#liana-cad-features-corners}

Return the four corners of a rectangle centered on the origin.

| Parameter | Type | Description |
|---|---|---|
| `x` | `float` | Half-width in mm. |
| `z` | `float` | Half-depth in mm. |

**Returns** `list[Pt2]`  
**Since** 1.0.0

### `fillet(comp: Component, edges: Sequence[BRepEdge], radius: str) -> Feature` {#liana-cad-features-fillet}

Round edges with a constant radius.

| Parameter | Type | Description |
|---|---|---|
| `comp` | `Component` | Component of the edges. |
| `edges` | `Sequence[BRepEdge]` | Edges to round. |
| `radius` | `str` | Radius expression. |

**Returns** `Feature`  
**Raises** `RuntimeError` - No edges were given.  
**Since** 1.0.0

### `chamfer(comp: Component, edges: Sequence[BRepEdge], dist: str) -> Feature` {#liana-cad-features-chamfer}

Chamfer edges with an equal distance.

| Parameter | Type | Description |
|---|---|---|
| `comp` | `Component` | Component of the edges. |
| `edges` | `Sequence[BRepEdge]` | Edges to chamfer. |
| `dist` | `str` | Distance expression. |

**Returns** `Feature`  
**Raises** `RuntimeError` - No edges were given.  
**Since** 1.0.0

### `csk_holes(ctx: BuildContext, comp: Component, y_expr: str, pts: Sequence[tuple[str, str]], dia: str, csk: str, angle: str, depth: str, name: str, want_y: int=1) -> Feature` {#liana-cad-features-csk-holes}

Drill countersunk holes from the plane `Y = y_expr` toward `want_y`.

The Hole feature is used when it works. Otherwise each hole is built as
two extrude cuts: the bore and a tapered countersink.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context. |
| `comp` | `Component` | Component to drill. |
| `y_expr` | `str` | Y of the surface the holes start from. |
| `pts` | `Sequence[tuple[str, str]]` | Hole centers as `(x, z)` expressions. |
| `dia` | `str` | Bore diameter. |
| `csk` | `str` | Countersink diameter at the surface. |
| `angle` | `str` | Countersink angle. |
| `depth` | `str` | Bore depth. |
| `name` | `str` | Sketch name. |
| `want_y` | `int` | `1` to drill toward +Y, `-1` toward -Y. |

**Returns** `Feature` - The last feature created.  
**Raises** `RuntimeError` - The countersink could not be cut in either taper sign.  
**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
