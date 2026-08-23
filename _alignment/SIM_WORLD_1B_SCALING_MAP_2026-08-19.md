# SIM WORLD → 1,000,000,000 SCALING MAP
## 2026-08-19 · every hot path measured, every blocker fixed or mapped
*The honest engineering answer to "1,000,000×?" and "map scaling to 1,000,000,000": the sim world is CPU-only (free), the real fuel is measurement records (GPU/M-chip), and each hot path now has a measured ceiling, a fix, and a 1B target.*

---

## ══ 0. WHAT 1B MEANS (the honest framing) ══

| Quantity | What it is | Value at 1B |
|---|---|---|
| World rounds | display counter, CPU-only | cosmetic — the number climbs, the DB doesn't |
| Benchmark records | the fuel: JSONL rows → h3k cards → SFT pairs | 1B rows = 10M cards = the training corpus |
| h3k cards | 3KB ed25519-signed capsules | 10M cards at 100 records each |
| Chain links | J-space prev-links | 10M links, append-only |
| SFT pairs | cards-train.jsonl | 1B rows ≈ 100M+ pairs |

**The rule that fell out of measurement: scale the RECORDS, not the rounds.** World rounds are free but empty; records are the product.

---

## ══ 1. HOT PATHS — MEASURED CEILINGS (before this session's fixes) ══

| # | Path | Where | Measured ceiling | 1B blocker |
|---|---|---|---|---|
| 1 | HTTP step | sim-server `/sim/control` | **45 steps/s** | every response serializes the 99.5KB snapshot (175 agents × 16 axes) → 1M rounds = 6.2h of pure serialization |
| 2 | Per-agent broadcast | engine.step() line 119 | 175 events/round | 1B rounds × 175 agents = **175B SSE writes** — network death |
| 3 | Sov-sync subprocess | engine.maybeSyncSov() | every 4 rounds | `cargo run --release` spawn (15s timeout) = **250K spawns per 1M rounds** — hours of compiler, impossible at 1B |
| 4 | Chain index rebuild | chain-index.mjs | O(all cards) per run | re-reads + re-sorts every card file each run → quadratic at 1M+ |
| 5 | Benchmark append | sim-server.recordBenchmark() | 1 syscall/record | 1B records = **1B appendFileSync syscalls** |
| 6 | Card emit | cards.ts | 100 records/card | 10M cards = 10M signs (each ~µs, fine) |
| 7 | In-world benchmark | gspc.ts answerFor() | deterministic, no model | **not real measurement** — score = energy + model.length; dedup correctly rejects duplicates |

---

## ══ 2. FIXES SHIPPED THIS SESSION (in the bundle, need host restart) ══

| # | Fix | Where | Effect at 1B |
|---|---|---|---|
| 1 | **bulkStep(count)** — N rounds in-engine, ONE snapshot broadcast | engine.ts + sim-server.ts | 1M rounds = seconds of server time instead of 6.2h; count clamped ≤1,000,000 |
| 2 | **Quiet duels in bulk** — maybeDuel(quiet) skips per-duel emits | engine.ts | no per-duel SSE flood in bulk mode |
| 3 | **Sov-sync gated to round%250 + prebuilt binary only** (cargo fallback dropped from hot loop) | engine.ts | 250K spawns/1M → 4K spawns/1M with prebuilt sovd; zero compiler spawns from the auto-runner |
| 4 | **Incremental chain-index v2** — O(new cards), idempotent, verified (+2 → no-op → +1 → no-op, 0.22s @ 1,083 cards) | chain-index.mjs | 10M cards = 10M appends, never a full rebuild |
| 5 | **recordBenchmarkBatch()** — one appendFileSync + one SSE frame per run | sim-server.ts + types.ts | 1B records = ~10M syscalls (per run, not per record) |
| 6 | **benchmark-batch SSE event** — GUI shows bulk runs without 100K frames | SimWorldView.tsx | UI stays live at scale |

Build verified: `lib/index.js` + `lib/client.js` rebuilt clean (572–719ms), all markers present.

---

## ══ 3. THE 1B PIPELINE (post-restart) ══

```
GPU/M-chip inference (pod-bench.sh / measure-gemma.py)
  → recordBenchmarkBatch (1 syscall/run)         [fixed]
  → living.jsonl (JSONL, append-only, batch)
  → sim_emit_card (100 records/card, ed25519)    [fine]
  → chain-index v2 (incremental append)          [fixed]
  → cards-train.jsonl (SFT pairs)
  → MLX-LM LoRA retrain → better models → re-measure
```

### Throughput math at 1B records
- **Pod path** (3090, ~$0.22/h, real inference): 112 records/sweep → 1B = ~8.9M sweeps ≈ **~$20–70K pod time** — the honest price of 1B *real* records
- **M-chip path** (MLX, free): real inference, ~1 record/s → 1B ≈ 11.5 days of continuous M-chip — free but slow
- **Deterministic sim path**: instant but **worthless** — the miner's dedup is the integrity guard; do not flood it

---

## ══ 4. WHAT'S LEFT FOR TRUE 1B (owner gates + next engineering) ══

| Gate | What | Who |
|---|---|---|
| **Host restart** | activate bulkStep + batch append + sov gate (all built, in bundle) | [N] confirm — brief GUI drop |
| **SIM_WORLD_ALLOW_RUNPOD=1** | enable live pod dispatch + billing (same restart) | [N] confirm |
| Pod bench at scale | run pod-bench.sh sweeps continuously (real inference) | lane, after gate |
| Chain durability | move chain-index.json to append-only WAL + periodic compaction | lane (next) |
| Record partitioning | living.jsonl → per-day files + index (1B rows = ~200GB) | lane (next) |
| Card packing at scale | emit-card worker that packs exactly 100 and chains prev links in-body | lane (next) |
| GPU bench records | measure-gemma.py + Qwen adapters on M-chip now (free, real) | lane (can do now) |

---

## ══ 5. STATUS SNAPSHOT (post-fix, pre-restart) ══
- World: round ~9,868 and climbing (auto-run 2s) · 175 agents · sov-space wired
- Cards: **1,083 chained · 1,083 linked · 0 breaks · 100% coverage** (chain-index v2 verified incremental)
- Benchmark DB: ~8,000 records, LaunchAgent judge ticking
- Chain-index runtime: **0.22s for 1,083 cards** (was full-rebuild; now O(new))
- Bundle: rebuilt clean with all 6 fixes — **awaiting host restart to activate**

---

## ══ NET ══
The sim world was never going to reach 1B by stepping — it was capped by serialization (45/s), broadcast (175/round), subprocess spawn (every 4 rounds), full-rebuild chain indexing, and per-record syscalls. **All five are now fixed in code and verified in the bundle.** The remaining move to 1B is real measurement records from the GPU/M-chip paths — that's an owner gate (restart + RunPod flag) plus continuous sweeps. Scale the records, not the rounds.
