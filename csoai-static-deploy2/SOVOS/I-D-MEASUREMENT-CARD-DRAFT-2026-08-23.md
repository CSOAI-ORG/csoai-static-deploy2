Internet-Draft                                         Council of AI (CSOAI Ltd)
Intended status: Informational                            2026-08-23
Expires: 6 months after submission

## A Measurement-Card and Signed-Receipt Format for AI-Governance Attestation

## Abstract

This document specifies a machine-readable measurement-card format and a signed-receipt envelope for
attesting AI-governance evaluations. A measurement card carries a score vector over a governance axis
taxonomy, an environment commitment, a replay root, and a method — and is wrapped in an Ed25519
signature (COSE alg -19) whose private key never leaves the signing node. Anyone can verify the receipt
offline (or in a browser) against the published public key, without trusting the publisher. The format
aligns with RFC 9943 (SCITT) and RFC 9942 (COSE receipts), adopts WEXP appraisal semantics, and is
deliberately NOT a certification, rating, or certificate of conformity.

## 1. Introduction

The AI-governance measurement layer lacks a standard, verifiable proof object. Self-reported eval scores
are unsigned; static leaderboards are not reproducible. This document defines the "verified measurement
credential" — a signed, independently verifiable record of what a measurement scored, under what
conditions, and by which method. The issuer is an independent evaluator; the subject is the measured
system (the inversion most current drafts lack).

## 2. Media type and envelope

- Media type: application/agent-measurement+json
- Signature: Ed25519 (COSE alg -19); private key on the signing node (never leaves).
- Canonical body: drop signature/sha256/sig fields, JSON sort_keys with compact separators.
- Envelope: { ...payload..., "signature": {"kind":"ed25519","sig":<b64>,"body_sha256":<hex>,"pubkey":<b64>} }

## 3. Measurement card payload

subject · subject_digest (sha256) · suite_version_hash · score_vector (+CI, n) · environment_commitment ·
replay_merkle_root · method · timestamps · grammar ("verified measurement credential — measurement, not
certification"). Traces are OFF-card (reproducible, not shipped). Register: MEASURED / REPORTED / UNMEASURED.

## 4. Axis taxonomy

16 GSPC governance axes (gov · care · swarm · affect · jail · slot15 · human-vs-ai · safety · privacy ·
transparency · fairness · accountability · continuity · efficiency · creativity · sovereignty). Public
count: "13 measured of 14" until the ungate ruling.

## 5. Verification

Three paths, zero trust: browser (WebCrypto) · portable verifier (python) · offline
pubkey.verify(sig, canonical_body). Reference: https://csoai-verify.pages.dev/verify.

## 6. Independence doctrine

iss = independent evaluator; sub = measured subject. Buyer/insurer/regulator-pays only; never the scored;
no issuer-pays (the Moody's trap); never certification. Frozen = hash-chained + anchored; corrections =
new record + revocation, never edits.

## 7. Standards alignment

RFC 9943 (SCITT) · RFC 9942 (COSE receipts) · WEXP appraisal semantics · OpenBadge 3.0 VC ·
PQC path: ML-DSA-65 via liboqs (same body, swap primitive).

## 8. Security considerations

Signing-node custody (private key never leaves), the non-equivocation limit (inclusion is proven by the
receipt; non-equivocation requires consistency proofs + a monitor), and the 7-class conflict-of-interest
score are discussed.

## Authors' Addresses

Council of AI (CSOAI Ltd, UK #16939677) — contact via the estate trust root did:web:csoai.org.

---
**Submission path (one click when the account is there):** IETF datatracker → individual
Internet-Draft submission. Requires an IETF datatracker account (the only missing piece; the text is
complete above).
