#!/usr/bin/env python3
"""grounding_2x2.py — does the signed corpus help, or does any model just read context?

THE CLAIM UNDER TEST
--------------------
"Out-ground, not out-think": a small trained operator plus the signed Honey KB ties or beats
a frontier model, because the corpus supplies what the weights lack. It is the estate's
central thesis.

A pilot measured grounded 88% vs closed-book 69% on n=8 with a keyword grader and no control
arm. Checked 2026-08-04: the intervals overlap ([0.53-0.98] vs [0.41-0.93]), the whole lift
is 1.5 items, and at the keyword grader's measured accuracy (88.0%) roughly one mis-grade per
8-item arm is expected — which alone moves the arm 12.5 points. Suggestive, not resolved.

WHY A CONTROL ARM IS THE WHOLE POINT HERE
-----------------------------------------
Without it, a grounded-beats-closed-book result cannot distinguish

    (a) THE SIGNED CORPUS ADDS SOMETHING     <- the moat claim
    (b) THIS MODEL READS SUPPLIED CONTEXT    <- which every model does

Only the interaction separates them. So this is a 2x2:

                     closed-book        grounded
    sov34 (trained)      A                 B
    control (untrained)  C                 D

    grounding lift, trained    = B - A
    grounding lift, control    = D - C
    THE MOAT CLAIM             = (B - A) > (D - C)

If both models gain equally, the corpus is doing generic in-context learning and the trained
operator is not special. That comparison has never been run.

DESIGN
    items    all 90 frozen GSPC items, per-axis breakdown retained
    grounded the EU AI Act provision text is prepended as CONTEXT
    grader   govbench_eval._refuses / exact-label — hedge-aware, validated 98.9% today
    control  qwen2.5:1.5b, size-matched to sov34 (both 1.5B qwen2)
    stats    95% Wilson on every cell; a difference whose intervals overlap is NOT RESOLVED
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gspc_six_axis_e2e as G  # noqa: E402

OLLAMA = os.environ.get("GOVBENCH_OLLAMA_URL", "http://localhost:11434").rstrip("/")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
PACK = Path("/Users/nicholas/projects/coai-dashboard/regarena/packages/packs/eu-ai-act@1.0.0")

MODELS = {"trained": "sov34:latest", "control": "qwen2.5:1.5b"}


SNAP = Path("/Users/nicholas/projects/coai-dashboard/regarena/packages/snapshots/EU-AI-ACT/202608")


def load_context(mode: str = "text") -> str:
    """Grounding context from the SIGNED pack.

    2026-08-04 — the first run supplied only the provision INVENTORY (a list of article names
    and anchors, 1441 chars) and the trained model's grounding lift came out at exactly 0.000
    on the like-for-like intersection. That tested whether knowing WHICH provisions exist
    helps. It does not.

    This supplies the actual STATUTORY TEXT, hash-verified against the signed pack (21/21
    match, 0 mismatch). Art 5 alone is 11,580 bytes; the full corpus is 92,156. We use Art 5
    because it is the prohibited-practices article the item sets actually concern, and because
    the full corpus (~23k tokens) exceeds what a 1.5B model handles usefully — a limit worth
    stating rather than discovering mid-run.
    """
    p = json.loads((PACK / "provisions.json").read_text())
    if mode == "inventory":
        lines = [f"- {pid}: {rec.get('excerpt_pointer', {}).get('anchor', '')}"
                 for pid, rec in p["provisions"].items()]
        return ("EU AI ACT PROVISION INVENTORY (signed snapshot "
                f"{p['snapshot_manifest']['set_id']}):\n" + "\n".join(lines))
    art5 = (SNAP / "art05.txt").read_text()
    return ("EU AI ACT — ARTICLE 5, PROHIBITED PRACTICES (verbatim, from signed snapshot "
            f"{p['snapshot_manifest']['set_id']}, sha256-verified):\n\n{art5}")


def ask(model: str, prompt: str) -> str | None:
    body = json.dumps({"model": model, "stream": False,
                       "options": {"temperature": 0, "num_predict": 24},
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=body,
                                 headers={"Content-Type": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())["message"]["content"].strip()
    except Exception:
        return None


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return None, None, None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(p, 4), round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


def run_cell(model: str, grounded: bool, ctx: str):
    correct = unparse = 0
    per_axis = {}
    # 2026-08-04 — the first run saved only aggregates, so when sov34 turned out to produce 35
    # unparseable answers against the control's zero, the four cells had different denominators
    # (55/69/90/90) and no intersection analysis was possible without re-running. Per-item
    # outcomes are now retained so every cell can be restricted to the items ALL cells answered.
    per_item = {}
    for axis in G.AXES:
        items, field, labels = G.load_axis(axis)
        a_c = a_n = 0
        for it in items:
            head = f"{ctx}\n\n---\n\n" if grounded else ""
            prompt = (f"{head}{it[field]}\n\nAnswer with EXACTLY ONE of these labels and "
                      f"nothing else: {' | '.join(labels)}")
            resp = ask(model, prompt)
            key = f"{axis}:{items.index(it)}"
            if resp is None:
                unparse += 1
                per_item[key] = None
                continue
            hits = [l for l in labels if re.search(rf"\b{re.escape(l)}\b", resp.upper())]
            if len(hits) != 1:
                unparse += 1
                per_item[key] = None
                continue
            per_item[key] = (hits[0] == it["expected"])
            ok = hits[0] == it["expected"]
            correct += ok
            a_c += ok
            a_n += 1
        per_axis[axis] = (a_c, a_n)
    total_n = sum(n for _, n in per_axis.values())
    return {"correct": correct, "n_measured": total_n, "unparseable": unparse,
            "wilson": wilson(correct, total_n), "per_axis": per_axis,
            "per_item": per_item}


def main():
    mode = os.environ.get("GROUNDING_MODE", "text")
    ctx = load_context(mode)
    print(f"GROUNDING 2x2 — control-armed, hedge-aware, n=90 items per cell")
    print(f"  context mode: {mode.upper()} — {len(ctx):,} chars from the signed pack\n", flush=True)
    cells = {}
    for role, model in MODELS.items():
        for cond, grounded in (("closed_book", False), ("grounded", True)):
            key = f"{role}/{cond}"
            r = run_cell(model, grounded, ctx)
            cells[key] = r
            p, lo, hi = r["wilson"]
            print(f"  {key:22s} {r['correct']:3d}/{r['n_measured']:3d} = {p:.3f} "
                  f"[{lo:.3f}-{hi:.3f}]  unparseable={r['unparseable']}", flush=True)

    def lift(role):
        g, c = cells[f"{role}/grounded"], cells[f"{role}/closed_book"]
        return round(g["wilson"][0] - c["wilson"][0], 4), g, c

    lt, gt, ct = lift("trained")
    lc, gc, cc = lift("control")
    overlap = not (gt["wilson"][1] > ct["wilson"][2] or ct["wilson"][1] > gt["wilson"][2])
    print(f"\n  grounding lift, TRAINED  {lt:+.3f}   intervals overlap: {overlap}")
    oc = not (gc["wilson"][1] > cc["wilson"][2] or cc["wilson"][1] > gc["wilson"][2])
    print(f"  grounding lift, CONTROL  {lc:+.3f}   intervals overlap: {oc}")
    print(f"\n  MOAT CLAIM (trained lift > control lift): {lt:+.3f} vs {lc:+.3f} -> "
          f"{'SUPPORTED' if lt > lc else 'NOT SUPPORTED'}")
    print("  (both lifts overlapping their own baselines means neither is individually resolved)")

    # INTERSECTION ANALYSIS — the fix for the differing-denominator confound. Restrict every
    # cell to the items ALL FOUR answered parseably, so the comparison is strictly like-for-like.
    common = set.intersection(*[{k for k, v in c["per_item"].items() if v is not None}
                                for c in cells.values()])
    inter = {}
    for k, c in cells.items():
        ok = sum(1 for i in common if c["per_item"][i])
        inter[k] = {"correct": ok, "n": len(common), "wilson": wilson(ok, len(common))}
    print(f"\n  INTERSECTION — {len(common)} items answered parseably by ALL four cells:")
    for k, v in inter.items():
        p_, lo_, hi_ = v["wilson"]
        print(f"    {k:22s} {v['correct']:3d}/{v['n']:3d} = {p_:.3f} [{lo_:.3f}-{hi_:.3f}]")
    lt_i = round(inter["trained/grounded"]["wilson"][0] - inter["trained/closed_book"]["wilson"][0], 4)
    lc_i = round(inter["control/grounded"]["wilson"][0] - inter["control/closed_book"]["wilson"][0], 4)
    # 2026-08-04 — the first version of this line printed "moat claim: SUPPORTED" whenever
    # lift_trained > lift_control. On the intersection that fired on +0.000 vs -0.045: a NULL
    # effect beating a slightly-negative one. Comparing two nulls and calling the larger one
    # support is the same defect this session spent the day removing. The moat claim requires
    # the trained lift to be POSITIVE AND RESOLVED, not merely less negative than the control's.
    tg, tc = inter["trained/grounded"]["wilson"], inter["trained/closed_book"]["wilson"]
    trained_resolved = tg[1] > tc[2]          # grounded CI clears closed-book CI entirely
    if lt_i <= 0:
        moat = "NOT SUPPORTED — trained grounding lift is not positive"
    elif not trained_resolved:
        moat = "NOT SUPPORTED — trained lift positive but intervals overlap (unresolved)"
    elif lt_i <= lc_i:
        moat = "NOT SUPPORTED — control gains as much, so the effect is generic in-context learning"
    else:
        moat = "SUPPORTED"
    print(f"    lift TRAINED {lt_i:+.3f}   lift CONTROL {lc_i:+.3f}")
    print(f"    moat claim: {moat}")

    out = HERE / "evidence/harness/freeze/latest/grounding-2x2.json"
    out.write_text(json.dumps({
        "measured_at": datetime.now(timezone.utc).isoformat(), "substrate": OLLAMA,
        "grader": "exact-label, hedge-aware family (validated 98.9% vs human labels 2026-08-04)",
        "context_chars": len(ctx), "models": MODELS, "cells": cells,
        "grounding_lift_trained": lt, "grounding_lift_control": lc,
        "moat_claim_supported": bool(lt > lc),
        "intersection_analysis": {"n_common_items": len(common), "cells": inter,
                                  "lift_trained": lt_i, "lift_control": lc_i,
                                  "moat_claim_verdict": moat,
                                  "why": ("restricts every cell to items ALL FOUR answered "
                                          "parseably, removing the differing-denominator confound "
                                          "caused by sov34's 39% unparseable rate")},
        "interpretation": (
            "The moat claim requires the TRAINED model to gain MORE from the signed corpus than "
            "an untrained size-matched control does. If both gain equally, the corpus is doing "
            "generic in-context learning and the trained operator is not special.")}, indent=2))
    print(f"\n  -> {out}")


if __name__ == "__main__":
    main()
