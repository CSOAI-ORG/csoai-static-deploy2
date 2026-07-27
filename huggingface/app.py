"""
app.py — Gradio UI for SOV33 Benchmark Runner (HF Space).

Run locally:
  HF_TOKEN=... gradio app.py

Or as a Space: see space_README.md for SDK config.
"""
from __future__ import annotations
import os, json, sys, time, hashlib, subprocess, threading
from pathlib import Path
from datetime import datetime

# Make sibling files importable when running on Spaces
sys.path.insert(0, os.path.dirname(__file__))

import gradio as gr

OUT = Path(os.environ.get("SOV33_OUT_DIR", "/data/bench-results"))
OUT.mkdir(parents=True, exist_ok=True)
SIGIL_CHAIN = OUT / "sigil_chain.jsonl"

def sigil_of(d): return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()

SUITE_INFO = {
    "general": {
        "quick":      ["mmlu_pro:50", "gsm8k:50", "hellaswag:50", "arc_challenge:50"],
        "code":       ["humaneval:164"],
        "math":       ["gsm8k:200", "aime_2024:30"],
        "knowledge":  ["mmlu_pro:200", "hellaswag:200", "arc_challenge:200", "truthfulqa_mc1:200"],
        "full":       ["mmlu_pro:200", "gsm8k:200", "aime_2024:30", "hellaswag:200",
                       "arc_challenge:200", "humaneval:164", "truthfulqa_mc1:200"],
    },
    "agentic": {
        "quick":   ["gaia_l1:10", "hotpotqa_distractor:20"],
        "agentic": ["gaia_l1:20", "tau_retail:20", "alfworld_text:20",
                    "hotpotqa_distractor:50", "swe_bench_lite:10"],
        "tools":   ["tau_retail:20", "alfworld_text:20"],
        "reason":  ["hotpotqa_distractor:50", "gaia_l1:20"],
        "code":    ["swe_bench_lite:20"],
    },
}

def run_bench(model_id: str, target: str, suite: str, n: int,
              quantize_4bit: bool, max_new_tokens: int,
              progress=gr.Progress()):
    progress(0.05, desc=f"Loading {model_id}…")
    os.environ["HF_TOKEN"] = os.environ.get("HF_TOKEN", "")

    if target == "general":
        script = os.path.join(os.path.dirname(__file__), "sov33_benchmark_general.py")
    else:
        script = os.path.join(os.path.dirname(__file__), "sov33_benchmark_agentic.py")
    cmd = [sys.executable, script, "--model", model_id,
           "--suite", suite, "--n", str(n),
           "--out", str(OUT)]
    if quantize_4bit:
        # 4bit only works with HF transformers path
        os.environ["SOV33_QUANTIZE_4BIT"] = "1"
    if max_new_tokens:
        cmd += ["--max-new-tokens", str(max_new_tokens)]

    progress(0.1, desc=f"Running {target}/{suite}…")
    log_lines = []
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, bufsize=1)
        for line in proc.stdout:
            log_lines.append(line.rstrip())
            if len(log_lines) % 10 == 0:
                progress(min(0.95, 0.1 + 0.85 * (len(log_lines)/500)),
                         desc=line.strip()[:80])
        proc.wait()
        if proc.returncode != 0:
            return "\n".join(log_lines), None, "FAILED"
    except Exception as e:
        return f"ERROR: {e}", None, "ERROR"

    progress(0.95, desc="Collecting results…")
    pat = f"{target}_{model_id.split('/')[-1]}_"
    candidates = sorted(OUT.glob(f"{pat}*.json"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        return "\n".join(log_lines), None, "NO_OUTPUT"

    result = json.loads(candidates[-1].read_text())
    # Sigil chain
    prev = None
    if SIGIL_CHAIN.exists():
        for line in SIGIL_CHAIN.read_text().splitlines()[-1:]:
            prev = json.loads(line).get("chain")
    chain = hashlib.sha256(f"{prev or 'genesis'}|{json.dumps(result, sort_keys=True)}".encode()).hexdigest()
    with SIGIL_CHAIN.open("a") as f:
        f.write(json.dumps({"ts": datetime.now().isoformat(),
                            "model": model_id, "target": target, "suite": suite,
                            "sigil": result.get("sigil", ""), "chain": chain}) + "\n")

    progress(1.0, desc="Done")
    summary = (
        f"Model: {model_id}\n"
        f"Target: {target}\n"
        f"Suite: {suite}\n"
        f"Composite: {result.get('composite_pct', 0):.2f}%\n"
        f"Sigil: {result.get('sigil', 'n/a')[:32]}…\n"
        f"Chain: {chain[:32]}…\n"
        f"Results file: {candidates[-1]}\n"
    )
    return "\n".join(log_lines[-50:]), str(candidates[-1]), summary

with gr.Blocks(title="SOV33 Benchmark Runner") as demo:
    gr.Markdown("# 🧪 SOV33 Benchmark Runner\nGeneral capability + Agentic capability eval against any HF model.")
    with gr.Row():
        with gr.Column():
            model_id = gr.Textbox(label="Model id", value="Qwen/Qwen2.5-3B-Instruct")
            target = gr.Radio(["general", "agentic"], value="general", label="Target")
            suite = gr.Dropdown(list(SUITE_INFO["general"].keys()),
                                value="quick", label="Suite")
            n = gr.Slider(10, 500, value=50, step=10, label="N per benchmark")
            quantize_4bit = gr.Checkbox(label="4-bit quant (saves VRAM)", value=False)
            max_new_tokens = gr.Slider(64, 2048, value=256, step=64, label="max_new_tokens")
            run = gr.Button("▶ Run", variant="primary")
        with gr.Column():
            log = gr.Textbox(label="Log (tail)", lines=20, interactive=False)
            output_file = gr.Textbox(label="Results JSON path", interactive=False)
            summary = gr.Textbox(label="Summary", lines=8, interactive=False)
    run.click(run_bench,
              inputs=[model_id, target, suite, n, quantize_4bit, max_new_tokens],
              outputs=[log, output_file, summary])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))