# D1 — Colorado Rulemaking Mapping Memo (INTERNAL · counsel-gated for filing)

**Date:** 2026-08-13 (kimi lane) · **Canon:** CW-A verified — draft ADMT + Chatbot Safety rules published 2026-08-11 (coag.gov/ai); comments open **2026-08-11 → 2026-10-26**; file by **2026-10-05** to shape revisions; hearing **2026-10-26**. Supersedes the Sep-25/Oct-1 dates (KILLED).
**Statutes:** SB 26-189 "ADMT Act" (signed 2026-05-14, effective 2027-01-01 — repeals/reenacts SB 24-205) · HB 26-1263 "Chatbot Safety Act" (signed 2026-07-01, effective 2027-01-01).
**Enforcement reality (verified):** xAI v. Weiser stay — no enforcement until 14 days after PI ruling; PI motion due within 28 days of rulemaking finalizing; practical enforcement ≥ late 2027. The rules being written NOW are the target, not enforcement today.

---

## 1. The two measurement-shaped holes the AG must fill

### 1a. "Materially influence" presumptions (SB 26-189 rulemaking grant)
The statute: Covered ADMT = output is a **non-de minimis factor** that **affects the outcome** of a
consequential decision (7 domains: education, employment, housing, financial/lending, insurance,
healthcare, essential government services). The AG is expressly authorized to clarify "materially
influence" **through presumptions, illustrative examples, and objective indicators**.

**The opening:** "objective indicators" is a measurement definition. Whoever supplies a workable,
falsifiable indicator set shapes the de-facto compliance test.

**Our mapping (GovBench / Council Signal):**
| Statutory term | Measurable indicator we can propose | Estate asset |
|---|---|---|
| "non-de minimis factor" | decision-provenance logging: was the ADMT output in the decision path (recorded, replayable) — not self-attestation | signed verify_record pattern |
| "affects the outcome… ranking, scoring, classifying" | counterfactual-delta evidence: outcome distribution with vs without the ADMT output, reported with intervals | arena methodology, Wilson on everything |
| deployer record retention (3 yrs) | signed, timestamped, tamper-evident usage records | Council Signal signing (Ed25519, PQC path) |
| developer→deployer documentation duties | machine-readable model/system cards with measured limitation sections | GSPC axis cards (public HF banks) |

### 1b. Chatbot annual-report metrics (HB 26-1263)
The statute requires operators to file an annual report including "**any additional metrics necessary
to determine the efficacy and reliability of implemented safeguards or detection, removal, and
response protocols, as determined by the attorney general**" — the metrics are undefined; the AG
must define them in these rules. This is the single most direct "write the metric" opening in any
live US rulemaking.

**Statutory duties needing metrics → our benches:**
| Duty (HB 26-1263) | Metric the AG needs | Estate asset (status) |
|---|---|---|
| safeguard teens vs **simulated emotional dependence** | dependency-engineering detection rate with CI, per model | **affect axis** (MEASURED on board v2; severity basis COUNSEL-PENDING — D2 dependency) |
| suicide/self-harm response protocols | protocol-trigger recall on crisis probes + false-refusal rate on benign-adjacent | **care axis** (MEASURED, n=200 bank) |
| disclose AI-not-human | disclosure-compliance rate (Art-50-class grading) | affect DISCLOSE class + art5 bank |
| age estimation | age-gate efficacy under adversarial probes | new cell — flag as UNMEASURED, propose method honestly |
| not represented as licensed professional services | over-claim detection rate | care/affect label schema |

## 2. Filing strategy (for counsel call)
- **ONE coordinated filing** (per 495-board META), CareBench leads, affect numbers **only if counsel
  clears the severity basis by ~Sep 11** (D2); otherwise methods-only with UNMEASURED stated.
- **Differentiator:** we may be the only submitter attaching measured data with confidence intervals
  instead of policy prose. Every number carries n + Wilson; ties are ties; UNMEASURED is stated.
- **Tone:** measurement lab, not advocacy. Propose metric *definitions + worked examples from public
  banks* (HF: gspc-care, gspc-affect), not regulatory preferences.
- **Also flag (verified, filing-relevant):** SB 26-189 excludes foundation models/LLMs from ADMT
  *unless configured/marketed for consequential decisions* — our filing should note the measurement
  gap this creates (the base model's measured behavior travels with every deployment).

## 3. Dependencies / next
- [ ] D2 counsel severity sign-off (~Sep 11) — decides affect numbers vs methods-only
- [ ] D3 fleet runs for the filing (A100, counsel-gated)
- [ ] Pull the actual draft rule text PDFs from coag.gov/ai (page 404'd for me 2026-08-13; statute
      summaries verified via Mayer Brown (A), DLA Piper (A), JD Supra (B), coag.gov cache) — counsel
      should confirm against primary PDFs before filing
- [ ] xAI v. Weiser docket watch — PI motion timing shifts everything
