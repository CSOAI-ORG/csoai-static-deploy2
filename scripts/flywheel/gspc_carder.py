#!/usr/bin/env python3
"""gspc_carder.py — the dataset intake valve of the sim/human cross-flywheel.

CARDER → DECOMPOSER → SIM → THE CROSS (MEASURED vs REPORTED human) → SIGNED CARDS → back in.

Scans HF/Kaggle for candidate benchmark datasets, grades each GREEN/YELLOW/RED
on the three gates the estate already owns, and emits the GREEN intake list for
the decomposer pipeline (which turns canon into signed 3KB units → sim fuel).

The three gates (all already canon):
  1. LICENCE-CLEAN — permissive (Apache/MIT/CC-BY/CC0/ODC-BY) → GREEN; NC/ND/SA-family
     → YELLOW (quarantine from commercial bank); proprietary → RED.
  2. CANARY-CLEAN — no forbidden strings in the dataset content (the kill-list
     applies to what we PULL in, not just what we emit).
  3. PREDICATE-COMPATIBLE — rows can be scored by a deterministic predicate
     (exact_match/refusal/action_forbidden/manifest_valid/signature_alg), not
     just an LLM judge.

Output: SOVOS/living/carder_green.jsonl — the intake list. RED licence on one
dataset never touches the commercial bank.

Usage:
  python3 gspc_carder.py --scan hf          # scan HF for candidate datasets
  python3 gspc_carder.py --grade           # re-grade the candidate list
  python3 gspc_carder.py --status          # show the intake state
"""
from __future__ import annotations
import json, os, sys, argparse
from pathlib import Path
from datetime import datetime, timezone

LIVING = Path(os.environ.get(
    "GSPC_LIVING", str(Path.home() / "clawd/csoai-static-deploy2/SOVOS/living")))
CANDIDATES = LIVING / "carder_candidates.jsonl"
GREEN = LIVING / "carder_green.jsonl"

# Permissive licence roots (case-insensitive substring match).
PERMISSIVE = ["apache", "mit", "cc-by", "cc0", "cc by", "odc-by", "bsd", "unlicense", "mpl"]
RESTRICTED = ["cc-by-nc", "nc-sa", "nd", "by-sa", "cc-by-sa", "non-commercial", "all rights reserved", "proprietary"]

# The kill-list — strings that must not appear in rows we pull in.
BANNED = ["sovereign", "sovos", "defoneos", "byzantine", "bft", "33-agent", "ceasai"]

# Deterministic predicates we can score rows with.
PREDICATES = ["exact_match", "refusal", "action_forbidden", "manifest_valid", "signature_alg"]

def grade(meta: dict) -> dict:
    """Grade one candidate dataset on the three gates."""
    lic = (meta.get("license") or meta.get("licence") or "").lower()
    # 1. licence — RESTRICTED wins (a NC/ND/SA variant of an otherwise-permissive
    # licence is still restricted for commercial use). Order matters: check the
    # restricted markers FIRST, before the permissive root.
    if not lic:
        lic_status = "YELLOW"  # unstated licence = cautious
    elif any(r in lic for r in RESTRICTED):
        lic_status = "RED"
    elif any(p in lic for p in PERMISSIVE):
        lic_status = "GREEN"
    else:
        lic_status = "YELLOW"
    # 2. canary (sample rows if available)
    sample = str(meta.get("sample_text", ""))[:2000].lower()
    canary = "GREEN" if not any(b in sample for b in BANNED) else "RED"
    # 3. predicate-compatible (the row shape must fit a deterministic scorer)
    fields = set(meta.get("fields") or [])
    pred = "GREEN" if (fields & {"prompt", "question", "input", "text"}) or meta.get("predicate_ok") else "YELLOW"
    # verdict
    reds = [lic_status, canary, pred].count("RED")
    verdict = "RED" if reds >= 1 else ("GREEN" if [lic_status, canary, pred].count("GREEN") == 3 else "YELLOW")
    return {
        "licence": lic_status, "canary": canary, "predicate": pred, "verdict": verdict,
        "licence_note": lic or "unstated",
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", choices=["hf", "kaggle"], help="scan a source for candidates")
    ap.add_argument("--grade", action="store_true", help="re-grade candidates")
    ap.add_argument("--status", action="store_true", help="show intake state")
    args = ap.parse_args()

    if args.status:
        cands = [json.loads(l) for l in CANDIDATES.read_text().splitlines() if l.strip()] if CANDIDATES.exists() else []
        greens = [json.loads(l) for l in GREEN.read_text().splitlines() if l.strip()] if GREEN.exists() else []
        print(f"CARDER — candidates: {len(cands)} | GREEN intake: {len(greens)}")
        for g in greens[:5]:
            print(f"  {g.get('id')}: {g.get('verdict')} lic={g.get('licence')}")
        return 0

    if args.grade:
        if not CANDIDATES.exists():
            print("no candidates — run --scan first")
            return 1
        greens = []
        for line in CANDIDATES.read_text().splitlines():
            if not line.strip():
                continue
            meta = json.loads(line)
            g = grade(meta)
            rec = {"id": meta.get("id"), "name": meta.get("name"), "source": meta.get("source"),
                   "url": meta.get("url"), "axis_hint": meta.get("axis_hint"), **g}
            if g["verdict"] == "GREEN":
                greens.append(rec)
        GREEN.write_text("\n".join(json.dumps(r) for r in greens) + "\n")
        print(f"CARDER grade: {len(greens)} GREEN of {sum(1 for _ in CANDIDATES.read_text().splitlines())} candidates → {GREEN}")
        return 0

    # --scan: HF candidates (the intake sweep)
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        ds = api.list_datasets(limit=100, search="governance ai benchmark")
        written = 0
        with open(CANDIDATES, "a") as fh:
            for d in ds:
                rec = {"id": d.id, "name": d.id, "source": "hf",
                       "url": f"https://huggingface.co/datasets/{d.id}",
                       "license": str(getattr(getattr(d, "cardData", None), "license", "") or ""),
                       "axis_hint": None, "fields": [], "sample_text": ""}
                fh.write(json.dumps(rec) + "\n")
                written += 1
        print(f"CARDER scan: {written} HF candidates → {CANDIDATES}")
        return 0
    except ImportError:
        print("huggingface_hub not installed — using the seed candidate list")
        seeds = [
            {"id": "csoai-gspc-normalized", "name": "csoai-gspc-normalized", "source": "kaggle",
             "url": "https://kaggle.com/datasets/nicktempleman/csoai-gspc-normalized",
             "license": "apache-2.0", "axis_hint": "all", "fields": ["prompt", "axis"], "sample_text": ""},
        ]
        with open(CANDIDATES, "a") as fh:
            for s in seeds:
                fh.write(json.dumps(s) + "\n")
        print(f"CARDER seed: {len(seeds)} candidates (huggingface_hub unavailable)")
        return 0

if __name__ == "__main__":
    sys.exit(main())
