# Human Arena Pilot Design v1.0 (Block B #9)
## Prolific-scope 100-participant gold run — human-vs-AI measurement cells

**Gated:** this is a DESIGN + consent scaffold. Launching the pilot requires
(a) owner approval of spend, (b) DPIA sign-off (v1.0 exists), (c) the
prolific-account setup. The design itself is agent-doable and needed.

---

## 1. Why

The measurement body's most defensible ground truth is a human judgement
bench: same items, same rubrics, humans vs models, all paired
signed/unsigned. The 15-axis × human-vs-AI cell is the missing
"measurement of the measurers."

## 2. Study design

| Item | Spec |
|---|---|
| Platform | Prolific (pre-screened participants, ~£12/hr) |
| N | 100 completions (3:1 quality checks) |
| Items | ~60 probe items sampled from the GSPC bank across 4 axes (gov, safety, proxy, care) — stratified, seeded |
| Task | For each item: "does this response comply (Yes/No/Unsure)" — gold labels from the deterministic gate, KR20 inter-rater check |
| Time | ~15 min/task → £3-5 per participant, ~£400-500 total |
| Blind | No model names shown; items randomized; no measurement framing (neutral "policy compliance" framing) |
| Consent | EDPB-compliant consent screen; pseudonym-by-default; opt-out pre-analysis |

## 3. The pair

Each human judgement row is emitted TWICE:
- `unsigned` row: {participant_pseudonym, item, verdict, ts} — no signature
- `signed` row: same fields + card_type `human-arena-gold-v1` + Ed25519 sig

Both carry the same `lineage_digest` — the A/B proves the trust delta, the
same mechanism as `replay_instrument.py`.

## 4. Quality gates

1. `n=100` completions, `>=3` seed items where a fake-gold (known wrong)
   is planted → exclusion if guessed wrong (attention check)
2. Inter-rater: Cohen's κ ≥ 0.7 on an overlap subset (10 items × 25
   participants) else the cell is re-run
3. Signed row per cell; verifier off
4. No individual raw judgement published; only aggregates with n≥30

## 5. Deliverables

- `human-arena/` prospectus + consent text (agent-ready)
- `human-arena/gold-cards/` — signed gold cells (once run)
- Scoreboard coloumn: human-gold vs model matches — same table as v2

## 6. Ethics & reg

- No deception beyond blind-labelling (disclosed post-task)
- No special-category data; age band only
- Payments via ProL built-in (don't collect bank data)
- Data minimisation; pseudonym-by-default; DPIA v1.0 §4.3 covers

## 7. Approval

Owner gate: (a) spend ~£400-500, (b) Prolific account access (via Nick),
(c) DPIA written sign-off. Without these, this design stays a scaffold.