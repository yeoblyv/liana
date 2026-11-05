---
id: api.liana.cad.design
title: Liana.cad.design
slug: /api/Liana.cad.design
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.cad.design`

# `Liana.cad.design`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Design-level helpers: documents, components, attributes and parameters.

## On this page

- [Constants](#constants)
  - [`ATTR_GROUP`](#liana-cad-design-const-attr-group)
  - [`SETTING_PARAMETERS`](#liana-cad-design-const-setting-parameters)
- [Functions](#functions)
  - [`tag`](#liana-cad-design-tag)
  - [`new_comp`](#liana-cad-design-new-comp)
  - [`find_system`](#liana-cad-design-find-system)
  - [`load_design_settings`](#liana-cad-design-load-design-settings)
  - [`save_design_settings`](#liana-cad-design-save-design-settings)
  - [`with_parameter_values`](#liana-cad-design-with-parameter-values)
  - [`upsert_params`](#liana-cad-design-upsert-params)
  - [`is_hybrid`](#liana-cad-design-is-hybrid)
  - [`is_empty`](#liana-cad-design-is-empty)
  - [`new_design`](#liana-cad-design-new-design)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `ATTR_GROUP` {#liana-cad-design-const-attr-group}

Attribute group of everything Liana stores in a design.

**Since** 1.0.0

### `SETTING_PARAMETERS` {#liana-cad-design-const-setting-parameters}

Dialog settings that are User Parameters of their own, by parameter name.

**Since** 1.0.0

## Functions

### `tag(occ: Occurrence, place: str) -> None` {#liana-cad-design-tag}

Mark an occurrence with its role, e.g. `"seat:S"`.

| Parameter | Type | Description |
|---|---|---|
| `occ` | `Occurrence` | Occurrence to mark. |
| `place` | `str` | Role, e.g. `"holder:"` or `"seat:S"`. |

**Since** 1.0.0

### `new_comp(parent: Component, name: str, place: str | None=None) -> Occurrence` {#liana-cad-design-new-comp}

Add a new component at identity under `parent`.

| Parameter | Type | Description |
|---|---|---|
| `parent` | `Component` | Parent component. |
| `name` | `str` | Component name. |
| `place` | `str \| None` | Optional role tag (see `tag`). |

**Returns** `Occurrence` - The new occurrence.  
**Since** 1.0.0

### `find_system(design: Design | None) -> Occurrence | None` {#liana-cad-design-find-system}

Return the Liana system occurrence of a design, if there is one.

| Parameter | Type | Description |
|---|---|---|
| `design` | `Design \| None` | Design to search, or None. |

**Returns** `Occurrence | None`  
**Since** 1.0.0

### `load_design_settings(design: Design) -> Settings | None` {#liana-cad-design-load-design-settings}

Return the settings stored in a design, or None if there are none.

The stored JSON is untrusted: the design may come from anyone.

| Parameter | Type | Description |
|---|---|---|
| `design` | `Design` | Design that may hold a system. |

**Returns** `Settings | None`  
**Since** 1.0.0

### `save_design_settings(design: Design, s: Settings) -> None` {#liana-cad-design-save-design-settings}

Store the settings in the design, so running Liana again edits it.

| Parameter | Type | Description |
|---|---|---|
| `design` | `Design` | Design that holds the system. |
| `s` | `Settings` | Settings of the system. |

**Since** 1.0.0

### `with_parameter_values(design: Design, s: Settings) -> Settings` {#liana-cad-design-with-parameter-values}

Return the settings with the sizes the design's User Parameters hold now.

A size changed in Change Parameters is not in the settings stored with
the system; without this the next Generate would set it back.

| Parameter | Type | Description |
|---|---|---|
| `design` | `Design` | Design with a Liana system. |
| `s` | `Settings` | Settings stored with the system. |

**Returns** `Settings` - The settings, with every in-range parameter value taken over.  
**Since** 1.0.0

### `upsert_params(design: Design, s: Settings) -> int` {#liana-cad-design-upsert-params}

Create missing User Parameters and update the ones that differ.

Changed parameters are set in one call, so the design recomputes once.

| Parameter | Type | Description |
|---|---|---|
| `design` | `Design` | Design to update. |
| `s` | `Settings` | Settings. |

**Returns** `int` - Number of parameters whose expression changed.  
**Since** 1.0.0

### `is_hybrid(design: Design) -> bool` {#liana-cad-design-is-hybrid}

Return whether a design can hold several components (hybrid intent).

| Parameter | Type | Description |
|---|---|---|
| `design` | `Design` | Design to check. |

**Returns** `bool`  
**Since** 1.0.0

### `is_empty(design: Design) -> bool` {#liana-cad-design-is-empty}

Return whether the root component has no occurrences, bodies or sketches.

| Parameter | Type | Description |
|---|---|---|
| `design` | `Design` | Design to check. |

**Returns** `bool`  
**Since** 1.0.0

### `new_design(app: Application) -> Design` {#liana-cad-design-new-design}

Open a new hybrid design document and return its design.

| Parameter | Type | Description |
|---|---|---|
| `app` | `Application` | Fusion application. |

**Returns** `Design`  
**Since** 1.0.0

## See also

- [`Liana.cad`](Liana.cad.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
