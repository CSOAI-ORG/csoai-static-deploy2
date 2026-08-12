# SOVOS/agents — operator pod scripts

These scripts run ON the RunPod pods (currently `sov-brain-2`, the RTX
3090 pod that holds the specialists training setup). The Mac
orchestrates; the pod does the heavy compute.

## Files

- **`run_care_specialist_train.sh`** — train the missing `care`
  specialist adapter (`/root/specialists_v1/care/adapter`). Idempotent:
  skips if the adapter already exists.
- **`merge_4_specialists_ties.sh`** — TIES-merge all four sovereign
  specialists (governance, safety, privacy, care) over a shared
  `qwen2.5:0.5b-instruct` base. Writes a fresh directory
  `/root/merge/oowm_4way_<ts>/` per run.
- **`bench_merge_v_parents.py`** — measure the merged model + each
  specialist + base on the 13 GSPC axes via ollama, and apply the
  **doctrine gate**: each specialist must beat base on its OWN axis
  before any merge claim is creditable. The merge inherits the
  doctrine per TIES-amplifies-what's-there rules.

## Reproducibility

All three scripts are idempotent and logged. The training script
exits cleanly if the adapter is already there. The merge script
writes to a timestamped directory, so multiple merges coexist and the
latest is always at `/root/merge/oowm_4way_<latest-ts>/`. The bench
script prints a per-axis and per-specialist table suitable for
tracking in `decisions/specialist_training_log.md`.

## End-to-end flow

```
1. nohup bash run_care_specialist_train.sh > care.log 2>&1 & disown
   (≈10-30 min, depending on dataset size)
2. python3 /workspace/merge_4_specialists_ties.sh  (≈5-10 min)
3. python3 merge_4_specialists_ties.sh               # writes $OUT_DIR
4. nohup bash merge_4_specialists_ties.sh > merge.log 2>&1 & disown
   (5-10 min)
5. ollama create sov-merge-4way -f <OUT_DIR>/...         (manual)
   (NO ollama FROM-dir import per the coordination doc)
6. python3 bench_merge_v_parents.py \
       --merged-dir <OUT_DIR> \
       --specialists-dir /root/specialists_v1
   (passes the doctrine gate if all specialists beat base on their own axis)
```

## Hard lessons baked into the scripts

- **schema format**: trainer expects `{"messages": [...]}` not
  `{"instruction", "response"}`. Run `normalize.py` first; the
  normalized files are already at `/root/specialists_v1/normalized/`.
- **ollama register** is unreliable from the trainer's post-step;
  skip it and register upstream via `ollama create` from the merge
  output (with the ollama FROM-dir trap avoided by using
  `convert_hf_to_gguf.py` if needed).
- **disk pressure**: `/` is at 99% on `sov-brain-2`. Always purge
  `pip cache` + unneeded merged `*.gguf` before a merge.
- **doctrine first**: TIES amplifies what's there. If a specialist
  regresses on its own axis (e.g. safety on gspc-gov at n=237),
  merging it produces a weaker model. Verify the gate before claiming
  any capability gain.

## Why these live in SOVOS

These scripts are part of the canonical absorption — `sov-brain-2`
already ran exactly this operation with hand-tuned incantations.
Pinning them as `SOVOS/agents/` is the abs orb target: every fresh
pod can `git clone` and `bash ./SOVOS/agents/run_*` instead of
discovering the schema and register-step bugs from scratch.
