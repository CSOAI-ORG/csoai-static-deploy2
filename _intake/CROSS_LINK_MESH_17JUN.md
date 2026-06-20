# M19: CROSS-LINK MESH — Article 50 Pages
**Date:** 17 June 2026
**Scope:** All 6 Article 50 pages under `/article-50/` on meok.ai

---

## The 6 Pages

| # | Page | Path | Type |
|---|------|------|------|
| 1 | Article 50 Compliance Suite Hub | `/article-50/index.html` | Hub/Overview |
| 2 | Transparency Requirements | `/article-50/transparency.html` | Deep-dive Guide |
| 3 | Technical Marking Specification | `/article-50/marking.html` | Deep-dive Guide |
| 4 | Deepfake Detection & Disclosure | `/article-50/deepfake.html` | Deep-dive Guide |
| 5 | Bot Interaction Disclosure | `/article-50/bot.html` | Deep-dive Guide |
| 6 | Code of Practice 2nd Draft | `/article-50/code-of-practice.html` | Deep-dive Guide |

---

## Cross-Link Audit

Legend: ✅ = links to this page  ❌ = does NOT link to this page

### Page 1: Article 50 Hub → all others

| → transparency | → marking | → deepfake | → bot | → code-of-practice |
|:--------------:|:---------:|:----------:|:-----:|:------------------:|
| ✅ (guide cards + footer) | ✅ (guide cards + footer) | ✅ (guide cards + footer) | ✅ (guide cards + footer) | ✅ (guide cards + footer) |

### Page 2: Transparency → all others

| → hub | → marking | → deepfake | → bot | → code-of-practice |
|:-----:|:---------:|:----------:|:-----:|:------------------:|
| ✅ (footer) | ✅ (footer) | ✅ (footer) | ❌ **MISSING** | ❌ **MISSING** |

### Page 3: Marking → all others

| → hub | → transparency | → deepfake | → bot | → code-of-practice |
|:-----:|:-------------:|:----------:|:-----:|:------------------:|
| ✅ (footer) | ✅ (footer) | ✅ (footer) | ❌ **MISSING** | ❌ **MISSING** |

### Page 4: Deepfake → all others

| → hub | → transparency | → marking | → bot | → code-of-practice |
|:-----:|:-------------:|:---------:|:-----:|:------------------:|
| ✅ (footer) | ✅ (footer) | ✅ (footer) | ❌ **MISSING** | ❌ **MISSING** |

### Page 5: Bot → all others

| → hub | → transparency | → marking | → deepfake | → code-of-practice |
|:-----:|:-------------:|:---------:|:----------:|:------------------:|
| ✅ (footer) | ✅ (footer) | ✅ (footer) | ❌ **MISSING** | ❌ **MISSING** |

### Page 6: Code of Practice → all others

| → hub | → transparency | → marking | → deepfake | → bot |
|:-----:|:-------------:|:---------:|:----------:|:-----:|
| ✅ (footer) | ✅ (footer) | ✅ (footer) | ❌ **MISSING** | ❌ **MISSING** |

---

## Summary Matrix

| From ↓ \ To → | Hub | Transparency | Marking | Deepfake | Bot | CoP |
|:-------------:|:---:|:------------:|:-------:|:--------:|:---:|:---:|
| **Hub** | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Transparency** | ✅ | — | ✅ | ✅ | ❌ | ❌ |
| **Marking** | ✅ | ✅ | — | ✅ | ❌ | ❌ |
| **Deepfake** | ✅ | ✅ | ✅ | — | ❌ | ❌ |
| **Bot** | ✅ | ✅ | ✅ | ❌ | — | ❌ |
| **CoP** | ✅ | ✅ | ✅ | ❌ | ❌ | — |

**Total possible links:** 30 (6×5)
**Present links:** 17
**Missing links:** 13

---

## Missing Links Detail

| Source Page | Missing Link To | Fix |
|-------------|-----------------|-----|
| transparency.html | bot.html | Add to footer Resources |
| transparency.html | code-of-practice.html | Add to footer Resources |
| marking.html | bot.html | Add to footer Resources |
| marking.html | code-of-practice.html | Add to footer Resources |
| deepfake.html | bot.html | Add to footer Resources |
| deepfake.html | code-of-practice.html | Add to footer Resources |
| bot.html | deepfake.html | Replace bot self-link with deepfake |
| bot.html | code-of-practice.html | Add to footer Resources |
| code-of-practice.html | deepfake.html | Add to footer Resources |
| code-of-practice.html | bot.html | Add to footer Resources |
| **All sub-pages** | (missing bot/CoP cross-links) | See rows above |

### Recommended Footer Template (Resources section, all pages):

```html
<li><a href="/article-50/">Article 50 Hub</a></li>
<li><a href="/article-50/transparency.html">Transparency Guide</a></li>
<li><a href="/article-50/marking.html">Marking Spec</a></li>
<li><a href="/article-50/deepfake.html">Deepfake Detection</a></li>
<li><a href="/article-50/bot.html">Bot Disclosure</a></li>
<li><a href="/article-50/code-of-practice.html">Code of Practice</a></li>
```

All 6 sub-pages should use **identical** footer Resources lists so every page links to every other page.
