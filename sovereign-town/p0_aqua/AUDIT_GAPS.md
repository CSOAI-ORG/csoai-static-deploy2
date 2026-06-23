# Sovereign Town — Gap Audit (2026-06-22)

Compiled from parallel audits of architecture, security, tests, UX, docs, and operations.
Findings are ranked P0 (fix immediately), P1 (this week), P2 (next 2 weeks).

---

## P0 — Critical

| # | Area | Finding | Suggested Fix | Owner Day |
|---|------|---------|---------------|-----------|
| 1 | Security | `benchmark/policy.py::load_policy()` imports arbitrary modules from user input → RCE | Whitelist built-in policy names; reject `.`/`:` unless explicitly allowed | Day 2 |
| 2 | Security | `POST /harness/run` is unauthenticated and writes signed manifests + burns compute | API-key auth ✅, rate-limit ✅, manifest cap ✅ | Day 2 |
| 3 | Security | WebSocket clients can mutate global `_TOWN_REGIME` for all viewers | Regime is now stored per-client (`_CLIENT_REGIMES`) ✅ | Day 2 |
| 4 | Security | Path traversal in `api_labs_file`, `api_passport_detail`, `api_ledger` | Resolve paths with `Path.resolve()` and re-anchor; restrict key/host patterns | Day 2 |
| 5 | Security | Unsanitized `innerHTML` across dashboard/workbench/verifier → stored/reflected XSS | Added `escapeHtml` helper and escaped dynamic values in dashboard, town3d, workbench, verifier, and public pages | ✅ |
| 6 | Security | Wildcard CORS on dashboard + harness enables cross-site requests to stateful endpoints | CORS only enabled when `SOV_TOWN_CORS_ORIGINS` is set; no wildcard by default | ✅ |
| 7 | Security | Disabled plist contains plaintext API keys (`~/Library/LaunchAgents/_disabled_sov3_20260617/...`) | Delete or encrypt; confirm with operator before destructive action | Day 2 |
| 8 | Ops | No supervisor for Mac flywheel; VM flywheel uses one-shot `nohup` | Add Mac LaunchAgent + VM watchdog; wrap `cycle()` in try/except | Day 11 |
| 9 | Ops | No backup for `.town_priv.key`, ledgers, manifests | Encrypt and copy key; rsync ledgers/manifests to secondary location | Day 11 |

## P1 — High

| # | Area | Finding | Suggested Fix | Owner Day |
|---|------|---------|---------------|-----------|
| 10 | Architecture | Pervasive `except Exception:` swallows failures | Use narrow exception types; log unexpected ones | Day 3 |
| 11 | Architecture | 9 near-identical `load_moat()` functions | Create `moat_common.py` with shared JSON/HTTP helpers | Day 3 |
| 12 | Architecture | `sim.py` is a 550-line god module | Extract moat loading, Agent/Town models, tick logic | Day 3 |
| 13 | Architecture | Duplicated event detectors (`event_detector.py` + `event_detect.py`) | `event_detect.py` now wraps `event_detector.py` ✅ | Day 3 |
| 14 | Architecture | File-handle leaks (`json.load(open(...))`, unflushed appends) | Convert to context managers; flush ledger writes | Day 3 |
| 15 | Architecture | Hardcoded ports/paths across files | Centralize in `config.py` / env vars | Day 3 |
| 16 | Tests | `consent_vault.py`, `pheromone_bus.py`, `verify_chain.py` have zero tests | Added `verify_chain` unit test; `consent_vault` + `pheromone_bus` queued | Day 4 |
| 17 | Tests | CI service startup does not wait for MCP SSE port | Add `:3942` health wait; track PIDs for cleanup | Day 8 |
| 18 | Tests | `requirements.txt` missing `numpy`, `scikit-learn`, `joblib`, `pandas` | Already present in `requirements.txt`; `ffmpeg` remains a system requirement | ✅ |
| 19 | UX/a11y | No ARIA landmarks, labels, focus rings, or keyboard paths | Add labels, focus-visible, ARIA live regions, roles | Day 6 |
| 20 | Docs | Missing RUNBOOK.md, CONTRIBUTING.md, EXAMPLES.md, TROUBLESHOOTING.md | RUNBOOK.md, CONTRIBUTING.md, SECURITY.md, EXAMPLES.md, TROUBLESHOOTING.md, PRIVACY.md created | ✅ |
| 21 | Docs | Stale metrics across README/ONEPAGER/WHITEPAPER/API | README + ONEPAGER refreshed from fleet_status ✅; WHITEPAPER/API queued | Day 5 |
| 22 | Docs | Research vision diverges from implementation (47 vs 140 agents, DORA twin, frontier-model arm) | RESEARCH_ALIGNMENT.md + SCOPE_NOTE.md + DEMO.md created | ✅ |

