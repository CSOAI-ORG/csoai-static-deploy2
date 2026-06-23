# Sovereign Town — the governed agent-world + data/attestation engine

A governed-vs-ungoverned agent-world simulation that doubles as a **data-moat flywheel**, an **IP engine**,
a **compliance-intelligence looking-glass**, and an **agent-identity (passport) layer** — our answer to
emergence.ai. Built 2026-06-19. Honest scope: **in-simulation (P0/P1), public archetypes only**, defensive-only,
ledger-only money, honest counts (27 personas / 12-around-1 council / 271 MCPs). Master plan:
`../SOVEREIGN_TOWN_MASTER_PLAN_2026-06-19.md`; full spec: `../SOVEREIGN_TOWN_POC_2026-06-19.md` (§1-16).

## The kernel — start here
`sovereign_os.py` is the **Governance OS control-plane** that unifies everything below:
`status` (unified dashboard) · `ps` (hives = processes) · `syscall <agent> <action>` (passport-gated permission
layer) · `verify <passport>` · `signal <hive> <alarm|trail> <msg>` (event bus) · `boot`. One interface over the
sim, passports, gate, bus, vault, models, ledger, Labs.

## The pieces (all in `p0_aqua/`)
| file | what it does |
|---|---|
| `sovereign_os.py` | **the OS kernel** — unified control-plane (status/ps/syscall/verify/signal/boot) |
| `sim.py` | 28-district governed-vs-ungoverned engine (needs/gate/contagion/commons/trust, block_rate regimes) |
| `batch.py` | parallel corpus generation (~750K episodes/s/10 cores) |
| `flywheel_forever.py` | **the 24/7 daemon** — ever-advancing seeds, singleton-locked, per-host (`--seed-base`), Ed25519 ledger, auto train+report+pack |
| `train_all_hives.py` | one sovereign threat model per hive (~0.99 acc) → `models/` |
| `jurisdiction.py` | **the Looking Glass** — pre-compute outcomes per regulatory regime (EU/US/UK/none) |
| `hive_pack.py` | each hive **eats its own industry** → signed industry pack → MEOK Labs |
| `agent_passport.py` | **the key** — signed offline-verifiable agent identity (King + 28 hives) |
| `gate_access.py` | **Zero-Trust gate** — passport-checked runtime access (grant/deny/quarantine) |
| `pheromone_bus.py` | **fleet nervous system** — cross-hive alarm propagation + trail diffusion (Ed25519) |
| `report.py` | publish per-hive whitepapers → MEOK Labs index |
| `sign_lib.py` / `verify_chain.py` | Ed25519 sign + offline chain verification |
| `data_moat.py` | Ingests real EU economic/regulatory data → `data_moat.json` → `sim.py` + `jurisdiction.py` |
| `attestation_moat.py` | Ingests MEOK compliance attestation audit events → `attestation_moat.json` → sim/dashboard |
| `threat_moat.py` | Ingests CISA KEV (+ optional MITRE ATT&CK) → `threat_moat.json` → sim/dashboard |
| `sanctions_moat.py` | Ingests OFAC SDN sanctions list → `sanctions_moat.json` → sim/dashboard |
| `psc_moat.py` | Ingests UK Companies House PSC snapshot → `psc_moat.json` → sim/dashboard (aggregate only) |
| `finance_moat.py` | Ingests FRED macro indicators → `finance_moat.json` → sim/dashboard |
| `agriculture_moat.py` | Ingests FAOSTAT Food Balance Sheets → `agriculture_moat.json` → sim/dashboard (aggregate only) |
| `energy_moat.py` | Ingests FRED energy price series → `energy_moat.json` → sim/dashboard |
| `climate_moat.py` | Ingests NOAA global temperature anomalies → `climate_moat.json` → sim/dashboard |
| `dashboard_server.py` | Starlette API + static server on `127.0.0.1:3940` — dashboard, 3D town, verifier, WebSocket ledger feed, benchmark harness proxy, MCP SSE proxy |
| `dashboard.html` | Live research dashboard with stats, hive directory, charts, ledger tail, server-side verifier |
| `benchmark/` | **Benchmark harness** — policy-vs-scenario A/B engine, signed run manifests, MCP server, Regulatory Workbench |
| `benchmark/server.py` | Harness REST + WebSocket server on `127.0.0.1:3941` — `/harness/run`, `/harness/leaderboard`, `/harness/runs/{id}`, `/harness/verify` |
| `benchmark/mcp_server.py` | MCP server exposing harness tools (`sov_benchmark_run`, `sov_benchmark_compare`, `sov_regulatory_classify`, `sov_world_info`, `sov_leaderboard`) |
| `benchmark/workbench.html` | **Regulatory Workbench** — run A/B lanes, sign runs, verify manifests, embedded MCP client |
| `../proofof-site/sovereign-town/leaderboard.html` | **Public signed leaderboard** with auto-refresh, scenario filter, and per-run detail links |
| `../proofof-site/sovereign-town/run.html` | **Signed run detail page** — human-readable manifest with validity badge, score bars, signature info |
| `API.md` | Endpoint reference for the JSON API, WebSocket feed, harness, and MCP proxy |
| `check.sh` | Pre-flight runner: `selftest.py` + `e2e_test.py` + optional `browser_test.py` (Playwright) |
| `town3d.html` | **Live 3D demo** — real-time governed-vs-ungoverned viewer, 28 hives, 140 agents, regime toggle |
| `town_sim_live.py` | Pre-computes a 21-day tick-by-tick timeline and streams it via WebSocket `/ws/feed` and `/api/town-state` |
| `../verify/index.html` | **public verifier** — anyone verifies a passport/attestation in-browser, no server |
| `../proofof-site/sovereign-town/fleet-status.html` | **Public, static** fleet-status mirror (safe for Vercel) |

