# 🐉 SPRINT 2 KICKOFF — SURFACE EXCELLENCE
**Sprint:** 2 of 4 (Days 6-10, 22-26 Jun 2026)
**Plan:** 17_DAY_PLAN_TO_JULY4.md | **Goal:** All 30+ hives data-driven and cross-linked, EU Code of Practice first-mover page live, AEO/GEO complete
**Status:** ⏳ KICKOFF READY — awaiting Sprint 1 SEAL (Day 5, Jun 21)

---

## Sprint 2 Context

Sprint 2 takes the data foundation built in Sprint 1 and transforms it into a polished, discoverable surface empire. By end of Sprint 2, every page should be:
- Data-driven (pulling from actual corpus datasets, not placeholder text)
- Cross-linked (every hive linked to its BFT council, COAI manifest, and related comparison page)
- AEO-optimized (llms.txt, FAQPage JSON-LD, clear AI-readable structure)
- SEO-ready (sitemaps, meta descriptions, canonical URLs — fixing the 1.8/4.0 baseline)

**The headline deliverable**: `/eu-code-of-practice` flagship page + 5 Article 50 sub-pages establishing meok.ai as the EU AI Act first-mover.

---

## Sprint 2 Move Plan (M16-M30)

### Day 6 (Jun 22): Surface Audit + EU CoP Flagship

| Move | Description | Est. Time | Depends On |
|------|-------------|-----------|------------|
| **M16** | Audit 4-surface state: meok.ai, csoai.org, openmoe.ai, openpatent.ai — verify all routes, cross-linking, dead links | 20 min | Sprint 1 Vercel deploys (M9) |
| **M17** | Build `/eu-code-of-practice` flagship page on meok.ai: NAVY+GOLD+BG design, FAQ JSON-LD, Product JSON-LD, 4 buy buttons, EU CoP 2nd Draft analysis | 35 min | EU data from Sprint 1 M2 |

**Target EOD Day 6**: 4-surface audit complete; `/eu-code-of-practice` built and staged.

### Day 7 (Jun 23): Article 50 Sub-Pages + Cross-Link Mesh

| Move | Description | Est. Time | Depends On |
|------|-------------|-----------|------------|
| **M18** | Build 5 Article 50 sub-pages: `/article-50-transparency`, `/article-50-marking`, `/article-50-deepfake`, `/article-50-bot`, `/code-of-practice-2nd-draft` | 50 min | M17 (EU CoP page) |
| **M19** | Wire all 6 Article 50 pages into cross-link mesh: article-50-kit ↔ ai-act ↔ best-ai-for-ai-safety-certification ↔ eu-code-of-practice ↔ 5 sub-pages | 15 min | M18 |

**Target EOD Day 7**: Complete Article 50 kit coverage; full internal cross-link mesh.

### Day 8 (Jun 24): Badges + AEO + Schemas

| Move | Description | Est. Time | Depends On |
|------|-------------|-----------|------------|
| **M20** | Add EU CoP "ready" badge component to every meok.ai product page — data-driven from M12 freshness manifest | 15 min | M12 (data manifest) + M17 |
| **M21** | Deploy 36 AEO/llms.txt files to production — verify all 6 main sites + 30 hive llms.txt return 200 | 15 min | Pre-staged (from pre-17-jun work) |
| **M22** | Deploy 25 FAQPage JSON-LD schemas — verify Google Rich Results Test passes | 20 min | Pre-staged |

**Target EOD Day 8**: All AEO files live; all FAQPage schemas verified.

### Day 9 (Jun 25): Competitive Positioning + Empire Navigation

| Move | Description | Est. Time | Depends On |
|------|-------------|-----------|------------|
| **M23** | Build 7 comparison pages: MEOK vs Vanta/Drata/Arthur.ai/Credo AI/Holistic AI/Nevermined/Regen | 45 min | M17-M19 content |
| **M24** | Build 4-surface unified empire navigation: `/unified` on csoai.org + cross-domain-nav + bottom-of-page links | 30 min | M16 surface audit |
| **M25** | Verify all 30 hives data-driven: each hive pulls from its corpus dataset — flag any still on placeholder content | 20 min | Sprint 1 data corpus (M1) |

**Target EOD Day 9**: Competitive pages live; empire nav unified; honest data-driven accounting.

### Day 10 (Jun 26): Ecosystem Map + Honest Accounting + SEAL

