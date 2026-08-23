# EU AI Act Article 50 — Signed Provision-Conformance Receipt Spec (pilot v1)
For: Mosaic × Munich Re aiSure (first target) — the objective threshold test inside their
parametric-like settlement. Research-verified 2026-08-21 (see INSURER_PILOT_v2).

## Why Art 50
- Only AI Act tranche LIVE in the pilot window: high-risk deferred to 2 Dec 2027 (Omnibus),
  **Art 50 applies from 2 Aug 2026**, penalties to €15M / 3% worldwide turnover.
- Duties are BINARY + machine-checkable (not probabilistic): disclosure present/absent,
  synthetic-output marking machine-readable, deepfake disclosure, biometric/emotion notice.
- Already inside a SOLD cover line ("AI Model Regulatory Violations — EU AI Act").
- 2 Dec 2026 legacy-marking cliff creates urgency NOW.
- CSOAI C2PA Contributor seat is directly on-point for the marking limb.

## The receipt (csoai.art50/0.1)
Envelope: body -> RFC 8785 canonical -> content_id = sha256(canonical minus signature) ->
Ed25519 sig, kid did:web:csoai.org#card-attestation-1. Offline-verifiable by any party.

Body fields:
- provision: EU-AI-Act-2024-1689-Art50
- frozen_text: (the exact Art 50 text the conformance was measured against)
- input_set: declared scope (which outputs were tested)
- verdict: CONFORMING | NON-CONFORMING | UNMEASURED
- measured_at: UTC timestamp
- predicate: machine-readable test description (exact_match / manifest_valid / present)

## WORKED EXAMPLE — CONFORMING -> NON-CONFORMING (the trigger)
### T0 (binding): system discloses AI interaction to users + marks synthetic output
- Predicate checks: (a) disclosure text present in the interaction preamble;
  (b) synthetic audio/image output carries machine-readable marking (e.g. C2PA manifest).
- Verdict: CONFORMING. Receipt R1 (content_id 7f3a…, sig valid, kid card-attestation-1).
- Underwriting artefact: condition precedent satisfied.

### T1 (mid-policy, cadenced re-measure): the marking disappears from a new output family
- Same frozen text, same predicate. New output family: no disclosure preamble, no marking.
- Verdict: NON-CONFORMING. Receipt R2 (content_id 91c2…, sig valid).
- THE TRIGGER: CONFORMING -> NON-CONFORMING on frozen text = non-discretionary, externally
  observable state change. aiSure-style settlement responds to the threshold breach.
- Claims answer: "breached — at T1, on provision Art 50, over input_set X" — deterministically,
  without forensic investigation.

### T2 (after fix): disclosure + marking restored
- Verdict: CONFORMING. Receipt R3. Chain R1 -> R2 -> R3 = the policy's conformance ledger.

## Honesty guardrails (stated, tested)
- Measurement, not certification; not loss prediction (concede Testudo's null result).
- Basis risk between conformance state and insured loss stays in the wording.
- UNMEASURED stays UNMEASURED (input sets outside scope never get a verdict).
- Frozen text = the yardstick cannot drift under the policy.

## Next
1. Wire the Art 50 predicate into council_ledger.py (live demo receipt).
2. One-page outreach brief for Dennis Bertram (Mosaic) with R1/R2/R3 example.
3. Verify dates against Official Journal publication before any external deck.
