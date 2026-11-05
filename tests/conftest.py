# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Install the fake Fusion API as ``adsk`` before the add-in is imported."""

from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

import tests.fake_adsk as fake
from tests.fake_adsk import core, fusion

SRC = Path(__file__).resolve().parents[1] / "src"
"""Folder that holds the add-in package."""

sys.modules["adsk"] = fake
sys.modules["adsk.core"] = core
sys.modules["adsk.fusion"] = fusion
setattr(fake, "core", core)
setattr(fake, "fusion", fusion)
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture
def world() -> Iterator[fake.World]:
    """Give the test a fresh fake Fusion process."""
    yield fake.reset()
