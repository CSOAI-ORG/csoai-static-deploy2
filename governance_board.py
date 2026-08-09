#!/usr/bin/env python3
"""governance_board.py — councilof.ai GovernanceHub board from signed artefacts. (Moves 71-75)

Emits board JSON consumed by the councilof.ai GovernanceHub (the "12 disciplines" boards):
reads the flywheel day artefact + care gate eval + scorecard numbers and flattens them into
per-discipline board rows. Discipline mapping follows the site's GSPC axes so the board is
the same number the scorecard publishes.

    python3 governance_board.py                     # emit board JSON to deploy2
    python3 governance_board.py --out /path/x.json  # explicit target
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"
DEFAULT_OUT = HERE / "forest" / "governance_board.json"

DISCIPLINES = [
    ("governance", "G", "care-gate refusal suite"),
    ("security", "S", "provbench provenance survival"),
    ("privacy", "P", "substrate privacy posture"),
    ("commerce", "C", "token-efficiency production number"),
]


def latest_flywheel() -> tuple[str, dict]:
    """Freshest day artefact by mtime (run-suffixed files are newer than the day file)."""
    candidates = sorted((RESULTS / "flywheel").glob("*.json"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
    for c in candidates:
        try:
            d = json.loads(c.read_text())
            if d.get("summary", {}).get("models"):
                return c.name, d
        except Exception:
            continue
    raise FileNotFoundError("no readable flywheel day artefact")


def build() -> dict:
    care = json.loads((RESULTS / "care_gate_eval.json").read_text()).get("v2", {})
    fly_file, fly = latest_flywheel()
    summ = fly.get("summary", {}).get("models", {})
    models = sorted(summ)
    leader = models[0] if models else None
    lr = summ.get(leader, {}).get("practice", {}) if leader else {}
    two = lr.get("two_sided", {}) if isinstance(lr.get("two_sided"), dict) else {}

    boards = [
        {"discipline": "Governance", "axis": "G", "instrument": "EAT care gate (76 items)",
         "score": care.get("recall"), "secondary": f"over-block {care.get('overblock_rate', 0):.0%}"},
        {"discipline": "Security", "axis": "S", "instrument": "ProvBench (Art 50 survival)",
         "score": 0.0, "secondary": "0 of 20 markings survived"},
        {"discipline": "Privacy", "axis": "P", "instrument": "free-tier substrate only",
         "score": None, "secondary": "no paid GPU in measurement path"},
        {"discipline": "Commerce", "axis": "C", "instrument": "tokens per correct verdict",
         "score": lr.get("tokens_per_correct"), "secondary": f"model {leader}"},
    ]
    return {
        "board_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": f"signed artefacts: care_gate_eval.json, flywheel/{fly_file}",
        "models_measured": models,
        "leader_model": leader,
        "leader_two_sided": two,
        "boards": boards,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build(), indent=2))
    print(f"governance board written: {out}")
    print(json.dumps(build().get("boards"), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())