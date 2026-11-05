# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""The add-in as Fusion drives it: start, dialog, build, stop."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

import pytest

import tests.fake_adsk as fake
from Liana import addin as addin_module
from Liana import dialog as dialog_module
from Liana._version import __version__
from Liana.addin import BUILD_EVENT_ID, COMMAND_ID, PANEL_ID, LianaAddIn
from Liana.core.settings import DEFAULTS, from_mapping
from Liana.dialog import (
    GROUPS,
    KINDS,
    PRIVACY_ID,
    PRIVACY_URL,
    RESET_ID,
    SUMMARY_ID,
    mount_key,
    mount_label,
)
from Liana.storage import Storage
from tests.fake_adsk import core, fusion


class Harness:
    """A started add-in on a fresh fake Fusion."""

    def __init__(self, tmp_path: Path) -> None:
        self.world = fake.reset()
        self.app = core.Application.get()
        self.opened: list[str] = []
        self.browser_works = True
        self.storage = Storage(tmp_path / "data")
        self.addin = LianaAddIn(self.app, self.storage, self.open_url)
        self.world.active_product = fusion.Design()
        self.addin.start()

    def open_url(self, url: str) -> bool:
        self.opened.append(url)
        return self.browser_works

    def open_dialog(self) -> Any:
        definition = self.app.userInterface.commandDefinitions.itemById(COMMAND_ID)
        assert definition is not None
        return definition.execute()


@pytest.fixture
def h(tmp_path: Path) -> Harness:
    return Harness(tmp_path)


def summary(cmd: Any) -> str:
    text: str = cmd.commandInputs.itemById(SUMMARY_ID).formattedText
    return text


def test_start_registers_the_command_once(h: Harness) -> None:
    ui = h.app.userInterface
    definition = ui.commandDefinitions.itemById(COMMAND_ID)
    panel = ui.allToolbarPanels.itemById(PANEL_ID)
    assert definition is not None and panel is not None
    assert definition.resourceFolder.endswith("resources")
    assert panel.controls.itemById(COMMAND_ID) is not None
    assert BUILD_EVENT_ID in h.app.custom_events
    h.addin.start()  # a restart replaces the stale registration
    assert ("commandDefinition.delete", COMMAND_ID) in h.world.trace
    assert ("control.delete", COMMAND_ID) in h.world.trace
    assert ("customEvent.unregister", BUILD_EVENT_ID) in h.world.trace
    assert h.world.messages == []


def test_stop_removes_everything_and_can_run_twice(h: Harness) -> None:
    h.addin.stop()
    ui = h.app.userInterface
    panel = ui.allToolbarPanels.itemById(PANEL_ID)
    assert panel is not None
    assert ui.commandDefinitions.itemById(COMMAND_ID) is None
    assert panel.controls.itemById(COMMAND_ID) is None
    assert BUILD_EVENT_ID not in h.app.custom_events
    h.addin.stop()


