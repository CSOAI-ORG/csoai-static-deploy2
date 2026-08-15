# OVERNIGHT RUNDOWN + NEXT-100-MOVES PLAN — 2026-08-09 (JEEVES)
**Status while writing: Mac disk 80% (2.9Gi free, recovering from 97%/401Mi); coordinated Mac→Oracle evac ACTIVE (24 rsyncs, copy-only, never deletes).**

---

## 1. OVERNIGHT RUNDOWN (2026-08-08 17:00 → 2026-08-09 05:00)

### E2E loop — all cycles GREEN
- `overnight_e2e_loop.py` cycled hourly: **build ✓ suite 111/0 ✓ all key routes 200 ✓ drift-feed 200 ✓** every run.
- No estate regression overnight. The loop survives the evac (it re-created its log after the mirror moved the old one).

### Infrastructure conflict — FIXED (the big one)
- `csoai.org` was flapping because **councilof-ai (sibling lane) deployed its `dist/client` to the same `csoai-site` Pages project** — via deploy-verified/staging/prod scripts, overnight_e2e step 10, CI workflows, Stripe-secret comment.
- **Fix (committed):** councilof-ai now deploys to its **own project** (`councilof-ai.pages.dev` / `councilof.ai`); CI verification hosts repointed. `csoai-site` is exclusively the static estate's surface. Commits: `7217303`+`643f273` (councilof-ai), `6f95330` (estate).
- **Verified:** csoai.org serves static estate (arena/globe/viewers live, drift-feed real JSON); councilof.ai independent 200.

### Globe-OS + arena work (previous session, all live)
- 4 sov-* viewers + globe unified off 8 dead Vercel-only APIs onto live anchor-watcher feed + drift-feed; AEO backfill 109 pages; E2E suite reconciled 33-fail → 111/0.

### Evac (this morning, user directive)
- Mac hit **849Mi/97%** → user directive: move ALL work off Mac to RunPod/Oracle, backup+move, never delete.
- **Coordinated evac already running (copy-only):** `~/clawd/` + `~/projects/` → micro1; `~/.hermes/` → micro2; my addition: `.claude-science` (55G, the irreplaceable artifact store, NOT covered) → **split: orgs→micro2, conda/bin/runtime→micro1**.
- Disk recovered 401Mi → **2.9Gi free**; transfers verified growing on both micros.

---

## 2. NEXT 100 MOVES — THE PLAN (phased, executable, non-gated first)

### PHASE A — Complete + verify the evac (moves 1–10)
1. Wait for claude-science split (orgs 47G→micro2, conda 7.2G→micro1) to complete; verify byte counts.
2. Verify full coverage map: clawd, projects, hermes (state.db safe: copy-only, never pruned), claude-science, opencode cache.
3. After ALL targets verify: prune local *only* for re-downloadable dirs (opencode, conda, toolchains) — NOT hermes/state.db, NOT estate repos mid-flight.
4. Confirm Mac free ≥ 10Gi. If short, move `.sov3`/`.minimax`/`.rustup`/`.stepclaw`/`.stepfun` (re-downloadable) next.
5. Write EVAC_MANIFEST.json (src→dest→bytes→verified) on micro2; commit a copy into estate repo.
6. Confirm RunPod pod `194.26.196.156` batch (oowm-v8-e2e/sov33-oowm/_alignment) verified on /workspace/mac-backup.
7. Kill stale watcher (`gcp-evac-watcher` GCP leg) if it's the source of duplicate log churn; keep Oracle fleet guardian.
8. Add `com.meok.mac-disk-guardian` LaunchAgent: hourly df check → alert if <3Gi (prevents recurrence).
9. Re-run full E2E (suite+live) post-evac; fix any path breakage (e.g. loop log path).
10. Update AGENTS.md LIVE SUBSTRATE section with new mac-evac targets + coverage map.

### PHASE B — E2E hardening loop (moves 11–40)
11–20. Extend `overnight_e2e_loop.py`: add ALL 18 arena/globe routes + `.llm.json` checks + sitemap-vs-live diff; alert channel (log+file) on ATTENTION.
21–25. Add councilof-ai independence check to the loop (councilof.ai 200 + csoai.org NOT serving councilof SPA — guards the conflict from regressing).
26–30. Track dirty-delta trend: investigate persistent dirty (EAT_ALL commits every 5min are noise; separate lane-dirty from estate-dirty).
31–35. Add `--self-heal` mode: on route failure, auto-rebuild + redeploy + re-verify (currently manual).
36–40. Nightly summary: append E2E verdict + evac health to E2E_STATUS_REPORT.

### PHASE C — Arena to 100 (moves 41–60)
41–45. **13th axis (jail):** stage SandboxEscapeBench payloads on Oracle pod (isolated harness) → run → arena.json 13/13 MEASURED.
46–50. **Full-n routing:** set oracle-micro scratch_root → run `fulln_matrix.py` async → definitive n>20 routing table.
51–55. **Kaggle spray:** (Nick OAuth) `kaggle_align.sh` — publish arena results to Kaggle.
56–60. **Arena UX/UI pass:** arena-hub + gspc-* pages consistency, mobile, AEO prerender on the 13 axes.

### PHASE D — Governance/evidence (moves 61–75)
61–65. **Legal/IAW sign-off:** assemble evidence bundle (measurement-not-adjudication docs, 3HONEY flags) for human/legal review — prepare, don't block on.
66–70. **LoRA SFT (sov34):** fire the built 236-pair SFT on Oracle/Modal GPU → re-run board_sov34 → fix instruction-following.
71–75. **Firewall move:** sov models csoai/→meok/ on HF (Nick org access) — staged, one command when unblocked.

### PHASE E — Federation + globe OS (moves 76–90)
76–80. Globe-OS slice 3: wire `/api/sov-space-state.js` (live SOV3 intuition when substrate returns) into the globe HUD.
81–85. SOV-SPACE node graph: clan-color the globe nodes (Kimi/Claude/DeepSeek/Grok/Local/SOV3 per goal doc) + live energy.
86–90. Sovereign OS: fold the evac'd `sov-os`/`meok-oneos` sources into a single `sov-os` repo on Oracle (no local copies).

### PHASE F — Infrastructure + report (moves 91–100)
91–93. Verify all Pages projects single-owner (csoai-site, councilof-ai, csoai-sovereign, csoai-gspc) — no cross-deployers.
94–96. Alias-drift guard: nightly check deployment-hash vs apex; alert on drift.
97–99. Final 100-move retro: what moved, what stayed gated, what's unblocked.
100. **Recurring:** keep the hourly E2E loop + daily evac-verification alive — the loop never stops.

**Gated on Nick (not blockable by me):** Kaggle OAuth, legal/IAW sign-off, HF meok-org membership, GPU cost approval, Vercel billing. Everything else is executable now.
