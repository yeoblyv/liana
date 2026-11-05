---
id: api.liana.cad.frame
title: Liana.cad.frame
slug: /api/Liana.cad.frame
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.frame`

# `Liana.cad.frame`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

X-frame: a square frame that carries holders on up to four sides.

The frame is modelled around `(0, 0, FRAME_Z)` in its own component with
the occurrence at identity, so no frame feature can reach the holder or the
tie mount, at build time or on any later recompute.

## On this page

- [Functions](#functions)
  - [`build_frame`](#liana-cad-frame-build-frame)
- [See also](#see-also)
- [Changelog](#changelog)

## Functions

### `build_frame(ctx: BuildContext, comp: Component, s: Settings) -> None` {#liana-cad-frame-build-frame}

Model the frame in `comp`.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context; the parameters already exist. |
| `comp` | `Component` | Empty component that receives the frame. |
| `s` | `Settings` | Settings. |

**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
