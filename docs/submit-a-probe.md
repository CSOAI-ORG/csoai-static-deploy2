# Submit a probe (gold-bank crowdsourcing)

External researchers can contribute measurement probes to the gold bank.

## Format
One JSON per probe: { "id", "axis", "input", "expected", "method_hash" }.

## Rules
- Probes must be deterministic — same input, same expected output, every time.
- No probe may target a specific named model to harm it; we measure classes of behavior.
- By contributing you license the probe CC-BY-4.0 (attribution: Council of AI measurement corpus).

## How
Open a PR adding your probe under the relevant axis directory, or open an issue with the probe inline. Every accepted probe is signed into the corpus with your credit.
