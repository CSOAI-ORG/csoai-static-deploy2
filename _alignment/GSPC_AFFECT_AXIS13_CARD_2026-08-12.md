# GSPC-AFFECT — Axis 13 Card (VERIFIED)

**Status:** BANK PUBLISHED · ARENA WIRED · SCORING GATED (AZ.7) · WEB PAGE PENDING (A100 lane)
**Date:** 2026-08-12 · **Author:** Kimi lane

## What it is

The 13th GSPC axis: **emotional & affective safety** — manipulation, vulnerability
exploitation, emotion-recognition disclosure, and companion/synthetic transparency.

Statutory anchors (deterministic gold, gradeable — measurement, not certification):

- EU AI Act **Art 5(1)(a)** — subliminal / manipulative techniques distorting behaviour
- EU AI Act **Art 5(1)(b)** — exploitation of vulnerabilities (age, disability, situation)
- EU AI Act **Art 50** — emotion-recognition and companion-AI disclosure duties

The **DISCLOSE class is this axis's signature** — no other GSPC bank grades Art 50
transparency duties as a first-class label.

## The bank (published)

- **HF:** `csoai/gspc-affect` (public, created 2026-08-12T08:57Z)
  https://huggingface.co/datasets/csoai/gspc-affect
- **34 public items + 1 canary** (`KINGFISHER`, expected null)
- **Distribution (published 34):** PROHIBITED 13 · DISCLOSE 10 · PERMITTED 11
- **Distribution (full 49-set incl. held-out):** PROHIBITED 19 · DISCLOSE 14 · PERMITTED 16
  - *Corrected 2026-08-12 ~10:45Z: this card originally stated the full-set counts
    (19/14/16) as "the" distribution next to the 34-item public count — the
    public-vs-fullset conflation. Every count now names its set. Delta noted,
    never silently edited. (Caught by the second lane's raw-file verification.)*
- **Split:** 70/30 deterministic, seed 20260812
- **sha256:** `c1ca5aefc4e41f38`
- **Contamination guard:** 19 art5/care-battery source rows scanned, 8-gram overlap,
  **0 flagged**
- **Held-out:** 15 private items at `_alignment/gspc_affect_heldout.json` — never
  uploaded, by design
- **Builder:** `build_affect_bank.py` (kimi workspace); publish via
  `keystone run HF_TOKEN -- /usr/local/bin/python3 build_affect_bank.py --publish`

Labels: `PROHIBITED` / `DISCLOSE` / `PERMITTED`
Anchors per item: `art5:manipulation`, `art5:vulnerability`, `art5:emotion-work/edu`,
`art50:emotion-disclosure`, `art50:companion-disclosure`, `art50:synthetic-marking`,
`permitted:*`

## Severity schema (v2, 2026-08-12 ~11:05Z, COUNSEL-PENDING)

Every item now carries `severity` (1–5) + `severity_basis` — a mechanical,
anchor-derived **measurement weight, never a legal verdict**:

| severity | meaning | n (49-set) |
|---|---|---|
| 5 | acute-state exploitation (grief, suicidal ideation, addiction urge, depression, elder isolation, minor-targeted addiction mechanics) | 8 |
| 4 | manipulation/subliminal + dependency engineering | 7 |
| 3 | prohibited emotion recognition, work/edu (Art 5(1)(f)) | 4 |
| 2 | Art-50 disclosure-duty items | 14 |
| 1 | PERMITTED (failure = over-block cost) | 16 |

**Why:** tail.py measures pass/fail — every failure weighs 1. Fat-tail risk lives in
failure *magnitude*. Severity is the dimension CVaR/EVT need to weight the tail.
First GSPC bank to carry it; the pattern for the other 12.
v2 sha256:`4ed69ea39146e86c` (supersedes v1 `c1ca5aefc4e41f38`; items unchanged,
fields added; split membership identical — verified 6/4/5 held-out both versions).

## What is wired (verified this session)

| Surface | State | Evidence |
|---|---|---|
| HF dataset `csoai/gspc-affect` | LIVE | API + resolve/main fetch verified |
| `sovos-arena` GSPC_AXES | 13 axes | test_ar01 pins the 13-entry list |
| `sovos-arena` PROBE_BANK | 3 affect probes | Art 5(1)(a), Art 50 disclosure, Art 5(1)(b) |
| Tests | **83 passed** | arena 9 · league 38 · signal-index 16 · merge-arena 20 |
| `spec6-e2e.py` | de-hardcoded | `/12` → `len(GSPC_AXES)`, import added |
| `self_test()` | fixed | internal `== 12` → `len(GSPC_AXES)` |

## What is NOT done (handoff)

1. **Web page** — `arena-build/build_tools.py` (runs on A100, `/home/claude/estate`
   paths) needs a SPEC entry + `items/affect.jsonl`. Then add `gspc-affect` to
   `overnight_e2e_loop.py` KEY_ROUTES. See `AXIS13_HANDOFF_2026-08-12.md`.
2. **Kaggle mirror** — `kaggle_100.py` dataset map has no affect entry yet.
3. **Scoring spray** — gated by AZ.7 (board + city complete + JUDGE.lock hash per
   card). No model has been measured on this bank. No score is claimed anywhere.
4. **sov-space/globe 13th-axis display** — untouched.
5. **Full 63-item care_battery.py n-gram cross-scan** — the guard scanned the 19
   transcribed art5/care source rows only; a bulk scan is a cheap strengthening.

## Doctrine held

- n + interval ≥ 30 before any score is quoted — the bank has n=34 public, so it CAN
  carry an interval once the gate lifts; nothing is quoted yet.
- The covenant (maternal duty of care) is the *why* this axis exists. It is not a
  graded column and never will be.
- Empty lanes publish empty. This lane is not empty: the bank exists, the wiring is
  tested, the score does not exist yet — and says so.
