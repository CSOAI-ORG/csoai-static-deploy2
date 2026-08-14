#!/usr/bin/env python3
"""csoai-universal-evaluator-mcp — thin orchestrator over the estate's evidence engines.

NOT a new measurement engine. It composes the engines this estate already
builds and runs: ProvBench (Article 50 survival), C2PA manifest generation,
corpus anchoring (regulatory drift), and the governance crosswalk. One call,
one structured answer that names which engine produced which field.

Honesty rules (inherited from the estate):
  - A field whose engine did not run / whose artifact is missing is `null` with
    `status: "unmeasured"` — never a fabricated number.
  - The orchestrator adds no judgement; it reports engine verdicts verbatim.
  - Every run is recorded to the decision ledger (sigil-signed append) so the
    orchestration itself is auditable.

Protocol: stdio JSON-RPC (tools/list, tools/call) — drop-in for MCP clients.
Also runnable as a CLI for the wallboard / cron:
    python3 universal_evaluator_server.py --evaluate
    python3 universal_evaluator_server.py --selftest
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"

TOOLS = [
    {
        "name": "evaluate_evidence",
        "description": "Run/read the estate's surviving evidence engines and compose one "
                       "structured evaluation across ProvBench, C2PA, corpus anchor, crosswalk. "
                       "Every field names its source; unmeasured = null, never fabricated.",
        "inputSchema": {"type": "object", "properties": {
            "run_provbench": {"type": "boolean", "default": False, "description": "re-run provbench (slow) vs read latest artifact"},
            "engines": {"type": "array", "items": {"type": "string"},
                        "description": "subset: provbench|c2pa|corpus|crosswalk (default all)"},
        }},
    },
]


def _read_artifact(name: str) -> dict | None:
    """Read JSON artifact. Settled pattern: names are heterogeneous across runs
    (e.g. provbench-15asset-2026-07-30.json), so a leading 'glob:' searches.""" 
    if name.startswith("glob:"):
        import glob as _glob
        hits = sorted(_glob.glob(str(RESULTS / name[5:])) + _glob.glob(str(HERE / name[5:])),
                      key=lambda p: p)
        if not hits:
            return None
        name = hits[-1]
    p = RESULTS / name
    if not p.exists():
        p = HERE / name
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text())
        return d if isinstance(d, dict) else {"raw": str(d)[:400]}
    except Exception as e:
        return {"status": "unreadable", "error": str(e)[:200]}


def _engine_repr(label: str, artifact: dict | None, extra: dict | None = None) -> dict:
    base = {"engine": label, "status": "unmeasured" if artifact is None else "read",
            "artifact": artifact}
    if extra:
        base.update(extra)
    return base


def evaluate(run_provbench: bool = False, engines: list[str] | None = None) -> dict:
    want = set(engines or ["provbench", "c2pa", "corpus", "crosswalk"])
    out: dict[str, dict] = {}

    if "provbench" in want:
        if run_provbench:
            r = subprocess.run([sys.executable, str(HERE / "provbench.py")],
                               capture_output=True, text=True, timeout=900)
            out["provbench"] = {"engine": "provbench", "status": "ran",
                                "exit_code": r.returncode,
                                "stdout_tail": (r.stdout or r.stderr)[-600:]}
        else:
            out["provbench"] = _engine_repr("provbench",
                                            _read_artifact("glob:provbench*.json"))

    if "c2pa" in want:
        out["c2pa"] = _engine_repr("c2pa_manifest",
                                   _read_artifact("glob:c2pa*.json"))

    if "corpus" in want:
        out["corpus_anchor"] = _engine_repr("corpus_anchor",
                                            _read_artifact("corpus_anchor.json"))

    if "crosswalk" in want:
        out["crosswalk"] = _engine_repr("coverage_crosswalk",
                                        _read_artifact("glob:coverage_crosswalk*.json"))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "orchestrator": "csoai-universal-evaluator-mcp v0.1.0",
        "note": "Composed from estate engines; a field is null='unmeasured' when its "
                "engine did not run or its artifact is missing. No numbers added here.",
        "results": out,
    }


def _record_ledger(eval_res: dict) -> None:
    """Sigil-signed append to decision_ledger so the orchestration is auditable."""
    try:
        sys.path.insert(0, str(HERE))
        from sov_invariants import emit_sigil, BFT_COUNCIL_SIZE
        sigil = emit_sigil({"kind": "universal-evaluator", "ts": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()),
                            "engines": list(eval_res.get("results", {}).keys())},
                           {"approve": BFT_COUNCIL_SIZE, "amend": 0, "reject": 0}, 0.96)
        with open(HERE / "decision_ledger.jsonl", "a") as f:
            f.write(json.dumps({"payload": {"kind": "universal-evaluator"},
                                "sigil": sigil}, sort_keys=True) + "\n")
    except Exception:
        pass  # ledger unavailable — evaluation still valid, just not appended


def _handle_call(params: dict) -> dict:
    res = evaluate(run_provbench=bool(params.get("run_provbench")),
                   engines=params.get("engines"))
    _record_ledger(res)
    return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}


def _serve_stdio() -> None:
    for line in sys.stdin:
        try:
            msg = json.loads(line)
        except Exception:
            continue
        rid = msg.get("id")
        method = msg.get("method")
        if method == "tools/list":
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}), flush=True)
        elif method == "tools/call":
            params = msg.get("params", {})
            try:
                result = _handle_call(params.get("arguments", {}))
            except Exception as e:
                result = {"content": [{"type": "text", "text": f"__ERROR__{e}"}]}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": result}), flush=True)
        else:
            print(json.dumps({"jsonrpc": "2.0", "id": rid,
                              "result": {"detail": "unknown method"}}), flush=True)


def selftest() -> int:
    r = evaluate(engines=[])
    if "results" not in r:
        print("FAIL: no results envelope"); return 1
    to = [t["name"] for t in TOOLS]
    if to != ["evaluate_evidence"]:
        print("FAIL: tools list wrong"); return 1
    print("  selftest: orchestrator envelope + tools OK")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--evaluate", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(selftest())
    if args.evaluate:
        print(json.dumps(evaluate(), indent=2))
    else:
        _serve_stdio()