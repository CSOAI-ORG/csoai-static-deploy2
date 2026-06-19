# Sovereign Town — Free-Compute Dispatch (the data-moat engine, global scale)

_How the P1 batch engine fans across free compute worldwide to build the cross-hive data moat.
Honest about what runs where, and ToS-clean. Pairs with `FREE_COMPUTE_APPLICATIONS_2026-06-16.md`._

## The honest architecture: two tiers, two kinds of compute
The phrase "eat all free GPU" is half right. The work splits cleanly:

| Tier | Work | Compute | Bound by | Where (free) |
|---|---|---|---|---|
| **Sim tier** | generate governed-vs-ungoverned episodes (`batch.py`) | **CPU, embarrassingly parallel** | cores | GitHub Actions · Colab · Kaggle · HF Spaces · free VMs |
| **Train tier** | per-hive sovereign models from the corpus (`train_all_hives.py`) | **GPU** | VRAM/hours | RunPod · Vast.ai · the ~$920K credit stack (NVIDIA/DO/MS/Google) |

The sim is **pure stdlib, CPU-only, ~750K episodes/sec/10-cores** — it does NOT need GPU. GPU is for turning
the harvested corpus into models. So we eat **free CPU** for data and **free GPU** for training.

## The unit of work
`batch.py` IS the portable worker — stdlib-only, runs anywhere Python runs. Slice the job space by
`(districts × seed-range × contagion)`; each free worker runs a seed-slice and emits a corpus shard.
Aggregate shards centrally (on the GCP VM), Ed25519-attest the merged corpus (proofof.ai), then train.

```
  dispatch:  for worker_k in free_workers:  run batch.py on seeds[k*S:(k+1)*S]  -> corpus_shard_k.json
  collect:   rsync/artifact shards -> VM -> merge -> sign (sign_lib) -> corpus_vN.jsonl
  train:     train_all_hives.py on GPU worker -> models/<hive>_threat_nn.pkl  (per hive)
  deploy:    swap retrained care/threat NN back into SOV3 (fixes the degenerate prod model)
```

## Free CPU tiers (the sim flood) — ToS-clean
- **GitHub Actions** ⭐ — the killer one: free minutes + **up to ~20 concurrent runners**, and it's literally CI
  (running our own test/sim matrix). A nightly matrix job = hundreds of free sim-hours/day, fully within ToS.
- **Google Colab / Kaggle** — free CPU sessions (Kaggle ~30h/wk); drop `sim.py`+`batch.py`, run a seed-slice.
- **HF Spaces (CPU)** — a scheduled Space that runs a slice and pushes shards to a dataset repo.
- **Free-tier micro-VMs** (Oracle Always-Free, GCP e2-micro) — long-running low-core workers.

## Free GPU tiers (the train flood)
- **RunPod serverless** — `runpod_train_handler.py` already exists (Unsloth/LoRA). Bursty per-hive training.
- **Vast.ai** — `vast_create_instance.sh` already exists. Cheapest spot GPU.
- **The ~$920K credit stack** — NVIDIA Inception / DigitalOcean Hatch / MS Founders Hub / Google Cloud
  (per FREE_COMPUTE_APPLICATIONS; 7–10-day approval lag — apply now, they fund the train tier).
- **Groq / Cerebras / Colab T4 / HF ZeroGPU** — free inference for the LLM-driven-agent variant (P2).

## ToS discipline (non-negotiable — we're the *governed* ones)
- One account per provider. **No multi-account farming.** Respect rate limits + fair-use.
- GitHub Actions usage = genuine CI of our own simulation matrix (it is). Colab/Kaggle = research sessions.
- Credits are **claimed, not gamed.** This posture is itself part of the brand.

## The moat math (honest)
30 hives × distinct economic profiles × seeds × contagion × free workers → **millions of labelled,
Ed25519-attested governed-behaviour episodes** → **30 per-hive sovereign models** (care/threat/relationship)
nobody else can reproduce, because nobody else has the governed verticals or the data. Per the DATA_MOAT
dossier this is the defensible asset (IP + data optionality), not current revenue.

## 3-tier compute (Kimi v3) — the LLM-agent inference layer, and the deepest "free GPU" unlock
When agents are LLM-driven (P2), route by complexity — and Tier-1 runs on the **user's own GPU**:
- **Tier 1 ($0, the moat):** Qwen3-4B (ECLD-distilled) via **Transformers.js v3 WebGPU IN THE BROWSER** —
  ~80% of agent queries, 25–40 tok/s, <500MB. The *spectator's* GPU pays the inference. This is the literal
  "eat free GPU globally" at inference time: every viewer/participant donates compute by watching.
- **Tier 2 (cheap/regional):** Cloudflare Workers AI (8B, 20–50ms) on Durable Objects — ~15% coordination.
- **Tier 3 (paid, rare):** Opus/GPT-5.5 via OpenRouter — ~5% sovereign decisions. Routing variance = free
  agent personality.

## Fine-tune toolchain (the train tier — turns the corpus into the moat models)
- **Unsloth + DoRA** per-hive/caste adapters (+3–4% over LoRA, zero inference overhead).
- **KTO** — trains on our **binary gate/pheromone/attestation signals directly** (already emitted; no new labels).
- **GRPO → M-GRPO** — hierarchical King→Queen→Worker credit assignment.
- **Distilabel** synthetic preference pairs (teacher = Opus); **Mem0 + Zep/Graphiti** temporal-KG memory.
- **Serving:** vLLM + **S-LoRA** (2,000 adapters/GPU — one per hive) + **KVCOMM** shared-context (7.8×).
- Runs on the GPU credit stack (RunPod/Vast/$920K). This is what the free GPU actually trains.

## Status (P1, 2026-06-19)
- ✅ `sim.py` district-parameterized (4 hives wired; trivially extends to all 30 via `DISTRICTS`).
- ✅ `batch.py` — 483,840 episodes / 0.7s / 10 cores; distinct per-hive corpora.
- ✅ `train_all_hives.py` — 4 per-hive models, 0.989 acc each, saved to `models/`.
- ⏭️ Next: GitHub Actions sim-matrix workflow; shard merge+sign on VM; extend DISTRICTS 4→30;
  wire retrained NN back into SOV3 (fixes the degenerate prod care model).
