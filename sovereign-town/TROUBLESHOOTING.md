# Sovereign Town — Troubleshooting Guide

## Installation / dependencies

### `ModuleNotFoundError` when running tests

Make sure you are using the project virtual environment:

```bash
cd p0_aqua
./.venv/bin/python selftest.py
```

If `.venv` is missing, recreate it with `uv sync` or `pip install -r requirements.txt`.

### Playwright browsers missing

```bash
cd p0_aqua
.venv-playwright/bin/python -m playwright install chromium
```

## Port conflicts

Services default to:

- Dashboard: `:3940`
- Harness: `:3941`
- MCP SSE: `:3942`

If a port is in use, find and stop the stale process:

```bash
lsof -i :3940
kill <pid>
```

Or override ports via environment variables:

```bash
export SOV_TOWN_DASHBOARD_PORT=3950
export SOV_TOWN_HARNESS_PORT=3951
export SOV_TOWN_MCP_SSE_PORT=3952
```

## Stale fleet status

`fleet_status_mac.json` and `fleet_status_vm.json` are updated by runners. If
numbers look stale, restart the flywheel or trigger the status runner manually:

```bash
bash runners/mac/sovereign-town-status.sh
```

## MCP proxy issues

The dashboard proxies `/mcp/sse` and `/mcp/messages/` to the dedicated MCP
server. If the MCP client in `/workbench` cannot connect:

1. Check the MCP server is listening: `curl http://127.0.0.1:3942/health`
2. Check the dashboard health: `curl http://127.0.0.1:3940/api/health`
3. Look at `mcp.log` if you started the server manually.

## `/agent/chat` returns 503

Set `SOV_TOWN_FREELLMAPI_KEY` to enable the FreeLLMAPI proxy. Without a key the
endpoint returns 503 by design.

## `/api/sov3/think` returns 503

The endpoint proxies to `SOV_TOWN_SOV3_MESH_URL` (default `http://127.0.0.1:3101/mcp`).
Verify the managed SSH tunnel to the VM is alive:

```bash
launchctl kickstart -k gui/$(id -u)/com.meok.sov3-vm-tunnel
```

Never create manual `ssh -L` tunnels — they collide with the managed KeepAlive
agents.

## Tests fail because services are not running

`e2e_test.py` and `browser_test.py` require the dashboard, harness, and MCP
servers. Start them before testing:

```bash
./.venv/bin/python -m benchmark serve --port 3941 &
./.venv/bin/python -m benchmark mcp --transport sse --port 3942 &
./.venv/bin/python dashboard_server.py &
```

## Unencrypted Ed25519 key warning

Set `SOV_TOWN_KEY_PASSWORD` and re-run any signing command to encrypt
`.town_priv.key` at rest.
