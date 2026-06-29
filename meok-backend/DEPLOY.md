# MEOK SOV3 Backend — Deployment Guide

**Status:** Sovereign · Production-ready · x402-enabled · MIT-licensed MCPs
**Port:** `3101` (the canonical SOV3 mesh port — never move it)
**Last verified:** 5 Jul 2026 — Hermes / JEEVES, Sprint Tick 6

---

## 1. Overview

The SOV3 backend (`sovereign-mcp-server`) is a FastAPI/Uvicorn server exposing the
MEOK sovereign composite — 222+ tools across 28 hives — over MCP (Model Context
Protocol) JSON-RPC at `POST /mcp`. It sits behind gunicorn (2 workers, graceful
restart) and is the single source of truth for the SOV3 mesh.

Two deployment targets are pre-configured: **Railway** (fastest, good DX) and
**Fly.io** (cheapest, sovereign-VM-style, persistent volume). Both use the same
`Dockerfile`.

---

## 2. Quick start (local)

```bash
cd /Users/nicholas/clawd/meok-backend
./start.sh                                # uses start.sh
curl -X POST http://127.0.0.1:3101/mcp \  # health-check (POST, see §4)
     -H 'Content-Type: application/json' \
     -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

Or straight Docker:

```bash
docker build -t meok-sov3:latest .
docker run --rm -p 3101:3101 --name sov3 meok-sov3:latest
```

---

## 3. Railway (one-click cold outreach)

```bash
# Install once
npm i -g @railway/cli && railway login

# First-time only — link the repo
railway link --project meok-sov3-backend

# Ship it
railway up --service meok-sov3-backend --environment production

# Tail logs
railway logs --service meok-sov3-backend | head -200
```

Railway will:
1. Build the `Dockerfile` (multi-stage, ~600 MB).
2. Run `gunicorn sovereign_mcp_server:app` with 2 uvicorn workers.
3. Issue a public URL on `*.up.railway.app` mapped to internal port `3101`.
4. Run `POST /mcp` healthcheck every 30 s, restart on failure.

Set secrets in the Railway dashboard (never commit):
- `MEOK_API_KEY` — bearer token for outbound calls
- `MEOK_OLM_SECRET` — Oracle Learning Mesh signing key
- `MEOK_BFT_PEERS` — comma-separated `host:port` for council peers

---

## 4. Fly.io (recommended for sovereignty)

```bash
# Install once
curl -L https://fly.io/install.sh | sh && fly auth signup

# First-time only — create app + volume
fly apps create meok-sov3-backend --region lhr
fly volumes create meok_data --size 10 --region lhr

# Deploy
flyctl deploy --remote-only   # builds in Fly's registry

# Verify
fly status
fly checks list

# Shell in
fly ssh console -C "/app/healthcheck.sh"
```

Blue/green deployment with auto-rollback on healthcheck failure.
Persistent `/data` volume for SQLite + sovereign cache (sovereign-mcp.db,
history.db, intuition engine state).

---

## 5. Production health-check

**CRITICAL:** Always use `POST /mcp` — **never `GET /health`** — see
`~/clawd/AGENTS.md` §3. The guardian GET-check false-kills the process.

A wrapper script (`healthcheck.sh`) is bundled:

```bash
./healthcheck.sh https://meok-sov3-backend.fly.dev
# → returns JSON-RPC `tools/list` response with 222+ tools
# → exit 0 on success, exit 1 on failure
```

Schedule it via:
- **UptimeRobot** — POST monitor to `/mcp`, 30 s interval (already configured).
- **Cron** — `*/5 * * * *  /Users/nicholas/clawd/meok-backend/healthcheck.sh`
- **GitHub Actions** — see `.github/workflows/healthcheck.yml`

---

## 6. Choosing Railway vs Fly

| Concern                | Railway                              | Fly.io                                 |
|------------------------|--------------------------------------|----------------------------------------|
| Cold-start time        | ~8 s                                 | ~6 s                                   |
| Egress pricing         | $0.10/GB                             | Free tier covers ~1.5 TB/mo           |
| Persistent volume      | No (ephemeral FS)                    | Yes (`fly volumes create`)            |
| Multi-region           | Yes, easy                            | Manual, slightly harder                |
| Sovereign / UK data    | `europe-west2` ✓                     | `lhr` (London) ✓                       |
| Best for               | Demos, cold-outreach landing pages   | Long-running sovereign workloads       |

For cold-outreach Sir Nick is shipping now → **start on Railway**, graduate
to Fly once you have ≥ 100 paying tenants.

---

## 7. Operational checklist

- [ ] `sovereign_mcp_server.py` imports cleanly (`python -c "import sovereign_mcp_server"`)
- [ ] `requirements.txt` is pinned (`pip freeze > requirements.txt`)
- [ ] `Dockerfile` builds in < 90 s on a 4-core machine
- [ ] Health-check is `POST /mcp` (not `GET /health`)
- [ ] Secrets in platform dashboard, not in repo
- [ ] Log drain configured to Axiom/Datadog (or `railway logs --tail`)
- [ ] UptimeRobot monitor green for ≥ 24 h before announcing

---

## 8. Rollback

Railway:
```bash
railway rollback --service meok-sov3-backend --environment production
```

Fly:
```bash
fly releases && fly releases rollback <version>
```

Docker:
```bash
docker tag meok-sov3:previous meok-sov3:latest
```

---

## 9. Emergency stop (rare — only if SOV3 misbehaves)

```bash
# Railway
railway scale --service meok-sov3-backend --environment production --replicas 0

# Fly
fly scale count 0 --app meok-sov3-backend

# Local
launchctl kickstart -k gui/$(id -u)/com.meok.sov3-gunicorn 2>/dev/null || pkill -f sovereign_mcp_server
```

Never kill without first capturing a stack:
```bash
py-spy dump --pid $(pgrep -f sovereign_mcp_server) > /tmp/sov3-stack-$(date +%s).txt
```

---

## 10. Sovereign-law reminder

Per `AGENTS.md` §3:
- `stack.yml` on Mac is **never** pushed to origin blind — VM is authoritative.
- The CSOAI rebrand script is **buggy** — do **not** re-run on any MCP until fixed.
- `POST /mcp` for healthcheck — **never** `GET /health`.

— 🜏 Sovereign Composite, 2026.
