# E2E COPY-EDIT MANIFEST — councilof.ai + meok.ai
**Date:** 2026-08-12 · **Method:** full-estate scan — Council SPA bundle + **all 396 lazy page chunks** downloaded and grep-audited against canon (62 files flagged); MEOK pages fetched and audited. Every finding has exact strings and exact replacements.

---

## 0. EXECUTIVE SCOREBOARD

| Site | Scan coverage | P0 doctrine/naming | P1 honesty | P2 hygiene |
|---|---|---|---|---|
| councilof.ai | 396/396 chunks + main bundle + HTML shell | 6 issues | 3 issues | 3 issues |
| meok.ai | /, /os, /arena, /pricing, /privacy, /about, /manifesto, /sovereign | 3 issues (1 already FIXED live) | 2 issues | 1 issue |

**Good news first:** the meok.ai homepage SOVOS kill is **deployed and externally verified clean** (0 hits). Council's SovOS axis table, Sov3ModelCard disclaimers, SectorAct dates, and Charter content are already doctrinally *good* — listed in §4 "do not touch".

---

## 1. COUNCIL — P0 (doctrine/legal, fix this deploy)

### 1.1 The unparsed contradiction — SovOS page (SovOS.r2-DZOHqM_o.js)
Canon (ratified Part AW, PUBLIC_DOCTRINE.json): **unparsed = reported separately as UNMEASURED, never scored wrong.**
- OLD: `"Nine axes show no number on purpose. A score appears only once an axis is MEASURED, and an interval only once usable n ≥ 30. Unparsed answers are counted incorrect, never dropped."`
- NEW: `"Nine axes show no number on purpose. A score appears only once an axis is MEASURED, and an interval only once usable n ≥ 30. Unparsed answers are reported separately as UNMEASURED — never scored wrong, never dropped."`
- OLD: `"Unparsed counted incorrect","An answer we cannot read is a wrong answer, never a dropped row."`
- NEW: `"Unparsed reported as UNMEASURED","An answer we cannot read is a measurement failure, reported in its own column — never a wrong answer, never a dropped row."`
- OLD (table row): `` `${(i.unparsed_rate*100).toFixed(1)}% (counted incorrect)` `` → NEW: `` `${(i.unparsed_rate*100).toFixed(1)}% (reported UNMEASURED)` ``

### 1.2 Outdated positioning + partnership language (main bundle index.r2)
- OLD: `"CSOAI homepage - AI safety partnership platform"` → NEW: `"Council of AI — independent, signed measurement of AI systems"`
- OLD: `"CSOAI is the Council for Safe, Open AI - a partnership framework for AI safety"` → NEW: `"Council of AI (CSOAI) is an independent measurement instrument: we measure AI systems against the rules that govern them, sign the result (Ed25519), and publish what we cannot yet measure. Not a certifier, not an enforcer, no accreditation chain."`

### 1.3 Wrong legal deadline (main bundle FAQ/quiz) — the credibility hole
- OLD question: `"How should an organization approach compliance with the August 2026 high-risk AI system deadline?"`
- NEW question: `"How should an organization sequence EU AI Act compliance after the Digital Omnibus?"`
- NEW answer (replace both options): `"Transparency duties (Art. 50) are in force since 2 August 2026; pre-existing generative systems must be machine-readably marked by 2 December 2026; the Annex III high-risk regime phases in from December 2027, Annex I from August 2028. Sequence: inventory now, transparency evidence first, high-risk conformity second."`
- **Lane spot-check:** `AiActFaq.r2-DWmasV3k.js` and `ActTimeline.r2-CtW5y2Za.js` each had 1 borderline hit — verify against the same canon; `SectorAct.r2` is already CORRECT (leave it).

### 1.4 Unsupported live counters (OsLauncher.r2)
- CURRENT: dynamic `"+ signed episodes"` counter + `"0"` governed/un-governed claims (the 1.45B/121M family from Part AW).
- RULE: no counter ships without a source endpoint and a `verified:` date. Replace with: `"signed artifacts issued: [live count from /api/cards/count] — verified [date]"` or remove the strip until the endpoint exists. Same rule anywhere `billion|million+|signed episodes` renders (OscalStudio, data-industries, ComplianceCommandCenter, ProsperityFund, GlobalAISafetyInitiative — 25 hits total).

### 1.5 "Sovereign OS" → "Council OS" (13 hits)
Locations: main bundle ("60-second live tour: the Sovereign OS…"), DemoOS.r2 (2), homepage JSON-LD `"name": "CSOAI Sovereign OS"`, breadcrumb `"Sovereign OS", item: csoai.org/os` (also fix the dead item URL → `https://councilof.ai/os`), SovOS route meta.
- Global: `Sovereign OS` → `Council OS`; `SOVEREIGN` (as product name) → `Council OS` or `Eunomia` (model context only).

