# NEXT 100 MOVES — FRAMEWORKS DRUM + Master Framework v1.4
## LEARN · ALIGN · EAT · 2026-08-20 · owner: JEEVES lane (drum) + aligned lanes

> Living plan of record, grounded in `docs/MASTER_FRAMEWORK.md` v1.4 and
> `docs/RESEARCH_VALIDATION.md`. Every move is EAT-scored: **measured → CI'd → signed →
> chained → anchored → boarded → mirrored** (the 7-box mission def). Moves tagged [GATE]
> need Nick or the deploy lane; [LANE] needs that lane's owner. Honest register: nothing
> below is claimed done until it is verified with output shown.

## MOVES EATEN (progress log — evidence below)

| Move | Status | Evidence (2026-08-20) |
|---|---|---|
| 11 — committed test suite | ✅ | `tests/test_drum.py` — ALL GREEN (catalog integrity, dup-ids=0, cards==items, hygiene, feeds) |
| 12 — `--check` mode | ✅ | `build_catalog.py --check` → PASS (dup ids, missing fields, counts, canary) |
| 13 — `--lint` gate | ✅ | `build_catalog.py --lint` → PASS (public surfaces clean; internal items flagged+filtered, status/issuer/region/effective scrubbed) |
| 14 — standing check script | ✅ + LaunchAgent live | `ops/frameworks-drum-check.sh` → ALL GREEN; `com.meok.frameworks-drum-check` loaded (15-min verify-only, log `/tmp/frameworks-drum-check.log`); `--verify-only` read-only mode added |
| 15 — canary string | ✅ | `catalog.json` carries `drum-canary-7f3a9c2e`; `--check` verifies it |
| 16 — crosswalk estate pointers | ✅ | `drum_crosswalk` note now names the estate crosswalk surfaces (csoai.org/frameworks, 12-framework crosswalk, 236-list) |
| 17 — `drum_watch` | ✅ | MCP tool added; diffs reg_events vs prev snapshot (added/changed/removed deltas) |
| 18 — `drum_freshness` | ✅ (fold-level, honest) | MCP tool: catalog generation age + counts; per-item verified dates not yet tracked (noted) |
| 19 — search pagination | ✅ | `drum_search` accepts `offset` (verified: gdpr 15 matches, offset paginates) |
| 20 — edge-case selftest | ✅ | MCP selftest 13/13 → now 21/21 with the 3 new tools (route/history/freshness edge cases) |
| 21–25 — conformal router core | ✅ | `router/conformal_router.py` — calibrate/route/realized_error + selftest PASS (quantile property 0.9533 vs 0.9502; realized error 0.0271 ≤ α=0.05; determinism + edge cases) |
| 26–29 — router wiring | ✅ scaffold (honest not-trusted) | `router/calibration_set.py` (200 simulated entries, clearly marked) + `drum_route` MCP tool (reports calibration/trust state explicitly) + `router/drift_monitor.py` (percentile-shift alarm). **Remaining:** the ensemble-disagreement score + realized-coverage check before trust |
| 30 — router measured card | ✅ data layer; ⏳ score | `router/collect_measured.py` → **80 measured labels** (79 human-vs-AI arena rounds with agreement + 1 experiment) in the calibration set. **Honest:** all measured scores are PROXY (no pre-label feature yet) — `drum_route` reports `measured_labels: 80, score_proxy: true, trusted: false`. Trust flips when the ensemble-disagreement score (move 26) + realized-coverage check land |
| 31–34 — Knowledge archive core | ✅ (unsigned honestly) | `archive/knowledge_archive.py` — append-only, content-addressed, lineage; selftest PASS; entries signed:false until the #dsh rail exists |
| 35–40 — archive signing/wiring/history tool | ✅ 36+40 done, 35 [GATE] | **36:** build_catalog.py appends a Knowledge entry per fold (7 entries so far — the drum eats itself); **40:** `drum_history` MCP tool (count + lineage by content_id); 35 (signing) needs #dsh |
| 54/74 — EAT box 6 (boarded) | ✅ 2026-08-23 | board live at frameworks-drum.pages.dev (HTTP 200); nav 404 fixed; eat_7box now COMPUTES the 7-box status (3/7 true, 2 partial, 2 false) |
| 88 — days-to-hours proof | ✅ 2026-08-23 | `ops/measure_latency.py` → `feeds/loop_latency.json`: full RUN→TEST→AUDIT→CHECK loop = **6.8s** (property suite dominant; stdlib-only, no GPU/fleet) |
| mining — holy-of-sources folds | ✅ 2026-08-23 | +5 verified frameworks (NIST AI 100-4, NIST AI 800-1, ISO/IEC 5339, 27559, TS 27560) → catalog 634→639; each web-verified before fold |
| benchmark — first-class kind | ✅ 2026-08-23 | 36 canonical benchmarks (MMLU/HELM/SWE-bench/GPQA/ARC/AILuminate/LiveBench + classic NLU/vision/agent/safety) — schema/cards/site/MCP/tests wired; catalog 625→661; board redeployed (649 public items live) |
| ci — cross-check pass | ✅ 2026-08-23 EAT ci COMPLETE | `ops/ci_crosscheck.py` → `feeds/ci_crosscheck.json`: 135 citations checked (both estate+sources), **0 dead** (fixed 6 stale: AWS lens/gov.uk x2/ITU/White-House archives/Salesforce + chat.lmsys.org→lmarena.ai); EAT 7-box now **4/7 true** (measured·ci·boarded·mirrored) |
| 62–65, 69 — doctrine audits | ✅ 2026-08-23 | adversarial-evidence ([BET]s all carry inline counter-evidence), public-grammar (measurement-not-certification), naming-quarantine + language-lock (lint gate now scans the live board too), GNN/MLP re-framed as catalogue-benchmarks-not-trust-scores |

