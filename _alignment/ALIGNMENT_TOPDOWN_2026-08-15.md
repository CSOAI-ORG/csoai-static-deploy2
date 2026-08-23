# v49.3 TOP-DOWN ALIGNMENT — 15 Aug 2026
## Council City + Arena + Clans + OOWM/OWEM/IWM/OWM/VWM — Phased EAT

**Source inputs:**
- `compass_artifact_wf-fcd910e6...` — Signed recomputable cards + BMR/Daily Agent Economy Index (regulatory + signing standards)
- `compass_artifact_wf-9963b77e...` — Master Blueprint: Matchup Matrix on a Signed Measurement Spine (fork-and-bind plan)

**Mode:** LEARN ALIGN (top-down). Then EAT ALL phases.

---

## WHAT WE HAVE TODAY (substrate state 15 Aug 2026)

**ALREADY LIVE on csoai-site.pages.dev (CF Pages):**
- `/api/sov-arena/rounds.jsonl` — **400 arena rounds** streaming live (321 ai-vs-ai + 79 human-vs-ai)
- `/api/sov-openttd/state.jsonl` — **272 lines** OpenTTD substrate ticks
- `/api/health` — phase 100, 752 pages
- `/pulse.html` (10.8KB) — wired to live arena + openttd
- `/experiments.html` (13.5KB) — wired to live arena
- `/arena_public.html` (9.2KB) — full live rounds dashboard
- `/sovereign-os.html` (21.5KB) — 5 worlds (OOWM/OWEM/IWM/OWM/VWM) anchor
- `/sov-city-3d.html` (17.2KB) — Council City 3D with clan districts
- `/bft33-live.html` — 33-voter council visualization

**ALREADY BUILT on disk:**
- `/spine` — `kimi-regen/spine.py` (J-card graph retrieval) + `sov-hive/src/spine.rs` (Rust core). **LACKS:** signing, card types, sigils, canonical JSON, Ed25519.
- 6 fleet clans active (csoai-adversarial/cited, defoneos-precise, law-adversarial, meok-operational, sovereignty-evidential)
- Fleet running on oracle-micro-2; OpenTTD city substrate live
- `sov-city/moa/` — MoA fusion, `sov-city/crdt/` — CRDT federation, `sov-city/runs/` — overnight E2E

**MCPs SHIPPED this turn (v49):**
- meok-sovereign-experiment-mcp (5 tools, 11/11 tests) — Wilson + McNemar
- meok-sovereign-pulse-mcp (5 tools, 9/9 tests) — heartbeat, BPM, drift

**GAPS to fill per compass:**
- Spine lacks: **canonical JSON (RFC 8785) + SHA-256 + detached sigs + DSSE/Sigstore/Rekor integration**
- Spine lacks: **honey-data card type** for training-pair provenance
- No fork of `a16z-infra/ai-town` or `joonspk-research/generative_agents`
- No `/fabric` eval layer wired to spine
- No `Prolific MCP` (human arm)
- No `/clients` router for paired parallel-world runs

---

## PHASED EAT PLAN (aligning to compass)

### Phase 0 — Gates before code [GATED]
- [GATED-counsel] Public-naming firewall (Council of AI + MEOK only). Internal codenames stay internal.
- [GATED-DPIA] Consent posture for human-cell data (UK GDPR lawful basis).
- **BUILD: extend spine.py → spine_v2.py with:**
  - RFC 8785 canonical JSON serialisation
  - SHA-256 content addressing (CID)
  - Ed25519 detached signatures (use `nacl.signing` or fallback to hash-sig)
  - Card kinds: `measurement` (existing), `honey-data` (NEW), `arena-round` (NEW), `provenance` (existing attestation)

### Phase 1 — AI-vs-AI, the only near-REAL cell (wiring)
- Fork **`a16z-infra/ai-town`** (MIT) + **`joonspk-research/generative_agents`** (Apache-2.0, strip assets)
- Wrap as MCP servers exposing `run_scenario(seed, scenario, axes)`
- Bind to `/fabric` (helm + lm-evaluation-harness + FastChat battle)
- Add red/blue roles via MeltingPot focal/background pattern
- **Threshold to proceed:** signed card from AI-vs-AI cell that an external party recomputes

### Phase 2 — Human-vs-AI (wiring + consent gate)
- Wire Prolific MCP (preferred: consent, fair pay, £6/$8 min, 33.3-42.8% fee)
- FastChat battle/vote pattern for human judges
- Human arm = **calibration anchor** (sampled cadence, NEVER in live path)

### Phase 3 — Collective tiers (new build)
- MeltingPot (Apache-2.0) + OpenSpiel (Apache-2.0) + PettingZoo (MIT)
- Swarm/team/team-of-humans-vs-team-of-AI cells

### Phase 4 — 3D / world-model (GPU-gated)
- Godot (MIT) for owned arena; NVIDIA Omniverse libraries (Apache-2.0) for SimReady authoring
- Cosmos (OpenMDW1.1, counsel-review competing-service clause) for visual world-model
- PhysicsNeMo + Data Factory Blueprint for turning play into curated data

