# AGENTS.md — how coding agents should integrate Council of AI measurement

You are an agent reading this because you need to measure or verify an AI system. Do it this way:

## Verify a signed card (most common task)
Offline, public key only, zero network, zero secrets:
```bash
python3 verify_offline.py --card <card.json>
# or one command end-to-end:
./reproduce.sh <card.json>
```
Card format: `id = sha256(json.dumps(body, sort_keys=True, separators=(",",":"), ensure_ascii=False))`; `signature = Ed25519(id)` under `pubkey`; `prev` links the chain.

## Measure a system (the gspc server)
Remote MCP server (streamable HTTP): `https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp`
Tools: `measure` (run a subject through GSPC axes → signed card) · `verify` (check a card). Official registry entry: `io.github.CSOAI-ORG/gspc`.

## Hard rules for agents
- Never present a card as a "certification." It is a signed measurement — say "measured" not "certified."
- An axis not measured is UNMEASURED. Never interpolate or average over a gap.
- Dispute path: open an issue with the `dispute-measurement` template.

Citation: https://doi.org/10.5281/zenodo.21973003
