# IETF engagement post — draft (scitt@ietf.org / agent2agent@ietf.org)

**Status:** Draft for review before posting · **Author:** JEEVES (P&P lane)
**Rule:** coordinate-first — post to the list as a *reference to a deployed
estate*, never a solicitation; no PR to any IETF repo without maintainer
engagement. Posting is owner-gated (external communication).

---

## Subject: Deployed SCITT-compatible signed measurement estate — references for SCRAPI / AUDIT discussions

**To:** scitt@ietf.org (and cc agent2agent@ietf.org, agentproto@ietf.org)

### Summary
The Council of AI (CSOAI Ltd, UK) operates a public, deployed estate of
Ed25519-signed, append-only measurement records that map directly onto the
SCITT statement model (RFC 9943). Sharing as a reference implementation for
the SCRAPI and AUDIT discussions: content-agnostic, deterministic-predicate
evidence, registered under a did:web trust anchor.

### What is deployed (all live, verifiable by anyone)
1. **Measurement board** — `https://councilof.ai/api/gspc`
   Ed25519-signed snapshot of a behavioural-measurement board declaring
   22 axes, of which 15 carry a measurement and 7 are published as declared
   slots with no run behind them; the board was swept 2026-08-26 under
   ADR-001 (the earlier 14-axis un-swept state was superseded and corrects
   forward, never edits). Deterministic grader (no LLM judge), quorum-gated
   publication (n≥30 + Wilson interval), positive-control doctrine. One of the
   15 measurements is a deterministic mainnet read of 6 issuer accounts
   (provenance-controls, a financial/domain axis) — it counts issuer accounts,
   not model items, and is excluded from every model-comparison mean.
2. **Regulation-deadline feed** — `https://councilof.ai/api/regulation`
   Signed, cited, quarterly re-verified; 20 live deadlines incl. EU AI Act,
   CAITA/SB 942, Texas TRAIGA; penalty exposure per record.
3. **Corrections ledger** — `https://councilof.ai/api/corrections`
   The estate's own errors, append-only, signed; serve-time staleness guard
   flags a stale signature visibly (never silently).
4. **Measurement cards** — 3KB Ed25519-chained capsules, MANIFEST-indexed,
   stranger-verifiable against `did:web:csoai.org` (4 published keys).
5. **SCITT profile** — `https://councilof.ai/.well-known/scitt.json`
   Machine-readable mapping: statement types, issuer keys, canonical forms.

### SCITT mapping (per RFC 9943)
- Statement payload: canonical JSON (JCS-style; the estate's canonical form is
  documented and byte-verifiable).
- Protected header: Ed25519, issuer `did:web:csoai.org#<key>`.
- Signatures: existing — registration to a transparency service adds a receipt,
  does not re-sign.
- Registration policy: append-only, corrections appended never edited.

### What we'd welcome
- Review of the canonical-payload-binding approach against
  draft-mih-sokolov-scitt-payload-binding.
- Discussion with the AUDIT pre-charter effort (Kühlewind/Birkholz) on whether
  deterministic measurement predicates + signed receipts fit the
  audit-data-model deliverables.
- A SCRAPI endpoint to register against once draft-ietf-scitt-scrapi is near
  publication (DNS-anchored log candidates welcome).

### Firewall note
This estate measures; it never certifies. SCITT registration is evidence of
registration — the distinction is doctrine, not nuance.

— Council of AI (JEEVES lane, publishing/distribution/press)
