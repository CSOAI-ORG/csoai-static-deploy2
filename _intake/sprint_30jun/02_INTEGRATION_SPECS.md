# Integration specs — 6 specs for the sovereign stack

## 1. Cognee (23.4K★, Apache 2.0) — AI memory layer
- Replace `meok-sovereign-memory-mcp` in-memory store with Cognee pipeline
- Cognee pipeline: ingest → graph construction → entity extraction → semantic search
- Sign every Cognee graph node with Ed25519 (uses our key store)
- REST endpoint: `POST /cognee/add` + `POST /cognee/search`
- Map Cognee's `add()` to `sov_memory_store`, `search()` to `sov_memory_recall`

## 2. MLflow (26.7K★, Apache 2.0) — agent engineering
- Track every sovereign MCP tool call as an MLflow run
- Parameters: tool_name, agent_id, decision (allow/deny/veto)
- Metrics: latency, verify_count, verify_success_rate
- Artifacts: signed receipts (`.json`), governance decisions (`.json`)
- Endpoint: `POST /mlflow/api/2.0/mlflow/runs/create` for each MCP call
- Dashboard: MLflow UI on http://localhost:5000 (default)

## 3. AG-UI Protocol (14.4K★, Apache 2.0) — agent-to-UI events
- SOV3 substrate emits AG-UI events on every MCP tool call
- Event types: `agent_thinking`, `tool_call`, `agent_message`, `agent_error`
- Frontend (Next.js 15) consumes via WebSocket / Server-Sent Events
- Endpoints: `wss://meok.ai/ag-ui/stream` + `POST /ag-ui/event`
- Maps to CesiumJS pulse, force-graph edge animation, VRM avatar lip-sync

## 4. Open WebUI (60K★, MIT) — sovereign chat layer
- Self-hosted Open WebUI instance at https://chat.meok.ai
- Connects to Ollama + sovereign MCP bridge (`mcp-bridge.meok.ai`)
- Tools: all 12 sovereign MCPs as MCP server endpoints
- Plugins: sovereign avatar (WebRTC), Ed25519 receipt viewer, EU AI Act audit panel
- Authentication: CSOAI passport (did:csoai:user:*) via OpenID Connect

## 5. iOK Farm IoT (the physical beacon)
- ESP32 + pH/DO/temperature sensors on the 13m koi pond
- MQTT broker: `mqtts://iot.meok.ai:8883` (TLS 1.3, client cert)
- Topic: `sovereign/farm/pond/{sensor_id}` (one sensor every 30 sec)
- Sovereign MCP wrapper: `meok-sovereign-iot-mcp`
- CesiumJS globe: pulsing gold beacon at Lincolnshire when sensors healthy
- Killswitch: any agent trying to actuate a pump without BFT council = auto-blocked

## 6. Open Patent / IP wedge
- 7 inventions locally filed + Bitcoin-anchored (blocks 892342-892348)
- When public push happens: opens to openpatent.ai registry
- Public domain licensing on the BFT topology (the governance primitive is free)
- Patent pending on: 12-around-1 council quorum math, Ed25519 sigil chain integration, sovereign MCP bridge protocol
- Filing fee: $30K via legal counsel (gated on the wall)
