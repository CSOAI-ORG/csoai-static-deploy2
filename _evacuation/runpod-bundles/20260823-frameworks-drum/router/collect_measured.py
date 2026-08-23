#!/usr/bin/env python3
"""Measured-outcomes register for the conformal router (move 30 data layer).

Collects REAL measured labels from estate data with known outcomes:
  1. signed_rounds.jsonl — human-vs-AI arena rounds (agreement = AI verdict matched the
     human reference; `simulated` absent/None = genuinely measured, the 23 'simulation'
     mode rounds are excluded).
  2. sov_experiments.jsonl — retrieval experiments with benchmark_correct/total.

HONEST REGISTER (binding): these are LABELS with known outcomes. A valid conformal score
must be a PRE-LABEL feature (e.g. the ensemble-disagreement score of move 26); the rounds
carry no such feature yet, so entries here are marked `score_proxy: true` and the router
must NOT be trusted on them (drum_route reports this). The register is the fuel source;
the score arrives with the ensemble.

Run:  python3 router/collect_measured.py [--dry-run]
"""
import json
import os
import sys

ROUTER_DIR = os.path.dirname(os.path.abspath(__file__))
SET_PATH = os.path.join(ROUTER_DIR, "calibration_set.jsonl")
ROUNDS = "/Users/nicholas/clawd/csoai-static-deploy2/signed_rounds.jsonl"
EXPERIMENTS = "/Users/nicholas/clawd/sovereign-charters/sov_experiments.jsonl"

ALREADY = set()


def _existing_ids():
    if not os.path.exists(SET_PATH):
        return set()
    out = set()
    for line in open(SET_PATH, encoding="utf-8"):
        line = line.strip()
        if line:
            out.add(json.loads(line).get("finding"))
    return out


def collect_rounds(dry=False):
    n = 0
    if not os.path.exists(ROUNDS):
        return n
    for line in open(ROUNDS, encoding="utf-8"):
        p = json.loads(line).get("payload", {})
        if p.get("mode") != "human-vs-ai":
            continue
        if p.get("simulated") is True:
            continue  # honest: simulated rounds are not measured labels
        if p.get("agreement") is None:
            continue  # unlabeled — skip
        finding = f"arena-{json.loads(line).get('cid', '')[:16]}"
        if finding in ALREADY:
            continue
        ALREADY.add(finding)
        entry = {
            "finding": finding,
            "score": 0.1 if p["agreement"] else 0.9,  # PROXY — see docstring
            "label_correct": bool(p["agreement"]),
            "source": "signed_rounds.jsonl",
            "simulated": False,
            "score_proxy": True,
        }
        if not dry:
            with open(SET_PATH, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        n += 1
    return n


def collect_experiments(dry=False):
    n = 0
    if not os.path.exists(EXPERIMENTS):
        return n
    for line in open(EXPERIMENTS, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        total = e.get("benchmark_total")
        if not total:
            continue
        correct = e.get("benchmark_correct", 0)
        finding = e.get("experiment_id", f"exp-{n}")
        if finding in ALREADY:
            continue
        ALREADY.add(finding)
        entry = {
            "finding": finding,
            "score": 1 - (correct / total),       # error rate — PROXY (post-hoc outcome)
            "label_correct": (correct / total) >= 0.5,  # beat chance = correct outcome
            "source": "sov_experiments.jsonl",
            "simulated": False,
            "score_proxy": True,
        }
        if not dry:
            with open(SET_PATH, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        n += 1
    return n


def summary():
    rows = [json.loads(l) for l in open(SET_PATH, encoding="utf-8") if l.strip()] if os.path.exists(SET_PATH) else []
    measured = [r for r in rows if not r.get("simulated")]
    n_corr = sum(1 for r in measured if r.get("label_correct"))
    print(f"calibration set: {len(rows)} entries | measured: {len(measured)} (correct {n_corr}) | simulated: {len(rows) - len(measured)}")
    print("HONEST: all measured scores are PROXY (score_proxy=true) — router stays NOT trusted until the ensemble-disagreement score lands (move 26).")


if __name__ == "__main__":
    ALREADY.update(_existing_ids())
    dry = "--dry-run" in sys.argv
    r = collect_rounds(dry)
    e = collect_experiments(dry)
    print(f"{'dry-run:' if dry else 'collected:'} {r} arena labels + {e} experiment labels")
    summary()
