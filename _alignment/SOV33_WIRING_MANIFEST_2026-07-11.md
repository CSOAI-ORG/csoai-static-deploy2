# SOV33 wiring manifest — the "one sovereign, all parts" gap, quantified (2026-07-11)
_Registry probe of 51 real governance components (bench/tests excluded). Import health measured, not assumed._

## VERDICT: the gap is NOT missing capability — it's 16 modules with IMPORT-TIME SIDE EFFECTS
- **35/51 import clean** — safe to register into sov33_registry.py + route from the entrypoint now.
- **10 HANG on import** — do a NETWORK CALL at module-top (Oracle/Ollama brains). Wiring as-is would hang sov33.py startup.
  This is WHY the entrypoint imports so few modules — self-protection, not neglect.
  FIX: move the network call out of module-top into a lazy init()/first-call. Modules:
  bft_layers, care_divergence, care_divergence_v2, care_scorer, conformal_veto, governance_eval,
  l3_anchor_quorum, l4_divergence, multimodel_gov, scored_owem_v2.
- **6 BROKEN** — all identical cause: PermissionError writing ~/.sovereign at import (sandbox-blocked).
  FIX: one shared change — SOV33_SIGIL_DIR env-override + fail-soft, EXACTLY as sov33.py + sov33_dorado.py already do.
  Modules: embodied_feedback_loop, nine_stage_orchestrator, owem_mixer, pyramid_owem, retrain_loop, y2d_dispatcher.

## The registry (sov33_registry.py, RUN-verified)
- Fail-soft imports every real component, records OK/BROKEN/HANG — a BROKEN entry is SURFACED, never hidden.
- This IS the "one sovereign entrypoint" honestly: route to what actually loads; fix the 16 with the two mechanical patches above.

## HONEST NOTE
- 51 components counted as runtime; 10 bench/test files (scorecard, e2e_benchmark, council_correlation, etc.) are FINDINGS, not wired.
- sov33_pyramid_owem.py ALREADY EXISTS = the 2-small+1-big+1-bigger topology the founder sketched. Built, just import-broken (path fix).
- Two triangle modules on the decorrelation law: mine (sov33_triangle_owem, RUN-verified) + MEOK's reported ring (not in tree). Reconcile when it lands.

## GitHub estate (CSOAI-ORG, token-accessible) — governance/MCP tools SOV33 could bridge (not yet wired)
- meok-compliance-gateway, meok-eu-code-of-practice-mcp, c2pa-watermark-mcp (provenance/watermark), credential-manager-mcp,
  csoai-governance, councilof-ai, mcp-servers, defoneos (private, defence lane). CANDIDATES to expose as SOV33 tools via the
  MCP bridge — audit each for license + fit before wiring; do NOT assume. (Directional list, not a merge order.)
