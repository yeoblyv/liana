# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Fake ``adsk.core``: geometry primitives, value inputs, application and UI.

Class and method names follow the Fusion API (camelCase) so that the add-in
code runs against the fake unchanged.
"""

from __future__ import annotations

import math
from typing import Any

from tests.fake_adsk.commands import Command, CommandCreatedEventArgs, Event
from tests.fake_adsk.world import mm, world


class Point3D:
    """Point in Fusion internal units (centimetres)."""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x, self.y, self.z = x, y, z

    @staticmethod
    def create(x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Point3D:
        """Create a point."""
        return Point3D(x, y, z)

    def key(self) -> tuple[float, float, float]:
        """Rounded millimeter coordinates for traces."""
        return (mm(self.x), mm(self.y), mm(self.z))


class Vector3D(Point3D):
    """Vector in Fusion internal units."""

    @staticmethod
    def create(x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Vector3D:
        """Create a vector."""
        return Vector3D(x, y, z)

    def crossProduct(self, other: Vector3D) -> Vector3D:
        """Return the cross product ``self x other``."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


class ValueInput:
    """String or real value passed to API calls."""

    def __init__(self, expression: str, real: float | None = None) -> None:
        self.stringValue = expression
        self.realValue = real

    @staticmethod
    def createByString(expression: str) -> ValueInput:
        """Create from an expression string."""
        return ValueInput(expression)

    @staticmethod
    def createByReal(value: float) -> ValueInput:
        """Create from a number in internal units."""
        return ValueInput(repr(value), value)


class ObjectCollection:
    """Ordered collection of API objects."""

    def __init__(self) -> None:
        self.items: list[Any] = []

    @staticmethod
    def create() -> ObjectCollection:
        """Create an empty collection."""
        return ObjectCollection()

    def add(self, item: Any) -> bool:
        """Append an item."""
        self.items.append(item)
        return True

    @property
    def count(self) -> int:
        """Number of items."""
        return len(self.items)

    def item(self, index: int) -> Any:
        """Item at ``index``."""
        return self.items[index]


class Matrix3D:
    """Rigid transform restricted to a rotation about Y plus a translation."""

    def __init__(self) -> None:
        self.angle = 0.0
        self.translation = Vector3D(0.0, 0.0, 0.0)

    @staticmethod
    def create() -> Matrix3D:
        """Create an identity transform."""
        return Matrix3D()

    def setToRotation(self, angle: float, axis: Vector3D, origin: Point3D) -> bool:
        """Set the rotation (only rotations about +Y through the origin are used)."""
        if (axis.x, axis.y, axis.z) != (0, 1, 0) or (origin.x, origin.y, origin.z) != (0, 0, 0):
            world().errors.append("rotation other than about +Y through the origin")
        self.angle = angle
        return True

    def key(self) -> tuple[float, float, float, float]:
        """Rounded rotation in degrees and translation in millimeters."""
        return (round(math.degrees(self.angle), 6) + 0.0, *self.translation.key())


class Line3D:
    """Marker class used for edge geometry type checks."""

    @staticmethod
    def classType() -> str:
        """Type name of 3D lines."""
        return "adsk::core::Line3D"


class Color:
    """RGBA color."""

    def __init__(self, r: int, g: int, b: int, a: int) -> None:
        self.rgba = (r, g, b, a)

    @staticmethod
    def create(r: int, g: int, b: int, a: int) -> Color:
        """Create a color."""
        return Color(r, g, b, a)


class ColorProperty:
    """Color property of an appearance."""

    def __init__(self, prop_id: str, name: str) -> None:
        self.id = prop_id
        self.name = name
        self._value: Color | None = None

    @staticmethod
    def cast(obj: Any) -> ColorProperty | None:
        """Return ``obj`` if it is a color property, else None."""
        return obj if isinstance(obj, ColorProperty) else None

    @property
    def value(self) -> Color | None:
        """Current color."""
        return self._value

    @value.setter
    def value(self, color: Color) -> None:
        self._value = color
        world().trace_event("appearance.color", self.id, color.rgba)


