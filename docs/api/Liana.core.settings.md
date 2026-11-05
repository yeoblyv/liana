---
id: api.liana.core.settings
title: Liana.core.settings
slug: /api/Liana.core.settings
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.core.settings`

# `Liana.core.settings`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Dialog settings: defaults, limits, validation and loading from untrusted JSON.

## On this page

- [Constants](#constants)
  - [`Mount`](#liana-core-settings-const-mount)
  - [`Side`](#liana-core-settings-const-side)
  - [`SETTINGS_VERSION`](#liana-core-settings-const-settings-version)
  - [`NUT_H`](#liana-core-settings-const-nut-h)
  - [`SIDES`](#liana-core-settings-const-sides)
  - [`MOUNTS`](#liana-core-settings-const-mounts)
  - [`MOUNT_SIDES`](#liana-core-settings-const-mount-sides)
  - [`DEFAULTS`](#liana-core-settings-const-defaults)
  - [`LIMITS`](#liana-core-settings-const-limits)
  - [`MAX_CRADLES`](#liana-core-settings-const-max-cradles)
- [Classes](#classes)
  - [`Settings`](#liana-core-settings-class-settings)
- [Functions](#functions)
  - [`defaults`](#liana-core-settings-defaults)
  - [`finite_number`](#liana-core-settings-finite-number)
  - [`migrate`](#liana-core-settings-migrate)
  - [`from_mapping`](#liana-core-settings-from-mapping)
  - [`in_limits`](#liana-core-settings-in-limits)
  - [`problems`](#liana-core-settings-problems)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `Mount` {#liana-core-settings-const-mount}

Which frame sides show a holder in the design preview.

**Since** 1.0.0

### `Side` {#liana-core-settings-const-side}

Frame side: south, east, north, west.

**Since** 1.0.0

### `SETTINGS_VERSION` {#liana-core-settings-const-settings-version}

Version written with saved settings; older files are migrated on load.

**Since** 1.0.0

### `NUT_H` {#liana-core-settings-const-nut-h}

M3 nut slot height in mm: a 2.4 mm nut plus room for a sagging bridge.

**Since** 1.0.0

### `SIDES` {#liana-core-settings-const-sides}

Frame sides in build order.

**Since** 1.0.0

### `MOUNTS` {#liana-core-settings-const-mounts}

Mount options: key, dialog label, frame sides that get a holder.

**Since** 1.0.0

### `MOUNT_SIDES` {#liana-core-settings-const-mount-sides}

Frame sides for each mount option.

**Since** 1.0.0

### `DEFAULTS` {#liana-core-settings-const-defaults}

Settings of a fresh install.

**Since** 1.0.0

### `LIMITS` {#liana-core-settings-const-limits}

Allowed range (inclusive) of every numeric setting.

**Since** 1.0.0

### `MAX_CRADLES` {#liana-core-settings-const-max-cradles}

Largest cradle count the dialog offers.

**Since** 1.0.0

## Classes

### `Settings(TypedDict)` {#liana-core-settings-class-settings}

Everything the dialog sets; lengths in millimeters.

**Since** 1.0.0

## Functions

### `defaults() -> Settings` {#liana-core-settings-defaults}

Return a fresh copy of the default settings.

**Returns** `Settings`  
**Since** 1.0.0

### `finite_number(value: object) -> float | None` {#liana-core-settings-finite-number}

Return `value` as a finite float, or None.

Booleans, strings, NaN, infinities and integers too large for a float
are rejected, so untrusted JSON cannot smuggle them into the arithmetic.

| Parameter | Type | Description |
|---|---|---|
| `value` | `object` | Value from JSON. |

**Returns** `float | None`  
**Since** 1.0.0

### `migrate(raw: dict[str, Any]) -> dict[str, Any]` {#liana-core-settings-migrate}

Upgrade settings saved by an older version, in place.

Version 1 used a 5.8 mm nut slot that is too tight for printed parts; a
stored value equal to that old default is raised to the current one.

| Parameter | Type | Description |
|---|---|---|
| `raw` | `dict[str, Any]` | Settings as read from JSON. |

**Returns** `dict[str, Any]` - The same dictionary, tagged with `SETTINGS_VERSION`.  
**Since** 1.0.0

### `from_mapping(raw: object, within_limits: bool=False) -> Settings` {#liana-core-settings-from-mapping}

Build settings from data of unknown quality, keeping well-typed known keys.

Unknown keys are dropped and every value is checked against the type of
its default; numbers must be finite.

Values read back from files, designs or events pass `within_limits`,
so an out-of-range value (a cradle count of a billion, say) is replaced
by the default before any arithmetic runs on it. The dialog leaves it
off: there an out-of-range value must stay visible and be reported by
`problems`.

| Parameter | Type | Description |
|---|---|---|
| `raw` | `object` | Parsed JSON; anything that is not an object yields the defaults. |
| `within_limits` | `bool` | Also drop numbers outside `LIMITS`. |

**Returns** `Settings` - Complete settings.  
**Since** 1.0.0

### `in_limits(key: str, value: float) -> bool` {#liana-core-settings-in-limits}

Return whether a value is inside the dialog limits of its setting.

| Parameter | Type | Description |
|---|---|---|
| `key` | `str` | Settings key. |
| `value` | `float` | Value to check. |

**Returns** `bool`  
**Since** 1.0.0

### `problems(s: Settings, fits_bed: bool) -> list[str]` {#liana-core-settings-problems}

List what is wrong with the settings, in dialog wording.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings to check. |
| `fits_bed` | `bool` | Whether every part fits on the printer bed. |

**Returns** `list[str]` - Problems; empty when the settings can be built.  
**Since** 1.0.0

## See also

- [`Liana.core`](Liana.core.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
