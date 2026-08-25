# KEY CUSTODY PROVISIONING — OWNER ONE-PAGER (2026-08-25)
# Unblocks the "scale to real assets" gate. Both curves (XRPL Ed25519 + EVM secp256k1).
# Set CSOAI_KEY_CUSTODY=hsm; batch_signal_run.py --publish refuses until set (by design).

## Why
The attestation engine signs Ed25519 (signlib.js, already pinning did:web:csoai-gspc.pages.dev#gspc).
Scaling to publish verdicts on real RWAs on-chain needs AUTOMATED (no-human-in-the-loop) signing
across BOTH XRPL (Ed25519) and EVM (secp256k1). Custody must be non-exportable + audit-logged, and
key provenance must stay did:web-publishable so a stranger-verifier can tie an attestation to the setup.

## The two cleanest self-serve paths (from 2026-08-25 research)

### Option A — AWS KMS (cloud-native, FIPS, likely already-owned infra)
- BOTH curves now supported: secp256k1 (ECC_SECG_P256K1) + Ed25519/EdDSA (ECC_NIST_EDWARDS25519, added Nov 7 2025).
- Keys non-exportable, FIPS-validated. Caveats you handle in code: KMS signs a digest and returns
  DER-encoded signatures → do EIP-2 low-S normalization for EVM; handle Ed25519 RAW-vs-DIGEST message
  type; KMS caps signable message at 4KB (sign the digest). CloudHSM underneath for dedicated HSM.
- Setup: `aws kms create-key --key-spec ECC_NIST_EDWARDS25519` (XRPL) + `ECC_SECG_P256K1` (EVM);
  create aliases; put keys in a policy that whitelists only sign operations + specific callers.

### Option B — Turnkey (purpose-built policy engine + root quorum + per-signature economics)
- Both curves natively ("Secp256k1 and Ed25519"). Policy engine with DENY-wins evaluation; explicit
  "agentic wallets"/delegated-access pattern for programmatic server-side signing.
- Published pricing: 25 free sigs then $0.10/sig PAYG; Pro tier (~$99/mo per 2026 comparison) →
  "unlimited" down to ~$0.01/sig; enterprise ~$0.0015. ~100–150ms latency.

### Decide
- Choose KMS if you want cloud-native + minimal new vendor surface (and you're already on AWS).
- Choose Turnkey if you want a policy engine + root quorum + per-signature billing.
- Open-source/self-host MPC alternative (sovereignty upgrade later): Coinbase cb-mpc (MIT, both curves).
  Avoid ZenGo (archived), Silence Labs (proprietary non-commercial despite "permissive"), 0xCarbon
  (secp256k1-only). YubiHSM 2 = cheap hardware key isolation (both curves) if you want real HSM.

## Signing policy (enforce regardless of provider)
- Whitelist allowed transaction types/destinations; DENY-wins evaluation.
- Log every signature attempt with attribution (who/what/when).
- Keep a Shamir/Vault cold backup of recovery material — NEVER on the workstation.
- Publish key provenance via did:web (already wired on gspc).

## Set the gate after provisioning
```
export CSOAI_KEY_CUSTODY=hsm
# batch_signal_run.py --publish now proceeds; without it, refuses (honest, by design).
```

## Verify
- Sign a test digest on both curves, verify offline, confirm the public key matches did:web doc.
- Confirm an unauthorized caller is denied; confirm every sig attempt is in the audit log.

## NOTE — the honest reason this is owner-gated
I cannot provision AWS/Turnkey cloud credentials or hold real keys from here, and I will not fake an
`CSOAI_KEY_CUSTODY` variable (that would pretend custody is done when it isn't). The signing spine is
ready; the custody swap is the owner action. Threshold to change this recommendation: if a net-new
unsolicited/permissionless on-chain attester competitor appears → accelerate.
