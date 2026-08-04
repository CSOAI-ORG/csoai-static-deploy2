---
license: apache-2.0
task_categories: [text-classification]
language: [en]
tags: [ai-governance, eu-ai-act, benchmark, csoai, gspc, provenance]
size_categories: [n<1K]
---

# ProvBench — Article 50 marking survival

**Axis: provenance** — one of the six axes of the CSOAI GSPC instrument.
By [CSOAI](https://csoai.org), the Council for the Safety of AI (UK).

Given an operation on a file carrying a C2PA manifest, does the provenance marking still verify?

## Grading is deterministic

A regex reads the answer token and an equality check decides. **No model judges another
model**, so the same answer always scores the same and the scoring rule is auditable by
anyone reading it. A model that declines to answer is scored **wrong, not skipped** —
dropping refusals would shrink the denominator and flatter the model.

## Not gameable by a single constant answer

| Answer | Count | Always-answer score |
|---|---|---|
| `DESTROYED` | 8 | 53% |
| `SURVIVES` | 7 | 47% |

Best single-answer strategy: **8/15 = 53%**. The item set is deliberately
spread, and includes cases that look like one answer but are the other. This property is
asserted offline in the task source, so a future edit that skews the set fails loudly
rather than quietly inflating the board.

## Fields

- `operation` — the item
- `expected` — ground truth
- `anchor` — the statute, standard or physical fact that makes the answer defensible.
  Argue with a label by arguing with its anchor.
- `axis` — `provenance`

## Honest scope

15 items. This is a focused instrument, not a complete conformity assessment, and it does
not by itself establish compliance with any regulation.

## Live leaderboard

Runs against frontier models on
[Kaggle Benchmarks](https://www.kaggle.com/benchmarks/tasks/nicktempleman).

## Citation

```bibtex
@misc{csoai_provenance_2026,
  title  = {ProvBench — Article 50 marking survival},
  author = {Templeman, Nicholas},
  year   = {2026},
  url    = {https://csoai.org}
}
```
