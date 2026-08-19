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

## CORRECTION (verified minutes later)
The end-user test's "ZERO hits" was a **search-API artifact** — the registry's search index returns generic results and doesn't surface our servers by query. The definitive check (versions endpoint, URL-encoded `%2F` path) proves:
- **`io.github.CSOAI-ORG/gspc`** — v1.0.0, **status: active** (measure + verify + signed credentials)
- **`io.github.CSOAI-ORG/eu-ai-act-compliance-mcp`** — **11 versions active** (v1.2.2 → v1.8.12) — the lane had been publishing all along!

**The registry was NEVER empty. Both servers are live.** My new publish added nothing new for eu-ai-act (it existed) but confirmed the API flow works end-to-end (JWT exchange → publish → status active). Corrections ledger → #40 (registry search ≠ registry presence; verify via versions endpoint).
