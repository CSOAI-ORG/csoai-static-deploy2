# M49: Full Cross-Link Audit — 17 June 2026

**Scope:** All 4 major surfaces + 30 hives + comparison pages + Article 50 pages
**Sources:** `_intake/CROSS_LINK_MESH_17JUN.md`, `_intake/4_SURFACE_AUDIT_17JUN.md`, `_intake/30_HIVE_CROSS_LINK_PLAN_17JUN.md`, live files at `~/clawd/meok.ai/public/`
**Status:** ✅ **Complete** after Sprint 4 cross-link fixes

---

## 1. Article 50 Pages (6 pages)

### Pre-fix Status (from M19 audit)
| From ↓ \ To → | Hub | Transparency | Marking | Deepfake | Bot | CoP |
|:-------------:|:---:|:------------:|:-------:|:--------:|:---:|:---:|
| **Hub** | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Transparency** | ✅ | — | ✅ | ✅ | ❌ | ❌ |
| **Marking** | ✅ | ✅ | — | ✅ | ❌ | ❌ |
| **Deepfake** | ✅ | ✅ | ✅ | — | ❌ | ❌ |
| **Bot** | ✅ | ✅ | ✅ | ❌ | — | ❌ |
| **CoP** | ✅ | ✅ | ✅ | ❌ | ❌ | — |

**Missing: 10 cross-links** (bot and CoP missing from 5 sub-pages)

### Post-fix Status (Sprint 4 — M46-FIX applied)
| From ↓ \ To → | Hub | Transparency | Marking | Deepfake | Bot | CoP |
|:-------------:|:---:|:------------:|:-------:|:--------:|:---:|:---:|
| **Hub** | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Transparency** | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| **Marking** | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| **Deepfake** | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| **Bot** | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| **CoP** | ✅ | ✅ | ✅ | ✅ | ✅ | — |

**✅ All 30 possible cross-links present. 0 dead links in Article 50 section.**

---

## 2. Four Major Surfaces

| Domain | Cross-link to Article 50? | Cross-link to siblings? | Dead Links |
|--------|:-------------------------:|:-----------------------:|:----------:|
| **meok.ai** | ❌ No direct links to `/article-50/` or `/eu-code-of-practice` from homepage | Has `/pricing/`, `/sectors/`, `/comparisons/` but no `/article-50/` | None found — all internal paths 200 |
| **csoai.org** | ❌ No Article 50 references | No links to meok.ai, proofof.ai (footer only has CSOAI links) | robots.txt returns HTML instead of plain-text — not a dead link, but broken |
| **openmoe.ai** | ❌ None | Standalone domain, no sibling links | None — single-page site |
| **openpatent.ai** | ❌ None | Links to CSOAI in footer but not meok.ai or proofof.ai | None — Next.js app, all routes resolve |

### Dead Links Found: 0
All sites serve 200 status on their internal navigation paths. No 404s detected in header/footer nav.

### Cross-link Gaps (not dead links, but missing connections):
1. **meok.ai homepage**: Should link to `/article-50/` and `/eu-code-of-practice`
2. **meok.ai homepage**: No direct Stripe/checkout links visible
3. **csoai.org**: robots.txt returns HTML instead of plain-text (broken format, not a dead link)
4. **csoai.org**: No cross-links to meok.ai, proofof.ai, or Article 50 content
5. **openmoe.ai**: Standalone — no JSON-LD, no sibling links
6. **openpatent.ai**: Missing JSON-LD schemas on a rich product page

---

## 3. Comparison Pages (8 pages)

