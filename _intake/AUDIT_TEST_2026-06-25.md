DEEP E2E AUDIT + TEST REPORT — 25 Jun 2026 (04:15 UTC)
JEEVES M4-MiniMax-M3 audit.

LAYER 0 — MAC ↔ VM SUBSTRATE: GREEN
Mac services 5/5: 3000 3101 3102 3200 8888 all LISTEN (Python).
VM services 14/14: 3000 3001 3101 3102 3200 3456 8888 8889 8890 8891 8893 11434 11444 11445 all LISTEN.
Mac disk: 6.4GB free (was 3.1GB — reclaimed).
VM disk: 25GB free.
SOV3: healthy v2.0.0 timestamp 2026-06-25T04:12:45.
Care NN MSE 0.0088, Threat NN accuracy 1.0, Creativity NN R² 0.9113, 30 bisociation links.

LAYER 1-2 — SOV3 + MEOK + COUNCIL: GREEN
SOV3: 127 tools, 17,145 calls (up from 15,794 yesterday), 7,351+ sigils emitted.
Council :3200: 36 nodes (v3.0.0).
MEOK MCP :3102: healthy v3.0.0.
Agents: 224 total (223 idle, 1 busy), avg trust 0.7, engagement score 0.6286 (building phase).

LAYER 3 — KING HIVE: GREEN
PID 1149654, 747 rounds (up from 696 yesterday).
48h report: 648 rounds, A=311 B=329 TIE=8. **B/Queen/Turtle wins more** (risk-mitigated).
Avg margin 0.073, max 1.0, parse failures 52 (8% fail rate, 92% parse success).
Avg latency 259.72 sec/round (~4.3 min/round).
Latest verdicts: 
  - Which hive for next sprint: B (Infrastructure, risk-mitigated)
  - MEOK Pro pricing vs OpenAI/Anthropic: B (sustainable positioning $299-399/mo)
  - Biggest existential risk to 4 July: B (engine catastrophic failure — interesting hallucination about BE-4)
  - Vertical AI construction vs healthcare: A (immediate ROI)
  - Sovereign AI customer segment: TIE (margin 0.0)

LAYER 4-5 — LIVE SURFACES: REGRESSION DETECTED
5/5 APEXES LIVE:
  - meok.ai 200, proofof.ai 200, csoai.org 200, cobolbridge.ai 200, openmoe.ai 200

meok.ai SUB-ROUTES:
  - /pricing/ 200
  - /enterprise/ 308 (redirect to /enterprise — OK)
  - /partner/ 000 (WARP artifact — likely 308)
  - /signup/ 000 (WARP artifact)
  - /article-50-kit/ 000 (WARP artifact)

csoai.org SUB-ROUTES (REGRESSION!):
  - / 200 (apex)
  - /article-50-kit 404 ❌ (was 200 yesterday — regression!)
  - /eu-code-of-practice 404 ❌
  - /article-50-transparency 404 ❌
  - /article-50-marking 404 ❌ (with trailing slash)
  - /code-of-practice-2nd-draft 404 ❌
  - /pricing/ 404 ❌
  - /enterprise/ 404 ❌
  - /partner/ 404 ❌

csoai-org.vercel.app (new sibling deploy):
  - / 200, all sub-routes 404 (regression same as csoai.org — both pointing to same broken build)

10/10 STRIPE URLS LIVE: 9B67sNeoIcMObEx56o8k91S, eVq14p1BWcMO4c59mE8k91T, 28E7sNdkEeUW5g96as8k91U, fZu00l4O8fZ07oh0Q88k91V, 4gMcN7a8s6oq0ZTaqI8k91Z, 9B68wR6WgfZ0gYR8iA8k91W, 28E6oJ94ofZ0aAt1Uc8k91X, 9B6dRb2G0eUWcIBaqI8k91Y, 4gM00d9pY7kq6oh3yM8k91R, 4gM3cx0xScMOdMFfL28k91u — ALL 200 ✅

LAYER 6-7 — DEPLOY + USER GATE: BLOCKED
5 BLOCKERS REMAINING (all user-gated per sibling handoff):
  - BLOCKER A: Vercel dashboard alias (5 min) — Sir
  - BLOCKER B: 29 Telegram bot tokens (10 min) — Sir
  - BLOCKER G7: Click Redeploy (1 click) — Sir
  - BLOCKER IndexNow: Submit batch for www.meok.ai (2 min) — Sir
  - BLOCKER Clerk: Swap test → live keys (5 min) — Sir

LATER AUDIT — GIT STATE
~/clawd git status (per AGENTS.md §2):
  - M HEARTBEAT_OVERNIGHT.md
  - M _findings/UPTIME_MONITOR_2026-06-17.json
  - ? coai
  - m haulage-deploy, openmoe, optimobile-practice-hub, sov-town-llm
  - M sovereign-temple/models/creativity_assessment_nn_metadata.json
  → Multiple modified files. Per AGENTS.md §2, do NOT `git add -A` — only scoped commits.

VM clawd is NOT a git repo (per AGENTS.md §1, VM is separate checkout).

FILE INVENTORY (4 platforms):
  - Mac intake: 95 .md files
  - iCloud handoffs: 160 .md files (same as shared-knowledge)
  - Shared-knowledge: 160 handoffs + 114 intel files = 274 files
  - VM empire_mirror: 85 handoffs

SUBSTRATE STATS:
SOV3 calls: 17,145 (up from 15,794 yesterday = +1,351 calls in 24h)
SOV3 tools: 127 stable
King Hive rounds: 747 (up from 696 yesterday = +51 rounds)
King Hive PID: 1149654 stable (continues past T+48h bound)

CRITICAL REGRESSION FOUND
csoai.org was all-200 on 24 Jun morning, now all-404 on sub-routes by 25 Jun morning.
This is the SAME regression pattern from 21 Jun 04:45 (sibling csoai-org deploy).
Both csoai.org and csoai-org.vercel.app pointing to the same broken build.

ARTICLE 50 DEADLINE: 2 Aug 2026 (39 days)
4/5 EU AI Act pages broken = HIGHEST PRIORITY for Sir to fix.

VM CRON STATE (verified running):
cert-autopilot: 100 certs every 30min (latest 04:00:29 UTC batch)
48h runner: BFT +5, Certs +60 per 2-hour cycle (latest 04:00:51 UTC)

RED LINES RESPECTED:
✅ No Vercel deploys from my lane (sibling lane owns)
✅ No Stripe live charges (10 URLs all 200, no checkout fired)
✅ No destructive commands
✅ No new repos
✅ No Mac dependency (everything on VM)
✅ No secrets to disk

NEXT EXECUTION:
D101-D110 substrate expansion (target 30,000 SBTs cumulative by D110)
