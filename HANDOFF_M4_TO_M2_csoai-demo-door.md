# HANDOFF: M4 → M2 — CSOAI free-audit "door" (needs master brand + OS flow)

**Date:** 2026-06-25 · **From:** M4 (Claude Code) · **To:** M2 (Cowork — owns CSOAI + master branding)

## Why this is yours, not mine
CSOAI is M2's lane (you hold the master brand + the OS flow). I built a **working free-audit demo** from the engine in `NICK_FINAL_DELIVERABLES_COMPLETE.zip`, but it uses **placeholder branding and the zip's standalone landing page — NOT the CSOAI master brand or the OS flow.** Nick flagged this. So: **take the working logic, drop my branding, re-skin to CSOAI master + the OS flow.**

## What's built and VERIFIED working (reuse the logic, not the skin)
Location: `~/clawd/csoai-demo-engine/` (pushed to private clawd-workspace — nothing lost).
- `eu_ai_act_compliance_checker.py` — **real engine, 1684 lines.** `classify_input(text)` → risk level + confidence + matches; `generate_checklist()` → EU AI Act Articles 8–14 items. **Verified:** ER-triage→HIGH/82, loan-screen→minimal, FAQ-bot→limited.
- `app.py` — Flask: serves the page + `POST /api/audit` → `{riskLevel, riskScore, confidence, checklist[], frameworks[]}`. **Verified end-to-end in browser.**
- `demo_landing_page.html` — ⚠️ **placeholder brand — replace.** Form → `/api/audit` → engine-verified panel; graceful static fallback.
- `requirements.txt` + `vercel.json` — Vercel-deployable.
- Also in the zip: `demo_report_generator.py` (the $49 report — Gap #4), `outreach_email_generator.py`.

## What M2 needs to do
1. **Keep** `app.py` + `eu_ai_act_compliance_checker.py` (the engine + API — they work).
2. **Replace** `demo_landing_page.html` with the **CSOAI master-brand** front end + the **OS flow** (your assets in `csoai-org-v2` / `csoai-platform`). Just point its form at `POST /api/audit` and render the JSON.
3. Wire Gap #4 ($49 report) with Stripe (Nick's keys) using `demo_report_generator.py`.
4. Deploy to `csoai.org/try` (or per your routing).

## Context
This closes **Gap #1 (30-sec demo) + #3 (lead magnet)** from `THE_5_MISSING_THINGS.md` (in `csoai-demo-engine/`). The engine + API are the hard part and they're done + tested. Only the skin/flow is left — and that's the master, which is yours.

— M4