## Tests

Three-layer regression guard:

```bash
cd p0_aqua
python3.11 selftest.py          # 47 unit/integration tests
python3.11 e2e_test.py          # 66 endpoint + WebSocket + MCP proxy checks with timing
./check.sh                      # runs selftest + e2e + optional Playwright browser tests
```

`e2e_test.py` covers content-type validation, CORS, 404/invalid flows, valid/tampered/missing verification, WebSocket regime switching, MCP SSE proxy handshake, signed run detail, and dashboard navigation.

Browser-level tests (`browser_test.py`) exercise real user flows in Chromium:
- dashboard navigation → workbench / leaderboard
- workbench MCP client: connect, list tools, call `sov_world_info`
- leaderboard → run detail page
- invalid run id error UX
- 3D town viewer canvas render

To run browser tests manually:
```bash
uv venv .venv-playwright
uv pip install --python .venv-playwright/bin/python playwright pytest pytest-playwright
.venv-playwright/bin/python -m playwright install chromium
.venv-playwright/bin/python -m pytest browser_test.py -v
```

## Run it
```
cd p0_aqua
python3.11 flywheel_forever.py --seed-base 200000000 --sleep 300   # the 24/7 fleet (Mac partition)
python3.11 jurisdiction.py        # the looking glass (regime outcomes)
python3.11 hive_pack.py           # every hive eats its industry
python3.11 agent_passport.py      # issue + verify agent passports
python3.11 gate_access.py         # zero-trust gate demo
python3.11 pheromone_bus.py       # cross-hive coordination demo
python3.11 data_moat.py           # derive sim/jurisdiction params from real EU data
python3.11 attestation_moat.py    # derive per-hive pass rates from MEOK attestations (needs MEOK_MASTER_API_KEY or export)
python3.11 threat_moat.py         # derive threat pressure from CISA KEV
python3.11 sanctions_moat.py      # derive compliance pressure from OFAC SDN
python3.11 psc_moat.py            # derive transparency pressure from UK PSC snapshot (VM, aggregate only)
python3.11 finance_moat.py        # derive financial stress / inflation from FRED
python3.11 agriculture_moat.py    # derive food security / scarcity from FAOSTAT
python3.11 energy_moat.py         # derive energy stress from FRED energy prices
python3.11 climate_moat.py        # derive climate pressure from NOAA temperature anomalies
python3.11 jurisdiction.py        # Looking Glass with data-grounded EU regime
python3.11 dashboard_server.py    # local dashboard + 3D town + WebSocket feed on :3940
```

