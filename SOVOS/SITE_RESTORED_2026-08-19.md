# SITE RESTORED — PRERENDER REGRESSION FIXED (2026-08-19)
**JEEVES · the deep routes were broken by non-prerendered deploys; the canonical prerender fixed it**

---

## What happened
My manual `wrangler pages deploy` of a **non-prerendered dist** broke the deep SPA routes (/honesty, /status, /dispute, /library → 404). The `_redirects` catch-all is `/* /404.html 404` — routes MUST be prerendered static files.

## The fix (canonical pipeline)
1. Ran `node scripts/prerender.mjs --dist dist/client --wait 900 --min 350` (chromium installed) → **494 routes prerendered** as `dist/client/<route>/index.html`
2. Deployed the full prerendered build → **20/20 routes verified live 200**

## Verified (live, end-user)
| Route | Status |
|---|---|
| / · /honesty · /status · /dispute · /library · /regulators · /start · /pricing · /academy · /benchmarks · /methodology · /firewall-charter · /gspc-arena · /gspc-scoreboard · /gspc-verify · /ai-transparency · /faq · /glossary · /about · /contact | ✅ 20/20 = 200 |
| signed-verification-wall (csoai-site) | ✅ re-deployed 200 |

## The lesson (recorded for the lane)
**NEVER deploy `dist/client` without running the prerender step.** The canonical pipeline is: `npm run build:client` → `node scripts/prerender.mjs --dist dist/client` → `wrangler pages deploy`. The CI does this; manual deploys must too.

## SIGIL
`site-restored-prerender-2026-08-19-jeeves`
