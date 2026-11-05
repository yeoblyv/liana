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
```

#### `CommandCreated.notify(self, args: Any) -> None`

```text
Called by Fusion.
```

### `InputChanged(adsk.core.InputChangedEventHandler)`

```text
Forwards ``inputChanged``.
```

#### `InputChanged.__init__(self, callback: Callback, on_error: ErrorCallback) -> None`

```text
Wrap a callback.
```

#### `InputChanged.notify(self, args: Any) -> None`

```text
Called by Fusion.
```

### `ValidateInputs(adsk.core.ValidateInputsEventHandler)`

```text
Forwards ``validateInputs``; an error disables the OK button.
```

#### `ValidateInputs.__init__(self, callback: Callable[[], bool]) -> None`

```text
Wrap a callback that returns whether the inputs are valid.
```

#### `ValidateInputs.notify(self, args: Any) -> None`

```text
Called by Fusion.
```

### `CommandExecute(adsk.core.CommandEventHandler)`

```text
Forwards ``execute``.
```

#### `CommandExecute.__init__(self, callback: Callback, on_error: ErrorCallback) -> None`

```text
Wrap a callback.
```

#### `CommandExecute.notify(self, args: Any) -> None`

```text
Called by Fusion.
```

### `CustomEvent(adsk.core.CustomEventHandler)`

```text
Forwards a custom event.
```

#### `CustomEvent.__init__(self, callback: Callback, on_error: ErrorCallback) -> None`

```text
Wrap a callback.
```

#### `CustomEvent.notify(self, args: Any) -> None`

```text
Called by Fusion.
```
