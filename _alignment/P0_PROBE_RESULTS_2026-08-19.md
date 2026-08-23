# P0 PROBE VERIFICATION — 19 Aug 2026 ~11:50 (K3, probe-wins)
| # | Fix | Status |
|---|---|---|
| 1 | site-release-1 in DID doc / re-sign | 🔴 ABSENT (live: keys-1/keys-2) — verify intended vs re-sign path |
| 2 | councilof.ai machine-path routing | 🟢 200 (gspc, agent.json, badge/) |
| 3 | /verify on csoai.org | 🟢 200 |
| 4 | api-catalog → openapi.json | 🟢 200 both |
| 5 | /mcp initialize 500 | 🔴 **500 confirmed** (initialize POST) |
| 6 | /api/badge both domains | 🔴 csoai.org 404 (councilof.ai 200) |

Handoff: these feed Claude lane's scheduled P0 queue. Re-probe after their next deploy.