### 1.6 CEASAI certification program (74 hits across ~15 pages) — structural
Pages: AboutCEASAI, CEASAITraining, Certification-v2, CertificationHowItWorks, TrainingHowItWorks, EUAIActUrgency, EarlyAccessLanding, FAQ, Support, WatchdogHelpProtectHumanity, Charter, GlobalAISafetyInitiative + main-bundle "How do I get certified?".
**Ruling:** a company whose trust page says *"we are not a notified body, we issue no certificates of conformity"* cannot sell "AI safety certification." Fold into the Academy:
- `CEASAI` → `Council Academy`
- `certification / certify / certified / certification exam` → `course completion / complete the course / course graduate / course assessment`
- `"Begin your AI safety certification journey"` → `"Start learning AI governance — measured, signed, and honest about what training proves."`
- "How do I get certified?" → "Can I get trained?" linking to Academy.
- Add to every Academy page: `"Completion certificates attest training, not conformity. Council of AI does not certify AI systems."`

---

## 2. MEOK — P0/P1

### 2.1 ✅ DONE & VERIFIED: homepage SOVOS kill (0 hits live). Note the SHA and move on.
### 2.2 P0 — meok.ai/os + os.meok.ai (7× SOVOS, SOVEREIGN model naming)
- `<title>MEOK OS — SOVEREIGN & SOVOS | …` → `<title>MEOK — your own sovereign AI | Council of AI`
- `"SOVOS — the sovereign operating substrate it lives in"` → `"Council OS — the sovereign operating substrate it lives in"`
- `og:title "SOVEREIGN & SOVOS — your own sovereign AI"` → `"MEOK — your own sovereign AI"`
- `"SOVEREIGN is the model, SOVOS is the OS — your AI runs for you"` → `"Eunomia-class models, Council OS — your AI runs for you"`
- **Verify or remove:** title suffix `"C2PA Contributor"` — if CSO AI LTD is not a registered C2PA contributor/member, this is a false affiliation claim (exactly what our trust page criticizes). Remove until membership exists.
### 2.3 P0 — meok.ai/arena (6× SOV4)
- `"SOV4 learning loop"` → `"the Council learning loop"` (or "Pantheon loop" where arena context)
- `"SOV4 learns from all of it"` → `"the Council loop learns from all of it"`
- `"SOV4 trains on GREEN-gated material only"` → `"the loop trains on GREEN-gated, signed material only"`
### 2.4 P1 — local-first claims scoped by mode (/os, 10 hits)
AW P1 stands: with `/api/chat` returning `model:"offline"`, every `"never leaves your device" / "100% private" / "fully offline"` string needs a mode scope: `"Local mode: your data never leaves your device. Cloud mode: signed, logged, and disclosed — status shown live."` The 22 `offline` strings show the honesty instinct is right — keep, and wire the status chip to the real backend state.
### 2.5 P1 — /pricing checkout truth (8 refs)
Until Stripe live-charges work: `"Checkout opens when payments are verified live — join the list and we'll sign you in first."` Never a button that fails after click.

---

## 3. P2 HYGIENE (both)
1. **Fleet naming:** public `sov34`/`Sov3` identifiers → display alias `council-34` / "Council fleet" (Sovos-adjacency hygiene; the measurement IDs stay internal).
2. **Layer0 LIVE statuses:** the pattern is good (per-source `verified: 2026-07-29`) but stale — add the re-verification cron; any status >30 days old renders `STALE` automatically. (22 LIVE hits, all connector statuses.)
3. **Font/SEO:** council shell loads 3 font families over 2 connections — preconnect + subset; every page chunk gets per-route `<title>`/meta (currently shared shell meta).

---

## 4. DO NOT TOUCH (verified good — protect these)
- SovOS axis table: MEASURED/UNMEASURED statuses, "Awaiting a clean multi-model board — no score shown until then", Wilson [0.451, 0.578], frontier-overlap honesty.
- Sov3ModelCard: "does not claim to beat frontier models… differentiator is the governed, auditable layer" + "capability grade still open, gated on a real GPU run" — model honesty, verbatim good.
- SectorAct dates: "Transparency duties land 2 Aug 2026; the full high-risk regime phases in by Dec 2027" — correct post-Omnibus.
- CharterArticle ASI content: legitimate existential-risk governance writing, not hype.
- Trust page disclaimers: "not a certifier · not an enforcer · no accreditation chain" — the doctrine's public face.
- Benchmarks page caveats (n=237 expansion note, open limitations).

---

## 5. EXECUTION ORDER (lane)
1. §1.1 unparsed strings (SovOS chunk) — doctrine contradiction, 15 min.
2. §1.3 deadline FAQ — legal correctness, 15 min.
3. §1.5 Sovereign OS → Council OS sweep + JSON-LD/breadcrumb — 30 min.
4. §2.2 + §2.3 MEOK /os + /arena renames — 30 min.
5. §1.2 positioning/meta + §1.4 counter rule + §1.6 CEASAI fold — half day.
6. Then: rebuild, deploy, and **re-run this manifest's probes against the live bundle** — the grep passing on production is the definition of done.

*Companion doctrine: PUBLIC_DOCTRINE.json (Part AW) should carry every replacement rule above as machine-checkable strings, so no future page can reintroduce them.*
