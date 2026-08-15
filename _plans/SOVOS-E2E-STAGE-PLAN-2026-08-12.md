# SOVOS E2E STAGE PLAN — "true, working, published"
**Compiled 2026-08-12 · covers everything outstanding from Parts AX–BV · dependency-ordered, gate-explicit**

Reading rules: a stage starts only when its **ENTRY GATE** is true. A stage is done only when its **EXIT GATE** is verified — with an outside-view receipt, never a self-report (A5). OWNER = Nick only. LANE = any sibling lane. Nothing public carries a number that isn't in the numbers registry (A4). The judge re-bolts, never evolves.

---

## STAGE 0 — Ungated parallel work (start NOW, lanes)
**Entry gate:** none. **Must not touch:** the running board, sibling jobs, GPU-heavy starts.

| # | Item | Owner | Notes |
|---|---|---|---|
| 0.1 | Board keeps grinding untouched | — | GPU 90%, ~19k calls, multi-hour. No restart. |
| 0.2 | MinIO security hardening | LANE | TLS + buckets private-by-default + per-pod least-privilege keys + rotation. **Before any external put/get** (BS.3 pin) |
| 0.3 | Numbers registry v0 (A4) | LANE | Every public number in one file; resolves 200-vs-201, 13/10/11, 34+18 |
| 0.4 | Claim-linter v0 (A3) | LANE | killed terms, non-canon dates, unratified ordinals, registry mismatches |
| 0.5 | Deploy ledger (A2) + fleet roster (A6) | LANE | repo→project→domain→hash→last probe; pod↔job↔GPU↔ETA |
| 0.6 | Owed verifications batch | LANE | (a) ADJUDICATE dead-end? (BP.5) (b) charter Art 32–49 reserve-vs-gap (BP.3) (c) care 200-vs-201 canonical (BS.1) |
| 0.7 | Copy-edit manifest remainder + live re-probes | LANE | BI order; done = probes pass on live bundle |
| 0.8 | gspc-art5 v1-row provenance cleanup | LANE | null ground-truth fields; ships with counsel pass (BS.1) |

**EXIT GATE:** registry + linter live; owed batch answered; no open "done-without-receipt" claims.

---

## STAGE 1 — Owner batch (Nick, cheapest-first, parallel with Stage 0)
**Entry gate:** none. This is the invisible queue made visible (A7).

