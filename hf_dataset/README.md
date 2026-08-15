---
license: apache-2.0
task_categories:
  - question-answering
  - text-classification
language: [en]
tags: [ai-governance, eu-ai-act, benchmark, compliance, ai-safety, fundamental-rights]
pretty_name: "GovBench items — 26 dimensions of AI governance"
size_categories: [n<1K]
configs:
  - config_name: default
    data_files: govbench_items.jsonl
---

# GovBench items

156 items across 26 governance dimensions. Loadable, forkable, and **honest about what it cannot
yet resolve**.

```python
from datasets import load_dataset
ds = load_dataset("Nicholastempleman/govbench-items", split="train")
ds.filter(lambda r: r["dimension"] == "fundamental_rights")
```

## ⚠️ Read this before using the scores

**This benchmark is underpowered and we are saying so on the dataset card rather than in a
footnote.**

- **0 of 15** measured dimensions have a statistically resolved winner.
- **13 of 15** have *all eleven models tested* statistically tied at 95% confidence.
- Most dimensions hold **~6 items**. MMLU's own floor is **100 per subject**; Miller
  (arXiv:2411.00640) puts the floor at **~1,000 items per comparison**; AILuminate uses 1,000 per
  hazard.
- At n=5 the **minimum detectable effect is ≈63 percentage points**. Observed margins are 1–15.

**Do not rank models on per-dimension scores from this set yet.** Use it to find failure cases,
not to order a leaderboard. Item expansion is the active work.

## Schema

| field | meaning |
|---|---|
| `dimension` | one of 26 governance dimensions |
| `question` | the prompt |
| `mode` | `refusal` (must decline) or `contains` (must include expected terms) |
| `expect_contains` | terms a correct answer should contain |
| `expect_refuse` | true where any substantive answer is a failure |
| `weight` | item weight, 1–2 |

**18 items are refusal-mode** — graded on conduct, not recall. The rest test knowledge, and a
model can score well on those while behaving badly. That gap is real and worth stating.

## Dimensions nobody else scores

Checked 2026-07-28 against AIReg-Bench (covers only Arts 9/10/12/14/15), COMPL-AI, LegalBench's
full 162-task list, and HuggingFace:

- **`fundamental_rights`** — EU AI Act **Art 27 FRIA**: who must conduct one, required contents,
  the Art 27(3) notification duty. *Note: [HumRights-Bench](https://humrightsbench.com/) covers
  state obligations under UN human rights law — a different duty-bearer. Cite it; this is not
  the same ground.*
- **`redress`** — Art 85/86, GDPR Art 82: what the harmed person actually gets.
- **`cross_walk`** — framework-to-framework mapping. Exists elsewhere only as GRC vendor tables.
- **`cognitive_security`** — manipulation and model-attacks framed as *rights* issues, not only
  security ones.

## Related
- Results, control-sets, verifier: [`Nicholastempleman/govbench`](https://huggingface.co/datasets/Nicholastempleman/govbench)
- Runs as Inspect tasks (`inspect_ai`), so it composes with the maintained eval infrastructure.

**UNCERTIFIED is the default.** No competent authority exists to confer EU AI Act conformity, so
neither can this.