### Phase 5 — Flywheel [THEORY]
- Only after Gates 1-2 close: route signed cards into safety-model training
- Publish recompute-able cards → external recompute creates authority
- This is what makes "Arena + Clans ready" MEASURED, not claimed

---

## EAT-ALL PHASES (executable now)

This lane-takeover session executes Phase 0 + Phase 1 fully, and stubs Phases 2-5 with the MCP contracts in place.

### EAT-0: Spine V2 (canonical JSON + signing + card types)
- `meok-sovereign-spine-mcp` — Python MCP wrapping `spine_v2.py`
- Tools: `sign_card`, `verify_card`, `register_kind`, `compute_cid`, `recompute_check`
- Card kinds: measurement, arena-round, honey-data, provenance, charter
- Tests: 15+ covering happy paths + adversarial

### EAT-1: AI-Town MCP wrapper
- Fork `a16z-infra/ai-town` to `~/clawd/sov-city/worlds/ai-town/`
- Strip Convex backend dependency; replace with substrate-runner
- Wrap as `meok-sovereign-aitown-mcp` exposing `run_scenario(seed, scenario, axes)` → returns signed card

### EAT-2: Generative-Agents MCP wrapper
- Fork `joonspk-research/generative_agents` (assets stripped per Apache-2.0 + issue #109 caveat)
- `meok-sovereign-genagents-mcp` exposing 25-agent sim → signed card

### EAT-3: /fabric (helm + lm-eval-harness + FastChat battle) → spine
- Python service: `meok-sovereign-fabric-mcp` consuming world outputs, calling `/spine`
- LM-Eval-Harness runs deterministic scoring, FastChat battle logic for pairwise
- Every output → signed card via spine_v2

### EAT-4: Arena loop upgrade — current sov-arena harness wired to spine
- 6 fleet clans already running — every round MUST emit a signed card via spine_v2
- 400 historical rounds → re-emit as signed cards (one-time script)
- `/api/sov-arena/rounds.jsonl` includes `card_cid` + `card_sig` per round

### EAT-5: Honey-data card type wired into training pipeline
- Once spine has honey-data kind: route training pairs through signing
- Pre-flight: every (prompt, response, model, weights) tuple is signed before becoming training data
- GATE: until this is live, no log is "honey data" — it is unprovenanced log

### EAT-6: Prolific MCP stub (consent-gated; human arm)
- `meok-sovereign-prolific-mcp` exposing Prolific API
- **GATED:** requires DPIA + counsel sign-off before any human cell runs
- Architecture in place; activation is a flag flip

### EAT-7: Ship dashboard — OOWM/OWEM/IWM/OWM/VWM + 33 Clans + Arena wired
- Update `/sovereign-os.html` to read live signed-card ledger
- New `/clans.html` page: 33 clan districts with current weights, last card signed, agreement rate
- Update `/arena_public.html` to show signed card verification status
- DEPLOY to csoai-site.pages.dev, byte-verified

---

## HONEST CONSTRAINTS

- **Signing ≠ correctness** — every signature proves provenance/integrity only, never that the measurement is right.
- **Authority is external** — every claim stays a claim until someone else recomputes the signed card.
- **Honey data is not honey until signed** — Gate 1 must close before the training pipeline can claim provenance.
- **Human cells need DPIA** — Prolific MCP stays stubbed until counsel approves.
- **NVIDIA Cosmos OpenMDW1.1** has "no competing model service" clause — counsel review before any Cosmos-derived model ships.
- **BMR gate** — daily index only stays research if no third party references it in a financial product.
- **Data-licence gate** — Polygon/Alpaca free/standard tiers do NOT permit building a public index.

## SIGIL

`v49.3-topdown-2026-08-15`

## LANE INVENTORY (verified 15 Aug 2026, 05:19 BST)

| Component | Location | Status |
|---|---|---|
| Spine (J-card graph) | `kimi-regen/spine.py` (108L), `sov-hive/src/spine.rs` (156L) | REAL — retrieval only |
| Arena harness | `sov-city/moa/sov_arena_loop.py`, `sov_arena.py`, `sov_ai_vs_ai.py` | REAL — 400 rounds live |
| Fleet (6 clans) | `sovereign-temple-public/dual_brain_router.py`, `quantum_council_router.py` | REAL — running on oracle-micro-2 |
| OpenTTD substrate | `sov-city/openttd/` | REAL — 272 lines live |
| CRDT federation | `sov-city/crdt/sov_crdt_*.py` | REAL — digest convergence |
| Sign/canonical JSON | — | **GAP — needs Phase 0 build** |
| /fabric (helm + FastChat) | — | **GAP — needs Phase 1 build** |
| Prolific MCP | — | **GAP — needs Phase 2 (DPIA-gated)** |
| Godot/Omniverse | — | **GAP — Phase 4, GPU-gated** |

## NEXT EXECUTE (start of session)

1. Write `spine_v2.py` with canonical JSON + signing + 5 card types
2. Build `meok-sovereign-spine-mcp` (15+ tests)
3. Replay 400 arena rounds through spine → signed cards
4. Update live HTML pages to show verification status
5. Deploy + byte-verify
