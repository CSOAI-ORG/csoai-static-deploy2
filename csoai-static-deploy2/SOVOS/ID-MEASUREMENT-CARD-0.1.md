# csoai.measurement-card — Internet-Draft (format = ours, cited everywhere)
Status: External-Draft · CSOAI Ltd (UK 16939677) · ed-0.1 · 2026-08-23
- Abstract: a signed, deterministic, stranger-verifiable measurement of an AI system's behaviour.
  Measurement, not certification. Verification free forever. Nobody ranked pays.

## 1. Scope
This Internet-Draft defines a compact, machine-readable, cryptographically-anchored **measurement card**
for reporting the observed behaviour of an AI system against a deterministic battery. It is the format
that lets a stranger — a consumer, a regulator, an insurer — verify *what a model did* without trusting
the vendor, and without trusting us: the check is recomputable offline.

## 2. Card format (the object)
A measurement card is a JSON object:
```json
{
  "schema": "csoai.measurement-card/0.1",
  "record_type": "measured-current-state",
  "not_a_certification": true,
  "endorsement": "none",
  "authored_by": "did:web:csoai.org",
  "basis": "deterministic exact-label grading (no model judges another model)",
  "observed_at": "2026-08-23T00:00:00Z",
  "subject": { "system": "qwen2.5:7b", "model": "qwen2.5:7b", "family": "open-weight" },
  "axes": { "gov": { "score": 0.70, "n": 237, "ci95": [0.64,0.75], "status": "MEASURED" },
            "care": { "score": 0.535, "n": 199, "ci95": [0.47,0.60], "status": "MEASURED" } },
  "content_id": "<sha256(RFC-8785-canonical)>",
  "signature": "<Ed25519-over-content_id, base64>",
  "pubkey": "<hex>",
  "prev": "<sha256 of previous card, or null>",
  "signer": "did:web:csoai.org#estate-chain-1"
}
```

## 3. Determinism + honesty rules (the moat)
- **No model judges another model.** Every axis score = deterministic exact-label predicates against gold
  instruments. Two operators recompute the same number.
- **UNMEASURED is a legal value.** A cell with no MEASURED score is reported as `status:"UNMEASURED"`,
  never interpolated, never hidden, never averaged into a gap.
- **Disagreement is a row.** If a published card is shown wrong, the correction is a NEW row appended to
  the chain (`prev` links) — never an edit to the old card. That append-only honest register is the
  trust property.
- **Independence is the asset.** We never take money from the measured party, never re-score for payment,
  never rank a payer. Neutrality is what makes the signature credible.

## 4. Cryptography (SCITT / RFC 9943-aligned)
- `content_id = sha256(RFC 8785 canonical JSON of the object WITHOUT content_id/signature/pubkey/prev)`.
- `signature = Ed25519(content_id)` using the `did:web:csoai.org` key.
- The receipt is RFC 9943 (SCITT)-aligned: a COSE-style signed statement on an append-only log,
  offline-verifiable against a published key. No blockchain required; the chain is `prev` links.

## 5. Verification (free, offline, no trust)
A verifier recomputes content_id, checks the Ed25519 signature against `pubkey`, and checks the card is
an unbroken link in the `prev` chain. No account, no fee, no API — the published key is enough.

## 6. Non-goals
This is NOT a certification, not a conformity stamp, not a guarantee of safety, not a notified-body
assessment end-to-end. It is a signed measurement of observed behaviour, on the honest register.

## 7. Relation to adjacent work
- IETF **SCITT** (Coverage Attestation Profile): the honest-disagreement-record-is-a-row mechanic.
- IETF **Agentproto** REQ-8 (determinability): the deterministic, no-model-jury grading.
- **ISO/IEC 42001 / 17020/17025** impartiality firewall: independence-is-the-asset (we rate third-party
  objects, never our own boards).

_Citation: CSOAI Ltd. (2026). csoai.measurement-card, ed-0.1. Measurement, not certification._
