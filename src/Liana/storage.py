# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Files Liana keeps between sessions: the last dialog settings and the build log.

They live in the per-user application data folder rather than next to the
code, because an add-in update replaces its own folder and the folder may be
read-only.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from collections.abc import Mapping
from pathlib import Path

from .core.settings import Settings, defaults, from_mapping, migrate

APP_FOLDER = "Liana"
"""Name of Liana's folder inside the user data folder."""

SETTINGS_FILE = "last_settings.json"
"""Last values of the dialog."""

LOG_FILE = "build_log.txt"
"""Report of the last build."""

_REPLACE_ATTEMPTS = 5
_REPLACE_DELAY_S = 0.05


def default_data_dir(platform: str, env: Mapping[str, str], home: Path) -> Path:
    """Return the per-user folder for Liana's files on a platform.

    Args:
        platform: Value of :data:`sys.platform`.
        env: Environment variables.
        home: The user's home folder.

    Returns:
        ``%APPDATA%\\Liana`` on Windows, ``~/Library/Application Support/Liana``
        on macOS, ``$XDG_DATA_HOME/Liana`` (default ``~/.local/share/Liana``)
        elsewhere.
    """
    if platform.startswith("win"):
        base = Path(env["APPDATA"]) if env.get("APPDATA") else home / "AppData" / "Roaming"
    elif platform == "darwin":
        base = home / "Library" / "Application Support"
    else:
        xdg = env.get("XDG_DATA_HOME")
        base = Path(xdg) if xdg else home / ".local" / "share"
    return base / APP_FOLDER


def atomic_write_text(path: Path, text: str) -> None:
    """Write a UTF-8 text file so that readers never see a partial file.

    The text goes to a temporary file in the same folder, which then replaces
    the target. On Windows the replace fails while another process (an
    editor, a virus scanner) has the target open, so it is retried briefly.

    Args:
        path: Target file; its folder is created when missing.
        text: Content.

    Raises:
        OSError: The file could not be written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        for attempt in range(_REPLACE_ATTEMPTS):
            try:
                os.replace(tmp, path)
                return
            except PermissionError:
                if attempt == _REPLACE_ATTEMPTS - 1:
                    raise
                time.sleep(_REPLACE_DELAY_S)
    finally:
        if tmp.exists():
            tmp.unlink()


class Storage:
    """Reads and writes Liana's files in one folder.

    Attributes:
        folder: Folder with the files.
        legacy_folder: Folder where pre-release builds kept their settings
            (the add-in folder); read when the data folder has none yet.
    """

    def __init__(self, folder: Path, legacy_folder: Path | None = None) -> None:
        """Create the store; nothing is touched on disk until a write.

        Args:
            folder: Folder with the files.
            legacy_folder: Optional folder to read old settings from.
        """
        self.folder = folder
        self.legacy_folder = legacy_folder

    @classmethod
    def for_user(cls, legacy_folder: Path | None = None) -> Storage:
        """Return the store in the current user's data folder."""
        return cls(default_data_dir(sys.platform, os.environ, Path.home()), legacy_folder)

    @property
    def settings_path(self) -> Path:
        """Path of the last dialog settings."""
        return self.folder / SETTINGS_FILE

    @property
    def log_path(self) -> Path:
        """Path of the build log."""
        return self.folder / LOG_FILE

    def load_settings(self) -> Settings:
        """Return the last dialog settings, or the defaults.

        A missing, unreadable or malformed file yields the defaults: losing
        the last values is better than a dialog that does not open.
        """
        candidates = [self.settings_path]
        if self.legacy_folder is not None:
            candidates.append(self.legacy_folder / SETTINGS_FILE)
        for path in candidates:
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(raw, dict):
                return from_mapping(migrate(raw), within_limits=True)
        return defaults()

    def save_settings(self, s: Settings) -> bool:
        """Store the dialog settings.

        Returns:
            Whether the file was written.
        """
        try:
            atomic_write_text(self.settings_path, json.dumps(s, indent=1))
        except OSError:
            return False
        return True

    def write_log(self, text: str) -> Path | None:
        """Write the build log.

        Returns:
            The log path, or None if it could not be written.
        """
        try:
            atomic_write_text(self.log_path, text)
        except OSError:
            return None
        return self.log_path
