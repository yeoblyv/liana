---
id: architecture.testing
title: Testing
slug: /architecture/testing
category: Architecture
since: 1.0.0
status: stable
---

[Docs](../README.md) / Architecture / Testing

# Testing

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

How Liana is tested without Fusion, what the golden traces pin down, and
what is left to the manual checks in Fusion.

## On this page

- [Testing without Fusion](#testing-without-fusion)
- [Golden traces](#golden-traces)
- [Unit tests](#unit-tests)
- [What needs Fusion](#what-needs-fusion)
- [Examples](#examples)
- [See also](#see-also)
- [References](#references)
- [Changelog](#changelog)

## Testing without Fusion

Fusion cannot run in CI, so `tests/fake_adsk` implements the part of the
API that Liana uses. `tests/conftest.py` installs it as `adsk` before the
add-in is imported. The fake keeps enough geometry to check that every
dimension agrees with the drawn geometry and every constraint holds, and
it records each call that changes the design in a trace.

## Golden traces

`tests/test_golden.py` runs 42 scenarios (cradle counts, cable sizes, part
combinations, updates, rebuilds, failure fallbacks) and compares each
trace with `tests/golden`. A change to any sketch, dimension or feature,
or to their order, fails there.

When a change to the model is intended, check it in Fusion [R1], then
record the traces again and review the difference:

```bash
python scripts/update_golden.py
git diff --stat tests/golden
```

## Unit tests

Unit tests cover what the traces do not: the fallbacks that run only when
Fusion refuses something, settings validation, storage, the dialog, the
event handlers and the add-in lifecycle.

## What needs Fusion

Real geometry, fillets and chamfers, the look of the dialog and the icons
are checked by hand in Fusion on Windows and macOS before a release [R1].

## Examples

```bash
python -m pytest -q tests/test_golden.py
python -m pytest -q --cov
```

## See also

- [Workflow](../contributing/workflow.md): when to run which gate.
- [Architecture overview](overview.md): the code under test.

## References

- [R1]: ../contributing/fusion-test-checklist.md#builds "Testing in Fusion - Builds"

## Changelog

- 1.0.0: page added.
