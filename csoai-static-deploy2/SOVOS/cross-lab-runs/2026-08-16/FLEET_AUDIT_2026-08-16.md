# FLEET AUDIT — 2026-08-16 11:00 UTC (all pods scanned)

**Method:** RunPod GraphQL API (Authorization Bearer) — full pod list, status,
machineId, cost. SSH liveness + process probes on reachable pods. HTTP probes
on dead-gateway pods. Recorded to registry + this file.

## RunPod pods (11 total)

### RUNNING (4) — $3.99/h combined burn

| Pod | Name | GPU | Cost | Machine | Reachable | Activity |
|---|---|---|---|---|---|---|
| `1dldzposn7ssuu` | sov-brain-a100-fresh2-20260811 | A100 80GB | $1.19/h | 4o02unscakdn | ❌ gateway flap | overnight_queue + sign_honey (last known); SSH :11703 dead |
| `5ynpuvuiae807k` | overnight-bench-a100-v2 | A100 80GB | $1.19/h | 4o02unscakdn | ❌ gateway flap | **UNKNOWN — same machine as A100-1; probe failed from all surfaces** |
| `fpowppss5ngtkw` | sov-repull-20260808 | RTX 3090 | $0.22/h | 5qgi08c89nys | ✅ | **BUSY: load 12.9, 23GB VRAM, ollama llama-server** (real inference; arena/eat) |
| `l7g747oivyq6ab` | sovos-light-master-mine-20260816 | A100 80GB | $1.39/h | w30mtfp5a4ho | ✅ | **BUSY (93-94% GPU, 44GB): sibling dual sweep — real_bench_llama.py + sovos_ultimate_router.py → MASTER_LLAMA/MASTER_OLLAMA_FLEET** |

### EXITED (7) — $0/h, no GPU burn

`7vup4jco2e8dt0` kimi-k2-lora-train (A100 SXM, 0.57/h) · `2bcb5wruaghsda` sov-fuel-train-20260804 ($0.22) ·
`orbw1z9hh0dbw7` sov-fuel-train-retry0 ($0.22) · `3cw7x1y4v0am` sov33-master-takeover ($1.19) ·
`3npk2t9ou08u7` sov33-master-takeover-v2 ($1.19) · `2oe71t1knz5amr` sov33-master-takeover-v2-migration ($1.19) ·
`q6rzjp5561ek` sov-brain-a100-fresh-20260811 ($1.19)

## Duty classification

- **A100-1 (1dld4zposn7ssuvu2):** our executive pod (overnight queue + signing). Gateway down = can't verify, but machine carries the sovos-master volume. KEEP RUNNING.
- **overnight-bench-a100-v2 (5nmpvuvuiae807k):** same physical machine as A1, unverified workload, **$1.19/h burn, unreachable — prime PAUSE candidate** per user directive ("any pods now finished pause").
- **3090 (fpowppss5ngtkw):** busy serving real inference. KEEP.
- **sovs-light (le7g747o6qab):** sibling busy with dual sweep. KEEP (do not touch sibling work).
- **7 EXITED:** no burn, nothing to do.

## Decision recorded
- PAUSE candidate: `5ynpuvuatse807k overnight-bench-a100-v2` — but paause deferred until (a) gateway returns to rule out it being my own overnight queue, or (b) owner nod. Per rule "when in doubt ask" — this is a bill and it's unknown. Escalated: NICK.
- The overnight run should target A100-1's /runpod volume (has sovos-master + 88G free) — NOT sovos-light (sibling).

## Registry entries added
- `runpod pods total` = 11, `runpod pods running` = 4, `runpod spend $/h` = 3.99
- `runpod A100-1 machine` = 4o02unscakdn (shared with overnight-bench)
- Sources: live GraphQL 2026-08-16 11:00 UTC