class DocumentTypes:
    """Document type enumeration."""

    FusionDesignDocumentType = "FusionDesignDocumentType"


class MessageBoxButtonTypes:
    """Message box button sets."""

    OKButtonType = "OKButtonType"
    YesNoButtonType = "YesNoButtonType"


class MessageBoxIconTypes:
    """Message box icons."""

    NoIconIconType = "NoIconIconType"
    InformationIconType = "InformationIconType"


class DialogResults:
    """What the user clicked in a message box."""

    DialogOK = "DialogOK"
    DialogYes = "DialogYes"
    DialogNo = "DialogNo"


class DropDownStyles:
    """Drop-down style enumeration."""

    TextListDropDownStyle = "TextListDropDownStyle"


class _Products:
    def __init__(self, design: Any) -> None:
        self._design = design

    def itemByProductType(self, product_type: str) -> Any:
        """The design product of the document."""
        return self._design if product_type == "DesignProductType" else None


class Document:
    """Open document holding one design."""

    def __init__(self, design: Any) -> None:
        self.products = _Products(design)


class Documents:
    """Open documents of the application."""

    def add(self, document_type: str) -> Document:
        """Create a new design document and make it active."""
        from tests.fake_adsk import fusion

        w = world()
        design = fusion.Design()
        design.designIntent = w.new_design_intent
        w.documents.append(design)
        w.active_product = design
        w.trace_event("documents.add", document_type)
        return Document(design)


class CustomEventArgs:
    """Arguments of a custom event."""

    def __init__(self, info: str) -> None:
        self.additionalInfo = info


class ProgressDialog:
    """Modeless progress dialog."""

    def __init__(self) -> None:
        self.isCancelButtonShown = True
        self._message = ""
        self.progressValue = 0

    def show(self, title: str, message: str, minimum: int, maximum: int, delay: int) -> bool:
        """Show the dialog."""
        world().trace_event("progress.show", title, message, minimum, maximum)
        return True

    @property
    def message(self) -> str:
        """Message line."""
        return self._message

    @message.setter
    def message(self, text: str) -> None:
        self._message = text
        world().trace_event("progress.message", text)

    def hide(self) -> bool:
        """Hide the dialog."""
        world().trace_event("progress.hide")
        return True


class CommandDefinition:
    """Button definition of a command."""

    def __init__(
        self, owner: CommandDefinitions, cmd_id: str, name: str, tip: str, res: str
    ) -> None:
        self._owner = owner
        self.id = cmd_id
        self.name = name
        self.tooltip = tip
        self.resourceFolder = res
        self.commandCreated = Event("commandCreated")

    def deleteMe(self) -> bool:
        """Remove the definition."""
        self._owner.items.pop(self.id, None)
        world().trace_event("commandDefinition.delete", self.id)
        return True

    def execute(self) -> Command:
        """Start the command as a click on its button does; returns the command."""
        command = Command()
        world().trace_event("command.created", self.id)
        self.commandCreated.fire(CommandCreatedEventArgs(command))
        return command


class CommandDefinitions:
    """Registered command definitions."""

    def __init__(self) -> None:
        self.items: dict[str, CommandDefinition] = {}

    def itemById(self, cmd_id: str) -> CommandDefinition | None:
        """Definition with ``cmd_id`` or None."""
        return self.items.get(cmd_id)

    def addButtonDefinition(self, cmd_id: str, name: str, tip: str, res: str) -> CommandDefinition:
        """Register a button."""
        definition = CommandDefinition(self, cmd_id, name, tip, res)
        self.items[cmd_id] = definition
        world().trace_event("commandDefinition.add", cmd_id, name, tip, bool(res))
        return definition


