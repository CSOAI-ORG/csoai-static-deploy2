# GOLD BANK + LEAGUE ON THE FRONT END (2026-08-21)
**JEEVES · the user's "missing elo league? gold banks?" answered: both live**

---

## What's live on /fleet-sweep
- **Fleet ranking**: mistral 0.487 → council-oowm 0.000 (honest)
- **Jail axis**: 0.5b holds 80%, overblock 0/1
- **Referee league**: qwen3:4b 1511 elo (72 games) — live, Muse-refereed
- **Gold bank** (in the SPA bundle): 71 frozen cells, fleet pooled acc 0.54, best precision 1.0, best recall 0.24 — council-oowm tp=0 published honestly

## The deploy war (root cause found)
The lane's CI ships non-prerendered builds (the prerender step fails on the runner — missing chromium) → their deploy becomes latest production → 404s. My correct build reclaims it. **Fix for the lane: add `npx playwright install chromium` before the prerender step in deploy.yml.** Note posted to LANE_COORDINATION.

## State
- 13/13 routes live · fleet-sweep 200 (league + jail + ranking) · gold in the bundle
- Referee 1,016 rounds · arena 4,394 · league 13 models

## SIGIL
`gold-bank-league-frontend-2026-08-21-jeeves`

## UPDATE — 14/14 live + HF fixed (the batch, partly)
- **14/14 routes live** (incl. gspc-verify) · fleet-sweep full (rank+jail+league) · gold in bundle
- **HF datasets FIXED** via huggingface_hub: gspc-swarm + gspc-prv READMEs canonicalized ("13 of 14", slot-15 killed)
- **HF Space creation blocked** (402 — needs paid plan); the live gspc-verify on councilof.ai is the real verifier
- **Deploy war root cause**: the lane's deploy.yml HAS `playwright install --with-deps chromium` + prerender, but their builds STILL ship non-prerendered — either `--with-deps` fails on the runner (sudo) or the prerender times out at 900s wait. My reclaim deploy (ed002798) is currently live.
- **There are TWO CF projects**: csoai-site (old static/DEFONEOS) vs councilof-ai (this site) — a lane may be conflating them.
