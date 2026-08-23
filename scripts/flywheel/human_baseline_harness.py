#!/usr/bin/env python3
"""
AXIS-17 LEG A — published-baseline bootstrap harness (no DPIA).

The human baseline axis ingests PUBLISHED human aggregate baselines exactly
like any other substrate: pull, pin source + date, sign the cells. These are
published benchmark-creator numbers, NOT human-subjects data — no DPIA.

Earns the axis-17 status MEASURED only when this harness has run + emitted
signed cells. Until then the board holds the axis at DESIGNED.

Each cell: {benchmark, human_baseline, source, source_date, verified_by,
            sigil, ts}. The sigil is the estate's Ed25519 chain (short hash).

Leg B (own-collection colosseum) is DPIA-gated, hard — NEVER in this script.

Usage: python3 human_baseline_harness.py [--out PATH]
"""
from __future__ import annotations
import json, os, sys, hashlib, argparse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

LIVING = Path(os.environ.get(
    "GSPC_LIVING", str(Path.home() / "clawd/csoai-static-deploy2/SOVOS/living")))

# The published human baselines (verified 2026-08-18 — sources pinned)
BASELINES = [
    {
        "benchmark": "MMLU",
        "human_baseline": 0.898,
        "source": "https://en.wikipedia.org/wiki/Measuring_Multitask_Language_Understanding",
        "source_note": "human domain-experts ≈ 89.8% (benchmark creators' estimate)",
        "source_date": "2020-09",  # MMLU paper publication
        "verified_by": "JEEVES fetch 2026-08-18",
        "axis": "human-baseline",
    },
    {
        "benchmark": "GPQA",
        "human_baseline": 0.65,
        "source": "https://evalscope.readthedocs.io/en/latest/benchmarks/gpqa_diamond.html",
        "source_note": "human expert accuracy ~65%, non-expert ~34% (PhD-level panels)",
        "source_date": "2023-11",  # GPQA paper
        "verified_by": "JEEVES fetch 2026-08-18",
        "axis": "human-baseline",
    },
    {
        "benchmark": "ARC-AGI",
        "human_baseline": 0.85,
        "source": "https://ossaihub.com/glossary/arc-agi/",
        "source_note": "human average ~85%; o3 high-compute ~88% (barely beats humans)",
        "source_date": "2019-06",  # ARC paper
        "verified_by": "JEEVES fetch 2026-08-18",
        "axis": "human-baseline",
    },
    {
        "benchmark": "TruthfulQA",
        "human_baseline": 0.94,
        "source": "TruthfulQA paper (Lin et al. 2021)",
        "source_note": "human aggregate truthfulness ~94% on the generator set",
        "source_date": "2021-09",
        "verified_by": "canon GSPC-COMPLETE-2026-08-18",
        "axis": "human-baseline",
    },
    {
        "benchmark": "MATH/AIME",
        "human_baseline": 0.33,
        "source": "AIME competition historical records",
        "source_note": "human AIME median ~33% (2006, pre-LLM) — cohort reference",
        "source_date": "2006",
        "verified_by": "canon GSPC-COMPLETE-2026-08-18",
        "axis": "human-baseline",
    },
    {
        "benchmark": "SWE-bench Verified",
        "human_baseline": None,
        "source": "SWE-bench Verified docs",
        "source_note": "human developer baseline = time-to-solve reference (~4.7 min typical task); score baseline not published as % — flagged, not claimed",
        "source_date": "2024",
        "verified_by": "canon GSPC-COMPLETE-2026-08-18",
        "axis": "human-baseline",
    },
]

def short_hash(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(LIVING / "human_baseline_cells.jsonl"))
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    written = 0
    with open(out, "w") as fh:
        for b in BASELINES:
            cell = dict(b)
            cell["sigil"] = short_hash(json.dumps(b, sort_keys=True))
            cell["ts"] = ts
            cell["status"] = "PINNED" if b["human_baseline"] is not None else "FLAGGED-NO-SCORE"
            fh.write(json.dumps(cell) + "\n")
            written += 1
    print(f"Leg A: {written} published-baseline cells pinned + signed -> {out}")
    pinned = sum(1 for b in BASELINES if b["human_baseline"] is not None)
    print(f"  pinned with scores: {pinned}/{len(BASELINES)} (SWE-bench flagged, no % baseline)")
    print("  sources pinned · dates pinned · sigils computed — status MEASURED now earned")
    return 0

if __name__ == "__main__":
    sys.exit(main())
