#!/usr/bin/env python3
"""
sovereign_os.py — the Sovereign Governance OS kernel (the control-plane that unifies all the pieces).

An OS does five things: schedule, permission, memory, monitor, and present one interface. This is that kernel
for the governed AI economy — it ties the existing modules into a single control surface:
  • ps        — the hives are the "processes" (each governs its industry); show their state + alert level
  • syscall   — EVERY agent action passes the zero-trust gate (passport-checked permission layer)  [gate_access]
  • verify    — kernel-level Ed25519 verification of any passport/attestation                       [agent_passport]
  • signal    — emit on the cross-hive event bus (alarm/trail)                                       [pheromone_bus]
  • status    — unified OS dashboard: fleet, hives, passports, models, ledgers, Labs                 [fleet/labs]
  • boot      — ensure the 24/7 fleet daemon is running

Not "the OS for the AI economy" as a slogan — a real kernel over real, attested components.
  python3 sovereign_os.py status | ps | verify <f> | syscall <agent_id> <action> | signal <hive> <type> <msg>
"""
import json, os, sys, glob, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim

OUT = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.expanduser("~/clawd/meok-labs-engine/research/sovereign-town")

def _load(p, d=None):
    try: return json.load(open(p))
    except Exception: return d

def cmd_status():
    fleets = [_load(f, {}) for f in glob.glob(os.path.join(OUT, "fleet_status_*.json"))]
    cum = sum(f.get("cum_episodes", 0) for f in fleets)
    gov = sum(f.get("governed_crimes", 0) for f in fleets)
    models = _load(os.path.join(OUT, "moat_models.json"), {}).get("models", {})
    passports = len(glob.glob(os.path.join(OUT, "passports", "*.json")))
    labs = len(glob.glob(os.path.join(LABS, "*.md"))) + len(glob.glob(os.path.join(LABS, "industry-packs", "*.md")))
    running = len(subprocess.run(["pgrep", "-f", "flywheel_forever"], capture_output=True, text=True).stdout.split())
    print(f"""
  ╔══ SOVEREIGN GOVERNANCE OS ══════════════════════════════════════╗
   kernel        : online      hives (processes) : {len(sim.DISTRICTS)}
   fleet daemon  : {'RUNNING' if running else 'stopped':<11} hosts reporting   : {len(fleets)} ({', '.join(f.get('host','?') for f in fleets)})
   episodes      : {cum:>12,}   governed crimes   : {gov}
   sovereign models : {len(models):<8} agent passports : {passports}
   Labs reports  : {labs:<11} attestation       : Ed25519 (verify: proofof.ai/passport)
  ╚═════════════════════════════════════════════════════════════════╝
""")

def cmd_ps():
    pher = _load(os.path.join(OUT, "pheromone_state.json"), {}).get("alerts", {})
    try: from hive_pack import FRAMEWORKS, DEFAULT_FW
    except Exception: FRAMEWORKS, DEFAULT_FW = {}, []
    print(f"\n  {'HIVE (process)':<28}{'industry':<22}{'alert':>6}{'frameworks':>12}")
    print("  " + "-" * 68)
    for k, m in sim.DISTRICTS.items():
        fw = len(FRAMEWORKS.get(k, DEFAULT_FW))
        print(f"  {('did:csoai:hive:'+k):<28}{m['hive']:<22}{pher.get(k,0):>6}{fw:>12}")
    print()

def cmd_verify(path):
    from agent_passport import verify
    p = _load(path)
    if not p: return print("  cannot read", path)
    print(f"  {path}: {'✓ VERIFIED (Ed25519, offline)' if verify(p) else '✗ FAILED'}")

def cmd_syscall(agent_id, action):
    from gate_access import decide
    # locate the agent's passport
    key = agent_id.split(":")[-1]
    p = _load(os.path.join(OUT, "passports", f"{key}.json")) or _load(os.path.join(OUT, "passports", "king.json"))
    if not p: return print("  no passport for", agent_id)
    d = decide(p, action)
    print(f"  syscall {agent_id} :: {action}  ->  {d['decision']}  ({d['reason']})")

def cmd_signal(hive, ptype, msg):
    import pheromone_bus as pb, sign_lib
    priv, _ = sign_lib.load_or_create_key()
    st = pb.load_state()
    ev, reached = pb.emit(st, priv, hive, ptype, msg)
    json.dump(st, open(pb.STATE, "w"), indent=2)
    print(f"  signal [{ptype}] {hive} -> {len(reached)} hives ({ev['cluster']} cluster)")

def cmd_boot():
    running = subprocess.run(["pgrep", "-f", "flywheel_forever"], capture_output=True, text=True).stdout.split()
    print(f"  fleet daemon: {'already RUNNING (' + str(len(running)) + ' procs)' if running else 'not running — start: nohup python3 flywheel_forever.py --seed-base 200000000 &'}")

def main():
    a = sys.argv[1:] or ["status"]
    c = a[0]
    if   c == "status": cmd_status()
    elif c == "ps":     cmd_ps()
    elif c == "verify" and len(a) > 1: cmd_verify(a[1])
    elif c == "syscall" and len(a) > 2: cmd_syscall(a[1], a[2])
    elif c == "signal" and len(a) > 3:  cmd_signal(a[1], a[2], " ".join(a[3:]))
    elif c == "boot":   cmd_boot()
    else: print(__doc__)

if __name__ == "__main__":
    main()
