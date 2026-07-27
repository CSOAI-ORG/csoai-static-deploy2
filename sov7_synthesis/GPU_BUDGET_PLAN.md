# SOV7 GPU Budget Plan

**Budget:** $100 / 10 days = **$10.00/day**
**Generated:** 2026-07-27
**Goal:** Run OWEM Sandwich Brain (4 layers), 12 clan hives, BFT quorum, EAT cycles, LoRA training, Groq distillation, and GovBench compliance testing.

---

## 1. FREE Resources — Always Available ($0)

| Resource | Spec | Availability | Can Run 24/7? | Assigned Workloads |
|----------|------|-------------|---------------|-------------------|
| **MacBook M4 (local)** | CPU + 19 Ollama 0.4B models | 24/7 | YES | OWEM L1/L2 inference (0.4B), task decomposition, J-space card generation, stigmergic coordination, code editing, E2E tests |
| **Oracle ARM** | 2 CPU, 956MB RAM, 37GB disk | 24/7 (always-free) | YES | Data synthesis, corpus building, JSONL preprocessing, Groq distillation orchestration, cron jobs, lightweight scoring |
| **Kaggle T4** | T4 16GB VRAM | 30h/week (4.3h/day avg) | NO — budget hours | LoRA training (reasoning OWEM), benchmark runs, capability matrix eval, mergekit TIES merge |
| **Groq API** | llama-3.3-70b-versatile | 100K tokens/day | YES (rate-limited) | Distillation teacher (50 prompts/day → training data), heavy reasoning for C-space synthesis |
| **NVIDIA API** | Various models | 1,000 calls/day | YES (rate-limited) | Backup inference, cross-validation of Groq outputs |
| **HuggingFace Spaces** | 2 CPU, 16GB RAM | 24/7 | YES | Lightweight inference server, model card hosting, demo endpoint for submissions |
| **RunPod (EXITED)** | 20 pods — all stopped | On-demand | NO — $0 when off | Spin up ONLY for specific tasks below |

### Free Resource Capacity (24/7)

```
MacBook M4 (19 × 0.4B models):
  ├─ Inference throughput: ~15 queries/min (4-layer sandwich)
  ├─ Daily capacity: ~21,600 full OWEM pipeline runs
  ├─ Clan routing: 12 pillars × 1,728 families = all covered
  └─ BFT quorum (23/33): runs locally on 0.4B ensemble

Oracle ARM:
  ├─ Data preprocessing: ~50K JSONL rows/day
  ├─ Groq distillation orchestration: 50 prompts/day
  ├─ Score aggregation and leaderboard updates
  └─ Cron: EAT cycle scheduling, overnight runs

Kaggle T4 (30h/week):
  ├─ LoRA training: ~7 full runs/week (4h each)
  ├─ Benchmark suite: ~10 full evals/week (3h each)
  └─ TIES merge: ~2 merges/week (1.5h each)

Groq API (100K tokens/day):
  ├─ 70b distillation: ~50 prompts/day (avg 1500 tokens/prompt = 75K tokens)
  ├─ Remaining 25K tokens: C-space heavy synthesis
  └─ Fallback to 8b when 70b rate-limited

NVIDIA API (1000 calls/day):
  ├─ Cross-validation: ~200 calls/day
  ├─ Benchmark comparison: ~300 calls/day
  └─ Reserve: 500 calls/day for GovBench
```

---

## 2. PAID Resources — RunPod Pricing

| Pod Type | GPU | VRAM | Cost/hr | Cost/day (8h) | Cost/day (24h) | Best For |
|----------|-----|------|---------|---------------|----------------|----------|
| **RTX 3090** | RTX 3090 | 24GB | $0.22 | $1.76 | $5.28 | 7B-13B LoRA training, medium inference |
| **A40** | A40 | 46GB | $0.44 | $3.52 | $10.56 | 13B-32B training, large LoRA, mergekit |
| **H100** | H100 | 81GB | $2.99 | $23.92 | $71.76 | 32B+ inference, full fine-tune, competition |

