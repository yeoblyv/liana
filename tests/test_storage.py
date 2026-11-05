# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Settings and log files in the add-in folder."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from Liana.core.settings import DEFAULTS, from_mapping
from Liana.storage import SETTINGS_FILE, Storage, atomic_write_text


def test_settings_round_trip_with_non_ascii_folder(tmp_path: Path) -> None:
    # a non-ASCII user name (Cyrillic)
    store = Storage(tmp_path / "\u0415\u0433\u043e\u0440" / "Liana")
    s = from_mapping({"cradles": 7, "mount": "L"})
    assert store.save_settings(s)
    assert store.load_settings() == s
    assert json.loads(store.settings_path.read_text(encoding="utf-8"))["cradles"] == 7
    assert [p.name for p in store.folder.iterdir()] == [SETTINGS_FILE]


def test_missing_or_broken_settings_give_defaults(tmp_path: Path) -> None:
    store = Storage(tmp_path)
    assert store.load_settings() == DEFAULTS
    store.settings_path.write_text("{oops", encoding="utf-8")
    assert store.load_settings() == DEFAULTS
    store.settings_path.write_text("[1]", encoding="utf-8")
    assert store.load_settings() == DEFAULTS


def test_old_settings_are_migrated(tmp_path: Path) -> None:
    store = Storage(tmp_path)
    store.settings_path.write_text(json.dumps({"cradles": 3, "nut_af": 5.8}), encoding="utf-8")
    s = store.load_settings()
    assert s["cradles"] == 3 and s["nut_af"] == DEFAULTS["nut_af"]
    store.save_settings(from_mapping({"cradles": 9}))
    assert store.load_settings()["cradles"] == 9


def test_write_failures_are_reported_not_raised(tmp_path: Path) -> None:
    blocker = tmp_path / "file"
    blocker.write_text("x", encoding="utf-8")
    store = Storage(blocker / "Liana")  # a folder below a file cannot exist
    assert not store.save_settings(DEFAULTS)
    assert store.write_log("log") is None


def test_write_log(tmp_path: Path) -> None:
    store = Storage(tmp_path)
    path = store.write_log("line 1\nline 2\n")
    assert path == tmp_path / "build_log.txt"
    assert path.read_bytes() == b"line 1\nline 2\n"


def test_replace_is_retried_while_the_target_is_locked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "a.txt"
    real = os.replace
    calls = []

    def locked_twice(src: str | os.PathLike[str], dst: str | os.PathLike[str]) -> None:
        calls.append(dst)
        if len(calls) <= 2:
            raise PermissionError("in use")
        real(src, dst)

    monkeypatch.setattr(os, "replace", locked_twice)
    monkeypatch.setattr(time, "sleep", lambda s: None)
    atomic_write_text(target, "done")
    assert target.read_text(encoding="utf-8") == "done"
    assert len(calls) == 3


def test_permanent_lock_raises_and_leaves_no_temp_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def locked(src: str, dst: str) -> None:
        raise PermissionError("in use")

    monkeypatch.setattr(os, "replace", locked)
    monkeypatch.setattr(time, "sleep", lambda s: None)
    with pytest.raises(PermissionError):
        atomic_write_text(tmp_path / "a.txt", "x")
    assert list(tmp_path.iterdir()) == []


def test_out_of_range_settings_are_not_trusted(tmp_path: Path) -> None:
    store = Storage(tmp_path)
    store.settings_path.write_text('{"cradles": 1000000000, "nut_af": 1e999}', encoding="utf-8")
    assert store.load_settings() == DEFAULTS
