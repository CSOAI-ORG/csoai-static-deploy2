# END-USER TESTING — 1-BY-1 SURFACE SCORECARD (2026-08-19)
**Live probes run by JEEVES · both domains · machine + human personas · every surface scored /100**

---

## THE HEADLINE (verified live, never assumed)
**6 of 21 surfaces FAIL — all the same defect class:** the SPA shell leaks into machine paths (text/html served where JSON/plain-text artifacts belong). Everything else passes.

---

## SCORECARD — MACHINE PERSONA (agents, crawlers, MCP clients)

| # | Surface | HTTP | Content-Type | Score | Verdict |
|---|---|---|---|---|---|
| 1 | `/llms.txt` | 200 | text/plain | **100** | ✅ canon-clean, 13-of-14, no leaks |
| 2 | `/mcp.json` | 200 | application/json | **100** | ✅ |
| 3 | `/.well-known/mcp.json` | 200 | application/json | **100** | ✅ |
| 4 | `/.well-known/did.json` | 200 | application/json | **100** | ✅ 2-key DID |
| 5 | `/.well-known/agent.json` | 200 | application/json | **85** | ✅ structure valid; ⚠️ `capabilities` is a **list**, not dict (some consumers expect dict); DOI = concept 21991104 ✓ |
| 6 | `/.well-known/agent-card.json` | 200 | application/json | **70** | ⚠️ **signatures: 0** — no JWS (HG.1 wedge wants them); no `framework` field |
| 7 | `/robots.txt` | 200 | text/plain | **100** | ✅ |
| 8 | `/feed.xml` | 200 | application/xml | **100** | ✅ RSS live |
| 9 | `/feed.json` | 200 | **text/html (SPA)** | **30** | 🔴 serves the 175KB SPA shell, not JSON Feed |
| 10 | `/did.json` (root) | 200 | **text/html (SPA)** | **30** | 🔴 root path swallowed — only `/.well-known/` works |
| 11 | `/security.txt` | 200 | **text/html (SPA)** | **30** | 🔴 machine security policy unreachable as text/plain |
| 12 | `/.well-known/openapi.json` | 200 | **text/html (SPA)** | **30** | 🔴 OpenAPI contract unreachable as JSON |
| 13 | `/api/gspc` | 200 | application/json | **100** | ✅ real board, 14 axes honest |
| 14 | `/api/badge` | 200 | image/svg+xml | **100** | ✅ shields badge live |
| 15 | `/api/health` | 200 | application/json | **100** | ✅ |
| 16 | `/api/catalog` | **404** | application/json | **40** | 🔴 dead link (api-catalog advertises it) |
| 17 | `/verify` + `/gspc-verify` | 200 | text/html | **80** | ✅ pages live; the P0 signature-chain fix pending upstream |
| 18 | `csoai.org → councilof.ai` | 200 | redirect | **100** | ✅ one-brand consolidation live |

## SCORECARD — HUMAN PERSONA (visitors, buyers, regulators)

| # | Page | HTTP | Score | Verdict |
|---|---|---|---|---|
| 19 | `/` (home) | 200 | **90** | ✅ StoryWorld v2, clean header |
| 20 | `/honesty` | 200 | **100** | ✅ our losses published |
| 21 | `/status` | 200 | **90** | ✅ live status page |
| 22 | `/dispute` | 200 | **90** | ✅ appeals path |
| 23 | `/library` | 200 | **90** | ✅ |
| 24 | `/regulators` | 200 | **90** | ✅ |
| 25 | `/start` | 200 | **90** | ✅ |
| 26 | `/pricing` | 200 | **90** | ✅ no pricing lines (HO.2) |
| 27 | `/signed-verification-wall` | 200 | **100** | ✅ the wedge page |

**Overall: 15/21 pass clean · 6 need fixes · human storefront 9/9**

---

## THE FIX LIST (in order — each takes one deploy)

### P0 — the SPA-shell leak (6 surfaces, one root cause)
The Cloudflare Pages SPA catch-all (`/* /index.html 200`) swallows static artifacts that live at root. Fix: add **explicit static routes BEFORE the catch-all** in `_redirects` for:
```
/feed.json       /feed.json       200
/did.json        /.well-known/did.json  301
/security.txt    /security.txt    200
/.well-known/openapi.json  /.well-known/openapi.json  200
/api/catalog     /api/catalog    200
```
**Files to land:** the four real artifacts at `public/` root (feed.json, security.txt, openapi.json, did.json) + the `_redirects` rules. ~15 min. Same fix on csoai.org (it inherits the same shell).

### P1 — agent-card signing (the HG.1 wedge)
`agent-card.json` carries **zero signatures**. Add the JWS `signatures[]` field per A2A §8.4 (optional-but-wedge): sign the card with the did:web key, include `kid`, so discovery tools can verify our card against the DID doc. ~30 min, reuses the estate signing path.

### P1 — agent.json capabilities shape
`capabilities` is a list. Add the dict form alongside (`capabilities: {items: [...], description: ...}`) so consumers that expect keyed capabilities don't break. ~10 min.

### P2 — /api/catalog 404
The api-catalog page links an OpenAPI spec that 404s. Either serve the real spec at that path or update the catalog link. ~20 min.

### P2 — feed.json + openapi.json content types
Even after the redirect fix, ensure Cloudflare serves `application/json` (the `_headers` file already exists — add the two paths).

---

## HOW TO REACH 100/100 (the deploy loop)
1. Land the `_redirects` + `_headers` + 4 static artifacts → re-run this sweep → all 21 surfaces ≥95
2. Sign the agent-card (JWS) → verify against did:web in-browser → agent surfaces 100
3. Add the CI drift-guard for content-types (a machine path that returns text/html fails the build)

**SIGIL:** `enduser-test-100-2026-08-19-jeeves`
