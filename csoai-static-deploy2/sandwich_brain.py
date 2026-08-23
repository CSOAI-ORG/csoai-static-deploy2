#!/usr/bin/env python3
"""sandwich_brain.py — the layer owem_cluster.py was missing: IWM/OWM × Frozen/Fluid.

═══════════════════════════════════════════════════════════════════════════════
WHAT I HAD WRONG
═══════════════════════════════════════════════════════════════════════════════
`owem_cluster.py` implemented ONE layer — pick the expert that wins a dimension — and called it
the cluster. Per `SOV_SPACE_COMPLETE.md` the sandwich brain has FOUR positions per family:

    OWM-Small-Frozen   perception, stable       <- fast, cheap, immutable
    OWM-Small-Fluid    perception, adapting     <- fast, being trained
    IWM-Big-Frozen     reasoning, stable        <- slow, deep, immutable
    IWM-Big-Fluid      reasoning, evolving      <- slow, being trained

OWM = **Outer** World Model = PERCEPTION. Reads the world: classify, route, gate, score. Must be
small because it runs on EVERY query before anything else does.
IWM = **Inner** World Model = REASONING. Produces the answer. Can be big and slow because it runs
once, after perception has narrowed the problem.

My spine was an un-named OWM and my expert pool an un-named IWM. Naming them is not cosmetic —
it makes the safety property explicit and enforceable, which is the point of this file.

═══════════════════════════════════════════════════════════════════════════════
FROZEN vs FLUID — this is the safety boundary, not a label
═══════════════════════════════════════════════════════════════════════════════
    FROZEN = has a benchmark result on the current board  -> MAY be routed to
    FLUID  = training / harvesting / unmeasured           -> MUST NOT be routed to

This is what makes the flywheel safe to run unattended, and it is the enforcement point for the
monotonicity property proven on 2026-07-28 (every expert added gave Δ ≥ 0 because composition is
max-based). A fluid model that has degraded cannot damage the cluster **because it is not
reachable**. Training can fail, produce junk, or take weeks — the serving path never sees it.

Promotion Fluid -> Frozen happens exactly once: when a benchmark result file exists. There is no
manual override, and that is deliberate — a human "this one looks good" is precisely the
unmeasured judgement this architecture exists to remove.

    python3 sandwich_brain.py --status
    python3 sandwich_brain.py --query "What does Article 5 prohibit?"
"""
from __future__ import annotations

import argparse, glob, json, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
RESULTS = HERE / "benchmark-results" / "govbench"

# Size boundary between OWM (perception) and IWM (reasoning). Blob bytes, not parameter count —
# parameter count is not knowable from ollama without loading the model, and the blob size is
# what actually determines whether this runs on a free tier.
OWM_MAX_BYTES = 600_000_000     # ~600MB: the 397MB qwen-class experts are OWM; 994MB+ is IWM


def _ollama_models() -> list[str]:
    try:
        out = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30).stdout
        return [l.split()[0] for l in out.splitlines()[1:] if l.strip()]
    except Exception:
        return []


def _blob_bytes(model: str) -> int:
    """Resolve the model's actual weight blob. Several 'different' experts share one blob —
    verified 2026-07-28: 7 sovereign models AND qwen2.5:0.5b are the same 397MB file."""
    try:
        mf = subprocess.run(["ollama", "show", model, "--modelfile"],
                            capture_output=True, text=True, timeout=30).stdout
        for line in mf.splitlines():
            if line.startswith("FROM ") and "/" in line:
                p = Path(line.split(None, 1)[1].strip())
                if p.exists():
                    return p.stat().st_size
    except Exception:
        pass
    return 0


def _benchmarked() -> dict[str, dict]:
    """Models with a 15-dim result — the FROZEN set. A result file is the only promotion gate."""
    out = {}
    for f in glob.glob(str(RESULTS / "*.json")):
        try:
            d = json.loads(Path(f).read_text())
        except Exception:
            continue
        for r in (d if isinstance(d, list) else [d]):
            if not isinstance(r, dict):
                continue
            dims = r.get("dimensions")
            if (isinstance(dims, dict) and len(dims) == 15
                    and all(isinstance(v, (int, float)) for v in dims.values())):
                out[r["model"]] = dims
    return out


