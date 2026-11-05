# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Every build scenario asks Fusion for exactly what the golden trace records.

The golden files were recorded from the release whose parts were checked in
Fusion and printed. A refactor that changes a sketch, a dimension, a feature
or their order changes the trace and fails here.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

import pytest

import tests.fake_adsk as fake
from Liana.cad.system import Progress, generate
from Liana.core.report import log_text
from Liana.core.settings import DEFAULTS, from_mapping
from tests.fake_adsk import core, fusion
from tests.golden_cases import CASES, Case

GOLDEN = Path(__file__).resolve().parent / "golden"
"""Folder with one gzip-compressed JSON record per case."""


def run_case(case: Case) -> dict[str, Any]:
    """Run one scenario against a fresh fake Fusion and return its record.

    Args:
        case: Scenario.

    Returns:
        Modes, fake-API errors, message boxes, build logs and the trace, in
        the layout of the golden files.
    """
    w = fake.reset()
    w.fail_first_direction = case.fail_first_direction
    w.point_constraints = case.point_constraints
    w.hole_feature_broken = case.hole_feature_broken
    app = core.Application.get()
    progress = Progress(app.userInterface)
    s = from_mapping({**DEFAULTS, **case.settings})
    design = fusion.Design()
    if case.scenario == "part_active":
        design.designIntent = "PART"
    if case.scenario == "busy_active":
        design.rootComponent.sketches.add(design.rootComponent.xYConstructionPlane)
    w.active_product = design
    mode, log = generate(app, s, progress)
    modes, logs = [mode], [log_text(mode, s, log)]
    if case.scenario in ("update", "rebuild", "new_flag"):
        s2 = from_mapping({**s, **case.second})
        mode, log = generate(app, s2, progress)
        modes.append(mode)
        logs.append(log_text(mode, s2, log))
    return {
        "modes": modes,
        "errors": w.errors,
        "messages": w.messages,
        "logs": logs,
        "trace": w.trace,
    }


def _normalise(record: dict[str, Any]) -> dict[str, Any]:
    """Round-trip through JSON so tuples and lists compare equal."""
    result: dict[str, Any] = json.loads(json.dumps(record))
    return result


@pytest.mark.parametrize("case", CASES, ids=[c.name for c in CASES])
def test_trace_matches_golden(case: Case) -> None:
    with gzip.open(GOLDEN / (case.name + ".json.gz"), "rt", encoding="utf-8") as fh:
        expected = json.load(fh)
    actual = _normalise(run_case(case))
    assert actual["errors"] == []
    assert actual["modes"] == expected["modes"]
    assert actual["messages"] == expected["messages"]
    assert actual["logs"] == expected["logs"]
    for i, (a, e) in enumerate(zip(actual["trace"], expected["trace"])):
        assert a == e, "first difference at event %d" % i
    assert len(actual["trace"]) == len(expected["trace"])