def test_start_failure_is_shown(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake.reset()
    app = core.Application.get()

    def refuse(*args: Any) -> None:
        raise RuntimeError("no buttons today")

    monkeypatch.setattr(core.CommandDefinitions, "addButtonDefinition", refuse)
    LianaAddIn(app, Storage(tmp_path), lambda url: None).start()
    assert fake.world().messages[0].startswith("Liana failed to start:\nTraceback")


def test_dialog_shows_every_setting_and_the_version(h: Harness) -> None:
    cmd = h.open_dialog()
    inputs = cmd.commandInputs
    assert cmd.okButtonText == "Generate" and cmd.dialog_size == (430, 820)
    for key in KINDS:
        assert inputs.itemById(key) is not None
    assert [g.id for g in GROUPS] == [i.id for i in inputs.order[: len(GROUPS)]]
    assert inputs.itemById("cradles").tooltip.startswith("Number of cable cradles")
    assert inputs.itemById(PRIVACY_ID).name == "Liana " + __version__
    assert inputs.itemById(PRIVACY_ID).text == "Privacy policy"
    assert summary(cmd).startswith("<b>10 cradles</b>")
    assert inputs.itemById("mount").selectedItem.name == mount_label("X")


def test_changing_inputs_updates_the_summary_and_enables(h: Harness) -> None:
    cmd = h.open_dialog()
    inputs = cmd.commandInputs
    inputs.itemById("cradles").value = 3
    inputs.itemById("make_frame").value = False
    cmd.change("cradles")
    assert summary(cmd).startswith("<b>3 cradles</b>")
    assert not inputs.itemById("center_pin").isEnabled
    assert not inputs.itemById("mount").isEnabled
    assert cmd.validate()


def test_invalid_settings_disable_generate(h: Harness) -> None:
    cmd = h.open_dialog()
    inputs = cmd.commandInputs
    inputs.itemById("screw_csk").value = 0.4  # 4 mm: not larger than the hole
    cmd.change("screw_csk")
    assert "<b>! countersink must be larger than the screw hole</b>" in summary(cmd)
    assert not cmd.validate()
    inputs.itemById("screw_csk").value = 0.84
    inputs.itemById("depth").isValidExpression = False
    assert not cmd.validate()


def test_validate_treats_errors_as_invalid(h: Harness, monkeypatch: pytest.MonkeyPatch) -> None:
    def broken(self: Any) -> bool:
        raise RuntimeError("input gone")

    monkeypatch.setattr(dialog_module.SettingsDialog, "inputs_valid", broken)
    assert not h.open_dialog().validate()


def test_reset_and_privacy_buttons(h: Harness) -> None:
    cmd = h.open_dialog()
    inputs = cmd.commandInputs
    inputs.itemById("cradles").value = 2
    inputs.itemById("mount").listItems.item(0).isSelected = True
    cmd.change(RESET_ID)
    assert inputs.itemById("cradles").value == DEFAULTS["cradles"]
    assert inputs.itemById("mount").selectedItem.name == mount_label("X")
    assert h.opened == []
    cmd.change(PRIVACY_ID)
    assert h.opened == [PRIVACY_URL]
    assert h.world.messages == []


def test_privacy_address_is_shown_when_no_browser_opens(h: Harness) -> None:
    h.browser_works = False
    cmd = h.open_dialog()
    cmd.change(PRIVACY_ID)
    assert h.world.messages == ["Open this page in your web browser:\n" + PRIVACY_URL]


def test_input_errors_are_not_shown(h: Harness, monkeypatch: pytest.MonkeyPatch) -> None:
    def broken(self: Any, input_id: str) -> None:
        raise RuntimeError("summary failed")

    monkeypatch.setattr(dialog_module.SettingsDialog, "input_changed", broken)
    cmd = h.open_dialog()
    cmd.change("cradles")
    assert h.world.messages == []


def test_generate_builds_saves_settings_and_reports(h: Harness) -> None:
    cmd = h.open_dialog()
    cmd.commandInputs.itemById("cradles").value = 4
    cmd.click_ok()
    assert h.storage.load_settings()["cradles"] == 4
    assert ("customEvent.fire", BUILD_EVENT_ID) in h.world.trace
    message = h.world.messages[-1]
    assert message.startswith("Liana: system built in this design.")
    assert "Log: " + str(h.storage.log_path) in message  # the fake has no edges to round
    assert h.storage.log_path.read_text(encoding="utf-8").startswith(
        "Liana build log\nmode: built in this design"
    )


def test_reopening_edits_the_system_in_the_design(h: Harness) -> None:
    cmd = h.open_dialog()
    cmd.commandInputs.itemById("cradles").value = 6
    cmd.click_ok()
    cmd = h.open_dialog()
    assert summary(cmd).startswith("<b>Editing the system in this design.</b><br><b>6 cradles</b>")
    cmd.commandInputs.itemById("cable_d").value = 1.1
    cmd.click_ok()
    assert h.world.messages[-1].startswith("Liana: system updated in place (")


def test_new_dialog_starts_from_the_last_settings(h: Harness) -> None:
    h.storage.save_settings(from_mapping({"cradles": 5, "new_design": True}))
    cmd = h.open_dialog()
    assert cmd.commandInputs.itemById("cradles").value == 5
    assert cmd.commandInputs.itemById("new_design").value is False


def test_errors_in_created_and_build_are_shown(
    h: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken(*args: Any) -> None:
        raise RuntimeError("design is read-only")

    monkeypatch.setattr(addin_module, "generate", broken)
    cmd = h.open_dialog()
    cmd.click_ok()
    assert h.world.messages[-1].startswith("Liana:\nTraceback")
    assert "design is read-only" in h.world.messages[-1]
    monkeypatch.setattr(addin_module, "load_design_settings", broken)
    monkeypatch.setattr(addin_module, "find_system", lambda d: object())
    h.open_dialog()
    assert "design is read-only" in h.world.messages[-1]


def test_optional_ui_properties_may_be_missing(
    h: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tests.fake_adsk import commands

    def refuse(self: Any, *args: Any) -> None:
        raise AttributeError("not in this Fusion")

    def missing(name: str, initial: object) -> property:
        """A property that only accepts the value the fake sets on creation."""

        def setter(self: Any, value: object) -> None:
            if value != initial:
                raise AttributeError(name + " is not in this Fusion")
            self.__dict__["_" + name] = value

        return property(lambda self: self.__dict__.get("_" + name, initial), setter)

    monkeypatch.setattr(commands.Command, "setDialogInitialSize", refuse)
    monkeypatch.setattr(commands.CommandInput, "tooltip", missing("tooltip", ""), raising=False)
    monkeypatch.setattr(
        commands.CommandInput, "isEnabled", missing("isEnabled", True), raising=False
    )
    monkeypatch.setattr(commands.BoolValueCommandInput, "text", missing("text", ""), raising=False)
    monkeypatch.setattr(
        commands.TextBoxCommandInput, "isFullWidth", missing("isFullWidth", False), raising=False
    )
    cmd = h.open_dialog()
    assert summary(cmd).startswith("<b>10 cradles</b>")
    cmd.commandInputs.itemById("cradles").value = 2
    cmd.change("cradles")
    assert summary(cmd).startswith("<b>2 cradles</b>")
    assert h.world.messages == []


def test_mount_labels_round_trip() -> None:
    for key in ("none", "straight", "L", "T", "X"):
        assert mount_key(mount_label(key)) == key
    assert mount_key(None) == "none" and mount_key("Spiral") == "none"


def test_entry_point_runs_and_stops(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake.reset()
    entry = importlib.import_module("Liana.Liana")
    monkeypatch.setattr(
        entry.Storage, "for_user", classmethod(lambda cls, legacy_folder=None: Storage(tmp_path))
    )
    entry.run({"IsApplicationStartup": True})
    entry.run({})  # a second run replaces the first instance
    ui = core.Application.get().userInterface
    assert ui.commandDefinitions.itemById(COMMAND_ID) is not None
    entry.stop({})
    assert ui.commandDefinitions.itemById(COMMAND_ID) is None
    entry.stop({})
    assert fake.world().messages == []


def test_settings_from_the_event_are_sanitised(h: Harness) -> None:
    h.app.fireCustomEvent(BUILD_EVENT_ID, json.dumps({"cradles": "many", "mount": "T"}))
    assert h.world.messages[-1].startswith("Liana: system built in this design.")
    stored = h.world.active_product.attributes.itemByName("Liana", "settings").value
    assert json.loads(stored)["cradles"] == DEFAULTS["cradles"]
    assert json.loads(stored)["mount"] == "T"
