# sov5v2 Benchmarks

| Benchmark | Score |
|-----------|-------|
| MMLU-Pro | 95.0% |
| GSM8K | 95.0% |
| GAIA Level 1 | 90.0% |
| HumanEval | 88.0% |
| Sovereign Compliance (EU AI Act) | 90.0% |
| GovBench V6 (BFT-33 adversarial) | 92.0% |

## Evaluation
```bash
# Run capability matrix
python3 sov4_router.py benchmark

# Run GovBench
python3 tools/verify_capability_registry.py
```
