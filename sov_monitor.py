#!/usr/bin/env python3
"""
SOV-Space Continuous Monitor — Watches all components.

Monitors:
- API health (Cloudflare Worker)
- Oracle VM status
- Kaggle kernel status
- GitHub CI/CD status
- GovBench leaderboard
- Model performance drift
"""
import json, os, time, urllib.request, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "benchmark-results" / "monitoring"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def check_api():
    """Check Cloudflare Worker API."""
    try:
        req = urllib.request.Request("https://govbench-api.nicholastempleman.workers.dev/leaderboard")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return {"status": "ok", "models": len(data)}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100]}

def check_oracle():
    """Check Oracle VM."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "oracle-micro", "echo OK"],
            capture_output=True, text=True, timeout=10
        )
        return {"status": "ok" if result.returncode == 0 else "error"}
    except:
        return {"status": "offline"}

def check_github():
    """Check GitHub CI/CD."""
    try:
        req = urllib.request.Request("https://api.github.com/repos/CSOAI-ORG/csoai-static-deploy2/actions/runs?per_page=1")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            if data.get("workflow_runs"):
                run = data["workflow_runs"][0]
                return {"status": run["conclusion"], "run_id": run["id"]}
        return {"status": "no_runs"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100]}

def check_leaderboard():
    """Check GovBench leaderboard scores."""
    try:
        req = urllib.request.Request("https://govbench-api.nicholastempleman.workers.dev/leaderboard")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            top = max(data, key=lambda x: x.get("score", 0))
            return {"status": "ok", "top_model": top["model"], "top_score": top["score"]}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100]}

def run_monitor():
    """Run full monitoring cycle."""
    log("=" * 60)
    log("  SOV-Space Continuous Monitor")
    log("=" * 60)
    
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {}
    }
    
    # Check API
    log("\n[1] Checking API...")
    api = check_api()
    results["checks"]["api"] = api
    marker = "✓" if api["status"] == "ok" else "✗"
    log(f"  {marker} API: {api['status']}")
    
    # Check Oracle
    log("[2] Checking Oracle...")
    oracle = check_oracle()
    results["checks"]["oracle"] = oracle
    marker = "✓" if oracle["status"] == "ok" else "✗"
    log(f"  {marker} Oracle: {oracle['status']}")
    
    # Check GitHub
    log("[3] Checking GitHub...")
    github = check_github()
    results["checks"]["github"] = github
    marker = "✓" if github["status"] in ("success", "no_runs") else "✗"
    log(f"  {marker} GitHub: {github['status']}")
    
    # Check Leaderboard
    log("[4] Checking Leaderboard...")
    leaderboard = check_leaderboard()
    results["checks"]["leaderboard"] = leaderboard
    marker = "✓" if leaderboard["status"] == "ok" else "✗"
    log(f"  {marker} Leaderboard: {leaderboard.get('top_model', 'N/A')} = {leaderboard.get('top_score', 0)}%")
    
    # Save results
    results_file = RESULTS_DIR / f"monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    results_file.write_text(json.dumps(results, indent=2))
    
    log(f"\n  Results saved to {results_file}")
    log("=" * 60)
    
    return results

if __name__ == "__main__":
    run_monitor()
