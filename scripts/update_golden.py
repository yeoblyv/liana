# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Record the golden traces again from the current code.

Run this only after checking an intended change of the model in Fusion; the
diff of ``tests/golden`` is then part of the review.

Usage:
    python scripts/update_golden.py
"""

from __future__ import annotations

import gzip
import importlib
import json
import sys

from _project import ROOT

GOLDEN = ROOT / "tests" / "golden"
"""Folder with the golden records."""


def main() -> int:
    """Command line entry point."""
    sys.path.insert(0, str(ROOT))
    importlib.import_module("tests.conftest")  # installs the fake Fusion API as adsk
    golden = importlib.import_module("tests.test_golden")
    cases = importlib.import_module("tests.golden_cases").CASES
    for case in cases:
        record = golden.run_case(case)
        if record["errors"]:
            print("%s: the fake API reports %s" % (case.name, record["errors"][:3]))
            return 1
        data = json.dumps(record, indent=0).encode("utf-8")
        with gzip.GzipFile(GOLDEN / (case.name + ".json.gz"), "wb", mtime=0) as fh:
            fh.write(data)
        print("%-24s %5d events  %s" % (case.name, len(record["trace"]), record["modes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
