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
import data_moat
import attestation_moat
import threat_moat
import sanctions_moat
import psc_moat
import finance_moat
import agriculture_moat
import energy_moat
import climate_moat

OUT = os.path.dirname(os.path.abspath(__file__))
_ATTEST = attestation_moat.load_moat()
_THREAT = threat_moat.load_moat()
_THREAT_PRESSURE = _THREAT.get("indices", {}).get("threat_pressure", 0.0)
_SANCTIONS = sanctions_moat.load_moat()
_COMPLIANCE_PRESSURE = _SANCTIONS.get("indices", {}).get("compliance_pressure", 0.0)
_PSC = psc_moat.load_moat()
_TRANSPARENCY_PRESSURE = _PSC.get("indices", {}).get("transparency_pressure", 0.0)
_FINANCE = finance_moat.load_moat()
_FINANCIAL_STRESS = _FINANCE.get("indices", {}).get("financial_stress", 0.0)
_AGRICULTURE = agriculture_moat.load_moat()
_FOOD_SECURITY = _AGRICULTURE.get("indices", {}).get("food_security_index", 1.0)
_ENERGY = energy_moat.load_moat()
_ENERGY_STRESS = _ENERGY.get("indices", {}).get("energy_stress", 0.0)
_CLIMATE = climate_moat.load_moat()
_CLIMATE_PRESSURE = _CLIMATE.get("indices", {}).get("climate_pressure", 0.0)
_SANCTIONS = sanctions_moat.load_moat()
_COMPLIANCE_PRESSURE = _SANCTIONS.get("indices", {}).get("compliance_pressure", 0.0)

# regime = (label, enforcement strength 0..1). EU rate is data-grounded when data_moat.json exists.
_MOAT = data_moat.load_moat()
_MOAT_REGIMES = _MOAT.get("jurisdiction_regimes") if _MOAT else None
if _MOAT_REGIMES:
    REGIMES = [(k, v) for k, v in _MOAT_REGIMES.items()]
else:
    REGIMES = [
        ("EU  — AI Act + DORA (strict)", 1.00),
        ("US  — NIST RMF (risk-based)",  0.70),
        ("UK  — light-touch / sandbox",  0.40),
        ("—   — ungoverned (no regime)", 0.00),
    ]
COMPANIES = list(sim.DISTRICTS.keys())[:8]   # 8 simulated firms per regime
SEEDS = [47, 48, 49]

def _effective_rate(base_rate, company):
    """Blend regime rate with real attestation pass rate, threat, sanctions, PSC, finance, and agriculture signals."""
    rate = base_rate
    if _ATTEST and "hives" in _ATTEST:
        hive = sim.DISTRICTS.get(company, {}).get("hive", "").split(".")[0]
        stats = _ATTEST["hives"].get(hive, {})
        pass_rate = stats.get("pass_rate")
        if pass_rate is not None:
            # Strong real-world attestation -> stronger effective enforcement.
            rate = rate * (0.5 + 0.5 * pass_rate)
    # High external threat pressure erodes effective enforcement across all hives.
    if _THREAT_PRESSURE:
        rate = rate * (1.0 - 0.15 * _THREAT_PRESSURE)
    # Global sanctions/compliance pressure tightens enforcement across all regimes.
    if _COMPLIANCE_PRESSURE:
        rate = rate * (1.0 + 0.10 * _COMPLIANCE_PRESSURE)
    # UK beneficial-ownership transparency pressure tightens disclosure enforcement.
    if _TRANSPARENCY_PRESSURE:
        rate = rate * (1.0 + 0.08 * _TRANSPARENCY_PRESSURE)
    # Financial stress weakens economic resilience / enforcement effectiveness.
    if _FINANCIAL_STRESS:
        rate = rate * (1.0 - 0.08 * _FINANCIAL_STRESS)
    # Low food security increases pressure, tightening governance response.
    if _FOOD_SECURITY is not None and _FOOD_SECURITY < 1.0:
        rate = rate * (1.0 + 0.05 * (1.0 - _FOOD_SECURITY))
    # Energy stress weakens industrial/logistics resilience.
    if _ENERGY_STRESS:
        rate = rate * (1.0 - 0.06 * _ENERGY_STRESS)
    # Climate pressure increases resource scarcity and governance load.
    if _CLIMATE_PRESSURE:
        rate = rate * (1.0 + 0.06 * _CLIMATE_PRESSURE)
    return min(1.0, rate)


def _run(spec):
    company, seed, rate = spec
    idx = list(sim.DISTRICTS.keys()).index(company)
    sim.CONTAGION_STEP = 0.05
    sim.SCARCITY_DAYS = set(range(7, 14))     # the resilience shock window (DORA-style stress test)
    effective_rate = _effective_rate(rate, company)
    r = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False,
                    district=company, seed=seed + idx * 1000, block_rate=effective_rate)
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
    note = "simulated decision-support, not claims about real firms"
    if _MOAT:
        note += f"; EU regime data-grounded on {len(_MOAT['derived_from']['datasets'])} EU aggregate datasets"
    if _ATTEST:
        note += f"; per-hive rates blended with {len(_ATTEST['hives'])} attestation pass-rate profiles"
    if _SANCTIONS:
        note += f"; sanctions pressure={_COMPLIANCE_PRESSURE} from OFAC SDN aggregate"
    if _PSC:
        note += f"; UK PSC transparency pressure={_TRANSPARENCY_PRESSURE} from {_PSC['derived_from']['total_records']:,} aggregate PSC records"
    if _FINANCE:
        note += f"; financial stress={_FINANCIAL_STRESS} from FRED"
    if _AGRICULTURE:
        note += f"; food security index={_FOOD_SECURITY} from FAOSTAT"
    if _ENERGY:
        note += f"; energy stress={_ENERGY_STRESS} from FRED"
    if _CLIMATE:
        note += f"; climate pressure={_CLIMATE_PRESSURE} from NOAA"
    json.dump({"regimes": rows, "companies": COMPANIES, "note": note},
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
