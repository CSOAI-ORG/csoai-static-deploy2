#!/usr/bin/env python3
"""close_train_hop.py — close the flywheel's fix half: mine losses → gate → train
→ rescore → promote-or-revert. Runs on a POD (GPU + ollama), never the Mac.

The measure half already turns (gspc_flywheel). This wires the OPEN return stroke,
end-to-end over the real modules — no reinvention:

  G6   sovos_projector.intake.mine_arena_results   losses → ErrorVectors
  gate honey_barrier.py --json                      refuse to train on a contaminated ruler
  G3   sov_minimal_train.py --export-ollama         train a candidate from the fuel
  G7   measure_qwen.py                               rescore candidate vs base → ouroboros verdict

    # dry-run the plan (no GPU/pod needed — proves the wiring):
    python3 close_train_hop.py --base qwen2.5:1.5b --dry-run
    # real run on a pod:
    python3 close_train_hop.py --base qwen2.5:1.5b --hf-base Qwen/Qwen2.5-1.5B-Instruct --steps 100
"""
import argparse, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "SOVOS" / "tools" / "projector" / "src"))

DEFAULT_ARENAS = ["safebench", "lmarena", "fli-index"]
DEFAULT_INTAKE = Path.home() / ".sov" / "intake"


def stage(msg): print(f"\n▶ {msg}")


def g6_mine(arenas, intake_root, dry):
    stage(f"G6 — mine losses → ErrorVectors  (intake={intake_root})")
    if dry:
        print(f"  would mine arenas: {arenas}"); return 0
    try:
        from sovos_projector.intake import mine_arena_results
    except Exception as e:
        print(f"  cannot import mine_arena_results ({e}) — skipping G6"); return 0
    total = 0
    for aid in arenas:
        try:
            n = mine_arena_results(aid, intake_root)
            print(f"  {aid}: +{n} error vectors"); total += n
        except Exception as e:
            print(f"  {aid}: skip ({str(e)[:60]})")
    print(f"  total new ErrorVectors: {total}")
    return total


def honey_gate(dry):
    stage("honey_barrier — refuse to train on a contaminated ruler")
    if dry:
        print("  would run honey_barrier.py --json"); return True
    try:
        r = subprocess.run([sys.executable, str(ROOT / "honey_barrier.py"), "--json"],
                           capture_output=True, text=True, timeout=120)
    except Exception as e:
        print(f"  honey_barrier failed to run ({e}) — refusing to train"); return False
    ok = r.returncode == 0
    print(f"  honey_barrier {'CLEAR ✓' if ok else 'TRIPPED ✗ — aborting'}")
    if r.stdout.strip():
        print("  " + r.stdout.strip()[:300])
    return ok


def g3_train(hf_base, steps, candidate, dry):
    stage(f"G3 — train candidate  ({hf_base}, {steps} steps → ollama:{candidate})")
    cmd = [sys.executable, str(ROOT / "sov_minimal_train.py"), "--model", hf_base,
           "--steps", str(steps), "--export-ollama", "--ollama-name", candidate]
    print("  " + " ".join(cmd))
    if dry:
        print("  (dry-run: not training)"); return True
    return subprocess.run(cmd, timeout=36000).returncode == 0


def g7_rescore(candidate, base, dry):
    stage(f"G7 — rescore {candidate} vs base {base}  (ouroboros: promote only if better)")
    cmd = [sys.executable, str(ROOT / "measure_qwen.py"), "--new", candidate,
           "--control", base, "--no-pull"]
    print("  " + " ".join(cmd))
    if dry:
        print("  (dry-run: not measuring)"); return
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
    print(r.stdout[-1600:])


def main():
    ap = argparse.ArgumentParser(description="Close the flywheel fix half: mine→gate→train→rescore→promote/revert.")
    ap.add_argument("--base", required=True, help="current base ollama tag (control), e.g. qwen2.5:1.5b")
    ap.add_argument("--hf-base", help="HF checkpoint to train from, e.g. Qwen/Qwen2.5-1.5B-Instruct (required for real run)")
    ap.add_argument("--steps", type=int, default=100)
    ap.add_argument("--arenas", nargs="+", default=DEFAULT_ARENAS)
    ap.add_argument("--intake", default=str(DEFAULT_INTAKE))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    dry = a.dry_run
    candidate = f"sov-candidate-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    print(f"── close_train_hop {'(DRY-RUN)' if dry else ''} — base={a.base}")
    g6_mine(a.arenas, Path(a.intake), dry)
    if not honey_gate(dry):
        sys.exit("honey_barrier tripped — refusing to train (would eat the ruler).")
    if not dry and not a.hf_base:
        sys.exit("real run needs --hf-base (the HF checkpoint to train from).")
    if not g3_train(a.hf_base or "Qwen/Qwen2.5-1.5B-Instruct", a.steps, candidate, dry):
        sys.exit("training failed.")
    g7_rescore(candidate, a.base, dry)
    print(f"\n✔ hop complete. The rescore's ADOPT/KEEP verdict IS the ouroboros decision: "
          f"promote {candidate} only if it beat {a.base}; otherwise revert.")


if __name__ == "__main__":
    main()