| Comparison Page | Cross-links to other comparisons? | Cross-links to Article 50? | Dead Links |
|----------------|:--------------------------------:|:--------------------------:|:----------:|
| vanta.html | ✅ Via comparison nav | ❌ None | None |
| secureframe.html | ✅ Via comparison nav | ❌ None | None |
| one-trust.html | ✅ Via comparison nav | ❌ None | None |
| hyperproof.html | ✅ Via comparison nav | ❌ None | None |
| drata.html | ✅ Via comparison nav | ❌ None | None |
| auditboard.html | ✅ Via comparison nav | ❌ None | None |
| trustarc-vs.html | ✅ Via comparison nav | ❌ None | None |
| onetrust-vs.html | ✅ Via comparison nav | ❌ None | None |
| ibm-vs.html | ✅ Via comparison nav | ❌ None | None |
| google-vs.html | ✅ Via comparison nav | ❌ None | None |
| bigid-vs.html | ✅ Via comparison nav | ❌ None | None |
| azure-vs.html | ✅ Via comparison nav | ❌ None | None |
| aws-vs.html | ✅ Via comparison nav | ❌ None | None |

All comparison pages link to each other via the comparison navigation section. **0 dead links.**

---

## 4. 30-Hive Cross-Link Status (from M29 plan)

### Cluster A: Compliance & Governance (Core)
| Hive | Domain | Links to meok.ai? | Links to csoai.org? | Links to proofof? | Dead Links |
|------|--------|:-----------------:|:-------------------:|:-----------------:|:----------:|
| meok | meok.ai | — | ✅ (footer) | ✅ (footer) | None |
| csoai | csoai.org | ❌ | — | ❌ | robots.txt broken |
| proofof | proofof.ai | ✅ | ✅ | — | None |
| accountabilityof | accountabilityof.ai | ❌ | ❌ | ❌ | ❌ Domain unreachable (no A record?) |
| dataprivacyof | dataprivacyof.ai | ❌ | ❌ | ❌ | ❌ Domain unreachable |
| ethicalgovernanceof | ethicalgovernanceof.ai | ❌ | ❌ | ❌ | ❌ Domain unreachable |
| transparencyof | transparencyof.ai | ❌ | ❌ | ❌ | ❌ Domain unreachable |
| safetyof | safetyof.ai | ❌ | ❌ | ❌ | ❌ Domain unreachable |
| biasdetectionof | biasdetectionof.ai | ❌ | ❌ | ❌ | ❌ Domain unreachable |

### Cluster B: Security & Safety
| Hive | Domain | Links to meok? | Links to csoai? | Dead Links |
|------|--------|:--------------:|:---------------:|:----------:|
| agisafe | agisafe.ai | ❌ | ❌ | ❌ Domain unreachable |
| asisecurity | asisecurity.ai | ❌ | ❌ | ❌ Domain unreachable |

### Cluster C: Vertical Industry Hives
| Hive | Domain | Links to meok? | Links to csoai? | Dead Links |
|------|--------|:--------------:|:---------------:|:----------:|
| commercialvehicle | commercialvehicle.ai | ❌ | ❌ | ❌ Domain unreachable |
| grabhire | grabhire.ai | ✅ (footer) | ❌ | None |
| muckaway | muckaway.ai | ❌ | ❌ | ❌ Domain unreachable |
| planthire | planthire.ai | ❌ | ❌ | ❌ Domain unreachable |
| landlaw | landlaw.ai | ❌ | ❌ | ❌ Domain unreachable |
| cobolbridge | cobolbridge.ai | ❌ | ❌ | ❌ Domain unreachable |
| openpatent | openpatent.ai | ❌ | ✅ (footer) | None |

### Cluster D: Data, Knowledge & Consumer
| Hive | Domain | Links to meok? | Links to csoai? | Dead Links |
|------|--------|:--------------:|:---------------:|:----------:|
| diyhelp | diyhelp.ai | ❌ | ❌ | ❌ Domain unreachable |
| fishkeeper | fishkeeper.ai | ❌ | ❌ | ❌ Domain unreachable |
| koikeeper | koikeeper.ai | ❌ | ❌ | ❌ Domain unreachable |
| pokerhud | pokerhud.ai | ❌ | ❌ | ❌ Domain unreachable |
| optimobile | optimobile.ai | ❌ | ❌ | ❌ Domain unreachable |
| openmoe | openmoe.ai | ❌ | ❌ | None (standalone) |

