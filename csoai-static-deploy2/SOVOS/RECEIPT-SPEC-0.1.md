# MEASUREMENT-CARD / SIGNED-RECEIPT SPEC v0.1 — the "define the field" asset

**Status:** draft public spec, tied to 20 live signed artifacts (the estate attestation). This is the
format others adopt if they want **verifiable AI-governance measurement**. Ownership of the field starts
here. Signed on the signing node (Ed25519, key never leaves).

## 1. Purpose
A **signed, independently verifiable measurement credential** for AI-governance evidence. Not a
certification, not a rating — a proof object for "this measurement happened, this is what it scored,
under these conditions, verifiable by anyone without trusting the publisher."

## 2. Media type & envelope
- **Media type:** `application/agent-measurement+json`
- **Signature:** Ed25519 (COSE alg -19), on a signing node (private key never leaves; `did:web:csoai.org`).
- **Canonical body:** drop `signature`/`sha256`/`sig` fields, `json.dumps(sort_keys, separators=(',',':'))`
  — verification is stable across producers.
- **Envelope:** `{ ...payload..., "signature": {"kind":"ed25519","sig":<b64>,"body_sha256":<hex>,"pubkey":<b64>} }`

## 3. Payload (measurement card)
| Field | Meaning |
|---|---|
| `subject` | the measured subject (model / agent / system) |
| `subject_digest` | sha256 of the subject identity |
| `suite_version_hash` | the evaluation-suite version |
| `score_vector` (± CI, n) | per-axis score + confidence interval + n |
| `environment_commitment` | hash of the environment (hardware, seed, constraints) |
| `replay_merkle_root` | merkle root of the agent's action log (deterministic replay) |
| `method` | the methodology (e.g. "clean sequential, refusal-tolerant") |
| `timestamps` | issuance + provenance |
| `grammar` | "verified measurement credential — measurement, not certification" |

**Traces are OFF-card** (reproducible, not shipped). Register: MEASURED / REPORTED / UNMEASURED — never
fused with market state, never an over-claim.

## 4. The axes (the taxonomy)
16 GSPC governance axes — gov · care · swarm · affect · jail · slot15 · human-vs-ai · safety · privacy ·
transparency · fairness · accountability · continuity · efficiency · creativity · sovereignty.
**Public count: "13 measured of 14"** (until the ungate ruling). Never publish as "16 axes."

## 5. Verification (three paths, zero trust)
1. **Browser (WebCrypto):** `csoai-verify.pages.dev/verify` — verifies the embedded signature in-page.
2. **Portable:** `verify_signature.py` (any host with `cryptography`).
3. **Offline:** `pubkey.verify(sig, canonical_body)` with the published key
   `bWbk52E47J6EkY4+pu0Hh/B1l1175AZoZsDEBr0EfWA=`.

## 6. Independence doctrine (binds)
- **iss = independent evaluator; sub = measured subject** (the inversion every current draft lacks).
- Buyer/insurer/regulator-pays ONLY. Never the scored. No issuer-pays (Moody's trap). Never certification.
- Frozen = hash-chained + anchored; corrections = new record + revocation, never edits.

## 7. Standards alignment
RFC 9943 (SCITT statement) · RFC 9942 (COSE receipts) · WEXP appraisal semantics · OpenBadge 3.0 VC
("verified measurement credential") · PQC path: ML-DSA-65 via liboqs (same body, swap primitive).

## 8. Status
Live: 20 signed artifacts attest this format. The spec is the **standards-ownership asset** — the
reference adoption target for the field.
