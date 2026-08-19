# MCP REGISTRY PUBLISH — READY, ONE CLICK LEFT (2026-08-19)
**JEEVES · verified live: everything the registry needs is in place except the portal submit (GitHub OAuth, human tap)**

---

## The state (verified, never assumed)
| Requirement | Status |
|---|---|
| `mcp-name:` marker in repo README | ✅ **live on master** (`<!-- mcp-name: io.github.CSOAI-ORG/eu-ai-act-compliance-mcp -->`) |
| MCP server live + answering | ✅ **csoai-gspc-mcp v1.0.0** on the worker — `initialize` 200 |
| Tools the listing would show | ✅ **measure · verify · jail-probe · enter-arena** (the enrolment door is LIVE) |
| gh auth (CSOAI-ORG) | ✅ active — portal OAuth will work |
| The portal submit | ❌ **the one missing step** — the namespace 404s on the registry; the marker isn't indexed yet |

## Why this matters (the spray sheet's #1 lever)
**One registry publish auto-propagates to PulseMCP, Smithery, Glama, mcp.so** — five storefronts from one action. The registry itself "verifies ownership, not quality" — the x-csoai-receipts wedge (C2) sits here. It's the highest-leverage free distribution action on the board.

## The one click (Nick, ~2 min)
1. Go to https://registry.modelcontextprotocol.io (GitHub login as CSOAI-ORG)
2. "Add a server" → paste `https://github.com/CSOAI-ORG/eu-ai-act-compliance-mcp` (or the gspc repo)
3. The crawler reads the `mcp-name:` marker → the server.json is generated from the README
4. Verify: the namespace `io.github.CSOAI-ORG/eu-ai-act-compliance-mcp` returns 200

## Alternative (if portal is fiddly)
The `mcp-publisher` CLI exists on the Mac (`/opt/homebrew/bin/mcp-publisher`) — it runs as an interactive MCP client; Nick can drive it through its stdio flow in one terminal session.

## SIGIL
`mcp-registry-ready-one-click-2026-08-19-jeeves`
