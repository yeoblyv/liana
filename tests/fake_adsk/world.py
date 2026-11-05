# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Process-wide state of the fake Fusion API: trace, parameters and switches."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any

TraceEvent = tuple[Any, ...]

_UNIT_RE = re.compile(r"\b(mm|deg)\b")


@dataclass
class World:
    """Everything the fake application knows; one instance per test.

    Attributes:
        trace: Ordered record of every call that changes the design or the UI.
        errors: Inconsistencies the fake detected, for example a dimension
            whose expression disagrees with the drawn geometry.
        values: Evaluated user parameters, in millimeters (degrees for angles).
        expressions: User parameter expressions by name.
        order: User parameter names in creation order (dependency order).
        fail_first_direction: When true, the first one-sided extrude or hole
            of every sketch goes the wrong way, as Fusion does when a plane
            normal points away from the part.
        point_constraints: Whether the sketch supports the newer
            ``addHorizontalPoints`` / ``addVerticalPoints`` constraints.
        hole_feature_broken: Makes every Hole feature raise, to exercise the
            extrude-cut fallback.
        new_design_intent: Design intent of documents created by
            ``documents.add``.
        messages: Text of every message box shown.
        answer: What the user clicks in a Yes/No message box.
    """

    trace: list[TraceEvent] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    values: dict[str, float] = field(default_factory=dict)
    expressions: dict[str, str] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)
    fail_first_direction: bool = False
    point_constraints: bool = True
    hole_feature_broken: bool = False
    new_design_intent: str = "HY"
    containment: str = "IN"
    containment_queue: list[str] = field(default_factory=list)
    attempts: dict[tuple[Any, ...], int] = field(default_factory=dict)
    messages: list[str] = field(default_factory=list)
    answer: str = "DialogNo"
    active_product: Any = None
    documents: list[Any] = field(default_factory=list)
    app: Any = None

    def trace_event(self, *event: Any) -> None:
        """Append one event to the trace."""
        self.trace.append(tuple(event))

    def evaluate(self, expr: str) -> float:
        """Evaluate a Fusion expression against the current user parameters.

        Args:
            expr: Expression such as ``"END_X0 + 2 mm"``.

        Returns:
            The value in millimeters (degrees for angle expressions).
        """
        names: dict[str, Any] = dict(self.values)
        names["sqrt"] = math.sqrt
        value = eval(_UNIT_RE.sub("", expr), {"__builtins__": {}}, names)
        return float(value)

    def recompute(self) -> None:
        """Re-evaluate every parameter after an expression change."""
        for name in self.order:
            self.values[name] = self.evaluate(self.expressions[name])


_current = World()


def world() -> World:
    """Return the world of the running test."""
    return _current


def reset() -> World:
    """Start a fresh world and return it."""
    global _current
    _current = World()
    return _current


def mm(value_cm: float) -> float:
    """Convert Fusion internal centimetres to millimeters, rounded for traces."""
    return round(value_cm * 10.0, 6) + 0.0
