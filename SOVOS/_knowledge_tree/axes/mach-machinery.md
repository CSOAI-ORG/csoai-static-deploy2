# Axis: machinery (mach)
## 1. What it measures
- Anchor: Machinery Reg 2023/1230 / ISO 10218. Bank: n=33, labels={'PART_A': 12, 'NOT_SAFETY_FUNCTION': 9, 'OUT_OF_SCOPE': 12}. On HF+Kaggle (13/13).
## 2. Working components
- Measurements: gspc-mach board — UNMEASURED (weak fleet; richer-fleet re-run owed via durable_board resume, which skips only MEASURED).
- Tooling: bench.py (field-resolver handles this schema), tail.py (correlated-failure), durable_board.py.
- Middle to automate: run->board->card->spray (all built; needs a stable fleet).
## 3. SWOT
- S: bank public, n=33 clears n>=30 floor; law-anchored deterministic gold.
- W: UNMEASURED; bank ok.
- O: Machinery Reg 2023/1230 / ISO 10218 is a live regulatory driver.
- T: ISO 10218 is the standard; we measure behavioral conformance to it.
## 4. Market & demographics
- Buyer: deployers/auditors under Machinery Reg 2023. Delivery: paygo SaaS + A2A API.
## 5. Competitor intel
- ISO 10218 is the standard; we measure behavioral conformance to it.
## 6. EAT (6 gates)
- Ingest named domain benchmarks; author items to n>=60 where thin; crosswalk to the standard.
## 7. SOV City surface
- End-user asks SOV about machinery; SOV auto-runs the board, shows the machinery sim (fleet-fragile items highlighted red).
