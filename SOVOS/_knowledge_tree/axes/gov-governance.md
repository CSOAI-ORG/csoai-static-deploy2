# Axis: governance (gov)
## 1. What it measures
- Anchor: EU AI Act Art 5 risk-tiering. Labels: from bank. Bank: n=237, MEASURED, HF+Kaggle.
## 2. Working components (inventory)
- Measurements: gspc-gov board — sovereign best 0.392 > base 0.291 (MEASURED). tail: 48.3% correlated-failure.
- Tooling: bench.py (deterministic), tail.py (correlated-failure), durable_board.py (HF-push).
- Procedures: n≥30 floor, Wilson CI, unparsed=incorrect, canary excluded.
- Fixes done: card scrubbed of sov34 (0 hits live). Middle to automate: the run→board→card→spray chain (spray.py exists).
## 3. SWOT
- S: only MEASURED axis with sovereign>base + a published correlated-failure number. n=237 (biggest bank).
- W: single-fleet (5 models); cross-lab blocked on OpenRouter.
- O: the greenfield paper (correlated over-refusal) lives HERE. NIST AI 800-3 Wilson mandate cites us.
- T: Credo/Holistic have governance "coverage" (docs, not measurement) — must keep the behavioral-vs-paperwork wedge sharp.
## 4. Market & demographics
- Buyer: EU AI Act deployers, insurers (NAIC supplement), auditors. Driver: Art 5 in force 2 Feb 2026.
## 5. Competitor intel
- Credo/Holistic: document governance. Arena: measures preference. Neither measures Art-5 obedience deterministically+signed. WE DO.
## 6. EAT
- Ingest (6 gates): Meta Muse Glimmer 30B (reproducible target), DarkBench for cross-check. Crosswalk: NIST AI RMF, ISO 42001.
## 7. SOV City surface
- End-user asks SOV "is my AI Art-5 compliant?" → auto-runs gov board → shows SOV City sim of the 237 items + the correlated-failure heatmap (the 20 fleet-fragile items lit red).
