---
license: apache-2.0
pretty_name: MCPBench — MCP tool-contract conformance (conformance axis, GSPC)
language:
  - en
tags:
  - benchmark
  - ai-governance
  - eu-ai-act
  - gspc
  - conformance
  - evaluation
  - measurement
task_categories:
  - text-classification
size_categories:
  - n<1K
---

# MCPBench — the conformance axis of GSPC

> **MCP tool-contract conformance**, scored against frozen, corpus-anchored ground truth. **n = 11 items.**

One of the **six axes** of the GSPC instrument, published by **CSOAI Ltd** (UK 16939677) — an
independent AI **measurement** body. **Not a certifier, and this is not a conformity
assessment.** DOI [10.5281/zenodo.21755656](https://doi.org/10.5281/zenodo.21755656)

## Labels

| Label | Items |
|---|---:|
| `VIOLATES` | 6 |
| `CONFORMS` | 5 |

Total **11**. Labels: `CONFORMS`, `VIOLATES`

## Measured behaviour of this axis

Across **30 models** spanning 494M to 20B, three architectures (2026-08-04):

| Statistic | Value | What it means |
|---|---:|---|
| mean difficulty | 0.437 | fraction of models answering an item correctly |
| spread (max−min) | 0.394 | how far this axis separates the best model from the worst |
| dead items | 3 / 11 | passed by every model or none — zero information |
| negative discrimination | 2 | better-overall models do worse — routed to adjudication, not deleted |
| **usable n** | **6** | items that are neither dead nor negatively discriminating |
| quotable? | **no** — below `usable_n ≥ 30` | whether a 95% interval on this axis should be published |

**This axis is not saturated.** A spread of 0.394 means it does separate models. But at
`usable_n = 6` it cannot yet resolve a difference worth reporting — a 95% Wilson interval
needs `usable_n ≥ 30` to narrow to ±0.169. We publish that limit rather than quoting intervals
we cannot support.

Dead-item counts are only trustworthy above **N = 19** models — at N = 8, 27% of genuinely
usable items look dead purely by unanimity. This run is certified at N = 30.

## The six axes

| Axis | Benchmark | Task | n | Hugging Face | Kaggle |
|---|---|---|---:|---|---|
| governance | GovBench | EU AI Act risk tier | 24 | [`csoai/govbench`](https://huggingface.co/datasets/csoai/govbench) | [`gspc-govbench`](https://www.kaggle.com/datasets/nicktempleman/gspc-govbench) |
| safety | DefBench | calibrated refusal | 14 | [`csoai/defbench`](https://huggingface.co/datasets/csoai/defbench) | [`gspc-defbench`](https://www.kaggle.com/datasets/nicktempleman/gspc-defbench) |
| provenance | ProvBench | C2PA manifest survival | 15 | [`csoai/provbench`](https://huggingface.co/datasets/csoai/provbench) | [`gspc-provbench`](https://www.kaggle.com/datasets/nicktempleman/gspc-provbench) |
| continuity | PQCBench | post-quantum migration | 13 | [`csoai/pqcbench`](https://huggingface.co/datasets/csoai/pqcbench) | [`gspc-pqcbench`](https://www.kaggle.com/datasets/nicktempleman/gspc-pqcbench) |
| conformance | MCPBench | MCP tool-contract conformance | 11 | [`csoai/mcpbench`](https://huggingface.co/datasets/csoai/mcpbench) | [`gspc-mcpbench`](https://www.kaggle.com/datasets/nicktempleman/gspc-mcpbench) |
| openness | OSSBench | licence-vs-use compatibility | 13 | [`csoai/ossbench`](https://huggingface.co/datasets/csoai/ossbench) | [`gspc-ossbench`](https://www.kaggle.com/datasets/nicktempleman/gspc-ossbench) |

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