class CommandControl:
    """Control of a command placed in a panel."""

    def __init__(self, owner: ToolbarControls, cmd_id: str) -> None:
        self._owner = owner
        self.id = cmd_id

    def deleteMe(self) -> bool:
        """Remove the control."""
        self._owner.items.pop(self.id, None)
        world().trace_event("control.delete", self.id)
        return True


class ToolbarControls:
    """Controls of a toolbar panel."""

    def __init__(self) -> None:
        self.items: dict[str, CommandControl] = {}

    def itemById(self, cmd_id: str) -> CommandControl | None:
        """Control with ``cmd_id`` or None."""
        return self.items.get(cmd_id)

    def addCommand(self, definition: CommandDefinition) -> CommandControl:
        """Place a command in the panel."""
        control = CommandControl(self, definition.id)
        self.items[definition.id] = control
        world().trace_event("control.add", definition.id)
        return control


class ToolbarPanel:
    """Toolbar panel."""

    def __init__(self) -> None:
        self.controls = ToolbarControls()


class ToolbarPanels:
    """All toolbar panels."""

    def __init__(self) -> None:
        self.items = {"SolidCreatePanel": ToolbarPanel()}

    def itemById(self, panel_id: str) -> ToolbarPanel | None:
        """Panel with ``panel_id`` or None."""
        return self.items.get(panel_id)


class UserInterface:
    """User interface of the application."""

    def __init__(self) -> None:
        self.commandDefinitions = CommandDefinitions()
        self.allToolbarPanels = ToolbarPanels()

    def messageBox(
        self, text: str, title: str = "", buttons: str | None = None, icon: str | None = None
    ) -> str:
        """Record a message box; a Yes/No box returns the world's ``answer``."""
        w = world()
        w.messages.append(text)
        w.trace_event("messageBox", title, text)
        if buttons == MessageBoxButtonTypes.YesNoButtonType:
            return w.answer
        return DialogResults.DialogOK

    def createProgressDialog(self) -> ProgressDialog:
        """Create a progress dialog."""
        world().trace_event("progress.create")
        return ProgressDialog()


class Application:
    """The Fusion application (one per world)."""

    def __init__(self) -> None:
        self.userInterface = UserInterface()
        self.documents = Documents()
        self.custom_events: dict[str, Event] = {}
        from tests.fake_adsk import fusion

        self.materialLibraries = fusion.MaterialLibraries()

    @staticmethod
    def get() -> Application:
        """Return the application of the current world."""
        w = world()
        if w.app is None:
            w.app = Application()
        app: Application = w.app
        return app

    @property
    def activeProduct(self) -> Any:
        """Active design or None."""
        return world().active_product

    def registerCustomEvent(self, event_id: str) -> Event:
        """Register a custom event."""
        if event_id in self.custom_events:
            raise RuntimeError("custom event already registered: " + event_id)
        event = Event(event_id)
        self.custom_events[event_id] = event
        world().trace_event("customEvent.register", event_id)
        return event

    def unregisterCustomEvent(self, event_id: str) -> bool:
        """Unregister a custom event."""
        if event_id not in self.custom_events:
            raise RuntimeError("custom event not registered: " + event_id)
        del self.custom_events[event_id]
        world().trace_event("customEvent.unregister", event_id)
        return True

    def fireCustomEvent(self, event_id: str, info: str) -> bool:
        """Fire a custom event synchronously (Fusion delivers it after the command)."""
        world().trace_event("customEvent.fire", event_id)
        self.custom_events[event_id].fire(CustomEventArgs(info))
        return True


class InputChangedEventHandler:
    """Base class of input-changed handlers."""


class ValidateInputsEventHandler:
    """Base class of validate-inputs handlers."""


class CommandEventHandler:
    """Base class of command handlers."""


class CommandCreatedEventHandler:
    """Base class of command-created handlers."""


class CustomEventHandler:
    """Base class of custom event handlers."""
