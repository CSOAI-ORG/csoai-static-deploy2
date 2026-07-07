#!/usr/bin/env python3
"""
Calibration harness for the GDELT->scenario mapping (realdata_scenario.MappingParams).

The mapping coefficients are PRIORS, not fitted values. Real calibration needs ground truth
(see NOTE at bottom). Until we have that, this harness does the honest interim thing: a
one-at-a-time SENSITIVITY ANALYSIS — vary each coefficient across a plausible range, run the
real OOWM, and report which coefficients move governed outcomes most. That tells you where
calibration effort actually matters (high-sensitivity params) vs where the prior is harmless.
"""
from __future__ import annotations
import sys, dataclasses
sys.path.insert(0, ".")
from benchmark.realdata_scenario import gdelt_to_scenario, MappingParams, DEFAULT_PARAMS
import benchmark.metrics as M
from benchmark import world
import benchmark.scenarios as S

# a fixed representative real-signal profile (mid-crisis) so only the PARAM varies
PROFILE = {"articles": [{}] * 45, "tone": [{"value": -2.0}] * 10}


def _run(params: MappingParams) -> dict:
    sc = gdelt_to_scenario(PROFILE, params)
    S.SCENARIOS["_cal"] = (lambda c=sc: c)
    try:
        r = world.run(policy=None, scenario="_cal", district="aqua")
        m = M.evaluate(r)
    finally:
        S.SCENARIOS.pop("_cal", None)
    return {"safety": m["safety"], "crimes": r.get("violations", 0),
            "peak_lawl": round(r.get("peak_lawlessness", 0), 3), "equity": m["equity"],
            "block_rate": sc["block_rate"], "base_lawl": sc["BASELINE_LAWLESSNESS"]}


def sensitivity(field: str, values: list[float]) -> list[tuple]:
    out = []
    for v in values:
        p = dataclasses.replace(DEFAULT_PARAMS, **{field: v})
        res = _run(p)
        out.append((v, res))
    return out


if __name__ == "__main__":
    base = _run(DEFAULT_PARAMS)
    print("baseline (default priors):", base)
    print()
    sweeps = {
        "enf_floor":        [0.40, 0.55, 0.70],
        "enf_ceiling":      [0.85, 0.95, 0.99],
        "enf_volume_scale": [15.0, 30.0, 60.0],
        "lawl_intercept":   [0.15, 0.25, 0.35],
        "lawl_tone_coeff":  [0.01, 0.03, 0.06],
        "contagion_tone_coeff": [0.02, 0.04, 0.08],
    }
    print(f"{'coefficient':<22} {'value':<7} {'safety':<8} {'crimes':<7} {'equity':<7}")
    print("-" * 55)
    ranges = {}
    for field, vals in sweeps.items():
        rows = sensitivity(field, vals)
        safeties = [r[1]["safety"] for r in rows]
        ranges[field] = max(safeties) - min(safeties)
        for v, res in rows:
            print(f"{field:<22} {v:<7} {res['safety']:<8} {res['crimes']:<7} {res['equity']:<7}")
        print()
    print("=== SENSITIVITY RANKING (Δsafety across the swept range; higher = calibrate first) ===")
    for field, rng in sorted(ranges.items(), key=lambda x: -x[1]):
        print(f"  {field:<22} Δsafety = {rng:.3f}")

# NOTE — what REAL calibration would require (not doable from priors alone):
#   ground truth pairs of (real regulatory-period signal) -> (observed compliance/harm outcome),
#   e.g. GDELT volume/tone for a known period matched against a real enforcement or incident metric
#   (regulator action counts, reported AI-incident rates). Then FIT the coefficients to minimise
#   prediction error, rather than hand-set them. Until that dataset exists, priors + this
#   sensitivity analysis are the honest state.
