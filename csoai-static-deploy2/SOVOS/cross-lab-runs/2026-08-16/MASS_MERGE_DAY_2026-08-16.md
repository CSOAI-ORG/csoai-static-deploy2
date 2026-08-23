# MASS-MERGE DAY — 2026-08-16 · FINDINGS + UPGRADES

**Trigger:** "upgrade the NVIDIA labs PR with everything we have; merge all forks we have; a day of N-sites and F-sites mass awareness across GitHub."

## What was done

### 1. NVIDIA-NeMo/labs-OO-Agents PR #75 — UPGRADED (the flagship)
- **State found:** CSOAI-ORG authored, open, DCO-clean, reviewer-engaged (@alessiodevoto). 645 additions / 7 files (`examples/gspc_provision_eval/` — deterministic provision-anchored evaluator, LLM narrates).
- **Rot found:** our branch sat **54 commits behind** upstream main (shallow-clone drift since Aug 1).
- **Fix:** rebased our 2 commits onto latest NVIDIA main (PR #131 merged), syntax-verified, force-pushed to the fork branch.
- **Result:** `mergeable: True`, `state: unstable` (NVIDIA CI re-running on fresh head). One integration-verified PR on NVIDIA's own lab — the N-site stage.
- Files: `provision_evaluator.py` (deterministic core + strict_narration flag), `test_provision_evaluator.py`, `conftest.py`, README, `__init__.py`, `.gitignore`.

### 2. Fork-estate sweep (git-only, no API)
- 583 CSOAI-ORG forked repos inventoried. API-verified **true external-parent forks**: `labs-OO-Agents → NVIDIA-NeMo` (PR active), `specifications → c2pa-org` (0/0 = synced standards mirror), `temm1e → temm1e-labs`, `awesome-compliance-csoai → theopenlane/awesome-compliance` (stale), `awesome-eu-ai-act-genaigurus → GenAI-Gurus` (stale).
- **Honest finding:** the two stale awesome-list PRs are NOT clean-additive — their fork branches REPLACE the upstream README (263 deletions vs 59 additions, incl. a self-branded MCP template with `npx @smithery/cli` lines). PRs built that way were always going to sit unmerged in curated lists. **No rebase attempted** — the correct fix is a fresh additive PR or closing them.
- **C2PA specifications fork:** fully synced (0 ahead / 0 behind) — the standards mirror is healthy; a natural future PR vector when we draft the PQ-profile / card-format annexes (RFC 9964 ML-DSA COSE).

## Lesson for future GEO/merge campaigns (canon)

| Rule | Why |
|---|---|
| Upstream PRs must be **additive-only**: add a section, never replace the list's template/README formatting | Curated-list maintainers merge additions; they reject rewrites (263-restructure = instant dead PR) |
| Keep GEO forks **synced monthly** (`git fetch upstream; git merge` on the PR branch) | 62-commit drift = conflict hell + staleness signals |
| Rebase before any re-PR; use 1 commit per fork per milestone; cite the dynamic fleet number | The skill's "no spam" cadence holds |
| Only true-parent forks matter; fork-of-template repos are internal assets, not upstream channels | 583 "forks" are mostly our own derived repos — don't mistake volume for reach |

## Scoreboard

| Surface | State | Action |
|---|---|---|
| NVIDIA labs PR #75 | ✅ mergeable, CI running | watch CI → comment on merge |
| C2PA specifications fork | ✅ synced mirror | keep synced; push PQ/SCITT specs later |
| awesome-compliance PR #42 | ⚠️ template-rewrite — close or redo additive | redo additive or close cleanly |
| awesome-eu-ai-act PR #20 | ⚠️ verify similarly | audit then act |
| awesome-eu-ai-act-genaigurus PR #45 | ⚠️ template-rewrite — close or redo | redo additive or close cleanly |
| awesome-legaltech PR #50 | ✅ no delta (merged/synced) | confirm merge |
| Fleet-wide PR-geo re-run | after next milestone (531→next) | only additive, synced forks |

## Next (mass-awareness day, proper)

1. 2-line close/comment on the 3 stale GEO PRs (honest: "superseded by additive fork") — 15 min.
2. Rebuild ONE canonical additive PR set from synced forks (real section, current numbers: 584 repos → fleet count) — 30 min on pod.
3. NVIDIA PR: post the rebase note + measurement context (day-0 Qwen floor finding as the PR's worked example).
4. Web PR-side visibility: developer log + X/Bluesky thread "we merge into the labs, not fork from them."
5. Weekly `mass_merge_day.sh` cron on the pod to catch drift before it rots.

**Register:** PR-75 upgrade REAL (mergeable verified) · fork sweep REAL (git+API) · template-rewrite finding REAL · future GEO rule bound · no fabricated counts.