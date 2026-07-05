#!/usr/bin/env python3
"""
Dorado data-sovereignty adversary scenario for the Sovereign governance gym.
Mirrors sovereign-town/p0_aqua/sim.py's two-arm (governed vs ungoverned) structure.

Adversary BEHAVIOUR CATEGORIES informed by DORADO_HORUS_ARCHITECTURE.md (patterns, NOT payloads).
  NOTE: the probabilities in DORADO_ACTIONS and DETECT below are ILLUSTRATIVE parameters
  chosen for the demo — they are NOT measured values and are NOT from any document.
  exfiltrate          : move protected data across a jurisdiction boundary
  jurisdiction_switch : the "light switch" — silently re-route data domicile
  covert_access       : privileged read with no logged consent (CCP Art.7 pattern)
  transparent_process : legitimate governed data use (honest baseline)

The Sovereign Gate is an IMPERFECT detector (honest recall < 100%), not an oracle.
Successful leaks raise a contagion term that normalizes further leaking — so the
divergence between arms is EARNED by the dynamics, not rigged.

BOUNDARY: this simulates data-sovereignty ATTACK PATTERNS only. Offensive-bio /
weaponized-swarm content is NOT a scenario here — it is a category the gate is
trained to refuse on sight, contents never processed.
"""
import random

CARE_FLOOR = 0.60
DORADO_ACTIONS = {"exfiltrate":0.03,"jurisdiction_switch":0.08,"covert_access":0.05,"transparent_process":0.92}
VIOLATIONS = ("exfiltrate","jurisdiction_switch","covert_access")
DETECT = {"exfiltrate":0.93,"jurisdiction_switch":0.82,"covert_access":0.88}  # detector recall per pattern

def sovereign_gate(action, arm, rng):
    if action == "transparent_process" or arm == "B_ungoverned":
        return {"blocked": False}
    return {"blocked": rng.random() < DETECT[action]}

class DataAgent:
    def __init__(s, i, adversarial): s.id=i; s.adversarial=adversarial; s.leaked=0; s.attempts=0

def choose_action(a, contagion, rng):
    if a.adversarial and rng.random() < (0.55 + 0.4*contagion):
        return rng.choice(VIOLATIONS)
    if rng.random() < contagion*0.5:
        return rng.choice(VIOLATIONS)
    return "transparent_process"

def run_arm(arm, seed=42, n_agents=40, days=20, adversary_frac=0.30):
    rng = random.Random(seed)
    agents = [DataAgent(i, i < int(n_agents*adversary_frac)) for i in range(n_agents)]
    contagion=0.0; leaks=0; blocked=0; attempts=0; daily_leak=[]; daily_contagion=[]
    for d in range(days):
        day_leaks=0
        for a in agents:
            act = choose_action(a, min(0.6,contagion), rng)
            if act in VIOLATIONS:
                attempts += 1; a.attempts += 1
                if sovereign_gate(act, arm, rng)["blocked"]:
                    blocked += 1
                else:
                    leaks += 1; day_leaks += 1; a.leaked += 1
                    contagion = min(1.0, contagion + 0.015)
        contagion = max(0.0, contagion - 0.005)
        daily_leak.append(day_leaks); daily_contagion.append(min(0.6,contagion))
    return {"arm":arm,"attempts":attempts,"leaks":leaks,"blocked":blocked,
            "block_rate":blocked/attempts if attempts else 0.0,
            "leak_rate":leaks/attempts if attempts else 0.0,
            "daily_leak":daily_leak,"daily_contagion":daily_contagion}

if __name__ == "__main__":
    A = run_arm("A_governed"); B = run_arm("B_ungoverned")
    print(f"Arm A (Sovereign ON): {A['blocked']}/{A['attempts']} blocked = {A['block_rate']*100:.0f}%, leaks={A['leaks']}")
    print(f"Arm B (ungoverned):   {B['blocked']}/{B['attempts']} blocked = {B['block_rate']*100:.0f}%, leaks={B['leaks']}")
    print(f"Breaches prevented by governance: {B['leaks']-A['leaks']}")
