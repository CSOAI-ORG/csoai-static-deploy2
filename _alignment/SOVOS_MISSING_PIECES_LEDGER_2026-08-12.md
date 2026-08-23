# SOVOS MISSING-PIECES LEDGER — 2026-08-12

**Mined on-disk 2026-08-12** (Claude Code / Opus lane), part of the "mine all else SOVOS needs" sweep.
Spec-vs-shipped enforced: DESIGNED/STAGED never counted as SHIPPED. SOVOS = the sovereign OS / measured universe;
sov34/sov4 are models *inside* it, not SOVOS itself. Every item is grounded in a disk path or live probe;
"no evidence found" is marked where a claimed artifact is absent.

> Provenance: produced by a background research agent that read `_alignment/*` (Aug 8–11), `SOVOS/*`, the
> MEOK/SOV3 ledgers + memory, grepped gap markers, and ran read-only live probes. Part 2 (measurement/parity)
> appended below when that miner lands.

**Clock:** ProvBench public gate = **14 Aug (2 days out)**; must ship with zero P0s. RunPod runway ~$82 (STATUS_2026-08-11).

## Stale blockers now CLEARED (don't re-work)
- **csoai.org outage** — RESOLVED. apex + www → `301 → councilof.ai` live. (Residual apex-hosting gap survives — Infra 1.2.)
- **Sovereign-dock crash** (`AISystemNotice is not defined`) — `client/src/components/AISystemNotice.tsx:18` now has a default export. Verify via smoke suite.
- **Trust-badge overclaims** (SOC2/99.99% SLA) — reframed honestly: `EnterpriseTrust.tsx:1,38` disclaims unheld badges; `trustWall.ts:36` marks SOC 2 `kind:"align"`.
- **Counter drift** — `councilof-ai/counters.json` now canonical (`canon_version 1.0.1`). Verify propagation into rendered copy.

## (1) INFRA / DEPLOY
- **1.1** No stable/persistent GPU; both paths need off-sandbox fixes (sov-brain-2 SSH stale = Nick UI; Modal gRPC `multidict` = sibling env). Evidence: `SOVSPACE_TOPDOWN_2026-08-10.md:44`. **Nick-gated + sibling.** (RunPod reachable via runpodctl intermittently — gap is durability.)
- **1.2** csoai.org apex is a redirect, not a host; NS still Namecheap. Evidence: `cron-diagnostics/csoai-org-apex-error-1034-2026-08-10.md`. **Nick-gated** (NS move).
- **1.3** Canonical-source drift: MASTER_MANIFEST says 38 pkgs, disk has 49, STATUS says 17 on Mac, pyproject has 115 refs. Evidence: `SOVOS/MASTER_MANIFEST.md:16`. **Executable** (regen manifest).
- **1.4** SOVOS `api/` is Vercel serverless; Vercel dead in estate (402). Evidence: `SOVOS/MASTER_MANIFEST.md:148`. **Executable** (port to CF Pages/Workers).
- **1.5** Pod `/workspace` disk exhaustion + idle A100 burn. Evidence: `RUNPOD_ONLY_REALIGN_2026-08-10.md:34,122`. **Executable** (reclaim/stop).
- **1.6** Watchdog has no out-of-band alert (voice alert failed silently ~4h). Evidence: `INCIDENT_csoai_org_2026-08-10.md:37`. **Nick-gated** (pick channel) — 5-line fix.

## (2) MEASUREMENT / DATA
- **2.1** ProvBench has ZERO external replication + T-14 C2PA/CAI notice unshipped — public gate 2 days out, LAUNCH_HOLD ON. Evidence: `TUI_DISPATCH_BOARD_2026-08-09.md:150`. **Blocked-external + Nick-gated.**
- **2.2** No sovereign model has a measured capability win (base Qwen2.5-1.5B beats every sovereign on 9 gov axes). Evidence: `SOVSPACE_TOPDOWN_2026-08-10.md:76`. **Executable** (reposition to refusal/safety, or land real merge).
- **2.3** SOV SIGNAL 4.21σ is a single (target,reference) pair, not multi-reference. Evidence: `SOVOS/REAL_MEASUREMENT_2026-08-11.md:68`. **Executable** (GPU).
- **2.4** sov34 care-battery PROTECT (0.97 vs 0.45) was TRAIN-ON-TEST (held-out n=0); 39% unparseable rate. Evidence: `meok-one/sovos/evidence/sov34-unparseable-rate.json`. **Executable** (re-measure clean).
- **2.5** inspect_evals submission not made; no arXiv preprint / pinned inspect_ai task. Evidence: `TOPDOWN_ALIGNMENT_20260810.md:17`. **Executable** (fabricated arXiv IDs banned).
- **2.6** 6/12 GSPC axes are single-sample n=33-34. Evidence: `SOVSPACE_TOPDOWN_2026-08-10.md:197`. **Executable** (GPU).
- **2.7** Harness sensitivity not frozen (art5 swung 0.53↔0.67). Evidence: `TUI_DISPATCH_BOARD_2026-08-09.md:148`. **Executable.**

