# SOV33 — MASTER ARCHITECTURE MAP (single source of truth)
**MEOK-SOV3 · 2026-07-10 · honesty split: RUNNING (verified) / WIRED-GAP (exists, not connected) / DESIGNED (spec only)**

This is the master. Every layer, every BFT role, the self-evolution loop, and SovSpace — in one place.
No layer is described from memory; each cites its file or its status.

## THE FULL STACK (12 layers, not 5)
| # | Layer | File on disk | Status | BFT role (what fault it tolerates) |
|---|---|---|---|---|
| L0 | **DRUM heartbeat** | drum/drum_heartbeat.py | RUNNING | cadence/liveness — a dead layer is detectable by missed beats |
| L1 | Sovereign Binding (Care-Floor) | sov33_owem_v3.py | RUNNING | **divergence**: two independent care-scores must agree, else block |
| L2 | BFT-33 Council | sov33_owem_v3.py | RUNNING | **quorum vote** — OWEM's real council is THE_13_MEMBERS (Hub+12 Queens, 9/13 quorum). The PDCA script's COUNCIL=33 was a DIFFERENT, un-polled constant — see correction below. |
| L3 | Elders MoE routing | sov33_owem_v3.py | RUNNING | **anchor quorum**: router disagreement → escalate, don't guess |
| L4 | Sovereign-merge brain | sov33_owem_v3.py + sov33_oracle_brain.py | RUNNING (live Oracle 70B) | **speculative cascade**: cheap draft + judge, escalate on FAIL (cuts 70B calls 67%, measured) |
| L5 | SIGIL chain | sov33_owem_v3.py | RUNNING | crypto hash-chain IS the BFT — tamper breaks verify, no vote needed |
| 5D | Dimensions | dimensions/dimension_harvester.py | WIRED-GAP | (Perception/Reason/Action/Memory/Emergence) — runs standalone, NOT called by OWEM |
| 6D | OpenWorld | openworld/openworld_harvester.py | WIRED-GAP | 5 harvesters (disk/web/data/edge/synth) — standalone |
| 7D | Intuition (8 senses) | intuition/intuition_layer.py | WIRED-GAP | consent-gated senses — standalone; **BFT role: sensor cross-check** |
| 8D | Sovereign Memory | mcp-memory-service (Hermes repo) | WIRED-GAP | separate repo; Care-Floor guard exists |
| — | **SovSpace** | csoai-os/sov-space, meek-sov-space-mcp | DESIGNED/partial | the world-sim UX layer — **BFT role: simulate outcomes, vote on best action before acting** |
| — | **PDCA self-evolution** | (not built) | DESIGNED | see below — the loop that lets BFT improve the system |

## THE #1 GAP (what you sensed)
**L0/5D/6D/7D/8D/SovSpace are NOT wired into OWEM** — verified: `grep` for their imports in sov33_owem_v3.py returns nothing.
They run as standalone scripts. OWEM today = L1–L5 only. The dimensional layers are real code that no request flows through.
**Fixing this wiring is the highest-value next build** — it's what makes the "12-layer" claim true instead of aspirational.

## BFT DOING MORE — the honest menu (per layer, measured where possible)
BFT is NOT just L2's vote. Verified/661 designed mechanisms:
1. L1 care divergence — two scorers must agree (DESIGNED, cheap to build)
2. L2 quorum vote — RUNNING
3. L3 anchor quorum — RUNNING (routing)
4. **L4 speculative cascade — RUNNING + MEASURED: 2/6 vs 6/6 70B calls (67% fewer expensive calls). Token count ~break-even — the win is $-cost, not raw tokens. Judge was too lenient on 1 hard task (tuning needed).**
5. L5 crypto chain — RUNNING
6. 7D sensor cross-check — DESIGNED (N-version on senses)
7. SovSpace action-vote — DESIGNED (simulate N outcomes, BFT picks best before acting)

## PDCA + DRUM SELF-EVOLUTION LOOP (designed, honest, BOUNDED)
Your ask: "BFT needs to PDCA, DRUM evolve, write its own frameworks."
Real version (NOT runaway ASI — bounded and human-gated):
- **PLAN**   — DRUM tick proposes a candidate change (e.g. "raise judge strictness", "add a crosswalk").
- **DO**     — run it in a SANDBOX sim (SovSpace), never live, never on canonical data.
- **CHECK**  — BFT council VOTES on the result vs current baseline (quality up? cost down? care held?).
- **ACT**    — if quorum passes AND care-floor held AND SIGIL-signed → propose to human. **Human ratifies.**
- Every cycle is SIGIL-logged → fully auditable. DRUM sets the cadence.
HARD BOUND (honesty register): the loop can PROPOSE a framework/param change; it CANNOT self-commit to
canonical charters or spend money or deploy — those stay owner-gated. "Writes its own frameworks" = drafts
candidates for human ratification, not autonomous law-making. This keeps it defensible and non-overclaimed.

