# Axis: continuity (asi)
## 1. What it measures
- Anchor: post-quantum cryptography (Falcon/FrodoKEM -> quantum-safe/vulnerable). Bank: n=33, labels={'NOT_APPLICABLE': 11, 'QUANTUM_SAFE': 13, 'QUANTUM_VULNERABLE': 9}. On HF+Kaggle (13/13).
## 2. Working components
- Measurements: gspc-asi board — UNMEASURED (weak fleet; richer-fleet re-run owed via durable_board resume, which skips only MEASURED).
- Tooling: bench.py (field-resolver handles this schema), tail.py (correlated-failure), durable_board.py.
- Middle to automate: run->board->card->spray (all built; needs a stable fleet).
## 3. SWOT
- S: bank public, n=33 clears n>=30 floor; law-anchored deterministic gold.
- W: UNMEASURED; bank ok.
- O: post-quantum cryptography is a live regulatory driver.
- T: NIST PQC migration guidance; no signed law-anchored bank like ours.
## 4. Market & demographics
- Buyer: deployers/auditors under post-quantum cryptography (Falcon. Delivery: paygo SaaS + A2A API.
## 5. Competitor intel
- NIST PQC migration guidance; no signed law-anchored bank like ours.
## 6. EAT (6 gates)
- Ingest named domain benchmarks; author items to n>=60 where thin; crosswalk to the standard.
## 7. SOV City surface
- End-user asks SOV about continuity; SOV auto-runs the board, shows the continuity sim (fleet-fragile items highlighted red).
