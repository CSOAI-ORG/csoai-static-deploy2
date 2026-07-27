# SOV8 GPU BUDGET PLAN — $100/10 Days

## FREE RESOURCES (24/7)

| Resource | GPU/CPU | Cost | What Runs |
|----------|---------|------|-----------|
| **Oracle ARM** | 2 CPU, 956MB RAM | $0 | Data hub, cron, lightweight monitoring |
| **Kaggle T4** | T4 16GB VRAM | $0 (30h/wk) | LoRA training, benchmarks, EAT cycles |
| **Groq API** | llama-3.3-70b | $0 (100K tok/day) | Distillation, critic, grading |
| **NVIDIA API** | llama-3.1-8b | $0 (1000 calls/day) | Backup inference |
| **HF Spaces** | 2 CPU, 16GB RAM | $0 | Web demos, API endpoints |
| **Local Ollama** | MacBook M4 | $0 | Development, testing |

**Free capacity:** ~4h/day GPU (Kaggle) + unlimited CPU (Oracle) + unlimited API (Groq/NVIDIA)

## PAID RESOURCES (On-Demand)

| Resource | GPU | $/hr | When to Use |
|----------|-----|------|-------------|
| **RunPod A40** | A40 46GB | $0.44 | Heavy inference, 7B+ models |
| **RunPod 3090** | RTX 3090 24GB | $0.22 | Training, benchmarking |
| **RunPod H100** | H100 81GB | $2.99 | Only for 32B+ training |

## BUDGET: $100 / 10 Days = $10/day

### Daily Schedule

```
HOUR    FREE                    PAID ($10/day budget)
────    ────                    ─────────────────────
00-04   Oracle: EAT cycles      —
04-08   Kaggle: LoRA training   —
08-12   Groq: distillation      RunPod A40: inference ($0.44×4=$1.76)
12-16   Oracle: benchmarks      —
16-20   Kaggle: evaluation      RunPod 3090: training ($0.22×4=$0.88)
20-24   Oracle: monitoring      —
                                DAILY TOTAL: $2.64
```

### 10-Day Breakdown

| Day | Free Work | Paid Work | Cost | Cumulative |
|-----|-----------|-----------|------|------------|
| 1 | Oracle sync, Kaggle train | A40: inference test | $2.64 | $2.64 |
| 2 | EAT cycles, Groq distill | A40: LoRA training | $3.08 | $5.72 |
| 3 | Benchmarks, compliance | 3090: benchmark suite | $1.76 | $7.48 |
| 4 | Kaggle: reasoning eval | A40: model merge | $2.20 | $9.68 |
| 5 | GovBench testing | A40: 7B inference | $2.64 | $12.32 |
| 6 | EAT cycles, distill | 3090: fine-tuning | $1.76 | $14.08 |
| 7 | Competition prep | A40: full benchmark | $3.08 | $17.16 |
| 8 | Kaggle: final training | A40: inference | $2.64 | $19.80 |
| 9 | GovBench submission | 3090: training | $1.76 | $21.56 |
| 10 | Final eval, submit | A40: production test | $2.64 | $24.20 |
| **TOTAL** | | | | **$24.20** |

**REMAINING: $75.80** for emergencies, competitions, scaling.

## MODEL PLACEMENT

```
FREE (24/7):
├─ Oracle: sov33-unified (0.4B) — always-on, lightweight
├─ Kaggle: Qwen2.5-3B + LoRA — training on T4
├─ Groq: llama-3.3-70b — distillation, critic
└─ HF Spaces: Demo endpoint

PAID (on-demand):
├─ A40 ($0.44/hr): sov5v2, sov6v2, Mistral-7B + LoRA
├─ 3090 ($0.22/hr): Training, benchmarking
└─ H100 ($2.99/hr): Only for 32B+ (rare)
```

## ROUTING TABLE

| Task Type | Route | Cost | Latency |
|-----------|-------|------|---------|
| Simple Q&A | Oracle (sov33-unified) | $0 | 3s |
| Reasoning | Kaggle (Qwen2.5-3B) | $0 | 5s |
| Complex reasoning | Groq (70b) | $0 | 2s |
| Training | Kaggle T4 | $0 | 4h |
| Heavy inference | RunPod A40 | $0.44/hr | 1s |
| Benchmarking | RunPod 3090 | $0.22/hr | varies |
| 32B+ training | RunPod H100 | $2.99/hr | varies |

## WHAT WE CAN RUN 24/7 ON FREE

1. **sov33-unified (0.4B)** on Oracle — always-on, handles 80% of tasks
2. **Groq 70b** — unlimited distillation, critic, grading
3. **NVIDIA 8b** — backup inference
4. **Kaggle T4** — 4h/day training + evaluation
5. **EAT cycles** — continuous on Oracle (CPU only)
6. **GovBench** — compliance testing on Oracle (CPU only)
7. **Stigmergy** — pheromone trails on Oracle (file-based)

## WHAT NEEDS PAID GPU

1. **7B+ model inference** — A40 ($0.44/hr)
2. **LoRA training on 7B+** — A40 or 3090
3. **Full benchmark suite** — 3090 ($0.22/hr)
4. **32B+ models** — H100 ($2.99/hr, rare)

## STRATEGY

1. **Free first:** Route everything through free resources
2. **Paid only when needed:** A40 for heavy lifting, 2-4hr/day max
3. **Budget reserve:** Keep $75 for competitions and emergencies
4. **Auto-scaling:** If free tier hits limit, spin up A40 for 1hr ($0.44)
5. **Competition mode:** When submitting, use A40 for full benchmarks

## TOTAL COST FOR FULL SOV SYSTEM

| Component | Resource | Monthly Cost |
|-----------|----------|-------------|
| Always-on inference | Oracle (sov33-unified) | $0 |
| Training | Kaggle T4 | $0 |
| Distillation | Groq API | $0 |
| Heavy inference | RunPod A40 (2h/day) | $26.40/mo |
| Benchmarks | RunPod 3090 (1h/day) | $6.60/mo |
| **TOTAL** | | **$33/mo** |

**With $100 budget: Run full SOV for 3 months.**
