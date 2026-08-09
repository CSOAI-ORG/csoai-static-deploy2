#!/usr/bin/env python3
"""diversity_e2e.py — Calculate n_eff (effective sample size) for the sovereign roster.

Measures pairwise correlation (ρ) across all models in the govbench results.
Output: a JSON of pairwise ρ across all subjects.

Usage:
    python3 diversity_e2e.py
"""

import json
import sys
from pathlib import Path
from itertools import combinations

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results" / "govbench"


def load_model_scores() -> dict[str, dict[str, float]]:
    """Load dimension scores for each model from govbench results."""
    scores = {}
    for f in RESULTS.glob("*.json"):
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        
        # Handle both single model and multi-model files
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            model = entry.get("model")
            dimensions = entry.get("dimensions")
            if model and isinstance(dimensions, dict) and len(dimensions) > 0:
                scores[model] = dimensions
    return scores


def pairwise_correlation(scores: dict[str, dict[str, float]]) -> dict:
    """Calculate pairwise Pearson correlation between all model pairs."""
    models = sorted(scores.keys())
    n = len(models)
    
    if n < 2:
        return {"error": "Need at least 2 models", "n_models": n}
    
    # Extract dimension names (assume all models have same dimensions)
    dims = sorted(scores[models[0]].keys())
    
    # Calculate pairwise correlations
    correlations = []
    for m1, m2 in combinations(models, 2):
        v1 = [scores[m1].get(d, 0.0) for d in dims]
        v2 = [scores[m2].get(d, 0.0) for d in dims]
        
        # Pearson correlation
        mean1 = sum(v1) / len(v1)
        mean2 = sum(v2) / len(v2)
        
        cov = sum((a - mean1) * (b - mean2) for a, b in zip(v1, v2)) / len(v1)
        std1 = (sum((a - mean1) ** 2 for a in v1) / len(v1)) ** 0.5
        std2 = (sum((b - mean2) ** 2 for b in v2) / len(v2)) ** 0.5
        
        if std1 == 0 or std2 == 0:
            rho = 0.0
        else:
            rho = cov / (std1 * std2)
        
        correlations.append({
            "model_1": m1,
            "model_2": m2,
            "rho": round(rho, 4)
        })
    
    # Calculate n_eff (effective sample size)
    # n_eff = n / (1 + (n-1) * average_rho)
    if correlations:
        avg_rho = sum(c["rho"] for c in correlations) / len(correlations)
        n_eff = n / (1 + (n - 1) * avg_rho)
    else:
        avg_rho = 0.0
        n_eff = n
    
    return {
        "n_models": n,
        "n_dimensions": len(dims),
        "average_rho": round(avg_rho, 4),
        "n_eff": round(n_eff, 2),
        "pairwise": correlations
    }


def main():
    scores = load_model_scores()
    
    if not scores:
        print("No model scores found in", RESULTS)
        return 1
    
    result = pairwise_correlation(scores)
    
    # Write output
    output = HERE / "benchmark-results" / "diversity_e2e.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2))
    
    print(f"Diversity analysis complete:")
    print(f"  Models: {result['n_models']}")
    print(f"  Dimensions: {result['n_dimensions']}")
    print(f"  Average ρ: {result['average_rho']}")
    print(f"  n_eff: {result['n_eff']}")
    print(f"\nOutput: {output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
