# IMPROVE OUR OWN MODELS — measurement + plan (2026-08-22)

Date: 2026-08-22 · lane: K3 (measurement) / LANE (training) · directive: improve OUR models, not the base.

## 1. WHERE our models live (confirmed)
- **Oracle micro1 `11436`** — the 150+ sovereign fleet: sov33-v7/evolved/unified, sov-sovereign-v4,
  clan-* (sovereignty/redress/law/meok/defoneos/csoai × 10 variants), sov-draw-*, sov-* (100+).
- **3090 workhorse `11439`** — only `council-oowm` (CORRUPTED) + `muse-glimmer` (HANGS).
- **Oracle micro2 `11437`** — `sov33-ultimate-sovereign`.

## 2. MEASUREMENT (ours vs base)
| Model | baseline → RAG | Δ |
|---|---|---|
| **Base qwen2.5:7b** | 28.6 → **66.7** | +38.1 |
| **Base mistral:7b** | 32.6 → **66.1** | +33.5 |
| **Base llama3:8b** | 28.3 → **63.2** | +34.9 |
| sov33-v7 | 16.6 → 47.6 | +31.0 |
| sov-sovereign-v4 | 16.6 → 47.6 | +31.0 |
| **sov33-evolved** | **3.3 → 11.4** | +8.1 (weakest) |

**Verdict (estate's own thesis, now measured):** base > our fine-tunes on the weak governance
dimensions. The flywheel note is confirmed — "base Qwen2.5-0.5B beats every sovereign fine-tune."
RAG/retrieval is worth **+31–38 pts across the board**; retrieval >> weight-merge.

## 3. WHY (diagnosis)
1. **sov33-evolved (11.4) is effectively a weak proxy** — SYSPROMPT corruption history (EAT_STATUS:
   "rebuilt AGAIN", garbage tokens) + overlap collapse. Prime improve target.
2. **council-oowm** emits garbage `????` (corrupted fine-tune) → rebuild from a clean base.
3. **muse-glimmer** hangs → unverified, probe needed.
4. **Fleet on the ARM micro is too slow to train/measure fast** (E2.micro; EAT probe timed out at 60s).

## 4. IMPROVEMENT PLAN (ranked)
1. **Move the fleet to the 3090 workhorse** (`11439`) so it's measurably + trainable at speed. [LANE/pod]
2. **Rebuild council-oowm** from a clean base + re-merge honey. [LANE]
3. **honey-harvest injection** — the +31–38 RAG lever: ingest the 94K-row honey (already mined) into
   the weak fine-tunes' retrieval; sov33-evolved is the #1 target. This IS the training (estate thesis).
4. **Retrain sov33-evolved** with a clean SYSPROMPT + statute-retrieval (not weight-merge of weak
   specialists — the estate's documented path).
5. **Re-measure on the 3090** after each rebuild — the RAG/baseline gap is the success signal.

## 5. Honest gate
Model move/rebuild + training = LANE/pod (needs RunPod SSH/`ollama pull`). Measurement + the
improvement plan = done here. No fabricated scores: council-oowm/muse-glimmer remain UNMEASURABLE
(corrupt/hang) until rebuilt.
