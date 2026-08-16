# Part CJ — Sovereign-Route Kill (councilof.ai) + HF Sov-Class Inventory
**Date:** 2026-08-13 · **Lane:** Kimi (frontend) · **Assigned by:** hermes (4-leaks settlement) · **Status:** SHIPPED to PR, merge gated on owner/hermes nod

## 1. What shipped

**PR:** https://github.com/CSOAI-ORG/councilof-ai/pull/150 · branch `feat/part-cj-sovereign-route-kill` · commit `beb47a6` · 58 files, +538/−536 · `npm run build:client` clean (vite + lint gates, 3m53s)

### Route rename map (old paths kept as client-side Redirects — zero dead links)
| Old | New canonical | Notes |
|---|---|---|
| `/sovereign` | `/council-hub` | SovereignHub |
| `/sovereign-twin` | `/council-twin` | SovereignTwin |
| `/sovereign-network` | `/council-network` | NetworkPage |
| `/sov-space`, `/sovereign-space`, `/simulate` | `/council-space` | SovSpace, query string preserved |
| `/sovereign-town` | `/council-city` → `/council-space?view=towns` | Council City is the brand term |
| `/sovereign-pricing` | `/pricing` | same component |
| `/gspc-arena`, `/towns`, `/globe`, `/world`, `/sov-towns` | → `/council-space?view=…` | repointed |

### Also in the PR
- **Art 50 disclosure registry** (`ai-surfaces.ts`) repointed to canonical routes; `/sovereign-space` entry merged with a dated note — the legal disclosure layer stays accurate.
- **AEO/SEO**: `llms.txt`, both sitemaps, 11 bench nav pages, `globe.html`/`sovspace*.html`, `regulatory-clock.json`.
- `generate-sitemap.mjs`: legacy sovereign redirects added to `EXCLUDE_EXACT` — sitemap now carries **canonical URLs only** (349 URLs, 0 sovereign-class).
- Post-rename grep: no user-visible sovereign-class strings remain outside the intentional set below.

### Deliberately untouched (flagged, not silently changed)
1. **External live endpoints** `proofof.ai/sovereign-town/*`, `proofof-site.vercel.app/sovereign-town/*` — real data feeds; renaming breaks pulls. Parks into AZ.3 (proofof.ai archive).
2. **"The Sovereign" agent persona** copy (dock/demo narration) — brand call above routes; owner decision.
3. **Code identifiers** (SovereignDock.tsx, sov-space-sim-mcp, etc.) — invisible to users.
4. **Deprecated root `src/`** (AppWithRouter.jsx) — dead code, confirmed via DEPRECATED-root-src.md + vite config.

## 2. HF sov-class inventory (read-only, 2026-08-13) — delist candidates

**42 public datasets, 6 sov-class:**
`sov34-1p5b-vs-baseline` · `oowm-sov-signal-v8` · `sov-signal-ground-truth-v8` · `sov-signal-leaderboard-v1` · `sov-signal-ground-truth-v10` · `sov33-v12-results`

**7 public models, 5 sov-class:**
`sov34-1p5b` · `sov-gate-ft2` · `sov-refusal-lora` · `sov-ethics-art5` · `sov-compliance-art5`

All 11 are public under `huggingface.co/csoai`. Canon name going forward is **Council Signal**; these are the sovereign-class public surface on HF.

**Proposed action (OWNER NOD REQUIRED — external visibility change, reversible):**
flip all 11 to **private** (not delete — reversible, no data loss), with a dated note in each card: "renamed into the Council Signal line; superseded sets remain available on request." Nothing flipped yet.

## 3. Gates
- PR #150 merge = deploy to Cloudflare Pages project `csoai` (master push auto-deploys). **Held for owner/hermes nod.**
- HF private-flip held for owner nod.

## 4. Verification trail
- Build: `npm run build:client` exit 0, 3m53s.
- Sitemap: regenerated, `grep -c "sovereign|sov-space" public/sitemap.xml` → 0.
- HF inventory: `GET /api/datasets?author=csoai` (42) + `/api/models?author=csoai` (7), live pull 2026-08-13.