**All 20 pods are currently EXITED — $0/hr when not running.**

---

## 3. $10/Day Budget Allocation

### Daily Budget Breakdown

```
$10.00/day total
├─ $0.00  Free resources (MacBook, Oracle, Kaggle, Groq, NVIDIA, HF Spaces)
├─ $6.60  RTX 3090 — 30h @ $0.22/hr (LoRA training, 7B-13B inference)
├─ $2.64  A40 — 6h @ $0.44/hr (mergekit, large model runs)
├─ $0.75  H100 — 0.25h @ $2.99/hr (competition submission, 32B+ burst)
└─ $0.01  Buffer / network egress
```

### What $10/Day Buys

| Resource | Hours/day | Daily Cost | What It Runs |
|----------|-----------|------------|-------------|
| RTX 3090 | 30h | $6.60 | LoRA training (reasoning OWEM, code OWEM), 7B-13B inference, benchmark sweeps |
| A40 | 6h | $2.64 | TIES model merge, 32B quantized inference, heavy eval suites |
| H100 | 0.25h (15 min) | $0.75 | Competition submission inference, 32B+ full-precision burst |
| **TOTAL** | **36.25h** | **$9.99** | |

### 10-Day Totals

| Resource | Total Hours | Total Cost | Deliverable |
|----------|-------------|------------|-------------|
| RTX 3090 | 300h | $66.00 | 75 LoRA training runs, full benchmark suite |
| A40 | 60h | $26.40 | 10 TIES merges, 32B eval sweeps |
| H100 | 2.5h | $7.50 | 5 competition submissions |
| **TOTAL** | **362.5h** | **$99.90** | |

---

## 4. Model Placement Table

### Where Each Model Runs

| Model | Size | Runs On | VRAM Needed | Cost | Notes |
|-------|------|---------|-------------|------|-------|
| qwen2.5:0.5b | 0.4B | MacBook (Ollama) | CPU | $0 | Frozen OWM — Layer 1 |
| sov33-unified (all variants) | 0.4B | MacBook (Ollama) | CPU | $0 | Fluid OWM — Layer 2 |
| sov33-evolved (all variants) | 0.4B | MacBook (Ollama) | CPU | $0 | Evolved model — Layer 4 |
| sov33-strong | 0.4B | MacBook (Ollama) | CPU | $0 | Strong variant — ensemble |
| Reasoning LoRA (trained) | 0.4B+adapter | MacBook (Ollama) | CPU | $0 | Post-training: load into Ollama |
| Groq llama-3.3-70b | 70B | Groq API | N/A | $0 | Distillation teacher, C-space |
| Groq llama-3.1-8b | 8B | Groq API | N/A | $0 | Fallback when 70b limited |
| Reasoning LoRA training | 0.4B | Kaggle T4 | 8GB | $0 | 4h per 100K samples |
| TIES merge (mergekit) | 0.4B×3 | RunPod A40 | 12GB | $0.44/h | Weight-level merge |
| 7B fine-tune (future) | 7B | RunPod 3090 | 18GB | $0.22/h | If we scale up |
| 13B inference (future) | 13B | RunPod 3090 | 22GB | $0.22/h | Competition eval |
| 32B+ inference | 32B+ | RunPod H100 | 65GB | $2.99/h | Burst only |
| GovBench compliance | 0.4B | MacBook + HF Spaces | CPU | $0 | Runs on free tier |
| OWEM Sandwich (full) | 0.4B×4 | MacBook (Ollama) | CPU | $0 | All 4 layers locally |
| BFT Quorum (23/33) | 0.4B×33 | MacBook (Ollama) | CPU | $0 | 33 parallel clan votes |

### Architecture-to-Hardware Mapping

