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

## ⚠️ Two-key finding — reconcile before deploy (owner)
Wiring did:web surfaced that **the estate has more than one signing key.** The local Mac keystone
(`~/.sovos/city_ed25519`) signs with `8f9a…313912`; a lane had published `f4b4…c342` in `did.json`.
`bind_did` correctly **refused** to stamp the local card (its key wasn't the published one) — the
honesty guard working. Consequences:
- `make_did.py` now generates `did.json` from whatever keystone it runs on (single source of truth).
  The committed `did.json` is the **local-dev** key (`8f9a…`) so the demo/selftests are self-consistent.
- **Before hosting at csoai.org, regenerate `did.json` on the PRODUCTION keystone (the A100).** The
  published identity MUST equal the key that actually signs production cards, or verification fails.
- **Owner decision:** which key is the canonical CSOAI identity — the A100 key (`f4b4…`?) or another?
  All production signing must use that ONE key; the Mac dev key must never be the published identity.
  (Firewall: the private key lives only on the keystone — a dev Mac holding a signing key is itself
  worth reviewing.)
- Cards carry `signer_did` only when their key is the published one, so nothing falsely claims the
  identity in the meantime.

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
