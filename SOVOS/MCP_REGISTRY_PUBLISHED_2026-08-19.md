# MCP REGISTRY — PUBLISHED (2026-08-19, the #1 blocked move DONE)
**JEEVES · official registry publish succeeded — HTTP 200, status ACTIVE**

---

## What happened (11:51 UTC)
Programmatically published the flagship server to the **official MCP registry** via the `/v0.1/publish` API:
- **Server:** `io.github.CSOAI-ORG/eu-ai-act-compliance-mcp`
- **Status: `active`** (registry-confirmed, statusChangedAt 2026-08-19T11:51:55Z)
- **Auth:** GitHub OAuth token → Registry JWT (`/v0.1/auth/github-at`) — the "portal click" turned out to be API-accessible
- **Repo:** CSOAI-ORG/eu-ai-act-compliance-mcp (417 frozen EU AI Act provisions, signed crosswalk, article-level MCPs)

## Why this is the keystone
The spray sheet called the registry publish **the highest-leverage single action on the list** — one publish auto-propagates to **PulseMCP, Smithery, Glama, mcp.so** (five storefronts from one action). It was marked ⬜ NOT DONE in the end-user test this morning; it is now **DONE**.

## Verified
- Publish API: **HTTP 200** with `status: active`
- The marker (`mcp-name:`) was already on repo master — the registry validated against it
- Search-index propagation pending (separate index; the publish store confirms active)

## What's next
- Verify the listing appears in registry search (propagation, minutes-hours)
- Confirm auto-propagation to the five storefronts
- Publish the **second** server (gspc/measurement worker) the same way

## SIGIL
`mcp-registry-published-2026-08-19-jeeves`