```
OWEM SANDWICH BRAIN (4 layers):
┌─────────────────────────────────────────────────────────┐
│ Layer 1 (frozen OWM) → qwen2.5:0.5b    → MacBook $0   │
│ Layer 2 (fluid OWM)  → sov33-unified    → MacBook $0   │
│ Layer 3 (frozen IWM) → Reasoning cache  → MacBook $0   │
│ Layer 4 (fluid IWM)  → sov33-evolved    → MacBook $0   │
└─────────────────────────────────────────────────────────┘

CLAN HIVE (12 pillars):
┌─────────────────────────────────────────────────────────┐
│ All 12 clans → 0.4B models on MacBook $0               │
│ 144 clans → parallel ThreadPoolExecutor on MacBook $0  │
│ 1,728 families → fractal sub-clans on MacBook $0       │
└─────────────────────────────────────────────────────────┘

BFT QUORUM:
┌─────────────────────────────────────────────────────────┐
│ 33 voters → 0.4B models on MacBook $0                  │
│ 23/33 threshold → local consensus $0                   │
└─────────────────────────────────────────────────────────┘

STIGMERGIC COORDINATION:
┌─────────────────────────────────────────────────────────┐
│ J-space cards → MacBook $0                              │
│ Pheromone trails → MacBook $0                           │
│ Cross-pollination → MacBook $0                          │
└─────────────────────────────────────────────────────────┘

EAT CYCLES:
┌─────────────────────────────────────────────────────────┐
│ Evolve → Kaggle T4 (LoRA training) $0                  │
│ Absorb → Oracle ARM (data synthesis) $0                │
│ Transform → RunPod A40 (model merge) $0.44/h           │
└─────────────────────────────────────────────────────────┘

REASONING LORA TRAINING:
┌─────────────────────────────────────────────────────────┐
│ Dataset → Oracle ARM (preprocess) $0                    │
│ Training → Kaggle T4 (100K samples) $0                 │
│ Eval → MacBook (benchmark) $0                           │
│ Merge → RunPod A40 (TIES) $0.44/h                      │
└─────────────────────────────────────────────────────────┘

GROQ DISTILLATION:
┌─────────────────────────────────────────────────────────┐
│ Orchestrate → Oracle ARM $0                             │
│ API calls → Groq (100K tokens/day) $0                  │
│ Save JSONL → Oracle ARM $0                              │
│ Train on distilled → Kaggle T4 $0                      │
└─────────────────────────────────────────────────────────┘

GOVBENCH COMPLIANCE:
┌─────────────────────────────────────────────────────────┐
│ EU AI Act checks → eu-ai-act-compliance MCP $0         │
│ Model evaluation → MacBook $0                           │
│ Heavy eval → Kaggle T4 $0                               │
│ Report generation → Oracle ARM $0                       │
└─────────────────────────────────────────────────────────┘
```

---

## 5. What Runs 24/7 on Free Resources

| Component | Runs On | Uptime | Daily Capacity |
|-----------|---------|--------|----------------|
| OWEM Sandwich Brain (all 4 layers) | MacBook | 24/7 | 21,600 pipeline runs |
| 12 Clan Hives | MacBook | 24/7 | 259,200 clan tasks |
| BFT Quorum (23/33) | MacBook | 24/7 | 648,000 votes |
| Stigmergic coordination | MacBook | 24/7 | Unlimited J-space cards |
| Task decomposition | MacBook | 24/7 | 1,440 tasks/day |
| Groq distillation | Oracle ARM + Groq | 24/7 | 50 prompts/day |
| Data preprocessing | Oracle ARM | 24/7 | 50K rows/day |
| NVIDIA cross-validation | NVIDIA API | 24/7 | 1,000 calls/day |
| HF Spaces demo | HuggingFace | 24/7 | Unlimited |
| GovBench scoring | MacBook | 24/7 | 500 evals/day |

**Total free compute value: ~$0/day (all free)**

---

## 6. What Needs Paid GPU and For How Long

### Tasks Requiring Paid GPU

