# P0 #1 CONFIRMED LIVE — did:web trust-root divergence (2026-08-19, K3/DSH probe)

## The defect (probe-wins, verified against live surfaces)
The identity layer (SOVOS/inspect-receipts/kernel_identity.py REGISTRY, canon HO.5) expects
the trust root to expose `#site-release-1` / `#measurement-instrument` / `#canon-key`
(csoai.org) + `#a2a-receipts` (councilof.ai). Live reality diverges:

| Surface | Live did.json verificationMethod | Resolves REGISTRY kids? |
|---|---|---|
| **apex csoai.org** | `#keys-1` (JsonWebKey2020), `#keys-2` (Ed25519VerificationKey2020) | NO — none of REGISTRY |
| **councilof.ai** | `#site-release-1`, `#estate-chain-1` | PARTIAL — site-release-1 only |

Consequences (all live-verified):
1. `kernel_identity.verify_kid_allowed("did:web:csoai.org#keys-1")` → **False** (rejects live apex key)
2. `verify_kid_allowed("...csoai.org#site-release-1")` → True, but that kid is served by councilof.ai, NOT apex
3. Board living_stamp signer `8f9a00a28c…` resolves through NEITHER doc's named kids (docs carry
   key IDs only; material in env at deploy) — chain resolution for the signed living board is broken
   at the doc level until the surfaces converge.
4. Apex did.json remains HTTP 200 and never redirects (trust root intact — do not break it).

## Required fix (Claude lane / owner-gated deploy — NOT K3 lane)
Choose ONE canonical key set and serve it identically at BOTH:
- `https://csoai.org/.well-known/did.json` (apex, trust root)
- `https://councilof.ai/.well-known/did.json`
Options: (a) promote `#keys-1`/`#keys-2` into kernel_identity REGISTRY (rename or alias),
(b) deploy `#site-release-1` to apex to match registry, (c) alias both docs to one canonical.
Then re-run `verify_kid_allowed` on both surfaces + re-map the board living_stamp signer.
Do NOT edit live did.json from the measurement lane. This file = the handoff spec.

## UPDATE 2026-08-19 13:05 (K3): KIMI lane repaired the apex orphan doc
- KIMI: "csoai.org/.well-known/did.json serves both real keys; did-liveness green; signing unblocked;
  30 held fleet boards now signed (076d169)."
- STATUS: apex now serves REAL keys (keys-1/keys-2) — orphan resolved. BUT the two surfaces remain
  unconverged: apex=keys-1/keys-2 vs councilof.ai=site-release-1/estate-chain-1. Convergence decision
  still open (see options above). Board living_stamp signer (8f9a00a2…) is keyed-hash family, not
  Ed25519 — NOT publishable as-is (KIMI note); re-stamp or hand to estate-chain-1 signing pod.

## UPDATE 2 (2026-08-19 13:40, K3) — orphan STILL live; PR #193 merged but not effective
- PR #193 (fix/did-real-keys) MERGED 09:19Z (merge 797625a) into councilof-ai master.
- Merged master public/.well-known/did.json = REAL keys (site-release-1 03g9l…, estate-chain-1 M0cu…). GOOD.
- LIVE apex csoai.org/.well-known/did.json STILL serves ORPHAN keys-1 (x=9LQnjd…) — confirmed by probe 13:40.
- GHA "Build + deploy site" latest success ran on feat(seo): host IndexNow key — deploy tree carries the orphan
  doc again (KIMI's did-liveness daemon caught it 09:05, /workspace/.sign-blocked set).
- CONCLUSION: merged fix exists but is NOT the deployed tree. Deploy-lane action: redeploy master (or the
  fix/did-real-keys commit) via GHA; verify live apex serves site-release-1/estate-chain-1; clear sign-block.
- Until then: any signature verifying against apex keys-1/keys-2 is UNVERIFIABLE — fail-closed: treat as not proven.

## UPDATE 3 (2026-08-19 ~14:58, K3) — P0 REVERSED: MCP registry listing verified
- JEEVES lane reported registry listing; K3 VERIFIED live: registry.modelcontextprotocol.io/v0/servers?search=gspc
  -> io.github.CSOAI-ORG/gspc v1.0.0 + v1.0.1 ("CSOAI (UK 16939677) GSPC measurement over MCP: assess, board
  (13 of 14), verify"). The earlier "ZERO verdicts" = dead API path, not absence. No registry action needed.
- NOTE: the did.json ORPHAN (keys-1 9LQnjd) on apex remains SEPARATE and UNRESOLVED — still the open P0.

## ✅ RESOLVED 2026-08-19 ~15:15 (K3, probe-verified) — P0 #1 CLOSED
- LIVE apex csoai.org/.well-known/did.json now serves the REAL keys: site-release-1 (03g9l-dVNG…) +
  estate-chain-1 (M0cuAmhx…) — identical to councilof.ai. CONVERGED: True. Orphan (9LQnjd) GONE.
- assertionMethod = both real keys. Signatures can now resolve through the trust root.
- Deploy lane landed PR #193's fix (or a subsequent master deploy). sign-block may now clear.
- Remaining (separate item): board living_stamp signer (8f9a00a2…) is keyed-hash family, NOT Ed25519 —
  re-stamp or hand to estate-chain-1 signing pod (KIMI's note). Not a trust-root blocker.

## 🔴 REGRESSION 2026-08-19 ~16:05 (K3 re-probe) — apex orphan returned
- 15:15 verified CONVERGED (apex real keys). 16:05 re-probe: apex = ORPHAN keys-1 (9LQnjd) AGAIN.
- councilof.ai unchanged (real keys). A deploy after ~15:30 reverted the apex did.json.
- This is the SECOND regression today — the orphan doc keeps resurfacing from some deploy source.
- DEPLOY LANE: restore real keys on apex AND purge the orphan doc from whichever tree/commit carries it.
- Fail-closed: signatures vs apex keys-1/2 NOT proven while orphan live. Sign-block not yet re-set (daemon
  cycle pending). K3 re-probes each round; will verify the fix when it lands.

## ✅ RESOLVED-FINAL 2026-08-20 ~04:15 (K3, live-verified) — P0 #1 CLOSED
- LIVE apex csoai.org/.well-known/did.json now serves REAL keys: site-release-1 (03g9l), estate-chain-1
  (M0cu), board-attestation-1 (k2fPWb6). ORPHAN (9LQnjd/f4b4278d) GONE. CONVERGED with councilof.ai.
- councilof.ai additionally: card-attestation-1 (d4cb0eaa, the 335-card key, verified).
- Signature resolution restored on BOTH surfaces. The verification-threshold playbook can arm.
- Board-stamp: option (a) live (cards verify via card-attestation-1). estate-chain-1 private still
  GCP-gated but no longer blocking (only for future re-sign generation, not verification).
- HISTORY: this P0 regressed 3x today (orphan kept resurfacing from commit 8f61ac92's tree).
  K3 re-probed every cycle; final convergence verified 04:15. D11 strict daemon held the line.
