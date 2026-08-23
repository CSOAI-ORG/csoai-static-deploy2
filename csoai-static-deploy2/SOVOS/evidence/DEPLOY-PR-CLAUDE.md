# PR — Publish CSOAI verified-measurement evidence (ready for Claude→GHA)

## Title
`publish: verified-measurement evidence (verify page + signed artifacts)`

## Why
CSOAI now has the first stranger-verifiable measurement results in the industry — every score is
Ed25519-signed on a signing node (key never leaves), verifiable in-browser (WebCrypto) or with one
command. This is the credibility engine for the measurement-body GTM. Deploy it live.

## Files to add (all attestable)
- `SOVOS/evidence/verify.html` — self-contained, browser-verifiable (WebCrypto) page; embeds the signed
  evidence-index + pubkey.
- `SOVOS/evidence/signed/*.json` — **15 Ed25519-signed verdicts** + `evidence-index.json` (attests all 15).
- `SOVOS/evidence/verify_signature.py` — portable verifier (`pip install cryptography`).
- `SOVOS/evidence/VERIFY-NOTE-2026-08-22.md` — verification instructions.
- `SOVOS/PUBLICATION-KIT-2026-08-22.md` — the mass-growth launch copy + arXiv abstract.

## The public verification key (publish on the page)
`bWbk52E47J6EkY4+pu0Hh/B1l1175AZoZsDEBr0EfWA=`

## What the evidence attests (all verified VALID + hash-matched)
- Clean sequential measurement (3090): mistral:7b 67.3 / llama3:8b 66.6 / qwen2.5:7b 63.3 / 1.5b 60.5 (RAG).
- Retrieved knowledge > trained (+34–38 pts). Base > our fine-tunes at same size (design, not size).
- Registry (10 instruments), master stack, full rundown, 100-step plan, machine-truth manifest.

## Deploy (after merge)
`wrangler pages deploy` to `councilof.ai` (or push to the site repo → GHA). Publish the pubkey in the
page. Link `/verify` from the home surface. Let `verify.html` resolve on `councilof.ai/verify`.

## Verify (acceptance)
1. `https://councilof.ai/verify` loads + shows **"Evidence index — VALID"** in-browser.
2. `python3 verify_signature.py signed/evidence-index.json` → **VALID**.
3. Tampering the JSON → **INVALID**.

## Discipline (binds)
- Measurement, not certification. Never take money from the scored.
- The Ed25519 **private key never left the signing node** (oracle-micro1); only pubkey + artifacts published.
