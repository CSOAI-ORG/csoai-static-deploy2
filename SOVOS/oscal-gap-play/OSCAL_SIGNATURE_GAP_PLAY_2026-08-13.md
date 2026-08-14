# OSCAL Signature-Gap Play — FedRAMP RFC-0024, 30 Sep 2026
**CSO AI Ltd (Council of AI)** · UK #16939677 · Built 13 Aug 2026
**Play 5** · Buyer: cloud service providers under FedRAMP + the documented
cryptographic-signature gap in OSCAL tooling.

---

## 1. The mandate (REAL, verified)
- **FedRAMP RFC-0024** (released 13 Jan 2026) requires machine-readable
  OSA/**OSCAL** packages from **ALL** FedRAMP providers (not just 20x
  participants).
- **Initial deadline: 30 Sep 2026.** Final: 30 Sep 2027. Miss = possible loss
  of certification.
- **A public comment (FedRAMP/community GitHub Discussion #114)** flagged the
  load-bearing gap: **"OSCAL does not mandate cryptographic signatures"** — an
  evidence-authenticity hole between the machine-readable package and the
  fact that it wasn't tampered with.

## 2. The gap → the play (verified)
| Side | State |
|---|---|
| OSCAL mandate | REAL — providers must ship machine-readable packages by 30 Sep 2026 |
| OSCAL signature hole | REAL — community-acknowledged; OSCAL alone doesn't anchor authenticity |
| **CSO AI's stack** | REAL — `sovos-oscal` emits **OSCAL v1.1.0 assessment-results** + **Ed25519 signed receipts** (`cose_ml_dsa_65` PQ path) |
| **The play** | Fill the documented gap: **OSCAL package + Ed25519 authenticity receipt**, verifiable, machine-readable, chain-anchored |

## 3. Why this converts (differentiators, each REAL)
1. **We already emit OSCAL v1.1.0** — no build needed, alignment verified.
2. **We already sign** — Ed25519 (and the PQ `cose_ml_dsa_65` path) closes
   exactly the GitHub-#114 gap the community named.
3. **1-2 weeks to productize** (the report's estimate): wrap
   oscal-export + Ed25519 receipt into a verifier a CSP can drop into its
   CI/release pipeline.
4. **The gap is dated** — 30 Sep 2026 is a hard clock; providers under RFC-0024
   need the tamper-evident answer *before* the deadline, not after.

## 4. Build status
| Asset | Status |
|---|---|
| OSCAL v1.1.0 export (`sovos-oscal`) | ✅ REAL |
| Ed25519 signed receipts | ✅ REAL (sovos-certification-loop / council) |
| PQ `cose_ml_dsa_65` binding | ✅ REAL (ProvBench artifact) |
| **Verifier product (package + receipt)** | 🟡 lane-buildable (~1-2 wks) — next builder move |
| **Buyer outreach (CSPs, FedRAMP GIS)** | 🔒 OWNER — external comms |

## 5. Honesty register
- **REAL:** mandate, deadline, GitHub-#114 gap, our OSCAL + Ed25519 + PQ stack,
  the 1-2 wk build estimate (from research pass).
- **THEORY:** buyer conversion (that providers will buy an authenticity layer —
  demand inferred from the mandate + named gap, not booked).
- Claim scope: "we close the FedRAMP OSCAL signature gap" is factual about the
  stack; "we are FedRAMP certified" is NOT claimed — certification authority
  stays with FedRAMP.
