# M22: FAQPage Schema Verification — 17 June 2026
**Scope:** All existing FAQPage JSON-LD schemas across meok.ai

---

## Summary

| # | Page | Schema Type | Q&A Count | Valid? |
|---|------|-------------|:----------:|:------:|
| 1 | `/eu-code-of-practice.html` | FAQPage | 7 | ✅ Valid |
| 2 | `/article-50/transparency.html` | FAQPage | 7 | ✅ Valid |
| 3 | `/article-50/deepfake.html` | FAQPage | 6 | ✅ Valid |
| 4 | `/article-50/bot.html` | FAQPage | 6 | ✅ Valid |
| 5 | `/article-50/code-of-practice.html` | FAQPage | 6 | ✅ Valid |
| 6 | `/article-50/marking.html` | Product (no FAQPage) | 0 | ⚠️ Missing FAQPage |
| — | **Total** | **5 FAQPage schemas** | **32 Q&A pairs** | |

---

## Per-Page Detail

### 1. `/eu-code-of-practice.html` (Root level)
- **7 Questions** covering: Code of Practice definition, who it applies to, transparency marking, MEOK Free tier, Pro attestations, Enterprise tier, deadline
- **Has both FAQPage + Product schemas** (only page with dual schemas)
- **Issues:** ✅ None

### 2. `/article-50/transparency.html`
- **7 Questions** covering: Article 50 definition, two-layer marking, responsibility split, scope, enforcement date, penalties, MEOK help
- **Issues:** None identified — well-structured `mainEntity` array

### 3. `/article-50/deepfake.html`
- **6 Questions** covering: deepfake definition, enforcement date, qualifying content, exceptions, penalties, MEOK help
- **Issues:** None identified

### 4. `/article-50/bot.html`
- **6 Questions** covering: bot disclosure definition, timing of disclosure, exceptions, voice systems, AI avatars, MEOK help
- **Issues:** None identified

### 5. `/article-50/code-of-practice.html`
- **6 Questions** covering: Code definition, 2nd draft changes, deployer impact, effective date, first-mover advantage, MEOK help
- **Issues:** None identified

### 6. `/article-50/marking.html` ⚠️
- **No FAQPage schema** — only a Product schema with pricing info
- **Missing:** Should have FAQPage with questions about C2PA, W3C, digital signatures, watermarking, etc.

---

## Structural Issues Found

### Issue 1: Missing FAQPage on marking.html
- **Page:** `/article-50/marking.html`
- **Current:** Only has `@type: Product` schema
- **Fix:** Add FAQPage with 5-6 Q&A about technical marking (C2PA, XMP, digital signatures, audio watermarking, format compliance, etc.)

### Issue 2: Inconsistent question phrasing
- **Pattern:** Several pages use "How can MEOK help..." as final Q&A
- **Finding:** This is acceptable but could be standardized to "How can MEOK help with [topic]?" across all pages for consistency
- **Current examples:**
  - "How can MEOK help with Article 50 compliance?" ✓
  - "How can MEOK help with deepfake compliance?" ✓
  - "How can MEOK help with bot disclosure compliance?" ✓
  - "How can MEOK help with Code of Practice compliance?" ✓

### Issue 3: Pages without ANY JSON-LD
- The following meok.ai pages have **no FAQPage or any schema**:
  - `/100-day-challenge.html`
  - `/by-numbers.html`
  - `/ecosystem-map.html`
  - `/manifesto.html`
  - `/partners.html`
  - `/press-kit.html`
  - All `/pricing/*.html` pages
  - All `/comparisons/*.html` pages
  - All `/sectors/*.html` pages

### Issue 4: Homepage has no FAQPage
- `meok.ai` (www) has Organization + SoftwareApplication + Person schemas
- **Missing:** FAQPage schema on the homepage

---

## Recommendations

1. **Add FAQPage to marking.html** — immediate priority for Article 50 completeness
2. **Add FAQPage to meok.ai homepage** — strong SEO signal for AI compliance queries
3. **Add FAQPage to all comparison pages** — each comparison page is ideal for FAQ structured data
4. **Standardize Q&A phrasing** across all schemas for brand consistency
5. **Consider adding FAQPage to pricing pages** — common pricing FAQs are great for rich snippets
