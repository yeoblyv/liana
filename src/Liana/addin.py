# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""The add-in: registers the Liana command and runs builds."""

from __future__ import annotations

import json
import traceback
from collections.abc import Callable
from pathlib import Path
from typing import Any

import adsk.fusion

from .cad.api import API_ERRORS, Application
from .cad.design import find_system, load_design_settings
from .cad.system import Progress, generate
from .core.report import log_text, result_message
from .core.settings import from_mapping
from .dialog import DIALOG_SIZE, SettingsDialog
from .handlers import CommandCreated, CommandExecute, CustomEvent, InputChanged, ValidateInputs
from .storage import Storage

ADDIN_DIR = Path(__file__).resolve().parent
"""Folder of the installed add-in."""

RESOURCES_DIR = ADDIN_DIR / "resources"
"""Command icons."""

COMMAND_ID = "lianaGeneratorCmd"
"""Id of the command definition."""

COMMAND_NAME = "Liana"
"""Command name shown in the toolbar."""

COMMAND_TOOLTIP = (
    "Liana: generate a parametric under-desk cable holder system - holder, X-frame and tie mount."
)
"""Toolbar tooltip."""

PANEL_ID = "SolidCreatePanel"
"""Toolbar panel that shows the command (Solid > Create)."""

BUILD_EVENT_ID = "lianaBuild"
"""Custom event that runs a build after the dialog has closed."""


class LianaAddIn:
    """Everything the add-in registers in Fusion, and the handlers behind it."""

    def __init__(
        self, app: Application, storage: Storage, open_url: Callable[[str], object]
    ) -> None:
        """Prepare the add-in; nothing is registered until :meth:`start`.

        Args:
            app: Fusion application.
            storage: Where the last settings and the build log are kept.
            open_url: Opens a web page in the browser and returns whether a
                browser accepted it, like :func:`webbrowser.open`.
        """
        self.app = app
        self.ui = app.userInterface
        self.storage = storage
        self._open_url = open_url
        self._progress = Progress(self.ui)
        # Fusion does not keep handler objects alive: hold them while connected
        self._handlers: list[object] = []
        self._command_handlers: list[object] = []

    # ------------------------------------------------------------ lifecycle

    def start(self) -> None:
        """Add the command to Solid > Create and connect the build event."""
        try:
            definitions = self.ui.commandDefinitions
            stale = definitions.itemById(COMMAND_ID)
            if stale:
                stale.deleteMe()
            icons = str(RESOURCES_DIR) if RESOURCES_DIR.is_dir() else ""
            definition = definitions.addButtonDefinition(
                COMMAND_ID, COMMAND_NAME, COMMAND_TOOLTIP, icons
            )
            created = CommandCreated(self._on_created, self._report_error)
            definition.commandCreated.add(created)
            self._handlers.append(created)
            panel = self.ui.allToolbarPanels.itemById(PANEL_ID)
            if panel:
                control = panel.controls.itemById(COMMAND_ID)
                if control:
                    control.deleteMe()
                panel.controls.addCommand(definition)
            try:
                self.app.unregisterCustomEvent(BUILD_EVENT_ID)
            except API_ERRORS:
                pass  # not registered: the normal case
            event = self.app.registerCustomEvent(BUILD_EVENT_ID)
            build = CustomEvent(self._on_build, self._report_error)
            event.add(build)
            self._handlers.append(build)
        except Exception:  # tell the user why the command is missing
            self.ui.messageBox("Liana failed to start:\n" + traceback.format_exc())

    def stop(self) -> None:
        """Remove everything :meth:`start` added; never raises."""
        steps: tuple[Callable[[], None], ...] = (
            self._remove_control,
            self._remove_definition,
            lambda: self.app.unregisterCustomEvent(BUILD_EVENT_ID),
        )
        for step in steps:
            try:
                step()
            except Exception:  # Fusion is shutting down or the item is already gone
                pass
        self._handlers.clear()
        self._command_handlers.clear()

    def _remove_control(self) -> None:
        panel = self.ui.allToolbarPanels.itemById(PANEL_ID)
        if panel:
            control = panel.controls.itemById(COMMAND_ID)
            if control:
                control.deleteMe()

    def _remove_definition(self) -> None:
        definition = self.ui.commandDefinitions.itemById(COMMAND_ID)
        if definition:
            definition.deleteMe()

    # ------------------------------------------------------------ events

    def _report_error(self) -> None:
        """Show the active exception; called from an ``except`` block."""
        self.ui.messageBox("Liana:\n" + traceback.format_exc())

    def _open_page(self, url: str) -> None:
        """Open a page in the browser, or show its address when no browser opens."""
        if not self._open_url(url):
            self.ui.messageBox("Open this page in your web browser:\n" + url, COMMAND_NAME)

    def _on_created(self, args: Any) -> None:
        """Open the dialog, filled from the design or from the last run."""
        cmd = args.command
        cmd.okButtonText = "Generate"
        try:
            cmd.setDialogInitialSize(*DIALOG_SIZE)
        except API_ERRORS:
            pass  # older Fusion picks its own size
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        s = None
        if design is not None and find_system(design) is not None:
            s = load_design_settings(design)
        editing = s is not None
        if s is None:
            s = self.storage.load_settings()
        s["new_design"] = False
        dialog = SettingsDialog(editing, self._open_page)
        dialog.build(cmd.commandInputs, s)
        dialog.refresh(s)
        # input errors are not reported: a message box per keystroke would
        # make the dialog unusable, and Validate keeps a broken state from building
        changed = InputChanged(lambda a: dialog.input_changed(a.input.id), lambda: None)
        validate = ValidateInputs(dialog.inputs_valid)
        execute = CommandExecute(lambda a: self._on_execute(dialog), self._report_error)
        cmd.inputChanged.add(changed)
        cmd.validateInputs.add(validate)
        cmd.execute.add(execute)
        # the previous command has ended, so its handlers can go
        self._command_handlers = [changed, validate, execute]

    def _on_execute(self, dialog: SettingsDialog) -> None:
        """Remember the settings and queue the build.

        The build runs from a custom event after the command has closed,
        because it may open a new document.
        """
        s = dialog.read()
        self.storage.save_settings(s)
        self.app.fireCustomEvent(BUILD_EVENT_ID, json.dumps(s))

    def _on_build(self, args: Any) -> None:
        """Build the system and report the result."""
        s = from_mapping(json.loads(args.additionalInfo), within_limits=True)
        mode, log = generate(self.app, s, self._progress)
        path = self.storage.write_log(log_text(mode, s, log))
        self.ui.messageBox(result_message(mode, log, str(path) if path else ""), COMMAND_NAME)