## Phase 1 — LEARN & ALIGN (moves 1–10)
1. Daily LEARN: re-read nearest AGENTS.md + master doc §0-§9 before any drum work (stage 1 of MAPE-K).
2. Run `build_catalog.py` after every mining fold; verify counts + hygiene (banned-string scan) each run.
3. Keep all six surfaces version-aligned to the master doc on every change (registry/PACK_INDEX/README/llms.txt/manifest/agent-card).
4. Weekly adversarial review: re-check each [BET]'s disconfirming evidence is still the strongest known.
5. Update feeds (reg_events.json / eat_7box.json) on every rebuild; never let them go stale.
6. Log every lane-status delta (did:web, PRs, pod state) into WIRING §0 with a date-stamped live check.
7. Re-verify the did:web apex↔mirror state weekly; record the reconcile gap honestly.
8. Keep the catalog's internal-item flag + public filter correct on every fold (no banned string leaks).
9. Review mining tray weekly; fold or retire raw files (nothing sits un-sorted).
10. Publish the drum status line to the shared-knowledge intel log at session end.

## Phase 2 — DRUM HARDENING (moves 11–20)
11. Turn the test pass into a committed `tests/test_drum.py` (catalog integrity, dup-ids=0, cards==items, JSON validity).
12. Add a `--check` mode to build_catalog.py: fail loudly on dup ids, missing fields, stale cards.
13. Add a banned-string lint gate (`--lint`): exit non-zero if any public surface carries a codename.
14. Wire the lint gate into the harness ops cron (brand-gate pattern from the master doc §6).
15. Add a canary-string check: catalog.json contains a unique canary; alarms if a public mirror strips it.
16. Improve `drum_crosswalk`: surface estate crosswalk page URLs (5,043 mappings) as link sources.
17. Add `drum_watch` tool: diff two catalog versions → reg-event deltas (drives DORADO reg_events).
18. Add `drum_freshness`: per-item last-verified date + age report (drive the freshness cron).
19. Add pagination + kind filters to drum_search (large-catalog UX).
20. Selftest must cover every tool with edge inputs (empty query, bad id, missing args).

## Phase 3 — STAGE 1: THE CONFORMAL 90/10 ROUTER (moves 21–30)
21. Define the nonconformity score `s(x)`: start with decorrelated ensemble disagreement (3 small models, different data slices/seeds).
22. Build the calibration set from past findings with known outcomes (never arena/benchmark data).
23. Implement split conformal threshold `q̂ = ⌈(n+1)(1−α)⌉`-th smallest calibration score (Vovk; Angelopoulos & Bates).
24. Freeze α at 1–5% auto-proceed error budget; document the choice with the cost model.
25. Freeze the threshold; make the router a pure deterministic predicate `s(x) ≤ q̂ → auto-proceed`.
26. Measure realized coverage on a fresh held-out slice BEFORE trusting the router (benchmark-to-change).
27. If realized error > α → recalibrate or lower α; every recalibration is a signed, logged event.
28. Implement drift monitoring on the score distribution; schedule recalibration (not continuous).
29. Route wiring: 90% → auto-queue next task; 10% → human escalate OR parallel candidate fan-out.
30. Publish the router's measured performance as a signed card (the 90/10 claim, measured not asserted).

## Phase 4 — STAGE 1: THE KNOWLEDGE ARCHIVE (moves 31–40)
31. Stand up the append-only Knowledge archive (residue/copy-and-improve substrate).
32. Content-addressed storage (sha256 key) with lineage fields: inputs, operator, parent, result, decision.
33. Sign every entry with the estate Ed25519 rail (did:web:csoai.org keys) — [GATE] #dsh publish first.
34. Wire the archive as MAPE-K stage 5 (Knowledge) in the drum's own loop.
35. Reuse inspect-receipts core (RFC 8785, content_id recomputable) — no new signing code.
36. Archive every drum fold: catalog version + mining deltas as an entry (the drum eats itself).
37. Implement ancestor re-sampling (DGM island-archive pattern — archive beats always-mutate-latest).
38. Add corrections-ledger semantics: entries can supersede, never delete.
39. Back up the archive off-Mac (Oracle micro / RunPod bundle) per fleet doctrine.
40. Expose archive via MCP (`drum_history` tool) so any agent can query residue.

## Phase 5 — STAGE 1: MAPE-K COLLAPSE (moves 41–50)
41. Rewire the estate's 9-step references to the 5 MAPE-K stages (Monitor/Analyze/Plan/Execute/Knowledge).
42. Cut BRAND/VISUAL/QUALITY from substrate loops; point it at a downstream consumer surface.
43. Update the nine-stage charter doc reference to the collapsed form (alignment, not deletion).
44. Map every existing stage artifact (PDCA loops, orchestrator) onto the 5 stages explicitly.
45. Name the promote-gate boundary in code: Analyze → Execute gate, frozen evaluator, significance test.
46. Make stage 1 (Monitor) real: the drum's mining tray + freshness cron IS Monitor — document the wiring.
47. Make stage 2 (Analyze) real: the conformal router (Phase 3) plugs here.
48. Make stage 4 (Execute) real: the merge-loop executor (Phase 7) plugs here.
49. Make stage 5 (Knowledge) real: the archive (Phase 4) plugs here.
50. Publish the collapsed loop diagram + stage map as a doc section (showable, doctrine-clean).

