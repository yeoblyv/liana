---
id: api.liana.cad.api
title: Liana.cad.api
slug: /api/Liana.cad.api
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.api`

# `Liana.cad.api`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Thin helpers over the Fusion API used by every builder.

The `adsk` package ships without type information, so its objects are typed
as `typing.Any` through the aliases below; the aliases document which
Fusion class a value is expected to be.

## On this page

- [Constants](#constants)
  - [`Application`](#liana-cad-api-const-application)
  - [`UserInterface`](#liana-cad-api-const-userinterface)
  - [`Design`](#liana-cad-api-const-design)
  - [`Component`](#liana-cad-api-const-component)
  - [`Occurrence`](#liana-cad-api-const-occurrence)
  - [`ConstructionPlane`](#liana-cad-api-const-constructionplane)
  - [`Sketch`](#liana-cad-api-const-sketch)
  - [`SketchPoint`](#liana-cad-api-const-sketchpoint)
  - [`SketchLine`](#liana-cad-api-const-sketchline)
  - [`SketchCircle`](#liana-cad-api-const-sketchcircle)
  - [`Feature`](#liana-cad-api-const-feature)
  - [`BRepBody`](#liana-cad-api-const-brepbody)
  - [`BRepEdge`](#liana-cad-api-const-brepedge)
  - [`Point`](#liana-cad-api-const-point)
  - [`MM`](#liana-cad-api-const-mm)
  - [`API_ERRORS`](#liana-cad-api-const-api-errors)
  - [`NEW_BODY`](#liana-cad-api-const-new-body)
  - [`JOIN`](#liana-cad-api-const-join)
  - [`CUT`](#liana-cad-api-const-cut)
- [Functions](#functions)
  - [`value`](#liana-cad-api-value)
  - [`point`](#liana-cad-api-point)
  - [`collection`](#liana-cad-api-collection)
  - [`bodies`](#liana-cad-api-bodies)
  - [`is_inside`](#liana-cad-api-is-inside)
  - [`inside`](#liana-cad-api-inside)
  - [`first_line`](#liana-cad-api-first-line)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `Application` {#liana-cad-api-const-application}

`adsk.core.Application`.

**Since** 1.0.0

### `UserInterface` {#liana-cad-api-const-userinterface}

`adsk.core.UserInterface`.

**Since** 1.0.0

### `Design` {#liana-cad-api-const-design}

`adsk.fusion.Design`.

**Since** 1.0.0

### `Component` {#liana-cad-api-const-component}

`adsk.fusion.Component`.

**Since** 1.0.0

### `Occurrence` {#liana-cad-api-const-occurrence}

`adsk.fusion.Occurrence`.

**Since** 1.0.0

### `ConstructionPlane` {#liana-cad-api-const-constructionplane}

`adsk.fusion.ConstructionPlane`.

**Since** 1.0.0

### `Sketch` {#liana-cad-api-const-sketch}

`adsk.fusion.Sketch`.

**Since** 1.0.0

### `SketchPoint` {#liana-cad-api-const-sketchpoint}

`adsk.fusion.SketchPoint`.

**Since** 1.0.0

### `SketchLine` {#liana-cad-api-const-sketchline}

`adsk.fusion.SketchLine`.

**Since** 1.0.0

### `SketchCircle` {#liana-cad-api-const-sketchcircle}

`adsk.fusion.SketchCircle`.

**Since** 1.0.0

### `Feature` {#liana-cad-api-const-feature}

Any timeline feature, e.g. `adsk.fusion.ExtrudeFeature`.

**Since** 1.0.0

### `BRepBody` {#liana-cad-api-const-brepbody}

`adsk.fusion.BRepBody`.

**Since** 1.0.0

### `BRepEdge` {#liana-cad-api-const-brepedge}

`adsk.fusion.BRepEdge`.

**Since** 1.0.0

### `Point` {#liana-cad-api-const-point}

`adsk.core.Point3D`.

**Since** 1.0.0

### `MM` {#liana-cad-api-const-mm}

One millimeter in Fusion internal units (centimetres).

**Since** 1.0.0

### `API_ERRORS` {#liana-cad-api-const-api-errors}

Exceptions that mean "Fusion refused this call".

Fusion raises RuntimeError for a refused operation and AttributeError when a
method or property is missing in an older release. Its bindings raise
NotImplementedError when no overload matches the arguments, and TypeError or
ValueError when an argument cannot be converted.

**Since** 1.0.0

### `NEW_BODY` {#liana-cad-api-const-new-body}

Feature operation that creates a new body.

**Since** 1.0.0

### `JOIN` {#liana-cad-api-const-join}

Feature operation that adds to the existing body.

**Since** 1.0.0

### `CUT` {#liana-cad-api-const-cut}

Feature operation that removes material.

**Since** 1.0.0

## Functions

### `value(expr: str) -> Any` {#liana-cad-api-value}

Return a `ValueInput` for an expression.

| Parameter | Type | Description |
|---|---|---|
| `expr` | `str` | Fusion expression, e.g. `"DEPTH + 2 mm"`. |

**Returns** `Any`  
**Since** 1.0.0

### `point(x: float, y: float, z: float) -> Point` {#liana-cad-api-point}

Return a `Point3D` from millimeter coordinates.

| Parameter | Type | Description |
|---|---|---|
| `x` | `float` | X in mm. |
| `y` | `float` | Y in mm. |
| `z` | `float` | Z in mm. |

**Returns** `Point`  
**Since** 1.0.0

### `collection(items: Iterable[Any]) -> Any` {#liana-cad-api-collection}

Return an `ObjectCollection` holding `items` in order.

| Parameter | Type | Description |
|---|---|---|
| `items` | `Iterable[Any]` | API objects, in the order they should keep. |

**Returns** `Any`  
**Since** 1.0.0

### `bodies(comp: Component) -> list[BRepBody]` {#liana-cad-api-bodies}

Return the bodies of a component.

| Parameter | Type | Description |
|---|---|---|
| `comp` | `Component` | Component. |

**Returns** `list[BRepBody]`  
**Since** 1.0.0

### `is_inside(body: BRepBody, p: tuple[float, float, float]) -> bool` {#liana-cad-api-is-inside}

Return whether a point in millimeters lies inside a body.

| Parameter | Type | Description |
|---|---|---|
| `body` | `BRepBody` | Body to test. |
| `p` | `tuple[float, float, float]` | Point `(x, y, z)` in mm. |

**Returns** `bool`  
**Since** 1.0.0

### `inside(comp: Component, p: tuple[float, float, float]) -> bool` {#liana-cad-api-inside}

Return whether a point in millimeters lies inside any body of a component.

| Parameter | Type | Description |
|---|---|---|
| `comp` | `Component` | Component whose bodies are tested. |
| `p` | `tuple[float, float, float]` | Point `(x, y, z)` in mm. |

**Returns** `bool`  
**Since** 1.0.0

### `first_line(error: BaseException) -> str` {#liana-cad-api-first-line}

Return the first line of an exception message, for logs.

| Parameter | Type | Description |
|---|---|---|
| `error` | `BaseException` | Exception to describe. |

**Returns** `str`  
**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
