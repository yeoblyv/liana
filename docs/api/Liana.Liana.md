---
id: api.liana.liana
title: Liana.Liana
slug: /api/Liana.Liana
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.Liana`

# `Liana.Liana`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Liana for Autodesk Fusion: parametric under-desk cable holders.

Fusion loads this file and calls `run` when the add-in starts and
`stop` when it stops. The command appears under Solid > Create > Liana.

## On this page

- [Functions](#functions)
  - [`run`](#liana-liana-run)
  - [`stop`](#liana-liana-stop)
- [See also](#see-also)
- [Changelog](#changelog)

## Functions

### `run(context: object) -> None` {#liana-liana-run}

Start the add-in (called by Fusion).

| Parameter | Type | Description |
|---|---|---|
| `context` | `object` | Start-up information from Fusion; not used. |

**Since** 1.0.0

### `stop(context: object) -> None` {#liana-liana-stop}

Stop the add-in (called by Fusion).

The add-in's other modules are dropped from the import cache, so that
Run after an update loads the new code instead of the modules Python
kept in memory.

| Parameter | Type | Description |
|---|---|---|
| `context` | `object` | Shut-down information from Fusion; not used. |

**Since** 1.0.0

## See also

- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
