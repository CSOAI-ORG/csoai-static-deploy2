# Axis: safety (agi)
## 1. What it measures
- Anchor: agentic safety refusal. Bank: n=36, labels={'COMPLY': 19, 'REFUSE': 17}. On HF+Kaggle (13/13).
## 2. Working components
- Measurements: gspc-agi board — UNMEASURED (weak fleet; richer-fleet re-run owed via durable_board resume, which skips only MEASURED).
- Tooling: bench.py (field-resolver handles this schema), tail.py (correlated-failure), durable_board.py.
- Middle to automate: run->board->card->spray (all built; needs a stable fleet).
## 3. SWOT
- S: bank public, n=36 clears n>=30 floor; law-anchored deterministic gold.
- W: UNMEASURED; bank ok.
- O: agentic safety refusal is a live regulatory driver.
- T: AgentHarm/HarmBench measure agentic safety; ours is law-classed + sign
## 4. Market & demographics
- Buyer: deployers/auditors under agentic safety refusal. Delivery: paygo SaaS + A2A API.
## 5. Competitor intel
- AgentHarm/HarmBench measure agentic safety; ours is law-classed + signed.
## 6. EAT (6 gates)
- Ingest named domain benchmarks; author items to n>=60 where thin; crosswalk to the standard.
## 7. SOV City surface
- End-user asks SOV about safety; SOV auto-runs the board, shows the safety sim (fleet-fragile items highlighted red).
