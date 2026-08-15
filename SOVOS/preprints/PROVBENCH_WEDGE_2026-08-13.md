# Does an EU AI Act Article 50 provenance marking survive real-world transforms?
## ProvBench: 18 of 105 marking cells survive — measured, with intervals

**CSO AI Ltd (Council of AI)** · UK Company #16939677 · 13 August 2026
**Zenodo DOI:** [10.5281/zenodo.21755656](https://doi.org/10.5281/zenodo.21755656) · **Art. 50-anchored, not a general durability claim**

---

### 1. The measured number (the whole wedge in three figures)

> Across **105 cells** (15 genuine AI assets × 7 real-world transforms), only
> **18 provenance markings survived — 17.14%**, with a statistical-interval
> treatment. Binding type distribution tested: `hard_hash` (5), `metadata_xmp`
> (4), `soft_watermark` (3), **`cose_ml_dsa_65` post-quantum (3)**.
> Survival mostly collapses the moment a compliant file is re-encoded, cropped,
> resized, screenshotted, or re-hosted on a platform.

This is a **measurement**, not a normative claim. It says nothing yet about
whether survival is legally required in every case — European general courts
decide that, not us. It measures what actually happens to a mark under the
transforms real users apply.

---

### 2. Why now / why this is load-bearing

- **Article 50 of the EU AI Act has been in force since 2 August 2026.**
  Generators of AI output must mark it as AI-generated in a machine-readable,
  detectable, digitally signed, timestamped, tamper-evident way.
- **2 December 2026** is the grace-period end for marking *pre-existing*
  systems (Digital Omnibus, Reg. (EU) 2026/1744 timeline canon).
- The Commission has **conceded no single marking technique meets all four
  Art. 50(2) criteria** — so deployers must reason about marking that survives
  their actual pipeline. Nobody was measuring survival. This is that
  measurement.

### 3. Falsification / related work (cited honestly)

- **arXiv:2608.08129** (8 Aug 2026): 16 manipulation types across 6 generators
  show watermark removal and forgery at scale. Our survival measurement aligns
  with — and is *empirically* corroborated by — that independent falsification
  pass.
- **arXiv:2604.11720** (13 Apr 2026): removal & forgery achievable from a
  single reference image, no model access.
- **arXiv:2603.02378**: cryptographic validity ≠ semantic truth — C2PA-style
  metadata in isolation has failure modes.
- We make **no "first systematic measurement of credential survival" claim**
  — such a claim has been falsified by 2608.08129. We claim the narrower,
  citable, defensible thing: **an Art. 50-anchored durability item bank with
  intervals and law-mapped verdicts.**

### 4. Method (reproducible, one line of honest scope)

15 assets, 8 transforms (incl. identity) → 105 cells; each cell = did the
marking's verification logic still pass after the transform. Intervals:
Wilson-style on the survival rate (18/105 → ~11–25% at 95% by the clustered
approximation, `ci` width computed in the artifact). Binding
`cose_ml_dsa_65` exercises the post-quantum path — relevant because the
field's provenance layer is commonly ECDSA/Ed25519 (quantum-doomed on current
PQC timelines; **C2PA has no PQ signature profile**).

### 5. What this is NOT

- NOT an exploit. NOT a demand that any lab's marking changes. NOT a claim
  that low survival is "non-compliant."
- It is the missing empirical baseline: **if you deploy an Art. 50 pipeline,
  what fraction of your end-user transforms actually lose the mark — and which
  transforms, which bindings?**

### 6. The Article 50 Alternative-Means Evidence Pack (the offer)

Non-signatories and open-weights deployers owe "adequate alternative means"
evidence by 2 Dec 2026 — typically a **gap analysis against the Code of
Practice**. This benchmark is the durability-evidence engine behind that
analysis: the signed, interval-bounded, law-mapped survival record a deployer
can actually attach. Available on request (councilof.ai/article-50).

---
*Measurement not certification. Every figure in this preprint traces to a
signed, reproducible artifact (Zenodo DOI). Corrections to this preprint are
published as dated Delta Notes on the same DOI chain.*
