# 🐉 CROSS-LINK AUDIT — 17 JUNE 2026
**Date:** 17 Jun 2026 | **Agent:** HERMES | **Sprint 1:** DATA DOMINANCE (Days 2-5)
**Scope:** 20 randomly sampled live Vercel deployments
**Method:** Extract all outbound href links, verify each target returns HTTP 200

---

## Methodology

20 deployments randomly sampled from 96 live deployments. For each:
1. Fetch index.html
2. Extract all `href="https://..."` links (excluding CDN/assets/schema.org/w3.org/fonts)
3. Curl each unique external URL with 10s timeout, follow redirects
4. Classify: 200 (live), 3xx (redirect), 4xx (dead), 5xx/error (unreachable)

---

### 1. `muckaway-deploy`
**URL:** https://meok-muckaway-ai.vercel.app | **Links found:** 8 | **Content:** enhanced

| # | Link | HTTP | Result |
|---|------|------|--------|
| 1 | `https://muckaway.ai/` | 200 | ✅ Live |
| 2 | `https://optimobile.ai/` | 200 | ✅ Live |
| 3 | `https://loopfactory.ai/` | 200 | ✅ Live |
| 4 | `https://haulage.ai/` | 200 | ✅ Live |
| 5 | `https://landlaw.ai/` | 200 | ✅ Live |
| 6 | `https://planthire.ai/` | 200 | ✅ Live |
| 7 | `https://tree-king.ai/` | 000 | 🔴 Unreachable |
| 8 | `https://meok.ai/` | 200 | ✅ Live |

### 2. `badge-deploy`
**URL:** https://badge.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 3. `koikeeper-deploy`
**URL:** https://koikeeper.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 4. `policy-gen-deploy`
**URL:** https://policy-gen.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 5. `keystone-playground-deploy`
**URL:** https://keystone-playground.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 6. `supplier-portal-deploy`
**URL:** https://supplier-portal.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 7. `integrations-deploy`
**URL:** https://integrations-deploy.vercel.app | **Links found:** 3 | **Content:** enhanced

| # | Link | HTTP | Result |
|---|------|------|--------|
| 1 | `https://meok.ai/integrations` | 200 | ✅ Live |
| 2 | `https://meok.ai` | 200 | ✅ Live |
| 3 | `https://app-deploy.vercel.app` | 200 | ✅ Live |

### 8. `gtm-deploy`
**URL:** https://gtm.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 9. `openpatent-ai-deploy`
**URL:** https://openpatent-ai-deploy.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 10. `demo-deploy`
**URL:** https://demo-deploy.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 11. `legal-acts-tracker-deploy`
**URL:** https://legal-acts-tracker-deploy.vercel.app | **Links found:** 5 | **Content:** enhanced

| # | Link | HTTP | Result |
|---|------|------|--------|
| 1 | `https://meok.ai/legal-acts-tracker` | 200 | ✅ Live |
| 2 | `https://meok.ai` | 200 | ✅ Live |
| 3 | `https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t` | 200 | ✅ Live |
| 4 | `https://buy.stripe.com/eVq6oJ3K49AC0ZTaqI8k91m` | 200 | ✅ Live |
| 5 | `https://app-deploy.vercel.app` | 200 | ✅ Live |

### 12. `play-deploy`
**URL:** https://play.vercel.app | **Links found:** 6 | **Content:** enhanced

| # | Link | HTTP | Result |
|---|------|------|--------|
| 1 | `https://nextjs.org` | 200 | ✅ Live |
| 2 | `https://nextjs.org/docs` | 200 | ✅ Live |
| 3 | `https://nextjs.org/learn` | 200 | ✅ Live |
| 4 | `https://github.com/vercel/next.js/tree/master/examples` | 200 | ✅ Live |
| 5 | `https://vercel.com/import?filter=next.js&amp;utm_source=create-next-ap` | 200 | ✅ Live |
| 6 | `https://vercel.com?utm_source=create-next-app&amp;utm_medium=default-t` | 200 | ✅ Live |

### 13. `help-deploy`
**URL:** https://help-deploy.vercel.app | **Links found:** 9 | **Content:** basic

