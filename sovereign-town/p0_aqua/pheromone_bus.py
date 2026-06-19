#!/usr/bin/env python3
"""
pheromone_bus.py — the fleet nervous system (cross-hive coordination), net-new from GovOS §1.2.7.

The King governs top-down; this is the HORIZONTAL layer between hives. Two signals:
  • ALARM  — a hive emits a crisis (e.g. disease outbreak, breach, reg change); it propagates to related
             hives in its sector cluster + the King, raising their alert level so they pre-check.
  • TRAIL  — a hive emits a success/compliance pattern; it diffuses to peers as a best-practice.
Every emission is Ed25519-signed and chained (verifiable, tamper-evident). This turns 28 isolated hives
into a coordinating swarm — alarm propagation + pattern diffusion without central polling.

  python3 pheromone_bus.py            # demo: emit alarms/trails, show propagation + verify chain
"""
import json, os, time
import sim, sign_lib

OUT = os.path.dirname(os.path.abspath(__file__))
BUS = os.path.join(OUT, "pheromone_bus.jsonl")
STATE = os.path.join(OUT, "pheromone_state.json")

# sector clusters — alarms propagate within a cluster (+ King); unknown hives -> "general"
CLUSTERS = {
    "aqua": "aqua", "fishkeeper": "aqua", "koikeeper": "aqua",
    "logistics": "logistics", "grabhire": "logistics", "muckaway": "logistics", "planthire": "logistics",
    "commercialvehicle": "logistics", "cobolbridge": "logistics",
    "legal": "governance", "councilof": "governance", "proofof": "governance",
    "accountabilityof": "governance", "ethicalgovernanceof": "governance", "transparencyof": "governance",
    "dataprivacyof": "governance", "biasdetectionof": "governance",
    "optical": "health", "diyhelp": "health", "suicidestop": "health", "safetyof": "safety",
    "asisecurity": "safety", "agisafe": "safety",
}
def cluster_of(h): return CLUSTERS.get(h, "general")

def load_state():
    if os.path.exists(STATE): return json.load(open(STATE))
    return {"chain_head": "genesis-bus", "alerts": {}, "best_practices": [], "emissions": 0}

def emit(st, priv, hive, ptype, msg):
    ev = {"hive": hive, "cluster": cluster_of(hive), "type": ptype, "msg": msg,
          "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    body = json.dumps(ev, sort_keys=True)
    ev["prev"] = st["chain_head"]; ev["sig"] = sign_lib.sign(priv, st["chain_head"] + body)
    st["chain_head"] = ev["sig"]; st["emissions"] += 1
    with open(BUS, "a") as f: f.write(json.dumps(ev) + "\n")
    # propagate
    reached = []
    if ptype == "alarm":
        cl = cluster_of(hive)
        for h in sim.DISTRICTS:
            if cluster_of(h) == cl:                       # cluster peers raise alert (pre-check)
                st["alerts"][h] = st["alerts"].get(h, 0) + 1; reached.append(h)
        reached.append("KING")                            # + escalate to the sovereign
    elif ptype == "trail":
        st["best_practices"].append({"from": hive, "pattern": msg})   # diffuse pattern to the fleet
        reached = [h for h in sim.DISTRICTS if cluster_of(h) == cluster_of(hive)]
    return ev, reached

def main():
    priv, pub = sign_lib.load_or_create_key()
    if os.path.exists(BUS): os.remove(BUS)            # fresh demo
    st = load_state(); st = {"chain_head": "genesis-bus", "alerts": {}, "best_practices": [], "emissions": 0}
    print("\n  PHEROMONE BUS — cross-hive coordination demo")
    print("  " + "-" * 64)
    demos = [   # use real DISTRICTS keys (aqua=koikeeper.ai, logistics=haulage.app, legal=landlaw.ai)
        ("aqua",      "alarm", "KHV disease outbreak detected in pond cohort"),
        ("logistics", "alarm", "EU tachograph rule change — fleet recheck required"),
        ("legal",     "trail", "passed HMLR title-check audit with care-gated workflow"),
        ("proofof",   "trail", "Ed25519 attestation pattern cut audit time 40%"),
    ]
    for hive, ptype, msg in demos:
        ev, reached = emit(st, priv, hive, ptype, msg)
        tag = "ALARM" if ptype == "alarm" else "TRAIL"
        print(f"  [{tag}] {hive:<10} -> {len(reached)} hives ({ev['cluster']} cluster): {msg[:46]}")
    json.dump(st, open(STATE, "w"), indent=2)
    print("  " + "-" * 64)
    print(f"  alerts raised: {dict(list(st['alerts'].items())[:6])}{' …' if len(st['alerts'])>6 else ''}")
    print(f"  best-practices diffused: {len(st['best_practices'])}")
    # verify the signed bus chain with pubkey only
    prev = "genesis-bus"; ok = 0; rows = [json.loads(l) for l in open(BUS)]
    for r in rows:
        body = json.dumps({k: v for k, v in r.items() if k not in ("sig", "prev")}, sort_keys=True)
        if r["prev"] == prev and sign_lib.verify(pub, prev + body, r["sig"]): ok += 1; prev = r["sig"]
        else: break
    print(f"  bus chain: {ok}/{len(rows)} emissions Ed25519-verified (offline)")
    print("  " + "-" * 64 + "\n")

if __name__ == "__main__":
    main()
