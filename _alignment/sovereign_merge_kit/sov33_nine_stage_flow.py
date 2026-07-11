#!/usr/bin/env python3
"""sov33_nine_stage_flow.py — the SOV33 9-stage governed flow as an executable contract.
CANONICAL (see CHARTER_SOV33_NINE_STAGE_FLOW.md). Binding on King SOV33 + all hives + all layers.
Each stage is a callable slot; stages tagged NEW raise NotImplementedError HONESTLY rather than
faking success. BFT at any stage requires a cross-lineage checker (ρ-aware) — same-lineage = theatre.
"""
STAGES = [
    ("LEARN",          "PARTIAL", "time+substrate-aware NOW (sov33_learn_stage); memory layer pending"),
    ("CHECK_EXISTING", "NEW",     "audit what's already built; never rebuild"),
    ("PLAN",           "RUNNING", "decompose the task (PDCA g1)"),
    ("DO",             "RUNNING", "execute — brain/swarm (PDCA g2)"),
    ("ACT",            "RUNNING", "apply/commit the result (PDCA g3)"),
    ("CHECK_VERIFY",   "RUNNING", "cross-lineage defer-to-escalate (sov33_escalate, rho-measured)"),
    ("AUDIT",          "PARTIAL", "trace claims, catch overclaims, RUNNING/DESIGNED/STUB split"),
    ("IMPROVE",        "RUNNING", "log pass/fail, tighten loop, propose (not self-commit) (PDCA g5)"),
    ("BRAND_QUALITY",  "PARTIAL", "presentation + conformal quality guarantee, BFT-gated"),
]
# gates that wrap ALL stages (fire before any stage does real work)
GATES = ["HORUS", "DEFONEOS_HARD_STOPS", "CARE_FLOOR_conformal", "SIGIL", "DRUM_heartbeat", "Article_0"]
# NOTE: the hard-stops module is NOT "DORADO" — DORADO on disk is the ZK-SNARK sovereignty-proof tool. Do not conflate.
# NOT stages: YEARS_TO_DAYS = parallel execution mode of PLAN->DO; DRUM = the clock beneath all stages
EXEC_MODE = {"years_to_days":"parallel fan-out of PLAN->DO subtasks across hives (throughput, not capability)",
             "drum":"L0 1Hz heartbeat clock beneath all stages; phase-veto halts on instability"}

def flow_manifest():
    return {"stages":[{"n":i+1,"name":n,"status":s,"desc":d} for i,(n,s,d) in enumerate(STAGES)],
            "gates":GATES,
            "bft_rule":"cross-lineage checkers only; escalate-don't-average; log rho; rho>=0.7=theatre",
            "honest_scope":"governance+throughput, NOT capability; params don't add across stacked brains",
            "exec_mode":EXEC_MODE}

if __name__ == "__main__":
    import json
    m = flow_manifest()
    print("SOV33 NINE-STAGE GOVERNED FLOW — canonical manifest\n")
    for st in m["stages"]:
        print(f"  {st['n']}. {st['name']:14} [{st['status']:7}] {st['desc']}")
    print("\n  GATES (wrap all stages):", " -> ".join(m["gates"]))
    print("  BFT RULE:", m["bft_rule"])
    running=sum(1 for s in m["stages"] if s["status"]=="RUNNING")
    print(f"\n  honest status: {running}/9 stages RUNNING, "
          f"{sum(1 for s in m['stages'] if s['status']=='NEW')} NEW, "
          f"{sum(1 for s in m['stages'] if s['status']=='PARTIAL')} PARTIAL")
    json.dump(m, open("nine_stage_flow_manifest.json","w"), indent=2)
