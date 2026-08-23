# DSH ↔ Sovereign Estate Integration — Landscape (2026-08-22)

Verified this session. This is the map of the sovereign model estate now wired into
DeepSeek Harness (DSH), so everything can be built off `~/.dsh` as the hub.

## The Sovereign OS architecture

**SOV SPACE** (`~/sov-space`) = the "Sovereign OS visual mind" — a binary mesh binding every
model clan (Kimi, Claude, DeepSeek, Grok, Gemini, SOV3 …) into one governable world, rendered
as a live **VWM** (Visual World Model) over **IWM** (Infinite World Memory).

- **IWM** — fractal quadtree addressing `(epoch, scale, x, y, z, w)` packed to a 128-bit key.
  Descend `scale` to zoom in, ascend to the whole world.
- **SovNode** — a logical agent projected to a ~541-byte `VisualNode` the VWM draws.
- **Protocol** — `[opcode][len][zstd payload]`, no JSON on the hot path.
- **Router** — cost/latency/quality-aware pick over the 2026 provider table.
- **Store** — DOL-like append-only records (zstd, FNV-1a content hash = the honey H-address).

Workspace crates: `sov-core` (Ring-0 core), `sovd` (demo daemon → `scene.json`),
`sov-honey` (ingests `honey_*.jsonl` → IWM), `sov-render` (VWM renderer, **gated to RunPod**).

**Operating principle (from the Claude lane):** *Honesty is architectural* — `UNMEASURED ≠ 0`,
never fabricate a record we did not produce.

### Name map (what the acronyms refer to in this tree)
- **SOVOS** — the Sovereign OS (the visual-mind sovereign OS + revenue rails endpoint).
- **OOWM** — Organic Open World Model (has MCP bridges: `sov3-oowm-mcp`, `meok-sovereign-oowm-mcp`).
- **OWEM** — the OWEM model family; runs on the Oracle micro **`sov33-owem-micro`** (145.241.232.16),
  serves 139 sovereign models (MCP: `meok-sovereign-owem-bridge-mcp`).
- **OLM** — the sovereign autonomous brain (Mamba-2 + MoE + attention + BFT council + Ed25519 sigil),
  on the GCP VM (`olm_autonomous_brain.py`, `/home/nicholas/sov3/`).
- These acronyms appear in MCP server names and pod names throughout `~/clawd/mcp-marketplace/` and
  `~/sov-space`; no single canonical glossary file was found, so names above are from the tree + AGENTS.md.

## Model estate wired into DSH (every advertised model verified present on its endpoint)

### 1. runpod-a100 — `sovos-light-master-mine` (tunnel `38.128.232.57:15094` → `127.0.0.1:11434`)
11 models (flagship inference): `sov33-unified`, `sov33-ultimate-sovereign`, `muse-glimmer`,
`mistral:7b`, `qwen3:8b`, `deepseek-r1:8b`, `nemotron-3-nano:30b`, `council-oowm`, `llama3.2:3b`,
`qwen2.5:0.5b`, `qwen2:0.5b`.

### 2. owem-estate — `sov33-owem-micro` (tunnel `145.241.232.16` → `127.0.0.1:11436`)
**73 models wired** (139 total on the endpoint). Families:
- **`sov33`** (16) — `sov33-unified`, `sov33-v7`, `sov33-v6`, `sov33-evolved`, `sov33-oracle`, `sov33-dist-*`
- **`sov-*`** (34) — task models: `sov-reasoning`, `sov-research`, `sov-math`, `sov-code`, `sov-vision`,
  `sov-compliance`, `sov-ethics`, `sov-defense-v2`, `sov-infra`, `sov-knowledge`, `sov-sovereign-v4`,
  `sov-general`, `sov-embedding`, `sov-gemma`, `sov-phi`, `sov-qwen`, `sov-nemotron`, `sov-minimax`, …
- **`sov-draw`** (6) — `sov-draw-{compliance,cybersecurity,sovereignty}` (+ `-terse`)
- **`clan-sovereignty`** (16) — `clan-sovereignty-{plain,cited,refusing,operational,evidential,risk_first,…}`
- (not wired but present: `clan-{redress,law,meok,defoneos,csoai}` × 12 each, plus mined/embed models)

The `clan-*` families are the measurement/safety variant families per DEFONEOS compartment
(sovereignty, redress, law, meok, defoneos, csoai), each tuned to a distinct grading behaviour
(`-plain`, `-cited`, `-refusing`, `-operational`, `-evidential`, `-adversarial`, `-stepwise`, …).

## DSH config (the hub)

- `~/.dsh/settings.yaml`
  - `llm-pi-ai`: 12 catalog vendors (anthropic, google, openai, groq, mistral, together, xai,
    moonshotai, minimax, zai, xiaomi, openrouter), each `apiKeyEnv` → key in `~/.dsh/.env`.
  - `llm-pi-ai-estate`: `runpod-a100` (11 verified models) + `owem-estate` (73 verified models).
  - Default model: `deepseek-official` / `deepseek-v4-flash-vision-exp`.
