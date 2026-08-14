# Two lane claims — verified 2026-08-14

## Claim 1 — "External verifier is LIVE (Cloudflare Worker), byte-identical canonicalization"
**Verdict: CODE REAL · "LIVE" NOT CONFIRMED (appears false at csoai.org) · byte-identical UNTESTED.**

- ✅ The verifier **code is real and correct**: `workers/attest-verify/src/worker.js` does genuine
  WebCrypto Ed25519 verification (`crypto.subtle.importKey`/`verify`), canonical JSON stringify
  (sorted keys, no spaces), needs no secret; endpoints `POST /verify`, `GET /pubkey`. wrangler
  `name = "csoai-attest-verify"`.
- ❌ **Not reachable at csoai.org.** `GET /pubkey` returns **200 but serves the SPA homepage HTML**,
  not a pubkey; `POST /verify` returns empty; `csoai-attest-verify.workers.dev` = 000. The site's
  catch-all shadows the worker — it is **not deployed/routed live** where claimed.
- ❌ **"byte-identical to Python" has no test** in the repo, and could not be empirically confirmed
  because the live worker isn't reachable.
- **Action:** the worker is built but must actually be **deployed and routed** (CF-token-gated —
  same rotation blocker). Until then, say *"the external verifier is built; deployment pending"* —
  **not** "the verifier is live." Also: it verifies the card's self-reported pubkey; pair it with
  did:web so identity is checked against the published key, and resolve the two-key issue first.

## Claim 2 — "EU high-risk clock slipped to 2 Dec 2027 (Digital Omnibus, Reg 2026/1744)"
**Verdict: CONFIRMED.**

- **Regulation (EU) 2026/1744** ("Digital Omnibus on AI") — published in the OJ **24 Jul 2026**, in
  force **27 Jul 2026**.
- **Standalone high-risk (Annex III) obligations deferred from 2 Aug 2026 → 2 Dec 2027**; AI embedded
  in Annex I products → 2 Aug 2028.
- **Unchanged (still on original timeline):** Article 50 transparency / AI-content-marking (2 Aug
  2026), GPAI provider obligations (since Aug 2025), Article 5 prohibited practices (since Feb 2025).
- **Action:** Diamond 2 (EU high-risk credit/insurance) has a **longer runway (Dec 2027) — do not
  lead with it.** The **near-term EU hook is Article 50 marking (2 Aug 2026)**, which did NOT slip —
  that's where `meok-watermark-attest` + `oscal_article50` point. Update any deck that still says
  "high-risk bites Aug 2026."

Sources: Cooley, Gibson Dunn, DLA Piper, Pinsent Masons, CSA, aiactblog.nl (Digital Omnibus / Reg (EU) 2026/1744 coverage, Jul 2026).
