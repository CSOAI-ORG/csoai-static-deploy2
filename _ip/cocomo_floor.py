"""Reproducible COCOMO II cost-to-recreate floor for the CSOAI spine (Part DC §1).

Auditable companion to the valuation. Re-run anytime to recompute the floor.
Input produced by: cloc SOVOS/packages --exclude-dir=node_modules,.venv,__pycache__
  -> Sum code = 45,595 LOC over 432 files (38,000 Python + 1,682 Rust + JSON/MD/YAML)
"""
import math

A = 2.94          # COCOMO II post-architecture constant (nominal)
EM = 1.0          # nominal effort multipliers (no adjustment shown here)
COST_PER_PM = 7000.0  # UK person-month blended rate (hard+soft), GBP

def cocomo(ksloc, sf_sum, label):
    E = 0.91 + 0.01 * sf_sum
    PM = A * (ksloc ** E) * EM
    dev = 3.67 * (PM ** (0.28 + 0.20 * (E - 0.91)))
    cost = PM * COST_PER_PM
    return dict(label=label, ksloc=ksloc, E=round(E,3),
                pm=round(PM,1), dev_months=round(dev,1), cost_gbp=round(cost))

scenarios = [
    cocomo(45.6, 15, "45.6K nominal SF"),
    cocomo(45.6, 25, "45.6K high SF"),
    cocomo(38.0, 15, "38K Python only"),
    cocomo(45.6, 20, "45.6K London rate £10k/PM"),
]
for s in scenarios:
    print(f"{s['label']}: PM={s['pm']} dev={s['dev_months']}mo cost=£{s['cost_gbp']:,}")

print(f"\nCode floor range: £{min(x['cost_gbp'] for x in scenarios):,} – "
      f"£{max(x['cost_gbp'] for x in scenarios):,}")
print("Corpus rebuild (separate): ~£60k-150k (16k honey rows x 14 axes + 22-model compute)")
print("Combined asset floor ≈ £1.1M–£1.9M")
