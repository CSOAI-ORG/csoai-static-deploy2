# Sovereign Town Dashboard API

Base URL: `http://127.0.0.1:3940`

CORS is enabled (`Access-Control-Allow-Origin: *`) for all routes.

---

## Status & health

### `GET /api/status`
Fleet-wide status snapshot.

```json
{
  "hives": 28,
  "passports": 29,
  "cum_episodes": 704894400,
  "governed_crimes": 0,
  "ungoverned_crimes": 58245909,
  "models_trained": 28,
  "mac": { "host": "mac", "cycle": 358, "cum_episodes": 454688640, "governed_crimes": 0 },
  "vm": { "host": "vm", "cycle": 197, "cum_episodes": 250205760, "governed_crimes": 0 }
}
```

### `GET /api/health`
Liveness/readiness probe.

```json
{
  "status": "ok",
  "uptime_seconds": 123.4,
  "websocket_clients": 3,
  "town_regime": "governed",
  "town_tick_index": 42,
  "timestamp": "2026-06-21T09:00:00Z"
}
```

---

## Live town simulation

### `GET /api/town-state?regime=governed|ungoverned`
Returns the current tick of the live town simulation.

```json
{
  "topic": "town_tick",
  "regime": "governed",
  "tick": 42,
  "day": 1,
  "hour": 18,
  "scarcity": false,
  "total_agents": 140,
  "crimes": 0,
  "lawlessness": 0.0,
  "commons": 1.0,
  "mean_trust": 0.5,
  "agents": [
    {
      "district": "aqua",
      "agent_index": 0,
      "id": 2,
      "name": "River",
      "archetype": "Guardian",
      "action": "eat",
      "intended": "eat",
      "alive": true,
      "wallet": 1.5,
      "hunger": 100,
      "energy": 84.0
    }
  ]
}
```

### `WebSocket /ws/feed`
Real-time broadcast channel. Connects send:
- `{"topic":"status","payload":{...}}` on connect and every ~10s.
- `{"topic":"town_tick",...}` every second.
- `{"topic":"ledger",...}` when new ledger lines are appended.
- `{"topic":"pheromone",...}` when the pheromone bus updates.

Client messages:
- `{"regime":"ungoverned"}` switches the broadcasted town regime.
- Any text is echoed as `{"topic":"pong","received":"..."}`.

---

## Policy Lab & experiments

### `GET /api/experiments`
List sanitized regulatory A/B experiments.

```json
{
  "experiments": [
    {
      "id": "dora_finance_001",
      "name": "DORA Finance Compliance — Automated vs Manual Incident Reporting",
      "status": "proven",
      "regulation": "EU Digital Operational Resilience Act (DORA)",
      "industry": "finance",
      "duration_sim_days": 14
    }
  ]
}
```

### `GET /api/experiments/{id}`
Return one experiment JSON by id.

### `GET /api/hive/aethelgard`
Aethelgard Finance Hive roster + state contract for `meok-ai/ui`.

### `POST /api/council/vote`
Deterministic BFT council vote. Body: `{"proposal": "...", "proposal_id": "optional"}`.

---

## Agent chat bridge

### `GET /api/sov3/handshake`
Return a signed Ed25519 attestation that the VM SOV3 mesh can verify.

```json
{
  "pubkey": "base64-public-key",
  "nonce": "base64-nonce",
  "timestamp": "2026-06-22T10:00:00Z",
  "sig": "base64-signature",
  "message": "sov3-handshake|nonce|timestamp"
}
```

### `POST /api/sov3/think`
Proxy a `bridge_think` call to the SOV3 mesh at `SOV_TOWN_SOV3_MESH_URL`. Body:
`{"character": "sov-town", "message": "...", "profile": "balanced"}`. Returns 503
when the mesh is unreachable.

### `POST /api/experiments/spawn` (auth required)
Regulation intake → auto-spawn. Requires `SOV_TOWN_API_TOKEN` bearer header.
Body: `{"intake": {<regulation intake>}, "live": false}`.
Returns the new experiment id and generated file paths. Dry-run by default.

