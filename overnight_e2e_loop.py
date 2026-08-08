#!/usr/bin/env python3
"""
overnight_e2e_loop.py — one cycle of the no-stop E2E loop.

Cycle: build -> run E2E suite -> live-sweep apex -> (report + exit).
The loop tool (cron) re-invokes this on cadence so it never stops.

Non-destructive: never edits pages, never deploys automatically; it measures,
reports and leaves decisions to the agent that owns the loop. Each run appends
a dated verdict to benchmark-results/overnight_e2e_loop.jsonl (append-only).
"""
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / "clawd" / "csoai-static-deploy2"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
LOG = ROOT / "benchmark-results" / "overnight_e2e_loop.jsonl"
KEY_ROUTES = ["arena", "globe3d", "sov-space-vwm", "sov-globe-portal",
              "sov-fluid-viewer", "sov-portal", "sov-local-viewer",
              "defoneos-index", "gspc-care", "gspc-mach", "gspc-jail"]

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0

def main():
    ts = datetime.now(timezone.utc).isoformat()
    # 1) Build + suite
    build = subprocess.run(["python3", "build_site.py"], cwd=ROOT,
                           capture_output=True, text=True, timeout=300)
    suite = subprocess.run(["python3", ".e2e_tests.py"], cwd=ROOT,
                           capture_output=True, text=True, timeout=300)
    suite_pass = "ALL" in suite.stdout and "FAILED" not in suite.stdout and suite.returncode == 0
    # 2) Live apex sweep
    live = {r: http(f"https://csoai.org/{r}") for r in KEY_ROUTES}
    drift = http("https://csoai.org/drift-feed.json")
    live_ok = all(v == 200 for v in live.values())
    rec = {
        "ts": ts, "build_ok": build.returncode == 0,
        "build_files": "" if build.returncode else "ok",
        "suite_pass": suite_pass,
        "suite_summary": (suite.stdout.strip().splitlines()[-1] if suite.stdout else "?"),
        "live_ok": live_ok, "drift_feed_status": drift,
        "routes": live,
        "dirty_delta": len(subprocess.run(["git", "status", "--short"], cwd=ROOT,
                         capture_output=True, text=True).stdout.splitlines()),
    }
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    flag = "OK" if (build.returncode == 0 and suite_pass and live_ok) else "ATTENTION"
    print(f"[{ts}] E2E-loop {flag}: build={build.returncode==0} suite={suite_pass} "
          f"live={live_ok} drift={drift} dirty={rec['dirty_delta']}")
    return 0 if flag == "OK" else 2

if __name__ == "__main__":
    sys.exit(main())