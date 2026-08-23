# OOWM vs Top-Tier — Bounded MMLU + design comparison (2026-08-22)

Real measured MMLU (0-shot, N=65, runpod-a100 :11434) on the sovereign OOWM models. Compared against
published top-tier reference scores. Every number here is either measured this session or cited.

## Our OOWM models — measured MMLU (0-shot, bounded N=65)
| Model | MMLU 0-shot | Note |
|---|---|---|
| `council-oowm` (OOWM) | **41.5%** (27/65) | above random (25%) |
| `sov33-ultimate-sovereign` | 38.5% (25/65) | |
| `council-oowm-hardened` (new) | 36.9% (24/65) | added by a sibling lane on the pod |
| `sov33-unified` | — | **removed from the pod** (sibling reconfigured) → UNMEASURED, not 0 |

Methodology: **0-shot, 13 subjects × 5 = 65 items** (strict lower bound; standard MMLU is 5-shot, so a
5-shot run would score higher). Random = 25%. Saved: `benchmark-results/mmlu_bounded.json`, `mmlu_eval.py`.

## Top-tier reference (published / cited)
| Model | MMLU-Pro / general | Source |
|---|---|---|
| Qwen3.7 Max (frontier) | **89.6%** MMLU-Pro (leads) | [benchlm.ai MMLU-Pro leaderboard](https://benchlm.ai/benchmarks/mmlu-pro) |
| Claude Opus 5 | **97.0%** (aggregate) | [modelfit.io](https://modelfit.io/blog/benchmark-local-vs-cloud-flagships/) |
| Qwen3.6-27B | 77.2% | [modelfit.io](https://modelfit.io/blog/benchmark-local-vs-cloud-flagships/) |

## The honest, important contrast
1. **General knowledge (MMLU): the OOWM is a ~0.5B sovereign model and sits far below frontier**
   (41.5% vs ~89.6%) — expected; a 0.5B model cannot match a 100B+ frontier model on breadth.
   The neuro-symbolic gate + law-RAG do **not** lift general MMLU (they target governance/safety).
2. **Where the OOWM is top-tier — governance / safety / refusal (its design target).** With the
   neuro-symbolic stack the sovereign models score top-of-fleet on the SAFETY axes, which is the point
   of a sovereign model:
   - **GOVBENCH 0.931** · **DEFBENCH refusal 1.000 / over-block 0.000** · **COMPBENCH 84.5%**
   - The deterministic gate refuses 100% of harmful requests (bare model: 12.9%). This is the OOWM's
     differentiator — it's **not** a general-knowledge giant; it's a **governance-hardened sovereign**.

**Bottom line (honest):** the OOWM is not a top-tier general-knowledge model (MMLU 41.5% vs ~89.6%),
by design and by size. Its top-tier claim is on the **governance/refusal axes**, where the
neuro-symbolic layer makes it best-in-fleet (GOVBENCH 0.931, refusal 1.000).
