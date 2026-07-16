# SOV4 ALIGNED STATE — everything we now know (2026-07-16, afternoon)
_RUNNING ✅ / TESTED 🔬 / DESIGNED 🧩 / GATED ⏸️. Every claim traces to a commit._

## THE ENGINE IS LIVE
- **BRUM running on the Mac** ✅ — `./launch_brum.sh` → governed OpenAI endpoint :8802
  (care-floor 0.35 + SIGIL signing ON; 5 backends: groq/nvidia/ollama/kimi/claude)
- Launch script hardened: auto-uses `.venv` (→ trained router), kills stale server on :8802,
  root status page (no more "not found"). Client: point Open WebUI at http://localhost:8802/v1
- **Full E2E chain verified**: route → care-gate → SIGIL → JRUM → TRUM/CRUM (CHAIN COMPLETE=True)

## THE ROUTER — recalibrated today (the real unblock)
| metric | v1 | v2 (current) |
|---|---|---|
| accuracy (held-out) | 0.716 | **0.822** |
| confidence stdev | 0.060 (flat) | **0.292** (discriminates) |
| conf when CORRECT | ~flat | **0.922** |
| conf when WRONG | ~flat | **0.342** |
| GDPR Qs → compliance | 3/24 (misrouted to defense) | **24/24** |
- vs keyword venturi baseline 0.393. v2 wired, v1 fallback. Isotonic calibration + balanced + terse examples.
- WHY IT MATTERS: confidence now tracks correctness → dynamic confidence-routing is now POSSIBLE (was not).

## THE EMERGENCE QUESTION — answered honestly (no spend)
- Hardened eval (24 tough gov Qs): **Qwen 0.917 / Bamba 0.708, rho=0.138 (LOW), oracle_headroom 0.042**
- **Thesis VALIDATED**: low rho = the MoE and SSM brains are genuinely decorrelated (different architectures work).
- **But capture is blocked, not by needing a 3rd brain** — headroom is 1 item; the fix was router calibration (done).
- **Ratio question (90/10?) answered NO**: can't weight-mix different architectures; fixed ratio dilutes;
  dynamic ratio needs a discriminating confidence signal — which v1 lacked and v2 now HAS.
- **NO flagship spend** — saved ~$15 re-run + ~$130-750 3rd brain. Decision backed by measured numbers.

## THE 7 SPINES (verified across runs; honest record)
DRUM (when) · KRUM (trust) · ARUM (layers) · SRUM (swarm) · JRUM (journal/dream/forest) ·
TRUM (render transform) · CRUM (creative representation) · + BRUM (intelligence engine, unifies router+brains+swarm)

## BUILT THIS SESSION (all committed)
- BRUM engine spine + launch_brum.sh + shim root page
- Trained router v1 (0.716) → recalibrated v2 (0.822, confidence discriminates)
- JRUM/TRUM/CRUM spines; dream cycle; evolve forest; co-evaluator
- Memory path bug fixed (37 modules) + sov33_paths.py resolver
- Hardened emergence eval + honest confidence-routing negative→fix

## NEXT (priority, all ~$0 unless noted)
1. **Confirm v2 router on the live engine** — relaunch, verify preflight says `trained_router` not fallback.
2. **Re-run confidence-routing test with v2** (now that confidence discriminates) — does routing-by-confidence
   beat best-single? This is the honest test of "dynamic ratio helps" — only worth a paid eval if a
   HARDER battery leaves real headroom (>1 item). Current headroom (1 item) still too small to be conclusive.
3. **Harden the battery further** (co-evaluator) so headroom >1 item → then a paid re-run is conclusive.
4. Migrate remaining 35 modules to sov33_paths.py; wire dream-loop scheduler.

## HONEST GATES (unchanged)
- No flagship 3rd-brain spend until a harder battery shows headroom the v2 confidence-router can capture.
- BRUM generation needs a model endpoint (NVIDIA NIM live / owned adapters) — routes correctly regardless.
- The mission: the one system where manipulation CAN'T hide — every value signed, every visual traced.
