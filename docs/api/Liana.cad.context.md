---
id: api.liana.cad.context
title: Liana.cad.context
slug: /api/Liana.cad.context
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.context`

# `Liana.cad.context`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

State shared by the builders during one build.

## On this page

- [Classes](#classes)
  - [`BuildContext`](#liana-cad-context-class-buildcontext)
    - [`BuildContext.ev`](#liana-cad-context-class-buildcontext-ev)
    - [`BuildContext.mag`](#liana-cad-context-class-buildcontext-mag)
    - [`BuildContext.soft`](#liana-cad-context-class-buildcontext-soft)
- [See also](#see-also)
- [Changelog](#changelog)

## Classes

### `BuildContext` {#liana-cad-context-class-buildcontext}

The design being built, the application and the log of the build.

| Attribute | Description |
|---|---|
| `app` | Fusion application. |
| `design` | Design that receives the system. |
| `log` | Problems recorded so far. |

**Since** 1.0.0

#### `BuildContext.ev(self, expr: str) -> float` {#liana-cad-context-class-buildcontext-ev}

Evaluate an expression against the design parameters, in mm.

| Parameter | Type | Description |
|---|---|---|
| `expr` | `str` | Expression of User Parameters, with units. |

**Returns** `float`  
**Since** 1.0.0

#### `BuildContext.mag(self, expr: str) -> tuple[str, float]` {#liana-cad-context-class-buildcontext-mag}

Return an expression for the magnitude of `expr` and its value in mm.

Sketch dimensions are always positive, so a negative coordinate is
driven by its negation.

| Parameter | Type | Description |
|---|---|---|
| `expr` | `str` | Expression of a coordinate. |

**Returns** `tuple[str, float]`  
**Since** 1.0.0

#### `BuildContext.soft(self, name: str, fn: Callable[[], _T]) -> _T | None` {#liana-cad-context-class-buildcontext-soft}

Run an optional finishing step; a failure is logged, not raised.

Fillets, chamfers and colors only refine a part, so the part stays
usable without them. Fusion can fail them in ways the API does not
document (edge topology, tangency), hence the broad catch.

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | Label for the log, e.g. `"Rail: end rounding"`. |
| `fn` | `Callable[[], _T]` | The step. |

**Returns** `_T | None` - What `fn` returned, or None if it failed.  
**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
