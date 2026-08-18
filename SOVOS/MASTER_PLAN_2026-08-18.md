# SOVOS/OOWM MASTER PLAN — Mine Everything, Improve, Next Phases
**Date:** 2026-08-18 · **Lane:** JEEVES (K3) · **Directive (Nick):** *"set all plans and mine all we have to improve or what else is needed as well for all next steps phases"*

---

## 1. THE MINE — what we have, all seams (verified this session)

| # | Seam | Source | Docs (Mac build) | Status |
|---|---|---|---|---|
| 1 | **Honey KB** | `forest/honey_all_producers.jsonl` — 94,181 rows / 113MB | 1,058 sampled | ✅ mined (600-row window) |
| 2 | **Benchmark results** | `benchmark-results/**/*.json` (15MB) | 307 | ✅ mined |
| 3 | **MCP marketplace** | 710 packages (`mcp-marketplace/*/README.md`) | 460 | ✅ mined |
| 4 | **llm.json companions** | `csoai-static-deploy2/**/*.llm.json` | 1,200 | ✅ mined |
| 5 | **Arena rounds (live)** | pod `reborn_rounds.jsonl` — 2,112+ Elo rounds | 400 window | ✅ mined, grows every tick |
| 6 | **Grok referee rounds (live)** | pod `grok_referee_rounds.jsonl` | 189 | ✅ mined, grows every tick |
| 7 | **GitHub estate** | CSOAI-ORG 120 repos (README/agent/mcp cards) | 90+26+4 | ✅ mined |
| 8 | **HF datasets** | `huggingface.co/api/datasets?author=csoai` | 29 | ✅ mined |
| 9 | **Kaggle datasets** | nicktempleman catalog | 40 | ✅ mined |
| 10 | **Charters** | `sovereign-charters/*.md` (218) | 218 | ✅ mined |
| 11 | **Sovereign-temple corpus** | `sovereign-temple-public/*.py` | 479 | ✅ mined |
| 12 | **Alignment canon** | `_alignment/**/*.md` | 110 (+499 pod) | ✅ mined |
| 13 | **csoai-site HTML** | `csoai.org/**/*.html` | 500 | ✅ mined |
| 14 | **Sim World h3k cards** | ed25519-signed benchmark cards | 1 (live) | ✅ mined, new cards bankable |
| 15 | **SOVOS packages + sov-os + doctrine** | SOVOS/ sov-os/ registry | 55 | ✅ mined |

**Totals:** Mac build **8,999 docs** (v4: honey 5K) · pod build **2,703 docs** (limited by volume mirror) · every 5-min tick re-mines and grows.

## 2. THE STACK — what's running (all on pod volume `/workspace`)

| Process | Role | Status |
|---|---|---|
| `overnight_sovos_driver.py` | Orchestrator, 5-min ticks, stop 04:00Z | ✅ ALIVE (tick 116+) |
| `grok_referee_keeper.py` | Measures OOWM-family vs frontier (Grok→OpenRouter→Groq fallback) | ✅ ALIVE |
| `arena_loop_keeper.py` | 24/7 Elo arena (7 models, 4 axes) | ✅ ALIVE (2,112+ rounds) |
| `a100_oowm_wire.sh` | Auto-wires A100-1 on reconnect (syncs code + keys + referee) | ✅ ALIVE (polling) |
| `overnight_axes.py` | **Sibling lane's job — untouched (fleet doctrine)** | ⚠️ saturating Ollama |

## 3. WHAT ELSE IS NEEDED — the honest gap list

### 🔑 Owner gates (Nick — 3 sittings, ~90 min total)
| Gate | Why | Sitting |
|---|---|---|
| **OpenRouter credits** (or unlock Grok Bot key → `~/.runpod/secrets/xai.key`) | Referee switches from Groq fallback to **true xAI Grok** | MONEY |
| **A100-1 unreachable** (RunPod infra flap, `uptimeSeconds:0` since Aug 17 10:56Z) | 100GB volume + A100 GPU idle; wire loop polls but RunPod-side stop/start may be needed | MONEY |
| **GCP billing** (P0 from AGENTS.md) | SOV3 :3101 coordination + keystone GCP mirror dead | MONEY |
| **Direct xAI key** GUI extraction | `security find-generic-password -a "Grok Bot Key" -s "Grok Bot Safe Storage" -w` | MONEY |

### 🤖 Agent-doable next (no owner needed)
| # | Phase | What | Est. |
|---|---|---|---|
| P1 | **Full honey ingestion** | ✅ **DONE — 5,458 honey rows (94K total available, 5K window)** | done |
| P2 | **Arena axis expansion** | ✅ **DONE — 4 → 16 GSPC axes live (round 2,123+)** | done |
| P3 | **Referee model pool** | Round-robin all 7 OOWM models vs frontier (currently 1 random) | 1h |
| P4 | **A100 fleet guardian** | Verify `com.meok.oracle-fleet-guardian` pattern → RunPod equivalent | 1h |
| P5 | **sovereign-os.html wiring** | Live-read `grok_referee_league.json` + arena rounds on the public surface | 2h |
| P6 | **Weekly mine refresh** | Pod cron: full re-mine + index commit-back to Mac daily | 30m |
| P7 | **Card pipeline** | Auto-emit h3k card per overnight run, sync to pod, feed mine | 1h |
| P8 | **mcp.json + llms.txt fix** (from canon) | Repair agent storefront (llms.txt sov33 line, mcp.json content-type) | 1h |

### 🧭 Phase roadmap (long arc)
```
NOW ──► P1-P3 (mine depth) ──► P4-P5 (fleet + surface) ──► P6-P8 (automation + storefront)
        │                          │                           │
   honey 5K · 16 axes ·     A100 guardian · public       weekly auto · cards ·
   full model pool          league on csoai.org          storefront repair
```

## 4. THE ALIGNMENT (top-down binding)

```
ESTATE MINE (15 seams, 4,600+ docs)
   │  estate_mine_ingest.py (every 5 min)
   ▼
OOWM knowledge graph (TF-IDF, persistent)
   │  oowm.server (MCP, stdio)
   ▼
council-oowm answers from real estate + live measurement
   │
   ├── Grok referee (measure-only, never governance)
   ├── Arena loop (24/7 Elo)
   ├── A100 wire (auto on reconnect)
   └── Sim World (18,060+ rounds, Grok 4.5 as agent, h3k cards banked)
```

**Codename binding (canon):** SOVOS = MEOK = our actual OOWM. Hives + OWEMs (12 hives / 95 OWEMs) + IWM (inner/sovos-world) + OWM (outer/Cosmos/V-JEPA) + VWM (visual/DA3) = the family; the OOWM index is the estate-learned substrate under them all.

## 5. SIGNED ARTIFACTS (this session)
- `h3k-2026-08-18T0243.json` — 5,001B / 1,714B gz, ed25519-signed, 16 records (all 16 GSPC axes)

## SIGIL
`sovos-master-plan-2026-08-18-jeeves`
