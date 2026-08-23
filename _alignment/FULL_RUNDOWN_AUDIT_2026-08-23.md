# FULL RUNDOWN + AUDIT — CSOAI EAT loop + products + front-end (2026-08-23)

## 1. What I did this session (consolidated, verified)
### Autonomous AXIS engine (make it produce, not $2/hr idle)
- Recovered a **serving-layer inference deadlock** (orphaned llama-runners + resident models held ~23GB VRAM -> every model evicted -> empty output). Fixed: OLLAMA_MAX_LOADED_MODELS=1 + kill orphaned runners. Verified: care->match=1.000/VETO, safety->match=1.000/AVOID.
- Fixed **chain-integrity**: ops_daemons dualwalk verified boards against a hardcoded key (M0cu...) but the pod SIGNS with j5oAooz8... -> every fresh board FAILED. Fixed key. Trust chain now **315 valid / 0 invalid**, 51 old-key boards quarantined.
- Fixed **pgrep self-match** (genetic thread always "skip", never ran). Anchored to `^python3 .*gspc_genetic.py` -> improve-loop actually runs.
- Fixed **measure_probe** (present verdict options) + built semantic classifier (reverted to correct exact-matching that works).
- Created **board_living.json** (was missing -> loop defaulted to jail which yields 0; now selects real gap axes).
- Added **templated probes** (5 jail + 5 swarm real content, replacing jail-000 stubs).
- Wired **gspc_genetic** into axis_supervisor.batch_loop (independent genetic_loop thread, 420s).
- Engine autonomous: measure_chain, axis_engine_16, gspc_genetic, ops_daemons, arena_loop_keeper, grok_referee all PPID=1 durable. EAT 7-box (measure->sign->chain->anchor->board->mirror) running.

### Products + front-end (published to councilof.ai)
- **ClaimGuard** + **Council Ledger** landing pages LIVE (schema.org JSON-LD, CC-BY-4.0). PyPI: csoai-claimguard 0.1.0, csoai-council-ledger 0.1.0.
- **/api/axis-register** (honest set-boundary: public 14 / internal 16) — fixed the recurring 404 by serving it inline in the /api/* catch-all (functions/api/[[path]].js). Now stable 200.
- **/mcp.json** fixed: was empty standard mcpServers + 404 csoai.org URLs. Now standard mcpServers -> csoai-tools, csoai-article50, csoai-gspc (all resolve).
- **/catalog.json** 2 products with MCP tools. /api/gspc (14-axes board), /api/badge (honest 13/14), /api/assess (POST, Ed25519-signed).
- Full front-end E2E passed for all user types (human/agent/verifier/SEO) — all 200.

### Consolidation
- Committed + pushed my monorepo files (bbcac2e on feat/founder-about): axis-register.ts, mcp.json, claimguard.html, council-ledger.html, AGUI_HANDOFF.
- Mirrored all work to pod RAG volume (/workspace/mac-offload/council-estate: SOVOS, councilof-ai, agui-wire, _alignment, deploy2). Mac disk freed 99%->~55%.

## 2. Audit checklist (done / known)
### DONE + verified
- EAT loop autonomous + producing (407 boards, GPU active, 15 durable procs, no SSH/human).
- Trust chain clean: 315 valid / 0 invalid.
- Products live + front-end all user-types tested (200).
- MCP discovery working (standard mcpServers, tools, assess signed).
- Work consolidated to monorepo + pod.

### KNOWN / OPEN (honest)
- **/api/cards 404** — referenced but no cards function built (sibling's or unbuilt endpoint).
- **GSPC signed-issuance + flywheel fuel UNMEASURED** (mining opportunity: EAT honey 94K events -> KB -> IWM; forest 10K+).
- **SOV3 :3101 / Sovereign Temple MCP DOWN** (GCP billing gate) — owner-gated.
- **Improve-loop genome growth compute-bound** (correct machinery, slow inference) + jail/swarm model gives empty signal.
- **Owner-gated (Nick)**: GitHub org appeal (API restricted, but git push works), PAT rotation, arXiv S7VDXA, domain/UKIPO, Kaggle verify, C2PA/DIF.

## 3. Recommended next (from the scan + my analysis)
1. Integrate the **deploy Functions-guard** (assert /api/gspc,/api/cards,/api/axis-register,/api/mcp,/api/tools all 200) so front-end endpoints stop silently 404ing.
2. **Mine the EAT honey/forest** -> signed measurement cards (unmeasured flywheel fuel) to grow the board + genome.
3. Fix **/api/cards** (build the cards function the MCP registry implies).
4. Owner-gated: GitHub org, SOV3 billing, arXiv, domains.
