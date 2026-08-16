# Database Right Assertions — CSOAI / Council for the Safety of AI (UK)

**Effective:** 2026-08-14
**Assertor:** Nicholas Templeman trading as CSOAI (Council for the Safety of AI), United Kingdom

Under the Copyright and Rights in Databases Regulations 1997 (SI 1997/3032), a sui generis
database right subsists automatically in a database where there has been a substantial
investment in obtaining, verifying, or presenting its contents. No registration is required;
the right vests in the maker. This document is the standing, dated assertion of that right
over the following CSOAI databases, and is itself timestamped in the estate's signed chain
(see OTS anchor references appended per update).

## Asserted databases

| Database | Contents (as of 2026-08-14) | Nature of substantial investment |
|---|---|---|
| **GSPC board results** (`board_v2` runs) | 15,580+ per-item measurement rows across 13+ axes × 22+ models, each row a graded, timestamped, transport-verified evaluation | Systematic verification: deterministic grading, canary exclusion, transport-failure separation, Wilson interval computation per model-axis |
| **GSPC gold banks** (gspc-* item banks, incl. DefBench v2, gspc-art5, gspc-care 200-item bank, SandboxEscapeBench extended 71-item bank) | Authored and rule-labeled evaluation items with paired/twin structure, held-out splits, and integrity assertions | Original authorship, statute-anchored labeling, exception-discrimination design, per-item integrity verification (`assert_gold`) |
| **corpus-watch drift corpus** | Daily-collected drift-attestation records (running since 2026-08) | Continuous daily collection, verification, and longitudinal structuring |
| **Signal index / verification records** | Signed measurement cards, inclusion proofs, and OTS-anchored time records | Chained, signed, and externally verifiable presentation of measurement contents |

## Terms

- The **structure** of these databases is asserted under database right; individual **content**
  items published under Apache-2.0 (the public gspc-* Hugging Face banks) remain Apache-2.0.
- **Held-out splits are trade secrets and are NOT published.** The anti-Goodhart
  held-out/visible split is the secrecy boundary; no public artifact contains held-out items.
- Wholesale extraction or re-utilisation of a substantial part of any asserted database,
  or repeated systematic extraction of insubstantial parts, is not licensed by this document.
- Verification of any individual record against https://csoai.org/verify is always permitted
  and encouraged — the instrument is checkable by design.

## Change log

- 2026-08-14 — Initial assertion (this document). OTS-stamped via the estate chain at issuance.
