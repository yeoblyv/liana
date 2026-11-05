# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Liana for Autodesk Fusion: parametric under-desk cable holders.

Fusion loads this file and calls :func:`run` when the add-in starts and
:func:`stop` when it stops. The command appears under Solid > Create > Liana.
"""

from __future__ import annotations

import os
import sys
import webbrowser

import adsk.core

from .addin import ADDIN_DIR, LianaAddIn
from .storage import Storage

# Fusion's entry points are module functions, so the running add-in is kept
# here between run() and stop(); it is the only module-level state.
_addin: LianaAddIn | None = None


def run(context: object) -> None:
    """Start the add-in (called by Fusion).

    Args:
        context: Start-up information from Fusion; not used.
    """
    global _addin
    if _addin is not None:
        _addin.stop()
    _addin = LianaAddIn(adsk.core.Application.get(), Storage(ADDIN_DIR), webbrowser.open)
    _addin.start()


def stop(context: object) -> None:
    """Stop the add-in (called by Fusion).

    The add-in's other modules are dropped from the import cache, so that
    Run after an update loads the new code instead of the modules Python
    kept in memory. A module counts as the add-in's when its file is in the
    add-in folder, whatever package name Fusion gave the folder.

    Args:
        context: Shut-down information from Fusion; not used.
    """
    global _addin
    if _addin is not None:
        _addin.stop()
        _addin = None
    for name in _own_modules():
        del sys.modules[name]


def _own_modules() -> list[str]:
    """Return the names of the loaded modules from the add-in folder, but this one."""
    folder = os.path.normcase(str(ADDIN_DIR)) + os.sep
    own = []
    for name, module in list(sys.modules.items()):
        path = getattr(module, "__file__", None)
        if name == __name__ or not isinstance(path, str):
            continue
        if os.path.normcase(os.path.realpath(path)).startswith(folder):
            own.append(name)
    return own
