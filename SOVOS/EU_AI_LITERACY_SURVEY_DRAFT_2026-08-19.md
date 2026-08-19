# EU AI Literacy Survey — Draft Answers (Article 4, AI Office living repository)
**Status:** DRAFTED 2026-08-19 · Survey: https://ec.europa.eu/eusurvey/runner/ai_literacy_survey
**Organisation:** Council of AI (CSOAI Ltd, UK Companies House 16939677) · Micro (1-15) · UK

## Section 1 — Contact
- 1.1 Name: Nicholas Templeman
- 1.2 Email: nicholas@csoai.org

## Section 2 — Company background
- 2.1 Organisation: Council of AI (CSOAI Ltd)
- 2.2 Size: Micro (1-15 employees)
- 2.3 HQ: United Kingdom

## Section 3 — AI system in use (the system our literacy practice concerns)
*The system we deploy is our own measurement instrument stack — the GSPC (Governance, Safety, Provenance, Continuity) 14-axis evaluation platform plus the public arena. It is an AI system that evaluates other AI systems using deterministic predicates; no LLM judges another LLM.*

- 3.x Type of AI system: AI evaluation / measurement platform (deterministic predicate scoring of AI models; Ed25519-signed measurement cards; public arena for human-vs-AI and AI-vs-AI rounds)
- AI techniques: model evaluation, prompt-based assessment on frozen statutory instruments, hash-chained attestation
- Deployment context: publicly accessible measurement service (councilof.ai), used by insurers, regulators, enterprises and developers

## Section 4 — AI literacy approach + the practice we share

### 4.x General approach to AI literacy (Article 4)
Council of AI treats AI literacy as a *first-party audit discipline*: everyone who touches the measurement stack — staff, contractors, and the public who use the arena — must understand (a) what a measurement card proves, (b) what it does not prove, and (c) how to read a confidence interval and an n. Our published doctrine is: "an attested answer is attested, never verified" and "the instrument governs provenance, not correctness." Literacy is enforced by the estate's claim grammar: every public statement must parse as data (register + evidence link + registered microcopy + signed artifact hash), so an untrained reader cannot be misled by a fluent-but-unsupported claim.

### 4.x The specific practice we share: the Open Measurement Literacy Practice
**Name:** The Open Measurement Literacy Practice (the "honesty gate" programme)

**What it is:** A public, free, structured programme that teaches stakeholders how to read independent AI measurement:

1. **The honesty gate page** (councilof.ai/honesty) — we publish the result that embarrasses us: our own fine-tunes losing to base models in our own arena, with every number from the signed pod state. Readers learn that a measurer publishing its own failures is the credibility test. 3,700+ signed arena rounds, fully reproducible.
2. **Verify-a-card walkthrough** (councilof.ai/verify) — anyone can paste a signed 3KB measurement card and recompute the Ed25519 hash chain in their browser. Literacy = being able to check the signature yourself, with no account and no fee.
3. **The frozen/fluid doctrine** — published instruments are hash-sealed and timestamp-anchored (frozen: never silently changed); the live board is a signed append-only chain (fluid: every update a new signed record). Stakeholders learn to distinguish "frozen evidence" from "live state."
4. **The corrections ledger** — every error we make is published as a superseding record, never silently edited. The ledger opens with our own mistakes (45 entries). Literacy includes knowing that a body which corrects itself in public is one you can trust.
5. **UNMEASURED is shown, never invented** — empty cells stay empty on the public board; the gated badge reads "not measured yet — we don't guess." Stakeholders learn the difference between an honest gap and a fabricated score.

**Target audience:** insurers underwriting AI, procurement officers, regulators, developers, and the general public entering the arena.

**Measured impact:** the practice is itself measured — every page view of the honesty gate and every successful browser verification is a signed event on the append-only chain; the estate's E2E scoreboard (15/15 live surfaces) is published. We also run an annual self-audit (the persona gauntlet: VC, auditor, regulator, AI company, legal, end user, machine agent, developer each walk the surfaces and their failures log as signed drift events).

**Why it is transparent and reliable (AI Office minimum criteria):**
- Transparency: every number traces to a signed artifact with n and confidence interval; the signing key is public (did:web:csoai.org); verification is free, loginless, and offline-capable.
- Reliability: deterministic predicates, no LLM-as-judge, frozen instruments, and a drift-guard CI that blocks any build whose axis count or banned strings drift from canon.

**Contact for the practice:** nicholas@csoai.org
