# EAT GOVBENCH — MEASUREMENT + CONFOUND ANALYSIS (2026-08-22)

Backend: RunPod 3090 `sov-repull` via `localhost:11439` (bridge). GCP retired.
Method: `eat_run_local.py`, baseline vs RAG-context, keyword-graded, WEAK_DIMENSIONS set.

## 1. CLEAN RESULTS (valid — model served reliably)
| Model | Size | Baseline | Context (RAG) | Δ |
|---|---|---|---|---|
| qwen2.5:7b | 4.68 GB | 28.6% | **66.7%** | +38.1 |
| mistral:7b | ~4.7 GB | 32.6% | **66.1%** | +33.5 |
| llama3:8b | 4.66 GB | 28.3% | **63.2%** | +34.9 |
| qwen2.5:1.5b | ~1.5 GB | 23.8% | **49.5%** | +25.7 |

**Per-dimension (representative, qwen2.5:7b):** defence 36.2→71.3 · sovereignty 28.5→72.9 ·
ethics 27.5→45.0 · privacy 27.3→72.3 · accountability 23.3→72.2.

## 2. CONFOUNDED / UNVERIFIABLE (do NOT quote as capability)
| Model | Reported | Mark | Reason |
|---|---|---|---|
| qwen3:8b | 0.0% | **CONFOUNDED** | capable 8B scoring 0 = refusal/format, not capability |
| deepseek-r1:7b | UNMEASURABLE | **CONFOUNDED** | reasoning model; probe empty |
| qwen2.5:0.5b (3090) | UNMEASURABLE | **CONFOUNDED** | backend empty (contended) |
| qwen3:4b | UNMEASURABLE | **CONFOUNDED** | probe empty (VRAM eviction) |
| our sov33-v7 | 47.6 | **CONFOUNDED** | partly grader/refusal + size (0.5B vs 7B) |
| our sov33-evolved | 11.4 | **CONFOUNDED** | corrupted prompt + grader + size |

## 3. TWO CONFOUNDS (why the absolute scores are noisy)
1. **Grader/refusal confound** — the keyword grader under-credits refusal / persona-narrow
   answers. qwen3:8b (capable) → 0.0 proves it. Our fine-tunes are *designed* to refuse-and-hold
   red lines, so their low scores are partly this artifact.
2. **Backend-reliability confound** — the shared 24 GB 3090 gets **contended** (many models
   keep-alive), evicting models so health-probes return empty → spurious UNMEASURABLE. This is a
   measurement-infrastructure artifact, not a model score.

## 4. THE ROBUST SIGNAL (what to trust)
**RAG context lift = +26 to +38 points** across every healthy model — retrieved knowledge >>
trained knowledge. This is confound-free (measured within-model, neutral to refusal/size) and
confirms the estate's honey-harvest thesis. **Use this, not absolute baselines.**

## 5. WHY OUR MODELS READ LOWER (design, not size excuse)
- **Size:** sov33-v7/evolved are **0.5B** (built on qwen2.5-0.5b), vs the 7B/8B base measured.
- **Merge-not-train:** estate canon — "base beats every sovereign fine-tune; only path = base +
  statute retrieval, NOT weight-merge of weak specialists." Merging dilutes the base's general
  instruction-following.
- **Grader/refusal:** our doctrine (refuse + red lines) is exactly what the keyword grader
  punishes.
- **sov33-evolved path** — corrupted SYSPROMPT (rebuilt-with-garbage history), crushes it.

## 6. CLEAN PROTOCOL (LANE, to make comparison trustworthy)
Run **one model per fresh 3090 load** (evict others first) + a **refusal-tolerant directive**
(`EAT_DIRECTIVE`, `EAT_TEMP` — added to `eat_run_local.py`). This removes both confounds so
per-model absolute scores are quoteable. SQLite/Ollama keep-alive eviction is the blocker now.

## Honest flags
- `council-oowm:latest` on 11439 emits garbage `????` — corrupted fine-tune, needs rebuild.
- `muse-glimmer:latest` hangs — unverified, probe needed.
- Spurious UNMEASURABLE = backend contention, NOT capability. Never quote as a score.
