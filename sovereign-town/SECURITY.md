# Sovereign Town — Security & Disclosure

Sovereign Town is an **in-simulation research engine**. It is not a production
control system. This document describes the current security model, bright lines,
and how to report a vulnerability.

## Scope

- `p0_aqua/` Python services (dashboard, harness, MCP SSE)
- Static public pages under `proofof-site/sovereign-town/`
- Ed25519 signing keys used for run manifests, passports, and attestations

Out of scope: third-party LLM APIs, the underlying host OS, and credentials stored
in unrelated LaunchAgents or dotfiles.

## Current controls

| Control | Where | Notes |
|---|---|---|
| Optional bearer auth on `POST /harness/run` and `/harness/live` | `benchmark/server.py` | Set `SOV_TOWN_API_TOKEN` to require a `Bearer` token |
| Per-IP rate limit + manifest cap | `benchmark/server.py` | Configurable via `SOV_TOWN_HARNESS_*` env vars |
| Request body / query length limits | `dashboard_server.py`, `benchmark/server.py` | `SOV_TOWN_MAX_BODY_BYTES`, `SOV_TOWN_MAX_QUERY_LENGTH` |
| Path-traversal-safe file APIs | `dashboard_server.py` | `_safe_path()` resolves targets under a known root |
| CORS origin allowlist | both servers | Empty default = deny cross-origin |
| Security headers (CSP, X-Frame-Options, etc.) | both servers | Added by `SecurityHeadersMiddleware` |
| Policy RCE whitelist | `benchmark/policy.py` | `load_policy()` only allows built-ins, `aia_*`, or an env allowlist |
| MCP leaderboard SSRF filter | `benchmark/mcp_server.py` | URL scheme/host allowlist |
| Ed25519 key encryption | `sign_lib.py` | Optional password-based encryption at rest |
| WebSocket regime per-client | `dashboard_server.py` | `_CLIENT_REGIMES` prevents one viewer mutating the feed for all |

## Bright lines

1. **No production deployment without review.** Sovereign Town is a research/demo
   stack; do not expose it to the public internet without additional hardening.
2. **No real PII.** Real-world moats ingest only aggregate public data. Names,
   full DOBs, addresses, and postcodes are stripped before any JSON is written.
3. **No financial transactions.** Ledger entries are Ed25519-signed simulation
   manifests, not monetary balances.
4. **No unauthenticated public writes.** If `SOV_TOWN_API_TOKEN` is set, all
   harness run/live endpoints require it.
5. **No manual SSH tunnels.** Use the managed KeepAlive LaunchAgents to bridge
   Mac↔VM services.

## Key handling

- The Ed25519 private key lives at `p0_aqua/.town_priv.key`.
- Set `SOV_TOWN_KEY_PASSWORD` to encrypt it at rest; the server will prompt once
  on first start if the key is unencrypted.
- Rotate the key by deleting `.town_priv.key` and `.town_pub.key`; the server will
  generate a new pair on next boot. Existing manifests signed with the old key will
  still verify if the old pubkey is retained in `verify/`.

## Reporting vulnerabilities

If you find a security issue in the Sovereign Town code or deployment:

1. Email `security@csoai.co` (or the repository owner if that alias is unavailable)
   with subject `[SECURITY] Sovereign Town`.
2. Include steps to reproduce, impact, and suggested mitigation.
3. Allow 90 days before public disclosure unless both parties agree otherwise.

Do not open a public issue for undisclosed vulnerabilities.

## Hardening checklist for public deploys

- [ ] Set `SOV_TOWN_API_TOKEN` to a high-entropy secret.
- [ ] Set `SOV_TOWN_KEY_PASSWORD` and store it in a secrets manager.
- [ ] Restrict `SOV_TOWN_CORS_ORIGINS` to the exact production origin.
- [ ] Run behind a reverse proxy (e.g., Cloudflare) with WAF and rate limiting.
- [ ] Move metrics/access logs to a centralized, tamper-resistant store.
- [ ] Replace in-memory rate-limit state with Redis for multi-worker deployments.
- [ ] Review and tighten the Content-Security-Policy for the production domain.
- [ ] Enable automatic security updates on the host and Python dependencies.
