#!/usr/bin/env python3
"""Calibration set builder for the conformal 90/10 router (moves 26-30).

Builds the calibration set file the router freezes qhat from. Honest register:
entries carry `label` = known correct outcome for a finding, and `source` of the label.
Until real measured labels exist, the file is seeded with SIMULATED entries clearly
marked simulated=true — the router must not be trusted on simulated data (moves 26-27
require measured labels + realized-coverage check before trust).

Stdlib-only. Run: python3 router/calibration_set.py --seed   (creates/seeds the set)
"""
import json
import os
import sys

SET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibration_set.jsonl")


def entry(finding_id, score, label_correct, source="simulated", simulated=True):
    return {"finding": finding_id, "score": round(float(score), 6),
            "label_correct": bool(label_correct), "source": source, "simulated": simulated}


def load():
    out = []
    if os.path.exists(SET_PATH):
        for line in open(SET_PATH, encoding="utf-8"):
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def seed():
    import random
    random.seed(7)
    os.makedirs(os.path.dirname(SET_PATH), exist_ok=True)
    rows = []
    for i in range(200):
        s = abs(random.gauss(0, 1))
        # simulated label: low score -> correct with high prob (uncertainty-calibrated toy)
        correct = random.random() > (0.01 + 0.1 * (s / 3.0))
        rows.append(entry(f"sim-{i:03d}", s, correct, source="simulated-pipeline-test", simulated=True))
    with open(SET_PATH, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    n_sim = sum(1 for r in rows if r["simulated"])
    print(f"seeded {len(rows)} entries ({n_sim} simulated) → {SET_PATH}")
    print("HONEST: simulated labels only — do NOT trust the router until measured labels replace them (moves 26-27).")
    return rows


def stats():
    rows = load()
    if not rows:
        print("calibration set empty — run --seed first")
        return
    n = len(rows)
    n_sim = sum(1 for r in rows if r["simulated"])
    n_corr = sum(1 for r in rows if r["label_correct"])
    print(f"entries: {n} | simulated: {n_sim} | measured: {n - n_sim} | label_correct: {n_corr}/{n}")


if __name__ == "__main__":
    if "--seed" in sys.argv:
        seed()
    else:
        stats()
