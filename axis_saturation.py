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


def ask(model: str, prompt: str) -> str | None:
    body = json.dumps({"model": model, "stream": False,
                       "options": {"temperature": 0, "num_predict": 24},
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
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
        with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=20) as r:
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

    print(f"AXIS SATURATION — {len(models)} models x 6 axes\n", flush=True)
    report = {}
    for axis in G.AXES:
        items, field, labels = G.load_axis(axis)
        # correct[model] = [1|0|None per item]
        correct = {}
        for m in models:
            row = []
            for it in items:
                prompt = (f"{it[field]}\n\nAnswer with EXACTLY ONE of these labels and "
                          f"nothing else: {' | '.join(labels)}")
                resp = ask(m, prompt)
                if resp is None:
                    row.append(None)
                    continue
                hits = [l for l in labels if re.search(rf"\b{re.escape(l)}\b", resp.upper())]
                row.append((hits[0] == it["expected"]) if len(hits) == 1 else None)
            correct[m] = row

        totals = {}
        for m in models:
            got = [c for c in correct[m] if c is not None]
            totals[m] = (sum(got) / len(got)) if got else None

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
            rows.append({"item": i, "difficulty": round(diff, 4), "discrimination": disc,
                         "expected": items[i]["expected"], "anchor": items[i].get("anchor"),
                         "dead": diff in (0.0, 1.0)})

        scored = [r for r in rows if "difficulty" in r]
        dead = [r for r in scored if r["dead"]]
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
                        "n_negative_disc": len(neg), "usable_n": len(usable),
                        "mean_difficulty": mean_diff, "spread": spread, "sd_across_models": sd,
                        "difficulty_mode": mode, "verdict": verdict,
                        "model_totals": totals, "items": rows}
        print(f"  {axis:12s} n={len(items):2d}  mean_diff {mean_diff}  dead {len(dead):2d}  "
              f"neg {len(neg)}  usable {len(usable):2d}  spread {spread}  sd {sd}")
        print(f"               {mode}")
        print(f"               {verdict}\n", flush=True)

    out = HERE / "evidence/harness/freeze/latest/axis-saturation.json"
    out.write_text(json.dumps({
        "measured_at": datetime.now(timezone.utc).isoformat(), "substrate": OLLAMA,
        "models": models, "excluded_absent": missing,
        "grader": "exact-label, single-hit; ambiguous or multi-label answers are UNGRADABLE not wrong",
        "definitions": {
            "dead": "difficulty 0.0 or 1.0 — zero information for any ranking",
            "usable_n": "items neither dead nor negatively discriminating — the effective sample size",
            "FLOOR vs CEILING": ("both look like 'no spread' in a mean, and need OPPOSITE fixes. "
                                 "A floor axis does not need harder items; it needs items its "
                                 "models can engage with at all.")},
        "axes": report}, indent=2))
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
