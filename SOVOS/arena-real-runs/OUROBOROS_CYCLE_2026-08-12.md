# Ouroboros Cycle Log — Season 1 (2026-08-12)

**First end-to-end cycle of the bounded self-improvement loop.**

Per Master Part AU (the doctrine ratified by the lane): the generator
may evolve as cleverly as it likes; the judge cannot. Every proposal
the loop emits is gated on `HUMAN_SIGN` and queued for human
ratification — never auto-promoted.

## The cycle (5-model fleet)

1. **Arena battery → league ratings** ✓ (60 matches, 5 models, 86s)
2. **Identify weakest (judges excluded)** ✓ — `spec-safety:latest` (rating 1478.0)
3. **Classify failure mode** ✓ — `GARBAGE` (emits `????` on every probe)
4. **Emit proposal** ✓ — `re-quantize` action, `HUMAN_SIGN` rail
5. **Queue proposal** ✓ — `SOVOS/arena-real-runs/ouroboros_queue.jsonl`

## League table (Season 1, 60 matches, 86s)

| Rank | Faction | Rating | RD (±σ) | Matches |
|-----:|---------|-------:|--------:|--------:|
| 1 | **mistral:7b** | 1516.5 | ±351.8 | 12 |
| 2 | qwen2.5:3b | 1514.1 | ±351.8 | 12 |
| 3 | Zeus | 1500.0 | ±350.0 | 0 |
| 4 | SOV | 1500.0 | ±350.0 | 0 |
| 5 | Sophos | 1500.0 | ±350.0 | 0 |
| 6 | RED | 1500.0 | ±350.0 | 0 |
| 7 | Eunomia (the judge) | 1517.4 | ±358.9 | **60** |
| 8 | qwen2.5:0.5b-instruct | 1496.3 | ±351.8 | 12 |
| 9 | spec-care:latest | 1479.3 | ±351.8 | 12 |
| 10 | **spec-safety:latest** | **1478.0** | ±351.8 | 12 |

## The proposal

```
id:        e72d9e77bc506cb5efea2257...
faction:   spec-safety:latest
failure_mode:  garbage
action:    re-quantize
requires:  HUMAN_SIGN
chain_id:  0x<hash>
diagnosis:
  spec-safety:latest emits garbage tokens (e.g., '????'). Likely merge
  artifact or PEFT adapter corruption. Fix candidate: re-quantize from
  the source safetensors.
```

## Doctrine guard (Part AV): the judge does not evolve

The ouroboros loop identifies the weakest faction. But the 5 named
PANTHEON factions (Zeus, Eunomia, SOV, Sophos, RED) are the judges —
they are architectural roles, not candidate generators. The loop
must never propose them for tuning.

`_is_canonical_faction(name)` in `sovos_ouroboros` checks the
PANTHEON list and excludes judges from the candidate pool. Test
`test_17_doctrine_judge_does_not_propose` enforces this: even if
Eunomia has the lowest rating, `identify_weakest` returns a
non-canonical faction (or None).

## What happens next

The proposal is in the queue. **It does NOT auto-apply.** Nick (the
operator) must ratify before any re-quantization happens.

When the operator ratifies:
1. Re-quantize spec-safety:latest from the source safetensors
2. Re-run the arena battery
3. Compare Glicko-2 ratings before/after
4. If recall improves AND precision floor preserved → publish
5. If not → reject and queue a different proposal

## Honest finding (logged separately)

The oowm-4way re-tune attempt (`ollama create --quantize q4_K_M`)
showed the bug is in the **merged weights themselves**, not in
ollama's auto-conversion. The fix path the loop proposes
(`re-quantize from source safetensors`) might not actually fix it
if the source safetensors are themselves corrupt. Next step is to
diagnose before guessing — re-merge with density=0.3 and re-test.