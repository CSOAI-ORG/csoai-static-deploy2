# 05 — Revenue Product Wire (CEO) — Monday-ready
**Probed:** 23 Aug 2026 ~18:30 Europe/London · executor revenue-wire  
**Estate:** Nick Templeman / Council of AI · councilof.ai · meok.ai · proofof.ai

---

## Binding locks (do not dilute)

| Lock | Rule |
|------|------|
| Measurement body | CSOAI **measures / signs / re-attests**. NEVER certifies. NEVER remediates ranked systems. |
| Human rail | **Paddle** (MoR) — `councilof-ai/api-server/payments.js` already coded; env-gated |
| Agent rail | **x402 / CDP or PayAI** — `csoai-org-v2/layer0_tunnels/x402_gateway_wrap/` |
| Forbidden for product | Do **not** auth Stripe or Vercel for CSOAI product checkout (COBOL deploy still has Stripe inject — quarantine, do not revive) |
| Public chrome | **13 measured + jail floor + unnamed empty slot-15** |
| Same-owner verticals | planthire / industrialhire / MEOK may A2A-eat the live board — **disclose same-owner**; never say certified/compliant |
| Verify | **Free forever**, loginless (`/verify`, `/gspc-verify`) |

---

## 1. Live probe matrix (curl/WebFetch, this session)

### councilof.ai

| Surface | HTTP | Class | Soft-404? | Pays / free |
|---------|------|-------|-----------|-------------|
| `/` homepage | 200 | LIVE | — | free board CTAs |
| `/api/gspc` | 200 | LIVE | — | **free** board JSON (DOI 10.5281/zenodo.21991104) |
| `/api/cards` | 200 | LIVE | — | **free** cards registry (1 signed card) |
| `/api/dorado` | 200 | LIVE | — | market **context** rail (REPORTED beside MEASURED; never fused) |
| `/claimguard` | 200 | LIVE | — | ClaimGuard product page (schema.org Offer £0) |
| `/.well-known/mcp.json` | 200 | LIVE | — | agent MCP catalogue (4 tools on worker) |
| `/mcp.json` (root) | **404** | 404 | hard | use `.well-known` only |
| `/api/mcp` | 200 | LIVE | — | 6 MCP servers catalogue (Assess/Anchors/Ledger/Watchdog/Spectrum/Drift) |
| `/api/corrections` | 200 | LIVE | — | **free** honesty ledger |
| `/api/regulation` | 200 | LIVE | — | **free** deadline feed |
| `/api/reported` | 200 | LIVE | — | human REPORTED rail |
| `/verify` · `/gspc-verify` | 200 | LIVE | — | **free** verify forever |
| `/scoreboard` | 200 | LIVE | — | living board UI |
| `/pricing` | 200 | LIVE | — | “rail is free” narrative page |
| `/os` | 200 | LIVE hub | **lobby soft-routes** via `?lobby=*` | UX door (CouncilLobby / OsLauncher assets) |
| `/ag-ui` | **308 → `/?lobby=home`** | SOFT-ROUTE | **yes** — SPA lobby catch | agent UI alias, not a separate product yet |
| `/comparison/` | **308 → SPA** | SOFT | yes | honesty UI pending PR 394 JSON |
| `/api/comparison` | **404** | 404 | hard | needs PR **394** |
| `/ras` | **404** | 404 | hard | primary RAS booking shelf missing |
| `/catalog.json` | **404** | 404 | hard | storefront missing |
| `/council-ledger` | **404** | 404 | hard | stop citing until shipped |
| `/dorado` (page) | **404** | 404 | hard | API live; FE page not on councilof.ai |
| `/badge` | **404** | 404 | — | use `/api/badge` |
| `/api/badge` | 200 | LIVE **wrong chrome** | — | aria-label still **“GSPC measured: 13 of 14 axes”** (399 merged ≠ live) |
| `/api/checkout` · `/api/paddle/key` | **404** | INTERNAL / not mounted | — | Paddle code exists; not live |

### meok.ai / proofof.ai

| Surface | HTTP | Class | Notes |
|---------|------|-------|-------|
| `meok.ai/` | 200 | LIVE | MEOK OS / keys / archetypes — **same-owner** disclose vs CSOAI |
| `meok.ai/pricing` | 200 | DRAFT commerce | Free £0 live; Pro = schema.org **PreOrder**; CTAs → `/` not Paddle |
| `meok.ai/.well-known/mcp.json` | **404** | 404 | CSOAI mcp lives on council/proof |
| `meok.ai/os` | 200 | LIVE | MEOK OS surface |
| `proofof.ai/` | 200 | LIVE mirror | same CSOAI chrome as councilof.ai |
| `proofof.ai/api/gspc` | 200 | LIVE | same board |
| `proofof.ai/.well-known/mcp.json` | 200 | LIVE | same mcp.json |