## Dashboard & public surface
- **Local interactive dashboard:** `http://127.0.0.1:3940/dashboard` — real-time stats, hive directory, character explorer, ledger tail, server-side verifier. Auto-refreshes via WebSocket `/ws/feed` (fallback polling every 10–30s).
- **Regulatory Workbench:** `http://127.0.0.1:3940/workbench` — run A/B policy lanes against scenarios, publish Ed25519-signed manifests to the leaderboard, verify manifests, and drive the harness through an embedded **MCP client**.
- **Aethelgard Finance Hive API:** `http://127.0.0.1:3940/api/hive/aethelgard` — roster + state contract for `meok-ai/ui`.
- **BFT Council vote:** `http://127.0.0.1:3940/api/council/vote` — deterministic 5-member council votes.
- **Agent chat bridge:** `http://127.0.0.1:3940/agent/chat` — OpenAI-compatible proxy to FreeLLMAPI (requires `SOV_TOWN_FREELLMAPI_KEY`).
- **Policy Lab experiments:** `http://127.0.0.1:3940/experiments.html` — gallery + comparison widget.
- **MCP SSE server:** `http://127.0.0.1:3942/sse` — the harness exposed as MCP tools. The dashboard proxies it at `/mcp/sse` and `/mcp/messages/{session_id}` so external clients only need port `3940`.
- **Public signed leaderboard:** `http://127.0.0.1:3940/leaderboard` — auto-refreshes, filters by scenario, links each run to a human-readable detail page.
- **Operational metrics:** `http://127.0.0.1:3940/api/metrics` (JSON) and `http://127.0.0.1:3940/harness/metrics` (proxied) — request counts, latency p50/avg, WebSocket regime counts, and manifest throughput. Toggle structured access logs with `SOV_TOWN_ACCESS_LOG=1`.
- **Signed run detail:** `http://127.0.0.1:3940/run.html?id=<run_id>` — validity badge, score dimension bars, raw metrics, signature/pubkey, and raw JSON.
- **3D town viewer (live demo):** `http://127.0.0.1:3940/town3d` — real-time Three.js view of all 28 hives and 140 personas. The headless Python sim (`town_sim_live.py`) pre-computes a 21-day governed/ungoverned timeline; the viewer receives one tick per second over WebSocket `/ws/feed`. Use the **Governed / Ungoverned** toggle to watch the same world split: governed keeps commons intact and crimes at zero, while ungoverned collapses into theft, lawlessness, and trust erosion during the scarcity week. Agent orbs change color and position by action; the action log surfaces crimes in real time.
- **Policy Lab:** `python3.11 policy_lab.py vote|spawn|status|report` — BFT council votes on experiments, spawns live A/B harness runs, and exports regulator-ready whitepapers/briefs/emails (see `experiments/dora_finance.json`).
- **Public static mirror: `https://proofof.ai/sovereign-town/fleet-status.html` — updated every 10 minutes by the Mac/VM status runners. **Decision:** `/dashboard` is kept local-only because the live ledger and full API contain host-specific, non-public data; the static `fleet-status.html` is the public-safe view.
- **LaunchAgents:**
  - `com.csoai.sovereign-town-dashboard` keeps `dashboard_server.py` alive on `:3940`.
  - `com.csoai.sovereign-town-harness` keeps `benchmark/server.py` alive on `:3941`.
  - `com.csoai.sovereign-town-mcp-sse` keeps the MCP SSE server alive on `:3942`.
