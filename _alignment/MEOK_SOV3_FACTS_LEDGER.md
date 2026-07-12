# MEOK-SOV3 FACTS LEDGER — assert once, honored every session
_Nick asserts a fact here ONCE; every future session reads it at start and stops re-asking / relapsing.
This file auto-loads via the alignment loader. Format: one fact per line, dated. Newest at top._

## CAPABILITIES (this agent = MEOK-SOV3 in Claude Science)
- 2026-07-12 — NO browser tool. Verified via search_skills. "Used browser yesterday" = Claude Code (different agent/env), NOT me. Never claim or attempt browser/Colab access.
- 2026-07-12 — NO compute target. list_compute is empty. Cannot spawn GPU or dispatch training. Colab T4 lives in Claude Code's browser, unreachable from my kernel.
- 2026-07-12 — hermes_ask (sov3 MCP) is a LOCAL Ollama proxy, NOT a live bridge to the Hermes build lane. Cross-lane channel = the git tree.

## DIVISION OF LABOUR (who does what — stop re-deriving this)
- 2026-07-12 — Claude Code owns: browser, Colab T4 GPU run, the 4-expert QLoRA fine-tune (2-4h real compute).
- 2026-07-12 — MEOK-SOV3 (me) owns: SOV33 code, readiness gate, distillation harness, ingestion path, commits. I build what runs ON the GPU; Claude Code runs it.
- 2026-07-12 — Coordination is via git tree + LANE_STATUS, not a live agent bridge.

## GPU TRAINING STATE (owner-confirmed facts go here)
- 2026-07-12 — Colab T4 training Expert 1/4 (compliance) reported RUNNING by Claude Code; ~2-4h for 4 QLoRA fine-tunes (physics, not stalling). No progress bar = subprocess tqdm not streamed by Colab, NOT hung.
- Adapters land at ~/.sovereign/models/ ; owner confirms with `ls ~/.sovereign/models` (I cannot read that path from sandbox).

## HOW TO USE THIS LEDGER
- If I'm about to tell Nick something he clearly already told me, or re-ask a settled fact: CHECK HERE FIRST.
- When Nick asserts a durable fact ("X is true, stop forgetting"): append it here dated, so it persists.
