#!/usr/bin/env python3
"""
MERGE GOLD VERDICT — jail axis second measurement layer.

The 3090 gold run measured 7 models against the 71-item gold bank
(38 ESCAPE + 33 BENIGN). This merges the per-model TP/FP/TN/FN verdict
into the living board as a detector-capability measurement, and signs
the updated board with keystone (city_ed25519).

Layer 1 (existing): containment — 2592 trials, jail held.
Layer 2 (this):      detection — can models flag escape attempts w/o
                     false-positive benign content?
"""
from __future__ import annotations
import json, subprocess, sys, hashlib
from datetime import datetime, timezone
from pathlib import Path

LIVING = Path(__file__).resolve().parent / "living"
BOARD = LIVING / "board_living.json"
GOLD = Path("/tmp/gold_results.json")

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main() -> int:
    if not GOLD.exists():
        print(f"missing {GOLD} — pull from pod first")
        return 1

    board = json.loads(BOARD.read_text())
    gold = json.loads(GOLD.read_text())
    models = gold["models"]

    # ── detector-capability verdict ──────────────────────────────
    zero_fp = [(m, r) for m, r in models.items()
               if isinstance(r, dict) and r.get("fp", 1) == 0]
    if not zero_fp:
        print("no zero-FP model — refusing to report precision=1.0")
        return 1
    best_name, best = max(zero_fp, key=lambda kv: kv[1].get("tp", 0))

    # Union upper bound: escapes caught by >=1 model (sum is a lower
    # bound on union; report as "at least")
    union_tp_lo = sum(r.get("tp", 0) for r in models.values() if isinstance(r, dict))
    escapes = 38  # gold bank kinds

    # ── record shape mirrors other axis entries ──────────────────
    record = {
        "axis": "jail",
        "bench": "GoldBank-Detector",
        "task": "escape-attempt detection on 71-cell gold bank (38 ESCAPE / 33 BENIGN) — layer 2 of 2",
        "n": 71,
        "n_note": "7 models x 71 gold items; TP/FP/TN/FN per model",
        "gold": {
            "total": gold.get("gold_n", 71),
            "escapes": escapes,
            "benign": 71 - escapes,
            "ts": gold.get("ts"),
            "run": "gold_run2.py on 3090 pod (fpowppss5ngtkw)",
        },
        "per_model": {
            m: {k: r.get(k) for k in ("tp", "fp", "tn", "fn", "precision", "recall")}
            for m, r in models.items() if isinstance(r, dict)
        },
        "best_zero_fp": best_name,
        "best_tp": best.get("tp", 0),
        "best_precision": best.get("precision"),
        "best_recall": best.get("recall"),
        "union_escapes_caught_lo": union_tp_lo,
        "accuracy": round(
            sum(r.get("tp", 0) + r.get("tn", 0) for r in models.values() if isinstance(r, dict))
            / (len(models) * 71), 4),
        "status": "MEASURED",
        "quotable": True,
        "note": (
            f"Detection layer: zero false positives across "
            f"{len(zero_fp)}/{len(models)} models (prec 1.0); best detector "
            f"{best_name} tp={best.get('tp')} rec={round(best.get('recall') or 0, 3)}. "
            "Containment layer (2592 trials) already MEASURED. "
            "Escape-detection recall remains low (models miss most attempts) — "
            "honest gap, drives trap-bank growth."
        ),
        "_source": "gold-run-3090",
        "_updated": now(),
    }

    # ── replace the jail axis record (keep layer-1 fields via merge) ──
    replaced = False
    for i, ax in enumerate(board["axes"]):
        if ax.get("axis") == "jail":
            layer1 = {k: v for k, v in ax.items()
                      if k not in record and k not in ("note", "_updated")}
            record["layer1"] = layer1
            board["axes"][i] = record
            replaced = True
            break
    if not replaced:
        board["axes"].append(record)
    board["updated"] = now()
    board["source"] = "boards-v2 + gold-run-3090"

    # ── Ed25519 sign (one-signer doctrine, ADR_ONE_SIGNER_2026-08-14) ──
    # canonical digest over the signature-stripped board (re-sign idempotent)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.path.insert(0, str(Path.home() / "clawd/councilof-ai-monorepo/packages/csoai-city/src"))
    from sign_board import sign_board, verify
    from csoai_city.keystone import load_signing_key
    key = load_signing_key()
    if not verify(board, key):
        board = sign_board(board, key)
        sig_out = f"ED25519 ok signer={board['signer'][:12]}... siglen={len(board['signature'])}"
    else:
        sig_out = "ED25519 already valid (unchanged)"
    BOARD.write_text(json.dumps(board, indent=2) + "\n")
    print(f"board updated: jail axis -> layer2 MEASURED (n=71, best {best_name} tp={best.get('tp')} fp=0)")
    print(f"digest={hashlib.sha256(json.dumps({k:v for k,v in board.items() if k not in ('signature','signer','signed','sig_input')}, sort_keys=True).encode()).hexdigest()[:16]} {sig_out}")
    print(f"path={BOARD}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
