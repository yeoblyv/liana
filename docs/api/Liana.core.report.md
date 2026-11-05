# `Liana.core.report`

Texts shown to the user: dialog summary, build log and result message.

## Constants

### `SHORT_BITE_MM`

Wood screw engagement below which the summary suggests longer screws.

## Classes

### `BuildLog`

```text
What went wrong during one build, grouped by severity.

Attributes:
    hard: Parts that could not be finished, with a short traceback.
    soft: Finishing features (fillets, chamfers, colours) that were skipped.
    dims: Sketch dimensions Fusion refused.
    aligned: Coordinates tied to an earlier point with the same expression.
```

#### `BuildLog.clear(self) -> None`

```text
Forget everything recorded so far.
```

#### `BuildLog.has_problems(self) -> bool`

```text
Whether anything was skipped or failed.
```

## Functions

### `summary_html(s: Settings, problems: list[str], editing: bool) -> str`

```text
Return the dialog summary as Fusion text-box HTML.

Args:
    s: Settings shown in the dialog.
    problems: Output of :func:`.settings.problems`.
    editing: Whether the dialog edits a system already in the design.

Returns:
    Lines joined with ``<br>``.
```

### `log_text(mode: str, s: Settings, log: BuildLog) -> str`

```text
Return the build log written after every build.

Args:
    mode: How the system was built, e.g. ``"built in this design"``.
    s: Settings of the build.
    log: Problems recorded during the build.

Returns:
    Plain text ending with a newline.
```

### `result_message(mode: str, log: BuildLog, log_path: str) -> str`

```text
Return the message shown when a build finishes.

Args:
    mode: How the system was built.
    log: Problems recorded during the build.
    log_path: Where the full build log was written, or ``""`` if it could
        not be written.

Returns:
    Plain text for a message box.
```
