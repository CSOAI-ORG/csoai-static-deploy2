# SAFE-SANDBOX SIMULATION — Rainbow-Security × 13-Axis Arena (2026-08-13)

**Owner directive (mining):** consolidate our security hive (Rainbow/ASI) with
the 13-axis arena into a **safe-sandbox simulation** — our model vs others,
security-gated, on the pod (safe, no live blast radius).

## What the mine found (we own far more than "1 bank")
| Asset | Where | State |
|---|---|---|
| **13-axis board estate** | `SOVOS/boards-v2-2026-08-12/peritem_*.jsonl` | **13/13 MEASURED**, 15,580 rows, 19 models, real law-anchored gold |
| **Rainbow Security (7-layer)** | `sovos-hive/rust-kernel/src/rainbow.rs` (Rust) | 7 defense layers: RED phys / ORANGE net / YELLOW behav / GREEN temporal / BLUE symbolic / INDIGO cognitive / VIOLET PQ |
| **Rainbow rotate control-plane** | `sovereign-temple-public/security/rainbow_rotate.py` | IP-rotation schedule (stub control plane) |
| **asisecurity packs** | `_alignment/asisecurity-audit`, `meok-labs-engine/.../asisecurity.*` | ASI-security research + industry packs |
| **simulation surfaces** | `csoai-platform/UX_RAINBOW_SIMULATION_REPORT.md`, `rainbow-simulation.test.ts`, `csoai-org-v2` sandbox/simulation pages | productized sim UI + tests |

## What I built (Rust -> Python, so it runs on the pod's Python stack)
1. **`sovos_city/rainbow_gate.py`** — faithful Python port of `rainbow.rs`
   (`Operation.validate()` must pass ALL 7 layers, each layer blocks its
   violation). Tested: 7 layers present, clean op passes, each layer blocks.
2. **`sovos_city/simulator.py`** — `SafeSandboxSimulator`: runs a model on a
   real per-axis board, rainbow-gates every interaction (injection-signal →
   Indigo layer), deterministically scores survivors, signs via the Chain.
3. **`tests/test_rainbow_simulator.py`** — 6/6 pass on the pod.

## Verified on the pod (real 13-axis data)
Ran the safe-sandbox across **all 13 axes**, our model (`sov6-preservation`)
vs 3 others: **6,240 rows emitted + signed**, Rainbow **Indigo (cognitive,
prompt-injection) layer firing on swarm + xr** (480 blocks each — the axes
whose item text carries injection vocabulary). No live blast radius — pure
simulation on the owned board estate.

## What this means
- The **security hive is now callable from the measurement stack** (not just a
  Rust kernel on disk) — Rainbow gate + simulator on the pod.
- We can **show a safe simulation: our model vs others, rainbow-gated, signed**,
  across the whole 13-axis arena — each emitted row is owned training data.
- Honesty: this is the internal harness; a public demo is a separate
  owner-gated surface. "Simulation" not "evaluation of live third parties".

## Durable facts (from this + prior passes)
- Public layer = **"Council City"** (SOV/SOV City never ships — Sovos
  Compliance US #6876686).
- Moat = signed + law-anchored + positive controls + honest Wilson intervals.
