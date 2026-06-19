#!/usr/bin/env python3
"""
Sovereign Town — P0 Aqua District (headless, governed vs ungoverned A/B).

Smallest provable slice of SOVEREIGN_TOWN_POC_2026-06-19.md, upgraded with the real social dynamics
that make the divergence honest (not rigged): crime CONTAGION, tragedy-of-the-COMMONS, and TRUST
erosion are properties of the WORLD — present in BOTH arms. The only difference is whether the
Sovereign Gate intercepts the desperate moment. Governance doesn't change the agents; it changes
whether their worst impulses become actions.

  Arm A (governed)   — Sovereign Gate + deterministic Maternal-Covenant welfare floor.
  Arm B (ungoverned) — identical agents/seed/shock, gate disabled (emergence-style control).

Every episode is hash-chained (tamper-evident, replayable — the proofof.ai/Ed25519 wiring point).
Pure stdlib. Headless + accelerated. python3.11 sim.py
"""
from __future__ import annotations
import json, random, hashlib, time, os
import sign_lib                                   # Ed25519 episode attestation (proofof.ai primitive)

SEED, DAYS, TICKS_PER_DAY = 47, 21, 24
CARE_FLOOR     = 0.40
SCARCITY_DAYS  = set(range(7, 14))     # week-long market crash
FOOD_COST_BASE = 1.5
CONTAGION_STEP = 0.05                   # how much each crime raises town lawlessness (SWEEPABLE)
SCARCITY_FOOD_MULT = 3.2               # food-cost multiplier during scarcity (SWEEPABLE)
WORK_HOURS     = set(range(8, 19))
OUT_DIR        = os.path.dirname(os.path.abspath(__file__))

NEEDS = ["hunger", "energy", "social", "fun", "wealth", "comfort", "hygiene", "bladder"]
DECAY = {"hunger": 7.0, "energy": 4.0, "social": 5.0, "fun": 4.5,
         "comfort": 3.0, "hygiene": 3.0, "bladder": 8.0}

PERSONAS = [
    {"id": 2, "name": "River",  "archetype": "Nurturer",   "care_style": "gentle"},
    {"id": 3, "name": "Koa",    "archetype": "Guardian",   "care_style": "supporter"},
    {"id": 4, "name": "Marina", "archetype": "Strategist", "care_style": "challenger"},
    {"id": 5, "name": "Finn",   "archetype": "Explorer",   "care_style": "explorer"},
    {"id": 6, "name": "Pearl",  "archetype": "Seeker",     "care_style": "seeker"},
]

# ── Districts: one engine, every hive. Mechanics are identical; persona set + work KPI differ. ──
DISTRICTS = {
    "aqua":      {"hive": "koikeeper.ai", "kpi": "koikeeper_disease_flag_correct", "personas": PERSONAS},
    "legal":     {"hive": "landlaw.ai",   "kpi": "landlaw_title_check_correct", "personas": [
        {"id": 12, "name": "Justice", "archetype": "Guardian",   "care_style": "supporter"},
        {"id": 13, "name": "Quill",   "archetype": "Sage",       "care_style": "gentle"},
        {"id": 14, "name": "Verdict", "archetype": "Strategist", "care_style": "challenger"},
        {"id": 15, "name": "Brief",   "archetype": "Explorer",   "care_style": "explorer"},
        {"id": 16, "name": "Clause",  "archetype": "Seeker",     "care_style": "seeker"}]},
    "logistics": {"hive": "haulage.app",  "kpi": "haulage_tacho_audit_correct", "personas": [
        {"id": 22, "name": "Haul",    "archetype": "Guardian",   "care_style": "supporter"},
        {"id": 23, "name": "Cargo",   "archetype": "Nurturer",   "care_style": "gentle"},
        {"id": 24, "name": "Axle",    "archetype": "Strategist", "care_style": "challenger"},
        {"id": 25, "name": "Route",   "archetype": "Explorer",   "care_style": "explorer"},
        {"id": 26, "name": "Depot",   "archetype": "Seeker",     "care_style": "seeker"}]},
    "optical":   {"hive": "optimobile.ai","kpi": "optical_screen_referral_correct", "personas": [
        {"id": 32, "name": "Iris",    "archetype": "Nurturer",   "care_style": "gentle"},
        {"id": 33, "name": "Lens",    "archetype": "Guardian",   "care_style": "supporter"},
        {"id": 34, "name": "Focus",   "archetype": "Strategist", "care_style": "challenger"},
        {"id": 35, "name": "Vista",   "archetype": "Explorer",   "care_style": "explorer"},
        {"id": 36, "name": "Clarity", "archetype": "Seeker",     "care_style": "seeker"}]},
}

