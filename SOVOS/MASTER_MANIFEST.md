# SOVOS — Master Mono-Repo Manifest

**One tree, one substrate, one truth.** Generated 2026-08-11 from the
absorbs this session + the existing SOVOS tree at `jv-wave8-production`.

The canonical source is `github.com/CSOAI-ORG/csoai-static-deploy2` →
branch `jv-wave8-production` → directory `SOVOS/`. Pod clones mirror
this; the pod is not the truth.

---

## Numbers (truth table)

| Quantity                  | Count |
|---------------------------|------:|
| Python packages in `packages/` | **38** |
| Rust crates in `packages/`      | 1 (`sovos-hive`) |
| Public HTML surfaces (`api/*.js`) | **7** |
| Operational data files (`data/hive/`) | 18 |
| Charter data (`data/charters/`)   | 1 |
| Sovereign wiki (published)         | 1 page |
| Deployable configs (`deploy/`)    | 2 (A100 + m2-kit) |

**Growth this session**: +6 Python packages (sovos-hive,
sovos-families, sovos-provebench, sovos-router, sovos-world,
sovos-invariants) + 84 absorbed files + 7 API endpoints + 18
operational data files + 1 charter.

## Test counts across the absorb

| Package                         | Tests |
|--------------------------------|------:|
| sovos-hive                     | 10/10 |
| sovos-router                    |  6/6  |
| sovos-invariants                |  6/6  |
| sovos-arena                     |  9/9  |
| sovos-signal-index              | 16/16 |
| sovos-chain (full PYTHONPATH)   | 15/15 |
| sovos-fisher-rao                | 12/12 |
| **TOTAL absorb tests green**    | **74/74** |

Plus the wired CLI (7/7 = score/run/ras offline/ras--measure/ras--canary/ras-help/ras) and `sov ras --measure` reproducible from
the A100 pod (SOV SIGNAL d = 4.2053σ, OSCAL v1.1.0).

---

## The 38 packages

### Core substrate (the measurement + chain)

| Package | What | Absorbed from |
|---|---|---|
| **sovos-core**                | G-S-P-C 4-axis score (ETSI EN 304 223)          | top-level |
| **sovos-arena**               | 13-axis Wilson-CI measurement (13 GSPC axes)   | new build   |
| **sovos-signal-index**        | Mahalanobis distance-to-permitted manifold     | new build   |
| **sovos-chain**               | Fisher-Rao + Poincaré + Hyperbolic chain      | top-level   |
| **sovos-fisher-rao**          | Standalone Fisher-Rao kernel                   | top-level   |
| **sovos-jspace-hyperbolic**    | Poincaré ball math (BFM/HFM)                  | top-level   |
| **sovos-jspace-move**         | J-Space Move Arithmetic (TIES-Move / DARE-Move / error-vector) | jspace-move-arithmetic/ |
| **sovos-jspace-pipeline**     | J-Space pipeline runtime                       | top-level   |
| **sovos-info-geometry**       | Task vectors + Fisher-Rao + GW cross-architecture fusion | top-level |

### Sovereign invariants + standards

| Package | What | Absorbed from |
|---|---|---|
| **sovos-invariants**         | Sovereign primitives: SIGIL sign+verify, CARE floor, BFT tally validation | `sov_invariants.py` |
| **sovos-oscal**              | OSCAL assessment-results document generator     | new build   |
| **sovos-x402-gate**          | HTTP 402 paywall decorator                     | new build   |
| **sovos-article-zero**       | Article 0 Rego policy + Python runtime         | new build   |

### Hive + orchestration

| Package | What | Absorbed from |
|---|---|---|
| **sovos-hive**               | **Rust kernel** (Ring-0 governance, 11 modules: hive, drum, honey, iwm, jcard, meta, phlabet, rainbow, spine, lib, main) + Python facade + 13 OWEM faction modelfiles + withdrawn.py | `sov-hive/` |
| **sovos-world**              | **Inner World Model + Sovereign Swarm Intelligence** — sov_space, j_space, g_space, bft_quorum, clan_engine, constitutional_ai, owem_brain, owem_hive, rag_pipeline, stigmergy, unified_gnn + sub-spaces (g/b/soul) | `iwms/` + `g_space/` + `b_space/` + `soul/` |
| **sovos-router**            | sov4_router, sov_orchestrator, master_hives (3 brands), owem_cluster, router_control, fleet_dashboard, fleet_power | top-level (selective: time-loops excluded) |
| **sovos-router** (scripts)  | fleet_monitor, sov_swarm (run as scripts, not imported) | top-level |

