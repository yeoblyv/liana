# `Liana.handlers`

Fusion event handler classes that forward to plain callables.

Fusion calls ``notify`` on a handler object and drops any exception raised
there without telling the user, so every handler catches errors and passes
them to an error callback. Fusion does not keep handler objects alive, so
the add-in holds every handler for as long as it is connected.

## Constants

### `Callback`

Receives the event arguments.

### `ErrorCallback`

Called inside ``except`` when a callback raised; reads the active exception.

## Classes

### `CommandCreated(adsk.core.CommandCreatedEventHandler)`

```text
Forwards ``commandCreated``.
```

#### `CommandCreated.__init__(self, callback: Callback, on_error: ErrorCallback) -> None`

```text
Wrap a callback.

Args:
    callback: Receives the event arguments.
    on_error: Called when ``callback`` raises.
```

#### `CommandCreated.notify(self, args: Any) -> None`

```text
Pass the event arguments to the callback.
```

### `InputChanged(adsk.core.InputChangedEventHandler)`

```text
Forwards ``inputChanged``.
```

#### `InputChanged.__init__(self, callback: Callback, on_error: ErrorCallback) -> None`

```text
Wrap a callback.

Args:
    callback: Receives the event arguments.
    on_error: Called when ``callback`` raises.
```

#### `InputChanged.notify(self, args: Any) -> None`

```text
Pass the event arguments to the callback.
```

### `ValidateInputs(adsk.core.ValidateInputsEventHandler)`

```text
Forwards ``validateInputs``; an error disables the OK button.
```

#### `ValidateInputs.__init__(self, callback: Callable[[], bool]) -> None`

```text
Wrap a callback.

Args:
    callback: Returns whether the inputs are valid.
```

#### `ValidateInputs.notify(self, args: Any) -> None`

```text
Set ``args.areInputsValid`` from the callback.
```

### `CommandExecute(adsk.core.CommandEventHandler)`

```text
Forwards ``execute``.
```

#### `CommandExecute.__init__(self, callback: Callback, on_error: ErrorCallback) -> None`

```text
Wrap a callback.

Args:
    callback: Receives the event arguments.
    on_error: Called when ``callback`` raises.
```

#### `CommandExecute.notify(self, args: Any) -> None`

```text
Pass the event arguments to the callback.
```

### `CustomEvent(adsk.core.CustomEventHandler)`

```text
Forwards a custom event.
```

#### `CustomEvent.__init__(self, callback: Callback, on_error: ErrorCallback) -> None`

```text
Wrap a callback.

Args:
    callback: Receives the event arguments.
    on_error: Called when ``callback`` raises.
```

#### `CustomEvent.notify(self, args: Any) -> None`

```text
Pass the event arguments to the callback.
```
