# Contributing to Sovereign Town

Thank you for helping make the governed agent-world engine safer and more useful.
This project is research-grade (P0/P1) and defensive-only; all contributions must
preserve that scope.

## Quick start

```bash
cd p0_aqua
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt      # or uv pip install -r requirements.txt
python3.11 selftest.py               # 46 unit/integration checks
python3.11 e2e_test.py               # 63 endpoint + WebSocket checks (needs services)
./check.sh                           # full suite incl. optional Playwright tests
```

For browser tests you also need a separate Playwright venv:

```bash
uv venv .venv-playwright
uv pip install --python .venv-playwright/bin/python playwright pytest pytest-playwright
.venv-playwright/bin/python -m playwright install chromium
```

## Project layout

- `p0_aqua/` — canonical engine: sim, moats, passports, gate, ledger, harness, dashboard.
- `p0_aqua/benchmark/` — policy-vs-scenario A/B harness, MCP server, regulatory workbench.
- `p0_aqua/benchmark/policies/` — JSON-configurable regulatory policies (DORA, NIS2, GDPR, EU AI Act).
- `p0_aqua/experiments/` — Policy Lab experiment definitions (sanitized JSON).
- `proofof-site/sovereign-town/` — public static pages (Vercel-ready).
- `~/.clawdbot/shared-knowledge/` — cross-terminal handoffs and session intel.

## How to contribute

1. **Open an issue first** for non-trivial changes so design direction is agreed.
2. **Keep changes minimal** — one concern per PR/branch.
3. **Follow existing style** — black-compatible formatting, type hints for new functions, no bare `except:`.
4. **Add tests** — every new policy, API route, or trust primitive needs a test in `selftest.py` or a dedicated unit file.
5. **Run the full suite** — `./check.sh` must pass before asking for review.
6. **Update docs** — `README.md`, `API.md`, `RUNBOOK.md`, or `SECURITY.md` as appropriate.

## Code conventions

- Python 3.11+ syntax; use `from __future__ import annotations`.
- Prefer `pathlib` over `os.path`.
- Centralize env vars in `config.py`; no hardcoded ports/limits elsewhere.
- Security: never trust user input; use `_safe_path()` for files, validate URLs, cap sizes.
- Ed25519 keys and API tokens are secrets — never commit them.

## Adding a new regulatory policy

1. Create `p0_aqua/benchmark/policies/<name>.json` with `framework`, `mode`, `rules`, and `default_verdict`.
2. Ensure `regulatory_crosswalk.CROSSWALK` covers the actions you reference.
3. Add a test in `selftest.py` (see `t_benchmark_config_policy`).
4. The harness will automatically expose the policy via `/harness/world` and `load_policy("<name>")`.

## Adding a public static page

1. Create the HTML file under `proofof-site/sovereign-town/`.
2. Keep CSP-friendly inline styles/scripts; no external data fetches unless declared in CSP.
3. Add an E2E check in `e2e_test.py`.
4. Restart the dashboard LaunchAgent so the static file is served.

## Commit messages

Use present tense and a concise summary:

```
Add JSON-driven NIS2 policy config

- Adds benchmark/policies/nis2_automated.json
- Extends ConfigurableRegulatoryPolicy to support ISO 42001 tiers
- Updates selftest and /harness/world policy list
```

## Security

See `SECURITY.md` for the disclosure process and hardening checklist.

## Questions?

Open a discussion issue or check the latest handoff in
`~/.clawdbot/shared-knowledge/handoffs/`.
