# VERIFY — how to check any Council of AI signed card

Every signed card is verifiable by anyone, without asking us. Four independent
checks, stdlib-only. **The verifiability is the distribution.**

## 1. Verify the card (digest + signature) — stdlib-only, no pip

```bash
python3 csoai_verify.py --card release-proof-REL-001.json
# ✅ VALID — digest recomputes, signature well-formed

# Tamper with any field and it fails with a reason
python3 csoai_verify.py --card tampered.json
# ❌ digest MISMATCH — recomputed ... != card ... (tampered or wrong key)
```

## 2. Verify in the browser (no tools at all)

Open https://csoai.org/releases — every card has a ✓ Verify button that runs
the recompute client-side. Nothing leaves your browser.

## 3. Verify the time anchor (OpenTimestamps)

The cards' `.ots` proofs attest when the card existed, committed to the
Bitcoin blockchain — independent of any server:

```bash
ots verify release-proof-REL-001.json.ots
# Success! Bitcoin block NNNNNN attests ...
```

## 4. Verify the transparency-log entry (Rekor/SCITT)

The signed statements are registered to the public transparency log:

```bash
rekor-cli verify --artifact release-proof-REL-001.json \
  --signature release-proof-REL-001.json.sig \
  --public-key keys/csoai-ed25519.pub
```

## Why this matters

A signed, anchored card is self-referencing: anyone who finds it can verify it
without asking us. Citation accrues because the card is *signed*, not because
it is advertised. That's how authority compounds — a regulator's footnote, a
buyer's diligence, a researcher's citation all point at a card that checks
itself.

## Firewall

Measurement, not certification. These cards report what was measured with a
signature. They do not certify or endorse any model, vendor, or framework.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21914702.svg)](https://doi.org/10.5281/zenodo.21914702)