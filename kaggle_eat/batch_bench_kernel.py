#!/usr/bin/env python3
"""batch_bench_kernel.py — benchmark MANY drawings in ONE free-GPU session.

═══════════════════════════════════════════════════════════════════════════════
WHY BATCHING IS THE WHOLE POINT
═══════════════════════════════════════════════════════════════════════════════
Measured today: an expert costs **16 KB** and composition is **monotonic**, so the flywheel is
limited by BENCHMARK THROUGHPUT. N free sites remove that limit — but only if used correctly.

    one GovBench run = ~93 model calls
    on GPU  ≈ 2-4 min       on Mac CPU (0.5B) ≈ 25-40 min       on Mac CPU (3B) ≈ 2.5+ HOURS

**Session startup dominates.** A Kaggle kernel spends ~4-6 min booting, installing and pulling
weights before the first call. Benchmarking ONE model per session spends more time on overhead
than on measurement:

    1 model/session   : ~6 min overhead + 3 min work  =  33% useful
    20 models/session : ~6 min overhead + 60 min work =  91% useful

And because every drawing shares ONE 397MB blob, the weights are pulled ONCE and reused by all
20. That is not an optimisation detail — it is why batching is possible at all here and would not
be for 20 genuinely different models.

    Kaggle 30 GPU-h/week ÷ ~66 min/batch ≈ 27 batches ≈ **540 drawings/week from one site.**

═══════════════════════════════════════════════════════════════════════════════
HONEST LIMITS — state these before anyone plans on 540/week
═══════════════════════════════════════════════════════════════════════════════
1. **Kaggle's GPU lottery**: free tier gives T4 (sm_75, torch fine) OR P100 (sm_60, torch often
   INCOMPATIBLE). This kernel probes and falls back to CPU rather than crashing — a crashed
   session wastes the whole quota block, which is the expensive failure here.
2. **Diminishing returns are guaranteed.** Drawings are prompt variants over one base; the first
   ones aimed at a weak dimension help most. Measured today: 1 of 3 aimed drawings raised the
   ceiling. Expect that hit-rate to FALL as the easy dimensions saturate. 540 drawings/week does
   not mean 540 improvements/week — it means 540 measurements, most of which will be inert.
3. **Inert is not free at scale.** Each miss costs 16 KB and a benchmark slot. The slot is the
   scarce thing, which is exactly why `sov_space_draw` aims rather than randomises.
4. **This does not touch the >8B tier.** Free GPU still tops out at QLoRA ~8B. Batching buys
   throughput on the substrate we have; it does not raise the ceiling on model size.

    kaggle kernels push -p .   # after writing kernel-metadata.json
"""
from __future__ import annotations

import json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path("./out")
OUT.mkdir(parents=True, exist_ok=True)


def gpu_probe() -> dict:
    """Kaggle's free tier is a lottery: T4 (sm_75) or P100 (sm_60). A P100 breaks many torch
    builds. Probe and degrade — never crash, because a crashed session burns the quota block."""
    info = {"gpu": None, "sm": None, "torch_ok": False}
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name,compute_cap",
                            "--format=csv,noheader"], capture_output=True, text=True, timeout=30)
        if r.returncode == 0 and r.stdout.strip():
            name, cap = [x.strip() for x in r.stdout.strip().split("\n")[0].split(",")]
            info["gpu"], info["sm"] = name, cap
            try:
                import torch
                info["torch_ok"] = torch.cuda.is_available()
                if info["torch_ok"]:
                    torch.zeros(8, device="cuda").sum().item()   # prove a kernel actually runs
            except Exception as e:
                info["torch_error"] = str(e)[:120]
                info["torch_ok"] = False
    except Exception as e:
        info["probe_error"] = str(e)[:120]
    return info


def run_batch(models: list[str], dims_module="govbench_eval") -> dict:
    """Benchmark every model in one session. A failure on one model must not kill the batch —
    losing 19 results because the 3rd model errored is the worst outcome available."""
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    results, failed = [], []
    t0 = time.time()
    try:
        import govbench_eval as G
    except Exception as e:
        return {"fatal": f"cannot import govbench_eval: {e}"}

    for i, m in enumerate(models, 1):
        t = time.time()
        try:
            r = G.evaluate_model(m, "ollama")
            results.append(r)
            print(f"  [{i}/{len(models)}] {m:28s} {r['overall_score']:5.1f}%  "
                  f"({time.time()-t:.0f}s)", flush=True)
        except Exception as e:
            # UnreachableModel included: no result is written, so it stays pending for the
            # next batch rather than entering the routing table on a failed measurement.
            failed.append({"model": m, "error": str(e)[:140]})
            print(f"  [{i}/{len(models)}] {m:28s} FAILED — {str(e)[:60]}", flush=True)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gpu": gpu_probe(),
        "requested": len(models), "measured": len(results), "failed": len(failed),
        "elapsed_s": round(time.time() - t0, 1),
        "per_model_s": round((time.time() - t0) / max(1, len(results)), 1),
        "results": results, "failures": failed,
        "note": "Failures write NO result file — they stay pending, never entering the "
                "routing table on an unmeasured basis.",
    }
    (OUT / "batch_bench_report.json").write_text(json.dumps(report, indent=2))
    print(f"\n  {len(results)} measured · {len(failed)} failed · "
          f"{report['elapsed_s']:.0f}s total · {report['per_model_s']:.0f}s/model")
    print(f"  -> {OUT/'batch_bench_report.json'}")
    return report


if __name__ == "__main__":
    models = sys.argv[1:]
    if not models:
        try:
            out = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30).stdout
            models = [l.split()[0] for l in out.splitlines()[1:] if l.strip()]
        except Exception:
            models = []
    if not models:
        print("  no models given and ollama unavailable"); sys.exit(2)
    print(f"  BATCH BENCH — {len(models)} models in one session")
    print(f"  gpu: {json.dumps(gpu_probe())}\n")
    run_batch(models)
