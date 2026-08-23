# IMPROVEMENTS FROM THE LIVE BOARD + FLEET AUDIT — 2026-08-16

Source: the LIVE RESULTS board (LLAMA track + FLEET track, sibling lane, cockpit
:8088) cross-read with my fleet audit (RunPod GraphQL, live 11:00 UTC).
This memo records what we DO differently because of them.

---

## 1. Track-bounded quoting rule (G3 class — now in registry)

`phi4:14b` carries TWO canonical averages:
- **LLAMA track 64.4** — raw weight layer, includes MATH-50 (20) and HumanEval
  (0). The full-ruler number.
- **FLEET track 82.0** — deployed with system prompt, 6-bench subset (arc, gsm8k,
  mmlu, hellaswag, truthfulqa, winogrande). The product number.

**Rule:** any public quote of phi4's average MUST carry its track label.
Without the label, 64.4 vs 82.0 is a G3 conflation (silent harness switch).
Registry entries added with this exact doctrine. Quote either as
"phi4:14b fleet-track 82.0" or "phi4:14b full-harness 64.4" — never bare.

## 2 — "System prompts lift scores" is ADJACENT, not LIFTED

Board claim: sov6-aesthetics (78.0) > gemma3:12b base (77.3) → "the Modelfile
adds ~1pt". At current n, 0.7pt is inside plausible Wilson CI overlap.
**Rule:** public wording = "sov6-aesthetics and gemma3 are adjacent (78.0 vs
77.3); CI resolution pending". Only after n and CIs land (n≥30 per canon, CI
computed) may we say "lifts". Principle: we measure the deployed layer; we
don't overclaim its magnitude.

## 3 — The honest zeros stay

MATH-50 (20-28%) and HumanEval (0%) are the honest resource-ceiling numbers.
14B-class models don't code under def+return+≥3-stmt scoring — that's a real
capability floor, not a harness bug. **Upleveling priority:** when the code
clan / bigger model lands (Qwen3.8-27B Apache-2.0 window), these two cells are
the first remeasure.

## 4 — Fleet-cost engineering (from the audit)

phi4:14b — the #1 model in BOTH tracks — runs on the RTX 3090 at **$0.22/h**
(23GB/24GB VRAM seen live). The A100s ($1.19-1.39/h) are NOT required for this
workload.

**Decision:** overnight + benchmark workloads route to the 3090 at $0.22/h
(≈6× cheaper per hour). A100s reserve for: signing waves, mergekit runs, and
the Qwen3.8-27B sweep when it arrives. This cuts the benchmark runway cost by
~80% while keeping the same #1 model.

## 5 — Billing leak open item

`overnight-bench-a100-v2` (5ynpuvuiae807i) = $1.19/h, same machine as A100-1,
unreachable, workload unknown. **Owner decision needed:** stop it (saves
$28.6/day at the overnight-run threshold) or confirm it's the overnight queue.

## Registry
+6 entries (phi4 fleet/llama avgs, sov6-aesthetics +0.7pt doctrine, sov6-creation
gsm8k 92, humaneval honest floor, fleet-cost phi4-on-3090). Total 16.

## Next mine (when gateway returns)
- Pause/confirm overnight-bench.
- Route the overnight queue to 3090 (sov-repull is the right home).
- Remeasure math + humaneval on Qwen3.8-27B day-0 window.