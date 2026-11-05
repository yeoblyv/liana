---
id: api.liana.dialog
title: Liana.dialog
slug: /api/Liana.dialog
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.dialog`

# `Liana.dialog`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

The Liana dialog: inputs, their mapping to settings and the live summary.

## On this page

- [Constants](#constants)
  - [`FieldKind`](#liana-dialog-const-fieldkind)
  - [`RESET_ID`](#liana-dialog-const-reset-id)
  - [`PRIVACY_ID`](#liana-dialog-const-privacy-id)
  - [`PRIVACY_GROUP_ID`](#liana-dialog-const-privacy-group-id)
  - [`POLICY_TEXT_ID`](#liana-dialog-const-policy-text-id)
  - [`SUMMARY_ID`](#liana-dialog-const-summary-id)
  - [`DIALOG_SIZE`](#liana-dialog-const-dialog-size)
  - [`GROUPS`](#liana-dialog-const-groups)
  - [`KINDS`](#liana-dialog-const-kinds)
- [Classes](#classes)
  - [`Field`](#liana-dialog-class-field)
  - [`Group`](#liana-dialog-class-group)
  - [`SettingsDialog`](#liana-dialog-class-settingsdialog)
    - [`SettingsDialog.__init__`](#liana-dialog-class-settingsdialog-init)
    - [`SettingsDialog.build`](#liana-dialog-class-settingsdialog-build)
    - [`SettingsDialog.read`](#liana-dialog-class-settingsdialog-read)
    - [`SettingsDialog.write`](#liana-dialog-class-settingsdialog-write)
    - [`SettingsDialog.problems`](#liana-dialog-class-settingsdialog-problems)
    - [`SettingsDialog.refresh`](#liana-dialog-class-settingsdialog-refresh)
    - [`SettingsDialog.inputs_valid`](#liana-dialog-class-settingsdialog-inputs-valid)
    - [`SettingsDialog.input_changed`](#liana-dialog-class-settingsdialog-input-changed)
- [Functions](#functions)
  - [`mount_label`](#liana-dialog-mount-label)
  - [`mount_key`](#liana-dialog-mount-key)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `FieldKind` {#liana-dialog-const-fieldkind}

How a setting is shown: spinner, length, check box or the mount list.

**Since** 1.0.0

### `RESET_ID` {#liana-dialog-const-reset-id}

Input id of the reset button.

**Since** 1.0.0

### `PRIVACY_ID` {#liana-dialog-const-privacy-id}

Input id of the button that opens the online privacy policy.

**Since** 1.0.0

### `PRIVACY_GROUP_ID` {#liana-dialog-const-privacy-group-id}

Input id of the collapsed group with the privacy policy text.

**Since** 1.0.0

### `POLICY_TEXT_ID` {#liana-dialog-const-policy-text-id}

Input id of the text box with the privacy policy.

**Since** 1.0.0

### `SUMMARY_ID` {#liana-dialog-const-summary-id}

Input id of the summary text box.

**Since** 1.0.0

### `DIALOG_SIZE` {#liana-dialog-const-dialog-size}

Initial dialog width and height in pixels.

**Since** 1.0.0

### `GROUPS` {#liana-dialog-const-groups}

Dialog layout, top to bottom.

**Since** 1.0.0

### `KINDS` {#liana-dialog-const-kinds}

Input type of every settings key shown in the dialog.

**Since** 1.0.0

## Classes

### `Field(NamedTuple)` {#liana-dialog-class-field}

One dialog input.

| Attribute | Description |
|---|---|
| `key` | Settings key, also the input id. |
| `label` | Label shown left of the input. |
| `kind` | Input type. |
| `tooltip` | Tooltip, empty for none. |

**Since** 1.0.0

### `Group(NamedTuple)` {#liana-dialog-class-group}

A collapsible group of inputs.

| Attribute | Description |
|---|---|
| `id` | Input id of the group. |
| `label` | Group title. |
| `expanded` | Whether the group starts expanded. |
| `fields` | Inputs of the group. |

**Since** 1.0.0

### `SettingsDialog` {#liana-dialog-class-settingsdialog}

The inputs of one open dialog.

| Attribute | Description |
|---|---|
| `editing` | Whether the dialog edits a system already in the design. |

**Since** 1.0.0

#### `SettingsDialog.__init__(self, editing: bool, open_url: Callable[[str], None]) -> None` {#liana-dialog-class-settingsdialog-init}

Prepare a dialog; inputs are created by `build`.

| Parameter | Type | Description |
|---|---|---|
| `editing` | `bool` | Whether the dialog edits a system already in the design. |
| `open_url` | `Callable[[str], None]` | Opens a web page in the browser. |

**Since** 1.0.0

#### `SettingsDialog.build(self, inputs: Any, s: Settings) -> None` {#liana-dialog-class-settingsdialog-build}

Create every input of the dialog, filled from the settings.

| Parameter | Type | Description |
|---|---|---|
| `inputs` | `Any` | `CommandInputs` of the command. |
| `s` | `Settings` | Initial values. |

**Since** 1.0.0

#### `SettingsDialog.read(self) -> Settings` {#liana-dialog-class-settingsdialog-read}

Return the settings currently shown in the dialog.

**Returns** `Settings`  
**Since** 1.0.0

#### `SettingsDialog.write(self, s: Settings) -> None` {#liana-dialog-class-settingsdialog-write}

Show the given settings in the dialog.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings to show. |

**Since** 1.0.0

#### `SettingsDialog.problems(self, s: Settings) -> list[str]` {#liana-dialog-class-settingsdialog-problems}

Return what prevents building the settings.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings to check. |

**Returns** `list[str]`  
**Since** 1.0.0

#### `SettingsDialog.refresh(self, s: Settings | None=None) -> bool` {#liana-dialog-class-settingsdialog-refresh}

Update enabled inputs and the summary.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings \| None` | Settings to show; read from the inputs when omitted. |

**Returns** `bool` - Whether the settings can be built.  
**Since** 1.0.0

#### `SettingsDialog.inputs_valid(self) -> bool` {#liana-dialog-class-settingsdialog-inputs-valid}

Return whether every length is a valid expression and the settings build.

**Returns** `bool`  
**Since** 1.0.0

#### `SettingsDialog.input_changed(self, input_id: str) -> None` {#liana-dialog-class-settingsdialog-input-changed}

React to a changed input: buttons act, then the summary is refreshed.

| Parameter | Type | Description |
|---|---|---|
| `input_id` | `str` | Id of the input that changed. |

**Since** 1.0.0

## Functions

### `mount_label(key: Mount) -> str` {#liana-dialog-mount-label}

Return the dialog label of a mount option.

| Parameter | Type | Description |
|---|---|---|
| `key` | `Mount` | Mount option. |

**Returns** `str`  
**Since** 1.0.0

### `mount_key(label: str | None) -> Mount` {#liana-dialog-mount-key}

Return the mount option for a dialog label (`"none"` if unknown).

| Parameter | Type | Description |
|---|---|---|
| `label` | `str \| None` | Dialog label, or None when nothing is selected. |

**Returns** `Mount`  
**Since** 1.0.0

## See also

- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
