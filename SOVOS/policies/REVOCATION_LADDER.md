# Revocation Ladder — deficiency → cure → suspension → revocation (v1, 2026-08-15)

Adapted from: NYSE continued-listing ladder + UL Variation Notice graduated
enforcement + FAA AD system. **Every step is public, machine-readable, and
appealable.**

## The ladder

| Stage | Trigger | Action | Timeline |
|---|---|---|---|
| **0 · Watch** | Drift detected, dispute filed, or anomaly report | `status: watch` on the card; public notice; no new cards in family | Immediate |
| **1 · Deficiency notice** | Material gap between card claim and re-measurement; failed continuing bar | Written deficiency notice (machine-readable), public in register | Within 5 business days of finding |
| **2 · Cure window** | Deficiency not contested | Published cure window with milestones (pattern: NYSE ~6-month cure) | Milestones checked monthly |
| **3 · Suspension** | Cure milestone missed OR contest fails | Family suspended; no issuance, no re-attestation; cards keep historical validity but show `superseded` | 30 days after miss |
| **4 · Revocation** | Fabrication proven / cure abandoned / no response | Card revoked — but **retained in the register, marked REVOKED, never deleted** (BrokerCheck pattern) | Decision + 14-day appeal window |
| **I · Immediate revocation** | Fabricated measurement (proven), collusion rings, key compromise | Immediate revocation bypassing the ladder; appeal preserved | Same-day, with published evidence |

## Codified immediate-revocation triggers (the NYSE $0.25 rule analog)

1. Proof the measurement was fabricated (no underlying run, tampered logs,
   algorithmically-inserted card data)
2. Proven coordinated fake-attestation ring
3. Signing-key compromise with un-revocable exposure
4. A card issued from the fallback/HMAC-stub path (never allowed — the
   `dev_stub` seam; published cards must never come from stub mode)

## Invariants

- **Deletion = destroying institutional evidence.** Revoked cards stay in the
  public register, marked revoked, with the revocation notice linked. Applies
  to the model register, index, and card lifecycle log.
- **Appeal preserved at every stage** (see DISPUTE_POLICY.md).
- **Surveillance is real**: drift between card claims and re-measured behavior
  is the trigger set; coordinated fake-attestation rings are detected by
  pattern (GNN-monoculture v0 operationalization).
- Every revocation is a **CVE-style citable ID** (`COAI-2026-NNNN`, signed)
  so corrections are reference-able.