## (3) MODEL / ARTIFACT
- **3.1** SOV4-T / SOV4-OWEM adapter weights not on any reachable pod (only docs). Evidence: `MASTER_MANIFEST.md:240`. **Blocked-GPU.**
- **3.2** sov34 weights not on pod (only Modelfiles/logs/jsonl) — can't re-measure 2.4. Evidence: `SOVOS/STATUS_2026-08-11.md:40`. **Blocked-GPU.**
- **3.3** 4-way TIES merge (`oowm-4way`) runs but outputs garbage (`??????` on 2+2). Evidence: `SOVOS/EAT_ALL_2026-08-11.md:18`. **Executable** (λ/density sweep on A100).
- **3.4** sov33-unified merely ties base (no lift); route-don't-merge proven (D214). Evidence: `RUNPOD_ONLY_REALIGN_2026-08-10.md:80`. **Executable** (real-base merge).
- **3.5** Visual/holographic SOVOS layer = 0 code (CPOLink is a datasheet model). Evidence: `CPO_VISUAL_STACK_MINE_2026-08-11.md:15`. **Blocked-research** (never claim present).
- **3.6** Mamba-3 / ITQ3_S not installed; "Qwen3-235B @1.58-bit on 16GB Mac" unverified. Evidence: `SOVOS/STATUS_2026-08-11.md:44`. **Owner-gated.**

## (4) GOVERNANCE / LEGAL
- **4.1 [P0]** Retracted BFT/23-of-33 quorum + "court-admissible" claims STILL in shipped UI (`CouncilVote.tsx:9`) and a PAID passport tool. Evidence: `TUI_DISPATCH_BOARD_2026-08-09.md:146`. **Executable** (strip) — hard ProvBench-gate P0.
- **4.2** No contest/appeal procedure; `CONTEST.md` assigned but absent on disk. Evidence: `TUI_DISPATCH_BOARD_2026-08-09.md:102`. **Executable** (one page).
- **4.3** Refusal-gate false-negative rate not measured-and-declared on any public surface. Evidence: `legal-gates-widen-only-via-counsel` memory. **Executable (measure) + counsel-gated (widening).**
- **4.4** DEFONEOS drift: 11 bare `defoneos-*` packages outside doctrine. Evidence: `DEFONEOS_COMPARTMENT_AUDIT_2026-08-10.md:22`. **Nick-gated** (Path A/B/C; rec B).
- **4.5** Open founder/legal decisions (Honey Credits form, two-Ltd incorp, sovos.ai ownership, "33" mark, cofounder-vs-advisor, BrowserOS AGPL, "auto-regulation" overclaim→"evidence tooling for supervisors"). **Nick-gated.**
- **4.6** `DNS_STATE.md` lesson doc never written (DNS failure recurs). Evidence: `TUI_DISPATCH_BOARD_2026-08-09.md:90`. **Executable** (one page).

## (5) REVENUE / OPS
- **5.1** £0 signed revenue; `sk_live_` rotation is the revenue wall (checkout 500s). proofof.ai sells "£299/mo compliance verdicts" on an overclaim → reframe to "measurement evidence." Evidence: `SOVSPACE_TOPDOWN_2026-08-10.md:124`. **Nick-gated + executable (copy).**
- **5.2** NVIDIA Inception credits ($10-25K) blocked on 2nd @csoai.org mailbox. Evidence: `WEIGHT_REGISTER_2026-08-09.md:36`. **Nick-gated** (couples to 1.2).
- **5.3** Grant funnel time-boxed + partner-blocked (Eurostars needs 1 EU partner; Innovate UK Phase 2 needs a university partner). **Nick-gated.**
- **5.4** HF meok-org membership staged but unfired; blocks ossbench sov34 card csoai→meok. Evidence: `SOVSPACE_TOPDOWN_2026-08-10.md:128`. **Nick-gated.**
- **5.5** RunPod burn hygiene: ~$82 runway; standby=1 workers billing at zero jobs. Evidence: `STATUS_2026-08-11.md:91`. **Executable (zero standby) + Nick-gated (top-up).**
- **5.6** Opt-in outreach funnel not built (mass-send prohibited). Evidence: `OUTREACH_100_PEOPLE_100_PLAYS_2026-08-08.md`. **Executable** (build funnel).

