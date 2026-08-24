# IETF SCITT contribution — Honest-Disagreement Records Are a Row (coverage attestation profile)
From: CSOAI Ltd (UK 16939677) · ed-0.1 · 2026-08-23 · Contribution to the IETF SCITT [Coverage Attestation Profile] debate.

## The mechanic
SCITT receipts prove *what was signed*. We propose a complementary property for the **coverage**
attestation profile: **an honest-disagreement record is itself a row in the log, never an edit.**

## Why it matters for coverage
The hard property of a transparency log is not "everything succeeded" — it is **"when a statement was
wrong, you can see it was wrong, in order."** A coverage attestation that can only ever grow by adding
successful attestations, and that silently corrects a prior claim by overwrite, destroys the audit
property. The honest form: a wrong claim is superseded by a **new appended entry** that references the
superseded one (`prev`), so the history of disagreement is itself attestable.

## The rule we'd add
- Appended rows are immutable; a correction is a **new row** with a link (`prev`) to the row it corrects.
- The ledger therefore records **disagreement**, not just agreement — "the log admits we were wrong" is
  the strongest audit property, and the thing a stranger can rely on.
- Independent, deterministic, signed measurement (Ed25519 over an RFC 8785 canonical content_id) is the
  natural form of an auditable coverage claim — re-checkable offline, no trust required.

## Why CSOAI's mechanic fits
We already implement it (the honest register): UNMEASURED is a legal value, a wrong number becomes a
published correction row, and every claim is signed + offline-verifiable. This is "the scarcest
instrument in the area" — the audit property a coverage log needs but that pure-success logs lack.

_Contributed under the CSOAI measurement-not-certification doctrine. The format is ours, by construction._