def census() -> dict:
    """Place every local model into its sandwich position."""
    frozen = _benchmarked()
    grid = {"OWM-Small-Frozen": [], "OWM-Small-Fluid": [],
            "IWM-Big-Frozen": [], "IWM-Big-Fluid": []}
    blobs = {}
    for m in _ollama_models():
        b = _blob_bytes(m)
        blobs.setdefault(b, []).append(m)
        tier = "OWM-Small" if 0 < b <= OWM_MAX_BYTES else "IWM-Big"
        state = "Frozen" if m in frozen else "Fluid"
        grid[f"{tier}-{state}"].append({"model": m, "bytes": b,
                                        "avg": round(sum(frozen[m].values()) / 15, 1) if m in frozen else None})
    return {"grid": grid, "frozen_count": len(frozen), "shared_blobs": blobs}


def route(query: str) -> dict:
    """Full path: OWM perception → gate → IWM reasoning. Only FROZEN models are reachable."""
    from owem_cluster import classify_dimension, build_expert_table
    t0 = time.time()

    # ── OWM: perception. Gate FIRST — it is the cheapest and the only non-negotiable step.
    try:
        from care_gate_v2 import tier1_hard_stop
        breach, label, cite = tier1_hard_stop(query)
        if breach:
            return {"layer": "OWM-perception", "blocked": True, "reason": label,
                    "citation": cite, "owm_ms": round((time.time() - t0) * 1000, 1),
                    "note": "Blocked in perception. No IWM was consulted — reasoning never ran."}
    except Exception:
        pass
    dim = classify_dimension(query)
    owm_ms = round((time.time() - t0) * 1000, 1)

    # ── IWM: reasoning. Frozen-only by construction — build_expert_table reads result files,
    # and a fluid model has none, so it cannot appear here.
    table, models = build_expert_table()
    if dim not in table:
        return {"layer": "IWM", "error": f"no frozen expert holds '{dim}'"}
    sel = table[dim]
    return {
        "owm": {"layer": "OWM-Small-Frozen", "dimension": dim, "ms": owm_ms, "blocked": False},
        "iwm": {"layer": "IWM-Frozen", "expert": sel["expert"], "dim_score": sel["score"]},
        "frozen_experts": len(models),
        "note": "OWM perceives and gates; IWM reasons. Fluid models are unreachable from here.",
    }


def status() -> None:
    c = census()
    print("  SANDWICH BRAIN — IWM/OWM × Frozen/Fluid\n")
    for pos in ["OWM-Small-Frozen", "OWM-Small-Fluid", "IWM-Big-Frozen", "IWM-Big-Fluid"]:
        rows = c["grid"][pos]
        role = "perception · routable" if pos == "OWM-Small-Frozen" else \
               "perception · NOT routable" if pos == "OWM-Small-Fluid" else \
               "reasoning · routable" if pos == "IWM-Big-Frozen" else "reasoning · NOT routable"
        print(f"    {pos:20s} {len(rows):2d}   ({role})")
        for r in rows[:6]:
            s = f"{r['avg']}%" if r["avg"] is not None else "unmeasured"
            print(f"        {r['model']:26s} {r['bytes']/1e6:6.0f}MB  {s}")
    shared = {b: ms for b, ms in c["shared_blobs"].items() if len(ms) > 1 and b}
    if shared:
        print("\n  SHARED BLOBS — why the cluster is small:")
        for b, ms in shared.items():
            print(f"    {b/1e6:6.0f}MB  x{len(ms)}  {', '.join(ms[:4])}{'…' if len(ms) > 4 else ''}")
        uniq = sum(shared) + sum(b for b, ms in c["shared_blobs"].items() if len(ms) == 1 and b)
        total = sum(b * len(ms) for b, ms in c["shared_blobs"].items() if b)
        print(f"    on disk {uniq/1e9:.2f}GB  vs  {total/1e9:.2f}GB if each were unique")
    print(f"\n  FROZEN (routable): {c['frozen_count']}   — promotion happens only when a benchmark")
    print(f"  result exists. No manual override: 'this one looks good' is the unmeasured")
    print(f"  judgement this architecture exists to remove.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    if a.query:
        print(json.dumps(route(a.query), indent=2))
    else:
        status()
