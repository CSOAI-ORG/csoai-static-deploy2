# 🔥 COMPUTE HANDOFF — fire the REAL sovereign training the instant a GPU appears (2026-07-14)
_From Fable to Claude Science. Your rung-4 (QLoRA train) is now a single runnable script wired to the real
corpus. The ONLY blocker is a wired GPU — here's every way to fire it, in order of speed._

## The one command (self-contained, fetchable anywhere)
```bash
curl -sL "https://gist.githubusercontent.com/CSOAI-ORG/2a3aa08d9d52c7452acec3d5afc6f1b6/raw/3a35a1aa938495c855e42fce6471e2007e3eccc3/sov33_gpu_fire.py" -o fire.py && python fire.py
# or: python sov33_gpu_fire.py   (already in _alignment/sovereign_merge_kit/)
```
It: pip-installs → QLoRA-fine-tunes **Qwen3-0.6B** (Apache, fits a T4) on **3,356 real expert_data examples
(65 domains)** → grades **GSM8K in solver-format** → writes `sov33_local_gsm8k.json` + `sov_expert_adapter/`.
Set `SOV_BASE=Qwen/Qwen3-4B-Instruct` for a bigger expert (needs more VRAM). **Verified:** syntax-clean +
the corpus loader parses all 3,356 examples. NOT executed here (no CUDA on the 16GB Mac) — it needs a GPU.

## Where the GPU comes from (fastest → most powerful) — verified July 2026
1. **Kaggle — ARMED NOW.** Notebook `notebooke3e821442d` (owner nicktempleman): GPU T4×2 ON, internet ON,
   phone-verified, 30 GPU-hr/wk. Owner pastes the one command in a cell → real weights + number. Fastest path today.
2. **Lightning AI** — 80 GPU-hr/mo free **incl A100/H200**. Best for the Qwen3-4B/larger experts. Owner login → new Studio → run the command.
3. **Colab** — free T4, Google login. Same command.
4. **A wired compute target** — if a GPU endpoint is added to Settings → Compute (your `list_compute`), dispatch from there.

## The honest split (unchanged, and it's the real boundary)
- **You (Claude Science, sandboxed):** author/refine the recipe — DONE; the script is wired to your corpus + the measured trinity config (base=Qwen3, solver-format eval, care-floor at serve).
- **Fable (me):** built + staged the fire script, verified the corpus, made it fetchable. DONE.
- **Owner (Nick) / a wired endpoint:** the ONE action neither of us can do — provide the GPU (login+run, or wire a compute target). Kaggle is armed, so this is one paste.

## What lands when it fires
`sov33_local_gsm8k.json` (the REAL sovereign-trained number, solver-graded) + `sov_expert_adapter/` (your own
weights). Then `python3 sov33_ingest_kaggle_result.py` auto-wires it into `sov333_canonical.json`. That's the
staged→real moment for the whole trinity.

**Everything buildable without a GPU is built, wired, and fetchable. The trigger is one GPU connection.**
