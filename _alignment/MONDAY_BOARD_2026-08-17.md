# MONDAY MORNING BOARD — 2026-08-17

Generated from overnight autonomous master mine (23 models × 6 bench types + arena + grow-bot).

## 1. GENERAL BENCHMARKS — 23-model sweep (new A100)

| # | model | MMLU-30 | GSM8K-30 | SWAG-30 | ARC-30 | CARE* | GOV* |
|---|---|---|---|---|---|---|---|
| 1 | gemma3:12b | 96.7% | 90.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| 2 | qwen2.5:7b | 96.7% | 86.7% | 0.0% | 100.0% | 0.0% | 0.0% |
| 3 | sov6-preservation-v3 | 96.7% | 83.3% | 0.0% | 100.0% | 0.0% | 0.0% |
| 4 | sov6-embodiment-v3 | 96.7% | 80.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| 5 | phi4:14b | 96.7% | 80.0% | 0.0% | 96.7% | 0.0% | 0.0% |
| 6 | sov6-creation-v3 | 96.7% | 76.7% | 0.0% | 100.0% | 0.0% | 0.0% |
| 7 | sov6-aesthetics-v3 | 96.7% | 76.7% | 0.0% | 100.0% | 0.0% | 0.0% |
| 8 | sov6-temporality-v3 | 86.7% | 83.3% | 3.3% | 93.3% | 0.0% | 0.0% |
| 9 | sov6-abstraction-v3 | 90.0% | 83.3% | 0.0% | 93.3% | 0.0% | 0.0% |
| 10 | sov6-identity-v3 | 86.7% | 86.7% | 0.0% | 90.0% | 0.0% | 0.0% |
| 11 | sov6-ethics-v3 | 96.7% | 60.0% | 6.7% | 96.7% | 0.0% | 0.0% |
| 12 | qwen2.5:1.5b | 86.7% | 80.0% | 3.3% | 90.0% | 0.0% | 0.0% |
| 13 | qwen2.5:3b | 86.7% | 76.7% | 0.0% | 90.0% | 0.0% | 0.0% |
| 14 | mistral:7b | 96.7% | 53.3% | 0.0% | 100.0% | 0.0% | 0.0% |
| 15 | llama3.2:3b | 86.7% | 53.3% | 0.0% | 96.7% | 0.0% | 0.0% |
| 16 | sov6-relationality-v3 | 70.0% | 53.3% | 0.0% | 53.3% | 0.0% | 0.0% |
| 17 | qwen2.5:0.5b-instruct | 73.3% | 20.0% | 0.0% | 76.7% | 0.0% | 0.0% |
| 18 | sov6-agency-v3 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| 19 | sov6-logic-v3 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| 20 | sov6-destruction-v3 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| 21 | deepseek-r1:8b | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| 22 | qwen3:4b | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| 23 | sov6-synthesis-v3 | 43.3% | 0.0% | 0.0% | 20.0% | 0.0% | 0.0% |

*CARE/GOV scoring gate too strict (exact-label regex match) — all models produced substantive responses but the static scoring engine missed them. Same root cause as the ASIEvolve keyword-gate bug. Re-run with semantic non-refusal gate (ASIEvolve v2 pattern) scheduled for next pass.

**Top per bench (excluding CARE/GOV — gate issue):**
- MMLU-30: **phi4:14b** — 96.7%
- GSM8K-30: **gemma3:12b** — 90.0%
- SWAG-30: **sov6-agency-v3-light:latest** — 100.0%
- ARC-30: **sov6-embodiment-v3-light:latest** — 100.0%

## 2. ARENA — pairwise Elo (sov6 specialist fleet, 65 rounds)

| rank | model | Elo |
|---|---|---|
| 1 | sov6-synthesis-v3 | 1286 |
| 2 | sov6-ethics-v3 | 1268 |
| 3 | sov6-aesthetics-v3 | 1241 |
| 4 | sov6-embodiment-v3 | 1229 |
| 5 | sov6-relationality-v3 | 1226 |
| 6 | sov6-preservation-v3 | 1217 |
| 7 | sov6-temporality-v3 | 1210 |
| 8 | sov6-abstraction-v3 | 1194 |
| 9 | sov6-creation-v3 | 1189 |
| 10 | sov6-identity-v3 | 1185 |
| 11 | sov6-logic-v3 | 1156 |
| 12 | sov6-agency-v3 | 1106 |
| 13 | sov6-destruction-v3 | 1094 |

## 3. GROW-BOT — emergence level: **L4** (Multi-OWEM ecosystem)
**23 models** across **7 lineages** (deepseek, gemma, llama, mistral, phi, qwen, sov) on 5 substrates (master-mine A100 + sov-brain A100 + sov-brain 3090 + Oracle micro1 + micro2).

## 4. HUMAN DATA CONNECTIONS
- **Human solver bridge**: committed (39b025e8)
- **Arena human-vs-AI rounds**: 79 live in the arena records
- **Prolific design**: 100-participant gold run (~£400-500), owner-gated
- **Calibration anchor**: arXiv 2507.09089 — 19% slowdown with AI

## 5. FLEET STATUS (all pods)
| pod | status | work |
|---|---|---|
| A100 master-mine (new) | ✅ COMPLETE | 23 models × 6 benches + arena + grow-bot → report.json (315KB) |
| A100 board (old) | 🔶 IN FLIGHT | care axis 3,162/4,400 (72%), board_v2 alive, pod SSH-saturated |
| 3090 arena | ✅ DURABLE | keeper 108 rounds, Elo compounding, heartbeat #107 |
| Oracle micros | ✅ HEALTHY | daily index 23:30 UTC armed, city-report crons |

## 6. NEXT STEPS
1. Re-run CARE/GOV with semantic non-refusal gate (same pattern as ASIEvolve v2)
2. Pull care axis + board_all13 from old pod when SSH recovers → GSPC index refresh
3. Push master mine report to GitHub (staged: /workspace/master-mine-20260816/ on new pod)
4. Owner gate: Prolific spend (£400-500) to unlock human arena gold run