- **Data moat:** `data_moat.py` reads public EU aggregate datasets (`~/clawd/eu_data/`) and writes `p0_aqua/data_moat.json`. `sim.py` and `jurisdiction.py` load this file to ground scarcity/contagion and the EU regime strength in real economic indicators. No personal data is used.
- **Attestation moat:** `attestation_moat.py` reads the MEOK Attestation API audit ledger (public `/api/audit` endpoint, requires `MEOK_MASTER_API_KEY`) or a local export, maps each regulation to the relevant hives, and writes `p0_aqua/attestation_moat.json`. The dashboard shows per-regime pass rates and linked hives. Only aggregate statistics are emitted.
- **Threat moat:** `threat_moat.py` fetches the CISA Known Exploited Vulnerabilities catalog (free, no key), maps CVEs onto security/governance hives, and writes `p0_aqua/threat_moat.json`. `sim.py` uses this to set baseline lawlessness and boost contagion; `jurisdiction.py` erodes effective enforcement under high threat pressure. Dashboard exposes `/api/threat`.
- **Sanctions moat:** `sanctions_moat.py` fetches the US Treasury OFAC SDN list (free, no key), maps sanction programs onto governance/security/privacy hives, and writes `p0_aqua/sanctions_moat.json`. `sim.py` uses this to boost regime enforcement; `jurisdiction.py` tightens effective enforcement under high compliance pressure. Dashboard exposes `/api/sanctions`.
- **UK PSC moat:** `psc_moat.py` reads the UK Companies House Persons with Significant Control snapshot (OGL-UK-3.0, currently on the VM at `/data/hive-data/.hive/data/government/companies_house_psc/`), streams ~15.6 M records, and emits **aggregate-only** statistics to `p0_aqua/psc_moat.json`. No names, full DOBs, full addresses, or postcodes are written. `sim.py` uses ownership-concentration signals to tune scarcity; `jurisdiction.py` tightens enforcement under transparency pressure. Dashboard exposes `/api/psc`.
- **Finance moat:** `finance_moat.py` fetches public US macro series from the St. Louis Fed FRED (GDP, unemployment, CPI, VIX, yield curve, Fed funds) without an API key, and writes `p0_aqua/finance_moat.json`. `sim.py` uses financial stress to lift baseline lawlessness and contagion sensitivity; `jurisdiction.py` weakens effective enforcement under high stress. Dashboard exposes `/api/finance`.
- **Agriculture moat:** `agriculture_moat.py` downloads the FAOSTAT Food Balance Sheets bulk ZIP (no key) and streams ~300 MB of csv to emit aggregate food-supply, production-by-category, import-dependency, and fish/seafood statistics to `p0_aqua/agriculture_moat.json`. No farm- or country-level records are emitted. `sim.py` uses food security and scarcity to tune the scarcity multiplier; `jurisdiction.py` tightens enforcement when food security is below benchmark. Dashboard exposes `/api/agriculture`.
- **Energy moat:** `energy_moat.py` fetches public FRED energy price series (WTI crude, Henry Hub natural gas, regular gasoline, electricity CPI) without an API key, and writes `p0_aqua/energy_moat.json`. `sim.py` uses energy stress to raise scarcity and contagion; `jurisdiction.py` weakens effective enforcement under high energy stress. Dashboard exposes `/api/energy`.
- **Climate moat:** `climate_moat.py` fetches NOAA global land+ocean temperature anomalies without an API key, and writes `p0_aqua/climate_moat.json`. `sim.py` uses climate pressure to increase scarcity and baseline fragility; `jurisdiction.py` tightens enforcement under climate pressure. Dashboard exposes `/api/climate`.

## Fleet (24/7, 3 hosts, disjoint seeds → no duplicate data)
- **VM** `meok-backend` seed-base 0 (systemd-style nohup + `@reboot` cron) · **Mac** seed-base 200M · **Actions** seed-base 100M (nightly, on `main`).
- Stop: `pkill -f flywheel_forever` (Mac) / `ssh meok-backend pkill -f flywheel_forever` (VM). Status: `fleet_status_*.json`.

## Bright lines (non-negotiable — see spec §16)
Public data only · every output labelled SIMULATION/prediction (never assert a named real firm is non-compliant) ·
opt-IN before contacting any entity · regulators get anonymized/aggregate + wind-tunnel-the-RULE (not name-and-shame) ·
consent-vault not surveillance · space = governance lane (no ISS collection) · defensive-only (no offensive/"worm") ·
no real money without legal sign-off · honest counts.

## Gated on Nick (deploys/credentials/legal — never done silently)
- Submit GPU credit applications (NVIDIA/DO/MS — needs company identity).
- Public openpatent push (7 inventions live in local 6-layer registry; publishing IP is your decision).
- Deploy `verify/` + the showcase to Vercel; VM crash-watchdog cron (you authorized `@reboot` only).
