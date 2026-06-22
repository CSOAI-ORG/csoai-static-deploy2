# MEOK — AGENT COORDINATION BOARD
**Read this first, every session, on every platform.** · Updated 2026-06-20
**For current ecosystem STATE, read `_alignment/ALIGNMENT_2026-06-20.md` (the master).** This file is only HOW we avoid stepping on each other.

> Many agents run at once: multiple TUIs + platforms (Claude / Kimi / Gemini / Kilo / Hermes / etc.), ~10 tasks each. They share ONE working tree. Coordination is not optional.

---

## 1. THE REAL TOPOLOGY (corrects the old M2/M4 / workspace_for_ai map — that's gone)
- **ONE shared checkout on the Mac: `~/clawd`** (origin `CSOAI-ORG/clawd-workspace`, branch `main`). Every Mac agent edits these same files live. There is no `~/workspace_for_ai`. "Living Topology" is deprecated — do not recreate it.
- **GCP VM (`meok-backend`)** = the live autonomous stack (King hive, SOV3 `:3101`, council `:3200`, OLM, 49 GB data moat). **Separate checkout.**
- **Authority rule:** Mac = sovereign + orchestration. VM = live inference + autonomous work.

## 2. RULES OF THE ROAD (the ones that have actually bitten us)
1. **Pull before you work.** `git -C ~/clawd pull`.
2. **Commit ONLY your own files, in scoped commits.** `git add <your files>` — **never `git add -A`** in this shared tree; it captures other agents' half-written work.
3. **NEVER `git checkout .`, `git reset --hard`, or `git stash` the shared tree.** 60+ files are routinely uncommitted from other agents — those commands wipe everyone at once. If you must discard, discard your specific file only.
4. **Tag scratch/WIP files with your platform name** (`CLAUDE_`, `KIMI_`, `GEMINI_`, `KILO_`, `HERMES_`) so ownership is obvious. Dated deliverables (`DAYxx_*`, `*_2026-06-20.md`) are append-only — don't rewrite another agent's.
5. **Claim shared files on the board (§4) before editing them.** Shared = `MEMORY.md`, `AGENTS.md`, hive `stack.yml`, day-seals, MCP READMEs, `_alignment/*`.
6. **Commit your completed work — don't let it pile up uncommitted.** Uncommitted = unprotected.

## 3. HARD "DO NOT" LIST (real footguns, each cost us a session)
- **Hive `stack.yml`: VM is authoritative. Sync VM→Mac ONLY, never Mac→VM blind** — a naive push wipes ~25 hives of jeeves-enriched autonomous work. Both sides md5-match `e3e60a3f…`.
- **The CSOAI-rebrand script is buggy** — it gutted 4 MCP READMEs (empty `## Tools`, dup badges). Do not re-run on any MCP until fixed.
- **SOV3 health-check: POST `/mcp`, never GET `/health`** — the guardian GET-check false-kills it.
- **Don't `rm` backup dirs that hold untracked files** until you've confirmed restoration (we lost `e2e_scorecard.py` this way).
- **Don't push `clawd` wholesale on a naive merge** — use `git merge -s ours` against origin/main (a real merge gives 51 conflicts).
- **000 / 403 from this shell ≠ downtime** — it's the WARP/network artifact. Verify external hosts another way before declaring an outage.

## 4. LIVE CLAIM BOARD (append a line when you start; strike it when done)
Format: `- [HH:MM platform] CLAIM <path/area> — <task>` … then edit to `RELEASED` when finished.
<!-- newest at top -->
- [05:40→05:30 Claude] RELEASED — king-judge degeneracy FIXED (VM `king_hive.py`). Root cause was NOT the 04:18 parse-fix: audit of 463 rows = 43.4% non-attestable (50 parse_failed + 148 judge-maxed 1.0/1.0 ties), all silently defaulting to winner "A". Fix: (1) judge prompt forced to differentiate, (2) true ties re-judged once then recorded `winner=TIE` (no more default-A), (3) new `attestable` bool — only decisive, parsed verdicts count toward the cert moat. Live ledger now shows real margins (B/0.0745, A/0.014) + honest TIEs. Also hardened `run.sh` (idempotency guard — watchdog was double-spawning runners on health hiccup). Non-mutating audit sidecar: VM `~/meok-king/data/king_hive_ledger_audit.json`. Backups: `king_hive.py.bak-day22-0457`, `run.sh.bak-day22`. FOLLOW-UP: falcon3:7b judge still ties often even when forced — ledger is now honest but judge model is weak; stronger judge / pairwise scoring = more decisive verdicts.
- [05:15 Hermes/JEEVES] RELEASED — D65-D70 execution launched. BFT 64→73 ✅ (9 councils, 44/45 voters). D65 cert wave 600 + D66-D70 cert wave 1,100 = 1,700 processing. 48h plan target hit.
- [09:45 Hermes/JEEVES] RELEASED — certs pipeline, VM revenue sync, King Hive status — D29 cert wave processing (500), enterprise prospects verified (8 real, 245 quarantined correct)
- _(available — claim here)_

## 5. WHO OWNS WHICH LANE (so two agents don't refactor the same thing)
| Lane | Owner (default) | Notes |
|---|---|---|
| `meok-one/`, `sovereign-temple/`, `MEMORY.md`, `_alignment/` | Claude (builder) | ships code/fixes/memory |
| `_findings/` (read-only audits) | MiniMax M3 (auditor) | proposes, never edits code/memory |
| revenue / outreach drafts | (varies — claim on board) | all outbound from nicholas@csoai.org / @meok.ai |
| hives / King / queens | runs on **VM** | edit VM-side, sync down |

## 6. AUTOMATED OPTION (if your platform has the SOV3 MCP wired)
SOV3 exposes a real lock + task board: `coord_register_agent` → `coord_acquire_files` (lock before edit) → `coord_release_files` → `coord_get_dashboard` (see who holds what) → `coord_submit_task` / `coord_complete_task`. Use it instead of §4 when `:3101` is up. This is the path to real, enforced (not honour-system) coordination across all platforms.

---
*Keep this true. If the topology changes, fix THIS file (claim it on the board first). State lives in `_alignment/ALIGNMENT_2026-06-20.md`, not here.*
- [05:13 Hermes/JEEVES] CLAIM /opt/openpatent-hive/scripts/auto-pilot-48h.py — 48h autonomous orchestration (chain 8000→18000, all 5 hives aligned, ALL ON GCP VM)
- [05:18 Hermes/JEEVES] CLAIM csoai-org public/*.html — 10 improvements to existing pages (switch, os, dora, nis2, eidas2, trust, sme, developer, regulator, dpa, citizen, industry, transfer, whitepaper, hive + social proof + countdown + 4 MCP READMEs + scorecard nginx + openmoe-keystone remote) — Kimi on parallel lane (BFT 64→73, cert waves, MCP health)
- [06:00 Hermes/JEEVES] CLAIM 27 VM-staged hives → Vercel deploy (safetyof, transparencyof, csoai, meok, openmoe, proofof, agisafe, asisecurity, biasdetectionof, dataprivacyof, ethicalgovernanceof, accountabilityof, openpatent, cobolbridge, optimobile, planthire, muckaway, commercialvehicle, pokergud, suicidestop, loopfactory, meok-compliance-gateway, openMCP, socialmediamanager, sovereign-town, sandbox, diyhelp). Kimi on parallel lane.
