# `Liana.dialog`

The Liana dialog: inputs, their mapping to settings and the live summary.

## Constants

### `FieldKind`

How a setting is shown: spinner, length, check box or the mount list.

### `RESET_ID`

Input id of the reset button.

### `PRIVACY_ID`

Input id of the privacy policy button.

### `SUMMARY_ID`

Input id of the summary text box.

### `DIALOG_SIZE`

Initial dialog width and height in pixels.

### `GROUPS`

Dialog layout, top to bottom.

### `KINDS`

Input type of every settings key shown in the dialog.

## Classes

### `Field(NamedTuple)`

```text
One dialog input.

Attributes:
    key: Settings key, also the input id.
    label: Label shown left of the input.
    kind: Input type.
    tooltip: Tooltip, empty for none.
```

### `Group(NamedTuple)`

```text
A collapsible group of inputs.

Attributes:
    id: Input id of the group.
    label: Group title.
    expanded: Whether the group starts expanded.
    fields: Inputs of the group.
```

### `SettingsDialog`

```text
The inputs of one open dialog.

Attributes:
    editing: Whether the dialog edits a system already in the design.
```

#### `SettingsDialog.__init__(self, editing: bool, show_policy: Callable[[], None]) -> None`

```text
Prepare a dialog; inputs are created by :meth:`build`.

Args:
    editing: Whether the dialog edits a system already in the design.
    show_policy: Shows the privacy policy.
```

#### `SettingsDialog.build(self, inputs: Any, s: Settings) -> None`

```text
Create every input of the dialog, filled from the settings.

Args:
    inputs: ``CommandInputs`` of the command.
    s: Initial values.
```

#### `SettingsDialog.read(self) -> Settings`

```text
Return the settings currently shown in the dialog.
```

#### `SettingsDialog.write(self, s: Settings) -> None`

```text
Show the given settings in the dialog.
```

#### `SettingsDialog.problems(self, s: Settings) -> list[str]`

```text
Return what prevents building the settings.
```

#### `SettingsDialog.refresh(self, s: Settings | None=None) -> bool`

```text
Update enabled inputs and the summary.

Args:
    s: Settings to show; read from the inputs when omitted.

Returns:
    Whether the settings can be built.
```

#### `SettingsDialog.inputs_valid(self) -> bool`

```text
Return whether every length is a valid expression and the settings build.
```

#### `SettingsDialog.input_changed(self, input_id: str) -> None`

```text
React to a changed input: buttons act, then the summary is refreshed.
```

## Functions

### `mount_label(key: Mount) -> str`

```text
Return the dialog label of a mount option.
```

### `mount_key(label: str | None) -> Mount`

```text
Return the mount option for a dialog label (``"none"`` if unknown).
```
