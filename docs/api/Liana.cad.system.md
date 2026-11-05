---
id: api.liana.cad.system
title: Liana.cad.system
slug: /api/Liana.cad.system
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.system`

# `Liana.cad.system`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Build, update or rebuild a whole Liana system in a design.

## On this page

- [Constants](#constants)
  - [`SYSTEM_NAME`](#liana-cad-system-const-system-name)
  - [`TITLE`](#liana-cad-system-const-title)
  - [`PartBuilder`](#liana-cad-system-const-partbuilder)
- [Classes](#classes)
  - [`Progress`](#liana-cad-system-class-progress)
    - [`Progress.__init__`](#liana-cad-system-class-progress-init)
    - [`Progress.start`](#liana-cad-system-class-progress-start)
    - [`Progress.step`](#liana-cad-system-class-progress-step)
    - [`Progress.close`](#liana-cad-system-class-progress-close)
- [Functions](#functions)
  - [`seat_matrix`](#liana-cad-system-seat-matrix)
  - [`seat_holders`](#liana-cad-system-seat-holders)
  - [`reseat_holders`](#liana-cad-system-reseat-holders)
  - [`build_system`](#liana-cad-system-build-system)
  - [`generate`](#liana-cad-system-generate)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `SYSTEM_NAME` {#liana-cad-system-const-system-name}

Name of the top component of a system.

**Since** 1.0.0

### `TITLE` {#liana-cad-system-const-title}

Title of the progress dialog.

**Since** 1.0.0

### `PartBuilder` {#liana-cad-system-const-partbuilder}

Function that models one part into an empty component.

**Since** 1.0.0

## Classes

### `Progress` {#liana-cad-system-class-progress}

Progress dialog for builds.

One dialog is kept for the whole session: Fusion does not destroy a
dialog it created, so a new one per build would pile up hidden windows.

**Since** 1.0.0

#### `Progress.__init__(self, ui: UserInterface | None) -> None` {#liana-cad-system-class-progress-init}

Create the reporter; the dialog itself is created on first use.

| Parameter | Type | Description |
|---|---|---|
| `ui` | `UserInterface \| None` | Fusion user interface, or None to report nothing. |

**Since** 1.0.0

#### `Progress.start(self, total: int) -> None` {#liana-cad-system-class-progress-start}

Show the dialog for a build of `total` steps.

| Parameter | Type | Description |
|---|---|---|
| `total` | `int` | Number of steps the build reports. |

**Since** 1.0.0

#### `Progress.step(self, message: str) -> None` {#liana-cad-system-class-progress-step}

Advance by one step and show what is being built.

| Parameter | Type | Description |
|---|---|---|
| `message` | `str` | What is being built now. |

**Since** 1.0.0

#### `Progress.close(self) -> None` {#liana-cad-system-class-progress-close}

Hide the dialog.

**Since** 1.0.0

## Functions

### `seat_matrix(ctx: BuildContext, side: Side) -> object` {#liana-cad-system-seat-matrix}

Return the transform that puts a holder under one side of the frame.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context. |
| `side` | `Side` | Frame side. |

**Returns** `object`  
**Since** 1.0.0

### `seat_holders(ctx: BuildContext, system: Component, holder: Component, s: Settings) -> None` {#liana-cad-system-seat-holders}

Show the holder on the frame sides chosen in the settings.

Each copy is inserted straight at its final position; moving occurrences
afterwards would rely on position snapshots that do not survive recompute.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context. |
| `system` | `Component` | System component. |
| `holder` | `Component` | Holder component to copy. |
| `s` | `Settings` | Settings with the mount option. |

**Since** 1.0.0

### `reseat_holders(ctx: BuildContext, system_occ: Occurrence, s: Settings) -> None` {#liana-cad-system-reseat-holders}

Replace the holder copies on the frame after a size change.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context. |
| `system_occ` | `Occurrence` | System occurrence. |
| `s` | `Settings` | Settings with the mount option. |

**Since** 1.0.0

### `build_system(ctx: BuildContext, s: Settings, progress: Progress) -> Occurrence` {#liana-cad-system-build-system}

Build every enabled part into the design of `ctx`.

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `BuildContext` | Build context. |
| `s` | `Settings` | Settings. |
| `progress` | `Progress` | Progress reporter. |

**Returns** `Occurrence` - The system occurrence.  
**Since** 1.0.0

### `generate(app: Application, s: Settings, progress: Progress) -> tuple[str, BuildLog]` {#liana-cad-system-generate}

Apply the dialog settings to the active design.

- A design that already holds a system with the same layout gets its
  parameters updated in place.
- A different layout is rebuilt in the same design.
- Otherwise the system is built into the active design when it is an
  empty hybrid design, or into a new design.

| Parameter | Type | Description |
|---|---|---|
| `app` | `Application` | Fusion application. |
| `s` | `Settings` | Settings. |
| `progress` | `Progress` | Progress reporter. |

**Returns** `tuple[str, BuildLog]` - How the system was built, and the problems recorded.  
**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
