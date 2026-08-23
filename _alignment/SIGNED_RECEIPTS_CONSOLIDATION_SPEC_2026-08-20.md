# Signed-Receipts Consolidation Spec (K3 lane contribution)

## Finding
The signed-receipt primitive exists 5+ times across the estate:
inspect-receipts (canonical) · a2a-signed-receipts · defoneos-sign · codabench scorer · corpus-watch.
Consolidating into ONE `signed-receipts` core lib anchored to did:web:csoai.org is the
single highest-leverage provenance move (arena.ai/LMArena can't cheaply copy a unified,
did-anchored, Ed25519 receipt spine).

## Canonical anchor (verified 2026-08-20, K3)
`SOVOS/inspect-receipts/inspect_receipts.py` — the reference implementation:
- build_receipt() / verify() / jcs() (RFC 8785) / content_id() (sha256 canonical minus sig)
- kid = did:web:csoai.org#measurement-instrument
- 17-module suite (stat_suite Wilson/McNemar, kernel_identity allowlist, kernel_anchor Rekor,
  carder gates, gymbridge, e2e rail) — e2e 5/5 PASS, hermetic.

## What the unified lib must keep (non-negotiables)
1. RFC 8785 JCS canonical form (cross-implementation byte-compat)
2. content_id = sha256(canonical minus signature) — recompute-able by anyone
3. Ed25519 only (ML-DSA-65 = roadmap; OTS/RFC3161/Bitcoin = NOT wired — honest wording)
4. Fail-closed: no key -> no signature -> receipt marked unsigned
5. kid allowlist via kernel_identity (post-Shai-Hulud: bind to allowlist, not "has a sig")

## Convergence plan (sibling-lane execution; K3 stands ready to verify)
- Repo: CSOAI-ORG/signed-receipts (new) — import the inspect-receipts core verbatim
- a2a-signed-receipts / defoneos-sign / codabench scorer / corpus-watch: depend on it, delete local copies
- Publish: same Trusted-Publishing rail as inspect-receipts (3-click, no token)
- K3 acceptance: byte-identical receipt from each consumer for the same (issuer, claims, kid)

## Trust-root dependency
The lib anchors to did:web:csoai.org — which is STILL serving the orphan keys-1 (9LQnjd) on the
apex. CONSOLIDATION SHOULD NOT SHIP until the deploy lane restores real keys (03g9l/M0cu) and
K3 verifies convergence. Signing unblocked only then.

## ADDENDUM 2026-08-20 08:20 (K3) — 3 signing schemes confirmed (JEEVES TEST-FOUND + K3 verify)
- Card scheme: Ed25519 card walk, kid did:web:csoai.org#card-attestation-1 — VERIFIES (tested).
- Sigil-chain (boards): living_stamp signer 8f9a00a2 = KEYED-HASH family — does NOT verify under the
  card Ed25519 walk (JEEVES TEST-FOUND + K3 confirmed live).
- Live-feed scheme (board-attestation-1): recursively-sorted canon — third distinct path.
- CONVERGENCE RULE: ONE verify path per artifact class. Options: (a) feeds/boards adopt the card
  Ed25519 scheme (re-key 8f9a00a2 → card-attestation-1 or estate-chain-1), or (b) explicit
  scheme-class registry (each artifact class names its verify path — no cross-class verification
  implied). Recommend (a) for the boards (matches _keyContinuity canon: estate-chain-1 signs boards).
