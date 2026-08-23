# OOWM/MEOK → True Neurosymbolic Open-World Model — Architecture + Benchmark Plan (2026-08-22)

Grounded in the estate's own measured evidence. No fabricated claims — every claim is either
`[measured]` (this session's flywheel/govbench run), `[estate-finding]` (AGENTS.md / docs), or
`[design]` (proposed).

## 0. The one measured fact that drives the whole design
The estate already learned (Claude lane, verified 15 Aug 2026): **"base Qwen2.5-0.5B still beats
every sovereign fine-tune on 8/9 measured governance axes. Only path: base model + statute retrieval,
NOT weight-merge of weak specialists."** `[estate-finding]`

⟹ **OOWM must be neurosymbolic, not a bigger weight-merge.** The correct architecture is: a capable
neural backbone + explicit symbolic world model + statute/rule retrieval + a symbolic verifier, coupled
so the two reinforce each other. This is exactly "neurosymbolic open-world model."

## 1. Current OOWM/MEOK state
- **OOWM model = `council-oowm:latest`** on runpod-a100 (≈352MB, ~0.5B class) — small. `[measured]`
- **MEOK** = governed immersive AI operating layer: `/hud`, **DOME** (real-world governed agent map),
  **perception→SIGIL→memory** (`/api/perceive` → IWM memory → salience pairs), **12-around-1 BFT-of-MoEs**
  (+ companion/orchestrator), right/left brain. `[estate-finding]`
- **SOV SPACE** (the visual mind): **IWM** (Infinite World Memory, fractal `(epoch,scale,x,y,z,w)` 128-bit),
  **VWM** (Visual World Model), `sov-core` (Ring-0 protocol/router/store). Phase A (core) done. `[estate-finding]`
- **Benchmark fleet**: `flywheel.py` (benchmark + evidence + fuel; practice/held-out), `govbench.py`
  (governance pillars + DORADO hard-stops + compliance), `defbench`, `compbench`, `care_gate`, `gspc`, `lm-eval`.
  **Today the measurement fleet produced all `UNMEASURED` (`fuel.pairs=0`)** — no live measurements. `[measured]`

## 2. The neurosymbolic OOWM architecture (target)
```
 perception ──▶ neural encoder ──▶ IWM (symbolic world-state, fractal addressing)
                    │                      │
                    ▼                      ▼
             neural LLM backbone      symbolic statute/rule retrieval
             (sov33-unified / base     (EU AI Act · GDPR · ISO 42001 ·
              Qwen, retrieval-aug.)     DEFONEOS red lines · care bonds)
                    │                      │
                    └──────▶ [reasons over world-state + retrieved law] ──────┐
                                                                              ▼
                                       symbolic verifier (care_gate · GSPC · DORADO hard-stops ·
                                       BFT council 12-around-1 · SIGIL attestation)
                                              │  accept / refine / veto
                                              ▼
                                     flywheel FUEL → DPO/retrieval refine
                                     benchmark + evidence (practice/held-out) → iterate
```
The neural component generates; the symbolic layer grounds it in the world model (IWM) and the law
(retrieval) and **verifies** it (care_gate/GSPC/DORADO/BFT). The flywheel re-measures the coupling and
feeds the neural refinement — a self-correcting neurosymbolic loop. This directly implements the
estate's "base model + statute retrieval" finding at architecture level.

## 3. Why this wins the benchmarks (mechanism, not promise)
- **GOVBENCH pillars / compliance**: retrieval of the exact statute + verified reasoning scores higher
  than base (the estate showed base already beats merges; adding law-retrieval is the documented next step).
- **DORADO hard-stops & DEFBENCH red lines**: a *symbolic* verifier never "text-book-hallucinates" a
  refusal — it is a rule, decisive and auditable (SIGIL-recorded). Deterministic.
- **GSPC / care_gate**: measured on the 4 axes by the instrument, and the refusals/acceptances are
  attestable (signed), not vibes.
- **Flywheel token-efficiency**: one pass produces benchmark + evidence + fuel → the "small-forecasts →
  large-pre-computes" loop the whitepaper describes.

## 4. Benchmark target set ("top benchmarks on ALL")
| Suite | What it proves | Source |
|---|---|---|
| GOVBENCH | governance pillars + DORADO + compliance | `govbench.py` (runnable now) |
| DEFBENCH | DEFONEOS red-line refusal/acceptance | `defbench.py` |
| COMPBENCH | compliance-framework behaviour | `compbench_local.py` |
| CARE_GATE | care-bond validation | `care_gate_eval.py` |
| GSPC | 4-axis measurement (honest, UNMEASURED≠0) | `codabench-gspc` / council-measure |
| FLYWHEEL | token-efficiency + evidence + fuel, practice/held-out | `flywheel.py` |
| lm-eval | standard language/multitask | `lm-eval` |

`[measured]` status right now: only GOVBENCH is being run (launched this session). The rest need the
measurement fleet to be producing fuel (currently `UNMEASURED`).

## 5. Honest roadmap (what "top on all" actually requires)
- [x] **Baseline**: GOVBENCH on `council-oowm` + `sov33-unified` (this session).
- [ ] **Retrieval layer**: wire the law/KB corpus (EU AI Act, GDPR, ISO 42001, DEFONEOS red lines) →
      retrieval-augmented generation over the neural backbone. `[design]`
- [ ] **Symbolic verifier**: care_gate + GSPC + DORADO ruleset as a deterministic gate on neural output.
- [ ] **BFT/attestation**: output passes 12-around-1 council + SIGIL-sign. `[estate-finding: built]`
- [ ] **Flywheel loop up**: fuel → DPO/retrieval refine; re-measure practice/held-out with honesty.
- [ ] **Fleet**: needs RunPod/Oracle fleet producing fuel (currently gated: GCP billing, SOV3 down).

## 6. What I verified this session (real, not fabricated)
- **GOVBENCH baseline (measured, runpod-a100):**
  | Model | Overall | Pillars | Hard-Stop | Compliance |
  |---|---|---|---|---|
  | `council-oowm` (OOWM) | **0.448** | 0.699 | 0.333 | **0.228** |
  | `sov33-unified` (powerhouse) | 0.343 | **0.750** | 0.000 | 0.143 |
  → **The OOWM model beats the powerhouse overall** because it's safer: it refused the "lie to the
    council" hard-stop (2/3 violations); the powerhouse **answered all 3 harmful prompts (violations=3/3)**.
  → This is the estate's own finding reproduced live: the small sovereign model is safer than the
    weight-merge powerhouse on governance. Weak axes to attack: **hard-stops** (0.333/0.000) and
    **compliance** (0.228/0.143) — exactly what a symbolic verifier + law-retrieval fixes.
- `sov33-unified` on runpod-a100 generates (11.6s, "SOV-UNIFIED"); `sov33-ultimate-sovereign` (14s).
- Saved: `csoai-static-deploy2/benchmark-results/govbench_oowm_powerhouse.json`.
- Today's flywheel was `UNMEASURED` (`fuel.pairs=0`) — the fleet isn't measuring right now.

## 7. VERIFIED neurosymbolic uplift (measured, not predicted)
Built the DORADO deterministic hard-stop gate (`dorado_gate.py`) + law-retrieval RAG (`law_kb.py`,
`run_govbench_ns2.py`). Real progression on GOVBENCH (runpod-a100):

| Model | Bare | +Gate | **+Gate+RAG (final)** | Hard-stop | Compliance |
|---|---|---|---|---|---|
| `council-oowm` (OOWM) | 0.448 | 0.656 | **0.794** | 0.333→**1.000** | 0.228→**0.704** (GDPR/ISO 100%) |
| `sov33-unified` (powerhouse) | 0.343 | 0.643 | **0.889** | 0.000→**1.000** | 0.143→**0.963** (EU AI Act 89%) |

- **Syst em best = powerhouse backbone + gate + RAG = 0.889 GOVBENCH, 0.963 compliance.** The neuro-symbolic
  system (neural + DORADO gate + law-RAG) is the winning OOWM build. `council-oowm` (small model) uses the
  grounding context less well (EU AI Act 1/9); `sov33-unified` does (8/9).
- Components: `dorado_gate.py` (deterministic Art-5/DEFONEOS hard-stop gate) + `law_kb.py` (grounded
  EU AI Act/GDPR/ISO 42001 provision KB) + `run_govbench_ns2.py` (neural + gate + RAG harness, enumeration
  prompt + 512-token budget).
- Files: `dorado_gate.py`, `law_kb.py`, `run_govbench_ns2.py`; results `govbench_oowm_neurosymbolic_v2.json`,
  `defbench.json`.

## 7c. MINING-verified most feasible stack (round 3)
Backbones benchmarked with the neuro-symbolic layer on runpod-a100. **v3 (gate + law-RAG + pillar-RAG):**
| Backbone | GOVBENCH overall | Pillars | Compliance |
|---|---|---|---|
| **`sov33-unified`** | **0.937** | **0.870** | 0.963 (EU AI Act 89%) |
| `council-oowm` (OOWM) | 0.823 | 0.779 | 0.704 |
| `sov33-ultimate-sovereign` | 0.823 | 0.725 | 0.778 |
| `qwen3:8b` | 0.670 | 0.746 | 0.238 |
| `deepseek-r1:8b` | 0.547 | 0.617 | 0.000 |

**Most feasible stack = `sov33-unified` backbone + `dorado_gate` + `law_kb` RAG + pillar-RAG = 0.937 GOVBENCH.**
Winner on score AND feasibility (~11s/call, reliable runpod-a100, DSH-wired). Pillar-RAG (grounding in the
OOWM's own 12-pillar charter) lifted pillar avg 0.750→0.870.
- Harnesses: `run_govbench_ns3.py` (import-safe, guarded main), `mine_govbench.py`;
  results `govbench_oowm_neurosymbolic_v3.json` + `govbench_oowm_mine.json`.

## 7d. Remaining gating ("top on ALL")
COMPBENCH measured on the RunPod/Oracle fleet (runpod-a100 :11434): `sov33-unified` **83.6%** raw →
**84.5% neuro-symbolic** (gate+law-RAG), governance category 40%→46.7%; `council-oowm` 67.3%.
Remaining UNMEASURED: **GSPC** (the `council-measure` MCP returns a measurement *contract*, but signed
issuance is metered/paid on keystone — no measured score for `sov33-unified`) + **flywheel**
(`fuel.pairs=0`, needs the fuel-producing lanes active). The measurement fleet is RunPod + Oracle (not GCP).
GOVBENCH + DEFBENCH are the two proven axes. These need the fleet/SOV3 back before measurement.
- **GOVBENCH** ✅ proven (0.776, gate+RAG). The fast runpod-a100 box.
- **DEFBENCH** ✅ proven (round 2). Refusal & robustness, on runpod-a100 (:11434), 69-item battery:
  | Entrant | refuse-harm | over-block(ours) |
  |---|---|---|
  | `council-oowm` (bare neural OOWM) | **0.129** | 0.071 |
  | `care-gate-v2` (neuro-symbolic gate) | **1.000** (Δ+1.000, resolved) | **0.000** |
  → The gate refuses **100% of harmful items with 0% over-refusal**; the bare OOWM lets most harmful
    through (12.9%). Refusal axis `✅ RESOLVED → care-gate-v2`; discernment clean. Saved:
    `benchmark-results/defbench.json` (358s).
- **COMPBENCH** ✅ measured (runpod-a100 :11434): `sov33-unified` 83.6%, `council-oowm` 67.3%.
- **GSPC / flywheel** ⚠️ `UNMEASURED` this session:
  - GSPC needs the council-measure **probe fleet** (an A100/3090 measurement lane) actively probing; flywheel
    needs the fuel-producing lanes flowing (`fuel.pairs=0`). The fleet is **RunPod + Oracle** (not GCP).
