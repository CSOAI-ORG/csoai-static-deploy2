# OTS Overclaim — bulk fix task (deploy lane; JEEVES wrangler flow)

## Verified state (K3, 2026-08-20 03:10 UTC)
- **CANONICAL (councilof-ai monorepo client/): FIXED** — 3 surfaces honest, committed 90a8cd6
  on `fix/ots-honest-wording-20260820` (index.html JSON-LD, chain.ts, Methodology.tsx).
  Deploy lane: PR + merge (Vercel csoai-v2-app auto-deploys).
- **LEGACY STATIC (csoai-static-deploy2 _site/): 16 LIVE pages** (all HTTP 200 on www.csoai.org)
  carry OTS/Bitcoin overclaims. Full list in repo: `grep -rl OpenTimestamps _site/*.html`.
  These deploy via `wrangler pages deploy _site --project-name csoai-site`.

## Fix wording (replace per occurrence, matching context)
- "anchored with OpenTimestamps" / "via OpenTimestamps" / "OTS (OpenTimestamps) anchoring"
  → "SHA-256 hash-chained with Ed25519 signatures (OpenTimestamps anchoring on the roadmap)"
- "Bitcoin-anchored" / "Bitcoin block" → "hash-chained (Bitcoin/OTS anchoring on the roadmap)"
- Never delete the surrounding sentence — only soften the anchor claim.

## Why it matters
Catching your own overclaim is the moat: an instrument that says honestly what is and
isn't wired is the one regulators and insurers can rely on. ~17 claims total (3 fixed,
16 pending legacy + any deep pages not in _site).

## Do NOT
- Do not touch _quarantine/ (0 hits anyway).
- Do not invent OTS attestations — the roadmap is the honest statement.
