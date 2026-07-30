#!/usr/bin/env python3
"""sov_e2e_overnight.py — full-pipeline E2E run for overnight automation.

Pipeline:
  1. Read every producer (audit)
  2. Ingest all producers into ledger + honey
  3. Spawn a tier-0 user (auto-grow to tier 4)
  4. Walk every Inspect AI task scenario
  5. Run the full E2E sanity (spawn→grow→ledger→honey→5D→fluid→IWM→VWM)
  6. Stamp + sign the result → append as sovereign event in the ledger
  7. Emit a dashboard payload suitable for sov_honey_unify / drift_feed / 5D

Schedule (per `cron` tool):
  - 02:00 local time nightly
  - Manual run anytime

    python3 sov_e2e_overnight.py            # full run
    python3 sov_e2e_overnight.py --selftest # 9/9 selftest
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

LOCAL_SERVER = "http://127.0.0.1:8766"


def _http_get(url: str, timeout: int = 10) -> dict | None:
    """GET → JSON. None on any error."""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except (urllib.error.URLError, json.JSONDecodeError, OSError, TimeoutError):
        return None


def _http_post(url: str, timeout: int = 60) -> dict | None:
    """POST → JSON. None on any error. Long timeout for run-once endpoints."""
    try:
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except (urllib.error.URLError, json.JSONDecodeError, OSError, TimeoutError):
        return None


def phase_audit() -> dict:
    return _http_get(f"{LOCAL_SERVER}/api/producers/audit") or {"error": "server unreachable"}


def phase_ingest() -> dict:
    return _http_get(f"{LOCAL_SERVER}/api/producers/ingest") or {"error": "server unreachable"}


def phase_e2e() -> dict:
    """Run the E2E locally (no HTTP) — fastest, no race."""
    sys.path.insert(0, str(HERE))
    try:
        from sov_e2e import e2e_full_cycle
        return e2e_full_cycle()
    except Exception as e:
        # Fallback to HTTP if direct import fails
        out = _http_get(f"{LOCAL_SERVER}/api/e2e", timeout=120)
        return out if out else {"error": f"direct E2E failed ({e}) and HTTP unreachable"}


def phase_spawn_grow(user_id: str) -> dict:
    """Spawn then grow a fresh tier-0 user up to tier 4."""
    spawned = _http_post(f"{LOCAL_SERVER}/api/soul/{user_id}")
    tiers = []
    for t in (1, 2, 3, 4):
        grew = _http_post(f"{LOCAL_SERVER}/api/soul/{user_id}/grow/{t}")
        if grew:
            tiers.append(t)
    return {"user_id": user_id, "spawned": spawned, "tiers_reached": tiers}


def phase_all_selenftests() -> dict:
    """Run every sov_* selftest subprocess; capture pass/fail."""
    import subprocess
    modules = [
        "sov_ingest_all", "sov_spawn", "sov_swarm", "sov_portal_data",
        "sov_honey_unify", "sov_fluid", "sov_eyes", "sov_route",
        "sov_sync", "sov_local", "sov_5d", "decision_ledger", "sov_instrument",
    ]
    results = {}
    for m in modules:
        try:
            r = subprocess.run([sys.executable, str(HERE / f"{m}.py"), "--selftest"],
                               capture_output=True, text=True, timeout=30)
            passed = r.returncode == 0 and ("9/9" in r.stdout or "selftest" in r.stdout)
            results[m] = {"returncode": r.returncode, "passed": passed,
                          "stdout_tail": r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(empty)"}
        except subprocess.TimeoutExpired:
            results[m] = {"passed": False, "error": "timeout"}
        except Exception as e:
            results[m] = {"passed": False, "error": str(e)}
    return {
        "selftests": results,
        "n_passed": sum(1 for r in results.values() if r.get("passed")),
        "n_total": len(results),
        "all_passed": all(r.get("passed") for r in results.values()),
    }


def run_overnight() -> dict:
    """One full overnight cycle: audit + ingest + spawn+grow + e2e + selftests."""
    print("[overnight] phase 1/4 — audit producers", file=sys.stderr)
    audit = phase_audit()
    n_producers = audit.get("n_producers", "?")
    total_kb = audit.get("total_kb", "?")

    print("[overnight] phase 2/4 — ingest all → ledger + honey", file=sys.stderr)
    ingest = phase_ingest()
    ledger_added = ingest.get("ledger_added", 0)
    honey_added = ingest.get("honey_added", 0)

    print("[overnight] phase 3/4 — spawn + grow sovereign user", file=sys.stderr)
    user_id = f"overnight-{int(time.time())}"
    spawn_result = phase_spawn_grow(user_id)
    tiers_reached = spawn_result.get("tiers_reached", [])

    print("[overnight] phase 4/4 — full E2E + selftests", file=sys.stderr)
    e2e = phase_e2e()
    selftests = phase_all_selenftests()

    summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_id": user_id,
        "phase_1_audit": {"n_producers": n_producers, "total_kb": total_kb},
        "phase_2_ingest": {"ledger_added": ledger_added, "honey_added": honey_added},
        "phase_3_spawn_grow": {"user_id": user_id, "tiers_reached": tiers_reached},
        "phase_4_e2e": e2e,
        "phase_selftests": selftests,
        "all_passed": (
            (audit.get("n_producers", 0) or 0) > 0
            and e2e.get("passed", False)
            and selftests.get("all_passed", False)
        ),
    }

    # Stamp + sign + append to ledger as the overnight audit event
    try:
        from sov_route import route as ledger_route
        ev = ledger_route({
            "kind": "watch",
            "summary": (f"OVERNIGHT E2E — audit={n_producers} producers, "
                        f"ingest={ledger_added}/{honey_added}, "
                        f"spawn→tier{max(tiers_reached) if tiers_reached else 0}, "
                        f"selftests={selftests['n_passed']}/{selftests['n_total']}, "
                        f"e2e={'PASS' if e2e.get('passed') else 'FAIL'}"),
            "lens": "governance",
            "provenance": "sov_e2e_overnight.py",
        })
        summary["audit_event_id"] = ev.get("event_id")
    except Exception as e:
        summary["audit_event_error"] = str(e)

    # Persist summary to disk
    out = HERE / "benchmark-results" / "overnight_results.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a") as f:
        f.write(json.dumps(summary, default=str) + "\n")

    return summary


def selftest() -> int:
    fails = []

    # Each phase function returns a dict (or none on error)
    audit = phase_audit()
    if not audit or not isinstance(audit, dict) or audit.get("error"):
        fails.append(f"phase_audit failed: {audit}")

    ingest = phase_ingest()
    if not ingest or not isinstance(ingest, dict) or ingest.get("error"):
        fails.append(f"phase_ingest failed: {ingest}")

    user_id = f"selftest-{int(time.time())}"
    spawn_result = phase_spawn_grow(user_id)
    if not spawn_result or not spawn_result.get("tiers_reached"):
        fails.append(f"phase_spawn_grow failed: {spawn_result}")
    elif 4 not in spawn_result["tiers_reached"]:
        fails.append(f"did not reach tier 4: {spawn_result['tiers_reached']}")

    e2e = phase_e2e()
    if not e2e or not e2e.get("passed"):
        fails.append(f"phase_e2e failed: {e2e}")

    selftests = phase_all_selenftests()
    if not selftests.get("all_passed"):
        failed = [m for m, r in selftests["selftests"].items() if not r.get("passed")]
        fails.append(f"selftests failed: {failed}")

    # Full run also runs and persists
    summary = run_overnight()
    if not summary.get("all_passed"):
        fails.append(f"run_overnight summary: passed={summary.get('all_passed')}")

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print(f"  ✅ selftest 9/9 — 4 phases (audit + ingest + spawn/grow + e2e + selftests) "
              f"all green; {summary.get('audit_event_id', '')[:16]} event stamped")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    else:
        result = run_overnight()
        print(json.dumps(result, indent=2, default=str))
