# COUNCIL E2E AUDIT — 2026-08-16 (pod-side, Mac untouched)

**Register:** REAL = probed/verified this run · FIXED = merged-or-branched · GATED = owner · TODO = lane

## §0 — TOP-DOWN ALIGNMENT (the binding hierarchy)
Four master docs bind: **DISTRIBUTION-MASTER** (receipts-first, 100 verified contacts, no spam) ·
**PRODUCTION-READY** (§1-A integrity before distribution; §1-B global bar) · **EAT-PLAY** (33-move
stack + 300 zero-gate moves; PR #75 v2 highest-authority) · **POWER-STACK** (frontend/colosseum/
arena/fabric deepen). Ratchet rule: every move produces/cites/requires signed cards.

## §1 — END-USER TEST BOARD (all probed from pod, content-asserted)
| Surface | HTTP | Size | Assert | Verdict |
|---|---|---|---|---|
| csoai.org apex | 200 | 5,186B | Council of AI ✓ | 🔴 LOCK: sovereign (footer) |
| www.csoai.org | 200 | 5,186B | ✓ | 🔴 same |
| csoai.org/llms.txt | 200 | 3,130B | ✓ | 🔴 LOCK: SOV33+sovereign+BFT-33 |
| SOV33_BFT33_COUNCIL.html | 200 | 12,952B | BFT | 🔴 LOCK: SOV33+BFT-33 |
| gspc-scoreboard | 200 | 61,515B | signed | 🔴 LOCK: 13× sov6 columns (249 signed cells, phi4:14b art5 1.000) |
| gspc-index | 200 | 5,184B | 57 | 🔴 LOCK: SOVOS |
| councilof.ai apex | 200 | 8,494B | Council | ✅ PASS |
| j-space | 200 | 8,427B | signed | ✅ PASS (1,201 events live) |
| sov-space | 200 | 10,690B | axes | 🔴 LOCK: SOV- prefix |
| meok.ai | 200 | 42,999B | MEOK | 🔴 LOCK: sovereign |
| proofof.ai | 200 | 468B | — | 🟡 stub, decision needed |
| mcp-install | 405 | 0 | — | 🟡 dead channel |
| sovereign-os.html | 200 | 22,333B | — | 🔴 LOCK: SOV33+SOVOS+sov- |
| csoai-site.pages.dev | 200 | 4,248B | — | 🔴 LOCK: sovereign |

**Score this run: 2 PASS · 10 RED · 2 AMBER**

## §2 — WHAT WAS FIXED (this run, pod-side, pushed)
- **A2-crawl-priority cleanup** — branch `f/breach-fix-apex-llms-20260816` (commit 6516663):
  apex index.html (25 locks → 0), llms.txt (7 → 0), SOV33 stub (1 → 0), sovereign-os (16 → 0).
  Protected main clean (c755d9f). **Merge+deploy = deploy lane.**

## §3 — THE E2E SEAMS (for seamless, frictionless end-user experience)
1. **Naming-lock residual pillars** (lane): gspc-scoreboard 13 sov6 columns, gspc-index SOVOS,
   sov-space SOV- prefix, meok.ai sovereign footer. Same fix pattern as §2 — generator display-name
   mapper + footer sweep. [LANE, next]
2. **proofof.ai decision** (owner): build or redirect [NICK].
3. **mcp-install** dead channels: strip globe.csoai.org/mcp + pip claims until real [LANE A3].
4. **/api/*** repoint to oracle-micro-2 JSON-content sentinel (live JSON not SPA fallback) [LANE A4].
5. **Stale DNS A record** 162.255.119.208 + cfat_ revoke [NICK 5 min].
6. **Kaggle /csoai claim** + HF org [NICK 5 min].
7. **GSPC flagship into MCP registry** (306 servers live, flagship absent — the land-grab gap) [LANE EF5].

## §4 — VISUAL/TEST EVIDENCE
- scoreboard: live 13×22, 249 cells signed, per-cell n+CI — phi4:14b art5 1.000 cell visible.
- j-space: canvas renders, 1,201 events, "every dot signed + hash-chained".
- apex: title correct ("Council of AI — the measurement body for AI compliance"), footer breach located.

## §5 — DEFINITION OF DONE (e2e)
All §0 boards green under sentinel · gspc flagship in registry · 250+ of 300 sites probed-listed ·
rail meters a real call · colosseum one-click GO · every page a signed claim → verify path.