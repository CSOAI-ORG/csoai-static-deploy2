# SOVOS Goal → Router + Top-Tier + Fusion/TTT — learned & measured (2026-08-22)

## The SOVOS goal (learned from Desktop/`_alignment` docs)
**One governed emergence model = 1 large core brain + 3 specialist students routed around it, under
ONE care-gate + ONE signature + ONE memory.** "Emergence" = the governed DECISION from
route→vote→care-gate→sign. NOT a monolithic giant. "Fusion" = **multi-teacher distillation**
(giants teach → we own the weights) + **output-ensemble routing**. Sources:
`_alignment/MASTER_PLAN_FUSION_OWEM.md`, `_alignment/MODEL_FUSION_PLAYBOOK_2026-07-14.md`,
`_alignment/EAT725_OWEM_FUSION_PLAYBOOK_2026-07-15.md`.

### What the playbook VERIFIED (don't re-litigate)
- **RAG exceeds best parent** — measured **84.2% vs 78.9%** (EAT-725, 6 approaches). The real lever.
- **Weight-merging does NOT reliably beat best parent** (REFUTED). Use Task-Arithmetic only if merging.
- **Output-fusion (MoA) + routing (RouteLLM)** = the fluid path; **routing → >2× cost cut, ~95% quality**.
- **TTT** (`realpde-track2/train_ttt.py`) = sim-pretrain → real-finetune for the LTTTA streaming surrogate.

## Router should route to the BEST (confirmed by measurement)
The "large core" is a **funded frontier model**. Frontier status this session:
| Provider | Status | MMLU (0-shot, N=65) |
|---|---|---|
| **DeepSeek (`deepseek-chat`)** | ✅ funded, works | **78.5%** |
| OpenRouter (`qwen3.7-max`) | ❌ 402 no credits | — (UNMEASURED) |
| Anthropic (Claude) | ❌ 401 bad key | — (UNMEASURED) |
| Local OOWM (`council-oowm`) | ✅ runpod-a100 | 41.5% |
| `sov33-ultimate-sovereign` | ✅ | 38.5% |
| `council-oowm-hardened` | ✅ | 36.9% |

**Conclusion:** general-capability queries should **route to DeepSeek (78.5%)** as the large core; the
sovereign OOWM + `dorado_gate` + `law_kb` RAG is the **governance/safety/refusal specialist** (GOVBENCH
0.931, DEFBENCH refusal 1.000). That IS the 1-large-core + specialists governed router the SOVOS goal
describes. Router should prefer a funded frontier for breadth, and the care-gated sovereign for governance.

## Honest caveats
- `deepseek-v4-flash` 0% = invalid model id / API error → UNMEASURED, not 0.
- **MuCoCo** (code-LLM consistency) not run — needs its specific data/harness; I ran the main multitask
  **MMLU** as the representative standard benchmark. Say the word to set up MuCoCo.
- **sov-light OOWM** = `council-oowm`/`council-oowm-hardened` on the runpod-a100 (`sovos-light-a100` pod);
  no separate "sov-light" model found on disk.
- Artifacts: `mmlu_eval.py`, `mmlu_eval_or.py`, `benchmark-results/mmlu_{bounded,frontier}.json`,
  `OOWM_VS_TOPTIER_MMLU_2026-08-22.md`.
