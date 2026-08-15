#!/usr/bin/env python3
"""arm_diff.py — pair the free-form and constrained arms item by item.

WHY THIS IS NOT A SUBTRACTION OF TWO SCORES
-------------------------------------------
The tempting read of a constrained-decoding arm is "the model always knew the answer, the
harness just couldn't hear it — so the difference between the arms is the share of the score
that was a formatting artefact". That read is wrong here, and this tool exists to show why
rather than to assert it.

Constraining the decoder to a label enum does not surface a hidden answer. It forces the
label at the FIRST token, so the label is no longer conditioned on the reasoning the model
would otherwise have produced first. A 10-item probe found the trained models agree with
themselves on 1-2 of 10 under that change. If constraint merely revealed an existing answer,
agreement would be near total.

So every gradable-in-both item falls into exactly one of two buckets, and they mean opposite
things:

    AGREE     same label both arms — constraint changed nothing
    FLIPPED   different label      — constraint changed the ANSWER, not its presentation

and the items ungradable free-form split into:

    RESCUED   no label free-form -> correct under constraint
    FORCED    no label free-form -> wrong   under constraint   (a coin-flip made legible)

RESCUED is the only bucket that supports "the harness was hiding a real answer", and it is
only credible if FLIPPED is small. A large FLIPPED count means the two arms measure two
different things and their scores must not be differenced at all.

FORCED matters on its own: constraint converts silence into a gradable wrong answer, which
LOOKS like a measurement where there was none. An enum cannot create knowledge; it can only
make a guess scoreable.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load(p: Path) -> dict:
    if not p.exists():
        sys.exit(f"missing arm file: {p}")
    return json.loads(p.read_text())


def main():
    here = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("evidence/harness/freeze/latest")
    free = load(here / "arm-freeform.json")
    cons = load(here / "axis-saturation-constrained.json")

    if free.get("models") != cons.get("models"):
        print("WARNING: fleets differ between arms — the pairing below is not like-for-like")
    print(f"free-form   {free['measured_at']}  n={len(free['models'])}  {free['substrate']}")
    print(f"constrained {cons['measured_at']}  n={len(cons['models'])}  {cons['substrate']}")
    print(f"certified: free-form {free.get('dead_item_count_certified')} / "
          f"constrained {cons.get('dead_item_count_certified')}")
    print()

    print(f"{'axis':13s} {'mean_diff f->c':>18s} {'spread f->c':>17s} "
          f"{'usable_n f->c':>15s} {'unparsed f->c':>16s}")
    for axis in free["axes"]:
        f, c = free["axes"][axis], cons["axes"].get(axis)
        if not c:
            continue
        fu = sum(s["ungradable"]["no_label"] + s["ungradable"]["multi_label"]
                 for s in f["model_stats"].values())
        cu = sum(s["ungradable"]["no_label"] + s["ungradable"]["multi_label"]
                 for s in c["model_stats"].values())
        ftot = sum(s["n_items"] for s in f["model_stats"].values())
        ctot = sum(s["n_items"] for s in c["model_stats"].values())
        print(f"{axis:13s} {f['mean_difficulty']:8.4f} -> {c['mean_difficulty']:<7.4f} "
              f"{f['spread']:7.4f} -> {c['spread']:<7.4f} "
              f"{f['usable_n']:6d} -> {c['usable_n']:<7d} "
              f"{fu/ftot:7.1%} -> {cu/ctot:<7.1%}")

    # ── the paired matrix: the only thing that can tell "revealed" from "changed" ──
    print()
    print("PAIRED, per model — gradable in BOTH arms:")
    print(f"{'model':34s} {'agree':>6s} {'flipped':>8s} {'rescued':>8s} {'forced':>7s} "
          f"{'agree%':>7s}")
    tot = {"agree": 0, "flip": 0, "resc": 0, "forc": 0}
    per_model = {}
    for m in free["models"]:
        agree = flip = resc = forc = 0
        for axis in free["axes"]:
            f, c = free["axes"][axis], cons["axes"].get(axis)
            if not c or m not in f.get("model_items", {}) or m not in c.get("model_items", {}):
                continue
            fi, ci = f["model_items"][m], c["model_items"][m]
            items = f["items"]
            for i in range(len(fi["given"])):
                fg, cg = fi["given"][i], ci["given"][i]
                if fg is not None and cg is not None:
                    agree += fg == cg
                    flip += fg != cg
                elif fg is None and cg is not None:
                    # ungradable free-form, gradable under constraint
                    exp = items[i].get("expected")
                    if ci["correct"][i] or cg == exp:
                        resc += 1
                    else:
                        forc += 1
        both = agree + flip
        per_model[m] = (agree, flip, resc, forc)
        tot["agree"] += agree; tot["flip"] += flip
        tot["resc"] += resc; tot["forc"] += forc
        pct = f"{agree/both:.0%}" if both else "n/a"
        print(f"{m:34s} {agree:6d} {flip:8d} {resc:8d} {forc:7d} {pct:>7s}")

    both = tot["agree"] + tot["flip"]
    print()
    print(f"FLEET  agree {tot['agree']}  flipped {tot['flip']}  "
          f"rescued {tot['resc']}  forced {tot['forc']}")
    if both:
        ar = tot["agree"] / both
        print(f"       self-agreement across arms: {ar:.1%} of items gradable in both")
        if ar < 0.75:
            print("       -> The arms DISAGREE on the answer itself. They are two different")
            print("          measurements; do NOT difference their scores or describe the gap")
            print("          as 'the share that was the harness'.")
        else:
            print("       -> Answers are largely stable under constraint, so the gap between")
            print("          arms is mostly formatting rather than a changed answer.")
    if tot["resc"] + tot["forc"]:
        keep = tot["resc"] / (tot["resc"] + tot["forc"])
        print(f"       of answers constraint made gradable, {keep:.1%} were correct "
              f"({tot['resc']} rescued vs {tot['forc']} forced-wrong)")
        print("       a fair coin would sit at 1/n_labels; above that is real signal recovered,")
        print("       at or below it the enum only made guessing scoreable.")


if __name__ == "__main__":
    main()
