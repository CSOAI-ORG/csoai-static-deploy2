#!/usr/bin/env python3
"""overrefusal_economics.py — GF-05: the business cost of a safety gate refusing too much.

A gate that REFUSES too much has a measurable cost, separate from safety benefit:
every false refusal is a customer request lost and an escalation incurred. This
computes that cost deterministically from the estate's own measured overblock
rates — the numbers are real (care_gate_eval overblock_rate; this session's
refusal-axis runs: v1 0.500 → v2 0.357 → composed 0.214).

The stark trade it makes visible: the composed sov-refusal-combo-lora cut
overblock from 0.500 to 0.214 WITHOUT losing safety (refusal still 0.871,
comply-leak 0.000). That is a ~57% reduction in false-refusal incidents — real
money at volume, and this tool prices it.

Model (deliberately simple, all inputs explicit — Law 1, no hidden assumptions):
  false_refusals  = request_volume * overblock_rate
  lost_revenue    = false_refusals * revenue_per_request * (1 - rescue_rate)
  escalation_cost = false_refusals * escalation_fraction * escalation_cost_each
  total_cost      = lost_revenue + escalation_cost

Only overblock_rate comes from measurement; volume/price/rates are configured
by the operator so the tool is an honest calculator, not a forecast.

    python3 overrefusal_economics.py --overblock 0.214 --volume 100000 \
        --revenue-per-request 0.5 --rescue-rate 0.3 \
        --escalation-fraction 0.25 --escalation-cost 4.0   # @100k requests/mo
    python3 overrefusal_economics.py --selftest
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

VERSION = "0.1.0"

# Measured overblock rates from this lineage (care_gate_eval + refusal-axis runs,
# 2026-08-08/09). Used as reference presets; --overblock overrides.
KNOWN_OVERBLOCK = {
    "stock-base": 0.0,          # qwen2.5:0.5b refused nothing benign (under-refuses, different cost)
    "lora-v1": 0.500,           # sov-refusal-lora-v20260808 (all-refusal training)
    "lora-v2": 0.357,           # sov-refusal-lora-v2-20260808 (mixed dataset)
    "combo-lora": 0.214,        # sov-refusal-combo-lora (charter + weights, best trade)
    "care-gate": 0.0,           # deterministic care gate refuses zero benign (by design)
}


def price(overblock: float, volume: int, revenue_per_request: float,
          rescue_rate: float, escalation_fraction: float,
          escalation_cost: float) -> dict:
    if not (0 <= overblock <= 1):
        raise ValueError("overblock must be 0..1")
    if not (0 <= rescue_rate <= 1):
        raise ValueError("rescue_rate must be 0..1")
    false_refusals = volume * overblock
    lost_revenue = false_refusals * revenue_per_request * (1 - rescue_rate)
    escalation_cost_total = false_refusals * escalation_fraction * escalation_cost
    total = lost_revenue + escalation_cost_total
    return {
        "detector": f"overrefusal_economics v{VERSION}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {"overblock": overblock, "volume": volume,
                   "revenue_per_request": revenue_per_request, "rescue_rate": rescue_rate,
                   "escalation_fraction": escalation_fraction,
                   "escalation_cost_each": escalation_cost},
        "false_refusals_per_unit_volume": round(false_refusals / max(volume, 1), 4),
        "false_refusals": round(false_refusals),
        "lost_revenue": round(lost_revenue, 2),
        "escalation_cost": round(escalation_cost_total, 2),
        "total_cost": round(total, 2),
        "cost_per_1000_requests": round(total / max(volume, 1) * 1000, 2),
        "frame": ("False refusals are a measurable business cost, distinct from safety "
                  "benefit. Overblock source is measured; volume/price are operator inputs."),
    }


def compare(volume: int = 100_000, rpr: float = 0.5, rescue: float = 0.3,
            esc_frac: float = 0.25, esc_cost: float = 4.0) -> dict:
    rows = []
    for name, ob in KNOWN_OVERBLOCK.items():
        r = price(ob, volume, rpr, rescue, esc_frac, esc_cost)
        rows.append({"model": name, "overblock": ob, "false_refusals": r["false_refusals"],
                     "total_cost": r["total_cost"]})
    rows.sort(key=lambda x: x["total_cost"])
    base = rows[0]["total_cost"]
    for r in rows:
        r["vs_best_pct"] = round((r["total_cost"] / base - 1) * 100, 1) if base else 0
    return {"detector": f"overrefusal_economics v{VERSION}",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "volume": volume, "row_count": len(rows), "rows": rows,
            "note": ("Measured overblock per model at @%d requests/mo, %.2f/req, "
                     "%.0f%% rescue — the composed model costs %.0f%% of the "
                     "all-refusal LoRA." % (volume, rpr, rescue * 100,
                        (([r for r in rows if r["model"] == "combo-lora"][0]["total_cost"]
                          / [r for r in rows if r["model"] == "lora-v1"][0]["total_cost"]) * 100) if any(
                            r["model"] == "lora-v1" for r in rows) else 0))}


def selftest() -> int:
    fails = []
    # math sanity
    r = price(0.5, 1000, 1.0, 0.0, 0.0, 0.0)
    if r["false_refusals"] != 500 or r["total_cost"] != 500.0:
        fails.append(f"math: expected 500/500 got {r['false_refusals']}/{r['total_cost']}")
    # bounds
    try:
        price(1.5, 10, 1, 0, 0, 0); fails.append("overblock>1 not rejected")
    except ValueError:
        pass
    try:
        price(0.5, 10, 1, 2.0, 0, 0); fails.append("rescue>1 not rejected")
    except ValueError:
        pass
    # reversal: reducing overblock must reduce cost
    a = price(0.500, 100_000, 0.5, 0.3, 0.25, 4.0)
    b = price(0.214, 100_000, 0.5, 0.3, 0.25, 4.0)
    if not b["total_cost"] < a["total_cost"]:
        fails.append("lower overblock did not lower cost")
    # known presets present
    c = compare()
    if len(c["rows"]) != len(KNOWN_OVERBLOCK):
        fails.append("compare() row count mismatch")
    for f in fails:
        print(f"  FAIL {f}")
    print(f"  selftest {'PASS' if not fails else f'FAIL ({len(fails)})'}")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--overblock", type=float, default=0.214)
    ap.add_argument("--volume", type=int, default=100_000)
    ap.add_argument("--revenue-per-request", type=float, default=0.5)
    ap.add_argument("--rescue-rate", type=float, default=0.3)
    ap.add_argument("--escalation-fraction", type=float, default=0.25)
    ap.add_argument("--escalation-cost", type=float, default=4.0)
    ap.add_argument("--compare", action="store_true", help="compare measured presets")
    ap.add_argument("--out", help="write report to path")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    report = compare(args.volume, args.revenue_per_request, args.rescue_rate,
                     args.escalation_fraction, args.escalation_cost) if args.compare else \
             price(args.overblock, args.volume, args.revenue_per_request,
                   args.rescue_rate, args.escalation_fraction, args.escalation_cost)
    if args.out:
        Path_out(args.out).write_text(json.dumps(report, indent=2))
        print(f"-> {args.out}")
    else:
        print(json.dumps(report, indent=2))
    return 0


def Path_out(p: str):
    from pathlib import Path
    return Path(p)


if __name__ == "__main__":
    raise SystemExit(main())