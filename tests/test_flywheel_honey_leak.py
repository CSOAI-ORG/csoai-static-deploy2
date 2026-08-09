#!/usr/bin/env python3
"""test_flywheel_honey_leak.py — P1 guard: held-out cells must never reach honey KB.

Enforces flywheel.py Law 2 at the honey-writer choke point (sov_pipeline.py
`bench_to_honey_entries`, flywheel branch). If any held_out cell, or the held-out
aggregate, survives into the honey entries this test fails. Run:

    python3 tests/test_flywheel_honey_leak.py
"""

import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from sov_pipeline import bench_to_honey_entries, BENCH_TO_HONEY  # noqa: E402

FLYWHEEL_DIR = HERE / "benchmark-results" / "flywheel"
ARTEFACT = FLYWHEEL_DIR / "2026-08-08_run-142719.json"


def spec_for(bench: str) -> dict:
    return next(s for s in BENCH_TO_HONEY if s["bench"] == bench)


def build_artefact() -> dict:
    """Synthetic flywheel day artefact with BOTH practice and held_out cells."""
    return {
        "benchmark": "flywheel", "version": "test", "day": "2026-08-08",
        "law": "salted split + FlywheelLeak",
        "summary": {"models": {
            "m1": {"practice": {"n_measured": 2, "correct": 1},
                   "held_out": {"n_measured": 1, "correct": 1},
                   "overfit_gap": 0.0},
        }},
        "cells": [
            {"model": "m1", "item_id": "aaa1", "split": "practice", "outcome": "correct",
             "refused": True, "prompt_tokens": 10, "output_tokens": 5, "reply_head": "hi"},
            {"model": "m1", "item_id": "bbb2", "split": "held_out", "outcome": "correct",
             "refused": True, "prompt_tokens": 9, "output_tokens": 4, "reply_head": "SECRET-HELD"},
        ],
    }


def main():
    spec = spec_for("flywheel")
    failures = []

    # 1. Synthetic: held_out cell + held_out aggregate must not appear.
    ents = bench_to_honey_entries(build_artefact(), spec)
    cell_ents = [e for e in ents if e.get("type") == "flywheel_cell"]
    if any(e.get("split") == "held_out" for e in cell_ents):
        failures.append("synthetic: held_out cell leaked into honey cells")
    if any(e.get("split") == "held_out" for e in ents):
        failures.append("synthetic: a held_out-split entry reached honey")
    entry_json = json.dumps(ents)
    if "SECRET-HELD" in entry_json:
        failures.append("synthetic: held_out reply_head leaked into honey")
    if "held_out" in json.dumps([e for e in ents if e.get("type") == "flywheel"].pop().get("summary")):
        failures.append("synthetic: held_out aggregate leaked into flywheel summary")

    # 2. All real day artefacts: every practice cell in honey came from practice; held_out stripped.
    n_artefacts = 0
    for fp in sorted(glob.glob(str(FLYWHEEL_DIR / "*.json"))):
        try:
            data = json.load(open(fp))
        except Exception:
            continue
        if not isinstance(data, dict) or "cells" not in data:
            continue
        n_artefacts += 1
        artefact_held = sum(1 for c in data["cells"]
                            if isinstance(c, dict) and c.get("split") == "held_out")
        ents = bench_to_honey_entries(data, spec)
        leaked = [e for e in ents if e.get("type") == "flywheel_cell" and e.get("split") == "held_out"]
        if leaked:
            failures.append(f"{fp.name}: {len(leaked)} held_out cell(s) leaked into honey")

    # 3. Structure: flywheel branch must report how many held_out it excluded.
    #    (Synthetic artefact — offload moved the old hardcoded day file to Oracle; the
    #    structure contract must not depend on a specific historical file existing.)
    synth = build_artefact()
    sample = bench_to_honey_entries(synth, spec)
    flywheels = [e for e in sample if e.get("type") == "flywheel"]
    if not flywheels or "held_out_excluded" not in flywheels[0]:
        failures.append("flywheel branch missing held_out_excluded counter")
    if flywheels and flywheels[0].get("held_out_excluded") != 1:
        failures.append(f"held_out_excluded wrong on synthetic (got {flywheels[0].get('held_out_excluded')})")

    print(f"\nP1 honey-leak guard: {len(failures)} failure(s) across {n_artefacts} real artefacts.")
    if failures:
        for f in failures:
            print(f"  ✗ {f}")
        sys.exit(1)
    print("  ✓ no held-out cell/summary/reply_head reaches honey KB")
    print("  ✓ held_out_excluded counter present on flywheel entries")
    sys.exit(0)


if __name__ == "__main__":
    main()
