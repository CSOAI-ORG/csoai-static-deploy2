#!/usr/bin/env python3
"""
common.py — single source of truth for helpers that were duplicated across the engine.

Before: profile_for() lived in batch.py + train_all_hives.py + flywheel_forever.py (3 copies) and the
episode feature-vector lived in flywheel_train.py + train_all_hives.py (2 copies). They were consistent
but one careless edit would have silently diverged the data each tool produced. Now they live here.
"""
import sim

def profile_for(district):
    """Per-hive economic profile — distinct scarcity season + seed offset so each hive's data is non-clone."""
    idx = list(sim.DISTRICTS.keys()).index(district)
    return {"scarcity": range(3 + idx % 9, 3 + idx % 9 + 4 + idx % 5), "off": (idx + 1) * 1000}

FEATURE_NAMES = ["hunger", "energy", "social", "wallet", "scarcity",
                 "lawlessness", "commons", "broke&hungry", "caring"]

def features(r):
    """Episode -> feature vector for the threat/care detectors (matches FEATURE_NAMES order)."""
    n = r["perception"]["needs"]; w = r["perception"]["wallet"]; t = r["town"]
    caring = 1.0 if r["agent"]["care_style"] in ("gentle", "supporter") else 0.0
    return [n["hunger"]/100, n["energy"]/100, n["social"]/100, min(w, 12)/12,
            1.0 if r["scarcity"] else 0.0, t["lawlessness"], t["commons"],
            1.0 if (n["hunger"] < 30 and w < 3) else 0.0, caring]
