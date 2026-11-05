# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Liana for Autodesk Fusion: parametric under-desk cable holders.

Fusion loads this file and calls :func:`run` when the add-in starts and
:func:`stop` when it stops. The command appears under Solid > Create > Liana.
"""

from __future__ import annotations

import sys
import webbrowser

import adsk.core

from .addin import ADDIN_DIR, LianaAddIn
from .storage import Storage

# Fusion's entry points are module functions, so the running add-in is kept
# here between run() and stop(); it is the only module-level state.
_addin: LianaAddIn | None = None


def run(context: object) -> None:
    """Start the add-in (called by Fusion)."""
    global _addin
    if _addin is not None:
        _addin.stop()
    _addin = LianaAddIn(
        adsk.core.Application.get(), Storage.for_user(legacy_folder=ADDIN_DIR), webbrowser.open
    )
    _addin.start()


def stop(context: object) -> None:
    """Stop the add-in (called by Fusion).

    The add-in's other modules are dropped from the import cache, so that
    Run after an update loads the new code instead of the modules Python
    kept in memory.
    """
    global _addin
    if _addin is not None:
        _addin.stop()
        _addin = None
    package = __name__.rpartition(".")[0]
    if package:
        for name in [n for n in sys.modules if n.startswith(package + ".") and n != __name__]:
            del sys.modules[name]