## P2 — Medium

| # | Area | Finding | Suggested Fix | Owner Day |
|---|------|---------|---------------|-----------|
| 23 | Security | Missing CSP, X-Frame-Options, X-Content-Type-Options | Add security-headers middleware | Day 2 |
| 24 | Security | `/api/episodes?limit` unbounded; `/api/verify` accepts large payloads | Cap limit and body size | Day 2 |
| 25 | Security | MCP `sov_leaderboard` fetches arbitrary URLs | Validate URL scheme/host | Day 2 |
| 26 | Tests | Browser tests have tight timeouts, no retries, no failure artifacts | Add `data-testid`, retries, traces/screenshots | Day 4 |
| 27 | Tests | `selftest.py`/`e2e_test.py` hardcode `28` districts | Drive from `len(sim.DISTRICTS)` | Day 4 |
| 28 | CI | No lint/format/type checks | Added `lint` job with ruff + mypy (allow-fail) | ✅ |
| 29 | CI | No dependency cache; Playwright reinstalls every run | Added pip + Playwright cache | ✅ |
| 30 | UX | Auto-refresh defaults on; color-only status; new-window links unmarked | Default off, add text labels, rel=noopener | Day 6 |
| 31 | Performance | No endpoint latency metrics or structured logs | Add `/metrics`/log timing; baseline harness endpoints | Day 7 |
| 32 | Ops | Shallow health endpoints | Add composite `/api/ready` checking harness + MCP + disk | Day 7 |
| 33 | Ops | VM/Mac runner drift | Collapse common logic into `runners/shared/` | Day 9 |

---

## Policy Lab intake gaps (2026-06-22)

Findings from `docs/MEOK_POLICY_LAB_INTAKE.md` (`/Users/nicholas/Downloads/meok_policy_lab.docx`).

| ID | Priority | Area | Finding | Suggested Fix | Owner Day |
|---|---|---|---|---|---|
| PL-1 | P1 | Architecture | No experiment registry or JSON schema | Create `experiments/` directory + `policy_lab.py` CLI | Day 4 |
| PL-2 | P1 | Architecture | No treatment/control pairing in harness | Extend `policy_lab.py` to call `/harness/run` twice and link run IDs | Day 4 |
| PL-3 | P1 | Architecture | No BFT Council vote simulation | Add deterministic council vote to `policy_lab.py vote` | Day 4 |
| PL-4 | P2 | UX/a11y | No experiment-specific dashboard | Add `/experiments/<id>` view or filter on leaderboard | Day 6 |
| PL-5 | P2 | Data pipeline | No auto-experiment spawning on new regulation | Hook regulation parser → `policy_lab.py spawn` | Day 10 |
| PL-6 | P2 | Docs | No experiment white-paper / regulator brief export | Extend `report.py` with experiment template | Day 11 |
| PL-7 | P2 | Data pipeline | No per-experiment outcome aggregation | Append experiment outcomes to distribution events / content factory | Day 10 |

## Immediate execution queue (today)

1. Fix `policy.load_policy()` RCE.
2. Add path-traversal defense to file routes.
3. Add security-headers middleware.
4. Patch `requirements.txt`.
5. Create `runners/.env.example`.
6. Start `RUNBOOK.md` and `CONTRIBUTING.md`.
7. Tighten exception handling in moat loaders.
8. Add shared `load_json` helper and deduplicate moat loaders.
9. Ingest `meok_policy_lab.docx` and seed first experiment (`experiments/dora_finance.json`).