## Phase 6 — STAGE 2: THE PROMOTE-GATE (moves 51–60)
51. Build the frozen, private, contamination-resistant held-out eval set (canary strings, password-protected).
52. Wire in the UK AISI Inspect eval-receipt package (already run — make it a service).
53. Build the regression pack: P0 known-good/known-bad cases; zero regressions = hard gate.
54. Implement statistical-significance gating vs equal-sized baseline cohort (not raw totals).
55. Add sequential/anytime-valid tests (Netflix-style canary) for early stopping without false positives.
56. Implement shadow-mode on replayed traffic (catches ~40% of regressions sandbox misses).
57. Implement graded canary (1%→5%→20%→50%→100%) with automated rollback triggers.
58. Enforce "never train on evals" in CI (already doctrine — add a guard that checks).
59. Document the promote-gate protocol in the drum (one page, references RESEARCH_VALIDATION §4).
60. Red-team drill: inject a regression; prove the gate catches it before any autonomy expansion.

## Phase 7 — STAGE 2: THE EVOLVE LOOP (moves 61–70)
61. Pick one narrow verifier-rich domain (a code module with strong tests) — the AlphaEvolve precondition.
62. Implement hunt: scan corpus + codebase for structurally similar patterns (signed-receipt ×5 was the proof).
63. Implement generate: candidate variants/combinations (evolutionary, not weight arithmetic).
64. Implement test: fixed evaluator, frozen baseline, scored gate (Phase 6).
65. Implement keep-if-better: promote permanently only on significance; else publish the negative result.
66. Log every candidate with full lineage into the Knowledge archive (Phase 4).
67. Guard against reward hacking: verifier/evaluator/config read-only from the optimizer.
68. Guard against rise-and-collapse: archived champion, never overwrite the best, rollback enabled.
69. Guard against diversity collapse: island/archive model with explicit novelty preservation.
70. Publish the first domain's evolve report: what merged, what was rejected, measured deltas.

## Phase 8 — WIRING LEGS: EAT · DORADO · SOV SIGNAL (moves 71–80)
71. Tick EAT box 3 (signed): emit a real signed h3k/receipt over the catalog via the #dsh rail — [GATE].
72. Tick EAT box 4 (chained): hash-chain drum entries into the sigil chain — [GATE] signing pod.
73. Tick EAT box 5 (anchored): OTS/Bitcoin anchor the drum manifest — [GATE].
74. Tick EAT box 6 (boarded): publish the drum board page (counts, feeds, doctrine links) — [LANE] deploy.
75. DORADO leg: hand `feeds/reg_events.json` to the DORADO lane as the REG_EVENTS sync source — [LANE].
76. SOV SIGNAL leg: hand reg-events as the regulatory-pressure feature channel to the sov_signal lane — [LANE].
77. Market leg: keep `NOT_PRESENT` until a licensed data source exists (Dorado doctrine, §9) — do not shortcut.
78. Enforce the three Dorado boundaries in code review (composed never fused, licensed, never a trading signal).
79. Wire `drum_watch` (move 17) → DORADO reg_events so reg drift re-measures pair-gap automatically.
80. Publish the Destinations map refresh: every leg's status honest, updated with this phase's outcomes.

## Phase 9 — MONOREPO SUBSTRATE (moves 81–90)
81. Execute signed-receipts consolidation: 5 dup copies → one core (spec dated 2026-08-20) — [LANE] K3.
82. Execute the did:web one-PR reconcile: add card-attestation-1 + #dsh to the apex — [GATE] deploy lane.
83. Build `registry/mcp-catalogue.json` (kills the 819/890/966 count drift) — one registry to rule them.
84. Collapse crosswalk ×3 → 1 (packages/csoai-crosswalk as the single impl).
85. Install the 52-article charter as the single canonical charter/ (charter/ is empty today).
86. Build packages/frameworks (FRAMEWORK_GROUND_TRUTH): sync verified items from the drum catalog.
87. Build packages/gspc: 14-slot axes registry + board harness + the missing separation gate.
88. Build packages/regwatch: corpus-watch detector (dedupe org/clawd) + reg-watch-state.
89. Quarantine donor material with banned strings into the internal-only tree (brand-gate in CI).
90. Harvest + retire the shadow copies (csoai-static-deploy2 / kimi-regen / csoai-org-v2 / csoai-platform).

## Phase 10 — SCALE & EAT (moves 91–100)
91. Write the key-continuity charter (a signing-key monorepo needs succession as first-class) — [GATE] Nick.
92. Expand loop autonomy only after move 60's red-team drill passes (the gate caught the injection).
93. Operationalize human+AI allocation: decisions/ambiguity → human; scale/synthesis → AI (task-allocation, not blending).
94. Add the drum's regulation web-sweep recovery to the mining queue (the one sweep that never landed) — [LANE].
95. Budget the evolve loop realistically (~$22k/run at DGM scale); days-to-hours only for narrow verifier-rich tasks.
96. Quarterly adversarial-evidence review: update each [BET]'s counter-evidence with any new literature.
97. Quarterly top-down alignment sweep: every surface re-checked against the master doc version.
98. Publish the drum's honest 7-box EAT score as a public card each quarter (measured, never certified).
99. Onboard OpenCode (installed, MIT) as a flow agent for estate tasks; Cursor/codex not installed (no need to add).
100. EAT: review this list, strike what's done with evidence, renumber, and set the NEXT 100.

---

# NEXT 100 — SET 2 (2026-08-21 · the polish + trust + substrate phases)

> Set 1 (moves 1–40) ate: gates (11–20), router core (21–25), router wiring (26–29),
> measured-labels data layer (30), archive core (31–34) + fold-hook + history (36, 40),
> E2E + overnight + scorecard (this set's polish opened in set 1's tail). Set 2 targets the
> **trust flip** (score), the **7-box mission**, and the **substrate**.

