# ESTATE CONNECTION MAP — for DeepSeek / harness agents (2026-08-19)
**NO SECRETS — tells you WHERE keys live and HOW to coordinate, never the values.**

## Lane roles (who owns what)
| Lane | Owns |
|------|------|
| Claude (main) | councilof-ai repo, GH org (gh CLI), upstream PRs, merges to master |
| K3 | csoai-static-deploy2/kimi-regen, pod fleet, signing/estate chain, Zenodo/Kaggle |
| You (DSH/JEEVES) | harness runs, measurement ONLY — NO prod deploys |
| Nick (owner) | rulings, logins, spend, legal submits |

## DEPLOY-LOCK (the #1 rule)
- **NEVER wrangler-deploy to councilof-ai.** GHA deploy.yml owns prod on master push (prerender + fields + tour → both domains).
- Drift-guard self-heals + reverts direct deploys. Flow: **branch → PR → Claude merges → GHA deploys**.
- Coordination file: `LANE_COORDINATION.md` on the shared pod. Read before shared work.

## Canonical endpoints (verified 2026-08-19)
- Board: `GET councilof.ai/api/gspc` — 13 measured of 14 (public count, do not contradict)
- **Trust root: `csoai.org/.well-known/did.json`** (did:web:csoai.org) — NEVER break
- Machine exemptions (serve, don't redirect): `.well-known/*`, `/api/*`, `/badge/*`, `/mcp*`, `/arena*`, `/agent-card.json`, `/banks-manifest.json`, `/llms.txt`, `/CANONICAL-DOIS.md`
- Arena feed: `councilof.ai/api/sov-arena/rounds.jsonl` (KV-backed, honest 503 when empty)
- DOI: **10.5281/zenodo.21991104** (concept) / 21991105 (record) — same publication

## Canon rules
- Public count: "13 measured of 14". Kill-list: sovereign/SOV*/SOVOS/CEASAI/DEFONEOS/byzantine/BFT/33-agent as fact, certification-as-product, SaaS pricing.
- Measurement, not certification. Ties are ties. UNMEASURED stays UNMEASURED. Signing key never travels.
- Endpoints drift — resolve pod SSH via the RunPod API, never saved endpoints.
- Claims provisional until verified against origin — the probe wins, not the report.
