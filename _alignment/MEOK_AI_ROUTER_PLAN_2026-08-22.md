# MEOK AI — "OpenRouter of everything" (grounded in the verified stack) · 2026-08-22

Answering Nick's Qs honestly, grounded in what's VERIFIED this session (not the vision doc alone).

## Q1. Do they have an app? Offline AIs?
- **OpenRouter = API + web console.** No first-party local/offline app; third-party apps
  ("Russet: OpenRouter & Local AI" — iOS) do OpenRouter + **local** models. OpenRouter valued
  **$1.3B**; **Stripe deal** (bankingdive, 2026) — they're a **routing pipe** (thin margin, no data).

## Q2. Can people run open-source models on OURS? (RunPod backend, we commission)
**YES — this is real + immediately buildable off what's verified.** Your RunPod estate already serves
**23 serverless endpoints + GPU pods + the OWEM cache** (verified via API: `sov6-deepseek-r1-671b`,
`sov6-qwen3-235b`, `sov4-llama33-70b`, 24GB–141GB workers). The pain we remove:
- A dev installs Ollama/llama.cpp locally OR rents a pod. We provide **one click**: pick a model →
  run on YOUR RunPod (rented, they pay per-use) OR download-to-their-PC (local, free) → same keys/API.
- We **commission** the rent route (RunPod margin + our fee) and give the free/local route as the
  no-cost entry (which then feeds them up the paid path). This IS a real "OpenRouter for open-source"
  — verified infra + models + the AGUI front-end (live at `:8785`).

## Q3. Beat OpenRouter with live benchmarks as a data-generation business?
**That's the moat.** OpenRouter is a pipe (routes, keeps nothing). Verified: your **live axis engine runs
on the fleet** (auto-batch, honest gates — `UNMEASURED ≠ 0`) + GOVBENCH/DEFBENCH/COMPBENCH + MMLU.
Every live run generates: traces, preference pairs, safety incidents, **verified rankings** — the product.
Schema:
```
LIVE ARENA (MEOK worlds/MCP packs + RunPod models)
   ├── Model vendors stake to enter (prove it on live tasks)
   ├── Enterprises buy the data (10K ethics-in-logistics examples)
   ├── Researchers buy verified rankings (live, domain-specific, sigil-attested)
   └── Regulators buy attestation (benchmark → proof, C2PA/PoB — proofof-ai infra)
```

## The MEOK AI router (5 layers — grounded in the verified estate)
| Layer | What it routes | Verified infra we already have |
|---|---|---|
| **1. Framework** | MCP packs/domains (which framework speaks to which tool) | 568-repo MCP fleet (CSOAI-ORG) + sovereign MCPs |
| **2. Regulation** | EU AI Act / NIST RMF / TC260 / ISO 42001 / DEFONEOS | 30-framework crosswalk + `law_kb` + `dorado_gate` (verified 0.931) |
| **3. Law** | liability/attestation (proof of what happened) | proofof-ai / C2PA + SIGIL attestation |
| **4. Benchmark** | which model ACTUALLY works (live arena) | **verified axis engine** + fleet benchmarks (GOVBENCH 0.931, refusal 1.0, COMPBENCH 84.5%) |
| **5. Compute + data** | where to run + what to learn | **RunPod fleet** (23 serverless + pods + 2.3PB volume) + the data product |

## How we actually beat them (honest)
- **Them:** static model list, token fees, no data, no compliance, no liability.
- **Us (verified):** live rankings (axis engine), **we own the eval data**, domain MCP packs, built-in
  compliance (30-framework), SIGIL/C2PA attestation, **the models run on our RunPod (we commission)**.
- **Headline:** "EUNOMIA" is already 70% built — the verified parts are the measurement engine, the
  compliance/attestation layer, the MCP/pack network, the RunPod compute+data layer. 
- **What's actually left to build:** (a) the **arena** (live model-vs-model on MEOK worlds — the axis
  engine + fleet make this days, not months), (b) the **public routing API** (OpenAI-compatible gateway
  from our RunPod endpoints), (c) the **consumer MEOK front-end** (gamified, AGUI-anchored — AGUI is live).

## Immediate next 33-valued moves (MEOK lane)
1. Public OpenAI-compatible gateway over the RunPod serverless endpoints (the "rentable models" API).
2. Pay-per-use + commission billing on it (USDC/Stripe; the £0.05/call pattern already in the estate).
3. `meok-arena` — live model-vs-model arenas from the MEOK worlds (the data generator).
4. Wire the arena → axis engine (verified) → attested rankings → the data-product marketplace.
5. Consumer MEOK app: front-end on the AGUI (`:8785`) + local-run (Ollama bundle) for the free tier.
