# Axis: swarm (swarm)
## 1. What it measures
- Anchor: multi-agent coordination safety. Bank: n=41, labels={'CONSENSUS_CORRECT': 39, 'CONSENSUS_WRONG': 1, 'CANARY': 1}. On HF+Kaggle (13/13).
## 2. Working components
- Measurements: gspc-swarm board — UNMEASURED (weak fleet; richer-fleet re-run owed via durable_board resume, which skips only MEASURED).
- Tooling: bench.py (field-resolver handles this schema), tail.py (correlated-failure), durable_board.py.
- Middle to automate: run->board->card->spray (all built; needs a stable fleet).
## 3. SWOT
- S: bank public, n=41 clears n>=30 floor; law-anchored deterministic gold.
- W: UNMEASURED; bank ok.
- O: multi-agent coordination safety is a live regulatory driver.
- T: SwarmBench (arXiv:2505.04364) is the base; ours adds law-graded coordi
## 4. Market & demographics
- Buyer: deployers/auditors under multi-agent coordination safety. Delivery: paygo SaaS + A2A API.
## 5. Competitor intel
- SwarmBench (arXiv:2505.04364) is the base; ours adds law-graded coordination.
## 6. EAT (6 gates)
- Ingest named domain benchmarks; author items to n>=60 where thin; crosswalk to the standard.
## 7. SOV City surface
- End-user asks SOV about swarm; SOV auto-runs the board, shows the swarm sim (fleet-fragile items highlighted red).
