---
id: api.liana.cad.tie_mount
title: Liana.cad.tie_mount
slug: /api/Liana.cad.tie_mount
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.tie_mount`

# `Liana.cad.tie_mount`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Tie mount: a small pad with two zip-tie tunnels and one screw.

The tie mount is modelled around `(0, 0, TIE_Z)` in its own component with
the occurrence at identity, so its tunnels can never cut the holder or the
frame.

## On this page

- [Functions](#functions)
  - [`build_tie`](#liana-cad-tie-mount-build-tie)
- [See also](#see-also)
- [Changelog](#changelog)

## Functions

### `build_tie(ctx: BuildContext, comp: Component, s: Settings) -> None` {#liana-cad-tie-mount-build-tie}

Model the tie mount in `comp`.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context; the parameters already exist. |
| `comp` | `Component` | Empty component that receives the tie mount. |
| `s` | `Settings` | Settings (the sizes come from the parameters). |

**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
