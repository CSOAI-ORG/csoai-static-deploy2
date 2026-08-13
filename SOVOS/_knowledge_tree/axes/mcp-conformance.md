# Axis: conformance (mcp)
## 1. What it measures
- Anchor: MCP tool conformance. Bank: n=35, labels={'VIOLATES': 17, 'CONFORMS': 18}. On HF+Kaggle (13/13).
## 2. Working components
- Measurements: gspc-mcp board — UNMEASURED (weak fleet; richer-fleet re-run owed via durable_board resume, which skips only MEASURED).
- Tooling: bench.py (field-resolver handles this schema), tail.py (correlated-failure), durable_board.py.
- Middle to automate: run->board->card->spray (all built; needs a stable fleet).
## 3. SWOT
- S: bank public, n=35 clears n>=30 floor; law-anchored deterministic gold.
- W: UNMEASURED; bank ok.
- O: MCP tool conformance is a live regulatory driver.
- T: no deterministic MCP conformance benchmark published - greenfield-ish.
## 4. Market & demographics
- Buyer: deployers/auditors under MCP tool conformance. Delivery: paygo SaaS + A2A API.
## 5. Competitor intel
- no deterministic MCP conformance benchmark published - greenfield-ish.
## 6. EAT (6 gates)
- Ingest named domain benchmarks; author items to n>=60 where thin; crosswalk to the standard.
## 7. SOV City surface
- End-user asks SOV about conformance; SOV auto-runs the board, shows the conformance sim (fleet-fragile items highlighted red).
