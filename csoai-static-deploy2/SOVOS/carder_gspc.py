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
    ap.add_argument("--enrich", action="store_true", help="fetch licence + fields for unstated candidates")
    ap.add_argument("--predicate", action="store_true", help="stream first rows to extract real column names (GREEN-licence only)")
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

    if args.enrich:
        # Fetch full card metadata (licence + fields) for candidates that lack it.
        # Batch via HF API; Kaggle candidates without a known licence stay unstated.
        if not CANDIDATES.exists():
            print("no candidates — run --scan first")
            return 1
        from huggingface_hub import HfApi
        api = HfApi()
        rows = [json.loads(l) for l in CANDIDATES.read_text().splitlines() if l.strip()]
        enriched = 0
        for i, r in enumerate(rows):
            if r.get("license") or r.get("licence"):
                continue
            if r.get("source") == "hf" and not r["id"].startswith("kaggle:"):
                try:
                    info = api.dataset_info(r["id"])
                    lic = str(getattr(info, "cardData", None) and getattr(info.cardData, "license", "") or "")
                    r["license"] = lic
                    r["licence"] = lic
                    cfg = getattr(info, "siblings", []) or []
                    r["fields"] = sorted({s.rfilename.split(".")[0] for s in cfg})[:12]
                    enriched += 1
                except Exception:
                    pass
            elif r.get("source") == "kaggle":
                r["licence"] = r.get("license") or "kaggle-unstated"
            if i and i % 50 == 0:
                print(f"  enrich {i}/{len(rows)} ({enriched} new)...")
        CANDIDATES.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        print(f"CARDER enrich: {enriched} candidates got metadata → {CANDIDATES}")
        return 0

    if args.predicate:
        # Extract REAL column names by streaming the first row of GREEN-licence
        # candidates — file paths are not predicates. Streaming reads a small
        # shard, not the whole dataset.
        if not CANDIDATES.exists():
            print("no candidates — run --scan first")
            return 1
        rows = [json.loads(l) for l in CANDIDATES.read_text().splitlines() if l.strip()]
        hits = 0
        for i, r in enumerate(rows):
            if r.get("source") != "hf" or r["id"].startswith("kaggle:"):
                continue
            if not (r.get("license") or r.get("licence")):
                continue  # unstated licence — predicate moot
            lic = (r.get("license") or r.get("licence") or "").lower()
            if any(x in lic for x in RESTRICTED):
                continue  # RED licence — predicate moot
            if not any(p in lic for p in PERMISSIVE):
                continue  # YELLOW licence — predicate moot
            try:
                from datasets import load_dataset
                import signal
                def _timeout(sig, frm):
                    raise TimeoutError("dataset stream hung")
                signal.signal(signal.SIGALRM, _timeout)
                signal.alarm(20)  # 20s per dataset — hung streams must not stall intake
                ds = load_dataset(r["id"], split="train", streaming=True)
                row = next(iter(ds))
                signal.alarm(0)
                cols = sorted(row.keys())
                if cols:
                    r["fields"] = cols
                    r["predicate_ok"] = True
                    hits += 1
            except Exception:
                pass
            if i and i % 40 == 0:
                print(f"  predicate {i}/{len(rows)} ({hits} with columns)...")
        CANDIDATES.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        print(f"CARDER predicate: {hits} candidates got real column names → {CANDIDATES}")
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

    # --scan: intake sweep (hf | kaggle), deduped against existing candidates
    existing = set()
    if CANDIDATES.exists():
        for line in CANDIDATES.read_text().splitlines():
            if line.strip():
                try:
                    existing.add(json.loads(line)["id"])
                except Exception:
                    pass

    def _append(recs):
        written = 0
        with open(CANDIDATES, "a") as fh:
            for r in recs:
                if r["id"] in existing:
                    continue
                fh.write(json.dumps(r) + "\n")
                existing.add(r["id"])
                written += 1
        return written

    if args.scan == "hf":
        try:
            from huggingface_hub import HfApi
            api = HfApi()
            # Broader sweep: multiple searches cover the measurement space.
            searches = ["ai benchmark", "llm evaluation", "jailbreak dataset", "governance ai",
                        "safety benchmark", "model evaluation", "alignment dataset"]
            recs = []
            for q in searches:
                for d in api.list_datasets(limit=40, search=q):
                    recs.append({"id": d.id, "name": d.id, "source": "hf",
                                 "url": f"https://huggingface.co/datasets/{d.id}",
                                 "license": str(getattr(getattr(d, "cardData", None), "license", "") or ""),
                                 "axis_hint": None, "fields": [], "sample_text": ""})
            written = _append(recs)
            print(f"CARDER scan: {written} new HF candidates (of {len(recs)} found) → {CANDIDATES}")
            return 0
        except ImportError:
            print("huggingface_hub not installed — using the seed candidate list")
            written = _append([{
                "id": "csoai-gspc-normalized", "name": "csoai-gspc-normalized", "source": "kaggle",
                "url": "https://kaggle.com/datasets/nicktempleman/csoai-gspc-normalized",
                "license": "apache-2.0", "axis_hint": "all", "fields": ["prompt", "axis"], "sample_text": ""}])
            print(f"CARDER seed: {written} candidates (huggingface_hub unavailable)")
            return 0

    if args.scan == "kaggle":
        import subprocess
        queries = ["llm benchmark", "ai safety", "jailbreak", "ai governance"]
        recs = []
        for q in queries:
            try:
                out = subprocess.run(["kaggle", "datasets", "list", "-s", q, "--sort-by", "hottest"],
                                     capture_output=True, text=True, timeout=60).stdout
                for line in out.splitlines()[3:]:  # skip header rows
                    parts = [p for p in line.split("  ") if p.strip()]
                    if len(parts) >= 2 and "/" in parts[0]:
                        ds_ref = parts[0].strip()
                        recs.append({"id": f"kaggle:{ds_ref}", "name": ds_ref, "source": "kaggle",
                                     "url": f"https://kaggle.com/datasets/{ds_ref}",
                                     "license": "", "axis_hint": None, "fields": [], "sample_text": ""})
            except Exception:
                continue
        written = _append(recs)
        print(f"CARDER scan: {written} new Kaggle candidates (of {len(recs)} found) → {CANDIDATES}")
        return 0

    print("no --scan source given — use --scan hf|kaggle, --grade, or --status")
    return 1

if __name__ == "__main__":
    sys.exit(main())