## WHAT IS ACTUALLY LIVE TODAY (verified this session)
- Oracle GenAI 70B brain at L4 (signed calls), 5 models benchmarked, governance 4/4 on all 5, veto held.
- Sustained ~140 tok/s at concurrency 5. Governance overhead ~7% (+0.24s).
- BFT L4 cascade cuts 70B calls 67% (measured).
- 63 uncommitted files on branch m4-handoff-2026-06-24; sov33_bft_layers.py UNTRACKED (needs commit).

## NEXT BUILDS (ranked)
1. WIRE the dimensional layers (5D/6D/7D) into OWEM so requests actually flow through them (closes the #1 gap).
2. Build L1 care-divergence + tune the L4 judge (it passed a hard task it should've escalated).
3. Build the PDCA sandbox loop (sim-only, human-ratified) — the safe version of self-evolution.
4. Commit + push everything so Colab/other agents see one consistent tree.


## WIRING STATUS UPDATE (2026-07-10, measured)
Request-flow wiring built (sov33_wired_owem.py) and run live. HONEST result:
- **7 layers legitimately flow through a request**: L0 DRUM + 7D Intuition + L1-L5 OWEM core. All SIGIL-verified, no OWEM regression.
- **5D Dimensions / 6D OpenWorld are HARVESTERS** — they build training data, they do NOT process a live request. Wiring them into request-flow would fake a role they don't have. They stay as data-prep layers. So "12 layers in the request path" is NOT literally true; 7 is the honest count.
- **8D Memory / SovSpace** — separate repos / DESIGNED, not in this request path.
- TWO KNOWN BUGS from the wiring run (not hidden):
  1. DRUM beat 'order_parameter' read as None — wrong key captured; tick + SIGIL work, the value doesn't.
  2. Intuition senses (WiFiCSI/BLE/Acoustic) are STUBS emitting a canned 'vetoed' on every read — plumbing wired, but no real geometry/event signal yet.
- Care-Floor SCORER not yet real: the gate short-circuits correctly on a sub-0.35 score, but the score
  is currently hardcoded in tests, not derived. Building a real scorer + L1 care-divergence is the top safety build.

## JUDGE TUNING RESULT (2026-07-10, honest — UNSOLVED)
Tried tightening the L4 cascade judge prompt. Result: it OVER-corrected.
- lenient judge: 2/6 escalate, passed a hard Annex IV task it shouldn't (too soft)
- strict judge:  4/6 escalate, now fails EASY tasks (kill-switch, risk-tiers) it shouldn't (too hard),
  AND still wrongly passes the Annex IV task. 70B calls went UP 2->4, tokens +78% — economics WORSE.
VERDICT: a binary PASS/FAIL judge on a fixed prompt is the wrong instrument. Prompt-wording ping-pong
will not fix it. Real fix = a CALIBRATED judge (confidence 0-1 + tunable threshold) or difficulty-routing
by task type. Flagged UNSOLVED — not claimed as a win.


## CORRECTIONS (2026-07-10, post-audit — honesty)
- PDCA "33/33 PASS" was VACUOUS: the script hardcoded yes=33; it never polled 33 councilors. RELABELLED:
  each stage is a SINGLE cheap-model screen + optional 70B escalation. "resolved by left/right brain",
  NOT a quorum vote. The real win is the 10/90 escalation economy (6/8 stages resolve cheap), not a vote count.
- "132 signed decisions/cycle" was WRONG: SIGIL fires ONCE per stage (aggregates the stage into one hash).
  Real = ~5 SIGIL hops per 5-stage cycle, chain-verified. Not 132.
- Super-stack vs single-70B overhead: the "~7%" is from a CONTROLLED same-warmth test (+0.24s). The
  uncontrolled live A/B this session measured +50% to +71% (mean +60%) dominated by API/network variance, NOT fixed
  compute. Do not cite ~7% as the live-run result; cite it only as the controlled-test figure.
- Care-Floor "veto held across 5 models" used HARDCODED care scores — proves the gate short-circuits on a
  sub-floor score, NOT that a scorer assigns them. Real scorer = still to build.