| Order | Gate | Unblocks | Cost |
|---|---|---|---|
| 1.1 | **OpenRouter key** (rotated mid-session — confirm working one) | cross-lab / East-vs-West runs | minutes |
| 1.2 | **proofof.ai disposition** (archive-or-redirect) | last live codename bleed — estate fully clean | one decision |
| 1.3 | **P6/P8/P20 counsel call** (re-scope; prior-art clock) | patent position | 1 call — **loudest clock** |
| 1.4 | **Counsel blessing**: affect + art5 legal-gold labels | Stage 3 re-bolt; affect cards | same call as 1.3 |
| 1.5 | **gspc-xr Kaggle title** (API can't edit) | last card-drift | minutes |
| 1.6 | **Master/volume go-ahead** + Sigsum net-capable host | durable corpus + transparency log | one yes |
| 1.7 | **DSIT £11M application** review/submit | funding line | hours |
| 1.8 | **Positioning line** publication timing | "Every lab marks its own output. We prove the whole pipeline." | one decision (hot-cycle dependent) |

**EXIT GATE:** 1.1–1.5 cleared (minimum for Stage 3); 1.6–1.8 scheduled.

---

## STAGE 2 — Board lands (the critical path)
**Entry gate:** the 12/13-axis run completes on stable ollama.

| # | Item | Owner | Notes |
|---|---|---|---|
| 2.1 | Verify run integrity | LANE | Wilson CIs present, per-item rows intact, `is_infra_tainted` clean, no silent drops |
| 2.2 | Check whether the run included `affect` | LANE | Wired mid-run (commit 9ab14ef) — if not included, queue the affect axis run immediately after |
| 2.3 | Correct `/api/gspc` | LANE | nine stale axes + new axis entry |
| 2.4 | Board artifacts → master (MinIO) | LANE | only after 0.2 hardening confirmed |
| 2.5 | Ollama upgrade 0.32.8 → 0.32.9+ | LANE | safe once GPU frees; then Nemotron pull (BK sequence) |

**EXIT GATE:** 12/12 verified with CIs; `/api/gspc` correct; affect run queued or included.

---

## STAGE 3 — Re-bolt + affect first measurement
**Entry gate:** Stage 1.4 (counsel) + Stage 2 complete.

| # | Item | Owner | Notes |
|---|---|---|---|
| 3.1 | **JUDGE.lock re-bolt** with affect law surface | OWNER | new hash, recorded in register; re-bolt never evolve (BS.1) |
| 3.2 | affect first clean run | LANE | n=34 → mean + Wilson OK; **tail stats NOT yet — n-hungry (BV.2)** |
| 3.3 | Season 1c completes (n≥30) | LANE | GPU free after board; then 1a→1b→1c delta computed |
| 3.4 | Eunomia gate-strength investigation | LANE | quiet, per BJ doctrine |
| 3.5 | Nemotron citizen run (East-vs-West) | LANE | same 12/13 banks, same grader, n≥30 — needs 1.1 + 2.5 |

**EXIT GATE:** affect carries an interval; 1c landed; re-bolt hash on record; nothing quoted below its gate.

---

## STAGE 4 — Tail aggregators v1
**Entry gate:** Stage 2 rows landed (per-item data exists).

| # | Item | Owner | Notes |
|---|---|---|---|
| 4.1 | Implement aggregator v1.0 | LANE | worst-case flag + CVaR + correlated-failure rate — named, versioned, reproducible (BV) |
| 4.2 | Pin aggregator on cards | LANE | signed triple: **gold + rows + aggregator version** (BV.3) |
| 4.3 | Compute on landed boards | LANE | report tail fraction + composition with uncertainty statement; tail-quotable ONLY where n≥100 |
| 4.4 | Tail-bank expansion plan | LANE | affect → n≥100 path (bank growth or pooled clean runs) |

**EXIT GATE:** aggregator v1.0 pinned; anyone can re-run it on published rows and get the same numbers.

---

## STAGE 5 — Publish wave 1
**Entry gate:** Stage 3 exit (affect interval + 1c + re-bolt). Each item also needs its own micro-gate.

| # | Item | Micro-gate | Owner |
|---|---|---|---|
| 5.1 | **Delta Note #1 (1a→1b→1c)** + Zenodo DOI | 1c landed | LANE drafts, OWNER publishes |
| 5.2 | Sign axis cards (affect + board) | n≥30 + counsel + re-bolt hash | OWNER (signature) |
| 5.3 | **T2 data-model spray** | board + city + judge hash on every card (BG) | LANE |
| 5.4 | Art 5(1)(c) publish | 400/400 + CIs — else stays internal | LANE |
| 5.5 | affect web page + KEY_ROUTES | A100 lane per handoff; routes only after page builds; live re-probe | LANE |
| 5.6 | Positioning line | OWNER timing (1.8) | OWNER |

**EXIT GATE:** every public artifact probe-verified from outside (cache-busted receipts); zero registry mismatches (A3 clean).

---

## STAGE 6 — Productization
**Entry gate:** Stage 5 exit (signed artifacts exist).

| # | Item | Owner | Notes |
|---|---|---|---|
| 6.1 | **Emotional Safety Card v1** (B1) with tail block | LANE builds, OWNER signs | insurance-grade format (BV.4: CVaR speaks insurer) |
| 6.2 | **Charter→Law crosswalk product** (B3) | LANE | 34 substantive articles mapped; ○ gaps shown honestly; "34+18" canon |
| 6.3 | Insurance outreach pack | OWNER | Munich Re / Armilla / AIUC-shaped language; card in hand, not pitch deck |
| 6.4 | Sovos Partner Network approach | OWNER | only after 1–2 pilots (earlier sequencing) |
| 6.5 | DOI automation (B4) | LANE | every landing auto-packages to Zenodo |
| 6.6 | MEOK one-liner (B5) | OWNER | publish only when the card exists to back it |

**EXIT GATE:** first external conversations held with signed artifacts, not promises.

---

## STAGE 7 — Deep publishing & IP
**Entry gate:** Stage 5+ corpus accumulating.

| # | Item | Owner | Notes |
|---|---|---|---|
| 7.1 | **Quorum-gated measurement whitepaper** (waggle/Seeley frame, BU.3) | LANE drafts, OWNER publishes | charter-layer frame, math stands alone |
| 7.2 | Patent provisionals from re-scoped P6/P8/P20 | OWNER + counsel | measurement semantics, never crypto plumbing (AX) |
| 7.3 | GNN-over-StateBus (THEORY) | LANE | ≥10k signed cards prerequisite; never "ASI" |
| 7.4 | Tail-quotable affect (n≥100) publish | LANE | the insurance-grade number |

**EXIT GATE:** DOI'd corpus + filed provisionals + the tail-quotable card.

---

## Standing rules (every stage)
1. No public number not in the registry. 2. No "done" without an outside-view receipt. 3. Never kill a sibling's job. 4. Killed claims never recur. 5. NVIDIA rule both directions. 6. Counsel holds the legal-gold pen. 7. Re-bolt, never evolve. 8. Names are free; numbers are earned. 9. The covenant steers; the boards sign. 10. Non-linear eyes, deterministic ruler — opaque never.

**The shortest path to "true, working, published":** Stage 0 items 0.2–0.6 (this week, lanes) + Nick clears 1.1–1.5 (one afternoon) → board lands → re-bolt → affect interval → Delta Note #1. Everything else is sequencing.
