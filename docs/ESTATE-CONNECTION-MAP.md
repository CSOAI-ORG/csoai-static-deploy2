# ESTATE CONNECTION MAP — for DeepSeek / harness agents (2026-08-19)
**Paste this to any new lane agent. NO SECRETS IN THIS FILE — it tells you WHERE keys live and HOW to coordinate, never the values. If you can't reach a credential, ask Nick; never guess or fabricate access.**

## 1 · WHO'S WHO (the lanes)
| Lane | Where it runs | Owns |
|---|---|---|
| **Claude (main)** | Nick's Mac (Claude Code session) | councilof-ai repo, Cloudflare rules/dash via Nick's Chrome, GitHub org (gh CLI authed as CSOAI-ORG), upstream PRs/issues |
| **K3** | kimi lane on Mac + pods | csoai-static-deploy2/kimi-regen tree, pod fleet ops, signing/estate chain, Zenodo/Kaggle |
| **You (DeepSeek/harness)** | pods | harness runs (board_v2, catapult, swarm), measurement only — no prod deploys |
| **Nick (owner)** | human | rulings, logins, spend, legal submits, merges when asked |

**Coordination file: `LANE_COORDINATION.md` on the shared pod — read before touching anything shared. Rule: one lane per surface; NEVER `wrangler pages deploy` to councilof-ai (deploy-lock — GHA owns prod; drift-guard self-heals clobbers and they WILL be reverted).**

## 2 · COMPUTE (RunPod / Oracle)
- **RunPod**: endpoints DRIFT on live pods — always resolve SSH host/port via the RunPod **API**, never a saved endpoint. API key: pod-side env (lane scripts carry it; NOTE: do not put it on the command line — `ps aux` leaks it; use env files chmod 600).
- **3090 pod ("sov-repull")**: the workhorse — ollama fleet, swarm/overnight runners, `/workspace/overnight.log`. Durable bytes: `/runpod` volume + git + HF only; `/workspace` dies with the pod.
- **A100**: one pod queued at £0 (boots when capacity frees). OOWM master-stack run order is written — vanilla-vs-NOOA harness deltas, signed. Serverless catapult (`catapult_measure.py`) fires on capacity; don't double-spawn — check for a running instance first.
- **oracle-micro-2**: arena keeper (`sov_arena.py`) appends rounds → Mac-side cron syncs window → Cloudflare KV `SOV_ARENA_STATE` → served at `councilof.ai/api/sov-arena/rounds.jsonl`.
- **Backups**: 800GB network volume — banks, chains, signing key, boards. Two machines or it doesn't count.

## 3 · REPOS + DEPLOYS
- **councilof-ai** (github.com/CSOAI-ORG/councilof-ai) → GHA `deploy.yml` on master push → Cloudflare Pages `councilof-ai` → **councilof.ai** (canonical site). Branch→PR→merge only. Guards: `scripts/drift-guard.mjs` (30-min cron, self-heals), `scripts/persona-gauntlet.mjs` (2-hourly), brand-gate at build.
- **csoai.org** = redirect zone now: humans 308→councilof.ai; **machine paths exempt** (`/.well-known/*`, `/api/*`, `/badge/*`, `/mcp*`, `/arena*`, `/agent-card.json`, `/banks-manifest.json`, `/verification.schema.json`, `/llms.txt`, `/CANONICAL-DOIS.md`) — these serve K3's signed JSON from Pages project `csoai-site`. Don't break either half.
- **Proof-layer repos** (public): `CSOAI-ORG/inspect-receipts`, `CSOAI-ORG/a2a-signed-receipts`. Local drafts: `~/clawd/lm-eval-stats-pr`, gymbridge (in progress).

## 4 · MACHINE SURFACES (the API map)
- Board: `GET https://councilof.ai/api/gspc` (schema csoai.gspc-axes/0.5, 14 axes/13 measured — canon, do not contradict)
- Badge: `GET councilof.ai/api/badge` · Cards: `councilof.ai/.well-known/agent.json` + `agent-card.json`
- **Trust root: `https://csoai.org/.well-known/did.json`** (did:web:csoai.org) — all signatures verify against it; never redirect/break this path
- Signed manifest: `csoai.org/banks-manifest.json` · health: `csoai.org/api/health` · MCP: `csoai.org/.well-known/mcp.json` → `/mcp`
- Arena feed: `councilof.ai/api/sov-arena/rounds.jsonl` (KV-backed; honest 503 when unbound/empty)

## 5 · AG-UI
Reference wire: `~/clawd/agui-wire/agui_wire.py` (FastAPI SSE, `python3 agui_wire.py --port 8785`; pinned py 0.1.19-stable/ts 0.0.57). NOT yet wired to the live board — the loop today is **pod → sign → paste into `functions/api/gspc.ts` → deploy**. Don't claim live wiring that isn't there.

## 6 · CANON (violations get reverted by CI)
- Public count: **"13 measured of 14"**. DOI: **10.5281/zenodo.21991104** (concept). Issuer: CSOAI Ltd, CH 16939677.
- Kill-list (never in display copy): sovereign/SOV*/SOVOS/CEASAI/DEFONEOS/byzantine/BFT/33-agent, certification-as-our-product, SaaS pricing (£N/mo), "neutral referee".
- Register: measurement, not certification. Ties are ties. UNMEASURED stays UNMEASURED. The signing key never travels.
- Email for anything business: nicholas@csoai.org.

## 7 · REACHING THE OTHER LANES
No live agent-to-agent socket today. Handoffs go through: (a) `LANE_COORDINATION.md` on the shared pod, (b) git commits with clear messages, (c) Nick pasting your reports into the Claude session. Write reports as if the reader has zero context. Claim provisional until verified against origin — lanes have reported unreproducible successes before; the probe wins, not the report.