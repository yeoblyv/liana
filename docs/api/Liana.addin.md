# `Liana.addin`

The add-in: registers the Liana command and runs builds.

## Constants

### `ADDIN_DIR`

Folder of the installed add-in.

### `RESOURCES_DIR`

Command icons.

### `COMMAND_ID`

Id of the command definition.

### `COMMAND_NAME`

Command name shown in the toolbar.

### `COMMAND_TOOLTIP`

Toolbar tooltip.

### `PANEL_ID`

Toolbar panel that shows the command (Solid > Create).

### `BUILD_EVENT_ID`

Custom event that runs a build after the dialog has closed.

## Classes

### `LianaAddIn`

```text
Everything the add-in registers in Fusion, and the handlers behind it.
```

#### `LianaAddIn.__init__(self, app: Application, storage: Storage, open_url: Callable[[str], object]) -> None`

```text
Prepare the add-in; nothing is registered until :meth:`start`.

Args:
    app: Fusion application.
    storage: Where the last settings and the build log are kept.
    open_url: Opens a web page in the browser and returns whether a
        browser accepted it, like :func:`webbrowser.open`.
```

#### `LianaAddIn.start(self) -> None`

```text
Add the command to Solid > Create and connect the build event.
```

#### `LianaAddIn.stop(self) -> None`

```text
Remove everything :meth:`start` added; never raises.
```