- `~/.dsh/.env` (0600) — ~46 keys; values managed by the sibling agent; DSH references them by name.
- `~/.ssh/config` — hosts: `meok-backend`, `m2`, `oracle-micro`, `oracle-micro-2`, `sov-brain-2`,
  `redblue-pod`, `sovos-light-a100` (port fixed 15094), RunPod proxy hosts.
- DSH MCP client (already wired, proven): `council-measure` (streamable-http) in
  `~/.dsh/profiles/web/cordis.patch.yml` → provides `mcp__council-measure__*` tools.

## Roadmap state (from `~/sov-space/PLAN.md`)
- **Phase A — Core** ✅ (IWM addressing, node/protocol/router/store, `sovd` demo, honey ingestion).
- **Phase B — VWM renderer** (wgpu) — RunPod-gated (billing Nick-gate).
- **Phase C — Eat/honey loop** — RunPod + Oracle-gated.
- Cross-cutting: fiber `sov-town` live sim into the mesh; claim/settle `oracle-micro-2`.

## SOV3 / Sovereign Temple substrate (from `clawd`)
- **SOV3** = Sovereign Temple (BFT-mesh v2.0). Runs on **:3101**; MCP endpoint `http://localhost:3101/mcp`.
  Two implementations: `sovereign-temple/` (Docker) and `sovereign-temple-live/` (Python 3.9 +
  Homebrew PostgreSQL 15 + pgvector, via `run-local.sh` — Docker is currently down).
- **`sov` CLI**: `sov status`, `sov health`, `sov council`, `sov agent`, `sov hunt`, `sov logs`, `sov restart`.
- **Orion-Riri-Hourman agent** (`sovereign-temple-live/agents/orion_riri_hourman.py`) — task hunter.
- **Status right now:** SOV3 :3101 is **DOWN** (GCP VM `meok-backend` billing-gated → the `:3101` SSH
  tunnel is dead), and Sovereign Temple public MCP (`sovereign.templeman-opticians.com/mcp`) returns **502**
  (cloudflared tunnel up, origin down). Both are the known **Nick billing-gate**, not fixable here.
  Once billing is restored → `launchctl kickstart` the `com.meok.*` tunnels / `ssh -L 3101` → SOV3 returns.
- **Layer-0 substrate scorecard** (canonical): 8 protocols at 100/100 (P1 MCP Federation · P2 Legacy Bridges ·
  P3 A2A · P4 x402 Payments · P5 SIGIL Attestation · P6 OSCAL/FedRAMP · P7 BFT Council · P8 Compliance Passport).
  ~531 MCPs, 479 ship-ready, 15 repos, 30 MCP servers wired.

## MCP / tool topology (reachable now)
| Server | Endpoint / spawn | Status | In DSH? |
|---|---|---|---|
| `council-measure` | streamable-http → csoai-gspc-mcp workers.dev | 200 | ✅ wired (`mcp__council-measure__*`) |
| `sov3-oowm-mcp` | (mcp-marketplace) | — | no |
| `meok-sovereign-owem-bridge-mcp` | (mcp-marketplace) | — | no |
| `sov3-bridge` | `~/.hermes/mcp-servers/sov3-bridge/mcp_server.py` | running | no |
| Sovereign Temple | :3101 / HTTPS /mcp | **down** (billing gate) | no |
| sov-gateway :8080 | OpenAI-compat (`SOV_GATEWAY_KEY`) | 200, auth-gated | no (thin wrapper of runpod-a100) |

## Session fixes already applied (background)
- Root cause of "chats not loading" = disk exhaustion → freed 2.8Gi→7.0Gi (temp files,
  npm/pip/homebrew caches, HF hub cache). DSH latency 0.09s→0.005s.
- Fixed `sovos-light-a100` SSH port (40637→15094).
- Removed phantom `runpod-a100` models (5 missing) → 11 verified present.
- **Powerhouse verification (this session):** `sov33-unified` on runpod-a100 generates (11.6s;
  identifies as "SOV-UNIFIED"); `sov33-ultimate-sovereign` generates (14s). `sov33-unified` guardrails
  on probe-style prompts ("can't fulfill") — normal for a safety-tuned sovereign model.
- **owem-estate :11436 is CPU-slow** (oracle Ampere, >60s even for trivial prompts) → added
  `timeoutMs: 180000` + `streamIdleTimeoutMs: 180000` to the provider so DSH waits instead of dropping.
- Gating note: SOV3 `:3101`, Sovereign Temple MCP, `sov3-bridge` and `meek-sov3-*` MCP servers all
  proxy to SOV3 `:3101` which is **down (GCP billing gate)** → NOT wired (would create broken tools).
- Backups: `~/.dsh/_backup-20260822-054930/`, settings `.bak-owem-*`, `~/.ssh/config.bak-*`.
