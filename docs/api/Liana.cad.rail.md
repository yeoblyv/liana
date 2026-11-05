---
id: api.liana.cad.rail
title: Liana.cad.rail
slug: /api/Liana.cad.rail
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.rail`

# `Liana.cad.rail`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Rail: the upper half of the holder, screwed to the table.

The rail is a plate with ears for the wood screws, end blocks that meet the
comb at the cable axis, an optional boss with a T-slot for the comb's center
pin, M3 channels and nut seats that pull the comb up.

## On this page

- [Functions](#functions)
  - [`build_rail`](#liana-cad-rail-build-rail)
- [See also](#see-also)
- [Changelog](#changelog)

## Functions

### `build_rail(ctx: BuildContext, comp: Component, s: Settings) -> None` {#liana-cad-rail-build-rail}

Model the rail in `comp`.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context; the parameters already exist. |
| `comp` | `Component` | Empty component that receives the rail. |
| `s` | `Settings` | Settings. |

**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
