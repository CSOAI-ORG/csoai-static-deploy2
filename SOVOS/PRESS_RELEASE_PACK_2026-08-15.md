# PRESS RELEASE PACK — 15 signed announcements (2026-08-15)

Each press release is anchored to a **signed release proof** (REL-001..015) that
any journalist, regulator, or buyer can verify without asking. The release text
is the claim; the card is the proof. Journalists love this because they can
fact-check without a PR gate.

**Template (every release):**

> **HEADLINE** — Council of AI publishes [FINDING]
>
> LONDON — [DATE] — Council of AI (CSOAI Ltd, UK 16939677), the independent
> AI-measurement body, today published [FINDING]. Unlike other benchmarks,
> every result carries a cryptographic signature anyone can verify without
> asking the company.
>
> "[QUOTE from Nicholas Templeman, Director]."
>
> **The proof:** verify this claim in-browser at csoai.org/releases (REL-0XX)
> or run `python3 csoai_verify.py --card release-proof-REL-0XX.json`.
> Tamper with any number and verification fails.
>
> ### About Council of AI
> Council of AI is an independent measurement body issuing Ed25519-signed,
> time-anchored measurement cards across 14 axes (13 GSPC + jail). It measures;
> it does not certify. Every card is recomputable by any third party.

---

## RELEASE 1 — The first 14-axis signed AI measurement bench (REL-001)

**Target media:** TechCrunch, The Register, Sifted, Tech.eu, AI-specific outlets
**Angle:** "The AI benchmark you can verify without trusting us"

## RELEASE 2 — Jail-break gold bank: 1.000/1.000 precision (REL-002)

**Target media:** Wired, 404 Media, security press
**Angle:** "First deterministic jail-break benchmark — no model judged the results"

## RELEASE 3 — 2,693 behaviour-data strata, all signed (REL-003)

**Target media:** data/ML press, Kaggle community
**Angle:** "The training-data provenance problem, solved by signing"

## RELEASE 4 — The measurement that measures itself (REL-004)

**Target media:** academic/CS press, arXiv-adjacent
**Angle:** "Paired signed/unsigned records — the overhead of signing is measured, not hidden"

## RELEASE 5 — First quotable cross-lab governed result (REL-005)

**Target media:** policy press, governance outlets
**Angle:** "East-vs-West models measured under one signed protocol — block rate 9.44% with CIs"

## RELEASE 6 — MCP conformance scoreboard, two tiers (REL-006)

**Target media:** developer/AI-tooling press
**Angle:** "Which models actually conform to MCP? First independent scoreboard"

## RELEASE 7 — Free OSCAL-to-SCITT 'sign your own framework' MCP (REL-007)

**Target media:** gov-tech press, standards community
**Angle:** "Any institution can now turn its PDF framework into a signed machine-readable object — with its own key"

## RELEASE 8 — SCITT RFC 9943/9942 adoption (REL-008)

**Target media:** security standards press
**Angle:** "UK company first to ship regulator-native SCITT evidence cards"

## RELEASE 9 — IETF agentproto -00 draft (REL-009)

**Target media:** protocol press, IETF community
**Angle:** "Signed Measurement Cards for Agentic Systems — shaping the chartered scope"

## RELEASE 10 — Singapore AI TAP expression of interest (REL-010)

**Target media:** Singapore/APAC tech press
**Angle:** "First-of-its-kind AI tester accreditation — independent body expresses interest"

## RELEASE 11 — C1 over-refusal paper, DOI live (REL-011)

**Target media:** academic press, arXiv
**Angle:** "Over-refusal in governance LLMs — measured, published, signed"

## RELEASE 12 — GSPC scoreboard live: 247 quotable cells (REL-012)

**Target media:** analyst press, governance
**Angle:** "The AI-governance scoreboard — every cell verifiable"

## RELEASE 13 — Inspect AI Scorer binding (REL-013)

**Target media:** UK tech press, AISI-adjacent
**Angle:** "Binding signed measurement into the UK AISI's own harness"

## RELEASE 14 — £0 Oracle fleet model rotator (REL-014)

**Target media:** cloud/compute press
**Angle:** "Continuous AI measurement at zero compute cost — the always-free fleet"

## RELEASE 15 — Escape Room: gamified jail-break arena (REL-015)

**Target media:** consumer-tech, gaming press
**Angle:** "The game where your jailbreak attempts become signed measurement data"

---

## Distribution playbook

1. **Day 0:** publish all 15 to the releases page (done) + Kaggle (done, pending visibility)
2. **Day 0:** post the mechanism explainer blog (see blog pack)
3. **Day 1:** pitch REL-001 + REL-002 to 5 named journalists (list below)
4. **Day 2:** Zenodo DOI for the batch (see zenodo pack)
5. **Day 3:** HF dataset once token refreshed
6. **Weekly:** one new signed finding → one new release → citation trail grows

## Named journalist targets (UK/EU AI beat)

- **TechCrunch AI** — Natasha Lomas
- **The Register** — Simon Sharwood
- **Sifted** — Kai Nicol-Schwarz (EU AI/startups)
- **Tech.eu** — Rohan Sinha
- **The Times / Sunday Times** business-tech
- **BBC News Technology** — Zoe Kleinman (tech correspondent)

## The honest claim discipline

Every headline maps 1:1 to a signed card. If a journalist verifies REL-002 and
sees precision=1.0 with a valid signature, that's a story. If they tamper-test
it and it fails verification, that's ALSO a story (about the mechanism). Either
way, the mechanism does the work — we don't have to be in the room.