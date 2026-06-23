# Deploy Manifest — Ready 17 Jun 2026

> **STATUS: STOP_DEPLOY** — Stage locally only. This manifest describes the complete deploy order for when the gate clears.
> All files are staged in `~/clawd/` and ready for `vercel --prod` deployment.

---

## Domain Groups & Priority

### meok.ai (Primary Domain)
**Vercel project:** `meok-ai-landing` (@ `~/clawd/meok.ai/`)

| Priority | File Path | Destination URL | Notes |
|----------|-----------|----------------|-------|
| **P0** | `meok.ai/public/article-50/marking.html` | `https://meok.ai/article-50/marking` | FAQPage schema fixed, Product schema present |
| **P0** | `meok.ai/public/article-50/index.html` | `https://meok.ai/article-50/` | Article 50 hub — verify schema coverage |
| **P0** | `meok.ai/public/article-50/transparency.html` | `https://meok.ai/article-50/transparency` | Transparency guide |
| **P0** | `meok.ai/public/article-50/deepfake.html` | `https://meok.ai/article-50/deepfake` | Deepfake detection page |
| **P0** | `meok.ai/public/article-50/bot.html` | `https://meok.ai/article-50/bot` | Bot disclosure page |
| **P0** | `meok.ai/public/article-50/code-of-practice.html` | `https://meok.ai/article-50/code-of-practice` | Code of Practice |
| **P0** | `meok.ai/public/pricing/index.html` | `https://meok.ai/pricing` | Main pricing — Stripe buy buttons |
| **P0** | `meok.ai/public/pricing/pro.html` | `https://meok.ai/pricing/pro` | Pro tier pricing |
| **P0** | `meok.ai/public/pricing/enterprise.html` | `https://meok.ai/pricing/enterprise` | Enterprise pricing |
| **P1** | `meok.ai/public/fleet.html` | `https://meok.ai/fleet` | MCP fleet page |
| **P1** | `meok.ai/public/ecosystem-map.html` | `https://meok.ai/ecosystem-map` | Ecosystem map |
| **P1** | `meok.ai/public/birthday-launch.html` | `https://meok.ai/birthday-launch` | Launch page |
| **P1** | `meok.ai/public/100-day-challenge.html` | `https://meok.ai/100-day-challenge` | Challenge landing |
| **P1** | `meok.ai/public/press-kit.html` | `https://meok.ai/press-kit` | Press kit |
| **P1** | `meok.ai/public/partners.html` | `https://meok.ai/partners` | Partners page |
| **P1** | `meok.ai/public/manifesto.html` | `https://meok.ai/manifesto` | Manifesto |
| **P1** | `meok.ai/public/by-numbers.html` | `https://meok.ai/by-numbers` | By the numbers |
| **P2** | `meok.ai/public/api/stripe-webhook.html` | `https://meok.ai/api/stripe-webhook` | API docs — Stripe |
| **P2** | `meok.ai/public/api/x402-endpoint.html` | `https://meok.ai/api/x402-endpoint` | API docs — x402 |
| **P2** | `meok.ai/public/blog/blog-eu-ai-act-article-50.html` | `https://meok.ai/blog/eu-ai-act-article-50` | Blog post |
| **P2** | `meok.ai/public/eu-ai-act/comparison-table.html` | `https://meok.ai/eu-ai-act/comparison-table` | Comparison table |
| **P2** | `meok.ai/public/industry-solutions/index.html` | `https://meok.ai/industry-solutions` | Industry solutions hub |
| **P2** | `meok.ai/public/eu-code-of-practice.html` | `https://meok.ai/eu-code-of-practice` | EU Code of Practice |
| **P2** | `meok.ai/public/sectors/*.html` | `https://meok.ai/sectors/{name}` | Sector pages (11 files) |
| **P2** | `meok.ai/public/comparisons/*.html` | `https://meok.ai/comparisons/{name}` | Competitor comparison pages |
| **P2** | `meok.ai/public/lead-magnets/*.html` | `https://meok.ai/lead-magnets/{name}` | Lead magnet pages |
| **P2** | `meok.ai/public/assets/cross-domain-nav.html` | `https://meok.ai/assets/cross-domain-nav` | Cross-domain nav component |

---

### proofof.ai (Compliance MCP Suite)
**Vercel project:** `proofof-ai` (@ `~/clawd/proofof-ai/`)

| Priority | File Path | Destination URL | Notes |
|----------|-----------|----------------|-------|
| **P0** | `proofof-ai/index.html` | `https://proofof.ai/` | Homepage — verify buy buttons |
| **P1** | `proofof-ai/verify.html` | `https://proofof.ai/verify` | Verification page |
| **P2** | `proofof-ai/public/llms.txt` | `https://proofof.ai/llms.txt` | LLM access file |
| **P2** | `proofof-ai/public/.well-known/agent.json` | `https://proofof.ai/.well-known/agent.json` | Agent card |

