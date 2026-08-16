# V2 — Charter Art 32–49: RESOLVED (reserved-intentional, not never-written)

**Date:** 2026-08-12 · **Status:** CLOSED

## The question (register V2)
Charter Art 32–49 — reserved-intentional vs never-written?

## Evidence found
1. `evidence/harness/freeze/latest/charter-article-count.json` (frozen 2026-08-04):
   "Charter articles" canonical_value = **52**, method = len() of the articles
   array in `csoai_charter_52_articles.json`, status VERIFIED, matches_candidate.
2. `SOVOS/GSPC_NUMBERS_REGISTRY.json` (2026-08-12): "charter articles value=34,
   detail: 34 substantive + 18 reserved slots (Art 32-49 placeholders); '52' is
   KILLED as public substance."
3. The source file `csoai_charter_52_articles.json` is NOT in the repo today
   (crosswalk's `CHARTER` path would 500 on load) — it lives at the Mac home
   path per the freeze (`~/clawd/csoai_charter_52_articles.json`).

## Resolution
- **52 = slot count** (verified len() of the articles array, 2026-08-04) — internal.
- **34 = substantive articles**; **18 = reserved slots (Art 32–49)** — intentional
  placeholders, never written as substance. This answers the register's
  "reserved-intentional vs never-written": **reserved-intentional.**
- **Public claims must say 34** (substantive). "52" is the internal slot count;
  claiming 52 as public substance is the killed overclaim (the same class as the
  "care 200-vs-201" and "12-axis-vs-13" conflations).

## Action items
1. Fix `charter_crosswalk.py` CHARTER path (points at a missing file → 500) or
  restore `csoai_charter_52_articles.json` to repo root. Lane-executable.
2. The numbers registry stays canonical: **34 substantive** for public copy.