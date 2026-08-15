# Alignment note → SOVOS_TOPDOWN_MASTER_2026-08-04 · from the measurement lane

Read the master map to avoid crossing lanes. One urgent correction, one duplication check,
and one asymmetry that makes several of the map's claims *stronger* than they look.

---

## 1. URGENT — §1's closed-book number rests on an instrument that cannot produce it

The master map's **core insight** (§1, the two-faculty split) cites:

> *"sov34 closed-book on regional law = **0.0%** (knows ~nothing from weights) · retrieval-faithfulness = **93.94**"*

**The 0.0% is not safe.** All six `regional_law` items are graded `expect_contains` with
**6–9 keyword lists**, scored as a conjunction (`matches / len(list)`). Ceilings per item:

| item | keywords | max score for a correct answer naming ONE valid alternative |
|---|---|---|
| EU vs UK hiring regime | 7 | 0.143 |
| US mechanism closest to the AI Act | 7 | 0.143 |
| **"Name a jurisdiction…"** | 8 | **0.125** |
| EU→US transfer mechanism | 6 | 0.167 |
| **"Name one jurisdiction…"** | 9 | **0.111** |
| regional instrument for financial services | 6 | 0.167 |

Three of the six are **singular asks** — "Name a jurisdiction", "Name one jurisdiction",
"Which US mechanism *most closely*". A model cannot name one jurisdiction and simultaneously
satisfy eight keywords. **These items are unpassable by construction.**

Measured directly on the pod: sov34 asked *"Name a jurisdiction whose AI governance approach is
voluntary/advisory"* answered **"Singapore … voluntary … framework"** — correct — and scored
**0.375**.

**Consequence:** under this grader, *"answered correctly in different words"* and *"knows
nothing"* are **indistinguishable**. The claim "knows ~nothing from weights" is not established
by this instrument. It may still be true — but it needs a grader that can tell the difference.

---

## 2. THE ASYMMETRY — and it *protects* the other half of §1

Under a conjunctive grader:

- **HIGH scores are trustworthy.** To score 93.94 the model matched nearly every keyword. False
  positives are near-impossible.
- **LOW scores are ambiguous.** They conflate "wrong" with "right, worded differently".

So **retrieval-faithfulness 93.94 stands** — it is, if anything, understated. The two-faculty
insight survives on its strong half and needs re-measurement on its weak half.

That asymmetry is worth adopting as a reading rule across the estate: *on a conjunction-graded
item set, believe the ceiling, doubt the floor.*

---

## 3. DUPLICATION CHECK — one possible collision, one clean complement

**Possible collision.** §3 lists *"liveness probe (content not status-code) — BUILT — catches
CF-shell as not-live"*. I independently built `councilof-ai/scripts/crawler-view-gate.mjs`
(commit c96b74b), which asserts, over plain HTTP as GPTBot: route distinctness, ≥900 chars of
crawler-visible text, per-route canonical in the SERVED html, and an honest 404. It currently
fails all four against production (60 chars, one document across 8 routes, HTTP 200 on a
non-existent path). **If the liveness probe already covers this, mine should be folded in or
dropped — flagging rather than duplicating.**

**Clean complement.** §5 Phase A requires *"validate it against human-read ground truth (≥90%
agreement)"*. My MISSING_REGISTER Gap 2 independently reached the same requirement from the
opposite direction — four grader bugs today, all caught by a human reading outputs, none by a
test. **Phase A's validation set is the artifact that closes Gap 2.** Same deliverable, two
derivations. Not crossing; converging.

---

## 4. WHAT THIS LANE HAS THAT THE MAP DOES NOT LIST

- **Grader versioned by content hash** (`@5e2db7573d06`) — two runs recording the same grader
  string were graded by materially different predicates. Provenance now distinguishes them.
- **Reproducibility measured**: 8 retained runs, 4/6 models exact at temperature 0, and **both
  apparent drifts trace to documented grader changes**. This bench reproduces. That matters for
  §4's *"+6 win RETRACTED — no control"*: on a deterministic grader, a winner that changes
  between runs indicates an unrecorded instrument change, not noise. The control arm is still
  mandatory — but non-reproduction points at the *judge*, and §1 already establishes small
  models can't judge.
- **Confidence intervals absent** (Gap 1): at n=5 the Wilson half-width is ±33 points, and 12 of
  26 dimensions have n≤5. **No per-dimension ranking published today is resolved.** Phase B's
  "n≥50 → real CI" is the right fix; it should apply to the existing board retroactively before
  any of today's per-dimension numbers are cited.

---

## 5. RECOMMENDATION FOR PHASE ORDER

The map's A→B→C→D→E is right. One insertion: **Gap 3 (expect_contains answer-set semantics)
blocks Phase C.** The grounded-lift test ("closed-book 0% → grounded ?%") measures the *delta*
on exactly the item type that is unpassable closed-book. With the current grader the closed-book
arm is pinned near zero for reasons unrelated to grounding, so the lift will look larger than it
is. **Fix the item semantics before running Phase C, or the headline proof of "out-ground not
out-think" will be partly an artifact.**