**Root files also at `~/clawd/proofof.ai/` (static Vercel):**
| Priority | File Path | Destination URL |
|----------|-----------|----------------|
| **P0** | `proofof.ai/index.html` | `https://proofof.ai/` |

---

### csoai.org (AI Safety Council)
**Vercel project:** `csoai-org` (@ `~/clawd/csoai-org/`)

| Priority | File Path | Destination URL | Notes |
|----------|-----------|----------------|-------|
| **P0** | `csoai-org/index.html` | `https://csoai.org/` | Homepage |
| **P0** | `csoai-org/pricing/index.html` | `https://csoai.org/pricing` | Pricing — Stripe buttons |
| **P1** | `csoai-org/sovereign-town/index.html` | `https://csoai.org/sovereign-town` | Sovereign town page |
| **P1** | `csoai-org/connect/mcp/index.html` | `https://csoai.org/connect/mcp` | MCP connect page |
| **P1** | `csoai-org/signup/index.html` | `https://csoai.org/signup` | Signup page |
| **P2** | `csoai.org/index.html` | `https://csoai.org/` | Static site root |
| **P2** | `csoai.org/sovereign-town/index.html` | `https://csoai.org/sovereign-town` | Town page (static copy) |
| **P2** | `csoai.org/public/llms.txt` | `https://csoai.org/llms.txt` | LLM access file |

---

### cobolbridge.ai (Legacy Modernization)
**Vercel project:** `cobolbridge-deploy` (@ `~/clawd/cobolbridge-deploy/`)

| Priority | File Path | Destination URL | Notes |
|----------|-----------|----------------|-------|
| **P0** | `cobolbridge-deploy/index.html` | `https://cobolbridge.ai/` | Homepage |
| **P0** | `cobolbridge-deploy/index/index.html` | `https://cobolbridge.ai/index` | Index page |
| **P2** | `cobolbridge-deploy/connect/index.html` | `https://cobolbridge.ai/connect` | Connect |
| **P2** | `cobolbridge-deploy/demo/index.html` | `https://cobolbridge.ai/demo` | Demo |
| **P2** | `cobolbridge-deploy/enterprise/index.html` | `https://cobolbridge.ai/enterprise` | Enterprise |

---

### Hives (Specialised Deployments)
Each hive is a separate Vercel project. Deploy independently — no dependency order.

| Priority | Hive | Vercel Project | Source Dir | Destination |
|----------|------|----------------|------------|-------------|
| **P1** | grabhire | `grabhire-deploy` | `~/clawd/grabhire-deploy/` | `grabhire.ai` |
| **P1** | koikeeper | `koikeeper-deploy` | `~/clawd/koikeeper-deploy/` | `koikeeper.ai` |
| **P1** | planthire | `planthire-deploy` | `~/clawd/planthire-deploy/` | `planthire.ai` |
| **P1** | fishkeeper | `fishkeeper-deploy` | `~/clawd/fishkeeper-deploy/` | `fishkeeper.ai` |
| **P1** | muckaway | `muckaway-deploy` | `~/clawd/muckaway-deploy/` | `muckaway.ai` |
| **P2** | optimobile | `optimobile-deploy` | `~/clawd/optimobile-deploy/` | `optimobile.ai` |
| **P2** | landlaw | `landlaw-deploy` | `~/clawd/landlaw-deploy/` | `landlaw.ai` |
| **P2** | commercialvehicle | `commercialvehicle-deploy` | `~/clawd/commercialvehicle-deploy/` | `commercialvehicle.ai` |
| **P2** | care-compliance | `care-compliance-deploy` | `~/clawd/care-compliance-deploy/` | `care-compliance.ai` |
| **P2** | healthtech-ai | `healthtech-ai-deploy` | `~/clawd/healthtech-ai-deploy/` | `healthtech.ai` |

---

## Deploy Order (when STOP_DEPLOY clears)

```
1. meok.ai        (P0 first, then P1, then P2)     — primary domain, highest traffic
2. proofof.ai     (P0 → P1 → P2)                   — MCP suite, payment gate
3. csoai.org      (P0 → P1 → P2)                   — council ecosystem
4. cobolbridge.ai (P0 → P2)                         — standalone
5. Hives          (any order)                       — independent deployments
```

---

## Pre-Deploy Checklist

### Stripe Buy Button Verification
- [ ] `meok.ai/public/pricing/index.html` — verify ≥3 Stripe buy buttons present
- [ ] `meok.ai/public/pricing/pro.html` — verify ≥1 Stripe buy button
- [ ] `meok.ai/public/pricing/enterprise.html` — verify ≥1 Stripe buy button
- [ ] `csoai-org/pricing/index.html` — verify ≥1 Stripe buy button
- [ ] `proofof-ai/index.html` — verify Stripe buy/pro button
- [ ] Confirm all Stripe publishable keys point to **live** (not test) mode
- [ ] Confirm price IDs (price_xxx) match current Stripe dashboard

