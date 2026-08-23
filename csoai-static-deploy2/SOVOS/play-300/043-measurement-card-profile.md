# 043 — MEASUREMENT-CARD PROFILE (👑 CROWN JEWEL · individual I-D · H9/D01 §4a)

Date: 2026-08-21 · lane: K3 · gate: datatracker confirmation · REAL: zero signed eval-score drafts exist —
this profile owns the score layer (I1).

## 1. Identity
- Media type: `application/agent-measurement+json`
- Envelope: COSE_Sign1, alg **-19** (EdDSA/Ed25519)
- Claims: CWT `iss` (independent evaluator) + `sub` (measured subject) + `kid` (key id)
- Conforms to RFC 9943 §6 (SCITT statement); receipts per RFC 9942 (TS registration, label 394,
  VDS RFC9162_SHA256, multi-TS) — the inversion every current draft lacks: **iss = evaluator, sub = subject.**

## 2. Card payload
```
subject_digest, suite_version_hash, score_vector (+CI), environment_commitment,
replay_merkle_root, method, timestamps
```
Traces stay off-card (reproducible, not shipped). JSON schema + 2 examples required (M).

## 3. Honest anti-equivocation section
- **Inclusion** proven by the receipt + Merkle root.
- **Non-equivocation** needs consistency proofs + monitor — NOT implied by the receipt
  (passes NOA-lesson review, D01 §5).

## 4. Semantics
Cite/adopt WEXP appraisal semantics BEFORE anyone builds on it (D01 §6). Register as individual I-D
(datatracker); no AAIF membership needed (SEP-932).

## 5. Status
Draft v0.1; UNSIGNED until POD key. Datatracker submission = external (NICK/Claude lane).
