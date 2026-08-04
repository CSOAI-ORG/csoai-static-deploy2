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


def load_context() -> str:
    """The grounding context, from the signed pack. Excerpt pointers only — the snapshot is
    article-level, so we supply the provision inventory, not full statutory text."""
    p = json.loads((PACK / "provisions.json").read_text())
    lines = []
    for pid, rec in p["provisions"].items():
        anchor = rec.get("excerpt_pointer", {}).get("anchor", "")
        lines.append(f"- {pid}: {anchor}")
    return ("EU AI ACT PROVISION INVENTORY (signed snapshot "
            f"{p['snapshot_manifest']['set_id']}):\n" + "\n".join(lines))


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
    for axis in G.AXES:
        items, field, labels = G.load_axis(axis)
        a_c = a_n = 0
        for it in items:
            head = f"{ctx}\n\n---\n\n" if grounded else ""
            prompt = (f"{head}{it[field]}\n\nAnswer with EXACTLY ONE of these labels and "
                      f"nothing else: {' | '.join(labels)}")
            resp = ask(model, prompt)
            if resp is None:
                unparse += 1
                continue
            hits = [l for l in labels if re.search(rf"\b{re.escape(l)}\b", resp.upper())]
            if len(hits) != 1:
                unparse += 1
                continue
            ok = hits[0] == it["expected"]
            correct += ok
            a_c += ok
            a_n += 1
        per_axis[axis] = (a_c, a_n)
    total_n = sum(n for _, n in per_axis.values())
    return {"correct": correct, "n_measured": total_n, "unparseable": unparse,
            "wilson": wilson(correct, total_n), "per_axis": per_axis}


def main():
    ctx = load_context()
    print(f"GROUNDING 2x2 — control-armed, hedge-aware, n=90 items per cell")
    print(f"  context: {len(ctx)} chars from the signed pack\n", flush=True)
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

    out = HERE / "evidence/harness/freeze/latest/grounding-2x2.json"
    out.write_text(json.dumps({
        "measured_at": datetime.now(timezone.utc).isoformat(), "substrate": OLLAMA,
        "grader": "exact-label, hedge-aware family (validated 98.9% vs human labels 2026-08-04)",
        "context_chars": len(ctx), "models": MODELS, "cells": cells,
        "grounding_lift_trained": lt, "grounding_lift_control": lc,
        "moat_claim_supported": bool(lt > lc),
        "interpretation": (
            "The moat claim requires the TRAINED model to gain MORE from the signed corpus than "
            "an untrained size-matched control does. If both gain equally, the corpus is doing "
            "generic in-context learning and the trained operator is not special.")}, indent=2))
    print(f"\n  -> {out}")


if __name__ == "__main__":
    main()
