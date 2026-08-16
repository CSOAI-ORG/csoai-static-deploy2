# Axis: care (care)
## 1. What it measures
- Anchor: care-cost / over-refusal. Bank: n=200, labels={'1': 100, '0': 100}. On HF+Kaggle (13/13).
## 2. Working components
- Measurements: gspc-care board — UNMEASURED (weak fleet; richer-fleet re-run owed via durable_board resume, which skips only MEASURED).
- Tooling: bench.py (field-resolver handles this schema), tail.py (correlated-failure), durable_board.py.
- Middle to automate: run->board->card->spray (all built; needs a stable fleet).
## 3. SWOT
- S: bank public, n=200 clears n>=30 floor; law-anchored deterministic gold.
- W: UNMEASURED; bank ok.
- O: care-cost / over-refusal is a live regulatory driver.
- T: SycoBench/OR-Bench measure over-refusal; ours ties to care-cost + seve
## 4. Market & demographics
- Buyer: deployers/auditors under care-cost. Delivery: paygo SaaS + A2A API.
## 5. Competitor intel
- SycoBench/OR-Bench measure over-refusal; ours ties to care-cost + severity.
## 6. EAT (6 gates)
- Ingest named domain benchmarks; author items to n>=60 where thin; crosswalk to the standard.
## 7. SOV City surface
- End-user asks SOV about care; SOV auto-runs the board, shows the care sim (fleet-fragile items highlighted red).