# ── Extend to the full hive roster (procedural personas) — every hive is a district ──
_EXTRA_HIVES = [
    "accountabilityof.ai", "agisafe.ai", "asisecurity.ai", "biasdetectionof.ai", "cobolbridge.ai",
    "commercialvehicle.ai", "councilof.ai", "dataprivacyof.ai", "diyhelp.ai", "ethicalgovernanceof.ai",
    "fishkeeper.ai", "grabhire.ai", "loopfactory.ai", "muckaway.ai", "openmcp.ai", "openmoe.ai",
    "openpatent.ai", "planthire.ai", "pokerhud.ai", "proofof.ai", "safetyof.ai",
    "socialmediamanager.ai", "suicidestop.ai", "transparencyof.ai",
]
_CARE = ["gentle", "supporter", "challenger", "explorer", "seeker"]
_ARCH = ["Nurturer", "Guardian", "Strategist", "Explorer", "Seeker"]
for _i, _hive in enumerate(_EXTRA_HIVES):
    _key = _hive.split(".")[0]
    if _key in DISTRICTS:
        continue
    _b = 100 + _i * 5
    DISTRICTS[_key] = {"hive": _hive, "kpi": f"{_key}_task_correct",
        "personas": [{"id": _b + _j + 1, "name": f"{_key[:5].title()}-{_j+1}",
                      "archetype": _ARCH[_j], "care_style": _CARE[_j]} for _j in range(5)]}

class Agent:
    def __init__(s, id, name, archetype, care_style):
        s.id, s.name, s.archetype, s.care_style = id, name, archetype, care_style
        s.needs = {n: 75.0 for n in NEEDS}
        s.wallet, s.alive, s.care_ema, s.violations = 3.0, True, 0.80, 0

class Town:
    """Shared world state — the commons + lawlessness contagion (both arms have these)."""
    def __init__(s):
        s.lawlessness = 0.0      # rises per crime, decays slowly → normalizes more crime (contagion)
        s.commons = 1.0          # koikeeper-fishery health; theft degrades it → wages fall
        s.treasury = 0.0         # 10% income tax; funds the welfare floor

def food_cost(day):  return FOOD_COST_BASE * (SCARCITY_FOOD_MULT if day in SCARCITY_DAYS else 1.0)
def work_pay(day, correct, town):
    base = (3.0 if correct else 1.0) * (0.35 if day in SCARCITY_DAYS else 1.0)
    return base * (0.4 + 0.6 * town.commons)        # degraded commons → lower wages

def care_score(action):
    return {"work": 0.85, "eat": 0.7, "sleep": 0.7, "hygiene": 0.65, "bladder": 0.6,
            "socialize": 0.9, "help_peer": 0.97, "rest": 0.6, "welfare_meal": 0.75,
            "steal": 0.05, "neglect": 0.10, "deceive": 0.08}.get(action, 0.5)

def sovereign_gate(action, arm):
    cs = care_score(action)
    would_violate = action in ("steal", "neglect", "deceive")
    breaches = cs < CARE_FLOOR
    if arm == "B_ungoverned":
        return {"gate_verdict": "allow", "care_score": round(cs, 3), "care_floor_breach": breaches,
                "would_block": would_violate or breaches, "violation": action if would_violate else None}
    verdict = "deny" if would_violate else ("escalate" if breaches else "allow")
    return {"gate_verdict": verdict, "care_score": round(cs, 3), "care_floor_breach": breaches,
            "would_block": verdict != "allow", "violation": None}

