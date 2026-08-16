# COUNCIL E2E AUDIT - 2026-08-16 (pod-side, Mac untouched)

## TEST BOARD (content-asserted, from RunPod 3090)
| Surface | HTTP | Verdict |
|---|---|---|
| csoai.org apex | 200 | RED: sovereign footer (FIXED branch) |
| llms.txt | 200 | RED: SOV33/sovereign/BFT-33 (FIXED branch) |
| SOV33_BFT33_COUNCIL.html | 200 | RED (FIXED branch) |
| sovereign-os.html | 200 | RED (FIXED branch) |
| gspc-scoreboard | 200 | RED: 13x sov6 cols (FIXED branch, now 0 locks, 248 signed) |
| gspc-index | 200 | YELLOW: SOVOS mention |
| councilof.ai apex | 200 | PASS |
| j-space | 200 | PASS (1,201 events live) |
| sov-space | 200 | YELLOW: SOV- prefix |
| meok.ai | 200 | YELLOW: sovereign footer |
| proofof.ai | 200 | YELLOW: 468B stub |
| mcp-install | 405 | RED: dead channel |
| csoai-site.pages.dev | 200 | RED: sovereign |

## FIXED THIS RUN (pushed branches)
1. f/breach-fix-apex-llms-20260816 (commit 6516663) — apex/llms/SOV33 stub/sovereign-os hygiene
2. f/scoreboard-public-names-20260816 (commit b16a93a4) — sov6-* -> public tuned labels, 0 lock-words, 248 signed cells

## E2E NEXT
- merge both branches -> deploy CF Pages (project csoai-site) from pod
- gspc-index/sov-space/meok.ai footer sweep
- proofof.ai rebuild-or-redirect decision
- mcp-install channel strip / repoint /api/*
- flagship GSPC into registry (io.github.CSOAI-ORG/gspc)

## DEPLOY (deploy lane, from pod with CF token):
git fetch origin
git checkout f/breach-fix-apex-llms-20260816   # merged head, 0 locks verified
git rebase origin/jv-wave8-production           # ensure clean against latest
python3 build_site.py                           # assemble _site
npx wrangler pages deploy _site --project-name csoai-site
# then verify live: curl csoai.org | grep -ci sovereign  -> 0
