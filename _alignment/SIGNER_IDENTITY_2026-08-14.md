# Signer identity — status & the owner leg

**Goal:** make "verify without trusting us" fully, not half, true — an outside verifier resolves
*who signed* to a published, controllable identity, not the card's own word.

## Done in-lane (this session)
- ✅ **did:web identity root** — `.well-known/did.json` publishes the CSOAI signing key
  (`did:web:csoai.org`) in both JsonWebKey2020 (OKP/Ed25519) and Ed25519VerificationKey2020
  (multibase `z6Mkp7…`) forms.
- ✅ **Resolving verifier** — `verify_via_didweb.py` resolves the key from the DID document and
  checks a card's Ed25519 signature over its `content_id` **against the published key, not the
  card's `signer` field**. Proven: a real card verifies; a tampered signature fails; a foreign DID
  fails; the live-MCP demo card verifies too.
- **Trust model:** you trust that the domain `csoai.org` controls the DID (did:web's premise). You
  do **not** trust CSOAI's word about who signed. Ed25519 today — **ML-DSA-65 is roadmap, not
  present, not claimed.**

## ✅ Two-key question — RESOLVED (2026-08-14): `f4b4…` is canonical
Wiring did:web surfaced two signing keys in the estate. It is now settled:

- **Canonical production identity = `f4b4278d…c342`.** This is the key the committed
  `.well-known/did.json` publishes AND the key the pod/production signs with (cards, `cose_wrapper`,
  A2A, `underwriting_pack`). Published identity and production signer agree — verification holds.
- **`8f9a00a2…313912` is the Mac DEV key only.** It never gets published and correctly never
  resolves to the DID. `_resolve_signer_did`/`bind_did` refuse to stamp it (proven), so a dev-signed
  envelope honestly carries `signer_did: None` — nothing falsely claims the identity.
- **Every signed surface now stamps `signer_did` when it signs with the published key.** Wired at the
  choke point via `cose_wrapper._resolve_signer_did` (one place → MCP / A2A / underwriting envelopes)
  and via `verify_via_didweb.bind_did` for cards. On the pod (f4b4 signs = f4b4 published), every
  artifact carries `signer_did: did:web:csoai.org`.

**Operating rules (settled):**
- Sign production ONLY on the pod/keystone (key `f4b4…`). The Mac dev key must never sign a
  production artifact and must never be published.
- **Do NOT regenerate `did.json` off the production keystone.** `deploy_attest_and_did.sh` no longer
  auto-runs `make_did.py` (that would clobber `f4b4` with the Mac dev key); it publishes the committed
  `did.json`. To *deliberately* change the identity, run `make_did.py` on the production keystone,
  commit, then redeploy.
- Residual hygiene (minor, owner): a dev Mac holding any signing key is worth reviewing against the
  "private key lives only on the keystone" firewall — but it is dev-only and unpublished, so it is
  not a verification risk.

## Owner-gated — the two steps I cannot do
1. **Host the DID document** at `https://csoai.org/.well-known/did.json` (deploy). The file is
   built and committed; publishing it needs the Cloudflare deploy (token being rotated). Until it
   is reachable at that URL, `did:web:csoai.org` does not resolve for third parties.
   - Verify after deploy: `python3 verify_via_didweb.py --did https://csoai.org/.well-known/did.json --card <card>`
2. **C2PA-trust-list / CA recognition** (for the C2PA ecosystem specifically): submit the generator
   to the **C2PA Conformance Program** to obtain the conformance record ID, then the **SSL.com**
   free-tier Level-1 cert (requires the record ID first), then swap the chain into
   `c2pa_manifest.py`. Account creation + payment + credentials — owner only.

## What this changes
did:web closes **identity resolution** without a CA: a verifier can already confirm the signer is
the key `csoai.org` publishes. The C2PA/SSL.com step adds recognition **inside the C2PA ecosystem**
so a C2PA verifier reports the signer as a known, listed issuer. State it honestly: **"identity
resolves via did:web today; C2PA-ecosystem trust-list recognition is in progress."** Never claim
C2PA-listed until step 2 lands.
