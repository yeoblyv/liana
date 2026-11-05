---
id: api.liana.storage
title: Liana.storage
slug: /api/Liana.storage
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.storage`

# `Liana.storage`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Files Liana keeps between sessions: the last dialog settings and the build log.

They live in the add-in's own folder, so uninstalling the add-in removes
them with it. An update replaces the folder, and the dialog then starts from
the default settings; systems in designs keep their own settings. When the
folder is read-only nothing is stored and the dialog starts from the
defaults.

## On this page

- [Constants](#constants)
  - [`SETTINGS_FILE`](#liana-storage-const-settings-file)
  - [`LOG_FILE`](#liana-storage-const-log-file)
- [Classes](#classes)
  - [`Storage`](#liana-storage-class-storage)
    - [`Storage.__init__`](#liana-storage-class-storage-init)
    - [`Storage.settings_path`](#liana-storage-class-storage-settings-path)
    - [`Storage.log_path`](#liana-storage-class-storage-log-path)
    - [`Storage.load_settings`](#liana-storage-class-storage-load-settings)
    - [`Storage.save_settings`](#liana-storage-class-storage-save-settings)
    - [`Storage.write_log`](#liana-storage-class-storage-write-log)
- [Functions](#functions)
  - [`atomic_write_text`](#liana-storage-atomic-write-text)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `SETTINGS_FILE` {#liana-storage-const-settings-file}

Last values of the dialog.

**Since** 1.0.0

### `LOG_FILE` {#liana-storage-const-log-file}

Report of the last build.

**Since** 1.0.0

## Classes

### `Storage` {#liana-storage-class-storage}

Reads and writes Liana's files in one folder.

| Attribute | Description |
|---|---|
| `folder` | Folder with the files. |

**Since** 1.0.0

#### `Storage.__init__(self, folder: Path) -> None` {#liana-storage-class-storage-init}

Create the store; nothing is touched on disk until a write.

| Parameter | Type | Description |
|---|---|---|
| `folder` | `Path` | Folder with the files. |

**Since** 1.0.0

#### `Storage.settings_path(self) -> Path` {#liana-storage-class-storage-settings-path}

Path of the last dialog settings.

**Returns** `Path`  
**Since** 1.0.0

#### `Storage.log_path(self) -> Path` {#liana-storage-class-storage-log-path}

Path of the build log.

**Returns** `Path`  
**Since** 1.0.0

#### `Storage.load_settings(self) -> Settings` {#liana-storage-class-storage-load-settings}

Return the last dialog settings, or the defaults.

A missing, unreadable or malformed file yields the defaults: losing
the last values is better than a dialog that does not open.

**Returns** `Settings`  
**Since** 1.0.0

#### `Storage.save_settings(self, s: Settings) -> bool` {#liana-storage-class-storage-save-settings}

Store the dialog settings.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings to store. |

**Returns** `bool` - Whether the file was written.  
**Since** 1.0.0

#### `Storage.write_log(self, text: str) -> Path | None` {#liana-storage-class-storage-write-log}

Write the build log.

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Log text. |

**Returns** `Path | None` - The log path, or None if it could not be written.  
**Since** 1.0.0

## Functions

### `atomic_write_text(path: Path, text: str) -> None` {#liana-storage-atomic-write-text}

Write a UTF-8 text file so that readers never see a partial file.

The text goes to a temporary file in the same folder, which then replaces
the target. On Windows the replace fails while another process (an
editor, a virus scanner) has the target open, so it is retried briefly.

| Parameter | Type | Description |
|---|---|---|
| `path` | `Path` | Target file; its folder is created when missing. |
| `text` | `str` | Content. |

**Raises** `OSError` - The file could not be written.  
**Since** 1.0.0

## See also

- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
