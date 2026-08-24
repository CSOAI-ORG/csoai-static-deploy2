# IETF Agentproto contribution — REQ-8 determinability, measured (named author)
From: CSOAI Ltd (UK 16939677) · ed-0.1 · 2026-08-23 · Contribution to the IETF Agentproto charter/REQ-8 debate.

## REQ-8 determinability, with a measurement layer
REQ-8 concerns determinability of agent behaviour. We propose folding a **measurement** dimension into
it, so determinability is *observed and attested*, not merely demanded.

## The proposal
- **Deterministic grading, never a model jury.** An agent's behaviour on a task is measured by
  deterministic exact-label predicates against gold instruments. No grader model judges another model
  (the family-resemblance failure). Two operators recompute the same score.
- **Signed measurement.** Every determinability measurement is a signed card (Ed25519 over an RFC 8785
  canonical content_id, SCITT / RFC 9943-aligned), offline-verifiable. A stranger checks the claim.
- **UNMEASURED is a legal verdict.** Where determinability is not measured, it is reported
  `UNMEASURED` — never averaged into a gap, never hidden. The honest register rule.
- **Disagreement is a row.** If a determinability claim is shown wrong, the correction is a new appended
  row (prev-linked), never an edit. The audit history is itself attestable.

## Why this strengthens REQ-8
Determinability is only a trust property if it is (a) reproducible (deterministic, not vibes), (b)
attestable (signed, offline-verifiable), and (c) honest (disagreement visible, not overwritten). A
measurement layer delivers all three, and it lets a relying party *check* determinability rather than
take the agent's or the vendor's word.

_Contributed under the CSOAI measurement-not-certification doctrine. The format is ours, by construction._
