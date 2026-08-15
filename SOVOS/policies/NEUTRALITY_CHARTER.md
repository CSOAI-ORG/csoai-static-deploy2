# Neutrality Charter (v1, 2026-08-15)

**The two firewalls, published as a versioned, institutional charter.**

Modelled on: BitSight co-authoring the "US Chamber of Commerce Principles for
Fair and Accurate Security Ratings" (institutionalizing the fairness rules of
its own category) + METR's independence firewall (refuses lab funding for the
models it evaluates) + rating-agency 17g-5 conflict engineering.

## Firewall 1 — rails, not certification

The Council provides **signing/measurement rails** so institutions sign
THEIR OWN frameworks with their OWN keys. We:

- ✅ Operate the methodology, the transparency service, and the audit function
- ✅ Issue "verified measurement credentials" (ISO CASCO vocabulary —
  measurement/attestation, never certification)
- ❌ NEVER certify, endorse, or approve any model, vendor, or framework
- ❌ NEVER accept referral fees tied to ratings, paid placement, or
  rating-for-listing reciprocity
- ❌ NEVER let a delegation grant become an original certificate (the FAA
  ODA analog: a self-signing institution attests conformance to OUR method,
  but cannot mint the method, confer standing, or alter the axes)

## Firewall 2 — analyse, never be the champion

We MAY analyse collected outcome data (including GNN cross-synthesis,
monoculture detection, correlated-failure analytics). We NEVER train and
ship a Council-owned champion model on the collected "honey."

- ✅ Analysis/synthesis of measurements (firewall 2 allows analysis)
- ❌ No model artifact derived from honey may be shipped or served
- ❌ MEOK stays architecturally separate; its data never becomes training
  data for a shipped champion
- Enforced in code: the dependency linter bans `meok → shippable-model`
  imports

## Structural independence

- Funding from measured parties is accepted ONLY when it does not affect
  methodology, thresholds, or publication (METR rule: independence is
  institutional identity)
- The auditor axis (CISO seat) always has veto over publication
- No analyst sits on the revenue side of re-attestation sales
- Key compromise / fallback-stub issuance is a same-day immediate revocation

## The refusal log (tamper-evident)

Every refusal — a partner asking us to certify, to build what we measure, to
endorse, to list-for-payment — is logged in a timestamped, signed, public
record. The refusals are part of the moat: by defining the fairness rules of
the category, we set the terms competitors must meet.

## Versioning

This charter is versioned and signed. A change without a signature does not
exist.