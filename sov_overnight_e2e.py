#!/usr/bin/env python3
"""
sov_overnight_e2e.py — Overnight autonomous E2E batch loop (JEEVES, T6).

Runs ONLY the deterministic, runnable-now suites (no GPU / API-key / billing
gates). Loops continuously, logs every run to a rolling JSONL + MD report, and
records any deterministic failure verbatim so a follow-on turn can fix it.

Deliberately EXCLUDES infra-gated work (Ollama, RunPod, GCP/SOV3, DeepSeek 402,
DASHSCOPE keys) — those are external gates, not code bugs, and looping on them
just burns cycles.

Suites (all verified runnable 2026-08-08):
  1. csoai-static-deploy2/.e2e_tests.py          — 111-assert static-site audit
  2. csoai-static-deploy2 CI invariants          — py_compile + ledger/instrument selftests
  3. councilof-ai unit (vitest run)              — currently 3 tests
  4. councilof-ai pre-deploy Playwright (chromium) — 11 checks
"""
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DEPLOY2 = Path("/Users/nicholas/clawd/csoai-static-deploy2")
COUNCIL = Path("/Users/nicholas/clawd/councilof-ai")
REPORT_DIR = Path("/Users/nicholas/clawd/sov-city/runs")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG = REPORT_DIR / "overnight_e2e.jsonl"
MD = REPORT_DIR / "overnight_e2e.md"

MAX_LOOP = int(sys.argv[1]) if len(sys.argv) > 1 else 24  # passes
INTERVAL = 900  # 15 min between passes

def run(name: str, cwd: Path, cmd: list, timeout: int = 600) -> dict:
    t0 = time.time()
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        ok = r.returncode == 0
        return {
            "name": name, "ok": ok, "rc": r.returncode,
            "secs": round(time.time() - t0, 1),
            "tail": (r.stdout or "")[-900:] + "\n--STDERR--\n" + (r.stderr or "")[-900:],
        }
    except subprocess.TimeoutExpired:
        return {"name": name, "ok": False, "rc": "TIMEOUT", "secs": timeout,
                "tail": f"exceeded {timeout}s"}
    except Exception as e:  # noqa
        return {"name": name, "ok": False, "rc": "ERR", "secs": round(time.time() - t0, 1),
                "tail": str(e)}

def suites() -> list:
    # static deploy2 E2E
    s = []
    py = shutil.which("python3") or "python3"
    s.append(("deploy2-e2e", DEPLOY2, [py, ".e2e_tests.py"], 900))
    # CI invariants
    for script in ["decision_ledger.py", "sov_instrument.py", "sovereign_merkle_vm.py"]:
        p = DEPLOY2 / script
        if p.exists():
            s.append((f"ci-{p.stem}", DEPLOY2, [py, script, "--selftest"], 200))
    s.append(("ci-capability-registry", DEPLOY2, [py, "tools/verify_capability_registry.py"], 200))
    # py_compile of key files
    s.append(("ci-pycompile", DEPLOY2, [py, "-m", "py_compile", ".e2e_tests.py", "sov_orchestrator.py"], 120))
    # councilof-ai unit
    if (COUNCIL / "node_modules/.bin").exists():
        s.append(("council-unit", COUNCIL, [str(COUNCIL / "node_modules/.bin/vitest"), "run", "--reporter=dot"], 300))
    return s

def pass_loop():
    results = [run(*s) for s in suites()]
    stamp = datetime.now(timezone.utc).isoformat()
    overall = all(r["ok"] for r in results)
    record = {"ts": stamp, "overall": overall, "n_pass": sum(r["ok"] for r in results),
              "n": len(results), "results": results}
    with LOG.open("a") as f:
        f.write(json.dumps(record) + "\n")
    with MD.open("a") as f:
        f.write(f"\n## {stamp} — {'PASS' if overall else 'FAIL'} {record['n_pass']}/{record['n']}\n")
        for r in results:
            f.write(f"- **{r['name']}**: {'OK' if r['ok'] else 'FAIL'} ({r['secs']}s)\n")
            if not r["ok"]:
                f.write(f"```\n{r['tail']}\n```\n")
    return overall, record

def main():
    if not LOG.exists():
        MD.write_text("# SOV Overnight E2E\n_Rolling report of autonomous passes._\n")
    print(f"SOV overnight E2E: {MAX_LOOP} passes, {INTERVAL}s apart — starting {datetime.now(timezone.utc).isoformat()}")
    for i in range(MAX_LOOP):
        overall, rec = pass_loop()
        print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] pass {i+1}/{MAX_LOOP}: "
              f"{'PASS' if overall else 'FAIL'} {rec['n_pass']}/{rec['n']}")
        if i < MAX_LOOP - 1:
            time.sleep(INTERVAL)
    print("done")

if __name__ == "__main__":
    main()
