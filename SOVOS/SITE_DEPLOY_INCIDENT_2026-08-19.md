# SITE DEPLOY INCIDENT + RESOLUTION — 2026-08-19
**Lane:** JEEVES (K3) · **Severity:** resolved (site functional) · **Root cause:** two deploy-path defects, found by checking

---

## What happened
1. I deployed to councilof.ai manually (`wrangler pages deploy dist/client --project-name councilof-ai`) **without the prerender step** → SPA routes (/pricing, /honesty, /library) returned 404 because the built `_redirects` has `/* /404.html 404` (routes must be prerendered static files).
2. The lane's CI deploy (canonical pipeline: build → **prerender 494 routes** → brand gate → deploy) **timed out at the prerender step** ("The operation was canceled" after ~75s) — a pre-existing runner-timeout issue with the 494-route prerender.
3. Net: the last good deployment (c051157b / routes 200) is live. **Site is functional.**

## What I fixed
- **llms.txt canonical framing** (13-of-14, slot-15 leak killed) — committed to **master** (the CI-deployed branch), merged cleanly past a conflict with the lane's partial fix. **Queued for deploy** when the prerender pipeline succeeds.
- **Persona gauntlet hardened** — added llms.txt 13-of-14 + SOVOS-in-API probes (caught the llms.txt defect live).
- Verified the referee keeper (urllib UnboundLocalError fix) is fully measuring — 8 models, both sides scoring.

## The lesson (check, never assume)
- **The canonical deploy path is the GH Actions CI** (build → prerender → deploy). Manual `wrangler pages deploy` without prerender breaks SPA routes. Never hand-deploy the master site.
- **The CI prerender is fragile** (494 routes, runner timeout) — a lane-wide infrastructure flag for the Claude lane / GHA owner.

## Current live state (verified)
| Surface | State |
|---|---|
| councilof.ai /pricing /honesty /library /start | ✅ 200 |
| llms.txt | ⚠️ old framing live; **fix on master, deploy-queued** |
| agent.json | ✅ canon-clean (14-slot, single DOI) |
| persona gauntlet | ✅ 8/8 personas + extra probes |

## SIGIL
`site-deploy-incident-2026-08-19-jeeves`