| # | Link | HTTP | Result |
|---|------|------|--------|
| 1 | `https://meok.ai/help` | 200 | ✅ Live |
| 2 | `https://meok.ai` | 200 | ✅ Live |
| 3 | `https://meok-attestation-api.vercel.app/signup` | 404 | ❌ Dead (404) |
| 4 | `https://meok-attestation-api.vercel.app/llms.txt` | 200 | ✅ Live |
| 5 | `https://meok-attestation-api.vercel.app/openapi.json` | 200 | ✅ Live |
| 6 | `https://meok-attestation-api.vercel.app/catalogue` | 200 | ✅ Live |
| 7 | `https://github.com/CSOAI-ORG` | 200 | ✅ Live |
| 8 | `https://pypi.org/user/MEOK_AI_Labs/` | 200 | ✅ Live |
| 9 | `https://app-deploy.vercel.app` | 200 | ✅ Live |

### 14. `empire-deploy`
**URL:** https://empire.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 15. `privacy-deploy`
**URL:** https://privacy.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 16. `partner-finder-deploy`
**URL:** https://partner-finder.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 17. `terms-deploy`
**URL:** https://terms.vercel.app | **Links found:** 0 | **Content:** enhanced

| Link | Status |
|------|--------|
| *(none)* | SPA shell — no external links in static HTML |

### 18. `asisecurity-deploy`
**URL:** https://meok-asisecurity-ai.vercel.app | **Links found:** 6 | **Content:** enhanced

| # | Link | HTTP | Result |
|---|------|------|--------|
| 1 | `https://asisecurity.ai/` | 200 | ✅ Live |
| 2 | `https://meok.ai/` | 200 | ✅ Live |
| 3 | `https://csoai.org/` | 200 | ✅ Live |
| 4 | `https://agisafe.ai/` | 200 | ✅ Live |
| 5 | `https://suicidestop.ai/` | 200 | ✅ Live |
| 6 | `https://safetyof.ai/` | 200 | ✅ Live |

### 19. `for-regulators-deploy`
**URL:** https://for-regulators-deploy.vercel.app | **Links found:** 3 | **Content:** enhanced

| # | Link | HTTP | Result |
|---|------|------|--------|
| 1 | `https://for-regulators-deploy.vercel.app` | 200 | ✅ Live |
| 2 | `https://meok-attestation-api.vercel.app` | 200 | ✅ Live |
| 3 | `https://meok.ai` | 200 | ✅ Live |

### 20. `positions-deploy`
**URL:** https://positions.vercel.app | **Links found:** 5 | **Content:** enhanced

| # | Link | HTTP | Result |
|---|------|------|--------|
| 1 | `https://positions.trialanderror.org/` | 200 | ✅ Live |
| 2 | `https://trialanderror.org` | 200 | ✅ Live |
| 3 | `https://journal.trialanderror.org` | 403 | ❓ 403 |
| 4 | `https://blog.trialanderror.org` | 200 | ✅ Live |
| 5 | `https://github.com/TrialAndErrorOrg/websites` | 200 | ✅ Live |

---

## Summary

| Metric | Count |
|--------|-------|
| **Deployments audited** | 20 |
| **External links found** | 45 |
| **Live (200)** | 42 |
| **Redirects (3xx)** | 0 |
| **Dead (4xx/5xx)** | 1 |
| **Unreachable** | 1 |

**Link Health: 93.3% of links resolve**

---

## Key Findings

1. **Most deployments are SPAs** — external links rendered client-side, invisible to curl extraction
2. **Static meok-* pages contain cross-links** — primarily to meok.ai, csoai.org, GitHub repos
3. **Few dead links** — most external references resolve correctly
4. **Internal cross-linking is sparse** — few deployments link to sibling hive pages
5. **GitHub links all resolve** — CSOAI-ORG repo structure is intact

---

## Recommendations

1. Implement SSG/prerendering to expose link graph to crawlers
2. Build systematic inter-hive cross-linking (Sprint 2 M29)
3. Deploy .well-known endpoints on all domains missing them
4. Add periodic dead-link checking to cron engine fleet
5. Generate full link-graph visualization for ecosystem map page

---

*HERMES AGENT, 17 Jun 2026 — Cross-link audit complete.*
