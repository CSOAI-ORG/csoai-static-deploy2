# Sovereign Town — Security Fix Log

Tracks security findings from the six-audit hardening sprint and their remediation.

## Verification

- `./selftest.py`: **45/45 passed**
- `./e2e_test.py`: **58/58 passed**
- `pytest browser_test.py`: **5/5 passed**

Run the full surface with the services up:

```bash
cd p0_aqua
python3.11 selftest.py
python3.11 e2e_test.py
source .venv-playwright/bin/activate && pytest browser_test.py
```

## Environment knobs

| Variable | Purpose | Default |
|---|---|---|
| `SOV_TOWN_CORS_ORIGINS` | Comma-separated allowed origins (e.g. `https://town.proofof.ai`). Empty = same-origin only. | *(empty)* |
| `SOV_TOWN_MAX_BODY_BYTES` | Maximum request body size in bytes. | `1048576` (1 MiB) |
| `SOV_TOWN_MAX_QUERY_LENGTH` | Maximum total query-string length. | `4096` |
| `SOV_TOWN_API_TOKEN` | Bearer token required for `POST /harness/run` when set. | *(unset, endpoint open)* |
| `SOV_TOWN_KEY_PASSWORD` | Passphrase to encrypt `.town_priv.key` at rest. | *(unset, key stored as raw base64)* |

## Findings & remediation

### P0 — Arbitrary policy import (RCE)
- **File:** `benchmark/policy.py`
- **Finding:** `load_policy()` accepted any dotted module path, allowing import of arbitrary modules/classes.
- **Fix:** Only built-in names (`sovereign_gate`, `strict`, `permissive`, `ungoverned`), `aia_required`, `aia_auto`, and explicit paths listed in `SOV_TOWN_POLICY_ALLOWLIST` are accepted.
- **Tests:** `t_benchmark_policy_whitelist` in `selftest.py`.

### P0 — Path traversal in dashboard file APIs
- **Files:** `dashboard_server.py`
- **Finding:** `api_labs_file` and `api_passport_detail` used user-supplied names to read files.
- **Fix:** Names are validated (`..`, leading `/`, etc.), paths are resolved with `_safe_path()` and re-anchored under their intended roots; traversal returns 404.
- **Tests:** `t_dashboard_path_traversal` in `selftest.py`.

### P0/P1 — Open CORS
- **Files:** `dashboard_server.py`, `benchmark/server.py`
- **Finding:** `CORSMiddleware(allow_origins=["*"])` permitted any website to call the API.
- **Fix:** Default is no CORS middleware. Origins are enabled only via `SOV_TOWN_CORS_ORIGINS`. `*` may be used for local dev but is not the default.
- **Tests:** `t_dashboard_cors_default_restricted` in `selftest.py`; `check_cors` in `e2e_test.py`.

### P1 — Missing security headers
- **Files:** `dashboard_server.py`, `benchmark/server.py`
- **Finding:** No CSP, X-Frame-Options, X-Content-Type-Options, or Referrer-Policy.
- **Fix:** Added `SecurityHeadersMiddleware` on both servers with a strict baseline CSP (`default-src 'self'`, `frame-ancestors 'none'`, etc.).
- **Tests:** `t_dashboard_security_headers` in `selftest.py`.

### P1 — Unbounded request sizes and query params
- **Files:** `dashboard_server.py`, `benchmark/server.py`
- **Finding:** `POST /api/verify` and other endpoints had no body-size cap; `/api/episodes?limit` accepted arbitrary integers.
- **Fix:** `RequestSizeLimitMiddleware` rejects bodies over `SOV_TOWN_MAX_BODY_BYTES` (413) and query strings over `SOV_TOWN_MAX_QUERY_LENGTH` (414). `/api/episodes` clamps `limit` to 1000.
- **Tests:** `t_dashboard_request_size_limits` in `selftest.py`.

### P1 — Unencrypted signing key
- **File:** `sign_lib.py`
- **Finding:** `.town_priv.key` stored raw base64 with only filesystem permissions protecting it.
- **Fix:** When `SOV_TOWN_KEY_PASSWORD` is set, the key is encrypted with Fernet derived via PBKDF2-HMAC-SHA256 (480k iterations). Existing plaintext keys are re-encrypted automatically. Without the password the module logs a warning.
- **Tests:** `t_sign_key_encryption` in `selftest.py`.

### P0 — Unauthenticated benchmark runs
- **File:** `benchmark/server.py`
- **Finding:** `POST /harness/run` could be invoked by anyone with network access.
- **Fix:** Optional `OptionalBearerAuthMiddleware` gates `/harness/run` (and `/harness/live`) when `SOV_TOWN_API_TOKEN` is set.
- **Tests:** `t_harness_optional_auth` in `selftest.py`.

### P0 — XSS via `innerHTML` in workbench
- **File:** `benchmark/workbench.html`
- **Finding:** Leaderboard, AIA list, and MCP tool select injected unsanitized server data into `innerHTML`.
- **Fix:** Added global `escapeHtml()` helper and used it for all dynamic strings; converted AIA list rendering to DOM nodes where possible.
- **Tests:** Covered by browser tests and manual code review.

### P1 — SSRF in MCP leaderboard tool
- **File:** `benchmark/mcp_server.py`
- **Finding:** `sov_leaderboard(harness_url)` fetched any URL supplied by an MCP client.
- **Fix:** Added `_is_safe_harness_url()` enforcing `http`/`https` scheme, no credentials in the URL, and an exact `/harness/leaderboard` path.
- **Tests:** `t_mcp_leaderboard_ssrf_defense` in `selftest.py`.

## Remaining items

- ~~Rate-limit / manifest-cap on `POST /harness/run`~~ — added `RateLimitMiddleware` (per-IP + manifest/hour cap).
- WebSocket regime switch auth gating or client-local regime (currently global state per viewer).
- URL scheme/host validation in MCP `sov_leaderboard` tool.
- Delete/encrypt the disabled LaunchAgent plist containing exposed API keys (operator action).
- Full accessibility pass on HTML pages (labels, focus, contrast, ARIA).
- Operations docs and key/ledger backup routine.
- Policy Lab experiment registry, BFT vote/spawn, and regulator-view dashboard (`docs/MEOK_POLICY_LAB_INTAKE.md`).

## Architecture cleanup (Day 3) — also security-relevant

- **Created `config.py`** to centralize ports/hosts/paths/security knobs so secrets and literals are not scattered.
- **Created `moat_common.py`** with one safe `load_moat()` implementation, safe JSON save (flush+fsync), and narrow exception types for network fetches.
- **Created `moat_params.py`** and removed moat-loading boilerplate from `sim.py`; moat files are loaded through the shared helper with proper defaults.
- **Tightened `except Exception:`** in all moat loaders to `(OSError, json.JSONDecodeError, ValueError)` or network-specific types, with logging.
- **Fixed file-handle leaks** in `sim.py` summary write and moat JSON writes by using context managers.
- **Extracted `_proxy_http()`** in `dashboard_server.py` so `/harness/*` and `/mcp/messages/*` share one hardened forwarding path.

## Notes

- No destructive deploys or commits performed as part of this sprint unless explicitly approved.
- Service restart after code changes: `launchctl kickstart -k gui/$(id -u)/com.csoai.sovereign-town-dashboard` (and `-harness`, `-mcp-sse`).
