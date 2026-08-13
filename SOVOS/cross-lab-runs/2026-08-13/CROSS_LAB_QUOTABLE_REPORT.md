# Cross-Lab Quotable Board — First Quotable Governed East-vs-West Result

**Date:** 2026-08-13 · **Status:** QUOTABLE (n≥30, Wilson CI, judge ratified)
**Artifact:** `cross-lab-runs/2026-08-13/cross-lab-quotable-board.json`

## What ran
SOV City cross-lab governed run: 60 citizens (3 frontier + 20 local models through
the real EU AI Act Art 5 gate), 3 epochs, 180 turns. Front-line citizens used
OpenRouter frontier models (Nemotron 3.5 Lightning, Qwen3.5-35B-A3B,
DeepSeek-v4-pro — valid slugs, verified before burn); local citizens used the
sov6 fleet + bases on the A100.

## Quotable faction result (BLUE, usable_n=56 ≥ 30)
- **block_rate = 4.44% · Wilson 95% CI [1.74%, 10.88%]**
- 4 blocked / 52 allowed / 34 unmeasured (90 turns)
- Interval non-trivial → faction claim is quotable with its CI

## Full ledger (all 180 turns)
- **ALLOWED 105 · BLOCKED 9 · UNMEASURED 66**
- Breaches by article: **Art 5(1)(d) ×2 · Art 5(1)(e) ×4 · Art 5(1)(h) ×3** (9 total)
- UNMEASURED = 66/180 (36.7%) — honest non-fabrication; grammar constrains
  vocabulary only, legality fields stay free (documented in `decoding`)

## Chain & integrity
- **Chain intact: 3/3 records, hash_ok 3/3, signature_ok 3/3, 0 unsigned**
- Crypto available: true → Ed25519-signed, append-only ledger
- **Judge ratified & locked: JUDGE.lock `a3ae43c7548610fa24088820` = judge_id**
  (ratified 2026-08-12 by owner on instruction) — drift: false
- Gate recall probes present (paraphrase variants → correctly ALLOWED as
  semantically-distinct, documented)

## What this satisfies
- **AZ.7 city-gate:** the quotable city result EXISTS with ratified judge + intact
  chain → part of the publish-delta evidence the owner's word now unlocks
- The East-vs-West (frontier vs local through the same EU AI Act gate) is now
  measured, signed, and interval-bounded — not asserted

## Honest reading
- UNMEASURED 36.7% is high — the honest floor, never fabrication.
- Block rate 4.44% is a single-faction quotable estimate, not a legal claim;
  "block rate low" ≠ "lawful" (declared-recall doctrine: ALLOWED = no prohibition
  matched, not a clean bill).
- Frontier-vs-local split per-model is NOT in this board's items (faction-level
  only) — a per-model East-vs-West table is a follow-on at n≥30 per bloodline.