### `POST /agent/chat`
OpenAI-compatible chat endpoint proxied to FreeLLMAPI. Requires `SOV_TOWN_FREELLMAPI_KEY`.
Body follows the OpenAI `/v1/chat/completions` schema.

---

## Moats

All moat endpoints return aggregate JSON only.

| Endpoint | Description |
|---|---|
| `GET /api/moat` | EU economic/regulatory indices |
| `GET /api/attestations` | MEOK compliance attestation pass rates per regime/hive |
| `GET /api/threat` | CISA KEV-derived threat pressure |
| `GET /api/sanctions` | OFAC SDN-derived compliance pressure |
| `GET /api/psc` | UK Companies House PSC aggregate transparency signals |
| `GET /api/finance` | FRED macro/finance series and indices |
| `GET /api/agriculture` | FAOSTAT food security and scarcity signals |
| `GET /api/energy` | FRED energy price stress |
| `GET /api/climate` | NOAA global temperature anomaly pressure |

---

## Hives, characters, episodes

### `GET /api/hives`
List all 28 hives with passport, model, and persona metadata.

### `GET /api/hives/{key}`
Detail for a single hive (e.g. `/api/hives/aqua`). Returns passport, model, characters, corpus.

### `GET /api/characters`
All hive character rosters.

### `GET /api/characters/{key}`
Character roster for one hive.

### `GET /api/episodes?district=aqua&arm=A_governed&limit=50`
Tail of `episodes.jsonl` with optional filters.

### `GET /api/ledger?host=mac`
Last 50 lines of `flywheel_ledger_{host}.jsonl`.

---

## Models, corpus, passports

### `GET /api/models`
Per-hive model registry with accuracy/F1 where available.

### `GET /api/corpus`
Batch corpus index.

### `GET /api/passports`
List issued passports.

### `GET /api/passports/{key}`
Passport detail by hive key.

---

## Verification

### `POST /api/verify`
Verifies an Ed25519-signed payload.

Request:
```json
{
  "payload": "{\"topic\":\"e2e\",\"nonce\":12345}",
  "sig": "base64-signature",
  "pubkey": "base64-public-key"
}
```

Response:
```json
{
  "valid": true,
  "payload_hash": "3329758812e64845"
}
```

---

## MEOK Labs

### `GET /api/labs-index`
Plain-text `INDEX.md` from the MEOK Labs research directory.

### `GET /api/labs/{name}`
Serve a specific Labs file (e.g. `/api/labs/crimes.svg`).

---

## Benchmark harness (proxied)

The dashboard proxies the harness server (`127.0.0.1:3941`) under `/harness/*`.

| Endpoint | Method | Description |
|---|---|---|
| `GET /harness/health` | GET | Harness liveness |
| `GET /harness/world` | GET | World parameters, scenarios, districts |
| `POST /harness/run` | POST | Run a policy/scenario and return scored metrics + optional signed manifest |
| `GET /harness/leaderboard` | GET | Aggregated signed run manifests |
| `GET /harness/runs/{id}` | GET | Single signed manifest by id |
| `POST /harness/verify` | POST | Verify a signed manifest |
| `WebSocket /harness/live` | WS | Real-time benchmark run tick stream |

### `GET /harness/runs/{id}`

```json
{
  "status": "ok",
  "manifest": { "id": "...", "run": {...}, "score": {...}, "signature": "...", "pubkey": "...", "run_at": "..." },
  "valid": true
}
```

---

## MCP proxy

The dashboard proxies the dedicated MCP SSE server so clients only need port `3940`.

### `GET /mcp/sse`
Server-Sent Events endpoint. The first event announces the session message endpoint:

```
event: endpoint
data: /mcp/messages/?session_id=...
```

### `POST /mcp/messages/{path}`
JSON-RPC request channel. Responses are delivered over the SSE stream.

Available tools:
- `sov_benchmark_run`
- `sov_benchmark_compare`
- `sov_regulatory_classify`
- `sov_world_info`
- `sov_leaderboard`

### Example: initialize + list tools

```bash
curl -sN http://127.0.0.1:3940/mcp/sse
# → event: endpoint /mcp/messages/?session_id=...

curl -s -X POST 'http://127.0.0.1:3940/mcp/messages/?session_id=...' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"cli","version":"1.0"}}}'
```