| Task | Why Paid? | GPU | Hours Needed | Cost | When |
|------|-----------|-----|-------------|------|------|
| TIES model merge | Weight-level merge needs VRAM | A40 | 1.5h/merge | $0.66 | After LoRA training |
| Reasoning LoRA training (fast) | Faster than Kaggle | RTX 3090 | 2h/run | $0.44 | When Kaggle quota exhausted |
| 7B+ model inference | Doesn't fit in 0.4B | RTX 3090 | 1h/day | $0.22 | Competition eval |
| 32B+ model inference | Too large for 3090 | H100 | 0.25h/day | $0.75 | Competition submissions |
| Full fine-tune (future) | Full weight update | A40 | 4h/run | $1.76 | If scaling to 7B |
| Competition submission | Time-critical | H100 | 0.5h/event | $1.50 | Deadline-driven |

### Kaggle T4 Allocation (30h/week = 4.3h/day)

| Task | Hours/week | Hours/day | Deliverable |
|------|------------|-----------|-------------|
| Reasoning LoRA training | 12h | 1.7h | 3 training runs/week |
| Code OWEM LoRA training | 8h | 1.1h | 2 training runs/week |
| Benchmark evaluation | 6h | 0.86h | Full eval suite/week |
| TIES merge (if fits) | 4h | 0.57h | 1 merge/week |
| **TOTAL** | **30h** | **4.3h** | |

---

## 7. Routing Table: Task Type → GPU → Cost

| Task Type | Primary | Fallback | Cost | Latency |
|-----------|---------|----------|------|---------|
| **OWEM inference (L1-L4)** | MacBook Ollama | — | $0 | 5-15s |
| **Clan routing** | MacBook Ollama | — | $0 | 2-5s |
| **BFT quorum** | MacBook Ollama | — | $0 | 10-30s |
| **Task decomposition** | MacBook Ollama | Groq 8b | $0 | 1-3s |
| **Heavy reasoning** | Groq 70b | Groq 8b | $0 | 1-2s |
| **Distillation teacher** | Groq 70b | NVIDIA API | $0 | 1-3s |
| **LoRA training** | Kaggle T4 | RTX 3090 | $0 or $0.22/h | 2-4h |
| **Model merge (TIES)** | RunPod A40 | Kaggle T4 | $0.44/h | 1-2h |
| **Benchmark eval** | Kaggle T4 | MacBook | $0 | 1-3h |
| **7B inference** | RunPod 3090 | Groq 70b | $0.22/h | 10-30s |
| **13B inference** | RunPod 3090 | — | $0.22/h | 20-60s |
| **32B+ inference** | RunPod H100 | — | $2.99/h | 5-15s |
| **Competition sub** | RunPod H100 | RunPod A40 | $2.99 or $0.44/h | varies |
| **Data preprocessing** | Oracle ARM | MacBook | $0 | varies |
| **GovBench eval** | MacBook | HF Spaces | $0 | 30-60s |
| **EAT evolve** | Kaggle T4 | RTX 3090 | $0 or $0.22/h | 2-4h |
| **EAT absorb** | Oracle ARM | MacBook | $0 | varies |
| **EAT transform** | RunPod A40 | Kaggle T4 | $0.44/h | 1-2h |

---

## 8. Optimal Strategy: $100 / 10 Days

### Day-by-Day Schedule

