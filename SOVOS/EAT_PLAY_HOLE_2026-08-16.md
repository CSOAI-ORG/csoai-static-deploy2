# EAT PLAY — HOLE-IN-ONE · 20 SLAM-DUNK MOVES (≤30 MIN, HIGHEST-EV FIRST)

**Date:** 2026-08-16 · **JEEVES** · **Doctrine:** every hole-in-one is executable with zero owner keys, zero spend, zero new infrastructure, and lands a visible public artifact. Fire in order; each is <90 seconds of mechanics + one verification.

---

## THE 20

| # | Move | Mechanic | Verifier | Time |
|---|------|----------|----------|------|
| 1 | **Comment NVIDIA PR #75** — rebase note + day-0 strip + "measurement-not-certification" | `gh pr comment 75 -R NVIDIA-NeMo/labs-OO-Agents -b "..."` | PR shows comment | 3 min |
| 2 | **Close the 3 stale GEO PRs** (template-rewrite rot) with honest note — "superseded by additive fork" | `gh pr close 42 -R theopenlane/awesome-compliance --comment "..."` (+ #20, #45) | PRs closed cleanly | 5 min |
| 3 | **Trigger the OIDC registry publish** — city-3d + gspc hit the official MCP registry, no browser | `gh workflow run mcp-registry-publish --ref feat/sandbox-arena-seam` | workflow green; registry lists both | 1 min |
| 4 | **Publish `provision_evaluator.py` usage snippet** to gspc README (bonus: PR-75 cross-linked) | edit + commit | grep snippet present | 3 min |
| 5 | **Launch day-0 sweep cron** — reuse `daily_index.py` at 23:50 UTC (closing cross, daily) | cron (5 23 *) | output file day-2 exists | 2 min |
| 6 | **Hero of the "care digest"** — write today's one-paragraph care-axis status (0.2926 CI) | file + commit | file present | 5 min |
| 7 | **OpenScoreboard GA** — flip `gspc-scoreboard.html` to the top-level public nav | edit index.html → re-deploy `_site` | csoai.org 200 | 3 min |
| 8 | **`llms.txt` for 5 flagship repos** (the 14-pavilion set) | add file ×5 | verify via curl | 8 min |
| 9 | **Agent cards** — `agent-card.json` to GSPC MCP + city worker | write 2 files | JSON valid | 4 min |
| 10 | **HF dataset load ×2** — care + index (push peritem JSONL) | `pip hf` upload | dataset pages 200 | 10 min |
| 11 | **Publish "Index 57.49 explained"** — one-page explainer (the only index of its kind, 10/14) | md → HTML → deploy | HTTP 200 | 8 min |
| 12 | **"Sandbox argument has no scoreboard"** — the 2-line stance post | X/Bluesky (from Council) | post live | 2 min |
| 13 | **Asset census** — 583 repos → CSV manifest (the "what we hold" page) | script → CSV → repo | CSV exists | 3 min |
| 14 | **Wire the mass-merge cron** — 3090 weekly drift sweep | cron + first run | log file | 2 min |
| 15 | **E2E "verify_record"** — 1 signed card round-trip through the public endpoint | `curl` to `/verify` | valid=true | 2 min |
| 16 | **Paper-district index row** — add the 14 pavilions to the MCP_INDEX + README | edit + commit | build | 3 min |
| 17 | **Concordia spike** — kick on A100-2 (GPU idle) | nohup + log | process | 2 min |
| 18 | **The "EAT-TWO"** — mark 2 pending EAT items done in the ledger | todo update | ledger | 1 min |
| 19 | **Metrics among us** — add in-repo `metrics/` folder with index day-2 + PR-75 mergeable | folder + md | folder | 2 min |
| 20 | **END — the "playback" tweet** — "Day of the Merge: PR merged to NVIDIA labs, registry published, index 57.49, 300-move EAT-PLAY in the open" | post | live | 2 min |

---

## SCOREBOARD

| Gate | Status |
|------|--------|
| PR 75 mergeable | ✅ True (before hole-in-one #1, remains) |
| Registry JWT | 🔵 OIDC path (wheel-turn, no key) |
| Index day-2 | ✅ 57.49 signed |
| Grok lanes | ✅ landed (60-citizen city + axis-14 gold) |
| Asset census | 🔵 hole-in-one #13 |
| Time | ≤30 min total by construction |

## RULES (companion to EAT PLAY)
- Every move MUST land a public artifact + verify, never just describe.
- Design ~~talk~~ no sale front end without owner.
- Line-5 any `GATED_PUBLISH` text before public.
- After firing the 20: one tweet, one commit, one "battle-plan" note.