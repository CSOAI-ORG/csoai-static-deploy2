# EAT Action Plan — 89% → 95% World Model

## Current State (Tick 186)
- **World Model: 89%**
- **Strong (100%):** Planning, Memory, Knowledge, Agentic, Visual, Autonomous, Sovereign
- **Weak (80%):** Reasoning, Tool Use, Decision Making, Governance, Creative

## Per-Category Action Plan

### Reasoning (80% → 95%)
- Run `kaggle/sov33_self_train.py` with GSM8K + BBH + GPQA curricula
- Add chain-of-thought distillation via `kaggle/sov33_distill.py`
- Sov4 router already routes `reasoning` to `deepseek-chat` cloud fallback

### Tool Use (80% → 95%)
- 33 MCPs, 111 tools in registry — verify all are exercised
- Run `tools/capability_assert.py` (8/8 passing) — expand to cover all 33 MCPs
- Run `tools/live_mcp_test.py` against live endpoints

### Decision Making (80% → 95%)
- BFT-33 council routing: 23/33 quorum, Ed25519 SIGIL chain
- Sov4 router pillar-aware routing for sovereign compliance/defence suites
- Expand `sov_master_scenarios.py` with more decision-making task scenarios

### Governance (80% → 95%)
- 12-layer maternal sovereign stack fully defined in registry
- 7 hard stops (DORADO red lines) enforced in sov_invariants.py
- Care floor at 0.95 — runtime-gated in `_governed()` + `sovereign_call()`
- Cross-jurisdiction mapping via M2_DEPLOYMENT_KIT/

### Creative (80% → 95%)
- 13 OWEM v3 Light specialists (aesthetics, creation, synthesis, etc.)
- Visual sandbox + C-space + infinite drawing pipeline
- Run `sov7_visual_synthesis.py` + `sov7_synthesis_orchestrator.py`

## Execution

| Category | Scripts | Frequency | Cost |
|----------|---------|-----------|------|
| Reasoning | sov33_self_train, sov33_distill | Daily (Kaggle T4) | $0 |
| Tool Use | capability_assert, live_mcp_test | Per commit | $0 |
| Decision Making | sov_master_run, bft-council | Weekly | $0 |
| Governance | verify_capability_registry | Per commit | $0 |
| Creative | sov7_visual_synthesis, sov7_synthesis | Weekly (Kaggle T4) | $0 |

## Target: Tick 200 — 95% World Model
