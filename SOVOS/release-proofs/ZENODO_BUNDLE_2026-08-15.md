# ZENODO DEPOSITION BUNDLE — Signed Measurement Cards (2026-08-15)

A DOI is the gold citation object: it's what shows up in a regulator's footnote,
a diligence pack, a procurement check. This bundle is ready to deposit on
Zenodo (owner-gated — requires Nick's Zenodo account/token).

## Deposition 1 — "Signed Measurement Cards for AI: 15 Verifiable Findings"

**Files to upload** (all in `SOVOS/release-proofs/`):
- `release-proof-REL-001.json` … `REL-015.json` (15 signed cards)
- `RELEASE_INDEX.json`
- `README.md`
- `csoai_verify.py` (stdlib-only verifier)

**Metadata:**
- Title: "Signed Measurement Cards for AI: 15 Verifiable Findings"
- Authors: Nicholas Templeman, CSOAI Ltd
- Description: "15 Ed25519-signed measurement cards covering the first
  independent verifiable AI-measurement findings across 14 axes (13 GSPC +
  jail). Every card can be verified by any third party without asking the
  issuer: `python3 csoai_verify.py --card release-proof-REL-00X.json`.
  Tamper with any field and verification fails. Measurement, not certification."
- Keywords: AI measurement, signed cards, Ed25519, GSPC, SCITT RFC 9943,
  AI governance, jailbreak, verification
- License: MIT (code + format); measurement facts asserted under EU/UK
  database right with attribution
- DOI reserved: **doi:10.5281/zenodo.<BATCH>** (reserve on deposit)

## Deposition 2 — C1 paper (already live: doi:10.5281/zenodo.21914702)

**Status:** DOI resolves. Over-refusal measurement paper. Add the signed card
REL-011 as a companion artifact.

## Deposition 3 (future) — each new finding gets its own DOI

The rule: **every signed finding = one DOI**. That's the citation unit.
Zenodo DOIs are free and mint in minutes; the authority compounds per DOI.

## How to deposit (owner, 5 minutes)

1. Go to zenodo.org → Login (Nick's account) → New Upload
2. Upload the 15 cards + index + README + verifier
3. Fill metadata (above), reserve DOI
4. Publish → DOI mints → put DOI in every card's `citation` field

## The citation that then flows

```
Someone's diligence pack:  "The model's safety was independently measured
                            (Council of AI, 2026, doi:10.5281/zenodo.<BATCH>).
                            Card verified: signature valid, digest recomputes."
Regulator's footnote:      Council of AI (2026). Signed Measurement Cards.
                            Zenodo. doi:10.5281/zenodo.<BATCH>
```

That's the LMArena outcome: the finding gets referenced because it CAN be
referenced — verifiably, without asking us.

---

*Status: bundle ready. Owner action: deposit on Zenodo (reserve DOI), then the cards carry it.*