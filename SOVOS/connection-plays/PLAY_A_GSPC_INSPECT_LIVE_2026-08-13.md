# Play (a) EXECUTED — GSPC → Inspect, live on the A100 (2026-08-13)

**Goal (research pass):** port GSPC banks onto UK AISI's Inspect (MIT) and make
them runnable evals — the credibility on-ramp into DSIT/AISI + NPL's Centre for
AI Measurement.

**What actually ran, from the pod (`/workspace/jeeves-exec`):**
- `sovos-inspect-bridge` `gspc_axis_task()` built a real **`gspc-gov` Inspect
  Task** from **real board data** (150 samples served from the 4503-row
  `peritem_gov.jsonl`).
- Gold labels are the real board's: HIGH_RISK / LIMITED_RISK / MINIMAL_RISK /
  PROHIBITED — not synthetic.
- Deterministic gate scorer (never LLM-judge — arXiv:2606.26185 validated).

**Two bugs fixed (both real, both to the benefit of the plan):**
1. **Inspect 0.3.258 rejects raw functions as `scorer=`** (TypeError: Unexpected
   scorer type). Fixed by wrapping the deterministic gate in `@scorer(...)`
   at build time (`_to_inspect_scorer`) while keeping the standalone callable
   for the no-inspect test path. Bridge tests still 4/4.
2. The board's field names are `item`/`expected`, not `prompt`/`gold` — mapped
   correctly (the naive map silently produced 0 items; caught by an empty
   dataset error, never assumed).

**Environment (the real enabler):** `inspect_ai 0.3.258` installed into the pod
venv (`/workspace/venv-test`). Working from the pod (Mac = editor only).

**Next step toward registration:** wrap the full axis, run against the Ollama
fleet, and register in `inspect_evals` (UK AISI / Arcadia / Vector) to open the
NPL Centre for AI Measurement conversation. Owner-gated only at the actual
external register/submit step.
