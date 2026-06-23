# Sovereign Town Open Benchmark Harness

Run the same deterministic town under different governance policies and compare outcomes.

## Quick start

```bash
# Compare built-in policies
python -m benchmark compare --policies sovereign,ungoverned,strict --scenario baseline --district aqua

# Run and sign a result
python -m benchmark run --policy sovereign --scenario scarcity_shock --district aqua --sign

# Verify a signed manifest
python -m benchmark verify benchmark_runs/<id>.json
```

## Writing a custom policy

Create a Python class with a `decide(observation)` method:

```python
from benchmark import GovernancePolicy

class MyPolicy(GovernancePolicy):
    name = "my_policy"
    def decide(self, observation):
        if observation["intended_action"] == "steal":
            return {"verdict": "deny", "reason": "no theft"}
        return {"verdict": "allow"}
```

Then run it by dotted path:

```bash
python -m benchmark run --policy my_module:MyPolicy --scenario baseline
```

## Scoring

Benchmark runs are scored across five dimensions:

- **Safety**: crimes, deaths, lawlessness
- **Prosperity**: commons health, work accuracy
- **Equity**: trust, survival, mutual aid
- **Liberty**: intervention cost (blocks + welfare)
- **Stability**: variance across the run

No single scalar — policies are compared on a Pareto front.

## Scenarios

- `baseline`
- `enforcement_gap_50`, `enforcement_gap_0`
- `scarcity_shock`
- `contagion_surge`
- `climate_stress`

## Attestation

Signed manifests use the existing Ed25519 keypair (`town_pub.key` / `.town_priv.key`).
Third parties can verify a manifest without trusting the submitter.
