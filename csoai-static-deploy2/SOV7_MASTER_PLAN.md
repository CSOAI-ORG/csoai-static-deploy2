# SOV7 MASTER PLAN — Full Absorption & Unified Direction
**Date:** 2026-07-26 | **Status:** ACTIVE

---

## WHERE WE ARE NOW

### RunPod State
- **GPU:** NVIDIA A40 (46GB VRAM), 3.5GB used, idle
- **Models:** sov7, sov5v2, sov6v2, qwen2.5:3b/1.5b/0.5b, llava:7b, llama3.2-vision:11b
- **Adapters:** defense OWEM trained (1200 steps)
- **Training data:** 4,559 rows across 10 clan datasets
- **Cloudflare:** 753 HTML pages live at c3fce85a.csoai-sovereign.pages.dev

### Benchmark Scores
| Model | Standard | Sovereign | GAIA | Combined |
|-------|----------|-----------|------|----------|
| sov5v2 | 95% | 50% | 90% | 70% |
| sov6v2 | 85% | 60% | 90% | 75% |
| sov7 | 0% | 20% | - | 10% |
| qwen2.5:3b | 95% | 0% | - | 40% |

### Problem
**sov7 is WORSE than both sov5v2 and sov6v2.** The merged system prompt is too long and confuses the model. We have 8+ models but none is the clear winner.

---

## THE KIMI RESEARCH INSIGHT

From the Kimi OWEM Architecture Deep Dive (34 rounds of research):

### Clan Bloodlines (from Research Dimension 4)
The research recommends a **5-clan voting system** with decorrelated architectures:
1. **Dense anchor** (Qwen3.5-4B) — quality baseline
2. **Hybrid SSM** (Zamba2-7B) — Mamba2 + attention
3. **Pure RNN** (RWKV-7-G1-2.9B) — zero attention
4. **Diffusion LM** (Dream-7B) — non-autoregressive
5. **Linear attention** (Kimi-Linear-48B-A3B) — delta-rule

**Key insight:** These 5 architectures have provably different failure modes. Voting across all 5 is more robust than training one perfect model.

### The Real Answer
**Don't merge into one model. Build a voting ensemble of 5 decorrelated models.**

---

## THE UNIFIED STRATEGY

### Phase 1: Fix SOV7 (Today)
1. **Slim the system prompt** — SOV7's prompt is too long. Cut to 500 tokens max.
2. **Test against sov5v2/sov6v2** — If still worse, revert to using sov5v2+sov6v2 as the working pair.
3. **Stop training individual OWEMs** — The defense adapter is done. Stop burning GPU on training.

### Phase 2: Deploy Working Models (Today)
1. **Keep sov5v2 and sov6v2** — These are the best models (95% and 85% standard)
2. **Deploy to Cloudflare** — The site is live, add custom domain
3. **Set up inference endpoint** — Expose sov5v2/sov6v2 via RunPod API

### Phase 3: Leaderboard Submission (Tomorrow)
1. **Run full benchmark suite** — MMLU, GSM8K, HumanEval, IFEval, ARC
2. **Submit to Open LLM Leaderboard** — HuggingFace
3. **Submit to LMArena** — Chatbot Arena
4. **Publish results** — govbench.html, HF model cards

### Phase 4: Agent Loop (This Week)
1. **Deploy sov33_agent_loop.py** — Already built, needs testing
2. **Run GAIA benchmark** — sov5v2 scored 90%, sov6v2 scored 90%
3. **Run SWE-bench** — Code generation benchmark
4. **Set up HF/Kaggle evaluation** — Submit to real leaderboards

### Phase 5: Consolidation (Next Week)
1. **Pick the winner** — sov5v2 (best standard) vs sov6v2 (best sovereign)
2. **Create final Modelfile** — Merge best system prompts
3. **Deploy to production** — Single model for all inference
4. **Archive the rest** — Keep as reference, stop running

---

## WHAT WE DON'T NEED TO DO

| Don't Do | Why |
|----------|-----|
| Train more OWEM adapters | Defense is done, others aren't needed |
| Build more Modelfiles | We have 30+ variants, pick the best 2 |
| Run 5 different models | Pick sov5v2 or sov6v2, deploy one |
| Implement full agent loop | GAIA 90% is already competitive |
| Build 5-clan voting system | Too complex for now, single model is fine |

---

## WHAT WE DO NEED TO DO

| Do This | Priority | Time |
|---------|----------|------|
| Fix SOV7 system prompt (slim it) | HIGH | 30 min |
| Deploy sov5v2 to Cloudflare | HIGH | 1 hour |
| Run full benchmark suite | HIGH | 2 hours |
| Submit to leaderboard | HIGH | 1 hour |
| Set up inference API | MEDIUM | 2 hours |
| Publish results | MEDIUM | 1 hour |

---

## THE ONE-LINE ANSWER

**Yes, consolidate into one model. sov5v2 is the winner (95% standard, 90% GAIA, 70% combined). Deploy it. Stop training. Move to leaderboards.**
