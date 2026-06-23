# Sovereign Town — 13-Day World-Class Execution Plan

Goal: close every gap across code, tests, docs, UX, security, observability, and operations so the project is demonstrably world-leading and production-ready.

## Success criteria (Day 13)
- `./check.sh` green: selftest + e2e + browser tests
- 100% of public HTML pages pass accessibility smoke (labels, contrast, focus)
- All user-input surfaces validated and escaped
- CI green on GitHub Actions
- README/API docs complete and accurate
- Runbook exists for local + VM + Mac operations
- No secrets, no PII leaks, no known security gaps
- Performance baseline recorded for harness endpoints

---

## Day 1 — Full audit & gap report ✅
**Deliverables:**
- ✅ `AUDIT_GAPS.md` with P0/P1/P2 findings
- ✅ Parallel audits: architecture, security, tests, UX, docs, ops
- ✅ Updated roadmap below

**Execution (today):**
- Fix P0 security issues: policy RCE, path traversal, security headers
- Patch `requirements.txt`
- Create `runners/.env.example`
- Start RUNBOOK.md / CONTRIBUTING.md

---

## Day 2 — Security & privacy hardening ✅
- [x] Whitelist policy names in `benchmark/policy.py` (P0 RCE)
- [x] Resolve and re-anchor file paths in `api_labs_file`, `api_passport_detail`, `api_ledger` (P0)
- [x] Replace `innerHTML` with safe helper across `workbench.html` (P0)
- [x] Restrict CORS origins via env var; default is no cross-origin access (P0)
- [x] Add security-headers middleware (CSP, X-Frame-Options, etc.) to dashboard + harness (P1)
- [x] Cap `/api/episodes?limit` and add request body/query size limits (P1)
- [x] Encrypt Ed25519 private key at rest when `SOV_TOWN_KEY_PASSWORD` is set (P1)
- [x] Add optional bearer-token auth to `POST /harness/run` via `SOV_TOWN_API_TOKEN` (P0)
- [x] Add rate-limit / manifest-cap to `POST /harness/run` (P1)
- [ ] Make WebSocket regime switch auth-gated or client-local (P1)
- [x] Validate URL scheme/host in MCP `sov_leaderboard` (P1)
- [ ] Delete/encrypt disabled plist with exposed API keys (P0 — confirm with operator)

## Day 3 — Code quality & architecture ✅
- [x] Tighten exception handling in moat loaders (narrow types + logging)
- [x] Create `moat_common.py` and deduplicate 9 `load_moat()` functions
- [x] Convert file-handle leaks to context managers; flush ledger appends
- [x] Create `config.py` for ports/hosts/paths; replace hardcoded literals
- [x] Extract moat loading from `sim.py` into `moat_params.py`
- [ ] Unify duplicate event detectors (`event_detector.py` vs `event_detect.py`)
- [x] Extract generic proxy helper in `dashboard_server.py`

## Day 4 — Unit/integration test expansion + Policy Lab scaffold
- [ ] Add tests for `consent_vault.py` grant/revoke/expire flows
- [ ] Add tests for `pheromone_bus.py` propagation and chain verification
- [ ] Add tests for `verify_chain.py` tamper detection
- [ ] Replace hardcoded `28` with `len(sim.DISTRICTS)` in tests
- [ ] Add error-path tests for malformed JSON/CSV, missing files, bad signatures
- [ ] Determinism test for `sim.run_arm` with fixed seed
- [x] Land `experiments/dora_finance.json` and `policy_lab.py` (PL-1)
- [x] Add `policy_lab.py vote` unit test with deterministic council outcome (PL-3)
- [x] Add real DORA policies (`dora_automated`, `dora_manual`) and unit test
- [x] Wire `policy_lab.py spawn` to `/harness/run` with treatment/control pairing (PL-2)

## Day 5 — Live A/B run + browser test expansion & CI reliability
- [x] Execute first live DORA A/B run (`spawn --live`) and generate regulator view (PL-2 / PL-4)
- [ ] Add `data-testid` attributes to key frontend elements
- [ ] Add env override (`SOV_TOWN_URL`) to `browser_test.py`
- [ ] Capture Playwright traces/screenshots on failure
- [ ] Test MCP client error paths (disconnect, bad URL, timeout)
- [ ] Test leaderboard auto-refresh and scenario filter
- [ ] Test run detail raw JSON toggle
- [ ] Fix CI to wait for `:3942` MCP health and track PIDs
- [ ] Cache pip + Playwright browsers in GitHub Actions

