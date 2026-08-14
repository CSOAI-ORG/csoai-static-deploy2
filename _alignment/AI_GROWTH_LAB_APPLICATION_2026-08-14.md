# AI GROWTH LAB APPLICATION — SKELETON (DSIT Grants Hub)
**Part DJ Move 1 · drafted 2026-08-14 · deadline 11:59pm 27 Sep 2026 (44 days)**
**Applicant**: CSOAI Ltd (#16939677) · trading as Council of AI
**Cohort**: Legal Services & Conveyancing (first AI Growth Lab cohort)
**Register**: REAL assets cited only · GATED = owner submit + counsel pass before send

---

## WHY THIS IS THE RIGHT WINDOW (brief)
The Lab is advisory-only (no rule relaxation in cohort 1) — but it buys **coordinated
regulator reading** (SRA, LSB, CLC, ICO) on how signed measurement maps to professional
conduct rules. Regulators are named in the Lab's structure; we bring the neutral,
verifiable measurement layer they'd otherwise have to invent. The court-hallucination
cases that motivated the sector choice are exactly our Art5Bench/crosswalk evidence class.

## SECTION A — APPLICANT
- **Legal name**: CSOAI LTD, company no. 16939677
- **Trading as**: Council of AI (measurement body — neutral, signs Ed25519 measurement
  credentials; issues measurement, never certification)
- **Type**: SME · sole founder + automated measurement fleet
- **Contact**: [FILL email] · [FILL phone]

## SECTION B — USE CASE (the pitch)
**Title**: "Independent, signed measurement of AI-assisted legal content against
professional-conduct evidence standards."

**Problem**: Legal-services AI (drafting, research, conveyancing support) can
hallucinate citations and misstate the law. Firms adopting it face an evidence gap:
how does a firm *prove* — to the SRA, its insurer, its clients — that its AI output is
reliable and within conduct rules? Self-reported vendor claims are not proof.

**Solution (what we build in the Lab)**: an independent measurement service that:
1. Runs a firm's chosen legal-AI stack through a **frozen, disclosed bank** of
   legal-governance probes (citation integrity, hallucination, advice-boundary,
   client-conflict, refusal behaviour) — our existing Art5Bench + GovBench engines,
   REAL (684/676 rows, 4,329 gov rows, crosswalk engine).
2. Returns an **Ed25519-signed, OTS-anchored measurement credential** a third party
   (firm, insurer, regulator) can verify without trusting us.
3. Provides **drift re-attestation** — re-measure on every model update, so the
   evidence never goes stale (18/18 drift lane, hourly cron, REAL).
4. Maps results to the **professional-conduct evidence record** firms must keep
   (SRA Principles / Codes via our OSCAL crosswalk engine, ~5,377 LOC, REAL).

**Why us / why now**: we are the only party with no side — we don't write the standard,
don't accredit auditors, don't underwrite. The Art 50 transparency regime is live
(2 Aug 2026) and machine-readable marking lands 2 Dec 2026; firms will need dated,
verifiable evidence before then.

## SECTION C — WHAT THE LAB GETS FROM US (our commitment)
- A **pilot cohort of up to 5 legal-AI deployments** measured on the frozen bank,
  results published as signed credentials (with participant consent).
- A **methodology disclosure** the Lab can share with regulators (SRA/LSB/CLC/ICO):
  the probe bank design, the held-out split discipline, the signing/anchoring scheme.
- A **regulator-facing evidence template** — "what a conduct-compliant AI-assisted
  workflow's measurement record looks like".

## SECTION D — WHAT WE SEEK FROM THE LAB
- Coordinated reading from SRA/LSB/CLC/ICO on how signed third-party measurement maps
  to existing conduct rules (advisory, no rule change requested).
- A named **regulator reference** for the evidence format (the neutrality firewall is
  the product — we never advise the measured firm on remediation).
- Visibility into the next cohort sectors (healthcare, professional services) to
  template the evidence pack.

## SECTION E — EVIDENCE / READINESS
| Asset | Register | Proof |
|---|---|---|
| Art5Bench 684/676 rows | REAL | frozen bank, per-item CIs |
| GovBench 4,329 usable rows | REAL | 237-item bank, canaries excluded |
| OSCAL crosswalk engine ~5,377 LOC | REAL | open release, signed tag (post-counsel) |
| Ed25519 + OTS spine 11/11 | REAL | master verify, did:web f4b4278d |
| Drift re-attestation 18/18 | REAL | hourly cron |
| Redteam scanner 21/21 | REAL | garak/PyRIT adapters |

## SECTION F — COMPLIANCE / HONESTY
- **Measurement, not certification** — no claim of SRA/conduct approval.
- **No public index/benchmark** framing until legally scoped.
- **Neutrality firewall**: we measure; we never sell remediation/consulting to the
  measured party (Part DC/DF doctrine).
- **Counsel pass required before submit** (naming, evidence-pack wording, any
  regulator-facing claims).

## SECTION G — OWNER CHECKLIST (before submit)
- [ ] Counsel pass on Sections B/F wording (Sep 11 session or earlier email)
- [ ] Fill contact + company address (published)
- [ ] Confirm DSIT Grants Hub live entry + form fields (re-verify 1 week before)
- [ ] Attach the signed Art5Bench sample card as evidence
- [ ] Submit via DSIT Grants Hub before 11:59pm 27 Sep 2026

---
*Companion: `REFEREE_MAP_2026-08-14.md` (Part DF) · `GTM_2026-08-14.md` (Part DG) ·
`PRIOR_ART_FTO_2026-08-14.md` · catapult. The AI Growth Lab was earlier mis-killed in
`VALUATION_AND_PARTNER_ROUTES` (call-for-evidence vs application cohort confusion) —
reversed 2026-08-14 with gov.uk primary source (Part DJ).*
