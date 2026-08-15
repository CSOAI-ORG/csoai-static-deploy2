# FRONTIER — the 2 moves that actually improve SOV4/5 (staged 2026-07-28, CC lane)
_Both are the DESIGNED-BLOCKED pieces from the 07-24 SOV4 synthesis. No scripts existed on disk;
these are ready-to-run starting points. **UNTESTED** — they need a live GPU (Kaggle T4 / HF Space / pod).
Nothing here climbs boards by fine-tuning (that's a settled 0.00-delta negative); both unblock EXISTING design._

## Move 1 — DeepSeek-OCR visual leg  (`move1_deepseek_ocr/`)
The biggest honest upgrade. The visual-honey leg was blocked ONLY on a GPU loader image.
- `Dockerfile` — DeepSeek-OCR on vLLM 0.8.5+, OpenAI-compatible endpoint.
- `smoke_test.py` — renders text→PNG→OCR, proves the ~7.77x optical-compression path (local or served).
- Unblocks Stage-4/5 visual retrieval WITHOUT changing the design.

## Move 2 — composite vs best-single  (`move2_composite_serve/`)
The one move that lifts hard boards. Best-of-N across decorrelated legs = 0.975 GSM8K served, but
composite-vs-best-single on HARD boards was never measured (needs ≥2 legs served live).
- `composite_vs_best_single.py` — serves N legs, best-of-N per leg, jury composite, prints the lift
  AND the measured correctness-rho (must be CROSS-FAMILY to seat: rho −0.725 seats, +0.764 does not).

## Where these run now (post-RunPod-drain world)
Kaggle T4 (free 30h/wk) is the go-forward GPU. Move 1 fits T4 (DeepSeek-OCR is small); Move 2 needs
two endpoints — run the two decorrelated legs quantized on T4, or one on T4 + one via a free API leg
(Groq / NVIDIA free tier already working per MASTER_CONSOLIDATION).

## Honesty
- Params don't sum; SOV4/5 is a governed composite. The lift comes from decorrelation + selection, not size.
- These are staged, not validated. First green run on real GPU replaces "UNTESTED" with a measured number.
