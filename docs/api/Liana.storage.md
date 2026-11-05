# `Liana.storage`

Files Liana keeps between sessions: the last dialog settings and the build log.

They live in the per-user application data folder rather than next to the
code, because an add-in update replaces its own folder and the folder may be
read-only.

## Constants

### `APP_FOLDER`

Name of Liana's folder inside the user data folder.

### `SETTINGS_FILE`

Last values of the dialog.

### `LOG_FILE`

Report of the last build.

## Classes

### `Storage`

```text
Reads and writes Liana's files in one folder.

Attributes:
    folder: Folder with the files.
    legacy_folder: Folder where pre-release builds kept their settings
        (the add-in folder); read when the data folder has none yet.
```

#### `Storage.__init__(self, folder: Path, legacy_folder: Path | None=None) -> None`

```text
Create the store; nothing is touched on disk until a write.

Args:
    folder: Folder with the files.
    legacy_folder: Optional folder to read old settings from.
```

#### `Storage.for_user(cls, legacy_folder: Path | None=None) -> Storage`

```text
Return the store in the current user's data folder.
```

#### `Storage.settings_path(self) -> Path`

```text
Path of the last dialog settings.
```

#### `Storage.log_path(self) -> Path`

```text
Path of the build log.
```

#### `Storage.load_settings(self) -> Settings`

```text
Return the last dialog settings, or the defaults.

A missing, unreadable or malformed file yields the defaults: losing
the last values is better than a dialog that does not open.
```

#### `Storage.save_settings(self, s: Settings) -> bool`

```text
Store the dialog settings.

Returns:
    Whether the file was written.
```

#### `Storage.write_log(self, text: str) -> Path | None`

```text
Write the build log.

Returns:
    The log path, or None if it could not be written.
```

## Functions

### `default_data_dir(platform: str, env: Mapping[str, str], home: Path) -> Path`

```text
Return the per-user folder for Liana's files on a platform.

Args:
    platform: Value of :data:`sys.platform`.
    env: Environment variables.
    home: The user's home folder.

Returns:
    ``%APPDATA%\Liana`` on Windows, ``~/Library/Application Support/Liana``
    on macOS, ``$XDG_DATA_HOME/Liana`` (default ``~/.local/share/Liana``)
    elsewhere.
```

### `atomic_write_text(path: Path, text: str) -> None`

```text
Write a UTF-8 text file so that readers never see a partial file.

The text goes to a temporary file in the same folder, which then replaces
the target. On Windows the replace fails while another process (an
editor, a virus scanner) has the target open, so it is retried briefly.

Args:
    path: Target file; its folder is created when missing.
    text: Content.

Raises:
    OSError: The file could not be written.
```