### External DNS

| Host | Status |
|------|--------|
| `cobolbridge.ai` | **NXDOMAIN / unresolved** from probe network — deploy tree exists on Mac; public DNS not live |

---

## 2. M4 clawd inventory (ExternalShell)

| Asset | Path | State | Revenue role |
|-------|------|-------|--------------|
| **cobol-a2a-bridge-mcp** | `~/clawd/cobol-a2a-bridge-mcp/` | DRAFT atomic (75 LOC) — COPYBOOK→JSON→DID→ISO42001 probe→C2PA-style attest | **COBOL wrap** shelf — wrap don’t replace; paid pack_finance on Paddle |
| demo.cpy + record.json | same dir | demo fixtures | agent demo only |
| **cobolbridge-deploy** | `~/clawd/cobolbridge-deploy/` | DRAFT site + pricing; **Stripe inject still in pricing.html** | Quarantine Stripe; re-point to Paddle when DNS live |
| **ras-front.html** | `~/clawd/ras-front.html` | DRAFT 43 LOC — **HARDCODES inventedscores** (governance 0.931 etc.) | **DO NOT ship as-is.** Must bind to `/api/gspc` only. RAS = paid verdicts |
| **dorado_market.py** | `~/clawd/scripts/flywheel/dorado_market.py` | LIVE script; inject into build | PR **396** / refresh — market rows currently `last: null` |
| **dorado_gate.py** | `~/clawd/csoai-static-deploy2/dorado_gate.py` | INTERNAL hard-stop gate | measurement harness, not product chrome |
| **csoai.org/dorado/** | `~/clawd/csoai.org/dorado/` | INTERNAL FE (ciso/report/white-label) | Bond Market narrative — wire via `/api/dorado` on council |
| **payments.js (Paddle)** | `~/clawd/councilof-ai/api-server/payments.js` | INTERNAL coded; env-gated 503 until `PADDLE_*` | Human rail: packs EU AI Act £999 · Finance/COBOL £1499 · Growth £499 · Art50 £999 |
| **x402_gateway_wrap** | `~/clawd/csoai-org-v2/layer0_tunnels/x402_gateway_wrap/` | INTERNAL | Agent rail per-tool USDC |
| ClaimGuard source | `~/clawd/councilof-ai/public/claimguard.html` | LIVE on site | claim-vs-signed-artifact; free check / MCP tools |
| RAS thesis | `~/clawd/kimi-regen/_plans/sovos-ras-monorepo.md` | INTERNAL plan | per-verdict / honey / insurance trigger / jurisdiction packs |

---

## 3. Product classification — what pays vs free verify

| Product | Class | What the buyer pays for | What stays free |
|---------|-------|-------------------------|-----------------|
| **Verify / board / corrections / regulation** | LIVE | — | Always free. No login. |
| **Signed measurement card (3KB)** | LIVE (registry thin) | Paid: full report pack, dataset export, re-attest booking | Verify signature + recompute |
| **ClaimGuard** | LIVE page / DRAFT monetization | Optional agent MCP volume (x402) + enterprise pack | Local `claimguard check` / page copy |
| **RAS (Regulation-as-a-Service)** | **404 public** / DRAFT Mac | **Primary human paid:** booking assessment packs via **Paddle**; continuous OSCAL-importable evidence | Methodology + empty-cell honesty |
| **Dorado / Bond Market (SOV SIGNAL)** | LIVE API / DRAFT FE | Future: parametric trigger observations / insurer rail (context never fused into grade) | Pair-gap JSON as measured+reported context |
| **MCP tools** (`.well-known/mcp.json` + `/api/mcp`) | LIVE catalogue | Agent calls beyond free quota → **x402/CDP/PayAI** | `verify` tool free; measure may meter |
| **Council OS + AG-UI** | LIVE hub + soft alias | UX door into paid shelves — not itself a fee | Lobby, board, verify |
| **COBOL Bridge wrap** | DRAFT MCP + DNS down | **pack_finance** Paddle + agent wrap calls x402 | Demo attest script |
| **MEOK** | LIVE marketing / PreOrder Pro | Separate same-owner head — do not blend into CSOAI ranking | Free key / open models |
| **Same-owner A2A eaters** (planthire etc.) | INTERNAL/POC | Vertical agents consume live board | Disclose same-owner; never “certified” |
| **Arena Elo / OS benchmarks** | OPEN PR 387 | Sibling feed only until n≥30 + 4-way + keystone | Do not invent scores |

### Payment rails map

```
Human browser ──Paddle──► /api/checkout?product=pack_* ──webhook──► signed entitlement cert
Agent / MCP   ──x402/CDP/PayAI──► paywalled tool call (gateway wrap)
Verify path   ──£0 forever──► /verify · /gspc-verify · ClaimGuard local check
```

---

## 4. Gaps (honest)

| Gap | Severity | Fix |
|-----|----------|-----|
| Badge still “13 of 14” | P0 honesty | Promote merged **399** (and homepage **398**) to live Pages |
| Dorado market `last: null` | P1 | Merge/refresh **396** + run `dorado_market.py` inject |
| `/api/comparison` 404; `/comparison` soft SPA | P1 | Ship PR **394** JSON then real FE |
| `/ras` 404; ras-front invents scores | P0 if shipping | Rebuild FE to **only** print `/api/gspc`; add Paddle CTA |
| `/catalog.json` 404 | P1 storefront | Static catalog: ClaimGuard, RAS packs, Dorado, COBOL, MCP — assessed not certified |
| `/council-ledger` 404 | P2 | Ship or stop citing |
| Paddle endpoints 404 live | P1 revenue | Mount payments.js + owner `PADDLE_*` env |
| `/ag-ui` only 308→lobby | P1 UX | Wire into Council OS one-door (**367**) after proof |
| COBOL DNS + Stripe leftover | P2 | DNS owner gate; strip Stripe; Paddle only |
| ras-front hardcoded scores | **BLOCK** | Inventing scores = binding lock violation |

---

## 5. Open PR → ship order (Mon–Fri, smallest first)

Goal: FE seamless with shelves · **no invented scores** · **no certify language**.

| Day | Ship | Why smallest / safe |
|-----|------|---------------------|
| **Mon** | Promote **398** + **399** (merged, not live) · badge chrome “13 measured + jail floor” | Honesty P0; zero product invention |
| **Tue** | Proof + merge **396** Dorado static/market inject · confirm `/api/dorado` rows non-null | Tiny surface; market is REPORTED not MEASURED |
| **Wed** | Proof + merge **394** comparison · expose `/api/comparison` (measured-vs-reported) | Honesty product; no grades invented |
| **Thu** | Ship **`/catalog.json`** + honest **`/ras`** (live from `/api/gspc` only) + ClaimGuard catalog entry · Paddle CTA stubs (503 until owner keys OK) | Revenue shelf without certifying |
| **Fri** | CEO-proof then merge **367** OS one-door · AG-UI alias into same lobby · careful **387** benchmarks as sibling feed only · **397** DOIs if proof green | Seamless FE; large PR last |

**Hold until after honesty P0:** unsigned Elo as board, 16-axis HF, named slot-15, any “certified/compliant” CTA.

---

## 6. Owner-only gates (Nick)

1. **Paddle** live products + webhook secrets (`PADDLE_API_KEY`, `PADDLE_WEBHOOK_SECRET`, `PADDLE_PRICE_*`) — no agent invents prices live.
2. **Do not** re-auth Stripe / Vercel for CSOAI product.
3. DNS for `cobolbridge.ai` / industrialhire if public shelf wanted.
4. arXiv endorser (deadline ~27 Aug) · LinkedIn Gmail · SOV3 GCP billing · Tailscale/A100 — from `04-monday-exec.md`.
5. Name slot-15 publicly **only** when CEO stamps (in-lane `instrument-honesty` stays unnamed).

---

## 7. Desk map (Mon)

| Desk | Job |
|------|-----|
| **Surface** | 398/399 live; catalog/ras routes; soft-404 hygiene |
| **Revenue** | Paddle mount + RAS booking CTA; x402 meter on MCP; Dorado 396 |
| **City** | Council OS one-door 367 after CEO proof; AG-UI into lobby |
| **Growth** | IP: signed cards + Zenodo DOIs + ClaimGuard receipts |
| **N-Sites** | HF honesty P0 before spray |
| **Measure** | Sit 14-axis stamp; jail = floor; empty slot-15; never certify |
| **Publisher** | No cite unsigned / 16-axis / filled slot-15 / “certified” |

---

## 8. One-line Monday thesis

**Sell assessed evidence packs (Paddle) and metered agent tools (x402); give away verify; wire OS/AG-UI as one door onto a catalog that already tells the truth about 404s and empty cells.**

