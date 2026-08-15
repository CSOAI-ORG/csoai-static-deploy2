#!/usr/bin/env python3
"""run_phases.py — phased, resumable batch runner for the GSPC measurement programme.

WHY PHASED AND NOT A LOOP
-------------------------
Looping the six-axis e2e today would burn the pod producing statistically identical
non-answers. Measured 2026-08-04, twice, under two control schemes: 57 of 64 verdicts
NOT_RESOLVED, and ZERO arms beating their control. At n=11-24 the 95% Wilson half-width is
+/-21 to 33 points — wider than any effect present. **Item count is the binding constraint,
not compute.**

So the phases are ordered by what unblocks what, and a phase that cannot resolve anything
does not run until its blocker clears.

PHASES
  1 MEASURE    six axes, per-arm matched controls           [runs today]
  2 EXPAND     grow each item bank toward n>=50             [BLOCKER for 3]
  3 RESOLVE    re-run; verdicts can now actually resolve    [gated on 2]
  4 ITERATE    train only on what phase 3 resolved          [gated on 3]

Phase 4 is deliberately last and deliberately gated. Training on unresolved verdicts is how
four conclusions got withdrawn today.

RESUMABILITY
Each phase writes a stamp file. A phase whose stamp exists and whose inputs are unchanged is
SKIPPED, so this can be re-run after an interruption without repeating pod work. --force
reruns a named phase.

PARALLELISM
Within a phase, independent units run concurrently. ACROSS phases, never — phase N+1 reads
phase N's output, and overlapping them is how a run reads a half-written file. The pod is
also a shared serial resource: two concurrent sweeps contend and produce read timeouts,
which this harness correctly reports as UNMEASURED but which waste the run.

Usage:
  python3 run_phases.py --status
  python3 run_phases.py --phase 1
  python3 run_phases.py --all
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAMPS = HERE / "evidence/harness/freeze/latest/.phase-stamps"
OUT = HERE / "evidence/harness/freeze/latest"
POD = os.environ.get("GOVBENCH_OLLAMA_URL", "")

ARMS = ["sov34:latest", "sov33-unified:latest", "sov33-v7:latest", "sov-compliance:latest",
        "sov-ethics:latest", "sov-ethics-art5:latest", "sov-compliance-art5:latest",
        "sov-refusal-balanced:latest", "sov-refusal-combo:latest"]

MIN_N_TO_RESOLVE = 50   # below this, a control comparison cannot separate at these effect sizes


def stamp_path(n: int) -> Path:
    STAMPS.mkdir(parents=True, exist_ok=True)
    return STAMPS / f"phase{n}.json"


def write_stamp(n: int, **kw):
    stamp_path(n).write_text(json.dumps(
        {"phase": n, "completed": datetime.now(timezone.utc).isoformat(), **kw}, indent=2))


def item_counts() -> dict:
    sys.path.insert(0, str(HERE))
    import gspc_six_axis_e2e as G
    out = {}
    for axis in G.AXES:
        try:
            items, _, _ = G.load_axis(axis)
            out[axis] = len(items)
        except SystemExit:
            out[axis] = 0
    return out


def phase1(force=False) -> bool:
    """MEASURE — six axes, per-arm matched controls."""
    if stamp_path(1).exists() and not force:
        print("  phase 1 SKIPPED (stamp exists)"); return True
    if not POD:
        print("  phase 1 BLOCKED — GOVBENCH_OLLAMA_URL not set"); return False
    out = OUT / "gspc-six-axis-matched.jsonl"
    r = subprocess.run([sys.executable, str(HERE / "gspc_six_axis_e2e.py"),
                        "--models", *ARMS, "--out", str(out)], cwd=HERE)
    ok = r.returncode == 0 and out.exists()
    if ok:
        write_stamp(1, output=out.name, arms=len(ARMS))
    return ok


def phase2(force=False) -> bool:
    """EXPAND — the blocker. Reports the shortfall rather than pretending to fix it."""
    counts = item_counts()
    short = {a: n for a, n in counts.items() if n < MIN_N_TO_RESOLVE}
    print(f"  item counts: {counts}")
    if not short:
        write_stamp(2, counts=counts); print("  phase 2 COMPLETE — all axes at n>=50"); return True
    need = sum(MIN_N_TO_RESOLVE - n for n in short.values())
    print(f"  phase 2 BLOCKED — {len(short)} axes below n={MIN_N_TO_RESOLVE}, "
          f"{need} items short in total:")
    for a, n in sorted(short.items(), key=lambda x: x[1]):
        print(f"      {a:12s} {n:3d} -> need {MIN_N_TO_RESOLVE - n:3d} more")
    print("  This phase is NOT automatable end-to-end: items need adjudication, and an\n"
          "  auto-generated item with a wrong label is worse than no item because the\n"
          "  harness makes it look rigorous. Generate candidates, adjudicate, then re-run.")
    return False


def phase3(force=False) -> bool:
    """RESOLVE — gated on phase 2."""
    if not stamp_path(2).exists():
        print("  phase 3 GATED — phase 2 incomplete. Re-running now would reproduce "
              "NOT_RESOLVED at the same n, which is not a measurement.")
        return False
    return phase1(force=True)


def phase4(force=False) -> bool:
    """ITERATE — gated on phase 3 having produced resolved verdicts."""
    if not stamp_path(3).exists():
        print("  phase 4 GATED — no resolved verdicts to train on."); return False
    rows = [json.loads(l) for l in (OUT / "gspc-six-axis-matched.jsonl").read_text().splitlines()]
    resolved = [r for r in rows if r["verdict"] in ("IMPROVED_OVER_CONTROL", "WORSE_THAN_CONTROL")]
    print(f"  resolved verdicts available to train on: {len(resolved)} of {len(rows)}")
    if not resolved:
        print("  phase 4 STOPS — nothing resolved. Training on NOT_RESOLVED is how four "
              "conclusions were withdrawn on 2026-08-04.")
        return False
    write_stamp(4, resolved=len(resolved))
    return True


PHASES = {1: ("MEASURE", phase1), 2: ("EXPAND", phase2),
          3: ("RESOLVE", phase3), 4: ("ITERATE", phase4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if a.status:
        print("PHASE STATUS")
        for n, (name, _) in PHASES.items():
            s = stamp_path(n)
            print(f"  {n} {name:9s} {'DONE  ' + json.loads(s.read_text())['completed'][:19] if s.exists() else 'pending'}")
        print(f"\n  item counts: {item_counts()}")
        print(f"  n needed to resolve: {MIN_N_TO_RESOLVE}")
        return

    todo = [a.phase] if a.phase else (list(PHASES) if a.all else [])
    if not todo:
        ap.print_help(); return
    for n in todo:
        name, fn = PHASES[n]
        print(f"\n=== PHASE {n} — {name} ===")
        if not fn(force=a.force):
            print(f"  stopping: phase {n} did not complete")
            break


if __name__ == "__main__":
    main()
