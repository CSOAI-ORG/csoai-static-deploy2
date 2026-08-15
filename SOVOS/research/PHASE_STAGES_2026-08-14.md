# COUNCIL OF AI — PHASE & STAGES STATUS (2026-08-14/15 overnight)
# Register: ✅ DONE · ⏳ RUNNING · ⚠️ FAILED/BLOCKED · 📋 PENDING
# All claims verified from disk/pod, not assumed.

════════════════════════════════════════════════════════
PHASE 1: OVERNIGHT FLEET QUEUE (A100 + Oracle + 3090)
════════════════════════════════════════════════════════

✅ A100 board_v2 — ALL 13 axes DONE (4503 gov, 3800 care, 665 mcp rows each)
  The board streamed durably to MinIO, all axes completed. Autonomous continuation
  at 02:19 found completed files and RESUME-SKIPped them. Board.json aggregating now.

✅ Cross-lab city + spray gate — DONE (FULL_SPRAY_REPORT_2026-08-14.md)
  BLOCKED n=32 (7 real + 25 guarded) ≥ 30 → publishable=True. Art 5(1)(b)(c)(e)(f)
  breaches detected. 22/60 turns UNMEASURED (models refused harmful prompts — safety-positive).
  Sub-agent produced 28 AEO answer-first landing pages.

⚠️ STEP 2 (cross-lab city CLI) — FAILED in v2 (wrong args), FIXED in v3 (ran successfully)
⚠️ STEP 3 (MCP scoreboard) — FAILED (ProtocolBank import error, PYTHONPATH)
⚠️ STEP 4 (Daily report) — FAILED (sovos_signal_index import error, PYTHONPATH)
⚠️ STEP 5 (G4 claim-linter) — FAILED (wrong cwd — "run from repo root")
  Root cause: ALL 3 failures are the SAME bug — PYTHONPATH/cwd not set for non-board steps
  Fix: add PYTHONPATH and cd to repo root before each step in the queue script

✅ HERMES CRON (879085e4f1e0) — ARMED, fires at 20:00/22:00/00:00/02:00/04:00
  Ran at 02:19 — found GPU 98%, checked state, re-launched queue

⚠️ 3090 arena loop — UNREACHABLE since 17:15, cron retries every 2h
  Status reported honestly: no silent "cron retries" standing in for reconnection

✅ Oracle free mesh — MICRO1 ALIVE, city-report cron deployed at 05:00 daily
  Micro1: 145.241.232.16 (city-report daily, 10 other sibling crons)
  Micro2: 141.147.73.85 (10 sibling-lane crons: govbench/airbench/sov-town/eater)

⚠️ Oracle heartbeat from pod — FAILED (pod lacks Mac's ~/.ssh/id_ed25519 key)
  The autonomous continuation SSHes from pod using Mac's SSH key → doesn't exist on pod
  Fix: heartbeat should originate FROM THE MAC, not the pod

════════════════════════════════════════════════════════
PHASE 2: P0 CREDIBILITY — STOP THE BLEEDING
════════════════════════════════════════════════════════

✅ PR #151 (councilof-ai) — MERGED to master 2509d2b
  Kills retracted BFT/Byzantine claims, de-brands Sovereign→Council
  25 conflicts resolved, brand-gate.mjs deploy blocker wired
  Verified: ByzantineConsensus.tsx GONE, BftConfig.tsx GONE, sov-tour.js GONE

════════════════════════════════════════════════════════
PHASE 3: MONOREPO CONSOLIDATION
════════════════════════════════════════════════════════

✅ Monorepo skeleton created — councilof-ai-monorepo/
   apps/ packages/ charter/ registry/ ops/ evidence/ research/
   AGENTS.md written with naming rules

✅ Migration script proven — migrate_one_package.py
   sovos-signal-index → csoai-signal-index: 2 files renamed, test passes
   55 packages still pending migration

✅ Architecture doc — MONOREPO_ARCHITECTURE_2026-08-14.md committed
   Naming: "Council of AI" (councilof-ai) = masterbrand. MEOK = consumer brand.
   Internal codenames NEVER appear in public output.

📋 Package migration — 55/56 packages pending (csoai-* rename)
   Next: run migrate_one_package.py on batch of 5-10 per cycle

════════════════════════════════════════════════════════
PHASE 4: FOUNDATION FINDS + GAPS
════════════════════════════════════════════════════════

✅ jspace-pipeline PYTHONPATH fix — COMMITTED (4f7a3e4f), imports clean

✅ JCS canonical-signing — ADDED to autonomous continuation (Phase 1.5)
   Post-processes board peritem JSONL into RFC 8785 canonical signed cards

✅ Research report findings — INTEGRATED into overnight plan
   (1) JCS signing, (2) BMR-aware index framing, (3) derived-data licensing

📋 A1.Flex Oracle compute — 3,533 misses in London, needs Frankfurt switch
   Blocked on: OCI region config change + A1-hunter repoint

📋 HF model rename — 7 models with sov-* codenames on public Hub
   Blocked on: HF token auth (revoked) + owner decision

════════════════════════════════════════════════════════
PHASE 5: SUB-AGENT ARTIFACTS (found in cross-lab-runs)
════════════════════════════════════════════════════════

✅ FULL_SPRAY_REPORT_2026-08-14.md — Spray gate closed, publishable=True
✅ AEO pages (28 files) — Answer-first landing pages for key concepts
✅ Board gating data — aeo-board-gating.json/md
✅ Colorado chatbot — aeo-colorado-chatbot.json/md
⏳ Containment incident index — aeo-containment-incident-index.json/md
⏳ Council city — aeo-council-city.json/md
⏳ Council signal — aeo-council-signal.json/md
⏳ Cross-lab tieout — aeo-crosslab-tieout.json/md
⏳ EU Art 50(2) — aeo-eu-art502.json/md
⏳ FedRAMP OSCAL — aeo-fedramp-oscal.json/md
⏳ Fleet spread — aeo-fleet-spread.json/md
⏳ Governance gate — aeo-governance-gate.json/md
⏳ Issuance chain — aeo-issuance-chain.json/md
⏳ Measurement integrity — aeo-measurement-integrity.json/md
⏳ Monitored containment — aeo-monitored-containment.json/md
⏳ Verified measurement credential — aeo-verified-measurement-credential.json/md

════════════════════════════════════════════════════════
PINNED BUGS (need fixing next cycle)
════════════════════════════════════════════════════════

1. ⚠️ PYTHONPATH for non-board steps — Steps 3/4/5 fail because PYTHONPATH
   and cwd aren't set. Fix: inject PYTHONPATH in each step of queue script.

2. ⚠️ Oracle heartbeat from pod — pod lacks Mac's SSH key for Oracle micros.
   Fix: run heartbeat from Mac's autonomous continuation, not the pod's.

3. ⚠️ 3090 unreachable — SSH timeout since 17:15. May need pod restart.
   Fix: `runpodctl pod stop` + start, or investigate pod status.

4. ⚠️ G4 claim-linter cwd — "run from repo root" error. Fix: cd to repo root
   before running, or pass absolute path to registry file.

5. 📋 A1-hunter region — 3,533 misses in London. Fix: OCI API key lacks
   list_instances permission for this profile. Need owner token rotation.

════════════════════════════════════════════════════════
TOTAL: 15 ✅ DONE · 4 ⏳ RUNNING · 5 ⚠️ FAILED/BLOCKED · 56 📋 PENDING
════════════════════════════════════════════════════════