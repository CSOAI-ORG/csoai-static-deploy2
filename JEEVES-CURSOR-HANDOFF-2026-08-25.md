# CURSOR HANDOFF — Council OS (csoai-gspc) live state + next-push checklist
# Date: 2026-08-25 · JEEVES lane → Cursor. Everything below is LIVE and legit for Cursor
# to consume + rebrand/polish. Walls are binding (see §walls). Do not own-gated items.

## PULL
- Repo: CSOAI-ORG/csoai-static-deploy2, branch `aligned-front-20260817`.
- Latest commits to pull: `338d4b09` (First-Fine feed) · `pac4e902`/`bac4e902` (jail gate, measure-axis) · `a09a6409` (sign-replay fix, SDK+methodology) · `481b9605` (registers/receipts/agent-card+did fix).

## WHAT IS LIVE (stranger-verifiable from outside) — push/polish freely
- Hub /app/ Council OS SPA (index.html) — 24+ tabs, live.
- Signed endpoints (pinned did:web:csoai-gspc.pages.dev#gspc):
  sign · attest(chain mint) · underwrite(bond) · crosswalk(east-west) · agent · dataset · dvp · settle · sign-replay · signal · sov-signal · ingest · registers · measure-axis · first-fine · receipt/latest(honest UNPUBLISHED)
- did:web resolve: /.well-known/did.json (#gspc) + /.well-known/agent-card.json (A2A).
- Drop-ins: widget.js · csoai-cli.mjs (measure|route|axis|watch|sov-signal) · sdk.mjs (isValid→stranger-verify).
- Honest grammar: board renders `12 measured of 13 · jail UNTESTED` (API + frontend gated). measurement≠certification.

## WALLS (must hold in any Cursor polish — do not break)
- R8: regulators + anything ranked FREE forever, NEVER a 402. £0.05/verified-execution is COMMERCIAL rail only (insurers/bond desks/vendors buying DATA).
- R1/R3: scores never sold; no money with anything ranked.
- **ATTESTATION (the new load-bearing wall, 2026-08-25):** an attestation is an independent, verifiable OPINION/MEASUREMENT about an asset — it NEVER tokenizes that asset, NEVER confers ownership/claim rights, and is NOT itself a token. It rides ALONGSIDE an instrument. We licence attestation infra white-label ("powered-by", Chainalysis/Chainlink model); we NEVER mint or tokenize anyone's assets. Never describe an attestation as "tokenizing" or "granting rights" (EAS: attestations are explicitly not tokens/NFTs; XRPL credential has no effect until accepted + no ownership; SEC 2026-01-28 + Peirce 2025-07: tokenized securities are still securities). Q1 (white-label attestation licensing) = recommended lower-risk path; Q2 (tokenization-as-a-service) ONLY as tech/distribution partner of a REGULATED issuer (Tokeny/Securitize/Archax), not by minting ourselves.
- measurement ≠ certification (never "certified"); "12 measured of 13" (moves only when a signed card lands); jail UNTESTED.
- Never "every problem of every AI company" → say "systematic signed coverage of the public enforcement record".
- agents = model + harness; never "C2PA-certified/approved/partner" → "member of TWG + TF".
- JL.5: never claim traction without a signed stranger-checkable row. Honest zeros, UNPUBLISHED, LANE-REPORTED render honestly.

## OWNER-GATED (do NOT attempt from Cursor — flag, don't fake)
- SOVOS_CHAIN KV binding attach (namespace b4eb1252766040d68bf6b10e6470ab57) → chained:false→true. CONFIRMED: `wrangler pages` has NO KV command; it's a Cloudflare dashboard action. (Cloudflare Dashboard → csoai-gspc → Settings → Functions → KV namespace bindings → add `SOVOS_CHAIN` = b4eb1252766040d68bf6b10e6470ab57.)
- P0-1 estate DID (did:web:csoai.org) merge on csoai.org domain.
- Off-Mac fleet state (RunPod unreachable this cycle per overnight note) — lane-side.

## WHAT CURSOR CAN ADD (highest value, in-lane)
1. Rebrand/polish SPA (branding pass, consistent tokens, a11y) — live files are clean.
2. Wire the remaining dashboard panels to the signed feeds (Compliance→/api/first-fine, Enforcement→already, Train→scenario).
3. Push a "Verification" affordance: paste card → stranger-verify (already in renderVerify) — make it a first-class CTA.
4. Fill /press + /academy + /challenge with branded, signed, wall-compliant copy (Stage-42 grammar wall: "to a verified training-outcome record", not "to certification").
5. Rebuild deploy dir (see recipe at bottom) + deploy + test.

## DEPLOY RECIPE (recurrent — /tmp wipe is constant)
rebuild /tmp/gspc-hub (rm -rf; mkdir -p functions/api/receipts functions/sov-* functions/.well-known .well-known;
  cp app.html→index.html; cp .hub/estate-data.js, registers-data.json, estate-board.json, llms.txt, widget.js, csoai-cli.mjs, sdk.mjs + feed JSONs;
  cp functions/api/*.js + nested dirs; cat .well-known/did.json; cp functions/.well-known/agent-card.json.js; NO _redirects)
then `npx wrangler pages deploy /tmp/gspc-hub --project-name=csoai-gspc --branch main`.
Validate: `node --check` every function (import path: nested = '../signlib.js'), `python3 re.findall('<script>')`→/tmp/inline.js→node --check.