```
DAY 1-2: FOUNDATION ($0 spent)
├─ MacBook: Run full OWEM sandwich brain on all tasks
├─ MacBook: Benchmark all 19 models on GovBench
├─ Oracle ARM: Download + preprocess SupraLabs reasoning corpus (5M rows)
├─ Groq: Run 100 distillation prompts (2 days × 50/day)
├─ Kaggle T4: First reasoning LoRA training run (4h)
└─ Goal: Baseline metrics, training data ready

DAY 3-4: TRAINING ($2.64 spent)
├─ Kaggle T4: 3 more LoRA training runs (12h total)
├─ RunPod A40: First TIES merge of trained adapters (1.5h = $0.66)
├─ RunPod A40: Second TIES merge (1.5h = $0.66)
├─ MacBook: Benchmark merged models
├─ Groq: Continue distillation (100 more prompts)
├─ NVIDIA: Cross-validate 200 Groq outputs
└─ Goal: Reasoning OWEM 80% → 90%+

DAY 5-6: OPTIMIZATION ($3.96 spent)
├─ Kaggle T4: Code OWEM LoRA training (8h)
├─ RunPod A40: Merge code adapters (1.5h = $0.66)
├─ RunPod 3090: 7B model eval for competition (8h = $1.76)
├─ MacBook: EAT cycle — evolve all 12 clan hives
├─ Oracle ARM: Build competition submission dataset
├─ Groq: Distill competition-specific prompts
└─ Goal: Code OWEM trained, competition eval done

DAY 7-8: COMPETITION ($2.64 spent)
├─ RunPod H100: First competition submission (0.5h = $1.50)
├─ RunPod A40: Final TIES merge with all adapters (1.5h = $0.66)
├─ RunPod 3090: 13B model inference for scoring (4h = $0.88)
├─ Kaggle T4: Final benchmark sweep (4h)
├─ MacBook: Full GovBench compliance test
├─ Oracle ARM: Generate compliance reports
└─ Goal: Competition submitted, compliance verified

DAY 9-10: FINALIZE ($0.75 spent)
├─ RunPod H100: Final competition submission (0.25h = $0.75)
├─ MacBook: EAT absorb — integrate all learnings
├─ Kaggle T4: Final capability matrix eval (4h)
├─ Oracle ARM: Generate final synthesis report
├─ Groq: Final distillation batch
├─ MacBook: Deploy best model to HF Spaces
└─ Goal: Final models deployed, reports generated

TOTAL: $9.99 spent of $100 budget
```

### Hourly Cost Breakdown

| Time Block | Resource | Activity | Cost/hr | Hours | Total |
|------------|----------|----------|---------|-------|-------|
| 00:00-08:00 | MacBook | OWEM inference, EAT absorb | $0 | 8h | $0 |
| 00:00-08:00 | Oracle ARM | Data preprocessing, cron | $0 | 8h | $0 |
| 00:00-08:00 | Groq API | Distillation (rate-limited) | $0 | 8h | $0 |
| 08:00-12:00 | Kaggle T4 | LoRA training | $0 | 4h | $0 |
| 08:00-12:00 | MacBook | Benchmark eval | $0 | 4h | $0 |
| 12:00-18:00 | RunPod A40 | TIES merge (if needed) | $0.44 | 1.5h | $0.66 |
| 12:00-18:00 | RunPod 3090 | 7B inference (if needed) | $0.22 | 4h | $0.88 |
| 18:00-22:00 | MacBook | GovBench, EAT evolve | $0 | 4h | $0 |
| 18:00-22:00 | NVIDIA API | Cross-validation | $0 | 4h | $0 |
| 22:00-00:00 | MacBook | Overnight auto-runs | $0 | 2h | $0 |
| 22:00-00:00 | Oracle ARM | Overnight synthesis | $0 | 2h | $0 |
| **TYPICAL DAY** | | | | **43.5h** | **$1.54** |

### Daily Budget Cap Rules

```
RULE 1: Never exceed $10/day on paid GPU
RULE 2: Always exhaust free resources first
RULE 3: Kaggle T4 is FREE — use all 30h/week before touching RunPod
RULE 4: Groq is FREE — use all 100K tokens/day before paid inference
RULE 5: RunPod pods auto-EXIT when task completes — never leave idle
RULE 6: H100 only for competition deadlines or 32B+ requirements
RULE 7: RTX 3090 for LoRA training when Kaggle quota exhausted
RULE 8: A40 only for TIES merge (needs VRAM for weight manipulation)
```

---

## 9. Fallback Chain When Budget Runs Out

### Emergency Protocol ($0 remaining)

