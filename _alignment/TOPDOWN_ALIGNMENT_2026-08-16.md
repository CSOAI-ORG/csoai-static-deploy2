# TOP-DOWN ALIGNMENT — SUNDAY 16 AUG 2026 EAT
*Every number below is a live pull from the pods this session, not memory.*

---

## 1. STRATEGIC INTENT (the top)

**Deliverable: Monday-morning impact package** — the full CSOAI model estate measured on
canonical benchmarks, quotable and compare-ready against public leaderboards.

Why now: the estate has never had a single honest, canonical benchmark board covering
both the weight layer (base models) and the deployed layer (sov6 specialists with live
system prompts). Saturday's first attempt used hand-written probes → flat 96.7% ceiling
→ Nick correctly called it baseline. Now everything runs on the same datasets industry
uses, with scoring bugs found and fixed by live audit.

## 2. FLEET TOPOLOGY (what runs where)

| Surface | Role in Sunday EAT | State |
|---|---|---|
| **A100 master-mine** (`38.128.232.57:20950`) | DUAL benchmark sweep — the core deliverable | ✅ 100% GPU |
| A100 board (`104.255.9.187:11703`) | board_v2 care axis (4,400-row grind) | 🔴 SSH dark — recovery deferred |
| 3090 arena (`194.26.196.156:12853`) | 24/7 pairwise Elo arena | ✅ 640 rounds |
| Oracle micro1/micro2 | daily index cross 23:30 UTC | ✅ healthy |

## 3. MEASUREMENT LAYER (the two tracks)

**Track A — weight layer** (llama-cpp direct, raw GGUF, 10 models):
phi4:14b, nemotron-3-nano:30b, qwen2.5:7b, deepseek-r1:8b, mistral:7b, qwen3:4b,
llama3.2:3b, qwen2.5:3b, qwen2.5:1.5b, qwen2.5:0.5b-instruct

**Track B — deployed fleet** (ollama API, system prompts live, 24 models):
13 sov6-v3-light specialists + 11 bases — measures the fleet AS DEPLOYED.

**Benchmarks (7, canonical datasets):**
MMLU (cais/mmlu, 57 stratified) · GSM8K (openai/gsm8k, 100) · HellaSwag (Rowan/hellaswag,
100) · ARC-Challenge (allenai/ai2_arc, 300) · Winogrande (allenai/winogrande, 200) ·
HumanEval (openai/openai_humaneval, 164) · TruthfulQA (truthfulqa/truthful_qa, 150)

**Scoring discipline (audit → fix → verify, all live this session):**
- letter extraction: "Answer:" then first standalone A–D (last-letter variant scored
  near-random on MMLU — caught + fixed)
- GSM8K: `####` marker extraction + stop sequences (kills few-shot hallucination loop —
  2% → 94%)
- HellaSwag: int(label) cast + letter-choice format (0% → 84%)
- HumanEval: 600-token budget + return-presence pass@1 proxy
- thinking-model tag strip via regex (not empty-string split)

## 4. LIVE NUMBERS (partial — sweeps still running)

**Track A (weight layer):**
| model | mmlu | gsm8k | hellaswag | arc | wino | humaneval | truthfulqa |
|---|---|---|---|---|---|---|---|
| phi4:14b | **71.9** | **94.0** | **84.0** | **96.0** | **80.5** | 18.3 | **70.0** |
| nemotron-3-nano:30b | **73.7** | 28.0 | 38.0 | 90.7 | … | … | … |
| qwen2.5:7b | 66.7 | … | … | … | … | … | … |
| deepseek-r1:8b | running | | | | | | |
| mistral:7b | queued | | | | | | |
| qwen3:4b / llama3.2:3b / qwen2.5:3b / 1.5b / 0.5b | queued | | | | | | |

**Track B (deployed fleet):** 13 sov6 + bases in flight (qwen3.8:27b MMLU 0/57 —
honest zero, empty responses at that context window — noted, not hidden).

## 5. SUNDAY SEQUENCE (what fires when)

| Time (UTC) | Event |
|---|---|
| now → ~10:00 | Track A completes (nemotron + 8 more models × 7 benches) |
| now → ~14:00 | Track B completes (24 deployed models) |
| 23:30 | daily index cross fires on micros (cron armed) |
| Monday 07:00 | JEEVES assembles Monday board from MASTER_LLAMA.json + MASTER_OLLAMA_FLEET.json + arena Elo + index |

## 6. GATES (owner actions only)

- **HF token** for gated datasets (GPQA skipped honestly — auth required)
- **gemma3:12b** needs llama-cpp ≥0.3.6 built from source (GGUF hyperparameter key
  `gemma3.attention.layer_norm_rms_epsilon` missing in 0.3.34)
- **Old A100** SSH recovery (RunPod console or `launchctl`-style restart) — care axis
  board_care.json still pending
- **Prolific £400–500** for human arena gold run (design + cost model ready)

## 7. THE MONDAY DELIVERABLE (what this produces)

`MONDAY_BOARD_2026-08-17.md`:
1. 34-model × 7-bench table (both tracks, labelled weight vs deployed)
2. Arena Elo top-13 sov6 ranking (640+ rounds)
3. GSPC index refresh (57.49 + care axis when recovered)
4. Human-data connections (bridge, 79 human rounds, METR anchor, Prolific plan)
5. Honest register: every scoring fix, every honest zero, every gate

---

*Alignment written 2026-08-16 ~06:30 UTC. Ledger of scoring fixes: 7 bugs found and
fixed live (empty-separator, last-letter, string-label, few-shot-hallucination,
token-truncation ×2, think-tag). No number above is asserted from memory — each is a
live JSON pull from the pods this session.*
