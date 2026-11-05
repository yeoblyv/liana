# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Fake command, its inputs and event arguments (part of ``adsk.core`` in Fusion)."""

from __future__ import annotations

from typing import Any

from tests.fake_adsk.world import world


class Event:
    """Event that keeps its handlers alive, as Fusion events do."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.handlers: list[Any] = []

    def add(self, handler: Any) -> bool:
        """Connect a handler."""
        self.handlers.append(handler)
        return True

    def fire(self, args: Any) -> None:
        """Call every handler's ``notify``."""
        for handler in list(self.handlers):
            handler.notify(args)


class CommandInput:
    """Common part of every command input."""

    def __init__(self, input_id: str, name: str) -> None:
        self.id = input_id
        self.name = name
        self.isEnabled = True
        self.tooltip = ""


class IntegerSpinnerCommandInput(CommandInput):
    """Integer spinner."""

    def __init__(self, input_id: str, name: str, lo: int, hi: int, step: int, value: int) -> None:
        super().__init__(input_id, name)
        self.minimumValue, self.maximumValue, self.spinStep = lo, hi, step
        self.value = value


class ValueCommandInput(CommandInput):
    """Length input; ``value`` is in internal units (cm)."""

    def __init__(self, input_id: str, name: str, units: str, value: Any) -> None:
        super().__init__(input_id, name)
        self.unitType = units
        self.value = float(value.realValue)
        self.isValidExpression = True


class BoolValueCommandInput(CommandInput):
    """Check box or button."""

    def __init__(self, input_id: str, name: str, is_check_box: bool, value: bool) -> None:
        super().__init__(input_id, name)
        self.isCheckBox = is_check_box
        self.value = value
        self.text = ""


class ListItem:
    """Entry of a drop-down."""

    def __init__(self, owner: ListItems, name: str) -> None:
        self._owner = owner
        self.name = name
        self._selected = False

    @property
    def isSelected(self) -> bool:
        """Whether the entry is selected."""
        return self._selected

    @isSelected.setter
    def isSelected(self, value: bool) -> None:
        if value:
            for other in self._owner.items:
                other._selected = False
        self._selected = value


class ListItems:
    """Entries of a single-selection drop-down."""

    def __init__(self) -> None:
        self.items: list[ListItem] = []

    def add(self, name: str, selected: bool, icon: str) -> ListItem:
        """Append an entry."""
        item = ListItem(self, name)
        self.items.append(item)
        if selected:
            item.isSelected = True
        return item

    @property
    def count(self) -> int:
        """Number of entries."""
        return len(self.items)

    def item(self, index: int) -> ListItem:
        """Entry at ``index``."""
        return self.items[index]


class DropDownCommandInput(CommandInput):
    """Drop-down list."""

    def __init__(self, input_id: str, name: str, style: str) -> None:
        super().__init__(input_id, name)
        self.style = style
        self.listItems = ListItems()

    @property
    def selectedItem(self) -> ListItem | None:
        """Selected entry or None."""
        return next((i for i in self.listItems.items if i.isSelected), None)


class TextBoxCommandInput(CommandInput):
    """Read-only text box."""

    def __init__(self, input_id: str, name: str, text: str, rows: int, read_only: bool) -> None:
        super().__init__(input_id, name)
        self.formattedText = text
        self.numRows = rows
        self.isReadOnly = read_only
        self.isFullWidth = False


class CommandInputs:
    """Inputs of a command or of a group; ids are unique across the command."""

    def __init__(self, registry: dict[str, CommandInput] | None = None) -> None:
        self.registry: dict[str, CommandInput] = {} if registry is None else registry
        self.order: list[CommandInput] = []

    def _add(self, inp: Any) -> Any:
        if inp.id in self.registry:
            raise RuntimeError("duplicate input id: " + inp.id)
        self.registry[inp.id] = inp
        self.order.append(inp)
        return inp

    def itemById(self, input_id: str) -> Any:
        """Input with ``input_id`` anywhere in the command, or None."""
        return self.registry.get(input_id)

    def addGroupCommandInput(self, input_id: str, name: str) -> GroupCommandInput:
        """Add a collapsible group."""
        group: GroupCommandInput = self._add(GroupCommandInput(input_id, name, self.registry))
        return group

    def addIntegerSpinnerCommandInput(
        self, input_id: str, name: str, lo: int, hi: int, step: int, value: int
    ) -> IntegerSpinnerCommandInput:
        """Add an integer spinner."""
        spinner: IntegerSpinnerCommandInput = self._add(
            IntegerSpinnerCommandInput(input_id, name, lo, hi, step, value)
        )
        return spinner

    def addValueInput(self, input_id: str, name: str, units: str, value: Any) -> ValueCommandInput:
        """Add a length input."""
        inp: ValueCommandInput = self._add(ValueCommandInput(input_id, name, units, value))
        return inp

    def addBoolValueInput(
        self, input_id: str, name: str, is_check_box: bool, icon: str, value: bool
    ) -> BoolValueCommandInput:
        """Add a check box or a button."""
        inp: BoolValueCommandInput = self._add(
            BoolValueCommandInput(input_id, name, is_check_box, value)
        )
        return inp

    def addDropDownCommandInput(
        self, input_id: str, name: str, style: str
    ) -> DropDownCommandInput:
        """Add a drop-down."""
        inp: DropDownCommandInput = self._add(DropDownCommandInput(input_id, name, style))
        return inp

    def addTextBoxCommandInput(
        self, input_id: str, name: str, text: str, rows: int, read_only: bool
    ) -> TextBoxCommandInput:
        """Add a text box."""
        inp: TextBoxCommandInput = self._add(
            TextBoxCommandInput(input_id, name, text, rows, read_only)
        )
        return inp


class GroupCommandInput(CommandInput):
    """Collapsible group."""

    def __init__(self, input_id: str, name: str, registry: dict[str, CommandInput]) -> None:
        super().__init__(input_id, name)
        self.isExpanded = True
        self.children = CommandInputs(registry)


class Command:
    """A running command with its dialog."""

    def __init__(self) -> None:
        self.commandInputs = CommandInputs()
        self.okButtonText = "OK"
        self.helpFile = ""
        self.dialog_size: tuple[int, int] | None = None
        self.inputChanged = Event("inputChanged")
        self.validateInputs = Event("validateInputs")
        self.execute = Event("execute")

    def setDialogInitialSize(self, width: int, height: int) -> bool:
        """Set the dialog size."""
        self.dialog_size = (width, height)
        return True

    # helpers for tests: what Fusion does when the user acts

    def change(self, input_id: str) -> None:
        """Fire ``inputChanged`` for an input."""
        self.inputChanged.fire(InputChangedEventArgs(self.commandInputs.itemById(input_id)))

    def validate(self) -> bool:
        """Fire ``validateInputs`` and return the verdict."""
        args = ValidateInputsEventArgs()
        self.validateInputs.fire(args)
        return args.areInputsValid

    def click_ok(self) -> None:
        """Fire ``execute``."""
        world().trace_event("command.execute")
        self.execute.fire(CommandEventArgs(self))


class CommandCreatedEventArgs:
    """Arguments of ``commandCreated``."""

    def __init__(self, command: Command) -> None:
        self.command = command


class CommandEventArgs:
    """Arguments of ``execute``."""

    def __init__(self, command: Command) -> None:
        self.command = command


class InputChangedEventArgs:
    """Arguments of ``inputChanged``."""

    def __init__(self, inp: Any) -> None:
        self.input = inp


class ValidateInputsEventArgs:
    """Arguments of ``validateInputs``."""

    def __init__(self) -> None:
        self.areInputsValid = True
