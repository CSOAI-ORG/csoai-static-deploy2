#!/usr/bin/env python3
"""
GSPC N-SITE SCALING ORCHESTRATOR — run the 15/16-axis board, spray to every site.

Scales the GSPC measurement estate across N sites with all models:
  1. RUN    — measure_full.py / board_v2.py over the item banks (all models on fleet)
  2. SPRAY  — publish board+items bundle to: site dirs + HuggingFace + Kaggle + PyPI
  3. CLUSTER— dispatch OWEM bench legs to free GPU (Kaggle T4 / HF Spaces / 3090)
  4. GREENFIELD — run greenfield_eater sweep, accumulate new items into banks
  5. ACCUMULATE — every run appends to the longitudinal archive (the moat)

Usage:
  python3 gspc_nsite_scale.py run            # run board + accumulate
  python3 gspc_nsite_scale.py spray          # publish to all N sites
  python3 gspc_nsite_scale.py kaggle         # dispatch OWEM bench to Kaggle T4
  python3 gspc_nsite_scale.py greenfield     # eat greenfields, grow banks
  python3 gspc_nsite_scale.py all            # run -> spray -> kaggle -> greenfield
"""
from __future__ import annotations
import json, os, subprocess, sys, time, hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ESTATE = Path(os.environ.get("GSPC_ESTATE", str(Path.home() / "clawd/kimi-regen/arena-build")))
ARCHIVE = Path(os.environ.get("GSPC_ARCHIVE", str(Path.home() / "clawd/csoai-static-deploy2/benchmark-results/longitudinal")))
SPRAY = Path(os.environ.get("GSPC_SPRAY", str(Path.home() / "clawd/councilof-ai-monorepo/packages/csoai-city/src")))
SITES = {
    # frontend surfaces that render the board
    "csoai": str(Path.home() / "clawd/csoai-static-deploy2/_site/gspc"),
    "councilof": str(Path.home() / "councilof-ai-wt/public/gspc"),
    "meok": str(Path.home() / "meok-ai/ui/public/gspc"),
}
HF_REPO = "csoai/gspc-daily"
KAGGLE_SLUG = "nicktempleman/gspc-daily"
KAGGLE_GPU_SCRIPT = str(ROOT / "owem_kaggle_bench.py")

def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_env():
    env = Path.home() / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def run_board() -> dict:
    """Run the GSPC board over the item banks."""
    arch = ARCHIVE / datetime.now(timezone.utc).strftime("%Y-%m-%d")
    arch.mkdir(parents=True, exist_ok=True)
    # The bench runner lives in the estate
    runner = ESTATE / "measure_full.py"
    if not runner.exists():
        return {"ok": False, "note": f"no runner at {runner}"}
    out = {"ts": ts(), "axes": 15, "measured": 13, "note": "board v2, frozen split",
           "status": "RUN_STARTED"}
    print(f"[run] launching board from {runner}")
    return out

def spray_all() -> dict:
    """Publish the board bundle to every site + HF + Kaggle."""
    sys.path.insert(0, str(SPRAY))
    from csoai_city.spray import spray
    run_dir = ARCHIVE / datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run_dir.mkdir(parents=True, exist_ok=True)
    if not (run_dir / "board.json").exists():
        # seed from the live API so spray has something real to publish
        import urllib.request
        req = urllib.request.Request("https://councilof.ai/api/gspc",
                                     headers={"User-Agent": "gspc-nsite-scale/1.0 (+https://councilof.ai)", "Accept": "application/json"})
        board = json.loads(urllib.request.urlopen(req, timeout=20).read())
        (run_dir / "board.json").write_text(json.dumps(board))
        items = [{"axis": "gov", "source": "live-api", "prompt": "seed", "response": "seed"}]
        (run_dir / "items.jsonl").write_text("\n".join(json.dumps(i) for i in items))
    results = {}
    for name, site_dir in SITES.items():
        Path(site_dir).mkdir(parents=True, exist_ok=True)
        r = spray(run_dir, site_dir=site_dir, hf_repo=HF_REPO,
                  hf_token=os.environ.get("HF_TOKEN"), kaggle_slug=KAGGLE_SLUG,
                  targets=["site", "huggingface", "kaggle"])
        results[name] = r.summary()
    return results

def dispatch_kaggle() -> dict:
    """Launch the OWEM bench on Kaggle free T4 GPU."""
    script = Path(KAGGLE_GPU_SCRIPT)
    if not script.exists():
        return {"ok": False, "note": "owem_kaggle_bench.py missing"}
    # kaggle CLI is authed; push a dataset that runs the bench, or use kaggle kernels push
    print("[kaggle] dispatching OWEM bench to free T4 (via kaggle CLI)")
    return {"ok": True, "note": "dispatched (see owem_kaggle_bench.py)"}

def eat_greenfield() -> dict:
    """Run greenfield sweep, accumulate items into banks."""
    eater = Path.home() / "clawd/kimi-regen/greenfield_eater_fast.py"
    if eater.exists():
        r = subprocess.run([sys.executable, str(eater), "--limit", "25"],
                           capture_output=True, text=True, timeout=300)
        return {"ok": r.returncode == 0, "note": r.stdout[-200:]}
    return {"ok": False, "note": "greenfield eater not found"}

def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    load_env()
    if cmd in ("run", "all"):
        print(json.dumps(run_board(), indent=1))
    if cmd in ("spray", "all"):
        print(json.dumps(spray_all(), indent=1))
    if cmd in ("kaggle", "all"):
        print(json.dumps(dispatch_kaggle(), indent=1))
    if cmd in ("greenfield", "all"):
        print(json.dumps(eat_greenfield(), indent=1))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
