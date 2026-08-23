# IMPROVE sov33-evolved — concrete recipe (2026-08-22)

Date: 2026-08-22 · lane: K3 (spec) / LANE (train) · target: sov33-evolved (0.5B), the weakest model
(EAT baseline 3.3 → 11.4). Root cause: corrupted SYSPROMPT + narrow-merge design.

## 1. Why it's the sick one
- **Corrupted SYSPROMPT** (EAT_STATUS: "rebuilt AGAIN", garbage/duplicate tokens). A 0.5B is
  dominated by its prompt — a broken prompt crushes it.
- **Merge-not-train + narrow sovereign data** → catastrophic forgetting on general governance.
- **0.5B size** — inherent ceiling vs 7B/8B baseline.

## 2. The fix (estate's documented path: base + retrieval, NOT weight-merge)
1. **Rebuild the SYSPROMPT clean** from `Modelfile.sov33-evolved-v2` (the working reference), no
   duplicate/garbage tokens. Verify with the 8-question sovereign test (must hit 8/8).
2. **Don't weight-merge weak specialists.** Base model + **statute retrieval (RAG)** — the +31–38
   pt lever measured this session. RAG >> merge.
3. **Honey-inject** the 94,181-row honey into the retrieval pool for the weak dimensions
   (defence, sovereignty, accountability) — the dimensions with the biggest RAG gap.
4. **Re-measure on the 3090** (11439, one model per fresh load + EAT_DIRECTIVE) after each step —
   the baseline↔RAG gap is the improvement signal. Target: baseline 3.3% → ≥28%, RAG ≥ 45%.

## 3. Success signal
| Metric | Now | Target |
|---|---|---|
| Baseline | 3.3% | ≥28% (parity with sov33-v7) |
| RAG context | 11.4% | ≥45% |
| Sovereign test | — | 8/8 |

## 4. Gates
Rebuild + training = LANE/pod (needs RunPod SSH). Prompt-clean rebuild could be done locally if the
`Modelfile` + a base are reachable. No fabricated scores — sov33-evolved stays CONFOUNDED until
rebuilt + re-measured on the 3090.
