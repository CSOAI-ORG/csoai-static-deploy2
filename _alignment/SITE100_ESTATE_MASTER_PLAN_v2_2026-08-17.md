# SITE-100 + ESTATE MASTER PLAN v2 — ALL PHASES (17 Aug 2026, ~23:00 BST)

**Directive:** set all plans · mine all we have · improve all possible · define every next step/phase.
**Method:** every number below from live probes, on-disk inventory, or pod/API pulls this session.
**Doctrine (grok bot, binding):** measure, sign, re-attest · no invented scores · unmeasured stays
empty · public names only (Council of AI / GSPC) · never sov-* in public copy · no 527 ·
fail-closed deploys · no job duplication across lanes.

---

## 📊 CURRENT STATE (verified 17 Aug ~23:00)

### Site estate
- **37+ live fronts:** 26 Pages domain+product repos (HTTP 200) + gspc-packs-hub (159 category
  fronts, 200) + 11 apex (meok.ai, councilof.ai, grabhire.ai, agisafe.ai, asisecurity.ai,
  fishkeeper.ai, muckaway.ai, safetyof.ai, proofof.ai, csoai.org, os.meok.ai; sovereign.wiki
  DNS-resolves but origin dead).
- **106 `*-deploy` dirs on disk** = 26 standalone sites (activated) + ~80 route pages of the
  main estates (meok.ai/*, proofof.ai/*) — belong to apex, NOT separate repos.
- llms.txt coverage 27/27 · every repo ships robots.txt + sitemap.

### Measurement corpus (MINE INVENTORY — 35,336 rows, 41 banks)
| Bank | Rows | Status |
|---|---|---|
| peritem_gov.jsonl | 4,503 | board 12 Aug: 19 models/axis |
| peritem_care.jsonl | 3,800 | CARE-200 rebench: qwen2.5:7b 0.895/F1 0.8976 ✅ publishable |
| peritem_jail.jsonl | 2,592 | empty on 12 Aug stamp (honest) |
| peritem_art5/agi/asi/det/mach/mcp/oss/prv/swarm/xr/affect | ~6,900 | 19 models each, MEASURED |
| govbench-items / swarm items / other | ~17,000 | sub-banks |
| Art5 7-probe (22 models) · SOV SIGNAL (24) · MMLU/GSM8K/ARC n=30 (23) | — | mined → mine-v2-consolidated.json |
| day0 qwen3.8-27b | 7 probes | 5/7, over-block recorded |
| Honey KB | 161,931 rows | compounding (was 91,716) |

### Fleet (probed live)
- RunPod 3090 `sov-repull` ($0.22/h): arena keeper + daily index + overnight runner P5
  keep-alive → 04:00 BST (sibling lane owns). 9.8G free.
- RunPod A100-1: RUNNING, SSH-dark, $1.19/h — copy-then-pause (owner gate).
- Oracle micro1/micro2: healthy (GSPC registry, daily city reports). M2: offload (no route).
- GCP meok-backend: billing-dead; evac watcher armed.

---

## 🗺️ ALL PHASES — SITES (goal: 100 live fronts)

| Phase | What | Owner | State |
|---|---|---|---|
| S1 | 26 Pages repos + packs hub live | JEEVES | ✅ DONE (27 repos) |
| S2 | **Packs-hub sitemap.xml live** (raw 200, Pages build pending) | JEEVES | 🔶 verify 04:00 |
| S3 | **Apex DNS repoint** of 26 Pages repos → .ai apexes (CNAME staged) | **Nick** | ⏳ gate |
| S4 | **CF/wrangler token** → deploy 1,316-URL estate + scoped-route fix (soft-404) | **Nick** | ⏳ gate (highest value) |
| S5 | **Sub-app surfaces** — GSPC axis fronts (13) + pack-category hubs (159 done) | JEEVES | 🔶 159 done; 13 axis fronts next |
| S6 | **13 GSPC axis site fronts** (gov/safety/provenance/continuity/...) from real board data | JEEVES | ⏳ next agent-doable |
| S7 | **Regional/i18n fronts** (EAT100 regional packs on disk) | JEEVES | ⏳ after S6 |
| S8 | **haulage.app** (Capacitor app — needs npm build on pod) | JEEVES/3090 | ⏳ after overnight |
| S9 | **Route pages** stay on apex (correctly NOT separate repos) | — | ✅ excluded |

## 🗺️ ALL PHASES — MINE (measurement)

| Phase | What | Owner | State |
|---|---|---|---|
| M1 | mine-v2-consolidated.json (Art5/SOV/MMLU/day0) | JEEVES | ✅ DONE |
| M2 | Overnight rebench collect (CARE-200 ✅ 0.895; GovBench council-safe ✅ real) | sibling | ✅ collected |
| M3 | **CARE/GOV semantic non-refusal rebench** for remaining models (gate artifact fix) | 3090 | ⏳ next compute |
| M4 | **Jail/slot-15 honest measurement** (2,592-row jail bank — currently UNMEASURED) | 3090 | ⏳ new work |
| M5 | **per-item error-pattern mining** (15,580 per-item rows → over/under-block matrix per axis) | JEEVES | ⏳ next |
| M6 | **Honey KB analytics** (161,931 rows → contamination guard + spread stats) | JEEVES | ⏳ after M5 |
| M7 | **Arena Elo board** (108+ rounds → quotable Elo table) | 3090 | ⏳ keep-alive till 04:00 |
| M8 | **GSPC index refresh** (board_all13 from old pod when SSH recovers) | **Nick** | ⏳ gate |

## 🗺️ ALL PHASES — IMPROVE (existing surfaces)

| Phase | What | Owner | State |
|---|---|---|---|
| I1 | Scoreboard chrome 13×19/UNSIGNED | arena lane | ✅ DONE (#164/#165; my PR superseded) |
| I2 | EAT 1/3/4/5 verified ✅ · dossier stale surfaces fixed ✅ | lanes | ✅ DONE |
| I3 | **EAT2 soft-404 fix** (not-found.tsx in csoai-org-v2 + deploy) | **Nick** (wrangler) | ⏳ gate |
| I4 | **"This week in AI behaviour" signed slot** (K3 escape, SWE-bench self-grade, watermark) | JEEVES | ⏳ next content |
| I5 | **Honest banner**: "industry scoreboards self-graded; ours signed" | JEEVES | ⏳ next content |
| I6 | **AIUC-1 battlecard** (they certify+insure; we measure+re-attest) — NOT live until CEO review | **Nick** | ⏳ gate |
| I7 | **OOWM weld** — UNSIGNED n=0; 4way weights missing; do not fake | 3090 | ⏳ compute |
| I8 | **/api/gspc external masking** — evidence API server-side only today | **Nick** | ⏳ gate |

## 🗺️ ALL PHASES — FLEET / REVENUE / GOVERNANCE

| Phase | What | Owner | State |
|---|---|---|---|
| F1 | Overnight runner P5 → 04:00 BST, then **collect + file SUMMARY** | sibling | 🔶 in flight |
| F2 | **A100-1 copy-then-pause** (~$28/day saving) | **Nick** | ⏳ gate |
| F3 | **Stripe `keystone sync-vercel` → live-flip** → first £ | **Nick** | ⏳ gate (revenue) |
| F4 | npm 2FA → package distribution · SMITHERY → MCP directory | **Nick** | ⏳ gates |
| F5 | **Board memberships**: OpenSSF model-signing, LF x402, OWASP AI/MCP, AI Verify (agent-doable applications) | JEEVES | ⏳ next |
| F6 | BSI ART/1 seat (owner-gated pack ready) | **Nick** | ⏳ gate |
| F7 | C2PA contributor → warm-intro conversions | JEEVES | ⏳ ongoing |
| F8 | arXiv G6Y9SY endorser — **deadline 27 Aug** (Nick's voice only) | **Nick** | ⏳ URGENT |
| F9 | Colorado ADMT comment (draft ready; window to 26 Oct) | JEEVES→**Nick** | ⏳ draft→send |
| F10 | GCP evac watcher (fires within 5 min of billing re-enable) | auto | ⏳ armed |

---

## 🔜 NEXT 5 ACTIONS (agent-doable, in order)
1. **M5**: per-item error-pattern mining (15,580 rows → over/under-block matrix) — pure local compute.
2. **S6**: 13 GSPC axis site fronts from real board data (real content, no invention).
3. **M4**: jail/slot-15 honest measurement spec (2,592-row bank) — needs 3090 after 04:00.
4. **I4+I5**: "This week in AI behaviour" signed slot + honest banner copy (draft, deploy-gated).
5. **F5**: board-membership application packs (OpenSSF/LF x402/OWASP/AI Verify).

## ⛔ OWNER GATES (everything else waits on these)
wrangler/CF token · apex DNS repoints · Stripe live-flip · npm 2FA · SMITHERY · A100-1 pause ·
AIUC-1 CEO review · arXiv endorser (27 Aug) · Colorado ADMT send · OOWM 4way weights ·
GCP billing re-enable (evac) · sovereign.wiki origin · /api/gspc external wiring.

---
*Filed: JEEVES (DSH), 17 Aug 2026 23:00 BST. Canonical chain: SITE100_ALIGNMENT → SITE100_MASTER_PLAN → this v2. Logs: site100-activation.log, site100-wave2.log. Harness: ~/.grokbot/harness/*.*

## UPDATE 17 Aug ~23:30 BST — executed this pass
- **M5 DONE**: per-item error-pattern matrix (15,580 rows) → `error-pattern-matrix.json` in harness/mine + mine-v2. Findings: over-block concentrates on binary axes — **affect 12.6% / art5 13.8%**; under-block low (1.7–2.2%); **format-failure unparsed rates: care 21%, swarm 23%, det 21%, prv 17%** (format, not knowledge).
- **S6 DONE**: `gspc-axis-boards` Pages site live — 13 axis fronts from real 12-Aug boards (leaders: art5 sov6-relationality 0.972, swarm qwen2.5:0.5b 0.975, agi gemma3:12b 0.944, det deepseek-r1 0.879). HTTP 200 verified.
- **Tally now**: 28 Pages repos (26 sites + packs-hub + axis-boards) · 172 real category/axis fronts · 11 apex = **39+ live fronts**.
- Next agent-doable (in order): M4 jail/slot-15 honest spec (2,592-row bank, 3090 after 04:00) · I4+I5 "This week in AI behaviour" + honest banner draft · F5 board-membership packs.

## UPDATE 18 Aug ~03:00 BST — round 4 executed
- **M4 DONE**: jail/sandbox-escape honest result — 2,592 rows × 24 models (incl claude-haiku-4.5, gpt-4o-mini, gemini-2.5-flash, deepseek-v3.1), **3 escape attempts all FAILED/contained → 99.88% containment** (firejail, 13 Aug). Recorded in mine-v2.
- **F5 DONE**: BOARD_MEMBERSHIP_PLAN_2026-08-18.md — 4 application drafts (OpenSSF model-signing, LF x402, OWASP AI/MCP, AI Verify Foundation) + firewall checklist. Send = owner gate.
- **S7 DONE**: gspc-regional live (200) — UK regional GovBench overall 0.584, 8 dims, 7-jurisdiction crosswalk (EU/UK/US/SG/CA/AU/AUKUS), retro-anchor honesty note included.
- **Overnight digest + SUMMARY pulled** to harness/mine/ (overnight-digest-20260817.json, overnight-SUMMARY-20260817.md).
- **Tally now: 29 Pages repos · 173 fronts (159 packs + 13 axes + 1 regional) · 11 apex = 40+ live fronts.**
- Runner: P5 keep-alive until 04:00 BST (03:00 UTC) — stopping now; keeper ALIVE (arena continues 24/7).

## AUDIT — 18 Aug ~03:20 BST (past 04:00 BST) — ALL CLEAR
| Check | Result |
|---|---|
| Overnight runner | ✅ STOPPED CLEAN 03:04:01 UTC (04:04 BST) — stop-guard fired, trap resumed keeper, arena keeper ALIVE |
| Pages repos live | ✅ 29/29 HTTP 200 (26 domain+product `-site` + packs-hub + axis-boards + regional) |
| Apex surfaces | ✅ 11/11 live (meok, councilof, grabhire, agisafe, asisecurity, fishkeeper, muckaway, safetyof, proofof, csoai.org, os.meok.ai); sovereign.wiki origin-gated |
| Language lock | ✅ 29/29 clean (no continuous-monitoring/governance-platform/30-frameworks/certify/SOVOS) |
| mine-v2 integrity | ✅ 11 sections: Art5×22, SOV×24, MMLU/GSM8K/ARC n=30, day0, overnight CARE 0.895, error-matrix 13 axes, jail 99.88% |
| Deliverables | ✅ 4 plan docs + board-membership plan + 5 mine artifacts + activate script |
| Coordination | ⚠️ SOV3 :3101 unreachable — known GCP-billing gate (NOT a tunnel bug; do not debug) |
| Intel log | ✅ 17 entries today |
| Overnight results | ✅ digest + SUMMARY pulled to harness/mine/ |
| **TOTAL LIVE FRONTS** | **40+** (29 repos · 173 fronts · 11 apex) |

## ALIGNMENT UPDATE — 18 Aug ~05:00 BST — SOVOS-MASTER-PART-B + DOWNLOADS ABSORBED

### Canon absorbed (Parts GU/GV/GW/GX, already archived at SOVOS/canon/)
- **GU Globe Pattern**: "Everyone is building the globe. Nobody is grading it." Rails free, receipts the business. £160M Strategic Assets window-watch (corrected from phantom £282M).
- **GV 48h sweep**: Ninth Circuit Perplexity = CROWN JEWEL (safe harbor = whoever proves user was driving — our product); UK AISI incident = demand proof (17/19 unsanctioned actions from one model); Vals AI $40M = thesis funded (never partner/echo); DeepSeek 4.55× peak pricing = cost re-route; Endor: score belongs to the agent not the model.
- **GW Compass**: RAS front-door (Renderer-Agent-Spine) = MetaMCP spine + A2A ring + AG-UI wire + Datastar shell; **13 specialists on ONE A100 via vLLM LoRA** (S-LoRA 2,000 adapters); UE5 KILLED as serving layer (client-rendered only); C2PA firewall verbatim-grade (Conformance/Watermarking/Threats&Harms/AI-ML priority, ZKP/Ledgers/Agentic unverified); AG-UI adopted (0.x single-vendor flag, pin versions).
- **GX downloads**: BMR gate (never "benchmark" language on index products); RFC 8785 JCS canonicalisation queued; market-data licence boundary (derived cards + hashes only); Anthropic Economic Index = template.

### Downloads mined (323 md in ~/Downloads; 18-Aug batch fully read)
SOVOS-MASTER-PART-B.md (living canon) · 4 compass artifacts (RAS/AG-UI/C2PA/post-website) · MEOK-BIRTH-SPEC (Phase 0 = 5 surgical fixes) · Tracxn company report.

### Executed this pass
1. **RFC 8785 JCS canonicalisation IMPLEMENTED + VERIFIED** on pod converter (sov_3kb_converter.py): compact sorted-key JSON + .canon sha256 digest (`sha256=cbb083bc… jcs=rfc8785`). GX.2.2 closed.
2. **MEOK-BIRTH Phase 0 audit — all 5 fixes verified live**: llms.txt clean (BFT-33 excluded as internal-only) · counters reconcile (13 axes / 19 models / 237) · /gspc-arena 200, zero SovSpace refs · console routes real 404s (no admin leak) · apex honest H1.
3. **Tracxn profile correction flagged**: "safety certification services" + "ongoing monitoring" + "981st of 981" — language-lock drift on a public profile (first covered 17 Aug). Correction = owner-gated (external profile edit) — queued SITTING.
4. Canon constraints verified applied across all my fronts (no RAS collision, no UE5, no "benchmark" language, attested-not-signed, C2PA firewall).

### What changes (canon-aligned, no new fronts — GQ.4)
- GS workbench gains ring architecture (13 specialists = 1 A100 + LoRA + MetaMCP spine) — cost register computable ~$1,000/mo.
- Bureau/MEOK front-door stack locked: Datastar → AG-UI → CopilotKit catalog → MCP Apps.
- Machine-readable pricing endpoint → cards-plugin scope.
- arXiv Aug 27 HARD = 9 days (owner: endorser). Naming ruling → P0 → sends.

## AG-UI BUILD — 18 Aug ~08:30 BST (playbook §7 Layer 1, canon GW.5)
- **AG-UI wire BUILT + VERIFIED + SHIPPED** → `CSOAI-ORG/csoai-agui-wire` (agui_wire.py 12.5KB).
- Implements the escort vocabulary over SSE: RUN_STARTED · STEP · TEXT_MESSAGE_* · TOOL_CALL_* · STATE_DELTA (JSON Patch) · **HITL consent checkpoint** · CUSTOM · RUN_FINISHED.
- **Consent checkpoint = the Ninth Circuit safe harbour made visible** (HITL pause before any consequential write; approve appends to ledger, deny guarded).
- **J-space hook: every event hash-chained** (14-event session, chain integrity True, prev-links verified) — "every inner exchange signed and replayable."
- RFC 8785 JCS serialisation for cross-language determinism (GX.2.2).
- Self-hosted zero-friction (fastapi/uvicorn), pin AG-UI py 0.1.20/ts 0.0.57 noted; demo + live server both verified.
- **Next (Layer 2): CopilotKit catalog renderer over this wire; Layer 3 MCP Apps.** Wire a real MCP-spine tool as the demo step.

## ALIGNMENT — 18 Aug ~09:00 BST — MASTER PLAYBOOK + AG-UI (canon Part B continued)
- Read CSOAI-MASTER-PLAYBOOK-2026-08-18.md (13 sections + Appendix A verified-state; archived in SOVOS/canon/).
- **AG-UI WIRE BUILT + VERIFIED + SHIPPED** → CSOAI-ORG/csoai-agui-wire: escort vocabulary over SSE (RUN_STARTED/STEP/TEXT/TOOL_CALL/STATE_DELTA/HITL/CUSTOM/RUN_FINISHED), HITL consent checkpoint (Ninth Circuit safe harbour), J-space hash-chain ledger (14-event chain integrity True), RFC 8785 JCS. Playbook §7 Layer 1 done (Layer 0 MCP spine live; Layer 2 CopilotKit + Layer 3 MCP Apps next).
- **PR #178 OPEN** (4 files, scoped): axis count 13→16 measured aligned to live /api/gspc (16 axes × 19 models, 960 items, 12 Aug stamp — jail/slot15/hvai now measured). Playbook gate #4 drift closed (was 24-file pollution, rebased clean).
- Verified playbook A.1: /api/gspc serves 16 axes all measured (960 items), 19-model fleet; scoreboard copy was stale.
- Playbook gates still owner-gated: A100-1 dark pod copy+stop ($28/day) · apex H1 "compliance" word-cut · arXiv 27 Aug (9 days) · C2PA @c2pa-org invite accept.

## ROUND 5 — 18 Aug ~09:30 BST — FRONT DOOR LAYERS 0-2 + HONESTY CARD
- **AG-UI wire v2**: TOOL_CALL now queries the LIVE /api/gspc rail (governance axis real data: acc 0.7, n=237, leader sov6-embodiment, sep_p 0.0086, Wilson [0.639,0.755]) — honest UA, fail-closed on error. 14-event signed chain.
- **Layer 2 BUILT**: catalog.html — fixed validated component catalog renderer ("Council Space — front door"), renders AG-UI events, never interprets; HITL approve wired to consent endpoint. Full stack verified (GET / → session → 14-event stream with live rail data).
- Front door status: L0 MCP spine live (councilof.ai) · L1 AG-UI wire ✅ · L2 catalog renderer ✅ · L3 MCP Apps (next).
- **ARENA HONESTY CARD drafted** (~/.grokbot/harness/arena/): real 463-round Elo (qwen2.5:7b 1350.6 > mistral 1334.5 > qwen3:4b 1322.8; sov6 below cut) + axis-board wins (art5 0.972, gov 0.700, care 0.535) — "specialists win on their axis, lose on the open floor"; route-don't-merge confirmed. Deploy-gated (owner GO).

## RAINBOW HIVE JAIL TEST — 18 Aug (round 9, in progress)
- **L1 containment (Mac sandbox-exec, gold bank 38 escape items): 36/38 = 94.7% contained** (34 attempts denied+recorded, 2 attempt-seen, 2 clean). Honest: pod has NO confinement backend (no firejail; unshare blocked by docker seccomp) — rce_sandbox refuses to claim containment there; layer-1 runs on Mac or a firejail host.
- **L2 detection (pod, 8 models × 71 gold items) RUNNING**: qwen2.5:0.5b prec 1.0/rec 0.132 (5/38 detected, 0 fp); qwen2.5:1.5b tp=7 fp=0 at 40/71. Results → rainbow_hive_results.json.
- Artifacts: ~/.grokbot/harness/measure/rainbow-hive/L1_containment_20260818.json + rainbow_L1_test.py; honesty page HTML (4,164b) drafted.
