#!/usr/bin/env python3
"""axis_saturation.py — WHICH of the six GSPC axes actually discriminate, measured not asserted.

A parallel session reports "5 of 6 benchmarks are saturated; only GovBench spreads". That is
the right shape of claim and it is the premise of the whole v2 item-set effort, so it should
rest on a measurement rather than on a report. This measures it directly.

WHAT SATURATION ACTUALLY IS
---------------------------
A benchmark is saturated when its items no longer separate models. Two distinct failure modes
get lumped together under "everyone scores ~100%":

    CEILING     nearly every model passes nearly every item        -> no headroom
    FLOOR       nearly every model fails nearly every item         -> no traction
    NO SPREAD   models differ little from each other in total      -> nothing to rank

They need different fixes. A ceiling axis needs HARDER items. A floor axis needs items the
models can engage with at all — its problem is not difficulty, and adding harder items makes
it worse. Reporting only a mean pass-rate cannot tell them apart, which is why this reports
per-item difficulty, the dead-item count, discrimination, and the between-model spread.

STATISTICS
----------
difficulty      fraction of models answering an item correctly
dead item       difficulty 0.0 or 1.0 — contributes zero information to any ranking
discrimination  point-biserial of item-correct against the model's REST-score on that axis
                (the axis total EXCLUDING this item; including it biases every item upward)
spread          max - min of model totals on the axis, with the SD across models
usable_n        items that are neither dead nor negatively discriminating — the effective
                sample size, which is what an interval should really be computed on
unparsed        the model never emitted a usable label. NOT the same as a wrong answer, and not
                the same as a dead endpoint — the three are recorded separately

WHAT IT RECORDS PER MODEL PER ITEM
----------------------------------
Earlier versions kept only per-item statistics across the fleet and per-model totals. That is
enough to say an axis discriminates, but it cannot answer "which items did THIS model fail?" —
so it could neither debug a single model nor be reconciled against an independently-written
harness. The output now carries the full matrix, the label each model actually emitted, and
why an answer was ungradable, and it reports accuracy under BOTH denominator conventions
(excluding ungradable answers, and counting them wrong) because harnesses differ on that and
the difference is not a disagreement about the model.
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
# The RunPod proxy rejects requests with no User-Agent, which made every pod call fail and
# the overnight run report "no substrate" against a pod that was serving 149 models fine.
UA_HDR = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

# Deliberately spans architectures and sizes: if an axis fails to separate THESE, it is not
# separating anything. A saturation claim measured only on same-size same-family siblings
# would be weak evidence.
MODELS = [
    "qwen2.5:0.5b",                    # 494M qwen2 base
    "qwen3:0.6b",                      # 752M qwen3
    "llama3.2:3b",                     # 3.2B llama
    "sov33-unified:latest",            # 3.2B llama, trained
    "clan-law-refusing:latest",        # 494M, refusal-prompted
    "clan-law-plain:latest",           # 494M, plain-prompted
    "sov-sovereign-v4:latest",         # 494M, sovereign-prompted
    "eat-unsloth-050b:2026-08-02",     # 494M, unsloth lineage
]


# 2026-08-04 — the first run used 8 models and flagged 18 items at r < -0.2. At n=8 a
# correlation of 0.2 is not resolved, so those flags were screening signals rather than
# verdicts, and the spec said so. GSPC_MODELS lets the same harness re-run at a fleet size
# where discrimination actually resolves, without editing the list in source.
if os.environ.get("GSPC_MODELS"):
    MODELS = [m.strip() for m in os.environ["GSPC_MODELS"].split(",") if m.strip()]


# 2026-08-05 — three separate measurements agreed that these models' dominant failure is
# instruction-following, not knowledge: they wrap the answer in prose and often never emit the
# bare label, which this harness then has to score as ungradable. The obvious fix is to restrict
# the decoder to the label set, and it was proposed as the cheapest available experiment.
#
# IT IS NOT A HARNESS FIX. A 10-item probe before running it found that constraining the decoder
# CHANGES the answer rather than merely revealing it:
#
#     sov34:latest          agree 1   flipped 7   rescued-from-unparsed 2
#     sov33-unified:latest  agree 2   flipped 6   rescued-from-unparsed 2
#     qwen2.5:1.5b          agree 9   flipped 1   rescued-from-unparsed 0
#
# The trained models disagree with themselves most of the time; the untrained stock model, which
# already emitted bare labels, is stable. That is consistent with WHERE the label is forced:
# free-form these models reason in prose and state a label last, while the enum forces a label
# at the first token, so the label is no longer conditioned on the reasoning.
#
# So the two arms are DIFFERENT MEASUREMENTS, not a biased one and a corrected one. The
# difference between them may not be read as "the share of the score that was the harness".
CONSTRAIN = os.environ.get("GOVBENCH_CONSTRAIN") == "1"


def ask(model: str, prompt: str, labels: list[str] | None = None) -> str | None:
    payload = {"model": model, "stream": False,
               "options": {"temperature": 0, "num_predict": 24},
               "messages": [{"role": "user", "content": prompt}]}
    if CONSTRAIN and labels:
        # Ollama accepts a JSON Schema here and constrains decoding to match it.
        #
        # 2026-08-05, MEASURED — the two claims previously made here were both WRONG, and the
        # paired 33-model run refuted them. Left as a warning rather than deleted.
        #
        # CLAIM 1, false: "an enum makes no_label structurally impossible". gpt-oss:20b
        # returned no_label on 24 of 24 governance items in the CONSTRAINED arm — identical to
        # free-form. The enum did not bind for that model at all. It is the only model mute in
        # either arm, and it is mute in both. A decoder constraint is a request to the server,
        # not a guarantee, and it must be verified per model rather than assumed.
        #
        # CLAIM 2, false: "it converts a formatting failure into a real answer that can be
        # graded right or wrong". It converts it into a GUESS. Of the 62 answers constraint
        # made gradable across the whole fleet, 28 were correct — 45.2%, Wilson95
        # [33.4%, 57.5%], against a mean chance level of 43.1% (four of the six axes are
        # binary). The interval CONTAINS chance. Nothing was recovered.
        #
        # Meanwhile 726 of 2816 answers gradable in both arms FLIPPED (74.2% self-agreement),
        # and governance — the family's best axis — lost half its usable items (23 -> 12) and
        # most of its spread (0.5583 -> 0.2083) under constraint. The constrained arm is not a
        # better measurement of the same thing; it is a worse measurement of a different thing.
        # Do NOT promote it to the default, and do not difference the two arms' scores.
        payload["format"] = {"type": "string", "enum": list(labels)}
    body = json.dumps(payload).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=body,
                                 headers={"Content-Type": "application/json", **UA_HDR})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())["message"]["content"].strip()
    except Exception:
        return None


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 4)


def available() -> set[str]:
    try:
        req = urllib.request.Request(f"{OLLAMA}/api/tags", headers=UA_HDR)
        with urllib.request.urlopen(req, timeout=30) as r:
            return {m["name"] for m in json.loads(r.read())["models"]}
    except Exception:
        return set()


def main():
    have = available()
    if not have:
        sys.exit(f"no substrate at {OLLAMA}")
    models = [m for m in MODELS if m in have]
    missing = [m for m in MODELS if m not in have]
    if missing:
        print(f"  absent, excluded: {missing}")
    if len(models) < 4:
        sys.exit(f"only {len(models)} models present — discrimination needs a real spread")

    # 2026-08-04 — the first run reported 35 dead items across 90 on a fleet of 8. At N=8 and a
    # true pass-rate of 0.85, 27% of LIVE items look dead by unanimity alone, so most of that
    # count was an artefact. The tool now states its own standing before reporting a number that
    # depends on fleet size, rather than leaving the reader to discover the limit afterwards.
    from fleet_power import certify  # noqa: E402
    certified, why = certify(len(models))
    print(f"AXIS SATURATION — {len(models)} models x 6 axes")
    print(f"  dead-item count: {'CERTIFIED' if certified else 'NOT CERTIFIED'}")
    print(f"  {why}")
    if not certified:
        print("  -> dead/usable figures below are UPPER BOUNDS on deadness, not measurements.")
    print(flush=True)
    report = {}
    for axis in G.AXES:
        items, field, labels = G.load_axis(axis)
        # correct[model] = [1|0|None per item]
        # given[model]   = [extracted label | None per item] — lets a reader re-grade under a
        #                  different rule without re-running the fleet
        # reasons[model] = [ok | no_response | no_label | multi_label per item]
        correct = {}
        given = {}
        reasons = {}
        for m in models:
            row, lab, rsn = [], [], []
            for it in items:
                prompt = (f"{it[field]}\n\nAnswer with EXACTLY ONE of these labels and "
                          f"nothing else: {' | '.join(labels)}")
                resp = ask(m, prompt, labels)
                if resp is None:
                    row.append(None)
                    lab.append(None)
                    rsn.append("no_response")
                    continue
                hits = [l for l in labels if re.search(rf"\b{re.escape(l)}\b", resp.upper())]
                if len(hits) == 1:
                    row.append(hits[0] == it["expected"])
                    lab.append(hits[0])
                    rsn.append("ok")
                else:
                    row.append(None)
                    lab.append(None)
                    rsn.append("no_label" if not hits else "multi_label")
            correct[m], given[m], reasons[m] = row, lab, rsn

        totals = {}
        for m in models:
            got = [c for c in correct[m] if c is not None]
            totals[m] = (sum(got) / len(got)) if got else None

        # 2026-08-05 — reconciling against an independently-written harness stalled here: it
        # scored unparsed answers WRONG, this one EXCLUDES them, so the two accuracies were not
        # comparable and there was no way to tell a real disagreement from a denominator
        # difference. Reporting both denominators, and splitting "ungradable" into its causes,
        # removes the ambiguity instead of leaving the reader to guess at it. A dead endpoint
        # (no_response) and a model that never emits the label (no_label) are not the same
        # failure and must not share a number.
        model_stats = {}
        for m in models:
            rsn = reasons[m]
            n = len(rsn)
            n_ok = rsn.count("ok")
            n_right = sum(1 for c in correct[m] if c)
            unparsed = rsn.count("no_label") + rsn.count("multi_label")
            model_stats[m] = {
                "n_items": n,
                "n_gradable": n_ok,
                "n_correct": n_right,
                # this harness's convention: ungradable answers are excluded
                "accuracy_gradable_only": round(n_right / n_ok, 4) if n_ok else None,
                # the other convention: ungradable answers count as wrong
                "accuracy_ungradable_as_wrong": round(n_right / n, 4) if n else None,
                "ungradable": {"no_response": rsn.count("no_response"),
                               "no_label": rsn.count("no_label"),
                               "multi_label": rsn.count("multi_label")},
                # instruction-following failure only — excludes substrate failure
                "unparsed_rate": round(unparsed / n, 4) if n else None,
            }

        rows = []
        for i in range(len(items)):
            vals = [(m, correct[m][i]) for m in models if correct[m][i] is not None]
            if len(vals) < 3:
                rows.append({"item": i, "status": "UNMEASURED",
                             "n_gradable": len(vals), "anchor": items[i].get("anchor")})
                continue
            diff = sum(1 for _, v in vals if v) / len(vals)
            xs = [1 if v else 0 for _, v in vals]
            ys = []
            for m, _ in vals:
                other = [c for j, c in enumerate(correct[m]) if j != i and c is not None]
                ys.append(sum(other) / len(other) if other else 0.0)
            disc = pearson(xs, ys)
            # 2026-08-05 — deadness is decided by unanimity among the models that actually
            # produced a gradable answer on THIS item, which is not the fleet size. gpt-oss:20b
            # returned no usable label on 100% of governance items, so it inflated the fleet
            # count that certification was granted on while contributing nothing to any item's
            # unanimity. Certifying per item against its own gradable N closes that gap — a
            # fleet of 22 does not certify an item only 6 models answered.
            is_dead = diff in (0.0, 1.0)
            rows.append({"item": i, "difficulty": round(diff, 4), "discrimination": disc,
                         "expected": items[i]["expected"], "anchor": items[i].get("anchor"),
                         "n_gradable": len(vals),
                         "dead": is_dead,
                         "dead_certified": bool(is_dead and certify(len(vals))[0])})

        scored = [r for r in rows if "difficulty" in r]
        dead = [r for r in scored if r["dead"]]
        dead_cert = [r for r in dead if r["dead_certified"]]
        # the effective fleet actually answering this axis — the number certification should be
        # read against, not len(models)
        eff_n = [r["n_gradable"] for r in scored]
        eff_min = min(eff_n) if eff_n else None
        eff_med = sorted(eff_n)[len(eff_n) // 2] if eff_n else None
        mute = [m for m in models if model_stats[m]["n_gradable"] == 0]
        neg = [r for r in scored if r["discrimination"] is not None and r["discrimination"] < -0.2]
        usable = [r for r in scored if not r["dead"]
                  and not (r["discrimination"] is not None and r["discrimination"] < -0.2)]
        tv = [t for t in totals.values() if t is not None]
        spread = round(max(tv) - min(tv), 4) if tv else None
        sd = (round(math.sqrt(sum((t - sum(tv) / len(tv)) ** 2 for t in tv) / len(tv)), 4)
              if len(tv) > 1 else None)
        mean_diff = round(sum(r["difficulty"] for r in scored) / len(scored), 4) if scored else None

        mode = ("FLOOR — models cannot engage; harder items make it worse"
                if mean_diff is not None and mean_diff < 0.25 else
                "CEILING — no headroom; needs harder items"
                if mean_diff is not None and mean_diff > 0.80 else
                "MID — difficulty is fine")
        verdict = ("SATURATED — no usable spread between models" if spread is not None and spread < 0.10
                   else "DISCRIMINATES")

        report[axis] = {"n_items": len(items), "n_scored": len(scored), "n_dead": len(dead),
                        "n_dead_certified": len(dead_cert),
                        "effective_fleet_min": eff_min, "effective_fleet_median": eff_med,
                        "models_mute_on_axis": mute,
                        "n_negative_disc": len(neg), "usable_n": len(usable),
                        "mean_difficulty": mean_diff, "spread": spread, "sd_across_models": sd,
                        "difficulty_mode": mode, "verdict": verdict,
                        "model_totals": totals, "model_stats": model_stats,
                        # the per-model-per-item matrix. Without it this file could report that
                        # an axis discriminates but not WHICH items a given model failed, so
                        # neither debugging one model nor reconciling against another harness
                        # was possible from the output alone.
                        "model_items": {m: {"correct": correct[m], "given": given[m],
                                            "why": reasons[m]} for m in models},
                        "items": rows}
        print(f"  {axis:12s} n={len(items):2d}  mean_diff {mean_diff}  dead {len(dead):2d}"
              f"(cert {len(dead_cert)})  neg {len(neg)}  usable {len(usable):2d}  "
              f"spread {spread}  sd {sd}")
        print(f"               effective fleet on this axis: min {eff_min}, median {eff_med} "
              f"of {len(models)}" + (f" — MUTE: {', '.join(mute)}" if mute else ""))
        print(f"               {mode}")
        print(f"               {verdict}")
        # An axis can look FLOOR purely because models never emit the label. Printing the worst
        # unparsed rates next to the verdict keeps that alternative explanation visible rather
        # than leaving it to be discovered later.
        worst = sorted(models, key=lambda m: model_stats[m]["unparsed_rate"] or 0, reverse=True)[:3]
        loud = [f"{m} {model_stats[m]['unparsed_rate']:.0%}" for m in worst
                if (model_stats[m]["unparsed_rate"] or 0) > 0]
        if loud:
            print(f"               unparsed (never emitted a label): {', '.join(loud)}")
        print(flush=True)

    # The constrained arm writes beside the baseline, never over it — the whole value of the
    # experiment is the DIFFERENCE between the two files, which an overwrite would destroy.
    name = "axis-saturation-constrained.json" if CONSTRAIN else "axis-saturation.json"
    out = HERE / "evidence/harness/freeze/latest" / name
    out.write_text(json.dumps({
        "measured_at": datetime.now(timezone.utc).isoformat(), "substrate": OLLAMA,
        "models": models, "excluded_absent": missing,
        "arm": "format-constrained (decoder restricted to the label enum)" if CONSTRAIN
               else "free-form (label requested in the prompt only)",
        # 2026-08-05 — the console printed "NOT CERTIFIED" while the JSON published n_dead with
        # no caveat attached, so anyone reading the file downstream saw a bare number and had no
        # way to know the tool had refused to stand behind it. The caveat now travels with the
        # data it qualifies.
        "dead_item_count_certified": certified,
        "certification": why,
        "fleet_n": len(models),
        "grader": "exact-label, single-hit; ambiguous or multi-label answers are UNGRADABLE not wrong",
        "definitions": {
            "dead": "difficulty 0.0 or 1.0 — zero information for any ranking",
            "usable_n": "items neither dead nor negatively discriminating — the effective sample size",
            "FLOOR vs CEILING": ("both look like 'no spread' in a mean, and need OPPOSITE fixes. "
                                 "A floor axis does not need harder items; it needs items its "
                                 "models can engage with at all."),
            "model_items": ("per-model-per-item matrix. correct = 1|0|null, given = the label the "
                            "model actually emitted, why = ok|no_response|no_label|multi_label. "
                            "Present so a reader can ask WHICH items a model failed, re-grade "
                            "under a different rule, or reconcile against another harness."),
            "two accuracies": ("accuracy_gradable_only EXCLUDES ungradable answers; "
                               "accuracy_ungradable_as_wrong COUNTS THEM WRONG. Harnesses differ "
                               "on this and the gap between the two is not a disagreement about "
                               "the model — comparing across conventions is the error."),
            "unparsed_rate": ("no_label + multi_label over all items — instruction-following "
                              "failure. EXCLUDES no_response, which is substrate failure.")},
        "axes": report}, indent=2))
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
