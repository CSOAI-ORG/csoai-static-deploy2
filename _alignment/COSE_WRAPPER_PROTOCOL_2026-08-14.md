# COSE Signing-Wrapper Protocol — the signing layer the MCP economy doesn't have

**Date:** 2026-08-14 · **Status:** Phase 2 LIVE · **Owner:** JEEVES in-lane

## The gap it closes
Anthropic Economic Index, OECD AI, Stanford HAI all opened data via APIs/MCP —
**callable but not verifiable.** No cryptographic proof of when a number was
generated, what version, whether drifted or tampered. The regulated economy
(banks, insurers, ministries) cannot formally rely on unsigned index flows.

## The envelope (Phase 2 — LIVE, verified)
`cose_wrapper.py` wraps ANY MCP/index/tool output:

```json
{
  "envelope": "csoai-cose-sign1", "version": "1",
  "protected": { "alg": "EdDSA", "kid": "ed25519:<pub16>", "typ": "sov-measurement" },
  "payload":   { "source": "...", "observed_at": "...", "data": <output> },
  "signature": "<Ed25519 over canonical(protected|payload)>",
  "content_id": "<sha256 of canonical payload>",
  "signer_pubkey": "<full Ed25519 pubkey — required for external verify>",
  "time_anchor": { "state": "calendar_commit", ... }
}
```

**Proven live on the pod (2026-08-14):**
- wrap anthropic-economic-index output → signed, `calendar_commit` anchor, 1,181 bytes
- verify real envelope → `valid: True`, signer `ed25519:f4b4278d`
- verify tampered payload → `valid: False`
- selftest 6/6

**Pushed to MinIO:** `sovos:signed-cards/mcp/anthropic-economic-index-20260814.json`
(signed-cards bucket: 3 objects — 2 GSPC cards + 1 MCP envelope)

## The honest register (phases — no overclaim)
| Phase | Capability | Status |
|---|---|---|
| **2** | Ed25519 COSE_Sign1-shaped envelope over any MCP output + OTS anchor | ✅ **LIVE** |
| **3a** | did:web identity binding | 🔴 owner-gated (domain/identity decision) |
| **3b** | SCITT transparency-log receipt | 🔴 owner-gated (infra) |
| **3c** | Real ML-DSA-65 (FIPS 204) signing (not the benchmark test-cell) | 🔴 owner-gated (key mgmt) |

**Pitch discipline:** say "the COSE wrapper is live" (true) — NOT "we already bind
did:web / SCITT / ML-DSA signing" (aspirational). Same affect-class breach guard.

## Wiring the J-Space index
Three J-Spaces (adoption / policy / behaviour) → each output wrapped by
`cose_wrapper.wrap()` → signed + anchored → Procrustes alignment computes the
governance-gap distance → one weekly index number. The crosswalk engine
(`governance.db`, 5,377 LOC) is already the policy↔behaviour bridge; J-Space one
(adoption) wires via the same wrap.

## Files
- `SOVOS/packages/sovos-city/src/sovos_city/cose_wrapper.py` — the wrapper
- `SOVOS/packages/sovos-city/src/sovos_city/timestamping.py` — OTS anchor
- `SOVOS/packages/sovos-city/src/sovos_city/correctness_gate.py` — pre-sign gate
- Live verifier: `https://csoai-attest-verify.nicholastempleman.workers.dev/verify`