```
LEVEL 1: Free resources only
├─ MacBook: All inference (0.4B models)
├─ Groq: Heavy reasoning (100K tokens/day)
├─ NVIDIA: Backup inference (1000 calls/day)
├─ Oracle ARM: Data processing
├─ HF Spaces: Demo hosting
└─ Kaggle T4: Training (if weekly quota remains)

LEVEL 2: Groq-exhausted fallback
├─ MacBook: All inference (0.4B models)
├─ NVIDIA API: Heavy reasoning (1000 calls/day)
├─ Oracle ARM: Data processing
└─ Kaggle T4: Training

LEVEL 3: All API-exhausted fallback
├─ MacBook: ALL tasks (0.4B is all we have)
├─ Oracle ARM: Data processing
└─ Kaggle T4: Training (if quota remains)

LEVEL 4: Kaggle-exhausted fallback
├─ MacBook: ALL tasks
├─ Oracle ARM: Data processing
└─ No training until next week's Kaggle reset

LEVEL 5: Total free-exhausted
├─ MacBook: ALL tasks
├─ Oracle ARM: Data processing
├─ Wait for: Kaggle weekly reset (Monday)
├─ Wait for: Groq daily reset (midnight UTC)
├─ Wait for: NVIDIA daily reset (midnight UTC)
└─ Emergency: Use $0.22/h RTX 3090 for critical tasks only
```

### Cost Optimization Tricks

```
1. BATCH RunPod tasks — spin up once, run multiple jobs, then EXIT
2. USE network volumes — persist data across pod restarts ($0.07/GB/month)
3. SPOT pods when available — 50-80% cheaper than on-demand
4. PREEMPTIBLE training — checkpoint every 30min, resume if preempted
5. CACHE Groq responses — never re-call for same prompt
6. PARALLELIZE on MacBook — 4 workers × 0.4B = fast enough
7. COMPRESS datasets — gzip JSONL before uploading to pods
8. SCHEDULE heavy tasks for off-peak (RunPod sometimes has spot availability)
```

---

## 10. Summary: The $100 Strategy

### Core Insight

**90% of the SOV system runs on FREE resources.** The 0.4B models on MacBook handle:
- All 4 OWEM sandwich layers
- All 12 clan hives (144 clans, 1,728 families)
- BFT quorum (23/33)
- Stigmergic coordination
- EAT absorb and evolve

**Paid GPU is ONLY for:**
1. Training (LoRA, fine-tune) — Kaggle T4 covers most, RunPod as backup
2. Model merging (TIES) — needs VRAM for weight manipulation
3. Competition submissions — time-critical, needs larger models
4. Heavy inference (32B+) — burst only, 15 min/day max

### Budget Allocation Visualization

```
$100.00 total budget
├─ $66.00 (66%) → RTX 3090: 300h LoRA training + 7B inference
├─ $26.40 (26%) → A40: 60h TIES merge + 32B eval
├─  $7.50 (8%)  → H100: 2.5h competition submissions
└─  $0.10 (0%)  → Buffer
```

### What You Get For $100

| Deliverable | Free | Paid | Total |
|-------------|------|------|-------|
| OWEM pipeline runs | 216,000 | 0 | 216,000 |
| LoRA training runs | 14 (Kaggle) | 75 (RunPod) | 89 |
| TIES model merges | 2 (Kaggle) | 10 (RunPod) | 12 |
| Benchmark evals | 10 (Kaggle) | 20 (RunPod) | 30 |
| Competition submissions | 0 | 5 (H100) | 5 |
| Distillation prompts | 500 (Groq) | 0 | 500 |
| GovBench compliance tests | 50 | 0 | 50 |
| Models deployed | 19 (Ollama) | 12 (merged) | 31 |

### Final Numbers

```
FREE compute value:     ~$0/day  × 10 days = $0
PAID compute:           ~$10/day × 10 days = $100
Total GPU hours:        362.5h paid + ~430h free = 792.5h
Cost per pipeline run:  $100 / 216,000 = $0.00046
Cost per LoRA run:      $100 / 89 = $1.12
Cost per competition:   $100 / 5 = $20.00
```

---

**Bottom line:** The MacBook's 19 × 0.4B models do 90% of the work for $0. Paid GPU is a precision tool for training and competition, not a daily driver. $100 buys you 10 days of serious ML work if you route tasks correctly.
