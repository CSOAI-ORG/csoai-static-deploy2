# CORRECTION — Board-Vs-API Gap: per-(axis,model) Gate 3 (2026-08-13)

**What got corrected:** the earlier BOARD_VS_API_GAP doc reported "all 13 axes
usable_n 517–4329" as the quotable-n evidence. **That was POOLED ROWS
(items × models), not per-model items.** The audit caught the 495-vs-33 class
recurring, this session. Corrected here with the per-(axis, model) table.

## The corrected Gate 3 (per-model usable items, floor = 30)
Computed live from peritem_*.jsonl: bank items × 19 models, usable = not
transport-error AND not unparsed. Per-model usable items = usable_rows / models.

| axis | bank | models | usable_rows | **items/model** | Gate 3 |
|---|---|---|---|---|---|
| gov | 237 | 19 | 4329 | **227.8** | ✅ PASS |
| care | 199 | 19 | 3138 | **165.2** | ✅ PASS |
| affect | 41 | 19 | 729 | **38.4** | ✅ PASS |
| art5 | 36 | 19 | 676 | **35.6** | ✅ PASS |
| agi | 36 | 19 | 647 | **34.1** | ✅ PASS |
| swarm | 32(?) | 19 | 618 | **32.5** | ✅ PASS |
| asi | 33 | 19 | 598 | **31.5** | ✅ PASS |
| mach | 33 | 19 | 592 | **31.2** | ✅ PASS (borderline) |
| xr | 32 | 19 | 593 | **31.2** | ✅ PASS (borderline) |
| oss | 32 | 19 | 578 | **30.4** | ✅ PASS (borderline) |
| mcp | 35 | 19 | 576 | **30.3** | ✅ PASS (borderline) |
| **prv** | 32 | 19 | 518 | **27.3** | ❌ **BELOW-30** |
| **det** | 33 | 19 | 517 | **27.2** | ❌ **BELOW-30** |

**Corrected verdict:** **11 axes pass per-model (>30), 2 FAIL (prv, det at ~27).**
The "13 ready" claim is wrong; prv + det must NOT be quoted as quotable until
their banks grow or unparsed rate drops. The honest "flip-ready" count is **11
(several borderline at 30-31)**.

## Why the pooled number was misleading
Pooled usable_rows conflate items × models; a Wilson interval on a card is per
model and needs n = items for that model. rows/19 ≠ bank size when some rows are
unparsed (det lost ~5 items to unparsing on average → 27 not 33).

## Cross-lab 4.44% — denominator + controls (resolved)
- **block_rate denominator: blocked / total_turns = 4/90 = 0.0444** (BLUE), **5/90 =
  0.0556** (RED). Reconstructable (was not stated inline — corrected).
- **Positive controls: PRESENT, all green** — Art 5(1)(a)/(c)/(e)/(f)/(g) BLOCKED,
  ok:true (satisfied the doctrine on the run's own code path).
- **East-vs-West NOT separable** — BLUE CI [0.017,0.109] OVERLAPS RED CI
  [0.024,0.124]. Frame as "measured under the same gate," NEVER "West beats East."

## Doctrine note
The audit's correction is accepted and re-verified from disk. The pooled-vs
-per-model mistake recurring in the same session that fixed 495-vs-33 is a sign
the numbers registry needs a **"n is per-(axis,model)" rule** enforced in the
claim-linter (add to the linter's CONFLATION patterns / a new guard). Queued.