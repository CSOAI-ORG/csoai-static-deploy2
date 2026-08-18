# BRAND ALIGNMENT — all old surfaces fixed, branded, deployed (2026-08-18)
**Lane:** JEEVES (K3) · **Directive (Nick):** *"align all old not added and get it branded and perfect into all"*

---

## What was swept & fixed (the "old not added" items)

### 1. Live master site (councilof.ai = CF Pages `councilof-ai`, worktree) — 3 deploys
| Item | Before | After (live) |
|---|---|---|
| Home `<title>` | "…measurement body for AI compliance" | **"CSOAI — the independent measurement body for AI"** |
| HomeGlobe badge | "The measurement body for AI compliance" | **"The independent measurement body for AI"** |
| HomeGlobe H1 | "Is your AI following the rules?" | **"We measure AI systems against statute. You verify it."** |
| og:title / twitter:title | compliance wording | independent wording |
| **SOV3 → Sovereign OS** (naming lock) | "SOV3 — a governed sovereign substrate", "SOV3³ / OWEM", "powered by SOV3", routes /sov3-* | **"Sovereign OS"** in all public copy; routes renamed `/sovereign-os-{model-card,system-card,whitepaper}`; 301 redirects added |
| **Axis-count leak (GY.0 #4)** | "13 axes… plus jail — 14 quotable across the 16-slot grid" | **canonical "13 of the 14 GSPC axes are measured"** — fixed in **96 sector pages** |

### 2. Other live surfaces (verified, already clean)
- **www.csoai.org** — "Council of AI — we measure, we sign, we re-attest" ✅
- **meok.ai** — "MEOK — yours, on your keys · MEOK OS" ✅ (public brand, correctly named)
- **csoai-org-v2** — 402 (Vercel billing-blocked, known; not a branding issue)

### 3. What was intentionally NOT changed (canon-consistent)
- **Training certifications** (CEASAI courses) — legitimate education credentials, not Firewall-1 violations
- **Third-party quotations** ("approved by Santander's board", "endorsed by AU Council") — their claims, quoted
- **API paths** (`/sov3/sigil/*` in api-v1-spec) — the backend surface, changing breaks clients
- **Route identifiers** (`/sov3` workbench) — internal plumbing, not public copy
- **keywords meta "AI compliance"** — SEO indexing, not a certification claim

## Deployed (all to project `councilof-ai`, production)
1. `24f652dc` — title/badge/H1 Firewall-1 fix
2. `5792e8e3` — SOV3→Sovereign OS copy + routes + 96 sector-page axis fix
3. `445855c0` — 301 redirects sov3-* → sovereign-os-*

## Final live state (verified)
```
councilof.ai   → 200 · "CSOAI — the independent measurement body for AI" · 0 visible codenames · 13-of-14 framing live
www.csoai.org  → 200 · "we measure, we sign, we re-attest"
meok.ai        → 200 · "MEOK — yours, on your keys"
```

## SIGIL
`brand-alignment-all-surfaces-2026-08-18-jeeves`
