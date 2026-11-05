---
id: api.liana.addin
title: Liana.addin
slug: /api/Liana.addin
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.addin`

# `Liana.addin`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

The add-in: registers the Liana command and runs builds.

## On this page

- [Constants](#constants)
  - [`ADDIN_DIR`](#liana-addin-const-addin-dir)
  - [`RESOURCES_DIR`](#liana-addin-const-resources-dir)
  - [`COMMAND_ID`](#liana-addin-const-command-id)
  - [`COMMAND_NAME`](#liana-addin-const-command-name)
  - [`COMMAND_TOOLTIP`](#liana-addin-const-command-tooltip)
  - [`PANEL_ID`](#liana-addin-const-panel-id)
  - [`BUILD_EVENT_ID`](#liana-addin-const-build-event-id)
- [Classes](#classes)
  - [`LianaAddIn`](#liana-addin-class-lianaaddin)
    - [`LianaAddIn.__init__`](#liana-addin-class-lianaaddin-init)
    - [`LianaAddIn.start`](#liana-addin-class-lianaaddin-start)
    - [`LianaAddIn.stop`](#liana-addin-class-lianaaddin-stop)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `ADDIN_DIR` {#liana-addin-const-addin-dir}

Folder of the installed add-in.

**Since** 1.0.0

### `RESOURCES_DIR` {#liana-addin-const-resources-dir}

Command icons.

**Since** 1.0.0

### `COMMAND_ID` {#liana-addin-const-command-id}

Id of the command definition.

**Since** 1.0.0

### `COMMAND_NAME` {#liana-addin-const-command-name}

Command name shown in the toolbar.

**Since** 1.0.0

### `COMMAND_TOOLTIP` {#liana-addin-const-command-tooltip}

Toolbar tooltip.

**Since** 1.0.0

### `PANEL_ID` {#liana-addin-const-panel-id}

Toolbar panel that shows the command (Solid > Create).

**Since** 1.0.0

### `BUILD_EVENT_ID` {#liana-addin-const-build-event-id}

Custom event that runs a build after the dialog has closed.

**Since** 1.0.0

## Classes

### `LianaAddIn` {#liana-addin-class-lianaaddin}

Everything the add-in registers in Fusion, and the handlers behind it.

**Since** 1.0.0

#### `LianaAddIn.__init__(self, app: Application, storage: Storage, open_url: Callable[[str], object]) -> None` {#liana-addin-class-lianaaddin-init}

Prepare the add-in; nothing is registered until `start`.

| Parameter | Type | Description |
|---|---|---|
| `app` | `Application` | Fusion application. |
| `storage` | `Storage` | Where the last settings and the build log are kept. |
| `open_url` | `Callable[[str], object]` | Opens a web page in the browser and returns whether a browser accepted it, like `webbrowser.open`. |

**Since** 1.0.0

#### `LianaAddIn.start(self) -> None` {#liana-addin-class-lianaaddin-start}

Add the command to Solid > Create and connect the build event.

**Since** 1.0.0

#### `LianaAddIn.stop(self) -> None` {#liana-addin-class-lianaaddin-stop}

Remove everything `start` added; never raises.

**Since** 1.0.0

## See also

- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
