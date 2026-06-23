# 🐉 24-HOUR LOOK-AHEAD — 23 JUN 2026 (Sprint 2 Day 2)
**Plan generated:** 23 Jun 2026 by JEEVES (Hermes Agent)
**Target:** 24-hour autonomous + Nick-gated execution window
**Reference:** `17_DAY_PLAN_TO_JULY4.md` Sprint 2 M16-M30, `EMPIRE_DASHBOARD_22JUN.md`, `SPRINT2_DAY1_EXECUTION_REPORT.md`

---

## EXECUTIVE SUMMARY
Today is Sprint 2 Day 2 (Surface Excellence, Jun 22-26). P0 blocker (csoai.org 404s) must be killed to unblock M17-M19 EU Code of Practice + Article 50 pages. Substrate is healthy and autonomous. Revenue pipeline is staged — 4 Nick gates remain the only wall to first £.

---

## PHASE 1: P0/P1 KILL (Hours 0-2) — AUTO where possible, HUMAN-gated where not

| # | Action | Owner | Time | Auto? |
|---|--------|-------|------|-------|
| 1 | **Fix csoai.org apex 404s** — re-alias to correct Vercel deploy for `eu-code-of-practice`, `article-50-transparency`, `article-50-marking`, `code-of-practice-2nd-draft` | JEEVES (verify) / Nick or Kimi (Vercel) | 2 min | ❌ Human-gated (Vercel dashboard) |
| 2 | **Add llms.txt to csoai.org** — AI-readable site index for ChatGPT/Claude/Gemini/Perplexity discovery | JEEVES | 5 min | ✅ AUTO (create file, deploy page) |
| 3 | **Add security.txt** to proofof.ai, cobolbridge.ai, accountabilityof.ai, ethicalgovernanceof.ai | JEEVES | 10 min | ✅ AUTO (create+deploy) |
| 4 | **Commit ~145 uncommitted files** — scoped git add for high-value files (policy-lab, MCP bridges, sovereign-town, gtm, sprint/) | JEEVES | 10 min | ✅ AUTO (git add + commit, scoped) |

---

## PHASE 2: SPRINT 2 EXECUTION (Hours 2-8) — AUTO

| # | Move | Description | Time |
|---|------|-------------|------|
| 5 | **M16 — 4-surface audit** | Verify all routes on meok.ai, csoai.org, openmoe.ai, openpatent.ai. Check cross-linking, flag dead links, verify HTTP 200 on all sub-pages. Produce audit report. | 20 min |
| 6 | **M17 — Build /eu-code-of-practice page** | Only if P0 resolved. NAVY+GOLD+BG design system, FAQ JSON-LD, Product JSON-LD, 4 buy buttons, EU CoP 2nd Draft analysis inline | 35 min |
| 7 | **M18 — 5 Article 50 sub-pages** | Build: /article-50-transparency, /article-50-marking, /article-50-deepfake, /article-50-bot, /code-of-practice-2nd-draft. Each with FAQ JSON-LD and cross-links. | 50 min |
| 8 | **M19 — Cross-link mesh** | Wire all 6 Article 50 pages into cross-link mesh: article-50-kit ↔ ai-act ↔ best-ai-for-ai-safety ↔ eu-code-of-practice ↔ all sub-pages | 15 min |
| 9 | **M20 — EU CoP "ready" badge** | Add EU Code of Practice readiness badge to all meok.ai product pages — data-driven from M12 freshness manifest | 15 min |

**If P0 NOT resolved by Hour 4:** pivot to offline-ready work:
- M21: Deploy 36 AEO/llms.txt files to production
- M22: Deploy 25 FAQPage JSON-LD schemas
- M23: Start building 7 comparison pages (MEOK vs Vanta/Drata/Arthur.ai/Credo AI/etc.)
- M24: Build 4-surface unified empire navigation

---

## PHASE 3: OUTREACH HYGIENE (Hours 8-12) — AUTO

