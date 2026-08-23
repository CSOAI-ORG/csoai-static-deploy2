# Scale the Free OWEM Bootstrap to N Sites — 2026-08-23

**Question:** can we bootstrap free OWEM/OOWM compute + data across many
free-GPU/CPU sites instead of renting one GPU / paying OpenRouter credits?

**Answer:** YES — and the estate already has the plumbing. Ground truth:
- **Kaggle API** configured (`~/.kaggle/kaggle.json`, user `nicktempleman`),
  with **OOWM ground-truth datasets v3/v7/v9** already published.
- **Oracle always-free** micros (2 cores each, free) reachable.
- **HF hub** + **gcloud/colab tokens** present.
- Estates **14-model free fleet** on the A100.

---

## The sites (N scalable), free compute + free data

| Site | Free GPU/CPU | Free data | Role in OWEM bootstrap |
|------|--------------|-----------|------------------------|
| **Kaggle** | T4 x1 (free, 30h/wk quota) | its datasets + your uploaded corpus | **primary free GPU** — fine-tune + eval |
| **HuggingFace Spaces** | free CPU-zero/small GPU | HF datasets (MMLU/GPQA/etc.) | experiment + inference API |
| **Colab** | T4/L4 free (limited) | drive + HF | ad-hoc fine-tune backups |
| **Oracle always-free** | 2× micro ARM/x86 (free) | self-hosted | **long-running inference + RAG** (the router gateway) |
| **A100 pod** | (paid) | full fleet | NOT free — keep only for the 30B/14B specialists |
| **Our 14-model fleet** | on A100 | our mined cards | **the sovereign specialists** the router routes to |

## The scaling architecture (N sites, one OWEM router)

```
                    ┌────────────── OWEM / OOWM ROUTER ──────────────┐
   query ──────────▶│  task → pick site+model by (quality,cost,lat)  │
                    └──────┬──────────────────────────────────┬──────┘
                           │ (free, sovereignty-prioritized)  │
        ┌──────────────────┼──────────────────┐              │
   Kaggle T4          Oracle free          HF Spaces        A100(fleet)
   (train+eval)       (long-run RAG+inf)    (experiments)   (30B/14B specialists)
        └────────── all free except A100 ──────────┘
```

- **Train** the sovereign models on **Kaggle T4** (free, 30h/wk quota).
- **Serve/RAG** on **Oracle always-free** (free, always-on — the domain gateway's home).
- **Eval/benchmark** on **Kaggle + HF** (free data: MMLU/GPQA).
- **Keep A100 only for the big-tier specialists** it's actually best at.
- **Route** across all via `route_planner` (warmth-aware, sovereignty-prioritized).

## Why this scales
- **Per-site free quota** (Kaggle 30h/wk, Colab limited, Oracle always-on, HF free) =
  aggregate ~40h/wk free GPU + always-on free CPU. Enough to train/eval our
  sovereign models without renting a GPU or paying OpenRouter.
- **Free data is the multiplier** — Kaggle/HF have the benchmarks (MMLU/GPQA)
  and we have our own mined corpus. No paid data.
- **The router already composes sites** (warmth-aware, sovereignty prior) — we
  just add each free site as a provider with its cost=0.

## Honest constraints (real, not hidden)
1. **Kaggle free GPU quota** (limited h/wk) — fine for small sovereign LoRAs,
   not massive pre-training. Our models are 0.5-7B LoRAs → fits comfortably.
2. **Colab free is rate-limited** — fine as backup, not primary.
3. **Oracle always-free is CPU-only** (2 cores) — good for RAG/inference, not
   training (use Kaggle T4 for training).
4. **Licensing** — MMLU/GPQA are open-license (legit free data). Kaggle datasets
   we upload are CC0. **We do not scrape proprietary APIs**; we use open datasets
   + our own corpus. (The estate already asserts its own IP/database rights.)
5. **Linkage** — the free sites must sync (corpus up, adapter back). Use
   Kaggle datasets + HF hub as the free transport.

## The N-site execution (what to do next, in order)
1. **Kaggle** → run `oowm_free_train.py` (kernel) — fine-tune on T4, free. ✅ kernel written.
2. **Oracle** → host the OWEM/domain gateway (RAG + inference), free always-on.
3. **HF** → mirror the corpus + adapter (free, extensible).
4. **Router** → add each free site as a provider (cost=0) so it routes across N.
5. **Aggregate** free-quota scheduler → run fine-tune/eval across the N sites'
   free windows, collect results back into the monorepo.

**Net:** the estate becomes an N-site free-grid for the sovereign OWEM — train
on Kaggle, serve on Oracle, eval on Kaggle+HF, route across all — **no paid GPU
merchant, no OpenRouter credits** for the core path. ✨
