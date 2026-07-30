#!/usr/bin/env python3
"""batch_all.py — rebuild every SOV drawing on free GPU and benchmark them in ONE session.

Ships 17 Modelfiles (206 KB total) rather than 17 models, because every drawing is a system
prompt over the SAME public qwen2.5:0.5b blob. Kaggle pulls that blob ONCE and all 17 reuse it.
That is the entire reason a 17-model batch fits in one free session.

Session boot dominates, so batching is the point:
    1 model/session  =  33% useful
   17 model/session  = ~90% useful
"""
import json, os, subprocess, sys, time
from pathlib import Path

OUT = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path("./out")
OUT.mkdir(parents=True, exist_ok=True)
MF = Path("modelfiles")


def sh(c, t=900):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)


def gpu():
    r = sh("nvidia-smi --query-gpu=name,compute_cap --format=csv,noheader", 60)
    return r.stdout.strip().split("\n")[0] if r.returncode == 0 else "CPU-only"


print(f"  GPU: {gpu()}", flush=True)

# ollama is the runtime; the drawings are Modelfiles over one public base
print("  installing ollama…", flush=True)
sh("curl -fsSL https://ollama.com/install.sh | sh", 900)
srv = subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(8)

print("  pulling qwen2.5:0.5b (ONCE — all 17 drawings share it)…", flush=True)
r = sh("ollama pull qwen2.5:0.5b", 1800)
if r.returncode != 0:
    print(f"  FATAL: base pull failed — {r.stderr[:200]}")
    json.dump({"fatal": "base pull failed", "stderr": r.stderr[:400]},
              open(OUT / "batch_all_report.json", "w"), indent=2)
    sys.exit(1)

built = []
for f in sorted(MF.glob("*.modelfile")):
    name = f.stem.replace("_latest", "")
    if sh(f"ollama create {name} -f {f}", 300).returncode == 0:
        built.append(name)
print(f"  rebuilt {len(built)}/{len(list(MF.glob('*.modelfile')))} drawings\n", flush=True)

sys.path.insert(0, ".")
import govbench_eval as G

results, failed = [], []
t0 = time.time()
for i, m in enumerate(built, 1):
    t = time.time()
    try:
        res = G.evaluate_model(m, "ollama")
        results.append(res)
        print(f"  [{i}/{len(built)}] {m:34s} {res['overall_score']:5.1f}%  ({time.time()-t:.0f}s)", flush=True)
    except Exception as e:
        # A failed model writes NO result — it stays pending rather than entering the
        # routing table on an unmeasured basis. One failure must not lose the other 16.
        failed.append({"model": m, "error": str(e)[:140]})
        print(f"  [{i}/{len(built)}] {m:34s} FAILED — {str(e)[:60]}", flush=True)

report = {"gpu": gpu(), "requested": len(built), "measured": len(results), "failed": len(failed),
          "elapsed_s": round(time.time() - t0, 1),
          "per_model_s": round((time.time() - t0) / max(1, len(results)), 1),
          "results": results, "failures": failed}
(OUT / "batch_all_report.json").write_text(json.dumps(report, indent=2))
print(f"\n  {len(results)} measured · {len(failed)} failed · {report['elapsed_s']:.0f}s "
      f"· {report['per_model_s']:.0f}s/model")
srv.terminate()