### Environment Variables Check
- [ ] `vercel env ls --scope meok` — confirm `STRIPE_SECRET_KEY` present
- [ ] `vercel env ls --scope meok` — confirm `NEXT_PUBLIC_STRIPE_KEY` present
- [ ] `vercel env ls --scope meok` — confirm `CONTACT_FORM_KEY` present
- [ ] All Vercel projects linked: `vercel ls` confirms each project exists

### Placeholder Text Audit
- [ ] `grep -r "TODO\|FIXME\|Lorem ipsum\|placeholder\|TBD\|coming soon" ~/clawd/meok.ai/public/` — zero hits
- [ ] `grep -r "TODO\|FIXME\|Lorem ipsum\|placeholder\|TBD\|coming soon" ~/clawd/proofof-ai/` — zero hits
- [ ] `grep -r "TODO\|FIXME\|Lorem ipsum\|placeholder\|TBD\|coming soon" ~/clawd/csoai-org/` — zero hits
- [ ] `grep -r "TODO\|FIXME\|Lorem ipsum\|placeholder\|TBD\|coming soon" ~/clawd/cobolbridge-deploy/` — zero hits

### Content Checks
- [ ] `~/clawd/meok.ai/public/article-50/marking.html` — FAQPage schema + Product schema both present
- [ ] `~/clawd/_intake/` — intake docs present (FAQPAGE_SCHEMAS, DEPLOY_MANIFEST)
- [ ] All HTML files valid (no unclosed tags, no broken JSON-LD)
- [ ] Sitemap `~/clawd/meok.ai/sitemap-visual.html` — lists all pages

---

## Post-Deploy Checklist

### URL Health Check (curl each for 200)
- [ ] `curl -sI https://meok.ai/` → 200
- [ ] `curl -sI https://meok.ai/article-50/marking` → 200
- [ ] `curl -sI https://meok.ai/article-50/` → 200
- [ ] `curl -sI https://meok.ai/pricing` → 200
- [ ] `curl -sI https://meok.ai/fleet` → 200
- [ ] `curl -sI https://meok.ai/assets/cross-domain-nav` → 200
- [ ] `curl -sI https://proofof.ai/` → 200
- [ ] `curl -sI https://csoai.org/` → 200
- [ ] `curl -sI https://csoai.org/pricing` → 200
- [ ] `curl -sI https://cobolbridge.ai/` → 200

### SSL Verification
- [ ] `curl -sv https://meok.ai/ 2>&1 | grep "SSL certificate verify ok"` — SSL valid
- [ ] `curl -sv https://proofof.ai/ 2>&1 | grep "SSL certificate verify ok"` — SSL valid
- [ ] `curl -sv https://csoai.org/ 2>&1 | grep "SSL certificate verify ok"` — SSL valid
- [ ] `curl -sv https://cobolbridge.ai/ 2>&1 | grep "SSL certificate verify ok"` — SSL valid
- [ ] No mixed content warnings (HTTPS all resources)
- [ ] HSTS headers present on each domain

### Sitemap & Indexing
- [ ] Confirm `https://meok.ai/sitemap-visual.html` renders
- [ ] Google Search Console — submit updated sitemap
- [ ] IndexNow — push `indexnow_batch.json` to Bing/Yandex/Seznam
- [ ] `curl -s https://meok.ai/llms.txt` — verify accessible
- [ ] `curl -s https://proofof.ai/llms.txt` — verify accessible
- [ ] `curl -s https://csoai.org/llms.txt` — verify accessible

### Schema Validation
- [ ] Google Rich Results Test — `meok.ai/article-50/marking` shows both Product + FAQPage schemas
- [ ] JSON-LD validator — all `@type` references resolve
- [ ] No duplicate `@id` values across domains

---

## Rollback Plan

| Issue | Rollback Command |
|-------|-----------------|
| Bad deploy on meok.ai | `cd ~/clawd/meok.ai && vercel rollback --scope meok` |
| Bad deploy on proofof.ai | `cd ~/clawd/proofof-ai && vercel rollback --scope meok` |
| Bad deploy on csoai.org | `cd ~/clawd/csoai-org && vercel rollback --scope meok` |
| Bad deploy on cobolbridge.ai | `cd ~/clawd/cobolbridge-deploy && vercel rollback --scope meok` |
| Hive issue | `cd ~/clawd/{hive-dir} && vercel rollback --scope meok` |
| Domain DNS | `vercel domains inspect {domain} --scope meok` to verify DNS propagation |

---

## Quick Deploy Commands (when gate clears)

```bash
# meok.ai
cd ~/clawd/meok.ai && vercel --prod --scope meok

# proofof.ai
cd ~/clawd/proofof-ai && vercel --prod --scope meok

# csoai.org
cd ~/clawd/csoai-org && vercel --prod --scope meok

# cobolbridge.ai
cd ~/clawd/cobolbridge-deploy && vercel --prod --scope meok

# Hives (examples)
cd ~/clawd/grabhire-deploy && vercel --prod --scope meok
cd ~/clawd/koikeeper-deploy && vercel --prod --scope meok
```

---

*Prepared: 17 Jun 2026. STOP_DEPLOY active — staged locally only.*
