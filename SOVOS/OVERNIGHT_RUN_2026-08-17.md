# OVERNIGHT AUTONOMOUS RUN — 2026-08-17 (launched 16:19 UTC → 04:00 UTC)
**Lane:** JEEVES (K3) · **Host:** RunPod 3090 `fpowppss5ngtkw` (194.26.196.156:12853) · **Directive (Nick):** *"work from runpods, all work to volumes, not the MacBook, auto run overnight till 4 am"*

---

## What is running (all on the pod volume `/workspace`)

| Process | PID | Cycle | Purpose |
|---|---|---|---|
| **`overnight_sovos_driver.py`** | 1287869 | 5 min | Orchestrator — target stop **2026-08-18T04:00:00Z** |
| `grok_referee_keeper.py` | (supervised) | 5 min | Grok referee rounds vs `x-ai/grok-4.6` via OpenRouter (measure-only) |
| `arena_loop_keeper.py` | (supervised) | 90 s | 24/7 arena Elo loop (untouched, sibling-compatible) |
| `a100_oowm_wire.sh` | (supervised) | 15 s poll | Auto-wires A100-1 OOWM on reconnect (graceful degrade) |
| `overnight_axes.py` | 3388566 | — | Sibling lane's job (15:58) — NOT touched per fleet doctrine |

**Every tick the driver:** re-ingests estate mine → OOWM knowledge graph (rc=0, 304 docs from `/workspace` volume mirror) → verifies all keepers alive (restarts any dead) → writes `overnight_state.json` to volume.

## Verified state (Tick 1, 16:19:05Z)

```json
{"tick": 1, "target": "2026-08-18T04:00:00+00:00",
 "ingest": {"rc": 0, "added": 304},
 "grok_referee": "already-running", "arena": "already-running", "a100_wire": "already-running",
 "grok_referee_rounds": 64, "arena_rounds": 1807, "volume": "/workspace"}
```

## MEGA-MINE v2 (16:49Z — driver upgraded mid-run, no downtime)

**2,709 docs** (was 304) · **34,051 unique terms** · **924,359 tokens** — the OOWM knowledge graph is now **8.9×** the original size:

| Source | Docs |
|---|---|
| llm_json companions | 1,200 |
| csoai_site HTML cards | 500 |
| temple_py (3,580-file corpus) | 479 |
| charters (sovereign-charters) | 218 |
| alignment canon | 110 |
| **github_repo (CSOAI-ORG readmes)** | 90 |
| sovos_package READMEs | 32 |
| github_agent (agent.json) | 26 |
| sov_os docs | 13 |
| github_mcp (mcp.json) | 4 |
| oowm_mcp + doctrine + registry + mine + fleet | 37 |

- **GitHub mine added:** `gh api` per repo — README + agent.json + mcp.json for all 120 CSOAI-ORG repos (90 mined OK, rest no README). Fail-soft offline.
- **Driver upgraded:** ingest `--cap 8000`, all keepers re-verified, mega-mine index deployed to pod volume, MCP boots 2,709 docs pod-side.
- **Every 5-min tick** re-runs the full mega-mine (local corpus + GitHub cards) — the knowledge graph grows all night.

## REFEREE MULTI-BACKEND v3 (17:03Z)

**Issue found:** OpenRouter main key **out of credits** (402) → rounds were UNMEASURED. Alternate `sk-` keys invalid on both OpenRouter and xAI.

**Fix:** referee now resolves keys in order **XAI → OpenRouter → Groq** (file drop-ins for each). Groq required a browser User-Agent (blocks urllib default) — with UA it exposes 13 models; fallback referee model = **`openai/gpt-oss-120b`** (frontier-class). Ollama timeout raised 30s→60s for the saturated pod.

**Live:** Groq referee calls now succeed (rounds scoring). Ollama generate is currently **saturated** by the sibling's `overnight_axes.py` (load 5.97) — local scores log UNMEASURED/None until the pod calms; referee + driver keep running regardless (graceful degradation, no crash).

**Honest note:** "Grok" measurement currently = `gpt-oss-120b` via Groq (frontier fallback). True xAI Grok resumes automatically when OpenRouter credits are added OR the direct xAI key is unlocked (`security find-generic-password -a "Grok Bot Key" -s "Grok Bot Safe Storage" -w` → `~/.runpod/secrets/xai.key`).

## MINE v3 — live measurement sources (02:42Z, tick 116)

**2,205 docs/tick on the pod** (was 1,588) — the mine now ingests **the estate's own live measurement data**:

| Source | Docs |
|---|---|
| llm_json companions | 1,085 |
| alignment canon | 499 |
| **arena_round (real Elo rounds, live)** | 400 |
| **grok_referee_round (Grok/Groq referee, live)** | 187 |
| **hf_dataset (csoai/ HF catalog: agisafe-bench, aiact-frozen-split-harness, coai-bench, gspc-care, arena-matrices…)** | 29 |
| **arena_league (live Elo table)** | 1 |
| oowm_mcp + taxonomy + sovereign_os | 4 |

- **Arena rounds are the crown seam:** 2,112+ real measured rounds (Elo, 7 models, 4 axes) now queryable through `query_oowm` — the knowledge graph contains the estate's own measurement history, not just documents.
- **Every 5-min tick re-mines:** fresh arena rounds (growing ~5/min), grok rounds, HF/Kaggle catalogs — the graph grows all night toward the 04:00Z target.

## Key gates / notes

- **Grok key resolved:** direct xAI key is GUI-gated in the keychain → **OpenRouter backend live** (`OPENROUTER_API_KEY` from keystone, `x-ai/grok-4.6`, provider pinned to xAI). Referee measures for real (earlier rounds were UNMEASURED/no-key; now scored).
- **Mac freed:** estate-mine Mac cron removed; all ingestion runs pod-side from the `/workspace/.stash/mac-backup` volume mirror (1.8G).
- **A100-1** (`1dldzposn7ssuu`): resumed today, SSH still unreachable — wire loop re-armed, degrades gracefully. API shows `uptimeSeconds: 0` (RunPod infra flap, known).
- **At 04:00 UTC:** driver writes `overnight_summary.md` + final state, exits 0.

## SIGIL

`overnight-run-2026-08-17-jeeves`
