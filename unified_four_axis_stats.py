#!/usr/bin/env python3
"""Pure statistics and claim logic for the unified four-axis benchmark.

This module intentionally contains no network calls, benchmark evaluators, or
partition-splitting logic. It operates on plain Python dicts so that tests can
exercise inference deterministically and cheaply.
"""
from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence

AxisID = str
CaseID = str
Partition = str


def counts_from_outcomes(outcomes: Sequence[str]) -> Dict[str, int]:
    c = {"total": 0, "pass": 0, "fail": 0, "indeterminate": 0}
    for x in outcomes:
        c["total"] += 1
        if x == "pass":
            c["pass"] += 1
        elif x == "fail":
            c["fail"] += 1
        elif x == "indeterminate":
            c["indeterminate"] += 1
        else:
            raise ValueError(f"unknown outcome: {x}")
    return c


def conditional_pass_rate(counts: Dict[str, int]) -> Optional[float]:
    determinate = counts["pass"] + counts["fail"]
    if determinate <= 0:
        return None
    return counts["pass"] / determinate


def coverage(counts: Dict[str, int]) -> float:
    if counts["total"] <= 0:
        return 0.0
    return (counts["pass"] + counts["fail"]) / counts["total"]


def indeterminate_rate(counts: Dict[str, int]) -> float:
    if counts["total"] <= 0:
        return 0.0
    return counts["indeterminate"] / counts["total"]


def _stable_seed_int(seed_prefix: str, case_ids: Sequence[CaseID]) -> int:
    joined = f"{seed_prefix}||{','.join(case_ids)}"
    h = 0x811c9dc5
    for ch in joined.encode("utf-8"):
        h ^= ch
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def _rng(seed_int: int):
    state = seed_int & 0xFFFFFFFF or 1

    def next_int() -> int:
        nonlocal state
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= (state >> 17) & 0xFFFFFFFF
        state ^= (state << 5) & 0xFFFFFFFF
        return state

    return next_int


def paired_records(baseline: Dict[CaseID, str], challenger: Dict[CaseID, str], case_ids: Sequence[CaseID]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for cid in case_ids:
        b = baseline.get(cid)
        c = challenger.get(cid)
        out.append({
            "case_id": cid,
            "baseline": b,
            "challenger": c,
        })
    return out


def paired_counts(pairs: Sequence[Dict[str, object]]) -> Dict[str, int]:
    out = {"paired_determinate": 0, "baseline_indeterminate": 0, "challenger_indeterminate": 0, "both_indeterminate": 0, "missing_execution": 0}
    for p in pairs:
        b, c = p["baseline"], p["challenger"]
        if b is None or c is None:
            out["missing_execution"] += 1
            continue
        if b == "indeterminate" and c == "indeterminate":
            out["both_indeterminate"] += 1
        elif b == "indeterminate":
            out["baseline_indeterminate"] += 1
        elif c == "indeterminate":
            out["challenger_indeterminate"] += 1
        else:
            out["paired_determinate"] += 1
    return out


def paired_pass_delta(baseline: Dict[CaseID, str], challenger: Dict[CaseID, str], case_ids: Sequence[CaseID]) -> Optional[float]:
    determinate = [(baseline[c], challenger[c]) for c in case_ids if baseline.get(c) not in (None, "indeterminate") and challenger.get(c) not in (None, "indeterminate")]
    if not determinate:
        return None
    base_mean = sum(1 if b == "pass" else 0 for b, _ in determinate) / len(determinate)
    chal_mean = sum(1 if c == "pass" else 0 for _, c in determinate) / len(determinate)
    return chal_mean - base_mean


def paired_bootstrap_ci(baseline: Dict[CaseID, str], challenger: Dict[CaseID, str], case_ids: Sequence[CaseID], level: float = 0.95, replicates: int = 10000, seed_prefix: str = "run|axis") -> Dict[str, object]:
    determinate = [cid for cid in case_ids if baseline.get(cid) not in (None, "indeterminate") and challenger.get(cid) not in (None, "indeterminate")]
    if not determinate:
        return {"paired_determinate_n": 0, "estimate": None, "confidence_interval": {"level": level, "lower": None, "upper": None, "method": "paired_case_bootstrap"}}
    deltas = []
    for cid in determinate:
        deltas.append((1 if challenger[cid] == "pass" else 0) - (1 if baseline[cid] == "pass" else 0))
    rng = _rng(_stable_seed_int(seed_prefix, determinate))
    samples: List[float] = []
    n = len(deltas)
    for _ in range(replicates):
        s = 0.0
        for _ in range(n):
            s += deltas[rng() % n]
        samples.append(s / n)
    samples.sort()
    lo_idx = max(0, int(math.floor((1 - level) / 2 * replicates)) - 1)
    hi_idx = min(replicates - 1, int(math.floor((1 + level) / 2 * replicates)) - 1)
    return {
        "paired_determinate_n": n,
        "estimate": sum(deltas) / n,
        "confidence_interval": {
            "level": level,
            "lower": samples[lo_idx],
            "upper": samples[hi_idx],
            "method": "paired_case_bootstrap",
        },
    }


def decide_claim(axis_thresholds: Dict[str, float], paired_n: int, coverage_challenger: Optional[float], coverage_baseline: Optional[float], estimate: Optional[float], lower: Optional[float], upper: Optional[float]) -> Dict[str, object]:
    min_n = int(axis_thresholds.get("minimum_paired_determinate_cases", 20))
    min_cov = float(axis_thresholds.get("minimum_coverage", 0.9))
    min_delta = float(axis_thresholds.get("minimum_paired_delta", 0.0))
    require_ci = bool(axis_thresholds.get("require_ci_lower_bound_above_zero", True))

    reasons = []
    if paired_n < min_n:
        reasons.append("insufficient_paired_determinate_cases")
    if coverage_challenger is None or coverage_baseline is None:
        reasons.append("missing_coverage")
    else:
        if coverage_challenger < min_cov:
            reasons.append("challenger_coverage_below_threshold")
        if coverage_baseline < min_cov:
            reasons.append("baseline_coverage_below_threshold")
    if estimate is None or lower is None or upper is None:
        reasons.append("missing_interval")
    if reasons:
        return {"outcome": "no_claim", "eligible": False, "reasons": reasons}

    if estimate < min_delta:
        return {"outcome": "challenger_worse", "eligible": True, "reasons": ["estimate_below_minimum_delta"]}
    if estimate == 0.0:
        return {"outcome": "no_material_difference", "eligible": True, "reasons": ["zero_effect"]}
    if require_ci and lower <= 0.0:
        return {"outcome": "no_material_difference", "eligible": True, "reasons": ["ci_crosses_or_touches_zero"]}

    return {"outcome": "challenger_better", "eligible": True, "reasons": []}
