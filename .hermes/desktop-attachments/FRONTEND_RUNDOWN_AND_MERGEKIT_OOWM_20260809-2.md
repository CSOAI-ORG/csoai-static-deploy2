# Full front-end rundown + the mergekit-OOWM verdict

*9 Aug 2026 · Part 1 is every live surface, checked this session. Part 2 answers your real question:
can we mergekit all our top specialists into a new top-tier OOWM "sandwich brain"? Honest answer —
the technique is real; the premise (that we have winning specialists) is not, yet. Here's exactly how
to make it real.*

---

# PART 1 — FRONT-END RUNDOWN (live-checked)

| surface | state now | note |
|---|---|---|
| **csoai.org** (apex) | ✅ **live, on-message** | "measurement body… never certificates of conformity… UNMEASURED is reported." Clean. |
| **csoai.org/arena** | 🔴 **DOWN — HTTP 522** | Cloudflare can't reach origin. The arena route is erroring right now. Fix origin / redeploy. |
| **councilof.ai** | ✅ **cleaned** | No BFT / quorum / certification language anymore — the integrity fix landed. Good. |
| **meok.ai** | ✅ live, consumer-clear | "Sovereign AI, one memory"; pricing Free/£12.99/PAYG. Rides on "Launch MEOK OS" actually booting (unverified). |
| **passport tool** (`/tools/article50-passport.html`) | ⚠️ **claim still to pull** | "23/33 threshold / court-admissible" on the Governance tier — forbidden. In corrections pack. |
| **/govbench** | ✅ fixed | two programmes separated, CIs + n present. |
| **templeman-opticians.com** | ✅ fixed (Science) | serves 200 from CF Pages; Vercel 402 gone. |
| **os.csoai.org** | ⚠️ in progress (Science) | CNAME→pages.dev switch pending; certification page reframed to "Watchdog Analyst." On-thesis. |
| **HF Spaces (12 tools)** | ✅ live | the tool suite runs. |
| **arena_public.html / csoai_arena_board.html** | ✅ built here | honest board, ready to deploy as the real /arena. |

**Front-end priorities, ranked:** (1) **/arena 522** — it's your flagship route and it's erroring; (2) pull the
passport "23/33/court-admissible" claim; (3) deploy the honest board to /arena; (4) finish os.csoai.org CNAME.

---

# PART 2 — CAN WE MERGEKIT A TOP-TIER OOWM? THE HONEST VERDICT

## Short answer

**The method is real. The premise is broken. Fix the premise and it works.**

- ✅ **Mergekit is legitimate.** Merging same-architecture models into one ("sandwich" = passthrough
  layer-stacking; "hive" = TIES/DARE weight-blending) is a proven technique. Your "OOWM clusters /
  sandwich brain" framing maps exactly onto it.
- ❌ **But you can't merge OUR specialists — because none of them are specialists.** Measured this
  session: **every** sovereign model (sov34, sov-gate, sov-compliance-art5, sov-ethics-art5) **loses to
  base Qwen on every axis.** A weight-merge **interpolates** parents; it does **not** invent capability
  none of them have. Merging four sub-baseline models yields something **≤ base**, not top-tier. Garbage
  in → garbage merged.

**"Merge the top specialist from each benchmark" only works if a real top specialist exists for each
benchmark. Right now, the top specialist for every axis is plain base Qwen.**

## The two honest routes to a real OOWM merge

### Route A — merge strong OPEN specialists (fast, testable)
Merge genuinely-capable open models in **one architecture family** (must match — you can't merge Qwen
weights with Llama). Same size too (can't weight-merge 7B with 1.5B).

- Family: **Qwen2.5-7B** (your base's family, scaled up). Components:
  - `Qwen/Qwen2.5-7B-Instruct` (general reasoning/instruct — the strong core)
  - a strong **reasoning** Qwen2.5-7B fine-tune
  - a strong **safety/refusal** Qwen2.5-7B fine-tune
- Merge with **TIES** or **DARE-TIES** (sign-consensus, density-pruned) — *not* raw passthrough.
- **Then measure the merge in the frozen arena vs base-7B and vs each component.** It wins only if it
  beats *both* with disjoint Wilson CIs / McNemar p<0.05.

### Route B — build real specialists first, then merge (slower, yours)
Our fine-tunes failed because refusal-tuning caused **catastrophic forgetting**. To make real per-axis
specialists:
1. Fine-tune with **rehearsal/replay** data (mix general + governance) so the model doesn't forget.
2. **Verify each specialist beats base on its axis** in the arena — if it doesn't, it's not a specialist,
   don't merge it.
3. Merge only the verified winners (TIES). Measure the merge.

## The actual recipe (mergekit.yaml — Route A starter)

```yaml
# oowm-merge-v1.yaml  —  Qwen2.5-7B family, TIES
merge_method: ties
base_model: Qwen/Qwen2.5-7B          # the shared base all components fine-tune from
dtype: bfloat16
models:
  - model: Qwen/Qwen2.5-7B-Instruct   # general/instruct core
    parameters: { weight: 0.5, density: 0.6 }
  - model: <strong-reasoning-qwen2.5-7B-ft>
    parameters: { weight: 0.3, density: 0.5 }
  - model: <strong-safety-qwen2.5-7B-ft>
    parameters: { weight: 0.2, density: 0.5 }
parameters:
  normalize: true
  int8_mask: true
tokenizer_source: base
```
```bash
pip install mergekit
mergekit-yaml oowm-merge-v1.yaml ./oowm-merge-v1 --cuda --allow-crimes
# then convert to GGUF and score in the SAME arena harness:
#   python3 sweep.py   # oowm-merge-v1 vs base-7B vs each component, 9 axes, Wilson+McNemar
```

## Hard constraints (the guardrails that keep it honest)

1. **Same architecture + size + tokenizer** to merge. Qwen2.5-7B with Qwen2.5-7B. Not cross-family, not cross-size.
2. **The arena is the judge.** No merge is "top-tier" until it beats base *and* its best component with a
   computed separation. We already have the harness (`sweep.py`); reuse it unchanged.
3. **Contamination gate.** No component's training data may contain the gspc items/labels (the sov33-strong
   82KB answer-key lesson). A merge that memorised the test isn't a model, it's a lookup table.
4. **"Convert to 3kb" is the RECORD, not the weights.** Measure the full merged model first; the 3KB j-card
   is a signed *summary* of the result, never a compression of the capability.
5. **Needs GPU + safetensors.** GGUF can't be merged; this runs on the RunPod/Science GPU, not Cowork CPU.

## The other OOWM (don't forget it)

The **composed** OOWM — base + **retrieval** over your 778-passage KB + router — is a *separate, possibly
better* path than merging weights. Retrieval of the actual statute text can lift governance where
fine-tuning didn't — **if** the KB is reference material, not the answer key (verify first; that's TUI-11's
job). Merge (Route A/B) and retrieval (RAG) are both legitimate; **measure both in the same arena and keep
whichever wins.**

---

## Bottom line

Yes — a mergekit OOWM is possible and it's the right idea. But the honest version is: **merge real
specialists (strong open Qwen2.5-7B models), gate every merge through the arena, and only crown one
"top-tier OOWM" when it beats base with a computed separation.** Merging our current sovereigns would just
average four models that already lose. The scoreboard tells you which merge is real — that's the whole point
of having built it.

*Verified this session: councilof.ai clean, csoai.org/arena 522, HF merge-candidate pool (Qwen2.5-7B family
mergeable with base). All model scores are measured, not assumed. Measurement, not certification.*
