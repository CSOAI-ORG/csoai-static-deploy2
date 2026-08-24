# BENCHMARK-AS-A-SERVICE — the OpenRouter question, answered honestly

> Doctrine-clean record of the strategic pivot ("can we be an OpenRouter of frameworks /
> regulations / law / benchmarks, and beat them with live benchmarks?"). Every claim is tagged
> [BET] / [BUILT] / [GAP] per the master-framework evidence discipline. Internal codenames stay
> quarantined; nothing here is a certification.

## The one-line answer

We are **not competing with OpenRouter** — we are in a different business. OpenRouter routes
traffic (a commodity pipe). The drum **indexes + measures** (a refinery). The moat is not
routing; it is **the accumulated data + the signed verification**, which a dumb pipe cannot own
without becoming a different company. [BET — the disconfirming evidence is that a reference
index and a measured gauge are only worth what a buyer will license; that market is unproven,
and the strongest counter is "nobody has yet paid for drum data." What survives: the reference
index is already the necessary substrate for the measured gauge, and both are cheap to keep.]

## The three layers (the actual architecture)

| Layer | What it is | Status |
|---|---|---|
| **Reference index (the drum)** | what exists — frameworks, charters, regulations, articles, sectors, **benchmarks** — each sourced and queryable over MCP/A2A | [BUILT] 640 items |
| **Measured gauge (the trust gauge)** | the live, continuous scoring layer — Fisher-Rao distance from a permitted manifold, split-conformal 90/10 router | [BET]/[GAP] scaffolded; not yet scoring live |
| **The data** | benchmark transcripts, preference pairs, safety incidents — the product | [BET] not yet at volume |

The drum **describes and sources**; the gauge **scores and never certifies**. The separation is
the moat, not a weakness.

## The four over-claims in the pitch, corrected (doctrine)

1. **"Blockchain attestation / Proof-of-Benchmark / Proof-of-Rank"** = [GAP]. What exists is
   Ed25519-signed cards + a Bitcoin-anchor *plan*. There is no "COAI blockchain." Selling it as
   built is the fastest way to lose the neutrality that is the whole asset.
2. **"2.5B gamers = unpaid benchmark runners … they don't know they're running evals"** = a red
   line. That is dark-pattern data harvesting. Doctrine is **measurement with consent** — every
   probe disclosed, every transcript licensed. We do not monetize people who are unaware they
   are being measured.
3. **"[internal] fly-brain 250Hz multi-path interference scoring"** = [internal codename] +
   [BET]. Not built; internal-only.
4. **"Compliance gold standard"** = certification language. Doctrine lock: *measurement, not
   certification.* We attest a measurement; we never certify a model.

## Why this beats the dumb pipe (the honest version)

| OpenRouter | The drum |
|---|---|
| static model list | **live, sourced, re-derivable index** |
| owns no data | **owns the index + the measurement traces** |
| generic API | **domain-specific cards (25 domains) + benchmark cards** |
| no verification | **signed (when the rail lands) + conformal-gated routing** |
| commodity margin | **data licensing + measurement (unproven, recurring-if-it-clears)** |

## What just shipped (the concrete first step)

The drum now indexes **`benchmark` as a first-class kind** (15 canonical, web-verified
benchmarks: MMLU, MMLU-Pro, HELM, Chatbot Arena, SWE-bench, HumanEval, GPQA, ARC, BIG-bench,
TruthfulQA, AILuminate, LiveBench, GSM8K, MATH, AGIEval). Each is **described and sourced,
never self-scored** — the drum is the reference index, not the leaderboard.

- `KIND_DIRS` + `norm_kind` + cards + site page (`benchmarks.html`) + MCP filter + tests all
  wired. Catalog **625 → 640**.
- Scorecard **93.0/100** — the catalog dimension is now **maxed (30/30)**; the only remaining
  gap is the 7-point trust flip (a real nonconformity score that clears realized-coverage).

## Next (in-lane, gated as marked)

1. Cross-verify the benchmark cards against primary sources (holy-of-sources pass) — in-lane
   (the CI cross-check `ops/ci_crosscheck.py` now runs this on web citations).
2. The measured gauge live-scoring = [GATE] fleet models + a nonconformity score that clears
   coverage. Not fabricable.
3. Data licensing = [BET] — needs a first consented, attested data product before it is claimed.

## Roadmap link (the full phased plan)

The end-to-end pivot lives in `ops/EUNOMIA_PHASED_PLAN_2026-08-23.md` (author: JEEVES):
**Phase 0** = the defensible core (this drum is its reference-index layer: frameworks ·
regulations · law · **benchmarks**), plus live-benchmark-as-data + attestation SKUs — no token.
**Phase 1** = verification/data monetization (attestation + data licensing) — no token.
**Phase 2** = crypto layers (token, staking, data-DAO, compute futures, prediction markets) —
**COMPLIANCE-GATED, do not build autonomously.** The drum does not touch Phase 2; it stays the
measured, sourced reference index under Phase 0.
