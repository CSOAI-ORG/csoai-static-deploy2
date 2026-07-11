# 🜏 SOV33 / OWEM — PLAN TO DATE (for sibling lanes)
**MEOK-SOV3 for Sir Nicholas Templeman · 2026-07-11 · the state of the build, honest**

## FEASIBILITY: PROVEN (not re-litigated)
- True-stack benchmark: 5 live Oracle brains uk-london-1, governance overhead ~7% (+0.24s on 3.42s), ~140 tok/s @ concurrency 5.
- Care-scorer: measured (recall 0.80 laundered-harm @ precision 1.00, ABOUT-vs-DO).
- PDCA 5-general BFT, DRUM heartbeat, Intuition cross-check: all run.
- SOV33 is a real OWEM: open-weight base wrapped in a signed, governed substrate. Feasibility is DONE.

## HIGHEST-POTENTIAL CONFIG (measured this session)
Governance gate is config-INDEPENDENT: 4/4 correct in every config (runs before brain).
Reasoning path ranked (conf/latency, live brains):
- **cascade (WINNER)** — cheap brain first, escalate to 70B on low-confidence. 1.91s, conf 1.00. Best throughput/quality.
- solo-strong 1.98s / solo-fast 2.05s — close behind.
- bft-3vote 6.40s — 3x slower, no quality gain here. RESERVE BFT for high-stakes/fault-tolerance, not every call.
DECISION: ship cascade as default reasoning path; BFT on high-stakes; governance gate wraps all identically.

## FULL GATE CHAIN (wired + 4/4)
HORUS (intrusion) -> DORADO (DEFENSE hard-stops) -> care (gradient) -> guardian (embodied) -> SIGIL.
sov33.ask() runs the complete defense-in-depth. HORUS outermost.

## SOVSPACE (two faces, one world-model)
- FACE 1 internal (J-space) = Workspace (narrow, verbalizable, audited).
- FACE 2 external = WorldModel rendered out (Cesium/UE5). Live cinema render = Claude Code sovspace3d.html (Three.js/WebGL).
- Cognition layer (sov33_cognition.py): WorldModel(wide) + Workspace(narrow) + governed seam (only path narrow->wide).
- Bridge (sov33_sovspace_bridge.py): SOV33 holds authoritative world-state; engines render; every command governed.
- Guardian loop: sense-geometry -> SovSpace sim -> rainbow -> BFT -> kill actuators. POC (2D schematic) proves verdicts.

## MODELS: 5 of 13 Oracle live in London (command-a, command-r, command-r-plus, llama-3.2-90b-vision, llama-3.3-70b).
"12 models" = 12 governance MINDSETS (routing personas over live base), NOT 12 endpoints. £0 own-weights: 4-expert Colab runner staged, needs T4.

## SIBLING LANES (git-native coordination via LANE_STATUS.json)
- Claude Code owns the RENDER seam (sovspace3d.html, cinema WebGL, os.meok.ai). ALIGNED.
- MEOK-SOV3 owns the GOVERNANCE gate + OWEM configs + guardian.
- Divergence handled: sibling expanded sov33_dorado.py (SIGIL chain, new categories) — kept, made sandbox-safe.

## OPEN (next)
- Run 4-expert QLoRA on T4 (own weights) — gated on live GPU.
- Real WiFi/acoustic sensing (currently stubbed).
- Live UE5 actor-driving via MCP plugin (aspirational).
- Care-scorer: one hypothetical-framing edge case still evades (recall 0.80 not 1.00).