| # | Action | Time |
|---|--------|------|
| 10 | Verify all 70 email drafts parse correctly via `send_all.py --dry-run` | 5 min |
| 11 | Article 50 deadline fact-check: Verify Claude's research (EU AI Act high-risk obligations postponed to Dec 2027) vs. current email content (Aug 2 2026). If postponed confirmed, flag all affected emails for update. | 10 min |
| 12 | Check Resend `mail.meok.ai` DNS verification status — if verified, auto-fire crons for 7 enterprise prospects | 5 min |

---

## PHASE 4: VM AUTONOMOUS OPS (Continuous) — AUTO, no action needed

| System | Cadence | Status |
|--------|---------|--------|
| **Cert autopilot** | Every 30 min, 50 certs/batch | 🟢 Running |
| **OLM Brain** | Every 5 min, Mamba-2+MoE+Attention+BFT+Ed25519 | 🟢 Running |
| **King Hive** | Continuous, watchdog/2min auto-restart | 🟢 Running |
| **SOV3 :3101** | Continuous, gunicorn | 🟢 Healthy |
| **Council :3200** | Continuous, 36 nodes | 🟢 Healthy |
| **Keepalive cron** | Every 2 min auto-restart dead services | 🟢 Running |
| **28 total cron jobs** | Per schedule | 🟢 All loaded |

---

## PHASE 5: END-OF-DAY SEAL (Hour 23-24)

| # | Action | Time |
|---|--------|------|
| 13 | Sprint 2 Day 2 completion report (what shipped, what's blocked, carry to Day 3) | 10 min |
| 14 | Update coordination board (`~/clawd/AGENTS.md`) if any claims needed | 2 min |
| 15 | Emit sigil for Day 2 moves completed | 2 min |
| 16 | Push all committed work to origin | 2 min |

---

## BLOCKERS THAT NEED NICK

| # | What | Why gated | Unlocks |
|---|------|-----------|---------|
| **H1** | Vercel re-alias csoai.org | Vercel dashboard access | M17-M19 EU CoP + Article 50 pages going live |
| **H2** | Resend `mail.meok.ai` domain verify | Resend dashboard or DNS | 326 email queue auto-fires |
| **H3** | `keystone sync-vercel` Stripe keys | Keystone session + decision to go live | First £ on Stripe |
| **H4** | Stripe live-flip | Human decision | Real revenue |

---

## RISK REGISTER

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| P0 csoai.org 404s not fixed within 24h | MEDIUM | Blocks Sprint 2 M17-M19 | Pivot to offline-ready work (M21-M24) |
| VM disk fills (26 GB free, 49 GB used) | LOW | Cert autopilot stalls | Monitor, cleanup if < 5 GB |
| Another sibling deploy regresses pages | LOW | Breakage on previously-working routes | Pre-deploy audit, claim board coordination |
| Article 50 deadline wrong in 70 outreach emails | MEDIUM | Credibility loss if sent with wrong date | Fact-check and update before any send |

---

## TOMORROW'S HANDOFF (Day 3, 24 Jun)

Expected state at end of Day 2:
- ✅ csoai.org apex fixed → all 5 EU AI Act pages HTTP 200
- ✅ M16 surface audit complete with report
- ✅ M17-M20 in progress or complete (dependent on P0 resolution)
- ✅ llms.txt + security.txt deployed (minimum viable Day 2 deliverables)
- ✅ ~145 uncommitted files committed in scoped batches
- ✅ 70 email drafts verified parse-clean and deadline-checked
- ✅ Cert autopilot + OLM brain + King Hive running autonomously
- ⏳ M21-M24 queued for Day 3 if not reached

---

*🐉 JEEVES — 23 Jun 2026. 24-hour look-ahead: P0 kill → Sprint 2 execute → seal. Substrate autonomous. Revenue wall = Nick gates. Onward.*
