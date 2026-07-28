# ⚠️ VOID — these are FAILED API CALLS, not scores

Every file here scored **0.0 on every dimension**. No real model does that; even a model that
answers nothing scores above zero on refusal dimensions, because "no answer" reads as a refusal.

**Cause (fixed 2026-07-28):** `govbench_eval.py::grade_response()` returned `0.0` when the
provider response began with `ERROR`. With no NVIDIA credential configured, every call errored
and the harness recorded a perfect zero for each dimension.

Published, these files state that **Google's and Mistral's models score zero on AI governance.**
They were never run. That would be false and defamatory.

`govbench_eval.py` now raises `UnreachableModel` and writes **no result file** for a model it
cannot reach. An unreachable model is ABSENT from the leaderboard — never scored.

Kept for provenance, excluded from every published artefact. Do not re-import.
