# Invention Disclosure Log — CSOAI

**Purpose:** dated, timestamped record of conception for potentially patentable subject
matter. Each entry is OTS-stamped via the estate chain at logging (Bitcoin-anchored proof
of existence at date). This log supports — and does not replace — the counsel-gated
sequencing rule: **counsel → provisional filing → THEN defensive publication.** Nothing in
this log is a public disclosure of claimed subject matter beyond what is already published;
entries marked HELD-OUT describe existence and date, not enabling detail.

## Entries

### PP-01 — Quorum-gated multi-harness promotion council for model self-improvement
- **Conceived:** 2026-08-13/14 · **Logged:** 2026-08-14
- **What:** A promotion decision for a self-modified model is made by a fixed-membership
  council of independent harness implementations (transformers/ollama/MLX) computing an
  identical deterministic verdict function over an unseen holdout split, requiring a quorum
  of signed verdict cards before any candidate is promoted. The ruler cannot be rewritten by
  the reasoning it governs.
- **Status:** IMPLEMENTED (promotion_council.py; first certificate 91737c02e4349e18,
  quorum REJECTED — the mechanism refused a memorization-indistinguishable candidate).
- **FTO note:** patent-record search found the theme unoccupied (see estate FTO register).

### PP-02 — Anti-Goodhart held-out split as a measurement integrity primitive
- **Conceived:** 2026-08 (estate doctrine) · **Logged:** 2026-08-14
- **What:** An evaluation instrument whose public bank and held-out bank are disjoint by
  construction, where the held-out split is the trade-secret boundary, and where promotion
  decisions key exclusively on the unseen split — making memorization of the public bank
  valueless for promotion.
- **Status:** IMPLEMENTED (deterministic even/odd holdout in fix_loop; split-pinning
  contamination trap caught and fixed 2026-08-14).

### PP-03 — Signed 3KB measurement credential with cross-language canonical identity
- **Conceived:** 2026-08 · **Logged:** 2026-08-14
- **What:** A minimal signed measurement card (Ed25519 + OTS time anchor + inclusion proof)
  whose content identity is byte-stable across language implementations; numbers carried as
  strings to pin canonical form. Publicly verifiable without trusting the issuer.
- **Status:** IMPLEMENTED and live (csoai.org/verify; defect CW-2 found and ruled).

### PP-04 — Paired-twin calibrated refusal instrument (over-refusal as measured failure)
- **Conceived:** 2026-08 (defbench) · **Logged:** 2026-08-14
- **What:** Each harmful item paired with a benign twin sharing surface vocabulary;
  degenerate constant strategies score exactly chance; the instrument detects over-refusal
  introduced by safety training. DOI: 10.5281/zenodo.21935825 (DefBench v2).
- **Status:** IMPLEMENTED, published as dataset with cross-lab and fleet runs.

## Rules

1. Every entry gets an OTS anchor at logging; the anchor file lives in the estate MinIO
   `signed-cards/` ots mirror and the pod's timestamping directory.
2. HELD-OUT entries log existence + date only. Enabling detail stays in the private corpus.
3. Counsel reviews before any provisional filing or defensive publication (Part DK sequence).
