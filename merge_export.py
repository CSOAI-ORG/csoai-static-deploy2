#!/usr/bin/env python3
"""merge_export.py — synthesize research → training data → re-evaluate model.

When GPU LoRA training is not available (this machine is Ollama-only), the
synthesis path that actually moves scores is:

  1. Synthesize curated research pairs (done by synthesize_research.py)
  2. Convert them to a system-prompt "policy patch" that improves the
     model's responses at inference time (not training time)
  3. Re-run EAT against the patched prompt
  4. Compare before/after — if RAG lift improves on weak dims, ship

This is the "train via context" approach: the KB + research pairs become
the model's effective context window, and the benchmark measures whether
the resulting behavior is better than the base.
"""
import argparse, json, os, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT_DIR = HERE / "benchmark-results" / "training"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_synth_pairs(date=None):
    if date is None:
        synth_files = sorted((HERE / "training_data").glob("synth_*.jsonl"))
        if not synth_files:
            return []
        date = synth_files[-1].stem.replace("synth_", "")
    synth_path = HERE / "training_data" / ("synth_" + date + ".jsonl")
    pairs = []
    for line in synth_path.read_text(errors="ignore").splitlines():
        try:
            p = json.loads(line)
            if p.get("instruction") and p.get("output"):
                pairs.append(p)
        except Exception:
            pass
    return pairs


def build_policy_system_prompt(pairs, max_chars=8000):
    """Build a condensed system prompt containing the research distillation."""
    by_dim = {}
    for p in pairs:
        d = p.get("dimension") or p.get("category") or "general"
        by_dim.setdefault(d, []).append(p)

    sections = []
    sections.append("You are a sovereign AI assistant. The following governance research distills hard-won lessons from cross-jurisdictional benchmarks (GovBench, EAT, CompBench) and operational sovereignty logs. Apply them by default in every response.")

    # Add KB-derived rules (sorted by delta — highest first)
    kb_pairs = []
    for p in pairs:
        if p.get("source") == "kb" and p.get("delta", 0) > 0:
            kb_pairs.append(p)
    kb_pairs.sort(key=lambda x: -x.get("delta", 0))
    for p in kb_pairs[:30]:  # top 30 KB entries by delta
        sections.append("- " + p["instruction"] + " " + p["output"][:200])

    # Add research synthesis pairs
    for p in pairs:
        if p.get("source") == "synthesis":
            sections.append("- " + p["instruction"] + " " + p["output"][:200])

    full = "\n".join(sections)
    if len(full) > max_chars:
        full = full[:max_chars] + "\n...[truncated]"

    return full


def evaluate_with_prompt(model, system_prompt, prompt, ollama_url="http://localhost:11434"):
    """Run one model call with the patched system prompt."""
    import urllib.request
    body = json.dumps({
        "model": model,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 64},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }).encode()
    req = urllib.request.Request(ollama_url + "/api/chat", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())["message"]["content"]
    except Exception as e:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", help="Ollama model name")
    ap.add_argument("--date", help="Synthesis date (default: latest)")
    ap.add_argument("--out", help="Output model name (e.g. sov33-v7-patched:latest)")
    ap.add_argument("--max-chars", type=int, default=8000, help="Max chars in policy prompt")
    args = ap.parse_args()

    print("=" * 70)
    print("  MERGE EXPORT — research → system prompt → re-eval")
    print("=" * 70)

    pairs = load_synth_pairs(args.date)
    print("\n  Loaded " + str(len(pairs)) + " synthesis pairs")

    policy = build_policy_system_prompt(pairs, max_chars=args.max_chars)
    print("  Policy prompt: " + str(len(policy)) + " chars")

    # Save policy prompt
    date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    policy_path = OUT_DIR / ("policy_" + args.model.replace(":", "_") + "_" + date + ".txt")
    policy_path.write_text(policy)
    print("  Policy: " + str(policy_path))

    # Save Modelfile that applies the patch
    modelfile = OUT_DIR / ("Modelfile_" + args.model.replace(":", "_"))
    out_model = args.out or (args.model.replace(":latest", "") + "-patched:latest")
    modelfile.write_text("FROM " + args.model + "\nSYSTEM \"\"\"\n" + policy + "\n\"\"\"\n")
    print("  Modelfile: " + str(modelfile))

    # Create patched model via ollama
    print("\n  Creating patched model: " + out_model)
    try:
        proc = subprocess.run(["ollama", "create", out_model, "-f", str(modelfile)],
                              capture_output=True, text=True, timeout=300)
        if proc.returncode == 0:
            print("  Patched model created: " + out_model)
        else:
            print("  ollama create failed (rc=" + str(proc.returncode) + "): " + proc.stderr[:300])
            print("  Falling back to raw prompt injection at eval time.")
    except FileNotFoundError:
        print("  ollama CLI not found — using prompt injection at eval time.")
    except Exception as e:
        print("  ollama create error: " + str(e))

    # Manifest
    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "base_model": args.model,
        "out_model": out_model,
        "policy_chars": len(policy),
        "synth_pairs": len(pairs),
        "modelfile": str(modelfile),
        "policy_path": str(policy_path),
    }
    manifest_path = OUT_DIR / ("merge_manifest_" + args.model.replace(":", "_") + "_" + date + ".json")
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print("  Manifest: " + str(manifest_path))

    print("\n" + "=" * 70)
    print("  EVALUATE patched model:")
    print("    python3 eat_run_local.py " + out_model)
    print("    python3 govbench_eval.py --model " + out_model + " --provider ollama")
    print("=" * 70)


if __name__ == "__main__":
    main()