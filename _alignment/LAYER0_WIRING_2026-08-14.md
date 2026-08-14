# Layer-0 Wiring — 14 Aug 2026

## Status: Layer-0 NOW CONNECTED (was dark)

The estate's external verification spine is now LIVE on a free Cloudflare Worker,
re-homed off the billing-blocked Vercel endpoint.

**Verifier:** https://csoai-attest-verify.nicholastempleman.workers.dev
- `POST /verify` — POST any signed card -> `{valid, signer, content_id_matches, signature_valid}`
- No secret present — Ed25519 asymmetric verification, third-party verifiable without trusting us.
- E2E PROVEN: real card -> valid:true (sig `f4b4278d`, content_id `37a0104a...`);
  tampered card -> valid:false.

## The two findings that drove this

1. **The old verifier was HMAC (symmetric).** `meok-attestation-verify` used HMAC —
   its own docstring: "True offline verification requires asymmetric signatures, on
   the roadmap." It could NOT verify without the server's secret key. That is the
   old hash-theater class. Re-homing it would only have lit a fake-proof.

2. **The real verifier is Ed25519 (asymmetric).** The signed cards from
   `chain.py`/`card_issuer` carry `{body, signature, signer, content_id}` — fully
   externally verifiable. The Worker verifies: recompute canonical content_id from
   body -> Ed25519 verify(signature, content_id). JS canonicalization proven byte-
   identical to Python chain (recomputed == claimed on the real card).

## Estate inventory (the mining result — 14 Aug 2026)

- **612 GitHub repos** (CSOAI-ORG)
- **22 bridge-MCPs** (cobol, sap, as400, cics, iso8583, iso20022, edi, acord,
  hl7-fhir, scada, mqtt, fix, nacha, oracle, tax, sip...)
- **16+ real attestation MCPs** (governance-crosswalk 5,377 LOC, ai-bom, supply-chain
  attestation, firmware attestation, sovereign-signature, tee-attest, sigstore-cosign,
  x402 paywall/payment/coinbase, watermark-attest, ai-gateway, a2a-governance-bridge)
- **364 MCPs** with sign/verify/attest/x402 machinery
- **19 compliance MCPs** (governance pack)

## What this unblocks
The four attestation markets (PQC migration, AI-Act banking/insurance, AI liability
underwriting, agent-cards) all sell "signed, independently-verifiable measurement."
With the Worker live, every card now verifies externally. Layer-0 is no longer dark.

## Remaining blocking gaps (the map's conclusion)
1. **Correctness gate** — a wrong answer can still carry a clean receipt. (build)
2. ~~Externally-verifiable signer~~ **DONE** — this Worker is it.
3. **GSPC-as-A2A-skill** — the live measure-and-sign flow for agents. (build)
4. **Real timestamping** — "OTS Bitcoin proof" is charter-claimed but ~1 code ref. (aspirational)
