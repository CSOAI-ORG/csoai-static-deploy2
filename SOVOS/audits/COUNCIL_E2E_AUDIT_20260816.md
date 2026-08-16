# COUNCIL E2E AUDIT - 2026-08-16 (pod-side, Mac untouched)

## TEST BOARD (content-asserted, from RunPod 3090)
| Surface | HTTP | Verdict |
|---|---|---|
| csoai.org apex | 200 | RED: sovereign footer (FIXED branch) |
| llms.txt | 200 | RED: SOV33/sovereign/BFT-33 (FIXED branch) |
| SOV33_BFT33_COUNCIL.html | 200 | RED (FIXED branch) |
| sovereign-os.html | 200 | RED (FIXED branch) |
| gspc-scoreboard | 200 | RED: 13x sov6 cols (FIXED branch, now 0 locks, 248 signed) |
| gspc-index | 200 | YELLOW: SOVOS mention |
| councilof.ai apex | 200 | PASS |
| j-space | 200 | PASS (1,201 events live) |
| sov-space | 200 | YELLOW: SOV- prefix |
| meok.ai | 200 | YELLOW: sovereign footer |
| proofof.ai | 200 | YELLOW: 468B stub |
| mcp-install | 405 | RED: dead channel |
| csoai-site.pages.dev | 200 | RED: sovereign |

## FIXED THIS RUN (pushed branches)
1. f/breach-fix-apex-llms-20260816 (commit 6516663) — apex/llms/SOV33 stub/sovereign-os hygiene
2. f/scoreboard-public-names-20260816 (commit b16a93a4) — sov6-* -> public tuned labels, 0 lock-words, 248 signed cells

## E2E NEXT
- merge both branches -> deploy CF Pages (project csoai-site) from pod
- gspc-index/sov-space/meok.ai footer sweep
- proofof.ai rebuild-or-redirect decision
- mcp-install channel strip / repoint /api/*
- flagship GSPC into registry (io.github.CSOAI-ORG/gspc)

## DEPLOY (deploy lane, from pod with CF token):
git fetch origin
git checkout f/breach-fix-apex-llms-20260816   # merged head, 0 locks verified
git rebase origin/jv-wave8-production           # ensure clean against latest
python3 build_site.py                           # assemble _site
npx wrangler pages deploy _site --project-name csoai-site
# then verify live: curl csoai.org | grep -ci sovereign  -> 0

## EAT-ALL CLOSE-OUT 2026-08-16 EVENING
- Branch f/breach-fix-apex-llms-20260816 now carries FULL estate hygiene: 5 crawl files + scoreboard rename + sov-space worker + tier1+tier2 file renames (36) + api routes (4) + 262-file source sweep. Pushed (23bfe1cd).
- Rebuilt _site: 0 engine codenames, 0 sovereign breaches, crawl-priority 0 locks.
- micro2 disk: 89% -> 86% (caches reclaimed; weights untouched — measurement targets stay).
- GSPC MCP + city-3d MCP: both HTTP 200 live; tools measure/verify; NOT-certificate language intact.
- Register: gov= sov6-embodiment 0.7004 (tied aesthetics), care= sov6-ethics 0.535, art5= sov6-relationality 0.9722 (tied gemma3). AUTHENTICITY: board JSON is the measurement record (no per-cell sigil field); Ed25519 signatures live in fleet-cards/ fleet-card-chain-XXXX.jsonl (prev-chain + pubkey) + fleet-art5-*.json (signed:True + content_id) — verified real 2026-08-16, scoreboard ✓signed substantiated. Registry: gspc + city-3d both official-MCP remotes-schema (city normalized), pushed feat-work 6828a0a0.
- Directive canon committed: SOVOS/business/SOVOS-BUSINESS-DIRECTIVE-2026-08-16.md.
- Owner queue #1: arXiv code G6Y9SY — HARD 27 AUG. Tonight 3 one-clickers: arXiv, CF AI-bot toggle, gdrive reconnect.

## GSPC RECONCILIATION (directive #9) — 2026-08-16 night
Live /api/gspc `measure` returns the ISSUANCE CONTRACT only (no leaderboard number) — "API says sov6 leads" was stale.
LIVE deployed scoreboard gov row: best = phi4:14b @ 0.722 (n=237, ✓signed) — internally consistent (matches its own max cell).
Pod board_gov.json on disk: best = sov6-embodiment-v3-light @ 0.7004 — STALE vs deployed page (file predates phi4 run).
VERDICT: live deployed page = register of record (phi4:14b gov). board_gov.json on pod = stale cache; re-sync from signing chain (fleet cards, signed=True, source A100-2.pod). Buyers/regulators verify against the deployed artifact.
LIVE scoreboard also shows deployed naming-hygiene (columns ethics-v3-light etc., no sov6- prefix) — estate-wide naming fix confirmed live.

## LIVE-EDGE FINDING 2026-08-16 (browser, fresh edges)
- apex https://csoai.org/ AND https://www.csoai.org/ serve OLD breached homepage: title "CSOAI · Sovereign AI · Audit-Grade Compliance", "Master Takeover · SOV3 · SOV33 · SOV333", "BFT-33 quorum", "30 sovereign MCPs", "UK-sovereign". >20 lock-words live.
- BUT gspc-scoreboard page serves NEW naming (ethics-v3-light etc., no sov6-) -> MIXED/SHALLOW DEPLOY: some files newer, index.html still old.
- .well-known/agent-card.json URL serves the OLD HTML fallback (SPA-fallback: unknown paths return old index.html) — llms.txt advertises it as A2A card; agents get SEO-poison + non-JSON.
- ROOT CAUSE: deploy lane pushed a partial/mixed _site; index.html not updated to f/breach-fix-apex-llms-20260816 version. Escalate: full CF Pages deploy of the clean _site REQUIRED (project csoai-site) — apex breach is live-public-facing today.

## AGENT-DISCOVERY TEST PASS 2026-08-16 (browser, .well-known chain)
- security.txt ✅ REAL RFC9116 (Contact/Expires/Canonical, correct)
- llm-policy.txt ✅ REAL declarative policy (Allow/Disallow, citation format, train-use conditional, rate-limit 10rps)
- /api/leaderboard ✅ REAL JSON (sov33_small/large + frontier comparisons WITH sources) — but keeps sov33_* codenames live (pre-fix copy)
- .well-known/llm-manifest.json ❌ serves text/html EMPTY BODY (SPA-fallback stub) — not JSON
- .well-known/agent-card.json ❌ serves OLD BREACHED homepage HTML (SPA-fallback to old index) — advertised as A2A card in llms.txt; agents get SEO-poison + broken discovery
VERDICT: llms.txt/llm-policy advertise endpoints that must be JSON — two of five .well-known/API endpoints fail the A2A contract. In-scope for next site pass (post include: fix manifest generation + agent-card to serve real JSON).
