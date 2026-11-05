# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Fusion event handler classes that forward to plain callables.

Fusion calls ``notify`` on a handler object and drops any exception raised
there without telling the user, so every handler catches errors and passes
them to an error callback. Fusion does not keep handler objects alive, so
the add-in holds every handler for as long as it is connected.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import adsk.core

Callback = Callable[[Any], None]
"""Receives the event arguments."""

ErrorCallback = Callable[[], None]
"""Called inside ``except`` when a callback raised; reads the active exception."""


class CommandCreated(adsk.core.CommandCreatedEventHandler):  # type: ignore[misc]  # untyped base
    """Forwards ``commandCreated``."""

    def __init__(self, callback: Callback, on_error: ErrorCallback) -> None:
        """Wrap a callback.

        Args:
            callback: Receives the event arguments.
            on_error: Called when ``callback`` raises.
        """
        super().__init__()
        self._callback = callback
        self._on_error = on_error

    def notify(self, args: Any) -> None:
        """Pass the event arguments to the callback.

        Args:
            args: Event arguments from Fusion.
        """
        try:
            self._callback(args)
        except Exception:  # report anything rather than lose it inside Fusion
            self._on_error()


class InputChanged(adsk.core.InputChangedEventHandler):  # type: ignore[misc]  # untyped base
    """Forwards ``inputChanged``."""

    def __init__(self, callback: Callback, on_error: ErrorCallback) -> None:
        """Wrap a callback.

        Args:
            callback: Receives the event arguments.
            on_error: Called when ``callback`` raises.
        """
        super().__init__()
        self._callback = callback
        self._on_error = on_error

    def notify(self, args: Any) -> None:
        """Pass the event arguments to the callback.

        Args:
            args: Event arguments from Fusion.
        """
        try:
            self._callback(args)
        except Exception:  # report anything rather than lose it inside Fusion
            self._on_error()


class ValidateInputs(adsk.core.ValidateInputsEventHandler):  # type: ignore[misc]  # untyped base
    """Forwards ``validateInputs``; an error disables the OK button."""

    def __init__(self, callback: Callable[[], bool]) -> None:
        """Wrap a callback.

        Args:
            callback: Returns whether the inputs are valid.
        """
        super().__init__()
        self._callback = callback

    def notify(self, args: Any) -> None:
        """Set ``args.areInputsValid`` from the callback.

        Args:
            args: Event arguments from Fusion.
        """
        try:
            args.areInputsValid = self._callback()
        except Exception:  # an input that cannot be read is not valid
            args.areInputsValid = False


class CommandExecute(adsk.core.CommandEventHandler):  # type: ignore[misc]  # untyped base
    """Forwards ``execute``."""

    def __init__(self, callback: Callback, on_error: ErrorCallback) -> None:
        """Wrap a callback.

        Args:
            callback: Receives the event arguments.
            on_error: Called when ``callback`` raises.
        """
        super().__init__()
        self._callback = callback
        self._on_error = on_error

    def notify(self, args: Any) -> None:
        """Pass the event arguments to the callback.

        Args:
            args: Event arguments from Fusion.
        """
        try:
            self._callback(args)
        except Exception:  # report anything rather than lose it inside Fusion
            self._on_error()


class CustomEvent(adsk.core.CustomEventHandler):  # type: ignore[misc]  # untyped base
    """Forwards a custom event."""

    def __init__(self, callback: Callback, on_error: ErrorCallback) -> None:
        """Wrap a callback.

        Args:
            callback: Receives the event arguments.
            on_error: Called when ``callback`` raises.
        """
        super().__init__()
        self._callback = callback
        self._on_error = on_error

    def notify(self, args: Any) -> None:
        """Pass the event arguments to the callback.

        Args:
            args: Event arguments from Fusion.
        """
        try:
            self._callback(args)
        except Exception:  # report anything rather than lose it inside Fusion
            self._on_error()
