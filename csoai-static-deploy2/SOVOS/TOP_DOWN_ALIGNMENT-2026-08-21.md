# TOP-DOWN ALIGNMENT — 2026-08-21 (revised binding)

Date: 2026-08-21 · lane: DSH/JEEVES (K3, measurement + drafting) · supersedes TOP_DOWN_AUDIT-2026-08-18.

## 1. THE SUBSTRATE (one line)
Mine → OOWM knowledge graph → council-oowm → Grok referee + 16-axis arena → Sim World → signed h3k cards.

## 2. COMPUTE FLEET (runpods, from FLEET_MAP-08-16)
| Pod | GPU | $/h | State | Duty |
|---|---|---|---|---|
| sov-repull-20260808 | RTX 3090 24GB | 0.22 | ✅ SSH-reachable | **BENCH ENGINE** — 4 llama-servers, arena_loop_keeper |
| sovos-light-master-mine | A100 | 1.39 | sibling | DO NOT TOUCH |
| sov-brain-a100-fresh2 | A100 80GB | 1.19 | ❌ gateway dead | exec pod + MinIO volume — recover on gateway |
| overnight-bench-a100-v2 | A100 | 1.19 | gateway dead | pause pending owner |
| 7 × EXITED | — | $0 | dead | atmos only |

**Inference truth (REVISED 2026-08-22 — GCP retired):** `localhost:11434` is an SSH bridge
(`runpod-ollama-bridge.sh`) to the **A100 sibling pod** (off-limits). The working backends are on
RunPod + Oracle:
- **`11439` → 3090 `sov-repull` WORKHORSE** ✅ chat verified (`qwen2.5:7b` → "ok", done:stop). Clean
  models: qwen3:8b, llama3:8b, mistral:7b, qwen2.5:7b, qwen3:4b, qwen2.5:1.5b, deepseek-r1:7b.
  (`council-oowm:latest` emits garbage `????` — corrupted fine-tune, flag for rebuild.)
- **`11436`/`11437` → Oracle micros** ✅ tags serve (qwen2.5-0.5b-mined / sov33-ultimate-sovereign).
EAT was pointed at the sibling (11434) → empty → misread as dead. Re-pointed to 11439 via
`OLLAMA_CHAT` env → model measurement UNBLOCKED.

## 3. EAT PHASES — run this session
| Phase | Result | Note |
|---|---|---|
| Runtime alignment (`test_sov_runtime_alignment.py`) | ✅ 6/6 OK | invariants/router/stack consistent |
| E2E selftest (`sov_e2e.py --selftest`) | ✅ PASS | spawn→grow→ledger→honey→5D→fluid→IWM→VWM |
| GovBench measure (3090, 3 models) | 🔄 RUNNING | re-pointed to 11439; real numbers incoming |

## 4. PLAY-300 STRATEGY LAYER (this session, 21 files in SOVOS/play-300/)
Movement 0 (truth) · 1 (standards) · 2 (GTM) · 3 (neutrality) · 4 (arena) · 7 (registry) ·
8 (evidence) · 9 (ops). Crown jewels: 043 measurement-card · 067 SB 315 · 072 crosswalk ·
091 ledger · 093 capture monitor · 121 replay · 126 rate-cap.
Movement 5 & 6 = code (LANE). External filings = NICK/Claude. Signed cards = POD key.

## 5. HONEST GATES (unchanged)
1. ~~GCP billing~~ RETIRED (no longer used) · 2. RunPod A100 gateway · 3. POD signing key ·
4. prod deploy (branch→PR→Claude→GHA) · 5. external credentials (IETF/GitHub/OSF).

## SIGIL
`topdown-alignment-2026-08-21-jeeves` (UNSIGNED until POD key).
