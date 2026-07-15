# 🐉 Batch build — Sovereign fusion, honest results (2026-07-14)
_Phased batch, EAT mode. Honesty register: real results incl. one negative. All local, no GPU/keys._

## Through-line (proven on our OWN weights this batch)
**Fuse/route at the OUTPUT level — never merge heterogeneous (or even our own) weights blindly.** Weight-merging
our 4 same-base OWEM adapters COLLAPSED the model; routing + output-fusion worked. Same lesson as the whole estate.

## Phase 1 — diagnose OWEM adapters ✅
Each adapter works SOLO (base coherent; `compliance` alone gave a real EU-AI-Act answer). Rank 16, q/k/v/o.

## Phase 2 — OWEM weight-merge FAILS (honest negative result) ✅
- `add_weighted_adapter(linear, 0.25×4)` → degenerate ("assistant assistant…").
- `add_weighted_adapter(cat)` → degenerate ("SIG SIG…").
- **Root cause:** the 0.6B base can't absorb 4 strong skill-adapters at once — capacity collapse. Broken merged
  adapter **deleted, not shipped** (honesty).
- **Working alternative — `sov33_owem_router.py`:** embed-route the query → hot-swap the right OWEM LoRA → answer
  → sign. Verified: compliance/defense/voice questions routed correctly, coherent, all signed. Routing beats
  merging on our own weights — the fluid thesis, confirmed.

## Phase 3 — unified Sovereign pipeline ✅ (`sovereign_pipeline.py`)
One entry point, one signed decision: **RAG-ground → care-floor → multi-model propose → GROUNDED care-gate
(drop contradictors) → fuse → Ed25519-sign.** Verified: 2 governance Qs grounded+answered+signed; 1 nonsense Q
correctly ABSTAINED; all receipts verify. This is the coherent product core, composed from the pieces that work.

## Honest limits
- Small local models (0.6B–1.7B) → answers are coherent but thin; facts come from RAG, not the weights.
- Fusion cost = multiple model calls (sequential on 16GB). Big councils need free GPU (owner-gated).
- The OWEM merge negative result stands — don't retry weight-merging the 0.6B experts; route them.

## Files (this batch)
sov33_owem_merge.py (documented failure) · sov33_owem_router.py (works) · sovereign_pipeline.py (capstone) ·
sov33_bft_vs_moa.py + _real.py (publishable differentiator) · benchmarks/*_2026-07-14.json (all signed).
