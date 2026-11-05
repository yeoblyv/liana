---
id: api.liana.cad.appearance
title: Liana.cad.appearance
slug: /api/Liana.cad.appearance
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.appearance`

# `Liana.cad.appearance`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Part colors, so the rail, comb, frame and tie mount stay apart visually.

## On this page

- [Constants](#constants)
  - [`APPEARANCE_LIBRARY_ID`](#liana-cad-appearance-const-appearance-library-id)
  - [`BASE_APPEARANCES`](#liana-cad-appearance-const-base-appearances)
  - [`PART_COLORS`](#liana-cad-appearance-const-part-colors)
- [Functions](#functions)
  - [`part_appearance`](#liana-cad-appearance-part-appearance)
  - [`paint_parts`](#liana-cad-appearance-paint-parts)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `APPEARANCE_LIBRARY_ID` {#liana-cad-appearance-const-appearance-library-id}

Id of the Fusion Appearance Library.

**Since** 1.0.0

### `BASE_APPEARANCES` {#liana-cad-appearance-const-base-appearances}

Library appearances to copy, in order of preference.

**Since** 1.0.0

### `PART_COLORS` {#liana-cad-appearance-const-part-colors}

Component name to appearance name and RGB color.

**Since** 1.0.0

## Functions

### `part_appearance(app: Application, design: Design, name: str, rgb: tuple[int, int, int]) -> Any` {#liana-cad-appearance-part-appearance}

Return the named appearance of the design, creating it on first use.

A plastic appearance from the Fusion library is copied into the design and
its color property is set.

| Parameter | Type | Description |
|---|---|---|
| `app` | `Application` | Fusion application. |
| `design` | `Design` | Design that owns the appearance. |
| `name` | `str` | Appearance name. |
| `rgb` | `tuple[int, int, int]` | Color. |

**Returns** `Any` - The appearance.  
**Raises** `RuntimeError` - The copied appearance has no color property.  
**Since** 1.0.0

### `paint_parts(app: Application, design: Design) -> None` {#liana-cad-appearance-paint-parts}

Color every Liana part of the design: rail red, comb green, frame blue.

| Parameter | Type | Description |
|---|---|---|
| `app` | `Application` | Fusion application. |
| `design` | `Design` | Design with the Liana parts. |

**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