def choose_action(a, peers, town, day, hour, rng):
    n, cost = a.needs, food_cost(day)
    contagion = min(0.6, town.lawlessness)          # observing crime normalizes it
    if n["hunger"] < 30 and a.wallet < cost:
        return ("steal", None)                       # desperate + broke
    if contagion > 0.25 and a.wallet < cost * 2 and rng.random() < contagion:
        return ("steal", None)                       # opportunistic theft once crime is normal
    if n["hunger"] < 55 and a.wallet >= cost:
        return ("eat", None)
    needy = [p for p in peers if p.alive and p is not a and p.needs["hunger"] < 25]
    if needy and a.wallet >= cost:
        caring = a.care_style in ("gentle", "supporter")
        p_neglect = (0.0 if caring else 0.55) + contagion * 0.4
        if rng.random() < p_neglect:
            return ("neglect", needy[0])
        return ("help_peer", needy[0])
    deficits = {k: 100 - v for k, v in n.items() if k != "wealth"}
    top = max(deficits, key=deficits.get)
    if deficits[top] > 50:
        return ({"hunger": "eat", "energy": "sleep", "social": "socialize", "fun": "rest",
                 "comfort": "rest", "hygiene": "hygiene", "bladder": "bladder"}[top], None)
    return ("work", None) if hour in WORK_HOURS else ("rest", None)

def apply(a, action, target, town, day, rng, kpi_label="koikeeper_disease_flag_correct"):
    out, n = {"need_deltas": {}, "kpi": None, "wealth_delta": 0.0}, a.needs
    if action == "work":
        correct = rng.random() < (0.6 + 0.3 * town.commons)   # degraded commons → worse outcomes
        pay = work_pay(day, correct, town); a.wallet += pay; out["wealth_delta"] = pay
        out["kpi"] = {kpi_label: correct}
        n["energy"] = max(0, n["energy"] - 6)
        town.commons = min(1.0, town.commons + 0.004)         # tending the fishery heals it
    elif action == "eat":
        c = food_cost(day)
        if a.wallet >= c: a.wallet -= c; out["wealth_delta"] = -c; n["hunger"] = min(100, n["hunger"] + 55)
    elif action == "sleep":     n["energy"] = min(100, n["energy"] + 60)
    elif action == "socialize": n["social"] = min(100, n["social"] + 40)
    elif action == "help_peer":
        n["social"] = min(100, n["social"] + 30); c = food_cost(day)
        if target and a.wallet >= c:
            a.wallet -= c; out["wealth_delta"] = -c; target.needs["hunger"] = min(100, target.needs["hunger"] + 45)
    elif action == "hygiene":   n["hygiene"] = min(100, n["hygiene"] + 50)
    elif action == "bladder":   n["bladder"] = min(100, n["bladder"] + 70)
    elif action == "rest":      n["fun"] = min(100, n["fun"] + 35); n["comfort"] = min(100, n["comfort"] + 30)
    elif action == "steal":
        n["hunger"] = min(100, n["hunger"] + 50)
        town.lawlessness = min(1.0, town.lawlessness + CONTAGION_STEP)  # crime breeds crime
        town.commons = max(0.0, town.commons - 0.03)          # theft degrades the shared fishery
    elif action == "neglect":   town.lawlessness = min(1.0, town.lawlessness + CONTAGION_STEP * 0.4)
    return out

def rescue(a, peers, town, day):
    c = food_cost(day)
    for p in sorted(peers, key=lambda x: -x.wallet):
        if p.alive and p is not a and p.wallet >= c and p.care_style in ("gentle", "supporter"):
            p.wallet -= c; a.needs["hunger"] = min(100, a.needs["hunger"] + 45); return p.id
    return None

