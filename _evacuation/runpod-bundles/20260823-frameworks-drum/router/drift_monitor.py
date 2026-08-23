#!/usr/bin/env python3
"""Drift monitor for the conformal router (move 28) — scheduled recalibration trigger.

Compares the live score distribution against the calibration distribution. Stdlib-only:
uses a percentile-shift statistic (fraction of live scores above the calibration qhat).
Recalibration is a controlled, signed, logged event — never continuous (doctrine).

Run: python3 router/drift_monitor.py --check
"""
import json
import os
import sys

SET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibration_set.jsonl")


def check(cal_scores, live_scores, alpha=0.05, drift_ratio=1.5):
    """Drift alarm if the fraction of live scores above qhat exceeds drift_ratio * alpha."""
    if not cal_scores:
        return {"alarm": True, "reason": "empty calibration set"}
    qhat, _ = __import__("conformal_router").calibrate(cal_scores, alpha)
    frac_above = sum(1 for s in live_scores if s > qhat) / len(live_scores) if live_scores else 0.0
    alarm = frac_above > drift_ratio * alpha
    return {"qhat": round(qhat, 4), "live_frac_above": round(frac_above, 4),
            "threshold": round(drift_ratio * alpha, 4), "alarm": alarm}


def load_scores(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    return [r["score"] for r in rows]


if __name__ == "__main__":
    cal = load_scores(SET_PATH) if os.path.exists(SET_PATH) else []
    # live feed placeholder: a JSON file of live scores (router/conformal_router.py CLI output)
    live_path = sys.argv[1] if len(sys.argv) > 1 else ""
    live = load_scores(live_path) if live_path and os.path.exists(live_path) else []
    res = check(cal, live)
    print(json.dumps(res, indent=1))
    sys.exit(1 if res.get("alarm") else 0)