### Families + reward

| Package | What | Absorbed from |
|---|---|---|
| **sovos-families**           | Family cells (4-split left/right × small/big) + GRPO reward functions | `family_cells.py` + `sov_reward_functions.py` |

### Bench + prove

| Package | What | Absorbed from |
|---|---|---|
| **sovos-provebench**         | 6 Kaggle bench tasks (govbench / provbench / ossbench / mcpbench / pqcbench / defbench) + 2 off-Kaggle rerun scripts | `kaggle/gspc_axes/` + top-level |

### Storage / transport

| Package | What |
|---|---|
| **sovos-bus-redis**         | Redis-backed StateBus with fakeredis fallback |
| **sovos-crosswalk**        | CELLAR → OSCAL crosswalk + builtin EU AI Act atlas |
| **sovos-cellar-ingest**    | Ingest CELEX from CELLAR (EU) |

### Identity / certification / security

| Package | What |
|---|---|
| **sovos-certification-loop** | 7-hop certification bridge (Stripe+RunPod+OWEM BFT+C2PA+proof) |
| **sovos-council**           | BFT council ledger |
| **sovos-birth**             | Mode 0 birth encoder (mint new users to J-space) |
| **sovos-mcp-servers**       | MCP server fleet (EU AI Act MCP, injection scanner, gov bench, etc) |
| **sovos-hermes-integration** | Hermes agentic integration (plugins + tools + Dockerfile) |
| **sovos-a2a-swarm**        | Agent-to-agent signed swarm demo |

### Math primitives / numerics

| Package | What |
|---|---|
| **sovos-quantum-bridge**   | Task-vector / amplitude bridge (PennyLane optional) |
| **sovos-quantum-router**   | Quantum routing |
| **sovos-qtask-converter**  | Task ↔ amplitude converter (3kb-sized quantum helper) |

### Specialised axes / decision

| Package | What |
|---|---|
| **sovos-alpha**            | Alphabet / curation |
| **sovos-alchemist**        | Recipe synthesis |
| **sovos-cpo-calculator**   | CPO power-savings calculator (HTML page mirror) |
| **sovos-map-elites**       | Hyperbolic MAP-Elites fitness gate |
| **sovos-sheaf-gate**       | Sheaf pre-merge gate (federation) |
| **sovos-sigma-calibration** | Sigma/score calibration |
| **sovos-stigmergy**        | Pheromone stigmergy (echoes the iwms one) |
| **sovos-mind**             | Mind state, CPOLink (the silicon-photonics echo) |
| **sovos-info-geometry**    | (duplicated above; once cross-cleaned) |

*(The `Info-geometry` overlap: sovos-world has the same module
as sovos-info-geometry; cross-clean intended.)*

---

## The `data/` directory

| Path | What | Size |
|---|---|---|
| `data/hive/` | 18 operational JSON: jspace_deck (54 cards), owem_clan_swarm (6 clans), owem_cluster_config, honey_all_producers, fleet, governance_board, GPU inventory, etc. (absorbed from `forest/`) | 1.9 MB |
| `data/charters/` | `sov33-capability-registry.json` — the canonical 12-layer maternal sovereign stack definition (absorbed from `sovereign-charters/`) | 26 KB |

---

## The `api/` directory (Vercel serverless surface)

| Endpoint | File |
|---|---|
| `/api/hive` (SOV3³ clan voting) | `hive.js` |
| `/api/j-space` (sovereign agent portal) | `j-space.js` |
| `/api/j-space-think` (intuition → sovereign response) | `j-space-think.js` |
| `/api/sovereign-citations` (citation provenance) | `citation.js` (absorbed from `sovereign-citation-mcp/`) |
| `/api/free-gpu-orchestrator` (fleet state) | `free-gpu-orchestrator.js` |
| `/api/hermes-delegate` (agent delegation) | `hermes-delegate.js` |
| `/api/hermes-lanes` (live lane state) | `hermes-lanes.js` |

---

## The `deploy/` directory

