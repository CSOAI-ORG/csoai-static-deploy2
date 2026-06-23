# Sovereign Town — Runbook

Operational procedures for the `p0_aqua` engine on macOS. The canonical fleet
runs on the **Mac terminal** plus a GCP VM (`meok-backend`); this runbook covers
the Mac side. VM procedures are analogous via the managed `com.csoai.*` LaunchAgents.

## Services

| Service | Port | LaunchAgent label | Entry point |
|---|---|---|---|
| Dashboard + proxy | 3940 | `com.csoai.sovereign-town-dashboard` | `p0_aqua/dashboard_server.py` |
| Harness | 3941 | `com.csoai.sovereign-town-harness` | `p0_aqua/benchmark/server.py` |
| MCP SSE | 3942 | `com.csoai.sovereign-town-mcp-sse` | `p0_aqua/benchmark/mcp_server.py` |

## Quick start (local)

```bash
cd p0_aqua
python3.11 selftest.py          # 45 unit/integration checks
python3.11 e2e_test.py          # 60 endpoint + WebSocket checks (needs services up)
./check.sh                      # full suite incl. optional Playwright tests
```

## Restart services after a code change

Always use `launchctl kickstart -k` so KeepAlive plists stay canonical. Never
spawn manual `nohup` tunnels or background Python processes.

```bash
launchctl kickstart -k gui/$(id -u)/com.csoai.sovereign-town-dashboard
launchctl kickstart -k gui/$(id -u)/com.csoai.sovereign-town-harness
launchctl kickstart -k gui/$(id -u)/com.csoai.sovereign-town-mcp-sse
```

Wait 2–3 seconds, then verify:

```bash
curl -s http://127.0.0.1:3940/api/health | python3 -m json.tool
curl -s http://127.0.0.1:3941/harness/health | python3 -m json.tool
curl -s http://127.0.0.1:3940/api/metrics | python3 -m json.tool
```

## Logs

LaunchAgents write to the macOS unified log. Tail with:

```bash
log stream --predicate 'process == "Python" AND eventMessage CONTAINS "sovereign"' --info --debug
```

For local debugging, run the server directly in the foreground:

```bash
cd p0_aqua
python3.11 dashboard_server.py
python3.11 -m benchmark serve --port 3941
```

## Environment knobs

See `p0_aqua/config.py` for the full list. Common overrides:

| Variable | Purpose | Default |
|---|---|---|
| `SOV_TOWN_API_TOKEN` | Bearer token for `POST /harness/run` and `/harness/live` | unset (open) |
| `SOV_TOWN_KEY_PASSWORD` | Encrypt the Ed25519 private key at rest | unset |
| `SOV_TOWN_CORS_ORIGINS` | Comma-separated allowed origins | empty (deny CORS) |
| `SOV_TOWN_MAX_BODY_BYTES` | Max POST body size | 1,048,576 |
| `SOV_TOWN_MAX_QUERY_LENGTH` | Max query-string length | 4,096 |
| `SOV_TOWN_HARNESS_MAX_RUNS_PER_MINUTE` | Per-IP rate limit for `/harness/run` | 10 |
| `SOV_TOWN_HARNESS_MAX_MANIFESTS_PER_HOUR` | Global signed-manifest cap | 100 |
| `SOV_TOWN_ACCESS_LOG` | Emit structured JSON access logs | `0` |
| `SOV_TOWN_METRICS_WINDOW` | Latency sample window | 10,000 |

Edit the plist `EnvironmentVariables` dictionaries to make overrides persistent,
then `launchctl bootout` / `bootstrap` the plist.

## Health checks

- Dashboard liveness: `GET /api/health`
- Harness liveness: `GET /harness/health` (via dashboard proxy or directly on :3941)
- Operational metrics: `GET /api/metrics` and `GET /harness/metrics`
- Public static mirror: `https://proofof.ai/sovereign-town/fleet-status.html`

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Connection refused` on :3940 | Dashboard not running | `launchctl kickstart -k gui/$(id -u)/com.csoai.sovereign-town-dashboard` |
| `/harness/*` returns 502/000 | Harness down or proxy blocked | Restart harness; check `HARNESS_URL` |
| E2E `CORS default restricted` fails | `SOV_TOWN_CORS_ORIGINS` set unexpectedly | Leave default empty for tests |
| `POST /harness/run` 429 | Rate limit or manifest cap reached | Wait one minute, or raise `SOV_TOWN_HARNESS_MAX_RUNS_PER_MINUTE` |
| `api/health` shows `degraded` | `town_sim_live` snapshot failed | Check `town_sim_live.py` logs; restart dashboard |

## Disaster recovery (Mac)

1. Confirm plist files are loaded: `launchctl list | grep sovereign-town`.
2. Kickstart each service.
3. Re-run `./check.sh`.
4. If corruption is suspected, regenerate static artifacts:
   - `python3.11 policy_lab.py report experiments/dora_finance.json`
   - `python3.11 dashboard_server.py` will re-serve the latest static files.

## VM bridge

The Mac reaches VM services through canonical KeepAlive SSH tunnels managed by
`com.meok.sov3-vm-tunnel` and related plists. Do **not** create manual `ssh -L`
tunnels; they collide with the managed plists and cause fake outages. See
`~/.clawdbot/shared-knowledge/README.md` for the full substrate topology.
