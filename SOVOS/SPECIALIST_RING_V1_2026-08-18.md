# SPECIALIST RING v1 — 3 agentic axis harnesses (Playbook §4, the missing legs)
**Date:** 2026-08-18 · **Lane:** JEEVES · **Milestone:** prove the delta, then fan out to 16

---

## What was built

`specialist_ring_v1.py` — 3 axis harnesses (**gov · care · safety**), each owning ingest (frozen anchor items) → probe (deterministic predicate, temp=0) → delta (signed per-item verdict). Harness per axis, not per benchmark. **The predicate adjudicates; the model is the contestant (Design Law 1).**

```
AXIS HARNESS (gov/care/safety)
  ├─ ingest: frozen anchor items (EU AI Act Art 5, GDPR 22, CARE bank, SAFETY bank)
  ├─ probe:  temp=0 deterministic, through the pod (GPU :11434)
  └─ delta:  per-item ✓/✗ vs anchor → signed ring_{ts}.json → feeds the mine
```

## Results (live, 2026-08-18, 3 axes × 3 models, 36 probe cells)

| Model | gov | care | safety | avg |
|---|---|---|---|---|
| **qwen3:4b (base)** | 0.50 | 0.25 | 0.50 | **0.42** |
| **council-safe** (our fine-tune) | 0.25 | 0.50 | 0.50 | **0.42** |
| **council-oowm** (our fine-tune) | **0.00** | **0.00** | **0.00** | **0.00** |

**Delta proven.** The ring independently reproduces the honesty-gate finding: **council-oowm, our flagship sovereign fine-tune, scores zero on all three axes against frozen anchors**, while a base 4B model scores 0.42. The instrument catches us; the instrument works.

## Design notes (playbook compliance)

- **Deterministic predicate** — exact-label matching (PROHIBITED/HIGH_RISK/UNSAFE/SAFE/YES/NO). No LLM-as-judge. ✓ Law 1
- **Auto-update the DATA, never the predicate** — anchors frozen; only items rotate. ✓ §4
- **Portability contract** — `INCOMPLETE` on no-response, never pass. ✓ §4
- **Start 3, prove, fan out** — 3 axes live; 13 more to add (privacy, jail, swarm, transparency, fairness, accountability, continuity, efficiency, creativity, sovereignty, human-vs-ai, slot15, affect). ✓ §4
- **Never the judge** — harness emits evidence; verdict stays with the predicate. ✓

## Infrastructure fix required to get here

The pod had a **zombie GPU-Muse llama-server** (left from the CPU/GPU flip) pinning 23GB VRAM and wedging the main instance. Fixed: killed stale llama-servers, clean restarted both instances (11434 GPU-arena, 11435 CPU-Muse). Probes went from 45s-timeout → 3.4s.

## Next (fan out)

1. Add the 13 remaining axis harnesses (mirror the 16-axis arena battery + GSPC registry mapping)
2. Wire ring deltas into the estate mine (`ring_{ts}.json` → OOWM knowledge graph)
3. Daily ring cron on the pod (cheap, GPU only when arena idle)

## SIGIL
`specialist-ring-v1-2026-08-18-jeeves`
