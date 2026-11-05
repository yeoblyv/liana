---
id: api.liana.core.params
title: Liana.core.params
slug: /api/Liana.core.params
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.core.params`

# `Liana.core.params`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

User Parameters that drive every sketch dimension of a Liana system.

## On this page

- [Constants](#constants)
  - [`ANGLE_PARAMS`](#liana-core-params-const-angle-params)
- [Classes](#classes)
  - [`ParamSpec`](#liana-core-params-class-paramspec)
- [Functions](#functions)
  - [`fmt`](#liana-core-params-fmt)
  - [`make_params`](#liana-core-params-make-params)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `ANGLE_PARAMS` {#liana-core-params-const-angle-params}

Parameters measured in degrees; all others are lengths in mm.

**Since** 1.0.0

## Classes

### `ParamSpec(NamedTuple)` {#liana-core-params-class-paramspec}

One User Parameter.

| Attribute | Description |
|---|---|
| `name` | Parameter name. |
| `expression` | Fusion expression, with units. |
| `comment` | Comment shown in Change Parameters. |

**Since** 1.0.0

## Functions

### `fmt(value: float) -> str` {#liana-core-params-fmt}

Format a length in mm as a Fusion expression, e.g. `"4.2 mm"`.

| Parameter | Type | Description |
|---|---|---|
| `value` | `float` | Length in mm. |

**Returns** `str`  
**Since** 1.0.0

### `make_params(s: Settings) -> list[ParamSpec]` {#liana-core-params-make-params}

Return the User Parameters for the settings, in dependency order.

Values the dialog sets become plain lengths; everything else is an
expression of other parameters, so a size changed later in Change
Parameters propagates through the whole design.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings. |

**Returns** `list[ParamSpec]` - Parameters; each one refers only to parameters listed before it.  
**Since** 1.0.0

## See also

- [`Liana.core`](Liana.core.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
