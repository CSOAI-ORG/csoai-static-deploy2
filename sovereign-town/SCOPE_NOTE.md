# Sovereign Town — Scope Note: 47 vs 140 Agents

## What is running now

The live simulation uses **140 procedural agents** split across 28 hives. This
is the research engine that:

- generates signed episodes and manifests 24/7,
- powers the governed-vs-ungoverned comparison,
- feeds the Policy Lab experiments, and
- backs the public fleet status and leaderboard.

## What the research narrative describes

Public-facing research documents (ONEPAGER, WHITEPAPER, investor briefs)
sometimes describe a **47-agent real-character town** — one specialist persona
per hive plus sovereign-tier advisors. That is the **product vision**, not the
current runtime.

## Why the difference

| Aspect | Current (140 agents) | Planned (47 agents) |
|---|---|---|
| Purpose | Data flywheel + policy wind-tunnel | Product demo + UI narrative |
| Agents | Procedural, parameter-driven | Curated real-character personas |
| Compute | CPU-friendly, runs continuously | GPU/LLM-backed, scene-driven |
| Output | Aggregate metrics + signed manifests | Rich character dialogue + decisions |

## Alignment

Both share the same:

- governance policies (`benchmark/policy.py`),
- regulatory crosswalk (`benchmark/regulatory_crosswalk.py`),
- signing and verification primitives (`sign_lib.py`, `verify_chain.py`),
- Policy Lab experiment schema (`experiments/`, `policy_lab.py`).

The 47-agent layer is a future presentation and inference layer on top of the
same proven backend physics.
