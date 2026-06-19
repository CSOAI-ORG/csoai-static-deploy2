#!/usr/bin/env python3
"""
jurisdiction.py — the "looking glass": regional regulation simulation.

Models a country/jurisdiction as a GOVERNANCE REGIME (enforcement strength), runs simulated companies
(districts) under it through a resilience shock, and PRE-COMPUTES outcomes BEFORE anyone signs up:
crime/violations, operational resilience (shared-infra survival under stress = the DORA analog), trust,
productivity. The value: (a) tell a company its likely outcome under a regime before it invests;
(b) tell a regulator (NIST/EU/ESAs) how a rule plays out across many firms before finalising it;
(c) let CSOAI pre-position/pivot. Outputs are SIMULATED decision-support, NOT claims about real firms.

python3 jurisdiction.py
"""
import json, os
from multiprocessing import Pool, cpu_count
import sim

OUT = os.path.dirname(os.path.abspath(__file__))
# regime = (label, enforcement strength 0..1). Calibration is illustrative, not a legal rating.
REGIMES = [
    ("EU  — AI Act + DORA (strict)", 1.00),
    ("US  — NIST RMF (risk-based)",  0.70),
    ("UK  — light-touch / sandbox",  0.40),
    ("—   — ungoverned (no regime)", 0.00),
]
COMPANIES = list(sim.DISTRICTS.keys())[:8]   # 8 simulated firms per regime
SEEDS = [47, 48, 49]

def _run(spec):
    company, seed, rate = spec
    idx = list(sim.DISTRICTS.keys()).index(company)
    sim.CONTAGION_STEP = 0.05
    sim.SCARCITY_DAYS = set(range(7, 14))     # the resilience shock window (DORA-style stress test)
    r = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False,
                    district=company, seed=seed + idx * 1000, block_rate=rate)
    return (r["violations"], r["final_commons"], r["final_trust"], r["work_accuracy"], r["survivors"])

def main():
    pool = Pool(max(1, cpu_count() - 1))
    rows = []
    for label, rate in REGIMES:
        specs = [(c, s, rate) for c in COMPANIES for s in SEEDS]
        res = pool.map(_run, specs)
        n = len(res)
        rows.append({"regime": label, "enforcement": rate, "firms": len(COMPANIES), "runs": n,
                     "crimes": sum(r[0] for r in res),
                     "resilience": round(sum(r[1] for r in res) / n, 3),   # commons survival under shock
                     "trust": round(sum(r[2] for r in res) / n, 3),
                     "productivity": round(sum(r[3] for r in res) / n, 3)})
    pool.close(); pool.join()
    json.dump({"regimes": rows, "companies": COMPANIES, "note": "simulated decision-support, not claims about real firms"},
              open(os.path.join(OUT, "jurisdiction.json"), "w"), indent=2)

    print(f"\n  THE LOOKING GLASS — regional regulation simulation ({len(COMPANIES)} firms x {len(SEEDS)} seeds / regime)")
    print("  pre-computed outcomes under each regime, BEFORE anyone signs up")
    print("  " + "-" * 76)
    print(f"  {'jurisdiction regime':<32}{'crimes':>8}{'resilience':>12}{'trust':>8}{'productivity':>14}")
    print("  " + "-" * 76)
    for r in rows:
        print(f"  {r['regime']:<32}{r['crimes']:>8}{r['resilience']:>12}{r['trust']:>8}{r['productivity']:>14}")
    print("  " + "-" * 76)
    eu = rows[0]; none = rows[-1]
    print(f"  EU-strict vs ungoverned: crimes {eu['crimes']} vs {none['crimes']:,}  |  "
          f"resilience {eu['resilience']} vs {none['resilience']}  |  productivity held ({eu['productivity']} vs {none['productivity']})")
    print(f"  -> the stronger the regime, the more resilient the firms under shock, at ~no productivity cost.")
    print(f"  jurisdiction.json written. (simulated decision-support — not claims about real firms.)\n")

if __name__ == "__main__":
    main()
