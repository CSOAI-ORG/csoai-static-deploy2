# M16: 4-SURFACE AUDIT — 17 June 2026

**Scanned:** meok.ai · csoai.org · openmoe.ai · openpatent.ai
**Method:** HTTP GET, content extraction, sitemap/robots check, JSON-LD inspection
**Date:** 17 June 2026

---

## 1. meok.ai (→ www.meok.ai)

| Check | Status | Notes |
|-------|--------|-------|
| **HTTP** | ✅ 307 → www 200 | Redirects `meok.ai` → `https://www.meok.ai` |
| **Title** | ✅ | "MEOK AI Labs — Sovereign AI Compliance Infrastructure" |
| **JSON-LD** | ✅ 3 schemas | Organization, SoftwareApplication (with pricing), Person |
| **Sitemap** | ✅ 200 | Serves `/sitemap.xml` |
| **Robots** | ✅ 200 | Allows `/`, disallows `/api/`, `/admin/`, `/checkout/` |
| **Stripe links** | ❌ None found | No `checkout` / `stripe` / `buy` / `subscribe` URLs on homepage |
| **Article 50 kit links** | ❌ None found | Homepage has no direct link to `/article-50/` or `/eu-code-of-practice` |

### Grades

| Criterion | Grade | Notes |
|-----------|-------|-------|
| Content Depth | **B** | Good topic coverage but homepage is product-focused, not educational |
| Pricing Visibility | **C** | Pricing mentioned in JSON-LD SoftwareApplication offers but no visible pricing page link above the fold |
| AEO Readiness | **B** | 3 JSON-LD schemas (Organization, SoftwareApplication, Person) — strong but missing FAQPage |
| Cross-linking | **D** | No links to Article 50 hub or eu-code-of-practice from homepage |

---

## 2. csoai.org

| Check | Status | Notes |
|-------|--------|-------|
| **HTTP** | ✅ 200 | Direct, no redirect |
| **Title** | ✅ | "CSOAI - Council Safety of AI | AI Safety Governance Platform" |
| **JSON-LD** | ⚠️ 1 schema | Has JSON-LD but count unclear (fetch showed 1 |
| **Sitemap** | ✅ 200 | Serves `/sitemap.xml` |
| **Robots** | ⚠️ Custom | Returns full HTML page, not a robots.txt file |
| **Stripe links** | ❌ None found | No checkout/stripe/buy links on homepage |
| **Article 50 kit links** | ❌ None found | No article-50 or eu-code-of-practice references |

### Grades

| Criterion | Grade | Notes |
|-----------|-------|-------|
| Content Depth | **B** | AI safety governance platform, TC260 equivalent positioning |
| Pricing Visibility | **D** | No pricing visible at all on homepage |
| AEO Readiness | **C** | Has JSON-LD but limited schemas |
| Cross-linking | **D** | No links to meok.ai, proofof.ai, or any Article 50 content |

---

## 3. openmoe.ai

| Check | Status | Notes |
|-------|--------|-------|
| **HTTP** | ✅ 200 | Direct, serves content |
| **Title** | ✅ | "openmoe — Byzantine-fault-tolerant consensus for MoE routing." |
| **JSON-LD** | ❌ 0 | No JSON-LD schemas found |
| **Sitemap** | ✅ 200 | Serves `/sitemap.xml` |
| **Robots** | ✅ 200 | `Allow: /` + Sitemap directive |
| **Stripe links** | ❌ None found | No checkout/purchase paths on homepage |
| **Article 50 kit links** | ❌ None found | No Article 50 / EU AI Act compliance content |

### Grades

| Criterion | Grade | Notes |
|-----------|-------|-------|
| Content Depth | **C** | Single-page site, BFT/MoE focused, limited depth |
| Pricing Visibility | **F** | No pricing information at all |
| AEO Readiness | **F** | Zero JSON-LD schemas |
| Cross-linking | **F** | Standalone domain, no links to sibling domains |

---

## 4. openpatent.ai

| Check | Status | Notes |
|-------|--------|-------|
| **HTTP** | ✅ 200 | Next.js app, serves homepage |
| **Title** | ✅ | "OpenPatent.ai — Disclose First. AI Second." |
| **JSON-LD** | ❌ 0 | No JSON-LD schemas found (Next.js app, rich but no s✓ |
| **Sitemap** | ✅ 200 | Serves `/sitemap.xml` |
| **Robots** | ✅ 200 | `Allow: /` + Sitemap directive |
| **Stripe links** | ⚠️ Checkout URLs | Links to `https://api.openpatent.ai/v1/checkout/*` — not native Stripe but checkout flow |
| **Article 50 kit links** | ❌ None | No Article 50 references |

### Grades

| Criterion | Grade | Notes |
|-----------|-------|-------|
| Content Depth | **B** | Good product page with clear value prop, industries, pricing tiers |
| Pricing Visibility | **A** | 5 clear pricing tiers ($0-$2,499), CTA buttons, featured card |
| AEO Readiness | **F** | Zero JSON-LD schemas, despite being an ideal candidate for FAQPage |
| Cross-linking | **D** | Links to CSOAI in footer, but not to meok.ai or other siblings |

---

## Overall Scores

| Domain | Content | Pricing | AEO | Cross-link | Overall |
|--------|---------|---------|-----|------------|---------|
| meok.ai | B | C | B | D | **C+** |
| csoai.org | B | D | C | D | **C** |
| openmoe.ai | C | F | F | F | **D** |
| openpatent.ai | B | A | F | D | **C** |

## Gap List (Action Items)

1. **meok.ai homepage**: Add links to /article-50/ and /eu-code-of-practice in hero/footer
2. **meok.ai**: Add FAQPage JSON-LD schema to homepage
3. **meok.ai**: Add stripe/checkout links visible on homepage
4. **csoai.org**: Fix robots.txt (currently returns HTML instead of plain-text directives)
5. **csoai.org**: Cross-link to meok.ai's Article 50 pages from relevant content
6. **openmoe.ai**: Add JSON-LD schemas (Organization + FAQPage minimum)
7. **openmoe.ai**: Cross-link to openpatent.ai and csoai.org
8. **openpatent.ai**: Add JSON-LD schemas (FAQPage, Product, Organization)
9. **openpatent.ai**: Cross-link to meok.ai, csoai.org from footer
10. **All domains**: Deploy FAQPage schema on every content page
11. **openmoe.ai**: Add pricing visibility if it's a commercial product
12. **All domains**: Cross-link to sibling domains in a unified footer