## TOP 5 MOST CRITICAL
1. **ProvBench external replication + T-14 C2PA/CAI notice** — 14-Aug gate 2 days out, LAUNCH_HOLD ON (2.1). *Blocked-external + Nick-gated.*
2. **Stripe live-key rotation — revenue wall** (5.1). *Nick-gated.*
3. **A reachable GPU with reachable sovereign weights** (1.1+3.1+3.2). *Nick-gated + sibling.*
4. **[P0] Strip retracted BFT/23-of-33 + "court-admissible" from shipped UI + paid passport tool** (4.1). *Executable-now.*
5. **One honest sovereign capability artifact — or the fully honest refusal/safety repositioning everywhere public** (2.2+3.3+3.4). *Executable-now.*

---

# PART 2 — MEASUREMENT & PARITY (mined 2026-08-12, read-only, evidence by path:line)

## Meta-gap: THREE instruments measure "the 12 axes" and DISAGREE
No single frozen harness measures all 12 axes with n≥30 *distinct* items on the same instrument + same models.
- **A · `csoai-static-deploy2/sovos.py`** — 9/12 axes with graders; fetches HF `csoai/gspc-{slug}/items.jsonl` live; enforces `USABLE_N=30` but public banks are mostly **14–16 items**; **0 signed verdicts on disk**.
- **B · `SOVOS/packages/sovos-arena`** — all 12 axes, Wilson CI, but **n=40 = 1–2 distinct probes cycled** (`bank[i % len(bank)]`); **1 real pair** (qwen2.5 vs sov-safety-v1).
- **C · globe `arena.json`** (E2E_STATUS_REPORT_2026-08-08 §2) — 12/13 axes, mixes gspc + legacy benches; reports mach/det/swarm as MEASURED.
sovos.py says **mach=DRAFT, det=SPEC, swarm=PLANNED (no grader)**; globe says all three MEASURED. Both cannot be canon.

## Axis → distinct-n → n≥30?
Only **gov (237)** and **asi (32)** clear n≥30 with *distinct* items on the instrument sovos.py actually uses. agi/prv/mcp/oss/xr/art5 are **14–16 public items** on that instrument and only "reach 30" by switching instruments or cycling. care has **no gspc-care bank** (lives in legacy CareBench). mach/det/swarm have **no grader** in sovos.py.

## Top measurement gaps
- **M1 [integrity] False-n in the only signed run** — `sovos_arena/__init__.py:293` cycles a 1–2 probe bank to 40; qwen2.5 scores exactly **40/40** on agi/mcp/mach/det (signature of one repeated deterministic probe). The Wilson CIs and headline **d=4.21σ** treat 40 correlated repeats as 40 independent trials → **statistically void**. *Executable-now* (feed the existing `build_*_bank.py` banks in; author ≥30 distinct probes).
- **M2 [owner] mach/det/swarm** DRAFT/SPEC/PLANNED in code vs MEASURED on site — pick one canon before any "12/12 measured" claim ships.
- **M3** 5 gspc banks at ~16 items → raise to ≥30 distinct so sovos.py clears its own `USABLE_N=30`. *Executable.*
- **M4** SOV SIGNAL manifold calibrated on **jittered copies of ONE model** — build a real reference population from the RunPod fleet (149 models incl. sov34). *Executable.*
- **M5** Parity checked for only **6/12** axes (`parity_e2e.py:15`); art5/xr/care/mach/swarm/det unchecked; `gspc-mach` not created, care still legacy-named; HF pushes blocked on `HF_TOKEN`. *Executable.*
- **M6** `provbench_audio/latest.json` **missing** (coverage 25/30 = 83.3%); hf_eat/groq_eat/regulator/backup lanes stale 63–86h. *Executable (free T4).*
- **M7** EU-AI-Act bench: 1 model, n=5, `ci95:null` (`aiact_benchmark/latest.json`). Governance axis: n=3/model in arena, **G-median 0.0** across 10-model hf_eat. *Executable.*
- **Correction:** found **no file enumerating "7 governance NNs"** (that exact framing = no evidence found); the real corroboration is the 6-model n=3 arena + 10-model G=0.0 hf_eat.

Key evidence: `csoai-static-deploy2/{sovos.py,parity_e2e.py,build_*_bank.py,apply_canonical_names.py}`, `SOVOS/packages/sovos-arena/src/sovos_arena/__init__.py`, `SOVOS/arena-real-runs/arena_profile_*.json`, `SOVOS/REAL_MEASUREMENT_2026-08-11.md`, `projects/coai-dashboard/benchmark-results/{coverage_status.json,consolidated_latest.json,aiact_benchmark/latest.json}`.
