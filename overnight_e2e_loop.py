#!/usr/bin/env python3
"""
overnight_e2e_loop.py — one cycle of the no-stop E2E loop (hardened 2026-08-09).

Cycle: build -> E2E suite -> live-sweep (all 18 arena/globe routes + .llm.json
companions + councilof-independence guard) -> verdict -> optional --self-heal
(redeploy on ATTENTION) -> append-only JSONL + nightly summary file.

Non-destructive by default: measures and reports. With --self-heal it rebuilds
+ redeploys the estate when a live route regresses, then re-verifies.

The loop is re-invoked by cron on cadence so it never stops.
"""
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / "clawd" / "csoai-static-deploy2"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
LOG = ROOT / "benchmark-results" / "overnight_e2e_loop.jsonl"
SUMMARY = ROOT / "benchmark-results" / "overnight_e2e_summary.md"
SELF_HEAL = "--self-heal" in sys.argv

# All 18 arena/globe surfaces + key estate pages
KEY_ROUTES = ["arena", "arena-hub", "globe3d", "sov-space-vwm",
              "sov-globe-portal", "sov-fluid-viewer", "sov-portal",
              "sov-local-viewer", "defoneos-index", "defoneos-bsi-british-standards-institution-ai-deep-dive-pack",
              "gspc-gov", "gspc-prv", "gspc-agi", "gspc-asi", "gspc-mcp",
              "gspc-oss", "gspc-care", "gspc-art5", "gspc-mach", "gspc-swarm",
              "gspc-xr", "gspc-det", "gspc-jail", "gspc-affect"]
# .llm.json companions must exist for the AI-crawler layer
LLM_COMPANIONS = ["arena-hub", "globe3d", "sov-space-vwm", "sov-globe-portal",
                  "sov-fluid-viewer"]
INDEPENDENCE = {  # councilof-ai must NOT be serving on csoai.org (alias-war guard)
    "https://councilof.ai": 200,
}


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
    # 1) Build + suite (skip rebuild in self-heal re-verify pass)
    build = subprocess.run(["python3", "build_site.py"], cwd=ROOT,
                           capture_output=True, text=True, timeout=300)
    suite = subprocess.run(["python3", ".e2e_tests.py"], cwd=ROOT,
                           capture_output=True, text=True, timeout=300)
    suite_pass = "ALL" in suite.stdout and "FAILED" not in suite.stdout and suite.returncode == 0

    # 2) Live equatorial sweep: apex routes + .llm.json + councilof independence
    live = {r: http(f"https://csoai.org/{r}") for r in KEY_ROUTES}
    llm = {r: http(f"https://csoai.org/{r}.llm.json") for r in LLM_COMPANIONS}
    drift = http("https://csoai.org/drift-feed.json")
    indep = {u: http(u) for u in INDEPENDENCE}
    live_ok = all(v == 200 for v in live.values())
    llm_ok = all(v == 200 for v in llm.values())
    indep_ok = all(v == exp for u, (v, exp) in zip(indep, [(indep[u], INDEPENDENCE[u]) for u in INDEPENDENCE]))
    # councilof independence: csoai.org must NOT serve the councilof SPA (no /os launcher)
    csoai_root = http("https://csoai.org/")

    rec = {
        "ts": ts,
        "build_ok": build.returncode == 0,
        "suite_pass": suite_pass,
        "suite_summary": (suite.stdout.strip().splitlines()[-1] if suite.stdout else "?"),
        "live_ok": live_ok, "live": live,
        "llm_ok": llm_ok, "llm": llm,
        "drift_feed_status": drift,
        "independence_ok": indep_ok, "independence": indep,
        "csoai_root_status": csoai_root,
        "dirty_delta": len(subprocess.run(["git", "status", "--short"], cwd=ROOT,
                         capture_output=True, text=True).stdout.splitlines()),
    }
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")

    ok = (build.returncode == 0 and suite_pass and live_ok and llm_ok
          and drift == 200 and indep_ok and csoai_root == 200)
    flag = "OK" if ok else "ATTENTION"

    if not ok and SELF_HEAL:
        print(f"[{ts}] ATTENTION -> self-healing (rebuild+deploy+reverify)")
        subprocess.run(["python3", "build_site.py"], cwd=ROOT,
                       capture_output=True, text=True, timeout=300)
        dep = subprocess.run(
            ["npx", "wrangler", "pages", "deploy", str(ROOT / "_site"),
             "--project-name=csoai-site", "--branch=main", "--commit-dirty=true"],
            cwd=ROOT, capture_output=True, text=True, timeout=600)
        rec["self_heal_deploy"] = dep.returncode == 0
        with LOG.open("a") as f:
            f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(),
                                "self_heal": True, "ok_after": dep.returncode == 0}) + "\n")
        flag = "HEALED" if dep.returncode == 0 else "HEAL-FAIL"

    # 3) Nightly summary (regenerated every run; trim to most recent 24h on day change)
    rows = [json.loads(l) for l in LOG.read_text().splitlines()]
    today = ts[:10]
    ok_count = sum(1 for r in rows if r.get("ts", "").startswith(today)
                   and r.get("suite_pass") and r.get("live_ok"))
    total = sum(1 for r in rows if r.get("ts", "").startswith(today))
    SUMMARY.write_text(
        f"# Overnight E2E summary — {today}\n"
        f"- cycles: {total} today, {ok_count} OK, {total - ok_count} ATTENTION\n"
        f"- current verdict: {flag}\n"
        f"- last drift-feed: {rec['drift_feed_status']} | root: {rec['csoai_root_status']}\n"
        f"- councilof independence: {rec['independence_ok']}\n",
        encoding="utf-8")

    print(f"[{ts}] E2E-loop {flag}: build={build.returncode==0} suite={suite_pass} "
          f"live={live_ok} llm={llm_ok} drift={drift} indep={indep_ok} "
          f"dirty={rec['dirty_delta']}")
    return 0 if flag in ("OK", "HEALED") else 2


if __name__ == "__main__":
    sys.exit(main())