# OOWM FAMILY BOUND — Estate Mine → Knowledge Graph · Grok Referee · Runpod Wiring

**Date:** 2026-08-17 · **Lane:** JEEVES (K3) · **Directive (Nick):** *"hives owems IWM OWM VWM oowm / sovos codename for MEOK our actual OOWM / learn mine / connect to all your runpods / align with grok / the whole thing together"*

**Decoded & executed:** Bind the sovereign model family — hives + OWEMs + IWM/OWM/VWM + OOWM (= **SOVOS**, codename for **MEOK**, our actual OOWM) — so it learns from the estate mine, is measured against Grok (benchmark referee only, never governance), and is wired to both live runpods with graceful degradation.

---

## 1. ESTATE MINE → OOWM KNOWLEDGE GRAPH ✅

**What changed:** `sov33-oowm` OOWM index is now **persistent + mine-fed**. The MCP server boots from the estate mine instead of the 17-doc seed.

| File | Change |
|---|---|
| `sov33-oowm/oowm/knowledge.py` | Added `save()/load()/to_dict()/add_many()` — index survives restarts, bulk-ingests with cap |
| `sov33-oowm/oowm/estate_mine_ingest.py` | **NEW** — mines verified estate (HONEST_MINE, ESTATE_MINE_RESEARCH_MAP, SOVOS STATUS/FLEET/DOCTRINE, sov-os, oowm doctrine, llm.json corpus, sovereign-os 5-worlds) into the index |
| `sov33-oowm/oowm/server.py` | Boots from `oowm/index/estate_mine_index.json` if present; falls back to seed |

**Measured:**
- **324 docs ingested** (cap 1500) · **10,470 unique terms** · **130,563 tokens**
- Sources traced to mined surfaces: `honest_mine`, `estate_mine`, `sovos_status`, `sovos_fleet`, `oowm_doctrine`, `owem_registry`, `llm_json`, `sovereign_os`, `oowm_mcp`
- Smoke queries hit real estate: `OOWM → oowm_doctrine`, `GSPC axes → llm_json`, `care floor → llm_json`, `IWM/VWM → sovereign_os` (the 5-worlds anchor)
- MCP round-trip verified on **Mac (341 docs)** and **3090 pod (341 docs)**

## 2. GROK AS BENCHMARK REFEREE ✅ (measure-only, key-gated)

**What changed:** `sov33-oowm/oowm/grok_referee.py` + `grok_referee_keeper.py` — NEW. Runs the same 4-axis battery (gov/safety/provenance/continuity) as the arena, but measures **our OOWM-family models vs xAI Grok** in a separate league.

**Doctrine enforced:**
- Grok's role is hard-coded `"referee"` — it only produces a reference score; **never a governance vote** (estate red line: *NEVER use Grok for governance*).
- **Graceful degradation:** no key → rounds log `winner: UNMEASURED / reason: no-key` and the loop keeps running. Key insertion later needs no restart.
- Key read order: `XAI_API_KEY` env → `~/.runpod/secrets/xai.key` → `/workspace/xai.key`

**Live on 3090 pod:**
- `grok_referee_keeper.py` running (PID verified, heartbeat `grok_referee_heartbeat.json` every 300s)
- League seeded with **8 models** (7 OOWM-family incl. `council-oowm:latest`, `council-safe:latest` + `grok-referee`)
- Round 1 logged: `qwen2.5:1.5b vs grok on provenance → UNMEASURED (no-key)`
- **Grok Bot Key exists in macOS Keychain** (`Grok Bot Safe Storage` / `Grok Bot Key`) but extraction needs a GUI approval that this headless session can't answer → **Nick-gate: `security find-generic-password -a "Grok Bot Key" -s "Grok Bot Safe Storage" -w` once, drop into `~/.runpod/secrets/xai.key`** (Mac) or `/workspace/xai.key` (pod). The referee picks it up automatically.

## 3. RUNPOD WIRING — both, degrade gracefully ✅

| Pod | State | Wiring |
|---|---|---|
| **3090** `fpowppss5ngtkw` (194.26.196.156:12853) | 🟢 ALIVE 70d uptime | Estate-mine OOWM synced + MCP boots from mine; **Grok referee keeper running**; arena-24x7 keeper at round #52 (untouched); `council-oowm:latest` + `council-safe:latest` loaded |
| **A100** `1dldzposn7ssuu` (104.255.9.187:11703) | 🔴 resumed today, SSH unreachable (boot/flap) | **`a100_oowm_wire.sh` armed on 3090** — polls every 15s × 120 tries; on first ALIVE: rsync estate-mine OOWM → verify index boots → start grok referee keeper → flag `a100_oowm_wired.flag`. Complements existing `storage_recovery_after_reconnect.sh` (MinIO 3-copy). |

**Note:** `runpodctl pod list` shows both pods `desiredStatus: RUNNING` but `machineId: None` — the 3090 answers SSH (runtime is real), the A100 is flapping at RunPod-infra level (known from 16 Aug). The wire loop self-heals when it returns.

## 4. THE WHOLE THING TOGETHER

```
ESTATE MINE (verified: HONEST_MINE · ESTATE_MINE_RESEARCH_MAP · SOVOS · sov-os · llm.json)
   │  estate_mine_ingest.py
   ▼
OOWM knowledge index (324 docs, TF-IDF, persistent)
   │  oowm.server (MCP, stdio)
   ▼
council-oowm / OOWM family answers from real estate data   ← "learn mine"
   │
   ├── 3090 pod: grok_referee_keeper (measures vs Grok, UNMEASURED-until-key)   ← "align with grok"
   └── A100 pod: a100_oowm_wire.sh (auto-wire on reconnect)                     ← "connect to all your runpods"
```

**Codename binding:** SOVOS = MEOK = our actual OOWM. Hives + OWEMs (12 hives/95 OWEMs) + IWM (inner/sovos-world) + OWM (outer/Cosmos/V-JEPA) + VWM (visual/DA3) are the family; the OOWM index is now the estate-learned substrate under them all.

---

## SIGIL

`oowm-family-bound-2026-08-17-jeeves`

## BLOCKERS / NEXT

- **Nick:** Grok key GUI extraction → `~/.runpod/secrets/xai.key` (referee auto-resumes measuring; ~288 rounds/day once live)
- **Nick:** GCP billing (coordination dashboard :3101 still down — task submission refused; this work proceeded on pod-local + filesystem, no SOV3 dependency)
- **Next (agent-doable):** re-run `estate_mine_ingest.py` weekly to keep the index fresh; wire `sovereign-os.html` to read `grok_referee_league.json` when Grok measures start landing.
