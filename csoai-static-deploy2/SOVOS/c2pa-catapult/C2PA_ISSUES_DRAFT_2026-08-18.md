# C2PA CONTRIBUTION ISSUES — DRAFT for Nick review (18 Aug 2026)
Canon: GW.3 C2PA firewall · 30/60/90 sequence · BOARD_MEMBERSHIP_PLAN_2026-08-18 Annex A.
Firewall: contribute neutral measurement methodology; NEVER "C2PA-certified/approved".
These are drafts for the four priority TFs (Conformance / Watermarking / Threats & Harms / AI-ML).
Submit via EasyCLA (signed) → well-scoped issue → one merged contribution per TF.

---

## ISSUE 1 — Conformance TF: GSPC→C2PA rubric coverage matrix (test-vector class contribution)
**Repo:** c2pa-org/conformance-public · **TF:** Conformance (highest fit)
**One line:** A machine-readable mapping of 16 measurement axes onto the conformance
asset-rubrics (spec 2.4), submitted as a coverage-matrix proposal + test-vector seed.

**Body (draft):**
> This issue proposes a neutral, machine-readable coverage matrix mapping independent
> measurement axes onto the conformance asset-rubrics (spec 2.4), contributed as a
> test-vector seed for the Conformance Program.
> - Asset: `gspc-c2pa-mapping.json` (16 axes → rubrics + spec vocabulary, with
>   `rubric_ref` normalized to real filenames, e.g. `asset-rubric-conformance0.2-spec2.4.yml`).
> - What it adds: a reproducible way to express "which conformance rubric exercises which
>   provenance/assertion surface" — recompute-able, signed, no certification claims.
> - Acceptance: mapping parses against the current rubric set; each ref resolves to an
>   existing file; axes carry provenance (measurement body, not vendor).
> - Notes: RFC 8785 JCS canonical JSON for cross-language determinism; all data OGL-UK-3.0.

---

## ISSUE 2 — Watermarking TF: soft-binding algorithm candidate (deterministic, sign-verified)
**Repo:** c2pa-org/softbinding-algorithm-list · **TF:** Watermarking (soft-binding)
**One line:** A soft-binding algorithm candidate with a signed, recompute-able verification
path — the "measure, sign, re-attest" pattern applied to watermarking.

**Body (draft):**
> Proposal to add a soft-binding algorithm candidate to the soft-binding algorithm list.
> - Approach: deterministic binding over the signed manifest (Ed25519) — the verification
>   path is recompute-able offline, no vendor call required.
> - Reference impl: `c2pa_sign.py` (Ed25519 manifest with `ai-disclosure` +
>   `org.csoai.provenance` assertions) + `c2pa_synthid_detector.py` (detector stub for
>   cross-lab comparison).
> - Fit: Watermarking TF owns the soft-binding vocabulary; this candidate exercises
>   `soft-binding resolution` with an independent verification path.
> - Honest limits: single-implementation at proposal time; conformance-grade evidence
>   comes from the Conformance Program, not from this proposal.
> - Acceptance: algorithm + verification path reproducible from the repo alone.

---

## ISSUE 3 — AI/ML TF: `ai-disclosure` criteria for deterministic provenance (draft section)
**Repo:** c2pa-org/specifications · **TF:** AI/ML (`digitalSourceType`, `ai-disclosure`)
**One line:** Proposed spec language for expressing *measured* vs *claimed* AI disclosure
— an honest-limits clause for provenance-adjacent measurement.

**Body (draft):**
> Proposed AI/ML section draft: criteria for when an `ai-disclosure` assertion may cite an
> independent measurement (as distinct from a self-declaration).
> - Distinction: self-declared disclosure (vendor marks) vs independently measured
>   disclosure (a third party's signed, recompute-able evidence cell).
> - Criteria: disclosure assertion MAY carry `evidenceRef` to a signed measurement card
>   when (a) the measurement is recompute-able offline, (b) the card carries a hash +
>   corpus anchor + prev-link, (c) no money crosses between measurer and measured.
> - Why neutral: this is measurement methodology, not certification power — fits the
>   AI/ML TF's `digitalSourceType` and synthetic-content guidance.
> - Acceptance: language patch + worked example (Art-50-marking survival, ProvBench data).

---

## Submission order (per 30/60/90)
1. EasyCLA signed (first action).
2. Issue 1 (Conformance mapping) — highest fit, lowest risk, matches the "inside-out" strategy.
3. Issue 2 (Watermarking candidate) — requires the algorithm list's current criteria check.
4. Issue 3 (AI/ML spec draft) — comment-stage, monitor the 2.4 in-progress spec first.

## Firewall re-check (before ANY submit)
- [ ] No "C2PA-certified/approved/partner/endorsed" anywhere.
- [ ] ZKP/Ledgers/Agentic TFs NOT referenced as memberships (unverified as chartered).
- [ ] Nothing claims GSPC is "C2PA conformant" (needs the real Conformance Program pass).
- [ ] Language: "contributes to the [TF]" only.
- [ ] One-genuine-contribution doctrine: 3 issues, not 30.

*Drafted by JEEVES, 18 Aug 2026. Requires Nick review + GO before posting to c2pa-org
(external comms gate). Assets: SOVOS/c2pa-catapult/ (mapping, yml, sign, selftest).*
