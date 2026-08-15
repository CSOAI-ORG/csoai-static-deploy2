#!/usr/bin/env python3
"""constrained_vs_freeform.py — does restricting the decoder REVEAL the answer, or CHANGE it?

WHY THIS EXISTS
---------------
An independently-written sov34 baseline found ~23% of answers unparseable and proposed the
obvious remedy: constrain the output to the label set. It is the cheapest experiment available
and it would lift every axis without touching the weights — and I was about to run it as a
harness fix, on the assumption that constraining decoding merely surfaces the label the model
had already chosen.

A 10-item probe before running it falsified that assumption:

    sov34:latest          agree 1   flipped 7   rescued 2
    sov33-unified:latest  agree 2   flipped 6   rescued 2
    qwen2.5:1.5b          agree 9   flipped 1   rescued 0

Free-form, these models reason in prose and state the label last. An enum schema forces a label
at the FIRST token, so it is no longer conditioned on the reasoning. The untrained stock model,
which already emitted bare labels, barely moves. The trained ones disagree with themselves.

Before trusting those flips, the obvious degenerate explanation was ruled out: an enum-
constrained decoder that simply emits the FIRST allowed value would manufacture exactly this
pattern. Re-asking the same items with the enum rotated and reversed:

    sov34:latest          order-INVARIANT 8/8   tracks-first-entry 0/8
    sov33-unified:latest  order-INVARIANT 8/8   tracks-first-entry 0/8

The constrained answer does not depend on label order, so it is a real model output and the
flips are a real disagreement between two decoding regimes.

So the constrained run is a DIFFERENT MEASUREMENT, not a corrected one, and the difference
between the arms may not be reported as "the share of the score that was the harness". This
tool measures the four outcomes separately rather than collapsing them into one delta:

    agree    both arms gradable, same label      — the constraint only reformatted
    flip     both arms gradable, DIFFERENT label — the constraint changed the answer
    rescued  free-form ungradable, constrained gradable — the constraint recovered an answer
    lost     free-form gradable, constrained ungradable — should be ~0; a check on the schema

A "rescued" answer is only a win if it is also CORRECT, so rescues are split by correctness.
Rescuing a wrong answer raises the gradable count while adding nothing but noise.

IT ALSO RECOUNTS DEAD ITEMS HONESTLY
------------------------------------
An item is called dead by unanimity among the models that actually produced a gradable answer
ON THAT ITEM — which is not the fleet size. gpt-oss:20b returned no usable label on 100% of
governance items, inflating the fleet that certification was granted on while contributing to
no item's unanimity. This recomputes deadness against each item's own gradable N, using the
per-model-per-item matrix, so a fleet of 22 never certifies an item that only 6 models answered.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fleet_power import certify  # noqa: E402

FREEZE = HERE / "evidence/harness/freeze/latest"
BASE = FREEZE / "axis-saturation.json"
CONS = FREEZE / "axis-saturation-constrained.json"


def load(p: Path):
    if not p.exists():
        return None
    return json.loads(p.read_text())


def recount_dead(doc) -> None:
    """Dead-item count re-derived against each item's OWN gradable N."""
    print("\nDEAD-ITEM RECOUNT — certified against each item's own gradable N")
    print(f"  fleet as launched: {len(doc.get('models', []))}")
    print(f"  {'axis':12s} {'raw dead':>9s} {'certified':>10s} {'eff-N min':>10s} "
          f"{'eff-N med':>10s}  mute models")
    for axis, a in doc.get("axes", {}).items():
        mi = a.get("model_items") or {}
        if not mi:
            print(f"  {axis:12s} (no matrix in this file — re-run to populate)")
            continue
        models = list(mi)
        n_items = len(next(iter(mi.values()))["correct"])
        raw = cert = 0
        effs = []
        for i in range(n_items):
            vals = [mi[m]["correct"][i] for m in models if mi[m]["correct"][i] is not None]
            if len(vals) < 3:
                continue
            effs.append(len(vals))
            diff = sum(1 for v in vals if v) / len(vals)
            if diff in (0.0, 1.0):
                raw += 1
                if certify(len(vals))[0]:
                    cert += 1
        mute = [m for m in models if not any(w == "ok" for w in mi[m]["why"])]
        emin = min(effs) if effs else None
        emed = sorted(effs)[len(effs) // 2] if effs else None
        print(f"  {axis:12s} {raw:>9d} {cert:>10d} {str(emin):>10s} {str(emed):>10s}  "
              f"{', '.join(mute) if mute else '-'}")


def compare(base, cons) -> None:
    print("\nFREE-FORM vs FORMAT-CONSTRAINED — same items, same fleet, one variable changed")
    tot = {"agree": 0, "flip": 0, "rescued_right": 0, "rescued_wrong": 0, "lost": 0}
    per_model = {}
    for axis, a in base.get("axes", {}).items():
        b_mi = a.get("model_items") or {}
        c_mi = (cons.get("axes", {}).get(axis) or {}).get("model_items") or {}
        if not b_mi or not c_mi:
            continue
        for m in set(b_mi) & set(c_mi):
            bm, cm = b_mi[m], c_mi[m]
            st = per_model.setdefault(m, {"agree": 0, "flip": 0, "rescued_right": 0,
                                          "rescued_wrong": 0, "lost": 0})
            for i in range(min(len(bm["given"]), len(cm["given"]))):
                bg, cg = bm["given"][i], cm["given"][i]
                if bg is None and cg is not None:
                    k = "rescued_right" if cm["correct"][i] else "rescued_wrong"
                elif bg is not None and cg is None:
                    k = "lost"
                elif bg is None and cg is None:
                    continue
                else:
                    k = "agree" if bg == cg else "flip"
                st[k] += 1
                tot[k] += 1

    print(f"  {'model':26s} {'agree':>6s} {'FLIP':>6s} {'resc+':>6s} {'resc-':>6s} {'lost':>5s}"
          f"  {'flip rate':>9s}")
    for m, s in sorted(per_model.items(), key=lambda kv: -(kv[1]["flip"])):
        both = s["agree"] + s["flip"]
        fr = f"{s['flip']/both:.0%}" if both else "-"
        print(f"  {m:26s} {s['agree']:>6d} {s['flip']:>6d} {s['rescued_right']:>6d} "
              f"{s['rescued_wrong']:>6d} {s['lost']:>5d}  {fr:>9s}")
    both = tot["agree"] + tot["flip"]
    print(f"\n  TOTAL agree {tot['agree']}  flipped {tot['flip']}  "
          f"rescued-correct {tot['rescued_right']}  rescued-wrong {tot['rescued_wrong']}  "
          f"lost {tot['lost']}")
    if both:
        print(f"  Of answers gradable in BOTH arms, {tot['flip']/both:.1%} changed label when "
              f"the decoder was constrained.")
        print("  That share is NOT a harness artefact being removed — it is the two arms "
              "disagreeing about the answer.")
    resc = tot["rescued_right"] + tot["rescued_wrong"]
    if resc:
        print(f"  Of {resc} answers the constraint rescued from ungradable, "
              f"{tot['rescued_right']} were correct ({tot['rescued_right']/resc:.0%}) — "
              f"the rest added gradable noise.")


def main():
    base = load(BASE)
    if not base:
        sys.exit(f"no baseline at {BASE}")
    print(f"baseline    : {base.get('measured_at')}  arm={base.get('arm', 'free-form (implied)')}")
    recount_dead(base)
    cons = load(CONS)
    if not cons:
        print(f"\n  no constrained arm yet at {CONS}")
        print("  run:  GOVBENCH_CONSTRAIN=1 GSPC_MODELS=... python3 axis_saturation.py")
        return
    print(f"constrained : {cons.get('measured_at')}  arm={cons.get('arm')}")
    compare(base, cons)


if __name__ == "__main__":
    main()
