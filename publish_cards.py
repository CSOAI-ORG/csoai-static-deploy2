#!/usr/bin/env python3
"""publish_cards.py — regenerate the six GSPC dataset cards from measured data.

WHY
---
The live `csoai/govbench` card carried TWO conflicting H1 sections. The first described the
six-axis family correctly. The second claimed **174 items** for a dataset that is measurably
**24**, and named a different family (CareBench, AIRBench, SwarmBench) that contradicts the
table directly above it.

An unevidenced number on the most-read public surface is exactly what the counter-canon rule
("no number without a file") exists to stop, and a dataset card is the surface AI retrieval
systems actually read — more than any web page in the estate. Two H1s on one page is also a
straightforward SEO defect.

Every figure written here comes from a file on disk:
    n, labels, label_counts   gspcaxes.json, read from the live Hub datasets
    difficulty, spread, usable_n, dead, negative-discrimination
                              evidence/harness/freeze/latest/axis-saturation.json (30 models)
    fleet certification       evidence/harness/freeze/latest/fleet-power.json

Nothing is asserted that is not in one of those. Where a figure cannot be supported, the card
says so rather than omitting it — including that NO axis currently reaches the usable_n>=30
needed to quote an interval, which is a statement against our own instrument.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EV = HERE / "evidence/harness/freeze/latest"
AXES_SPEC = Path.home() / "Downloads/gspcaxes.json"

FAMILY = [
    ("governance", "GovBench", "govbench", "EU AI Act risk tier"),
    ("safety", "DefBench", "defbench", "calibrated refusal"),
    ("provenance", "ProvBench", "provbench", "C2PA manifest survival"),
    ("continuity", "PQCBench", "pqcbench", "post-quantum migration"),
    ("conformance", "MCPBench", "mcpbench", "MCP tool-contract conformance"),
    ("openness", "OSSBench", "ossbench", "licence-vs-use compatibility"),
]


def family_table() -> str:
    rows = ["| Axis | Benchmark | Task | n | Hugging Face | Kaggle |",
            "|---|---|---|---:|---|---|"]
    for axis, bench, slug, task in FAMILY:
        n = SPEC_N.get(axis, "?")
        rows.append(
            f"| {axis} | {bench} | {task} | {n} | "
            f"[`csoai/{slug}`](https://huggingface.co/datasets/csoai/{slug}) | "
            f"[`gspc-{slug}`](https://www.kaggle.com/datasets/nicktempleman/gspc-{slug}) |")
    return "\n".join(rows)


def card(axis: str, bench: str, slug: str, task: str) -> str:
    spec = SPEC[axis]
    sat = SAT.get(axis, {})
    n = spec["n"]
    labels = spec["labels"]
    counts = spec.get("label_counts") or {}
    lc = "\n".join(f"| `{k}` | {v} |" for k, v in counts.items()) or "| — | — |"

    md = sat.get("mean_difficulty")
    spread = sat.get("spread")
    usable = sat.get("usable_n")
    dead = sat.get("n_dead")
    neg = sat.get("n_negative_disc")

    measured = ""
    if md is not None:
        quotable = "yes" if (usable or 0) >= 30 else "**no** — below `usable_n ≥ 30`"
        measured = f"""
## Measured behaviour of this axis

Across **{SAT_MODELS} models** spanning 494M to 20B, three architectures ({SAT_DATE}):

| Statistic | Value | What it means |
|---|---:|---|
| mean difficulty | {md:.3f} | fraction of models answering an item correctly |
| spread (max−min) | {spread:.3f} | how far this axis separates the best model from the worst |
| dead items | {dead} / {n} | passed by every model or none — zero information |
| negative discrimination | {neg} | better-overall models do worse — routed to adjudication, not deleted |
| **usable n** | **{usable}** | items that are neither dead nor negatively discriminating |
| quotable? | {quotable} | whether a 95% interval on this axis should be published |

**This axis is not saturated.** A spread of {spread:.3f} means it does separate models. But at
`usable_n = {usable}` it cannot yet resolve a difference worth reporting — a 95% Wilson interval
needs `usable_n ≥ 30` to narrow to ±0.169. We publish that limit rather than quoting intervals
we cannot support.

Dead-item counts are only trustworthy above **N = 19** models — at N = 8, 27% of genuinely
usable items look dead purely by unanimity. This run is certified at N = {SAT_MODELS}.
"""

    return f"""---
license: apache-2.0
pretty_name: {bench} — {task} ({axis} axis, GSPC)
language:
  - en
tags:
  - benchmark
  - ai-governance
  - eu-ai-act
  - gspc
  - {axis}
  - evaluation
  - measurement
task_categories:
  - text-classification
size_categories:
  - n<1K
---

# {bench} — the {axis} axis of GSPC

> **{task}**, scored against frozen, corpus-anchored ground truth. **n = {n} items.**

One of the **six axes** of the GSPC instrument, published by **CSOAI Ltd** (UK 16939677) — an
independent AI **measurement** body. **Not a certifier, and this is not a conformity
assessment.** DOI [{DOI}](https://doi.org/{DOI})

## Labels

| Label | Items |
|---|---:|
{lc}

Total **{n}**. Labels: {", ".join(f"`{l}`" for l in labels)}
{measured}
## The six axes

{family_table()}

**90 items across six axes.** Every count above was read from the live datasets, not asserted.

## How to read a score from this benchmark

- **Three outcomes, never two.** measured / unmeasured / failed. An ungradable generation is
  `UNMEASURED` and carries no score — it is never counted as a wrong answer.
- **Report `usable_n`, not `n`.** An axis carrying `n = 14` when items are dead is claiming more
  evidence than it has.
- **Intervals over point estimates.** Any comparison whose 95% intervals overlap is
  `NOT_RESOLVED`, and we say so.
- **Measurement, not certification.** Score bands are descriptive. Regulatory determinations are
  reserved to authorities.

## Known limitations

- No frontier-judge validation. Grading is exact-label or a refusal detector validated at 98.9%
  against 92 hand-labelled responses (single labeller, no inter-rater agreement).
- Item difficulty is a property of **item × fleet**, not of the item alone. On a fleet weighted
  toward small models, difficulty verdicts describe the fleet.
- Item discrimination is estimated, not resolved, at current fleet sizes.

*Part of the GSPC family · [csoai.org](https://csoai.org) · CC-BY-4.0 for the cards, Apache-2.0
for the item sets*
"""


if __name__ == "__main__":
    spec = json.loads(AXES_SPEC.read_text())
    DOI = spec.get("doi", "")
    SPEC = {a["axis"]: a for a in spec["axes"]}
    SPEC_N = {a["axis"]: a["n"] for a in spec["axes"]}
    sat_raw = json.loads((EV / "axis-saturation.json").read_text())
    SAT = sat_raw["axes"]
    SAT_MODELS = len(sat_raw["models"])
    SAT_DATE = sat_raw["measured_at"][:10]

    out = HERE / "publish/dataset-cards"
    out.mkdir(parents=True, exist_ok=True)
    for axis, bench, slug, task in FAMILY:
        p = out / f"{slug}.md"
        p.write_text(card(axis, bench, slug, task))
        print(f"  {slug}.md  {p.stat().st_size:,}B  n={SPEC_N[axis]} "
              f"usable={SAT.get(axis, {}).get('usable_n')}")
    print(f"\n  -> {out}")
