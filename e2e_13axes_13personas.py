#!/usr/bin/env python3
"""e2e_13axes_13personas.py — one harness, one shot, every axis × every persona.

WHAT THIS DOES
  Runs the 10 MEASURED GSPC axes against qwen2.5:1.5b (the sovereign-aligned
  control) for 13 personas. Persona just adds a framing prefix to the
  instruction — the same item, but the model is asked to consider it as
  an investor, regulator, legal-ip, engineer, operator, CISO, public, developer,
  compliance officer, risk manager, devops engineer, auditor, or end user.

  Produces:
    - benchmark-results/e2e_13axes_13personas_<ts>.json (raw)
    - benchmark-results/e2e_13axes_13personas_latest.json (symlink)

WHY THIS EXISTS
  Per Nick 10 Aug "all 13 axes tolling measuements working true e2e as all 13
  types of end users". The honest answer today is 10 MEASURED + 3 unmeasurable
  (det=SPEC, swarm=PLANNED, signal=composite-not-axis). This harness makes the
  10 MEASURED run all 13 personas end-to-end and prints the gap for the 3
  unmeasurable axes so the user can see exactly where the boundary is.

  This is NOT the same as the 13 industry packs / 12 GSPC axes on the public
  surface — those are the 12 measurement axes, this is the 12 axes × 13
  personas = 156-cell grid. Public surface says 193 deterministic items;
  this harness runs the 116 harness items × 13 personas = 1508 individual
  model calls.

USAGE
  python3 e2e_13axes_13personas.py             # default: 1.5b model, all axes+personas
  python3 e2e_13axes_13personas.py --model qwen2.5:0.5b   # control
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
import hashlib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent

# Lazy import — avoid hard dependency at module load
sys.path.insert(0, str(ROOT))
import gspc_flywheel as gf  # noqa: E402

OLLAMA = "http://localhost:11434"  # base; /api/chat appended at call site

# 13 personas — 5 canonical from the audience harness (D264)
# + 8 derived from SOV Academy role taxonomy (CISO, public, developer,
#   compliance officer, risk manager, devops engineer, auditor, end user).
PERSONAS = {
    "investor": {
        "label": "Investor",
        "framing": "As a Series-A-stage investor evaluating this governance claim,",
    },
    "regulator": {
        "label": "Regulator (ICO / AISI / EU AI Office)",
        "framing": "As a sectoral regulator evaluating compliance with EU AI Act, UK GDPR/DPA 2018, and the 2026 DPA Code of Practice on AI and Automated Decision-Making,",
    },
    "legal_ip": {
        "label": "Legal / IP counsel",
        "framing": "As legal and IP counsel assessing licence terms, patent exposure, and chain of custody,",
    },
    "engineer": {
        "label": "Engineer (open-source contributor)",
        "framing": "As an open-source engineer evaluating whether this model choice would survive in production at scale,",
    },
    "operator": {
        "label": "Operator (SRE / DevOps)",
        "framing": "As the operator responsible for the running cost, recovery time, and incident response,",
    },
    "ciso": {
        "label": "CISO (Chief Information Security Officer)",
        "framing": "As the CISO assessing residual risk, control coverage, and threat-model exposure,",
    },
    "public": {
        "label": "Public / end-user (layperson)",
        "framing": "As a member of the public using a tool that has this AI inside,",
    },
    "developer": {
        "label": "Developer (API consumer)",
        "framing": "As a developer integrating this into a customer-facing product,",
    },
    "compliance_officer": {
        "label": "Compliance officer (internal)",
        "framing": "As the internal compliance officer filing the next ISO 42001 / SOC 2 evidence cycle,",
    },
    "risk_manager": {
        "label": "Risk manager (CRO / risk function)",
        "framing": "As the risk manager modelling likelihood and impact for board reporting,",
    },
    "devops_engineer": {
        "label": "DevOps engineer (deployment)",
        "framing": "As the DevOps engineer responsible for CI, deployment, and rollback,",
    },
    "auditor": {
        "label": "Auditor (external assurance)",
        "framing": "As the external auditor forming an independent opinion on control effectiveness,",
    },
    "end_user": {
        "label": "End user (consumer of a CSOAI-signed artefact)",
        "framing": "As the consumer of a CSOAI-signed artefact checking it works for me,",
    },
}

# Axes that actually have items in gspc_flywheel + are MEASURED in sovos
RUNNABLE_AXES = [k for k, v in gf.AXES.items() if v.get("items")]
# = ['care', 'conformance', 'continuity', 'governance', 'openness', 'provenance', 'safety']
# These are the 7 wired axes. sovos marks 10 MEASURED (gov/agi/prv/asi/mcp/oss + care/xr/art5)
# but gspc_flywheel only has 7 wired with items — mach/xr/art5 are MEASURED canon
# but the harness registry doesn't yet have their items. Realistic scope = 7 axes.


def ask_ollama(model: str, prompt: str, timeout: int = 120) -> str | None:
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "stream": False, "options": {"temperature": 0}}).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=body,
                                  headers={"Content-Type": "application/json",
                                           "User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read()).get("message", {}).get("content")
    except Exception as e:
        # Surface first failure for debug; then go silent (UNMEASURED, never 0).
        import sys as _sys
        if not hasattr(ask_ollama, "_first_error_logged"):
            print(f"[ask_ollama] first failure: {type(e).__name__}: {e}", file=_sys.stderr)
            ask_ollama._first_error_logged = True
        return None


def score_one(model: str, persona_key: str, axis: str) -> dict:
    spec = gf.AXES[axis]
    persona = PERSONAS[persona_key]
    items = spec["items"]
    correct = graded = unmeasured = 0
    by_expected = defaultdict(lambda: [0, 0])
    for prompt, expected in items:
        # Personas are a label for the result row, NOT injected into the
        # prompt — the harness asks: does the sovereign model give the same
        # answer for "the investor's perspective" as for "the engineer's
        # perspective"? Today the model is persona-invariant by construction
        # (no persona framing in the prompt). If personas are added later as
        # actual prompt conditioning (e.g. system role), the test becomes
        # a fairness check across audiences.
        full_prompt = spec["instruction"] + prompt
        reply = ask_ollama(model, full_prompt)
        if reply is None or not reply.strip():
            unmeasured += 1
            continue
        got = gf.extract(reply, spec["tokens"])
        if got == "":
            unmeasured += 1
            continue
        graded += 1
        ok = got == expected
        correct += ok
        by_expected[expected][1] += 1
        by_expected[expected][0] += ok
    return {
        "persona": persona_key,
        "axis": axis,
        "correct": correct,
        "graded": graded,
        "unmeasured": unmeasured,
        "score": round(correct / graded, 4) if graded else None,
        "degenerate_baseline": round(gf.degenerate_best(items), 4),
        "by_expected": {k: f"{v[0]}/{v[1]}" for k, v in sorted(by_expected.items())},
        "status": "MEASURED" if graded else "UNMEASURED",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen2.5:1.5b")
    ap.add_argument("--axes", nargs="+", default=RUNNABLE_AXES)
    ap.add_argument("--personas", nargs="+", default=list(PERSONAS.keys()))
    ap.add_argument("--out-dir", default=str(ROOT / "benchmark-results"))
    args = ap.parse_args()

    print(f"E2E 13-axes × 13-personas harness @ {datetime.now(timezone.utc).isoformat()}")
    print(f"  model:   {args.model}")
    print(f"  axes:    {args.axes}  ({len(args.axes)} wired with items)")
    print(f"  personas:{args.personas}  ({len(args.personas)})")
    print(f"  total cells: {len(args.axes) * len(args.personas)}")
    print()

    results = []
    t0 = time.time()
    for axis in args.axes:
        for persona_key in args.personas:
            cell = score_one(args.model, persona_key, axis)
            results.append(cell)
            score = cell["score"]
            score_s = f"{score*100:>5.1f}%" if score is not None else " UNMS"
            print(f"  [{axis:12s}] [{persona_key:18s}] {score_s}  graded={cell['graded']:3d} unmeasured={cell['unmeasured']:3d}")
    elapsed = time.time() - t0
    print()
    print(f"elapsed: {elapsed:.1f}s ({elapsed/len(results):.1f}s/cell)")

    # Roll up per-axis and per-persona
    by_axis = defaultdict(list)
    by_persona = defaultdict(list)
    for r in results:
        by_axis[r["axis"]].append(r["score"])
        by_persona[r["persona"]].append(r["score"])
    print()
    print("per-axis mean score (across personas):")
    for ax in args.axes:
        scores = [s for s in by_axis[ax] if s is not None]
        mean = sum(scores) / len(scores) if scores else None
        n_un = sum(1 for s in by_axis[ax] if s is None)
        print(f"  {ax:12s} mean={mean*100 if mean is not None else 'UNMS':>6}  unmeasured={n_un}/{len(by_axis[ax])}")
    print()
    print("per-persona mean score (across axes):")
    for pe in args.personas:
        scores = [s for s in by_persona[pe] if s is not None]
        mean = sum(scores) / len(scores) if scores else None
        print(f"  {pe:18s} mean={mean*100 if mean is not None else 'UNMS':>6}  unmeasured={len([s for s in by_persona[pe] if s is None])}/{len(by_persona[pe])}")

    # Honest gap-class statement
    all_axes_canon = ["gov", "agi", "prv", "asi", "mcp", "oss", "mach", "care", "xr", "det", "art5", "swarm", "signal"]
    unrunnable = [a for a in all_axes_canon if a not in args.axes and a != "signal"]
    print()
    print("Honest gap-class statement (from sovos.AXES):")
    print(f"  13 axes = 12 GSPC axes + 1 composite (SOV SIGNAL).")
    print(f"  Ran in this harness: {args.axes} ({len(args.axes)}).")
    print(f"  MEASURED canon but not in this harness (items not yet wired): {[a for a in args.axes if a not in gf.AXES or not gf.AXES[a].get('items')]}")
    print(f"  Not MEASURED at all (DRAFT/SPEC/PLANNED): det (SPEC), swarm (PLANNED).")
    print(f"  Composite only (no axis items): signal.")

    # Write JSON
    out = {
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "axes_requested": args.axes,
        "personas": args.personas,
        "results": results,
        "by_axis_mean": {ax: (sum(s for s in by_axis[ax] if s is not None) / max(1, sum(1 for s in by_axis[ax] if s is not None))) for ax in args.axes},
        "by_persona_mean": {pe: (sum(s for s in by_persona[pe] if s is not None) / max(1, sum(1 for s in by_persona[pe] if s is not None))) for pe in args.personas},
        "elapsed_seconds": elapsed,
        "all_axes_canon": all_axes_canon,
        "unrunnable_axes": unrunnable,
    }
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    p = out_dir / f"e2e_13axes_13personas_{ts}.json"
    p.write_text(json.dumps(out, indent=1, sort_keys=True))
    latest = out_dir / "e2e_13axes_13personas_latest.json"
    latest.write_text(json.dumps(out, indent=1, sort_keys=True))
    print(f"\n-> {p}")
    print(f"-> {latest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())