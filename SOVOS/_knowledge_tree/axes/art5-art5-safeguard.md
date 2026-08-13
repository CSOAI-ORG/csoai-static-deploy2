# Axis: art5-safeguard (art5)
## 1. What it measures
- Anchor: EU AI Act Art 5 prohibited practices. Bank: n=36, labels={'PERMITTED': 19, 'PROHIBITED': 17}. On HF+Kaggle (13/13).
## 2. Working components
- Measurements: gspc-art5 board — UNMEASURED (weak fleet; richer-fleet re-run owed via durable_board resume, which skips only MEASURED).
- Tooling: bench.py (field-resolver handles this schema), tail.py (correlated-failure), durable_board.py.
- Middle to automate: run->board->card->spray (all built; needs a stable fleet).
## 3. SWOT
- S: bank public, n=36 clears n>=30 floor; law-anchored deterministic gold.
- W: UNMEASURED; bank ok.
- O: EU AI Act Art 5 prohibited practices is a live regulatory driver.
- T: DarkBench/DarkPatterns-LLM cite EU AI Act; ours is PROHIBITED/DISCLOSE
## 4. Market & demographics
- Buyer: deployers/auditors under EU AI Act Art 5 prohibited practices. Delivery: paygo SaaS + A2A API.
## 5. Competitor intel
- DarkBench/DarkPatterns-LLM cite EU AI Act; ours is PROHIBITED/DISCLOSE/PERMITTED legally-classed.
## 6. EAT (6 gates)
- Ingest named domain benchmarks; author items to n>=60 where thin; crosswalk to the standard.
## 7. SOV City surface
- End-user asks SOV about art5-safeguard; SOV auto-runs the board, shows the art5-safeguard sim (fleet-fragile items highlighted red).
