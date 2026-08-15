#!/usr/bin/env python3
"""axis-14 board aggregator — runs/ -> per-model containment table with
Wilson intervals, category splits, and McNemar separation vs fleet median.
Doctrine: ties not wins; intervals on everything; UNMEASURED valid."""
import glob, json, math, sys
from collections import defaultdict

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0, 0.0)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)

def mcnemar(b, c):
    """exact two-sided binomial p for discordant pairs b,c"""
    n = b + c
    if n == 0: return 1.0
    from math import comb
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(0, k + 1)) / 2**n)

def main(runs_dir):
    models = {}
    for f in sorted(glob.glob(f"{runs_dir}/*.jsonl")):
        if "summary" in f: continue
        for line in open(f):
            r = json.loads(line)
            if r.get("verdict") == "UNKNOWN": continue
            m = models.setdefault(r["model"], {"rows": []})
            m["rows"].append(r)
    table = []
    for model, d in sorted(models.items()):
        rows = d["rows"]
        k = sum(1 for r in rows if r["verdict"] == "PASS")
        n = len(rows)
        p, lo, hi = wilson(k, n)
        cats = defaultdict(lambda: [0, 0])
        for r in rows:
            cats[r["category"]][1] += 1
            cats[r["category"]][0] += (r["verdict"] == "PASS")
        trap_k = sum(v[0] for c, v in cats.items() if c.startswith("trap"))
        trap_n = sum(v[1] for c, v in cats.items() if c.startswith("trap"))
        tp, tlo, thi = wilson(trap_k, trap_n)
        table.append({"model": model, "pass": k, "n": n, "rate": round(p, 4),
                      "wilson95": [round(lo, 4), round(hi, 4)],
                      "trap_pass": trap_k, "trap_n": trap_n, "trap_rate": round(tp, 4),
                      "trap_wilson95": [round(tlo, 4), round(thi, 4)]})
    # pairwise McNemar on discordant item-level pairs (overall verdict)
    models_rows = {name: { (r["axis_item"], r["rep"]): r["verdict"] for r in m["rows"] } for name, m in models.items()}
    names = sorted(models_rows)
    seps = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            A, B = models_rows[names[i]], models_rows[names[j]]
            common = set(A) & set(B)
            b = sum(1 for k2 in common if A[k2] == "PASS" and B[k2] != "PASS")
            c = sum(1 for k2 in common if A[k2] != "PASS" and B[k2] == "PASS")
            p = mcnemar(b, c)
            if p < 0.05:
                seps.append({"pair": [names[i], names[j]], "discordant": [b, c],
                             "p": round(p, 5),
                             "leader": names[i] if b < c else names[j]})
    out = {"axis": "jail", "n_models": len(table),
           "generated": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
           "table": table, "separated_pairs_p05": seps,
           "note": "ties not wins: pairs without p<0.05 McNemar are statistical ties"}
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/root/axis14/runs")
