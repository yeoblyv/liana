---
id: api.liana.core.report
title: Liana.core.report
slug: /api/Liana.core.report
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.core.report`

# `Liana.core.report`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Texts shown to the user: dialog summary, build log and result message.

## On this page

- [Constants](#constants)
  - [`SHORT_BITE_MM`](#liana-core-report-const-short-bite-mm)
- [Classes](#classes)
  - [`BuildLog`](#liana-core-report-class-buildlog)
    - [`BuildLog.clear`](#liana-core-report-class-buildlog-clear)
    - [`BuildLog.has_problems`](#liana-core-report-class-buildlog-has-problems)
- [Functions](#functions)
  - [`summary_html`](#liana-core-report-summary-html)
  - [`log_text`](#liana-core-report-log-text)
  - [`result_message`](#liana-core-report-result-message)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `SHORT_BITE_MM` {#liana-core-report-const-short-bite-mm}

Wood screw engagement below which the summary suggests longer screws.

**Since** 1.0.0

## Classes

### `BuildLog` {#liana-core-report-class-buildlog}

What went wrong during one build, grouped by severity.

| Attribute | Description |
|---|---|
| `hard` | Parts that could not be finished, with a short traceback. |
| `soft` | Finishing features (fillets, chamfers, colors) that were skipped. |
| `dims` | Sketch dimensions Fusion refused. |
| `aligned` | Coordinates tied to an earlier point with the same expression. |

**Since** 1.0.0

#### `BuildLog.clear(self) -> None` {#liana-core-report-class-buildlog-clear}

Forget everything recorded so far.

**Since** 1.0.0

#### `BuildLog.has_problems(self) -> bool` {#liana-core-report-class-buildlog-has-problems}

Whether anything was skipped or failed.

**Returns** `bool`  
**Since** 1.0.0

## Functions

### `summary_html(s: Settings, problems: list[str], editing: bool) -> str` {#liana-core-report-summary-html}

Return the dialog summary as Fusion text-box HTML.

| Parameter | Type | Description |
|---|---|---|
| `s` | `Settings` | Settings shown in the dialog. |
| `problems` | `list[str]` | Output of `settings.problems`. |
| `editing` | `bool` | Whether the dialog edits a system already in the design. |

**Returns** `str` - Lines joined with `<br>`.  
**Since** 1.0.0

### `log_text(mode: str, s: Settings, log: BuildLog) -> str` {#liana-core-report-log-text}

Return the build log written after every build.

| Parameter | Type | Description |
|---|---|---|
| `mode` | `str` | How the system was built, e.g. `"built in this design"`. |
| `s` | `Settings` | Settings of the build. |
| `log` | `BuildLog` | Problems recorded during the build. |

**Returns** `str` - Plain text ending with a newline.  
**Since** 1.0.0

### `result_message(mode: str, log: BuildLog, log_path: str) -> str` {#liana-core-report-result-message}

Return the message shown when a build finishes.

| Parameter | Type | Description |
|---|---|---|
| `mode` | `str` | How the system was built. |
| `log` | `BuildLog` | Problems recorded during the build. |
| `log_path` | `str` | Where the full build log was written, or `""` if it could not be written. |

**Returns** `str` - Plain text for a message box.  
**Since** 1.0.0

## See also

- [`Liana.core`](Liana.core.md): the package this module belongs to.
- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
