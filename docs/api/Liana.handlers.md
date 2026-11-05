---
id: api.liana.handlers
title: Liana.handlers
slug: /api/Liana.handlers
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.handlers`

# `Liana.handlers`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Fusion event handler classes that forward to plain callables.

Fusion calls `notify` on a handler object and drops any exception raised
there without telling the user, so every handler catches errors and passes
them to an error callback. Fusion does not keep handler objects alive, so
the add-in holds every handler for as long as it is connected.

## On this page

- [Constants](#constants)
  - [`Callback`](#liana-handlers-const-callback)
  - [`ErrorCallback`](#liana-handlers-const-errorcallback)
- [Classes](#classes)
  - [`CommandCreated`](#liana-handlers-class-commandcreated)
    - [`CommandCreated.__init__`](#liana-handlers-class-commandcreated-init)
    - [`CommandCreated.notify`](#liana-handlers-class-commandcreated-notify)
  - [`InputChanged`](#liana-handlers-class-inputchanged)
    - [`InputChanged.__init__`](#liana-handlers-class-inputchanged-init)
    - [`InputChanged.notify`](#liana-handlers-class-inputchanged-notify)
  - [`ValidateInputs`](#liana-handlers-class-validateinputs)
    - [`ValidateInputs.__init__`](#liana-handlers-class-validateinputs-init)
    - [`ValidateInputs.notify`](#liana-handlers-class-validateinputs-notify)
  - [`CommandExecute`](#liana-handlers-class-commandexecute)
    - [`CommandExecute.__init__`](#liana-handlers-class-commandexecute-init)
    - [`CommandExecute.notify`](#liana-handlers-class-commandexecute-notify)
  - [`CustomEvent`](#liana-handlers-class-customevent)
    - [`CustomEvent.__init__`](#liana-handlers-class-customevent-init)
    - [`CustomEvent.notify`](#liana-handlers-class-customevent-notify)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `Callback` {#liana-handlers-const-callback}

Receives the event arguments.

**Since** 1.0.0

### `ErrorCallback` {#liana-handlers-const-errorcallback}

Called inside `except` when a callback raised; reads the active exception.

**Since** 1.0.0

## Classes

### `CommandCreated(adsk.core.CommandCreatedEventHandler)` {#liana-handlers-class-commandcreated}

Forwards `commandCreated`.

**Since** 1.0.0

#### `CommandCreated.__init__(self, callback: Callback, on_error: ErrorCallback) -> None` {#liana-handlers-class-commandcreated-init}

Wrap a callback.

| Parameter | Type | Description |
|---|---|---|
| `callback` | `Callback` | Receives the event arguments. |
| `on_error` | `ErrorCallback` | Called when `callback` raises. |

**Since** 1.0.0

#### `CommandCreated.notify(self, args: Any) -> None` {#liana-handlers-class-commandcreated-notify}

Pass the event arguments to the callback.

| Parameter | Type | Description |
|---|---|---|
| `args` | `Any` | Event arguments from Fusion. |

**Since** 1.0.0

### `InputChanged(adsk.core.InputChangedEventHandler)` {#liana-handlers-class-inputchanged}

Forwards `inputChanged`.

**Since** 1.0.0

#### `InputChanged.__init__(self, callback: Callback, on_error: ErrorCallback) -> None` {#liana-handlers-class-inputchanged-init}

Wrap a callback.

| Parameter | Type | Description |
|---|---|---|
| `callback` | `Callback` | Receives the event arguments. |
| `on_error` | `ErrorCallback` | Called when `callback` raises. |

**Since** 1.0.0

#### `InputChanged.notify(self, args: Any) -> None` {#liana-handlers-class-inputchanged-notify}

Pass the event arguments to the callback.

| Parameter | Type | Description |
|---|---|---|
| `args` | `Any` | Event arguments from Fusion. |

**Since** 1.0.0

### `ValidateInputs(adsk.core.ValidateInputsEventHandler)` {#liana-handlers-class-validateinputs}

Forwards `validateInputs`; an error disables the OK button.

**Since** 1.0.0

#### `ValidateInputs.__init__(self, callback: Callable[[], bool]) -> None` {#liana-handlers-class-validateinputs-init}

Wrap a callback.

| Parameter | Type | Description |
|---|---|---|
| `callback` | `Callable[[], bool]` | Returns whether the inputs are valid. |

**Since** 1.0.0

#### `ValidateInputs.notify(self, args: Any) -> None` {#liana-handlers-class-validateinputs-notify}

Set `args.areInputsValid` from the callback.

| Parameter | Type | Description |
|---|---|---|
| `args` | `Any` | Event arguments from Fusion. |

**Since** 1.0.0

### `CommandExecute(adsk.core.CommandEventHandler)` {#liana-handlers-class-commandexecute}

Forwards `execute`.

**Since** 1.0.0

#### `CommandExecute.__init__(self, callback: Callback, on_error: ErrorCallback) -> None` {#liana-handlers-class-commandexecute-init}

Wrap a callback.

| Parameter | Type | Description |
|---|---|---|
| `callback` | `Callback` | Receives the event arguments. |
| `on_error` | `ErrorCallback` | Called when `callback` raises. |

**Since** 1.0.0

#### `CommandExecute.notify(self, args: Any) -> None` {#liana-handlers-class-commandexecute-notify}

Pass the event arguments to the callback.

| Parameter | Type | Description |
|---|---|---|
| `args` | `Any` | Event arguments from Fusion. |

**Since** 1.0.0

### `CustomEvent(adsk.core.CustomEventHandler)` {#liana-handlers-class-customevent}

Forwards a custom event.

**Since** 1.0.0

#### `CustomEvent.__init__(self, callback: Callback, on_error: ErrorCallback) -> None` {#liana-handlers-class-customevent-init}

Wrap a callback.

| Parameter | Type | Description |
|---|---|---|
| `callback` | `Callback` | Receives the event arguments. |
| `on_error` | `ErrorCallback` | Called when `callback` raises. |

**Since** 1.0.0

#### `CustomEvent.notify(self, args: Any) -> None` {#liana-handlers-class-customevent-notify}

Pass the event arguments to the callback.

| Parameter | Type | Description |
|---|---|---|
| `args` | `Any` | Event arguments from Fusion. |

**Since** 1.0.0

## See also

- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
