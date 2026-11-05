# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""State shared by the builders during one build."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

from ..core.expr import neg
from ..core.report import BuildLog
from .api import MM, Application, Design, first_line

_T = TypeVar("_T")


@dataclass
class BuildContext:
    """The design being built, the application and the log of the build.

    Attributes:
        app: Fusion application.
        design: Design that receives the system.
        log: Problems recorded so far.
    """

    app: Application
    design: Design
    log: BuildLog = field(default_factory=BuildLog)

    def ev(self, expr: str) -> float:
        """Evaluate an expression against the design parameters, in mm."""
        return float(self.design.unitsManager.evaluateExpression(expr, "mm")) / MM

    def mag(self, expr: str) -> tuple[str, float]:
        """Return an expression for the magnitude of ``expr`` and its value in mm.

        Sketch dimensions are always positive, so a negative coordinate is
        driven by its negation.
        """
        v = self.ev(expr)
        return (expr, v) if v >= 0 else (neg(expr), -v)

    def soft(self, name: str, fn: Callable[[], _T]) -> _T | None:
        """Run an optional finishing step; a failure is logged, not raised.

        Fillets, chamfers and colours only refine a part, so the part stays
        usable without them. Fusion can fail them in ways the API does not
        document (edge topology, tangency), hence the broad catch.

        Args:
            name: Label for the log, e.g. ``"Rail: end rounding"``.
            fn: The step.

        Returns:
            What ``fn`` returned, or None if it failed.
        """
        try:
            return fn()
        except Exception as e:  # any failure of an optional step is acceptable
            self.log.soft.append("%s: %s" % (name, first_line(e)))
            return None