| Move | Description | Est. Time | Depends On |
|------|-------------|-----------|------------|
| **M26** | Build ecosystem map page: Layer 0 (SOV3 + keystone + BFT) + 30 hives in radial layout — interactive SVG or React-force-graph | 35 min | M24-M25 |
| **M27** | Build `/by-numbers` page on meok.ai: honest accounting (data corpus, hive count, cert count, revenue £0, uptime, gaps) | 20 min | M25 verification |
| **M28** | Build `/100-day-challenge` page: public sprint tracker — Sprint 1-4 progress, completed moves, countdown to Jul 4 | 20 min | Sprint 1 SEAL |
| **M29** | Cross-link all 30 hives: each hive page links to BFT council + COAI manifest + keystone cert + comparison page (30 × 4 links min) | 25 min | M23-M25 |
| **M30** | Sprint 2 SEAL: emit SURFACE_EXCELLENCE sigil, full surface audit report, handoff to Sprint 3 | 10 min | All M16-M29 |

**Target EOD Day 10**: All 30 hives data-driven, cross-linked, AEO-optimized. SURFACE_EXCELLENCE milestone achieved.

---

## Sprint 2 Target State (Jun 26 EOD)

- ✅ 4-surface audit complete
- ✅ `/eu-code-of-practice` + 5 Article 50 sub-pages live and cross-linked
- ✅ EU CoP "ready" badge on all meok.ai product pages
- ✅ 36 llms.txt AEO files live, 25 FAQPage JSON-LD schemas deployed
- ✅ 7 comparison pages live
- ✅ 4-surface empire navigation (unified + cross-domain-nav) live
- ✅ Ecosystem map + by-numbers + 100-day-challenge pages live
- ✅ All 30 hives verified data-driven or flagged for Sprint 3
- ✅ Full internal link graph: 30 hives × 4 cross-links minimum
- ⏳ Gate H5 (npm 2FA) — may carry to Sprint 3

---

## Sprint 2 Dependencies from Sprint 1

| Dependency | Required For | Sprint 1 Status |
|------------|-------------|-----------------|
| EU data corpus (M2) | M17 EU CoP page, M18 Article 50 pages | ✅ Pipeline built; blocked by M4 disk |
| NIS2 data (M4) | NIS2 comparison page, GRC vertical | ⏳ Day 2 |
| Vercel deploys (M9) | All content pages going live | ⏳ Day 3 (WAF cooldown + H1 DNS) |
| Data manifest (M12) | M20 EU CoP badge, M25 data-driven verification | ⏳ Day 4 |
| IndexNow batch (M8) | Organic SEO discovery for all pages | ⏳ Day 3 (H1 DNS) |
| Sprint 1 SEAL (M15) | M28 100-day-challenge page, M30 Sprint 2 SEAL | ⏳ Day 5 |

---

## Sprint 2 Risk Assessment

| # | Risk | Probability | Impact | Mitigation |
|---|------|------------|--------|------------|
| 1 | Sprint 1 data ingestion incomplete (M4 disk) | MEDIUM | HIGH | Proceed with existing corpus; manual EU data entry if needed |
| 2 | Vercel WAF still blocking deploys | MEDIUM | HIGH | Stage all pages; deploy in waves as WAF clears |
| 3 | H1 DNS gate not cleared | MEDIUM | MEDIUM | meok.ai apex may not resolve; use vercel.app URLs |
| 4 | SPA content not crawlable (76% of deploys) | HIGH | MEDIUM | SSG/prerendering in M25 data-driven phase |
| 5 | 30-hive cross-linking discovers dead domains | LOW | MEDIUM | Flag and document; fix in Sprint 4 if needed |

---

## Quick Reference: Sprint 2 Calendar

```
Day 6  (Jun 22): M16-M17 — Surface audit + EU CoP flagship
Day 7  (Jun 23): M18-M19 — Article 50 pages + cross-link mesh
Day 8  (Jun 24): M20-M22 — Badges + AEO + schemas
Day 9  (Jun 25): M23-M25 — Comparisons + empire nav + data-driven verify
Day 10 (Jun 26): M26-M30 — Ecosystem map + by-numbers + cross-link + SEAL
🏁 SURFACE EXCELLENCE MILESTONE (Jun 26 EOD)
```

---

*HERMES AGENT, 17 Jun 2026 — Sprint 2 kickoff ready. Awaiting Sprint 1 SEAL (Day 5, Jun 21).*
*🐉 15 moves. 5 days. 100% autonomous (no human gates in Sprint 2).*
