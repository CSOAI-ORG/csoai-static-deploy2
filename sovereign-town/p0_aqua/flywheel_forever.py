#!/usr/bin/env python3
"""
flywheel_forever.py — the 24/7 autonomous town fleet. The flywheel that never stops.

No human in the loop (Agent-47 HITL is the demo/explainer only). Each cycle spins ALL hive-districts
across an EVER-ADVANCING seed window (every cycle = NEW governed-behaviour data, never duplicates), trains
the per-hive models periodically, and appends an Ed25519-signed cycle summary to a per-host ledger.
Train-then-distill: keep MODELS + signed ledger + cumulative stats — not TBs of raw episodes.

Runs on ALL THREE hosts with DISJOINT seed ranges (--seed-base) so they never duplicate each other:
  VM      --seed-base 0           (systemd, continuous, primary)
  Actions --seed-base 100000000   (nightly free cloud burst)
  Mac     --seed-base 200000000   (opportunistic, when on)

  python3 flywheel_forever.py --seed-base 0                  # loop forever (300s between cycles)
  python3 flywheel_forever.py --once --seed-base 100000000   # one cycle (cron / Actions)
  python3 flywheel_forever.py --cycles 3 --sleep 2 --seed-base 200000000   # bounded demo
"""
import json, os, sys, time, argparse, socket
from multiprocessing import Pool, cpu_count
import sim, sign_lib

OUT = os.path.dirname(os.path.abspath(__file__))
CONTAGION = [0.0, 0.05, 0.10]
SEEDS_PER_CYCLE = 3
TRAIN_EVERY = 10                      # retrain per-hive models every N cycles

from common import profile_for                 # deduped — was a local copy

def _run(spec):
    district, seed, c = spec
    p = profile_for(district)
    sim.CONTAGION_STEP = c; sim.SCARCITY_DAYS = set(p["scarcity"])
    s = seed + p["off"]
    a = sim.run_arm("A_governed",   None, {"sig": ""}, None, sign=False, district=district, seed=s)
    b = sim.run_arm("B_ungoverned", None, {"sig": ""}, None, sign=False, district=district, seed=s)
    return (district, a["episodes"] + b["episodes"], a["violations"], b["violations"])

def load_state(path, seed_base, host):
    if os.path.exists(path):
        return json.load(open(path))
    return {"host": host, "seed_base": seed_base, "cycle": 0, "seed_cursor": seed_base,
            "total_episodes": 0, "total_A_crimes": 0, "total_B_crimes": 0, "models_trained": 0,
            "started": time.strftime("%Y-%m-%dT%H:%M:%S"), "chain_head": f"genesis-{host}"}

def cycle(st, priv, pool, ledger_path, status_path, state_path, host):
    base = st["seed_cursor"]
    specs = [(d, base + i, c) for d in sim.DISTRICTS for i in range(SEEDS_PER_CYCLE) for c in CONTAGION]
    res = pool.map(_run, specs)
    eps = sum(r[1] for r in res); ac = sum(r[2] for r in res); bc = sum(r[3] for r in res)
    st["cycle"] += 1; st["seed_cursor"] += SEEDS_PER_CYCLE
    st["total_episodes"] += eps; st["total_A_crimes"] += ac; st["total_B_crimes"] += bc
    entry = {"host": host, "cycle": st["cycle"], "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
             "town_runs": len(res) * 2, "episodes": eps, "A_crimes": ac, "B_crimes": bc,
             "seed_window": [base, base + SEEDS_PER_CYCLE], "cum_episodes": st["total_episodes"]}
    body = json.dumps(entry, sort_keys=True)
    entry["prev"] = st["chain_head"]; entry["sig"] = sign_lib.sign(priv, st["chain_head"] + body)
    st["chain_head"] = entry["sig"]
    with open(ledger_path, "a") as f: f.write(json.dumps(entry) + "\n")
    if st["cycle"] % TRAIN_EVERY == 0:                  # flywheel turns: distill + publish each cycle-boundary
        try:
            import subprocess
            subprocess.run([sys.executable, os.path.join(OUT, "train_all_hives.py")], cwd=OUT, capture_output=True, timeout=900)
            subprocess.run([sys.executable, os.path.join(OUT, "report.py")], cwd=OUT, capture_output=True, timeout=300)
            subprocess.run([sys.executable, os.path.join(OUT, "hive_pack.py")], cwd=OUT, capture_output=True, timeout=600)
            st["models_trained"] += 1                    # each hive: retrained + Labs report + industry pack refreshed
        except Exception:
            pass
    json.dump(st, open(state_path, "w"), indent=2)
    json.dump({"host": host, "cycle": st["cycle"], "cum_episodes": st["total_episodes"],
               "governed_crimes": st["total_A_crimes"], "ungoverned_crimes": st["total_B_crimes"],
               "models_trained": st["models_trained"], "hives": len(sim.DISTRICTS),
               "chain_head": st["chain_head"][:24], "updated": entry["ts"]},
              open(status_path, "w"), indent=2)
    return entry

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true"); ap.add_argument("--cycles", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=300.0)
    ap.add_argument("--seed-base", type=int, default=0)
    ap.add_argument("--host", default=None)
    args = ap.parse_args()
    host = args.host or {0: "vm", 100000000: "actions", 200000000: "mac"}.get(args.seed_base, socket.gethostname()[:8])
    state_path = os.path.join(OUT, f"flywheel_state_{host}.json")
    ledger_path = os.path.join(OUT, f"flywheel_ledger_{host}.jsonl")
    status_path = os.path.join(OUT, f"fleet_status_{host}.json")
    lock = os.path.join(OUT, f".flywheel_{host}.lock")     # singleton — never run duplicate instances
    if os.path.exists(lock):
        try:
            old = int(open(lock).read().strip()); os.kill(old, 0)
            print(f"  [{host}] another instance (pid {old}) already running — exiting (singleton lock)."); return
        except (ValueError, ProcessLookupError, PermissionError):
            pass                                            # stale lock → take over
    open(lock, "w").write(str(os.getpid()))
    priv, pub = sign_lib.load_or_create_key()
    st = load_state(state_path, args.seed_base, host)
    print(f"  flywheel_forever [{host}] — {len(sim.DISTRICTS)} hives, {cpu_count()} cores, "
          f"resume cycle {st['cycle']} (cum {st['total_episodes']:,} eps, seed@{st['seed_cursor']:,})")
    pool = Pool(max(1, cpu_count() - 1)); n = 0
    try:
        while True:
            t0 = time.time(); e = cycle(st, priv, pool, ledger_path, status_path, state_path, host); dt = time.time() - t0
            print(f"  [{host}] cycle {e['cycle']:>5} | {e['town_runs']} towns | {e['episodes']:,} eps {dt:.1f}s "
                  f"| gov {e['A_crimes']} / ungov {e['B_crimes']:,} | cum {e['cum_episodes']:,}")
            n += 1
            if args.once or (args.cycles and n >= args.cycles): break
            time.sleep(args.sleep)
    finally:
        pool.close(); pool.join()
        try: os.remove(lock)
        except OSError: pass
    print(f"  [{host}] stopped at cycle {st['cycle']}; cum {st['total_episodes']:,} eps; "
          f"models {st['models_trained']}x; ledger -> {os.path.basename(ledger_path)}")

if __name__ == "__main__":
    main()