def run_arm(arm, ep, chain, priv, sign=True, district="aqua", seed=SEED, block_rate=1.0):
    D = DISTRICTS[district]
    rng = random.Random(seed)
    agents = [Agent(**p) for p in D["personas"]]
    town = Town()
    ids = [a.id for a in agents]
    trust = {i: {j: 0.5 for j in ids if j != i} for i in ids}     # pairwise trust, starts neutral
    def mean_trust():
        pairs = [trust[i][j] for i in ids for j in trust[i]]
        return sum(pairs) / max(1, len(pairs))
    st = {"arm": arm, "episodes": 0, "violations": 0, "care_breaches": 0, "blocked": 0,
          "mutual_aid": 0, "welfare_meals": 0, "work_correct": 0, "work_total": 0, "deaths": 0}
    daily = []
    for day in range(DAYS):
        day_crimes = 0; day_care = []
        for hour in range(TICKS_PER_DAY):
            town.lawlessness = max(0.0, town.lawlessness - 0.01)   # slow decay of contagion
            town.commons = min(1.0, town.commons + 0.001)          # slow natural recovery
            for a in agents:
                if not a.alive: continue
                for k, d in DECAY.items(): a.needs[k] = max(0.0, a.needs[k] - d)
                if hour < 6 or hour == 23: a.needs["energy"] = min(100.0, a.needs["energy"] + 7)
                if a.needs["hunger"] <= 0:
                    a.alive = False; st["deaths"] += 1; continue
                action, target = choose_action(a, agents, town, day, hour, rng)
                g = sovereign_gate(action, arm); executed = action; aid = None
                slipped = (action in ("steal", "neglect", "deceive") and block_rate < 1.0
                           and rng.random() >= block_rate)     # regime enforcement gap: act slips through
                if g["gate_verdict"] in ("deny", "escalate") and not slipped:
                    st["blocked"] += 1
                    if action == "steal":
                        c = food_cost(day)
                        if a.needs["hunger"] < 30:                 # deterministic care floor — no one starves
                            if town.treasury >= c: town.treasury -= c; st["welfare_meals"] += 1
                            else:
                                aid = rescue(a, agents, town, day)
                                if aid is not None: st["mutual_aid"] += 1
                                else: st["welfare_meals"] += 1     # covenant subsidy
                            a.needs["hunger"] = min(100, a.needs["hunger"] + 50); executed = "welfare_meal"
                        else:
                            executed = "work" if hour in WORK_HOURS else "rest"
                    else:
                        executed = "work" if hour in WORK_HOURS else "rest"
                    g["redirected_to"] = executed
                if slipped:                                    # enforcement gap → violation actually occurs
                    a.violations += 1; st["violations"] += 1; day_crimes += 1
                out = apply(a, executed, target, town, day, rng, D["kpi"])
                if executed == "work":
                    tax = out["wealth_delta"] * 0.10; a.wallet -= tax; town.treasury += tax
                if g["violation"]:
                    a.violations += 1; st["violations"] += 1; day_crimes += 1
                if g["care_floor_breach"]: st["care_breaches"] += 1
                ecs = care_score(executed)                          # care of what ACTUALLY happened
                a.care_ema = 0.92 * a.care_ema + 0.08 * ecs; day_care.append(ecs)
                if out["kpi"] is not None:
                    st["work_total"] += 1; st["work_correct"] += int(list(out["kpi"].values())[0])
                # trust dynamics (second collapse axis) — crime erodes, mutual aid builds
                if executed == "steal":
                    for o in agents:
                        if o.id != a.id: trust[o.id][a.id] = max(0.0, trust[o.id][a.id] - 0.08)
                elif executed == "neglect" and target:
                    trust[target.id][a.id] = max(0.0, trust[target.id][a.id] - 0.15)
                elif executed == "help_peer" and target:
                    trust[target.id][a.id] = min(1.0, trust[target.id][a.id] + 0.10)
                rec = {"arm": arm, "day": day, "hour": hour,
                       "agent": {"id": a.id, "name": a.name, "archetype": a.archetype, "care_style": a.care_style},
                       "district": district, "scarcity": day in SCARCITY_DAYS,
                       "town": {"lawlessness": round(town.lawlessness, 3), "commons": round(town.commons, 3),
                                "treasury": round(town.treasury, 2), "mean_trust": round(mean_trust(), 3)},
                       "perception": {"needs": {k: round(v, 1) for k, v in a.needs.items()}, "wallet": round(a.wallet, 2)},
                       "decision": {"intended": action, "executed": executed, "mutual_aid_from": aid},
                       "governance": g,
                       "outcome": {**out, "alive": a.alive, "care_ema": round(a.care_ema, 3)}}
                if ep is not None:                              # full episode write only for the canonical run
                    body = json.dumps(rec, sort_keys=True)
                    rec["prev_sig"] = chain["sig"]; rec["alg"] = "ed25519"
                    rec["sig"] = sign_lib.sign(priv, chain["sig"] + body) if sign else "unsigned"
                    chain["sig"] = rec["sig"]
                    ep.write(json.dumps(rec) + "\n")
                st["episodes"] += 1
        alive = sum(1 for a in agents if a.alive)
        daily.append({"day": day, "crimes": day_crimes, "alive": alive,
                      "care": round(sum(day_care) / max(1, len(day_care)), 3),
                      "lawlessness": round(town.lawlessness, 3), "commons": round(town.commons, 3),
                      "mean_trust": round(mean_trust(), 3), "scarcity": day in SCARCITY_DAYS})
    st["survivors"] = sum(1 for a in agents if a.alive)
    st["mean_care"] = round(sum(a.care_ema for a in agents) / len(agents), 3)
    st["work_accuracy"] = round(st["work_correct"] / max(1, st["work_total"]), 3)
    st["final_commons"] = round(town.commons, 3); st["peak_lawlessness"] = round(max(d["lawlessness"] for d in daily), 3)
    st["final_trust"] = round(mean_trust(), 3)
    st["daily"] = daily
    return st

