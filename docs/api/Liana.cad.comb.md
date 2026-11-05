---
id: api.liana.cad.comb
title: Liana.cad.comb
slug: /api/Liana.cad.comb
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.comb`

# `Liana.cad.comb`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Comb: the lower half of the holder with the cable cradles.

The comb is a bar with end blocks that meet the rail at the cable axis,
optional raised teeth between the cradles and an optional T-pin that hooks
into the rail's slot so a long comb cannot sag in the middle.

## On this page

- [Functions](#functions)
  - [`build_comb`](#liana-cad-comb-build-comb)
- [See also](#see-also)
- [Changelog](#changelog)

## Functions

### `build_comb(ctx: BuildContext, comp: Component, s: Settings) -> None` {#liana-cad-comb-build-comb}

Model the comb in `comp`.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context; the parameters already exist. |
| `comp` | `Component` | Empty component that receives the comb. |
| `s` | `Settings` | Settings. |

**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
