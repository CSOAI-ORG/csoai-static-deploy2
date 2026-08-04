#!/usr/bin/env python3
"""item_gate.py — the DISCRIMINATING_ITEMS_SPEC §4 R3 acceptance gate, as a runnable check.

A spec that only describes a gate does not gate anything. This is the gate.

    difficulty        0.20 <= d <= 0.80
    discrimination    r >= 0.20 against the REST-score
    prediction gap    |d - predicted_difficulty| <= 0.30
    usable_n          >= 30 per axis before any interval on that axis is quoted

WHAT THIS GATE DOES **NOT** DO, AND WHY
--------------------------------------
It does not reject an item for negative discrimination.

That was the original rule and it was wrong. On 2026-08-04 all 18 GSPC items with r < -0.2 were
adjudicated by a judge that never saw the answer key: 13 agreed with the key, and all 5
disagreements were resolved in the KEY's favour on domain grounds — Shor does not apply to hash
functions, an analogue round-trip does destroy digital provenance, accepting out-of-shape
traversal is the schema violation. **Zero of eighteen keys were wrong.**

The negative loading was a property of the MODELS, not the items: capability correlated with
holding a specific false belief. A naive `r < -0.2 -> reject` rule would have deleted the only
items in the battery that detect capability-correlated error — the sharpest instrument there,
thrown away for looking broken.

So negative discrimination routes to ADJUDICATE. Rejection requires adjudication plus domain
review actually finding the key wrong. This is the single most important line in the file.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

D_MIN, D_MAX = 0.20, 0.80
R_MIN = 0.20
GAP_MAX = 0.30
USABLE_TARGET = 30


def wilson_halfwidth(n: int, p: float = 0.5, z: float = 1.96) -> float:
    """Half-width at the widest point. What an axis can actually resolve at that n."""
    if n <= 0:
        return 1.0
    d = 1 + z * z / n
    return round(z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d, 4)


def gate_item(rec: dict) -> tuple[str, str]:
    """-> (verdict, reason). Verdicts: ACCEPT | REJECT | ADJUDICATE | UNGRADED."""
    d = rec.get("difficulty")
    r = rec.get("discrimination")
    pred = rec.get("predicted_difficulty")

    if d is None:
        return "UNGRADED", "no measured difficulty — an unpiloted item cannot be accepted"
    if d in (0.0, 1.0):
        return "REJECT", f"dead item (difficulty {d}) — carries zero information"
    if r is not None and r < -0.2:
        # The rule this file exists to get right. See module docstring.
        return "ADJUDICATE", (f"negative discrimination ({r:+.3f}) — route to an independent "
                              f"adjudicator; do NOT reject. May be capability-correlated model "
                              f"error rather than a bad key.")
    if not (D_MIN <= d <= D_MAX):
        return "REJECT", f"difficulty {d:.2f} outside [{D_MIN}, {D_MAX}] — do not tune, replace"
    if r is None:
        return "UNGRADED", "discrimination not computed — needs >= 3 gradable models"
    if r < R_MIN:
        return "REJECT", f"discrimination {r:+.3f} < {R_MIN} — near-noise"
    if pred is not None and abs(d - pred) > GAP_MAX:
        return "REJECT", (f"prediction gap |{d:.2f} - {pred:.2f}| = {abs(d - pred):.2f} > "
                          f"{GAP_MAX} — the author's model of this item is wrong")
    return "ACCEPT", f"difficulty {d:.2f}, discrimination {r:+.3f}"


def gate_axis(name: str, items: list[dict]) -> dict:
    verdicts = {}
    for it in items:
        v, why = gate_item(it)
        verdicts.setdefault(v, []).append({"item": it.get("item"), "why": why})
    accept = len(verdicts.get("ACCEPT", []))
    adjud = len(verdicts.get("ADJUDICATE", []))
    # usable_n counts ACCEPT plus items pending adjudication, because an adjudicated-and-kept
    # item is usable. Counting only ACCEPT would understate an axis mid-review.
    usable = accept + adjud
    return {"axis": name, "n": len(items), "accept": accept, "adjudicate": adjud,
            "reject": len(verdicts.get("REJECT", [])),
            "ungraded": len(verdicts.get("UNGRADED", [])),
            "usable_n": usable, "meets_target": usable >= USABLE_TARGET,
            "resolvable_halfwidth": wilson_halfwidth(usable),
            "quotable": usable >= USABLE_TARGET,
            "detail": verdicts}


def selftest() -> bool:
    cases = [
        ("dead-0", {"difficulty": 0.0, "discrimination": 0.5}, "REJECT"),
        ("dead-1", {"difficulty": 1.0, "discrimination": 0.5}, "REJECT"),
        ("negative-disc goes to ADJUDICATE not REJECT",
         {"difficulty": 0.5, "discrimination": -0.6}, "ADJUDICATE"),
        ("too easy", {"difficulty": 0.9, "discrimination": 0.5}, "REJECT"),
        ("too hard", {"difficulty": 0.1, "discrimination": 0.5}, "REJECT"),
        ("low disc", {"difficulty": 0.5, "discrimination": 0.05}, "REJECT"),
        ("bad prediction", {"difficulty": 0.7, "discrimination": 0.5,
                            "predicted_difficulty": 0.2}, "REJECT"),
        ("good", {"difficulty": 0.5, "discrimination": 0.4,
                  "predicted_difficulty": 0.45}, "ACCEPT"),
        ("no difficulty", {"discrimination": 0.4}, "UNGRADED"),
        ("no discrimination", {"difficulty": 0.5}, "UNGRADED"),
        # a dead item that is ALSO negative must reject on deadness first: difficulty 0/1 means
        # no variance, so any r is undefined or meaningless.
        ("dead beats negative", {"difficulty": 0.0, "discrimination": -0.9}, "REJECT"),
    ]
    ok = True
    for name, rec, want in cases:
        got, _ = gate_item(rec)
        good = got == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: {got} (want {want})")
    hw = wilson_halfwidth(USABLE_TARGET)
    good = 0.15 < hw < 0.20
    ok &= good
    print(f"  [{'PASS' if good else 'FAIL'}] halfwidth at usable_n={USABLE_TARGET} is {hw} "
          f"(target band 0.15-0.20)")
    print(f"  selftest {'GREEN' if ok else 'RED'}")
    return bool(ok)


def main():
    if not selftest():
        sys.exit("gate selftest failed — a gate that cannot grade itself grades nothing")
    src = Path(__file__).resolve().parent / "evidence/harness/freeze/latest/axis-saturation.json"
    if not src.exists():
        print(f"\n  no saturation data at {src} — gate is verified but unapplied")
        return
    axes = json.loads(src.read_text())["axes"]
    print(f"\nAPPLYING THE GATE to the current banks ({src.name}):\n")
    print(f"  {'axis':12s} {'n':>3s} {'acc':>4s} {'adj':>4s} {'rej':>4s} {'ungr':>5s} "
          f"{'usable':>7s} {'+-':>6s}  quotable")
    tot = {"n": 0, "accept": 0, "adjudicate": 0, "reject": 0, "usable_n": 0}
    for name, a in axes.items():
        g = gate_axis(name, a["items"])
        for k in tot:
            tot[k] += g[k]
        print(f"  {name:12s} {g['n']:3d} {g['accept']:4d} {g['adjudicate']:4d} {g['reject']:4d} "
              f"{g['ungraded']:5d} {g['usable_n']:7d} {g['resolvable_halfwidth']:6.3f}  "
              f"{'YES' if g['quotable'] else 'NO — do not quote intervals on this axis'}")
    print(f"\n  TOTAL n={tot['n']} accept={tot['accept']} adjudicate={tot['adjudicate']} "
          f"reject={tot['reject']} usable={tot['usable_n']}")
    print(f"  items to author to reach usable_n>={USABLE_TARGET} on every axis: "
          f"{sum(max(0, USABLE_TARGET - gate_axis(n, a['items'])['usable_n']) for n, a in axes.items())}")


if __name__ == "__main__":
    main()