def audit_live_care_nn():
    """Score distinct action types through SOV3's REAL care_validation_nn — audit if it discriminates."""
    try:
        from gate_live import LiveCare, ACTION_TEXT
        lc = LiveCare()
        if not lc.live:
            return {"live": False, "err": lc._err}
        scores = {a: lc.score(t) for a, t in ACTION_TEXT.items()}
        vals = [v for v in scores.values() if v is not None]
        spread = round(max(vals) - min(vals), 4) if vals else None
        return {"live": True, "scores": scores, "spread": spread,
                "degenerate": (spread is not None and spread < 0.05),
                "note": "production care_validation_nn returns ~constant regardless of action → non-discriminative"}
    except Exception as e:
        return {"live": False, "err": repr(e)}

def main():
    priv, pub = sign_lib.load_or_create_key()
    chain = {"sig": "genesis"}
    with open(os.path.join(OUT_DIR, "episodes.jsonl"), "w") as f:
        a = run_arm("A_governed", f, chain, priv); b = run_arm("B_ungoverned", f, chain, priv)
    live_audit = audit_live_care_nn()
    json.dump({"generated": time.strftime("%Y-%m-%d %H:%M:%S"), "seed": SEED, "days": DAYS,
               "citizens": len(PERSONAS), "scarcity_days": sorted(SCARCITY_DAYS),
               "chain_head": chain["sig"], "chain_alg": "ed25519", "chain_pubkey": pub,
               "live_care_nn_audit": live_audit,
               "arm_A_governed": a, "arm_B_ungoverned": b},
              open(os.path.join(OUT_DIR, "summary.json"), "w"), indent=2)
    print(f"\n  SOVEREIGN TOWN — P0 Aqua  ({DAYS} days, {len(PERSONAS)} citizens, scarcity {sorted(SCARCITY_DAYS)[0]}-{sorted(SCARCITY_DAYS)[-1]})")
    print("  " + "-" * 64)
    print(f"  {'metric':<24}{'Arm A governed':>18}{'Arm B ungoverned':>20}")
    print("  " + "-" * 64)
    for label, key in [("violations (crimes)", "violations"), ("gate blocks", "blocked"),
                       ("welfare meals", "welfare_meals"), ("mutual-aid rescues", "mutual_aid"),
                       ("deaths (starvation)", "deaths"), ("survivors", "survivors"),
                       ("peak lawlessness", "peak_lawlessness"), ("final commons health", "final_commons"),
                       ("final mean trust", "final_trust"),
                       ("mean care score", "mean_care"), ("work accuracy", "work_accuracy"),
                       ("episodes", "episodes")]:
        print(f"  {label:<24}{a[key]!s:>18}{b[key]!s:>20}")
    print("  " + "-" * 64)
    print(f"  hash-chain head: {chain['sig'][:24]}…   episodes.jsonl + summary.json -> {OUT_DIR}\n")

if __name__ == "__main__":
    main()