### Cluster E: Platform & Infrastructure
| Hive | Domain | Links to meok? | Links to csoai? | Dead Links |
|------|--------|:--------------:|:---------------:|:----------:|
| loopfactory | loopfactory.ai | ❌ | ❌ | ❌ Domain unreachable |
| meok-compliance-gateway | (internal) | ❌ | ❌ | Internal only |
| openmcp | (openMCP) | ❌ | ❌ | Internal only |
| councilof | councilof.ai | ❌ | ❌ | ❌ Domain unreachable |

### Cluster F: Social & Community
| Hive | Domain | Links to meok? | Links to csoai? | Dead Links |
|------|--------|:--------------:|:---------------:|:----------:|
| socialmediamanager | socialmediamanager.ai | ❌ | ❌ | ❌ Domain unreachable |
| suicidestop | suicidestop.ai | ❌ | ❌ | ❌ Domain unreachable |

### Cluster G: Labs & Internal
| Hive | Domain | Links to meok? | Links to csoai? | Dead Links |
|------|--------|:--------------:|:---------------:|:----------:|
| sovereign-town | (lab) | ❌ | ❌ | Internal only |
| sandbox | (internal) | ❌ | ❌ | Internal only |

---

## Dead Links Summary

### Category 1: Broken/Dangling Links — 0 found
All links within the meok.ai public site (`/article-50/*`, `/comparisons/*`, `/pricing/*`, `/sectors/*`) resolve to 200. No 404s.

### Category 2: Unreachable External Domains — 21 hives
These `.ai` domains did not resolve during the audit (likely not yet deployed/pointed):

1. accountabilityof.ai
2. agisafe.ai
3. asisecurity.ai
4. biasdetectionof.ai
5. cobolbridge.ai
6. commercialvehicle.ai
7. councilof.ai
8. dataprivacyof.ai
9. ethicalgovernanceof.ai
10. fishkeeper.ai
11. koikeeper.ai
12. landlaw.ai
13. loopfactory.ai
14. muckaway.ai
15. planthire.ai
16. pokerhud.ai
17. optimobile.ai
18. safetyof.ai
19. socialmediamanager.ai
20. suicidestop.ai
21. transparencyof.ai

**These are NOT dead links in the traditional sense** — they are domains registered but not yet live. The audit flags them as cross-link opportunities for when they go live.

### Category 3: Missing Internal Cross-Links (gaps, not dead)
1. meok.ai homepage → missing `/article-50/` link
2. meok.ai homepage → missing `/eu-code-of-practice` link
3. meok.ai → missing FAQPage JSON-LD
4. csoai.org → broken robots.txt (returns HTML)
5. csoai.org → missing cross-links to meok.ai, proofof.ai
6. openmoe.ai → zero JSON-LD, zero sibling links
7. openpatent.ai → zero JSON-LD schemas
8. Article 50 pages → **ALL 10 MISSING LINKS NOW FIXED (Sprint 4)**

---

## Overall Link Graph Health

| Metric | Value |
|--------|:-----:|
| Total pages audited | ~56 (6 Article 50 + 4 surfaces + 13 comparisons + 32 hives + 1 ecosystem map) |
| Dead links (404) | **0** |
| Missing cross-links (Article 50) | **0** ✅ (10 fixed in Sprint 4) |
| Missing cross-links (4 surfaces) | **6 gaps** identified |
| Missing cross-links (30 hives) | **21 domains not yet live** — expected |
| Unreachable external domains | **21** — registered but not deployed |
| Total cross-links verified present | **30/30 in Article 50 section** |

---

## Recommendations

1. **Sprint 4 immediate:** ✅ Article 50 cross-links fixed (10 links patched across 5 files)
2. **Sprint 4 medium:** Add `/article-50/` and `/eu-code-of-practice` links to meok.ai homepage hero/footer
3. **Sprint 4 medium:** Fix csoai.org robots.txt
4. **Deferred (domain deployment):** Add MEOK compliance footer to all 21 hives when their domains go live
5. **Future sprint:** Implement unified cross-link footer across all 4 major surfaces
6. **Future sprint:** Add JSON-LD schemas to openmoe.ai and openpatent.ai

---

*Audit completed: 17 June 2026 · Sprint 4 cross-link verification · Owner: MEOK AI Labs / CSOAI Ltd*
