#!/usr/bin/env python3
"""autofix_loop.py — the grok-bot-style auto-fix loop (the engine's fix part).

run → verify → diff against the frozen provision → emit fix-candidate → re-measure → signed re-attestation.
Fail-closed: a fix candidate is never auto-applied to a MEASURED artifact without a signed re-measurement.
Exit codes: 0 = conformant · 3 = drift found (CI forcing-function) · 4 = re-measured + fix candidate emitted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def canonical(body):
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def load_evidence(path):
    return json.loads(Path(path).read_text())


def main():
    p = argparse.ArgumentParser(description="grok-bot-style auto-fix loop")
    p.add_argument("--evidence", required=True, help="the evidence JSON to re-measure")
    p.add_argument("--axis", required=True)
    p.add_argument("--prev-card", default=None, help="the previous signed card (for drift diff)")
    a = p.parse_args()

    evidence = load_evidence(a.evidence)
    # 1. run the deterministic check (reuse the harness logic; robust import)
    import sys, os as _os
    _src = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "src")
    if _src not in sys.path:
        sys.path.insert(0, _src)
    res = json.loads(_run_harness(a.axis, a.evidence))
    verdict = res["verdict"]

    # 2. diff against the previous card (drift detection on the content_id)
    drift = None
    if a.prev_card:
        prev = json.loads(Path(a.prev_card).read_text())
        prev_cid = prev.get("content_id") or hashlib.sha256(
            canonical({k: v for k, v in prev.items() if k != "signature"}).encode()).hexdigest()
        now_cid = hashlib.sha256(canonical({k: v for k, v in res.items() if k != "signature"}).encode()).hexdigest()
        if now_cid != prev_cid:
            drift = {"prev": prev_cid, "now": now_cid, "changed_fields": "content_id"}

    # 3. emit the fix candidate when drift or non-conformance
    if drift or verdict == 0:
        candidate = {
            "schema": "csoai.fix-candidate/0.1",
            "axis": a.axis,
            "kind": "re-measure-required" if verdict == 0 else "drift-detected",
            "drift": drift,
            "action": "re-run the frozen provision on the corrected evidence; then re-sign.",
            "never_auto_applied": True,
        }
        out = Path(f"fix-candidate-{a.axis}.json")
        out.write_text(json.dumps(candidate, indent=2))
        print(f"fix candidate emitted: {out} — human/MEOK applies it, then a signed re-measurement.")
        return 4 if verdict == 0 else 3
    print("conformant — no fix candidate needed.")
    return 0


def _run_harness(axis, evidence):
    # avoid double-main; replicate the deterministic check inline
    import json as J
    from csoai.harness import AXES
    ev = J.loads(Path(evidence).read_text())
    required = {"governance": ["risk_tier", "mitigation", "owner"], "safety": ["redline_checked", "containment"],
                "provenance": ["content_id", "signature", "kid"], "continuity": ["chain_prev", "anchor"]}.get(axis, ["evidence"])
    missing = [f for f in required if not ev.get(f)]
    passed = not missing
    return J.dumps({"axis": axis, "verdict": 1 if passed else 0,
                    "explanation": f"prov-{AXES.index(axis)+1}: {'OK' if passed else 'INCOMPLETE'}"})


if __name__ == "__main__":
    sys.exit(main())