## P11 · POLISH & PERFECTION (the 100/100 pursuit — moves 1–10)
1. Automate the scorecard: `ops/scorecard.py` recomputes docs/SCORECARD.md from live gates (no hand numbers).
2. Card quality pass: every card's effective/status/binding rendered consistently; null → "—" everywhere.
3. llms.txt completeness: add scorecard + overnight runbook pointers; keep it one-shot readable.
4. README parity: verify every listed path exists; dead links zero.
5. Manifest/agent-card parity: versions track the master doc version on every bump (already manual — make it a gate).
6. doc lint: every `docs/*.md` internal cross-reference resolves (script it).
7. Feed polish: reg_events carries east/west/global + binding always; eat_7box boxes carry dates.
8. Card searchability: titles contain the canonical names (no dup-title cards — dedupe by norm name holds).
9. Consistency: catalog counts == cards == feeds counts (already gated in E2E — extend to status card).
10. Release the scorecard as the drum's own "measured current state" card (never certified) — the honest badge.

## P12 · THE TRUST FLIP (the measured score — moves 11–20)

> **OUTCOME 2026-08-21 — NOT ACHIEVED (honest negative result):** moves 11–13 executed —
> 79/79 arena probes real-scored by the 3-model ensemble (llama3.2:3b · qwen3:4b ·
> qwen2.5:1.5b, local Ollama, votes 1–3 per probe). The realized-coverage check (move 15)
> **FAILED**: qhat=0.5, n_cal=47 / n_val=32, **realized error 0.5312 vs α=0.05** — ensemble
> disagreement does NOT predict the human-reference outcome on these legal probes. The
> negative result is published in `feeds/router_trust.json`; `drum_route` now reads the
> marker and reports `trusted: false` (ledger #12 — it previously inferred trust from
> proxy-status alone; fixed before any claim shipped). **Attempt #3 (frontier confidence, Gemini via the estate key):** the rail works (16 scored, model follows the format), then **quota 429 blocked the rest** + a wipe incident (supersede-without-safety-net) fixed with backup/restore + key-to-config (ledger #14). **Next attempts:** majority-confidence
> instead of raw disagreement · fleet models (Oracle 70B / Groq gpt-oss-120b) · retrieval-
> grounded scores; re-run the check; only then flip.
11. Build the ensemble-disagreement score: 3 small decorrelated models score the arena probes; disagreement = s(x).
12. Backfill scores onto the 79 arena measured labels (pre-label features only — never the outcome).
13. Re-run `collect_measured.py` with real scores → measured entries lose score_proxy.
14. Split measured into calibration/validation (e.g. 60/40) — never calibrate on the validation slice.
15. Freeze qhat; run the realized-coverage check on the validation slice (move 27, now with real scores).
16. If realized error ≤ α → flip `drum_route trusted: true` (the card that matters).
17. If realized error > α → lower α or fix the score; publish the negative result.
18. Wire the drift monitor to the ensemble score distribution (scheduled recalibration, signed events).
19. Extend collect_measured to the full 508-round corpus (ai-vs-ai agreement as a second signal once decorrelation is verified).
20. Publish the trusted-router card: measured coverage, n, α, realized error, signature [GATE #dsh].

## P13 · OVERNIGHT & OPS HARDENING (moves 21–30)
21. Overnight: fold git-dirty check → morning report includes uncommitted drum files.
22. Overnight: disk guard — abort if < 2Gi free (estate ENOSPC lessons).
23. Overnight: archive the status card + scorecard as Knowledge entries (the drum eats its own reports).
24. Overnight: alert hook — non-zero gates → marker file + one-line morning scan (no external sends).
25. Standing check: add `e2e_drum.py` to the 15-min verify-only run (currently unit only).
26. Standing check: add scorecard recompute (read-only numbers) so drift in quality is caught.
27. Backup: tar the drum pack to the fleet bundle dir weekly (Oracle micro / RunPod, per fleet doctrine).
28. Restore drill: prove the pack restores from the backup in < 5 min (red-team-lite).
29. Log rotation: cap /tmp drum logs at 1 MB each (avoid the estate's disk-crisis class).
30. Agent registry: record both drum LaunchAgents in ops (label, schedule, log paths) for audit.

## P14 · E2E EXPANSION (moves 31–40)
31. Property tests: for random queries, drum_search returns ≤ limit items and never errors.
32. Fuzz catalog: mutate catalog.json fields; assert MCP tools degrade gracefully (never crash).
33. Concurrency: 5 parallel MCP clients — no interleaved/corrupt responses (stdlib threading test).
34. Long-input tests: 10 MB query string — bounded memory, no hang.
35. Unicode: emoji/CJK regulation names (Korea/Taiwan/Vietnam entries) round-trip through search/get.
36. Router property: route() is a pure function — same (s, qhat) → same decision, 10k trials.
37. Archive property: append-only invariant — counts never decrease across rebuilds.
38. Drift property: alarm fires when live scores shift > threshold; silent when stable.
39. Determinism: build_catalog.py twice → byte-identical catalog.json (minus generated date).
40. Golden-file: hash the catalog; any fold that changes >N items triggers review (contamination guard).

## P15 · MINING COMPLETION (moves 41–50)
41. Regulations web-sweep content: fold or retire honestly (Digital Omnibus/state-wave already in via estate 236-list).
42. Index the meok-compliance-gateway 136-entry MCP registry as a single source-of-truth article (count drift note).
43. Index `_findings/` corpus: scan for named frameworks/charters/regulations not yet in the drum.
44. Space completion: verify EU Space Law status monthly; add COPUOS LTS Guidelines + UNOOSA register pointers.
45. xAI/Grok sector: mine Grok/Preparedness-type capability reporting for the jail/safety axes (measure, never partner).
46. Tesla/AV sector: add UK AV Bill + EU AI Act Annex III road-safety mapping to the tesla-automotive-ai card.
47. Orbital data-centers sector: watch ITU/ISO + EU Space Law for the first binding regime (honest NOT_PRESENT until then).
48. Freshness schema: add per-item last-verified date (move 18's gap) — schema addition + backfill from fold date.
49. Depth: for the top-20 frameworks, add clause-level crosswalk pointers to the estate crosswalk pages.
50. Tray discipline: any `_mining/` file older than 7 days un-folded → auto-flag in the overnight report.

## P16 · WIRING LEGS (the 7-box — moves 51–60)
51. EAT box 3 (signed): first real Ed25519 receipt over the catalog manifest via the #dsh rail [GATE].
52. EAT box 4 (chained): chain fold entries into the sigil chain [GATE signing pod].
53. EAT box 5 (anchored): OTS/Bitcoin anchor the v1.4 manifest [GATE].
54. EAT box 6 (boarded): public drum board page (counts, feeds, doctrine, scorecard) [LANE deploy].
55. DORADO leg: hand `feeds/reg_events.json` (126 events) to the DORADO lane as REG_EVENTS sync [LANE].
56. SOV SIGNAL leg: hand reg-events as the regulatory-pressure feature channel [LANE sov_signal].
57. `drum_watch` → DORADO reg_events auto-wire (reg drift re-measures the pair-gap) [LANE].
58. Enforce the three [Dorado] boundaries in code review (composed never fused · licensed · never a trading signal).
59. Sector cards → GSPC 14-slot registry mapping (space/xAI/Tesla axes) [LANE gspc].
60. Publish the Destinations map refresh with this phase's actual outcomes.

## P17 · MONOREPO SUBSTRATE (moves 61–70)
61. Execute signed-receipts consolidation: 5 dup copies → one core [LANE K3].
62. Execute the did:web one-PR reconcile (card-attestation-1 + #dsh on the apex) [GATE deploy lane].
63. Build `registry/mcp-catalogue.json` — one registry, kills the 819/890/966 count drift.
64. Collapse crosswalk ×3 → 1 (packages/csoai-crosswalk single impl).
65. Install the 52-article charter as the single canonical charter/ (charter/ is empty today).
66. Build packages/frameworks — FRAMEWORK_GROUND_TRUTH synced from the drum catalog (581 items).
67. Build packages/gspc — 14-slot axes registry + board harness + separation gate.
68. Build packages/regwatch — corpus-watch detector + reg-watch-state (feeds drum_watch).
69. Brand-gate in CI — donor material with banned strings quarantined (the drum lint generalized).
70. Harvest + retire shadow copies (csoai-static-deploy2 / kimi-regen / csoai-org-v2 / csoai-platform).

## MODEL-LAYER MILESTONE (2026-08-22) — first promote on the drum's own corpus

> Kind-classification protocol (frozen 80/20, baseline majority, promote-if-better):
> **baseline 0.317 → MLP 0.592 → GNN-lite 0.742** (pure-torch GraphSAGE-style message passing
> on feeds/catalog_graph.json — 596 nodes / 11,035 issuer+region edges; transductive, labels
> train-only). Graph structure genuinely helps. Reports: feeds/corpus_model_report.json +
> feeds/graph_model_report.json. Next tasks attach the GovBench/GSPC findings + arena
> agreement labels; GNN upgrade path to torch_geometric on the pods (ship_to_pod.sh).

## P18 · SCALE (moves 71–80)
71. Key-continuity charter (a signing-key monorepo needs succession) [GATE Nick].
72. Red-team drill: inject a regression; the promote-gate must catch it before any autonomy expands.
73. First verifier-rich evolve domain (a code module with strong tests) — the AlphaEvolve precondition.
74. Shadow → canary with auto-rollback on the promote-gate (Stage 2 build).
75. Task-allocation ops: route decisions/ambiguity to humans; scale/synthesis to AI (the corrected thesis in practice).
76. Budget the evolve loop (~$22k/run at DGM scale) — one approved run [GATE].
77. Days-to-hours proof: measure the drum's own loop latency per stage (Monitor→Analyze→Knowledge).
78. Autonomy expansion only after the drill + gate pass (never before).
79. Multi-domain: second verifier-rich domain once the first shows kept-if-better evidence.
80. Publish the evolve report: merged/rejected candidates with measured deltas (negative results included).

## P19 · GOVERNANCE & DOCTRINE (moves 81–90)
81. Adversarial-evidence review #1: re-check every [BET]'s strongest counter-evidence (quarterly cadence starts).
82. Kill-list lint in CI: the drum lint generalized to the monorepo (brand-gate, move 69's twin).
83. Version discipline: master doc bumps are signed events with a changelog (v1.4 → v1.5 discipline).
84. Amendment drill: propose a change; run the 23/33 BFT ratification path once (dry-run, honest).
85. Public grammar audit: every public surface uses "measurement, not certification" + "13 measured of 14".
86. Dorado doctrine audit: no surface implies a trading signal (the §9 hard line, enforced in copy).
87. Naming quarantine audit: no [bracket] codename on any public surface (lint is the mechanical check).
88. Language-lock audit: no "fully autonomous"/"ASI evolves itself" on public surfaces (master doc §0 locks).
89. Corrections ledger: log every doc correction (this session: split-brain direction, E2E bug, toy-model bug).
90. Doctrine review: Nick signs v1.4 as canonical (the doc's own amendment rule).

## P20 · CADENCE & CONTINUOUS (moves 91–100)
91. Daily: LEARN (read AGENTS.md + master doc §0-§9) before any drum work.
92. Daily: rebuild + gates + archive (the overnight cycle is this — verify it ran each morning).
93. Weekly: adversarial review + did:web re-check + tray fold (Phase 1 moves 4/6/7 cadence).
94. Weekly: scorecard recompute + publish the delta.
95. Monthly: mining depth pass — hunt one new estate corpus (like _findings) for unindexed material.
96. Monthly: cross-lane alignment check — PACK_INDEX/registry/feeds match the master doc version.
97. Quarterly: full adversarial-evidence review + [BET] ledger refresh.
98. Quarterly: 7-box EAT card publish (measured, never certified).
99. Each release: top-down alignment sweep — every surface re-checked against the master doc.
100. EAT: strike what's done with evidence, renumber, and set the NEXT 100 (set 3).

---

*Set 2's spine: the trust flip (P12), the 7-box mission (P16), the substrate (P17). Moves
[GATE] need Nick or the deploy lane; [LANE] needs that lane's owner. Nothing marked done
without output shown.*

---

# NEXT 100 — SET 3 (2026-08-22 · SOV SIGNAL bridge + real tasks + production)

> Set 2 ate the polish/trust/overnight phases. Set 3's spine: **the SOV SIGNAL composition**
> (drum = reference index, SOV SIGNAL = measured gauge — see docs/SOV_SIGNAL_INDEX.md), the
> **real model tasks** (kind 0.592 / binding 0.917 already measured), and **production** (pods).

## P21 · SOV SIGNAL BRIDGE (the reference-index vs gauge composition — 1–10)
1. Honor the distinction: drum = reference index; SOV SIGNAL = measured gauge (done: docs/SOV_SIGNAL_INDEX.md) — enforce on all surfaces.
2. Map the drum's sectors/kinds onto the GSPC 14-slot axis registry [LANE gspc].
3. Define the permitted manifold from the binding charters/frameworks (the drum's binding predicates).
4. Candidate: a measured-gauge smoke — compute a mock Fisher-Rao distance on 10 known items (no trust claim).
5. Wire the NN/GNN feature layer (0.742 GNN) as the gauge's feature input.
6. Add the gauge to WIRING §6 Destinations (drum → feature → manifold → gauge).
7. Document the drum→SOV SIGNAL data contract (what the gauge consumes from catalog.json/features).
8. Add the sector axis mapping to the sector cards (each sector lists its GSPC axes).
9. Continuous: every fold refreshes the feature layer (overnight GNN train already runs).
10. Publish the SOV_SIGNAL_INDEX doc to the catalog (done — indexed as article).

## P22 · REAL MODEL TASKS (beyond kind — 11–20)
11. Binding-prediction task — done 0.917 (de-leaked, promote-gated).
12. Attach the GovBench 12-axis / GSPC axis labels as the next prediction tasks.
13. Attach the arena human-vs-AI agreement labels (80 measured) as a task — the findings layer.
14. Region-classification task (predict jurisdiction from features + graph).
15. Crosswalk-link prediction (predict if two items share a crosswalk — the graph's natural task).
16. Promote-gate the model layer: keep-if-better when a real task beats the MLP with significance.
17. GNN on the pod with torch_geometric (vs the 0.742 local baseline).
18. Publish the model reports (feeds/corpus_model_report.json, graph_model_report.json) as cards.
19. Refactor the trainer into a single `train/run_all.py` (kind + binding + graph).
20. Calibration-vs-benchmark correlation: do the model scores correlate with the estate's measured findings? (the SOV-SIGNAL-feature question).

> **Mining completion (2026-08-22, personal dirs):** Downloads/Documents/Desktop mined (447+ md files, estate operational + research docs) — surfaced ISO 12100, 13849, 17024 (personnel certification — the certification-ladder tie-in). The instrument universe is now covered across every major corpus (clawd, _TABS, proofof, sim-world, kimi-regen, sovereign-charters, personal dirs); 65+ real standards folded across all passes, every one sourced or honestly flagged. The miner's residual hits are known artifacts/noise. **Mining is complete at this depth** — next is a genuinely new corpus only if a new one appears.

> **Mining note (2026-08-22, updated):** NIST IR 8477 was verified + folded (Cybersecurity & Privacy Mapping Guide, verified via NIST/CSRC). The miner's residual ~15 'missing' codes are now known artifacts: already-indexed standards referenced by short form (ISO 27001 vs ISO/IEC 27001, ISO 17020/23894/5259/27701/20000/31000 etc.) plus value-format noise (ISO 8601 date format, ISO 2023 year, ISO 25785/21617 unknown). No genuine un-indexed instrument remains in the scanned corpora; the miner's VALUE is captured. Next mining depth = a fresh corpus (e.g. the sim-world findings, kimi-regen research) rather than re-scanning the same corpora.

## P23 · MINING COMPLETION (21–30)
21. Full `_findings` corpus scan → index genuine instruments (the corpus entry is registered; fold real finds).
22. openpatent-hive vault scan (unindexed governance/defence material).
23. meok-universe + csoai-org corpora scan (space universe, country packs).
24. Sim-world findings corpus scan (the 12-axis sim results).
25. Regulations web-sweep recovery decision — fold or retire honestly (scorecard −4 until resolved).
26. Add `_findings`/`openpatent-hive` to ops/mine_gaps.py CORPORA.
27. Depth pass: clause-level crosswalk pointers for the top-20 frameworks (overweighted by estate use).
28. Freshness schema: per-item re-verification cadence (last_verified is fold-date; add a re-check cadence).
29. Continuous mining cadence: the gap-miner runs weekly; every new find folds into the seed.
30. Index the model/doctrine docs as catalog articles (SOV_SIGNAL_INDEX, catalog-graph-model done).

## P24 · POD / FLEET PRODUCTION (31–40)
31. Ship_to_pod to a LIVE pod [LANE RunPod/Oracle]. 32. torch_geometric GNN on the pod. 33. Nightly training there + report back. 34. Pod-side manifest TEA walk (verify the bundle is intact). 35. Fleet cpu budget for nightly training (cost-register). 36. The measured capability deltas from pod training feed back into the drum (the evolve loop crosses the pod boundary). 37. Multi-pod sync (fleet register). 38. A pod-side self-check script (the drum's gates on the pod). 39. Backup/restore across pods. 40. Publish pod availability in WIRING (SOVOS/CSOAI consume the drum).

## P25 · WIRING LEGS (41–50)
41. EAT box 3 signed [GATE #dsh]. 42. EAT box 4 chained [GATE]. 43. EAT box 5 anchored [GATE]. 44. EAT box 6 boarded [LANE deploy]. 45. DORADO consumes reg_events.json [LANE]. 46. SOV SIGNAL feature channel [LANE]. 47. drum_watch → DORADO reg_events auto-wire [LANE]. 48. Enforce the [Dorado] boundaries in review. 49. Sector cards → GSPC 14-slot mapping [LANE]. 50. Destinations map refresh.

## P26 · MONOREPO SUBSTRATE (51–60)
51. Receipts ×5→1 [LANE K3]. 52. did:web reconcile + #dsh [GATE]. 53. One mcp-catalogue registry. 54. Crosswalk ×3→1. 55. 52-article charter canonical. 56. packages/gspc 14-slot. 57. packages/regwatch. 58. FRAMEWORK_GROUND_TRUTH sync from the drum. 59. Brand-gate CI (the drum lint generalized). 60. Harvest/retire shadow copies.

## P27 · GOVERNANCE & DOCTRINE (61–70)
61. Key-continuity charter [GATE]. 62. Adversarial-evidence review #1. 63. Public-grammar audit ("measurement, not certification"). 64. Naming-quarantine audit (no [bracket] codename on public surfaces). 65. Language-lock audit. 66. Version discipline (bumps = signed events). 67. Amendment drill (23/33 ratification, dry-run). 68. Corrections ledger quarterly review. 69. The GNN/MLP numbers re-framed (catalogue benchmarks, not trust scores — doctrine rule). 70. Nick signs v1.4 [GATE].

## P28 · CADENCE & OPS (71–80)
71. Daily LEARN before any drum work. 72. Nightly: verify the train + TEA walk + align audit ran (morning scan). 73. Weekly adversarial + did:web re-check. 74. Weekly scorecard recompute + delta publish. 75. Monthly mining depth (one new corpus). 76. Monthly cross-lane alignment. 77. Backup restore drill (< 5 min). 78. Log/disk guard (already in overnight — verify). 79. Fleet cost register. 80. The drum's own status card published.

## P29 · SCALE & TRUST (81–90)
81. Promote a real task only after the promote-gate catches an injected regression. 82. Second verifier-rich domain. 83. Budget one evolve run [GATE]. 84. Task-allocation ops (decisions→human, scale→AI). 85. Autonomy expansion only after the drill. 86. Multi-model evaluate the gauge features. 87. The trusted-router path re-attempt (fleet/Gemini after quota). 88. Days-to-hours proof (measure the drum's own loop latency). 89. Cross-manifold measurement (space/xAI sectors). 90. Quarterly 7-box EAT card publish.

## P30 · EAT REVIEW (91–100)
91. Strike set-3 moves done with evidence. 92. Renumber + set SET 4. 93. Publish the drum's honest state. 94. Recompute the scorecard. 95. Re-align every surface. 96. Record the session's corrections. 97-100. EAT: the loop eats, aligns, mines, improves. Forever.

---

*Set 3's spine: SOV SIGNAL composition (reference index vs measured gauge), real model tasks,
production. [GATE] = Nick/deploy lane; [LANE] = lane owner. Nothing marked done without
output shown.*

---

# NEXT 300 — SET 4 (2026-08-22 · POD WORKFLOW + PRODUCTION READINESS + MAC OFFLOAD)

> Directive: all work off the Mac and onto RunPod/Oracle RAG volumes; every aspect production-ready;
> full sweep + clean + improve E2E. Spine: **the drum runs on pods; the Mac is the terminal only.**

## P31 · POD WORKFLOW (the Mac-out-of-the-path doctrine — 1–30)
1. Canonical RAG volume: `/workspace/frameworks-drum` on sov-brain-2 (DONE — 634 items + OOWM index ingested).
2. ship_to_pod.sh targets sov-brain-2 + refreshes the pod OOWM index (DONE).
3. Nightly: push catalog/graph/feeds/features to the pod (the overnight already ships; wire the pod ingest).
4. Training runs on the pod (torch_geometric GNN + the NN tasks) — Mac is inference-free.
5. pod_selfcheck.sh: the drum's gates run on the pod (port align_audit + dualwalk + tests to the pod).
6. Oracle micros as the secondary RAG mirror (oracle-micro-2 reachable).
7. Mac disk guard: keep >2Gi; the drum's caches auto-trim (overnight already; extend to bundles).
8. clawd/.git (3.3G) + deploy2/.git (1.1G) — [LANE] git gc, not purged (red line).
9. The Mac keeps ONLY: the git repo + terminal/browser (per the estate offload directive).
10. Every pod write is content-addressed + TEA-walked (the dualwalk covers the pod manifest).
11–30. (reserve: multi-pod sync, fleet register, cost-register, the pod-side RAG retriever wiring.)

## P32 · PRODUCTION READINESS (31–60)
31. The board = content pages (DONE — index + 5 kind pages live).
32. MCP/A2A = the machine surface (DONE — 8 tools).
33. Feeds = product inputs (DONE — reg_events, gauge_features).
34. Scorecard self-computing (DONE — 87.8 measured).
35. Alignment audit self-enforcing (DONE — every 15 min).
36. TEA backward walk (DONE — every 15 min + nightly).
37. Seed-integrity guard (DONE — tests).
38. Holy-of-sources (DONE — 65+ sourced standards, 2 flagged for verification).
39. Corrections ledger (DONE — 20+).
40. Model benchmarks honest (DONE — kind .65/binding .87/status .854/GNN .691, region rejected).
41–60. (reserve: 100/100 A+++ checklist, publish parity, board SEO/JSON-LD, llms.txt on the pod.)

## P33 · MINING COMPLETION + IMPROVE (61–90)
61. All corpora mined (DONE — clawd, _TABS, proofof, sim-world, kimi-regen, sovereign-charters, personal dirs).
62. 65+ standards folded; residual = artifacts (DONE).
63. Improve: miner → the pod (runs against the pod corpus, not the Mac).
64. Fresh-corpus watch: new Downloads/docs auto-flag for mining.
65. The drum's own research docs (MASTER_FRAMEWORK, RESEARCH_VALIDATION, PHYSICAL_COMPUTATION_MAP) are indexed.
66–90. (reserve: per-item re-verification cadence, depth pass, the SOV SIGNAL axis mapping.)

## P34 · TEST + AUDIT + IMPROVE AGAIN (91–120)
91. Full stack green every cycle (DONE — tests/properties/e2e/scorecard/align/standing).
92. The dual-walk + seed-guard + alignment audit catch regressions (DONE — they've caught 20+).
93. Property/fuzz/concurrency suites (DONE).
94. Backup restore drill (DONE — <5 min).
95. Red-team drill: inject a regression, prove the gates catch it.
96–120. (reserve: pod-side E2E, cross-pod TEA walk, quarterly adversarial review.)

## P35 · EAT FOREVER (121–150)
121. Every cycle: mine → index → graph → train → feature → publish → verify (DONE, auto).
122–150. (reserve: the loop compounds; the drum eats itself nightly, the pod holds the RAG, the Mac stays clean.)

---
## P36 · POD SELF-VERIFICATION + MULTI-POD (151–180)
151. pod_selfcheck.sh: the drum's gates run ON the pod (catalog parse, lint, dualwalk, ingest). 
152. Ship it + run on sov-brain-2 (the pod verifies itself nightly).
153. Pod-side TEA walk: the bundle's MANIFEST.sha256 re-verified on the pod (content integrity across the wire).
154. Oracle micros mirror the RAG volume (oracle-micro-2 reachable).
155. Multi-pod sync via the fleet register (config, not code).
156. Pod cost-register (RTX 3090 $/hr tracked — fleet doctrine).
157. The pod corpus-watch: new drum pushes auto-flag for pod ingest.
158. Pod-side training cadence (torch_geometric GNN nightly on the GPU).
159. Pod report-back: measured deltas flow into the drum (the evolve loop crosses the pod boundary).
160–180. (reserve: pod alerts, pod disk guard, pod backup/restore.)

## P37 · PRODUCTION HARDENING (181–210)
181. Red-team drill (DONE — 4/4 regressions caught, tests/redteam_drill.py).
182. llms.txt on the pod + board.
183. Board SEO: JSON-LD + canonical + llm.json companions (DONE; verify parity).
184. Publish parity gate: the deployed board == the local site (hash check).
185. The 100/100 A+++ measured checklist (scorecard, not self-grade).
186. A public status card (measured, never certified).
187. Sitemap for the board pages.
188. Monitoring: board uptime + pod health in the standing check.
189–210. (reserve: CDN, edge cache, rollback playbook.)

## P38 · TRUSTED-ROUTER RE-ATTEMPT (211–240)
211. The coverage check failed 3× (small-model disagreement, text, Gemini-quota) — all honest negatives.
212. Next score: majority-confidence via the pod's fleet models (Oracle 70B / Groq gpt-oss-120b) [LANE].
213. Retrieval-grounded score: does the answer match the retrieved statute? (the estate's own finding: base model + statute retrieval beats weight-merge).
214. Re-run collect_measured with the real score.
215. Re-run the coverage check; flip trusted only if realized error <= alpha.
216. The flip is [GATE]-free once a score passes — it is the model-layer's honest end.
217–240. (reserve: calibration-set growth, drift recalibration schedule, the trusted card.)

## P39 · WIRING + MONOREPO (241–270)
241. EAT 7-box legs (signed/chained/anchored/boarded) [GATE #dsh + deploy lane].
242. DORADO consumes reg_events.json [LANE].
243. SOV SIGNAL feature channel [LANE].
244. Monorepo: receipts ×5→1, one registry, crosswalk ×3→1, 52-article canonical, gspc, regwatch [LANE].
245. did:web reconcile + #dsh [GATE].
246–270. (reserve: brand-gate CI, harvest shadow copies, key-continuity charter.)

## P40 · EAT FOREVER (271–300)
271. Every cycle: mine → index → graph → train → feature → publish → verify (auto).
272. The drum eats itself nightly; the pod holds the RAG; the Mac stays clean.
273. Quarterly adversarial-evidence review.
274. Quarterly 7-box EAT card publish (measured).
275. The corrections ledger reviewed quarterly.
276–300. (reserve: the loop compounds; each cycle either finds something new or confirms honesty.)

---
*THE FULL 300 (SET 4, P31–P40). DONE this pass: red-team drill 4/4, pod RAG volume + OOWM
ingest, Mac offload, ship-to-pod, full-stack front end, mining complete, model layer honest.
Remaining = the [GATE]/[LANE] tail (wiring, monorepo, trusted-router score) + the reserved
hardening moves. Nothing marked done without output shown.* (pod multi-region, cost, the trusted-router
re-attempt, the 7-box EAT legs, the monorepo substrate). [GATE]/[LANE] as before. The drum now
runs on pods; the Mac is the terminal. Production-ready = the board live, the RAG live, the
gates self-verifying, every claim measured.*
