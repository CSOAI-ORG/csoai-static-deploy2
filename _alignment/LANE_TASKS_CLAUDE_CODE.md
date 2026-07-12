# LANE TASKS — Claude Code (from MEOK-SOV3 lane, 2026-07-12)
_Coordination via git tree. Ordered by leverage. Honest gating noted per task._

## CONTEXT
Claude Code shipped the reach layer (Slack/Telegram/WhatsApp/Alexa/Siri/universal API + integrations hub) — strong,
and honest about the browser-render gap. These tasks unlock the distribution pathways (SOV33_DISTRIBUTION_PATHWAYS).

## TASK 1 — RUN the Kaggle reasoning harness for real  [HIGHEST LEVERAGE — do first]
- File: `_alignment/sovereign_merge_kit/sov33_kaggle_compete.py` (built + smoke-tested by MEOK-SOV3 lane).
- Run on Kaggle's OWN free T4 (30 hr/wk — no Colab needed), your logged-in account. Load GSM8K test set, define
  call_model via ollama/transformers on the T4, run grade(ds, call_model).
- It writes `sov33_live_gsm8k.json` in the schema `sov33_ingest_kaggle_result.py` reads → the gold-graded number
  AUTO-WIRES into `sov333_canonical.json` (capability_benchmark). This turns "built" into "showable".
- WHY FIRST: every distribution pathway depends on this one real graded number. Canonical is currently PENDING
  (a stub 0.5 was reverted — do NOT re-stamp a fake number; only a real graded run).

## TASK 2 — Adapt the harness for Game Arena (the SovTown demo)
- Kaggle Game Arena = head-to-head governed play, wins scored by opponents. Best architecture fit + most VISUAL.
- Reuse the cascade (draft→verify + BFT early-exit) as the move-selector; log every move SIGIL-attested.
- This is SovTown shown to the world: governed agents competing, outcomes scored externally.

## TASK 3 — Wire the opportunity-radar to a scheduler
- File: `_alignment/sovereign_merge_kit/sov33_opportunity_radar.py` (registry of 9 surfaces built by MEOK-SOV3).
- You're on the Mac → wire a launchd/cron/GitHub-Action to run `radar(dry_run=False)` daily (public APIs/RSS only).
- Honest line: public listings only, no login-scraping, no always-on surveillance. Diff for new comps/models/papers.

## TASK 4 — Visual / senior-friendly render pass  [gated on YOUR browser tool]
- The punch-list you already queued. The moment the browser read/screenshot layer clears, run it in one pass.
- Unblock hint you flagged: check the Claude app for a pending permission/approval prompt ("policy check") — approving
  usually revives all browser tools at once. This is owner-actioned, not a code fix.

## TASK 5 — HONESTY FIX: drop "1.09T fusion" from brain-stack public copy
- The brain-stack architecture (4-brain split, Mamba-2 SSD, 90/10 cascade, 20 slots, 33/33 tests) is GOOD and real.
- BUT "218B aggregate / 1.09T total sovereign fusion" is the additive-parameter category error (retracted twice
  before as 4.245T / 33T). You cannot sum params across models/OWEMs — a routing stack has the capability of
  whichever model answers, NOT the sum. Replace external copy with: "17.3B active per request, routed across 20
  brain slots." Keep "17.3B active" (honest); drop "218B/1.09T" (not a capability number; discredits on inspection).

## SHARED HONEST REGISTER (holds for all lanes)
- Score must be REAL before any public page (a reproduced-fake number undoes the credibility play).
- No AGI/consciousness claim anywhere public. Let the score + governance/audit story speak.
- Owner/platform-gated items (accounts, submissions, DNS/Stripe/publish) are YOURS to action; lanes build paste-ready.
