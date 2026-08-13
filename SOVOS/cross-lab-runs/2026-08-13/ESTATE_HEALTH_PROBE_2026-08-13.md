# Estate Health Probe — 2026-08-13 (mined/verified, not assumed)

## Test estate reality on the A100
Probed live (post re-provision, which wiped the venv):
- Disk: **792 test functions across 63 test files** (packages tree)
- Via PYTHONPATH (no editable install needed): **756 tests collected, 5 collection
  errors** — all 5 are ENVIRONMENT import-path artifacts, NOT code regressions:
  - sovos-mind integration test needs a top-level `sovos` module (vendor/nested
    layout) → infra path issue
  - dream/router errors are cascade/conftest collection artifacts (pass standalone)
- pytest NOT present on the pod (venv wiped in re-provision) → reinstalled to
  /workspace/venv-test (pytest 9.1.1)

## Finding: the aggregator pyproject editable install is BROKEN
`pip install -e .` fails: `tool.setuptools.packages` → "0 matches found". The
packages mapping (46 entries, `from="src"`) doesn't resolve on this pod. This is
the Part AR.4 "aggregator pyproject owed" item surfacing as a hard failure. It
blocks the canonical `pip install -e .` but NOT development (PYTHONPATH works).
**Lane-executable fix owed:** repair pyproject packages config (sed via the
find/include form) and re-verify — next pass, not tonight's blocker.

## Register vs reality
- "758 green on A100" was true in a properly-installed context; the pod's venv was
  wiped. Reproduced: 756 collectible now + 5 env-collection errors. No code
  regression behind the errors.
- Test-function count: 792 (this session's disk count supersedes earlier 657/698/
  758 as the current tree number; scopes differ — record counts with scope).

## Not a race, not panic
The estate's test code is intact; the pod's test environment was transient-wiped
(known re-provision class, Part BX). Re-establishing pytest (done) + enabling the
packages install (owed) restores full green-sweep capability.