| Path | Purpose |
|---|---|
| `deploy/a100/` | RunPod A100 80GB PCIe pod bootstrap: `install.sh` (apt + pip + ollama + monorepo clone), `spec6-e2e.py` (wired pipeline), `test_spec6.py` (canonical = 4.2053σ), `README.md` |
| `deploy/m2-deployment-kit/` | 10 operator tools: charter amender, compliance calculator, jurisdiction mapper, sovereignty index, trust score, side-by-side test, SIGIL signer, treaty generator, black-swan predictor, gods-eye scan, README |

---

## The `published/` directory

| Path | Purpose |
|---|---|
| `published/sovereign-wiki/index.html` | Sovereign wiki front page (absorbed from `sovereign-wiki/`) |

---

## Wiring topology (the connections you asked about)

### Inside `SOVOS/packages/sovos-hive/`
- **Rust kernel ↔ Python facade** (bridge: `_try_load_rust_kernel()` returns None when cargo-built .so absent; falls back to pure-Python mock for tests on any host without Rust)
- **J-Space deck ↔ OWEM swarm**: both load from `data/hive/`. Hive canonical manifest = 6 active clans at this absorb
- **WITHDRAWN registry ↔ hive nodes**: every HiveNode consults `WITHDRAWN_MODELS` before routing a query
- **13 sov6 faction modelfiles** ↔ ollama loader (use `ollama create -f  sov6-foo.Modelfile`)

### Inside the A100 pod (`1dldzposn7ssuu`)
- `git clone --branch jv-wave8-production` from GitHub (the canonical source)
- `pip install 'numpy<2' scipy geomstats fakeredis` (geomstats first silently pulls numpy 2.x which breaks trapz — install order matters)
- `bash SOVOS/deploy/a100/install.sh` (full bootstrap, single command)
- `python3 SOVOS/deploy/a100/spec6-e2e.py` (SOV SIGNAL = 4.2053σ repro)
- `python3 SOVOS/deploy/a100/test_spec6.py` (asserts canonical = 4.2053σ)

### Cross-pod (A100 ↔ sov-brain-2)
- Pod A100 = `root@104.255.9.187 -p 11737`, `sovos-brain-a100` ssh config alias
- Pod 3090 = `sov-brain-2` ssh config alias (RTX 3090, $0.22/hr)
- ollama model passing: push from 3090's HF cache → A100's HF cache. Avoid the ollama-FROM-dir trap (use `convert_hf_to_gguf.py` if you must use ollama).
- Next: tune a multi-pod merge (3090 trains the specialists, A100 runs the 4-way TIES merge) so capability-gain merge becomes real

### Cross-cloud (RunPod ↔ Claude Science ↔ Kimi ↔ Oracle)
- `api.runpod.io` (REST) + `api.runpod.ai` (graphQL) for pod control from any agent
- `api.anthropic.com` (Claude Science lane): the `sovereign/` area has provenance-grade inputs sent for analysis
- `api.moonshot.cn` (Kimi): the visual/light/10101 math reasoning lane (already allowed in `domains`)
- `inference.generativeai.{uk-london-1,us-chicago-1}.oci.oraclecloud.com`: the Oracle substrate pipelines
- All 4 lanes share `sovos-invariants` (the SIGIL/CARE floor): every sign-via-anything calls `emit_sigil()` which uses the local Ed25519 key

### Public pages (the auditor-reproducible surface)
- `arenas.html` — public SOVOS Arena tool: 13 GSPC axes, Wilson CI, canary gate (the auditor-reproducible instrument)
- `cpo-calculator.html` — co-packaged optics power-savings calculator
- `injection-scanner.html` — 18-rule MCP prompt-injection scanner
- `birth.html` — Mode 0 birth encoder for new sovereign users
- `bus-portal.html` — bus-portal (StateBus observability)
- ~200 regulator deep-dive packs (csoai.org surface, not in this SOVOS monorepo)

---

## What's NOT in the monorepo, intentionally