## Day 6 — Documentation rewrite + experiment dashboard
- [ ] `RUNBOOK.md`: start/stop/restart, health checks, logs, LaunchAgent reload
- [ ] `CONTRIBUTING.md`: install, test commands, code style, PR checklist
- [ ] `EXAMPLES.md`: benchmark, passport, moat, MCP tool-call walkthroughs
- [ ] `TROUBLESHOOTING.md`: deps, port conflicts, stale fleet, MCP proxy issues
- [ ] `SECURITY.md` + `PRIVACY.md`: keys, aggregate-only policy, disclosure
- [ ] Refresh stale metrics in README/ONEPAGER/WHITEPAPER/API
- [ ] Add honest-counts glossary (27 personas planned vs 140 current sim)
- [ ] Fix `requirements.txt` (add numpy, sklearn, joblib, pandas)
- [x] Create static, aggregate-only regulator view under `proofof-site/sovereign-town/experiments/` (PL-4 partial)
- [ ] Add dynamic experiment comparison widget to leaderboard or workbench (PL-4)

## Day 7 — UX/UI polish & accessibility
- [ ] Add `<label for>` associations to all form inputs
- [ ] Restore `:focus-visible` rings; remove `outline:none`
- [ ] Add ARIA landmarks, live regions, roles
- [ ] Convert `<div class="tab">` to accessible `<button role="tab">`
- [ ] Improve color contrast for brand/muted text
- [ ] Add text alternatives to color-only status indicators
- [ ] Default auto-refresh off; add pause/resume toggle
- [ ] Mark new-window links with `rel="noopener noreferrer"` + accessible text

## Day 8 — Performance & observability
- [ ] Add structured request-timing logs to dashboard/harness
- [ ] Add `/metrics` or `/api/ready` endpoint checking harness + MCP + disk
- [ ] Record harness endpoint latency baseline
- [ ] Add disk-space and ledger-age checks to health

## Day 9 — CI/CD & deployment automation
- [ ] Validate GitHub Actions workflow (service health wait, PID cleanup)
- [ ] Add lint/format/type check job (`ruff`, `mypy`)
- [ ] Add Docker compose for one-command local stack
- [ ] Add deployment script for VM/Mac runners
- [ ] Add `timeout-minutes` and test artifacts to CI

## Day 10 — Data pipeline hardening + auto-experiments
- [ ] Add retry/backoff and offline fallback to moat fetchers
- [ ] Validate downloaded dataset checksums/sizes
- [ ] Add data freshness timestamps and stale alerts
- [ ] Enforce aggregate-only outputs in moat modules
- [ ] Hook new-regulation parser to `policy_lab.py spawn` (PL-5)
- [ ] Aggregate per-experiment outcomes into distribution events / content factory (PL-7)

## Day 11 — Research alignment, examples, and experiment reports
- [x] Generate first experiment report + static regulator brief for DORA finance
- [ ] `RESEARCH_ALIGNMENT.md`: POC/master-plan → implemented files status matrix
- [ ] `SCOPE_NOTE.md`: current procedural 140-agent sim vs planned 47-agent real-character sim
- [ ] Update ONEPAGER with latest numbers
- [ ] Record narrated demo script (`DEMO.md`)
- [ ] Add experiment white-paper / regulator brief export to `report.py` (PL-6)

## Day 12 — Monitoring & alerting
- [ ] Add Mac LaunchAgent for flywheel
- [ ] Add VM cron watchdog for flywheel restart
- [ ] Wrap `flywheel_forever.py cycle()` in try/except
- [ ] Add service-heartbeat script / uptime checks
- [ ] Add disk-space and data-growth alerts
- [ ] Set up ledger/key backup routine

## Day 13 — Final integration & ship
- [ ] Full stack test: flywheel → manifest → leaderboard → run detail
- [ ] Concurrent WebSocket + SSE load smoke
- [ ] Memory-leak check on long-running dashboard
- [ ] Final `./check.sh` run
- [ ] Read-through all docs; fix inconsistencies
- [ ] Record final metrics and before/after
- [ ] Prepare PR / clean commit history
- [ ] Handoff report with next 30-day horizon

---

## Running notes
- Owner: JEEVES (strategic commander)
- Execution: JARVIS mode for low-level sprints
- Daily checkpoint: update this file, log to `~/.clawdbot/shared-knowledge/intel/session-2026-06.md`
- Red line: no destructive deploys, no commits, no external communications without explicit approval
