#!/usr/bin/env python3
"""run_e2e_batch.py — auto-run the runnable-now e2e/selftest scripts, capture results.

Discovery + classification lives in BATCH_PLAN_2026-08-08.md. This runner:
- runs each script SERIALLY with a timeout via subprocess (python3 <file>)
- captures exit code, wall-time, and tail of output
- writes results to _batch/e2e_batch_results_<date>.jsonl + a markdown report
- marks INFRA-gated scripts as SKIP (not executed — no GPU/cloud/billing)

Usage:
    python3 _batch/run_e2e_batch.py              # run LOCAL+SELF scripts
    python3 _batch/run_e2e_batch.py --include-infra   # honest report incl. gated list
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

RUNTIME_PY = sys.executable or "python3"

# script -> (label, reason)
RUNNABLE: dict[str, tuple[str, str]] = {
    "sov_e2e.py": ("SELF", "pure --selftest path, no network"),
    "self_test_5bench.py": ("SELF", "deterministic 5-bench battery"),
    "test_provbench_three_outcomes.py": ("SELF", "unittest three-outcome contract"),
    "test_sov_runtime_alignment.py": ("SELF", "unittest of local sov modules"),
    "test_trust_layer.py": ("SELF", "stdlib-only regression unittest"),
    "spine_accuracy_test.py": ("LOCAL", "local math on govbench results"),
    "sov_master_scenarios.py": ("LOCAL", "data module, import no-op"),
}

# Compute-only scripts whose INPUT is a full multi-model benchmark run that isn't always
# present on disk. Not logic bugs — they report a clean "no data" exit 1 when input is absent.
DATA_GATED: dict[str, str] = {
    "diversity_e2e.py": "needs 15-dimension model scores in benchmark-results/govbench (not present this session)",
}

INFRA_GATED: dict[str, str] = {
    "e2e_continuous_loop.py": "orchestrates distill/train/arena + API_KEY",
    "e2e_routes_sovereign.py": "8-route E2E over ollama/HF + subprocess",
    "greenfield_e2e.py": "GovBench dims against local Ollama (11434)",
    "gspc_six_axis_e2e.py": "GOVBENCH_OLLAMA_URL/runpod/kaggle live pod",
    "overnight_e2e.py": "Kaggle/Modal/Cloudflare GPU orchestrator",
    "parity_e2e.py": "needs HF_TOKEN+KAGGLE creds, checks HF/Kaggle",
    "sov_e2e_overnight.py": "full overnight pipeline + HTTP :8766 server",
    "sov_master_run.py": "parallel swarm against live H100 forest (11434)",
    "sov_pipeline.py": "trains GNN + POST to localhost:8080",
    "sovspace_e2e.py": "Hermes service + cloud APIs, remote path",
    "sov_sovereign_test.py": "NVIDIA_API_KEY + urllib, runs on Oracle",
    "bloodline_test.py": "pod calls (11434/runpod/HF)",
    "bloodline_test_v2.py": "pod calls (11434/runpod), 5s backoff",
    "refusal_axis_test.py": "GOVBENCH_OLLAMA_URL/Ollama/RunPod",
    "honey_pipeline.py": "--full harvests from live Ollama models",
    "unified_free_pipeline.py": "Ollama+Kaggle+Oracle+Cloudflare+ssh",
}


def run_one(script: str, timeout_s: int) -> dict:
    t0 = time.time()
    try:
        proc = subprocess.run(
            [RUNTIME_PY, script],
            cwd=HERE, capture_output=True, text=True, timeout=timeout_s,
        )
        ok = proc.returncode == 0
        tail = (proc.stdout + proc.stderr).strip().splitlines()[-15:]
        tail = "\n".join(tail) if tail else "(no output)"
        return {
            "script": script, "ok": ok, "exit": proc.returncode,
            "wall_s": round(time.time() - t0, 2),
            "status": "PASS" if ok else "FAIL",
            "tail": tail[:2000],
        }
    except subprocess.TimeoutExpired:
        return {"script": script, "ok": False, "exit": "TIMEOUT",
                "wall_s": round(time.time() - t0, 2), "status": "TIMEOUT",
                "tail": f"exceeded {timeout_s}s timeout"}
    except Exception as e:  # noqa: BLE001
        return {"script": script, "ok": False, "exit": "ERR",
                "wall_s": round(time.time() - t0, 2), "status": "ERROR",
                "tail": str(e)[:500]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-infra", action="store_true",
                    help="append the infra-gated list to the report as SKIP (not executed)")
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    out_jsonl = HERE / "_batch" / f"e2e_batch_results_{stamp}.jsonl"
    out_md = HERE / "_batch" / f"e2e_batch_report_{stamp}.md"
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)

    print(f"Batch runner — {RUNTIME_PY} — timeout {args.timeout}s/script")
    results = []
    for script, (label, reason) in RUNNABLE.items():
        print(f"  · {script} [{label}] ...", flush=True)
        r = run_one(script, args.timeout)
        r["label"], r["reason"] = label, reason
        results.append(r)
        print(f"      -> {r['status']} in {r['wall_s']}s (exit {r['exit']})")

    # Persist JSONL
    with out_jsonl.open("a") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    # Markdown report
    passed = [r for r in results if r["status"] == "PASS"]
    failed = [r for r in results if r["status"] != "PASS"]
    lines = [
        f"# e2e BATCH REPORT — {stamp}",
        "",
        f"**Ran:** {len(results)} scripts · **PASS:** {len(passed)} · **FAIL/TIMEOUT/ERR:** {len(failed)} · "
        f"total wall {round(sum(r['wall_s'] for r in results),1)}s",
        "",
        "## Passed",
    ]
    for r in passed:
        lines.append(f"- {r['script']} [{r['label']}] — {r['wall_s']}s")
    lines.append("\n## Failed / hung")
    if not failed:
        lines.append("- (none)")
    for r in failed:
        lines.append(f"- {r['script']} [{r['label']}] — {r['status']} ({r['exit']})")
        lines.append("```")
        lines.append(r["tail"])
        lines.append("```")
    if args.include_infra:
        lines.append("\n## Infra-gated (SKIP, not executed — need GPU/cloud/billing)")
        for script, reason in INFRA_GATED.items():
            lines.append(f"- {script}: {reason}")
    if DATA_GATED:
        lines.append("\n## Data-gated (no logic bug; input run absent this session)")
        for script, reason in DATA_GATED.items():
            lines.append(f"- {script}: {reason}")
    lines.append("")
    lines.append(f"_Generated by _batch/run_e2e_batch.py · {stamp}_")
    out_md.write_text("\n".join(lines))

    print(f"\nWrote {out_jsonl.name}")
    print(f"Wrote {out_md.name}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
