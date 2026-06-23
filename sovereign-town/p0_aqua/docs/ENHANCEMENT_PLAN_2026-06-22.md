# Sovereign Town Enhancement Plan — Post-DORA-Experiment

**Date:** 2026-06-22  
**Prepared by:** JEEVES (Kimi Code CLI)  
**Status:** In progress — Option D (P0/P1 hardening + observability + docs + productization + cross-terminal bridge)

---

## 1. Where we are now

### Delivered today
- Real-data DORA policies (`dora_automated`, `dora_manual`) in `benchmark/policy.py`.
- Event detector unification (`event_detect.py` now wraps `event_detector.py`).
- Operational `/metrics` endpoints on dashboard + harness with structured logging.
- JSON-driven regulation policies (`benchmark/policies/*.json`) + `ConfigurableRegulatoryPolicy`.
- Policy Lab experiment gallery (`/experiments.html`) + `/api/experiments` + comparison widget.
- Cross-terminal bridge endpoints: `/api/hive/aethelgard`, `/api/council/vote`, `/agent/chat` (FreeLLMAPI proxy).
- `CONTRIBUTING.md`, CI lint/type-check job, and `verify_chain` unit test.
- `RUNBOOK.md` + `SECURITY.md` at repo root; README and ONEPAGER refreshed.
- First live A/B experiment (`experiments/dora_finance.json`) — status **PROVEN**.
- `policy_lab.py` CLI: `vote`, `spawn --live`, `status`, `report` with whitepaper/brief/email export.
- Public, aggregate-only regulator view + downloadable brief (MD + DOCX).
- `selftest.py` 47/47, `e2e_test.py` 66/66, `browser_test.py` 5/5.

### Context from shared knowledge
- `sovereign-town` is the canonical P0/P1 engine; older `sovereign-temple*` stacks are runtime/source primitives.
- Dragon Mode 13-day plan (June 22 → July 4) targets `www.meok.ai` / `try.meok.ai` with a 12-agent Aethelgard Finance Hive, BFT voting UI, and a flagship white paper.
- FreeLLMAPI (`sov-town-llm/`) provides the zero-cost inference layer for the agents.
- Shared-knowledge handoffs flag remaining VM/Mac tunnel health, credential gates, and the need for one public apex site.

---

## 2. Internal audit findings

| Area | Finding | Severity |
|---|---|---|
| Event detectors | `event_detect.py` now wraps `event_detector.py` with legacy-state migration. | ✅ |
| Policy engine | JSON-driven policy configs for DORA/NIS2/GDPR/EU AI Act; `load_policy("<name>")` works | ✅ |
| Scenario config | `dora_incident_deadline` now aligned to 14 days; other regulatory scenarios are shallow | P2 |
| Metrics | `policy_lab` cost index is simulation-only; no real currency or productivity model | P2 |
| Dashboard | `/experiments.html` gallery + dynamic comparison widget + `/api/experiments` | ✅ |
| Auto-spawn | `regulation_parser.py` + `POST /api/experiments/spawn` auto-spawn hook live | ✅ |
| Observability | `/api/metrics` + `/harness/metrics` endpoints; structured JSON access logs via `SOV_TOWN_ACCESS_LOG`. | ✅ |
| Performance | `sim.py` loops are pure Python; no profiling baseline | P2 |
| Content pipeline | `distributor.py` has TODO stubs for X/LinkedIn/YouTube APIs | P2 |
| Security | WebSocket `/ws/feed` now stores regime per-client (`_WS_REGIMES`). | ✅ |
| Security | `POST /harness/run` now has configurable per-IP rate-limit (manifest cap queued). | 🔄 |
| Docs | README/ONEPAGER refreshed; `RUNBOOK.md` + `SECURITY.md` created. `CONTRIBUTING.md` queued. | 🔄 |

---

## 3. Strategic options

### Option A — Internal hardening sprint
Focus on closing every open P0/P1 gap before building outward.

- Unify `event_detector.py` + `event_detect.py`.
- Add rate-limit + manifest cap to `/harness/run`.
- Auth-gate or client-localize WebSocket regime switching.
- Add `/metrics` + structured request logging.
- Refresh README/ONEPAGER numbers and create RUNBOOK/CONTRIBUTING.
- Add lint/type-check CI job (`ruff`, `mypy`).

**Pros:** Lowest risk, world-class foundation.  
**Cons:** No new user-facing product motion for 3–4 days.

---

### Option B — Policy Lab productization sprint
Turn the DORA experiment into a repeatable, self-service product.

- Experiment gallery page (`/experiments`) with filterable cards.
- Dynamic experiment comparison widget on leaderboard/workbench.
- Generic policy loader so new regulations (NIS2, GDPR, EU AI Act) become JSON configs, not Python classes.
- Regulation → experiment auto-spawn hook (parse + spawn + report).
- Publish experiment outcomes to MEOK Labs index and content factory.
- Real-time (but still aggregate) public experiment dashboard.

**Pros:** Directly extends today's proven work; strong regulator/enterprise pitch.  
**Cons:** Leaves some P0 security gaps open for another cycle.

---

### Option C — Dragon Mode alignment sprint
Bridge `p0_aqua` to `meok-ai/ui` / FreeLLMAPI / SOV3 so the public site can go live.

- Add an OpenAI-compatible `/agent/chat` endpoint in `p0_aqua` that proxies to FreeLLMAPI.
- Expose Aethelgard Finance Hive roster + state via JSON API.
- Add BFT Council vote simulation endpoint with deterministic outcomes.
- Provide a Next.js-ready data contract for `/town` and `/dome`.
- Keep the simulation as the "backend physics" while the UI owns presentation.

**Pros:** Aligns with the 13-day launch plan; highest external impact.  
**Cons:** Touches multiple repos and credentials; requires UI coordination.

---

### Option D — Phased hybrid (RECOMMENDED)
Combine A + B in Week 1, then C in Week 2.

**Week 1: Foundation + Policy Lab productization**
1. Close P0 security gaps (rate-limit, WS regime auth).
2. Unify event detectors + fix file-handle/exception hygiene.
3. Make policies data-driven (JSON regulation configs).
4. Add experiment gallery + dynamic comparison widget.
5. Refresh docs + CI lint.

**Week 2: Public bridge (Dragon Mode prep)**
6. Agent chat/chat-completions endpoint backed by FreeLLMAPI.
7. Aethelgard Finance Hive API contract for `meok-ai/ui`.
8. BFT vote endpoint + pheromone signal API.
9. Integrate with SOV3 `bridge_think` for heavier reasoning.
10. Deploy static experiment + regulator pages to `proofof.ai`.

**Pros:** Builds on today's momentum while closing risks before public launch.  
**Cons:** Two-week scope; requires daily checkpoint discipline.

---

## 4. Immediate no-regret actions (any option)

- Fix `event_detector.py` / `event_detect.py` duplication.
- Add a `metrics/` latency baseline for harness endpoints.
- Update `README.md` and `ONEPAGER.md` with honest counts from `fleet_status_*.json`.
- Create `RUNBOOK.md` for local + VM + Mac operations.
- Add a `SECURITY.md` pointing to the bright lines and disclosure process.

---

## 5. Decision needed

Which option should JEEVES/JARVIS execute?

- **A** — Harden first, ship nothing new publicly for a few days.
- **B** — Productize Policy Lab now, defer public UI bridge.
- **C** — Race to public town UI, accept some technical debt.
- **D** — Two-week phased plan (recommended): harden + Policy Lab, then public bridge.
