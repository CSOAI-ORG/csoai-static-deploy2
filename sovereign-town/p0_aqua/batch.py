#!/usr/bin/env python3
"""
P1 batch harness — flood every CPU core with governed-vs-ungoverned runs across all hive-districts.

The sim mechanics are CPU-bound and embarrassingly parallel: every (district × seed × contagion) cell
is an independent run. This is the data-moat engine — it produces the cross-hive corpus of
self-labelled governed-behaviour episodes that the per-hive sovereign models train on.

Scales from a laptop (multiprocessing.Pool) to N free workers (each runs a job slice — see worker.py).
python3.11 batch.py [n_seeds]
"""
import json, os, sys, time
from multiprocessing import Pool, cpu_count
import sim

OUT = os.path.dirname(os.path.abspath(__file__))
DISTRICTS = list(sim.DISTRICTS.keys())
N_SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 8
CONTAGION = [0.0, 0.05, 0.10]
SEEDS = [47 + i for i in range(N_SEEDS)]

# per-hive profiles — distinct scarcity seasons + seed offsets → genuinely diverse corpora (not clones).
# Every district (all 28) gets a unique window+offset derived from its index, so none are clones.
def profile_for(district):
    idx = list(sim.DISTRICTS.keys()).index(district)
    start = 3 + (idx % 9)                      # scarcity start rotates 3..11
    length = 4 + (idx % 5)                     # window length rotates 4..8
    return {"scarcity": range(start, start + length), "off": (idx + 1) * 1000}

def job(spec):
    """One independent cell: run BOTH arms headless, return stats (no file IO in workers)."""
    district, seed, contagion = spec
    p = profile_for(district)
    sim.CONTAGION_STEP = contagion
    sim.SCARCITY_DAYS = set(p["scarcity"])                    # distinct economic season per hive
    seed = seed + p["off"]                                    # distinct stochastic trajectory per hive
    a = sim.run_arm("A_governed",   None, {"sig": ""}, None, sign=False, district=district, seed=seed)
    b = sim.run_arm("B_ungoverned", None, {"sig": ""}, None, sign=False, district=district, seed=seed)
    eps = a["episodes"] + b["episodes"]
    return {"district": district, "seed": seed, "contagion": contagion,
            "A_crimes": a["violations"], "A_trust": a["final_trust"], "A_commons": a["final_commons"],
            "B_crimes": b["violations"], "B_trust": b["final_trust"], "B_commons": b["final_commons"],
            "episodes": eps}

def main():
    specs = [(d, s, c) for d in DISTRICTS for s in SEEDS for c in CONTAGION]
    t0 = time.time()
    with Pool(max(1, cpu_count() - 1)) as pool:
        results = pool.map(job, specs)
    dt = time.time() - t0

    total_eps = sum(r["episodes"] for r in results)
    # per-district moat aggregation
    moat = {}
    for d in DISTRICTS:
        rs = [r for r in results if r["district"] == d]
        moat[d] = {
            "hive": sim.DISTRICTS[d]["hive"], "runs": len(rs), "episodes": sum(r["episodes"] for r in rs),
            "A_crimes_total": sum(r["A_crimes"] for r in rs), "B_crimes_total": sum(r["B_crimes"] for r in rs),
            "A_mean_trust": round(sum(r["A_trust"] for r in rs) / len(rs), 3),
            "B_mean_trust": round(sum(r["B_trust"] for r in rs) / len(rs), 3)}
    json.dump({"generated": time.strftime("%Y-%m-%d %H:%M:%S"), "cores": cpu_count(),
               "districts": DISTRICTS, "seeds": SEEDS, "contagion_grid": CONTAGION,
               "runs": len(results) * 2, "total_episodes": total_eps, "wall_seconds": round(dt, 1),
               "moat": moat, "results": results},
              open(os.path.join(OUT, "batch_corpus.json"), "w"), indent=2)

    print(f"\n  P1 BATCH — data-moat engine")
    print("  " + "-" * 64)
    print(f"  cells: {len(specs)}  ·  arm-runs: {len(results)*2}  ·  episodes: {total_eps:,}")
    print(f"  cores: {cpu_count()}  ·  wall: {dt:.1f}s  ·  throughput: {int(total_eps/max(dt,0.1)):,} episodes/s")
    print("  " + "-" * 64)
    print(f"  {'district':<11}{'hive':<16}{'episodes':>9}{'A crimes':>9}{'B crimes':>9}{'A trust':>8}{'B trust':>8}")
    for d in DISTRICTS:
        m = moat[d]
        print(f"  {d:<11}{m['hive']:<16}{m['episodes']:>9,}{m['A_crimes_total']:>9}{m['B_crimes_total']:>9}"
              f"{m['A_mean_trust']:>8}{m['B_mean_trust']:>8}")
    print("  " + "-" * 64)
    a_tot = sum(r["A_crimes"] for r in results); b_tot = sum(r["B_crimes"] for r in results)
    print(f"  ALL HIVES — governed crimes: {a_tot}   ungoverned crimes: {b_tot:,}")
    print(f"  corpus → batch_corpus.json  ({total_eps:,} labelled episodes for per-hive model training)\n")

if __name__ == "__main__":
    main()
