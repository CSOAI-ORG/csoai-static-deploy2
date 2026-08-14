---
license: apache-2.0
tags: [ai-governance, gspc, measurement, eu-ai-act]
---
# GSPC fleet board — 20 models

Control-anchored GSPC measurement of a model fleet. **Measurement, not certification.**

- **Control (untrained baseline):** `qwen2.5:0.5b-instruct` — 43% mean
- **Models measured:** 20
- **Models that beat the control by >1pt:** 19 — `nemotron-3-nano:30b`, `creation-v3-light:latest`, `preservation-v3-light:latest`, `embodiment-v3-light:latest`, `agency-v3-light:latest`, `aesthetics-v3-light:latest`, `gemma3:12b`, `destruction-v3-light:latest`
- **Measured:** 2026-08-13T16:55:42.431130+00:00

Each score is an accuracy on a fixed item set with an untrained control on the same axes.
A model at or below the control learned nothing measurable. Missing axes are UNMEASURED,
never zero. See `board.json` for the raw signed record and `scorecard.html` for the table.