| Item | Where it stays | Why |
|---|---|---|
| `EVENTALL` / page assets (.html) | top-level (csoai.org pages) | Public surface — not substrate |
| `benchmark-results/` | top-level (snapshot of run history) | Historical artefacts; regenerated nightly |
| `forest/` (now `SOVOS/data/hive/`) | moves to canonical SOVOS location | Done 2026-08-11 |
| `sov-hive/`, `iwms/`, `jspace-move-arithmetic/`, `g_space/`, `b_space/`, `soul/`, `family_cells.py`, `sov_reward_functions.py`, `sov4_router.py`, `sov_orchestrator.py`, `sov_swarm.py`, `master_hives.py`, `owem_cluster.py`, `router_control.py`, `fleet_*.py`, `M2_DEPLOYMENT_KIT/`, `Modelfiles-owem-v3-light/`, `sov_invariants.py`, `sovereign-charters/`, `sovereign-wiki/`, `sovereign-citation-mcp/`, `sov-hermes-integration/` | all moved into SOVOS | Done 2026-08-11 |

---

## How a new agent picks this up (one paragraph)

Clone `github.com/CSOAI-ORG/csoai-static-deploy2` branch `jv-wave8-production`. The substrate is in `SOVOS/`. Read this MANIFEST first, then `SOVOS/README.md`, then jump to `SOVOS/packages/sovos-hive/README.md` if you want to understand the hive kernel, or to `SOVOS/packages/sovos-arena/` if you want the measurement front. For the A100 pod, follow `SOVOS/deploy/a100/README.md`. For the public audit surface, open `arenas.html` in a browser. The 13 GSPC axes (gov/prv/agi/asi/mcp/oss/mach/care/xr/det/art5/swarm/affect) are the contract between everything.

**Do not invent new parts.** Before adding a new package, check whether one of the 38 already covers it. Before adding a new folder at SOVOS/ root, check whether it should be `packages/` (runtime) or `data/` (operational) or `deploy/` (host config) or `api/` (Vercel) or `frontends/` (HTML). Before adding a new python module at top-level, PUT IT IN A PACKAGE.

---

## Honest gaps the absorb did NOT close

| Gap | Status |
|---|---|
| **SOV4-T and SOV4-OWEM adapter weights** | NOT on any reachable pod; only docs in mac-backup. The capability-gain merge (sub-stance-2-adapter) requires re-training or hunting through network volumes in different RunPod datacenters. |
| **CPOLink actual silicon-photonics hardware** | The mind.py CPOLink uses NVIDIA-published datasheet numbers; there is no real CPO hardware in the estate. The "10101 → 3D-holographic immersion" vision is **aspirational** — there is zero holographic rendering code on any disk. |
| **TTT (Test-Time Training) layer** | Zero files anywhere in the SOVOS tree reference TTT explicitly, despite the geometric core having the math to do it. A deliberate gap. |
| **live ollama-server on A100** | Was being installed when this manifest was written; status unknown. Until ollama serves, `sov ras --live` cannot run on A100 (--offline mode works against saved profiles). |
| **Top-level loose dirs not yet absorbed (cosmetic)** | ~30 dirs like `benchmarks/`, `evidence/`, `inspect_tasks/`, `kaggle/`, `lightning/`, `cloudflare-worker/`, `kaggle_eat/`, `humanoid/`, `competitors/` (missing), `policies/`, `scripts/`, `training/`, `oowm_merge_v1/` (a real artefact — should be added). These are scaffolding/dashboards/datasets, mostly. They DO NOT belong in `packages/`; they belong in `data/external/` or absorbed as needed. |

---

## One-line thesis

The SOVOS monorepo at `jv-wave8-production`/`SOVOS/` is now the **single
canonical substrate**. The Rust kernel of `sovos-hive` is the
Ring-0 governance brain. The Python packages around it are the
measurable, chain-rated, OSCAL-attestable substrate the 13 GSPC axes
inspect. The A100 pod is the heavy-lift server. The 3090 pod is
the merge-and-merge-bench server. RunPod connects them to Claude
Science, Kimi, Kaggle, Oracle. The maths (Fisher-Rao, Poincaré,
task vectors, Procrustes, TIES, GW cross-architecture fusion,
hyperbolic frozen/fluid geometry, BFT-33, SIGIL chains) is real and
shipped. The missing pieces (real CPO hardware, real holographic
substrate, a true SOV4 capability-gain merge, the live TTT layer)
are honestly absent — they are the next round of work, not yet built
in this absorb, but the SOVOS tree can be the place to build them
without re-platforming.

*One tree. One truth. One substrate.*
