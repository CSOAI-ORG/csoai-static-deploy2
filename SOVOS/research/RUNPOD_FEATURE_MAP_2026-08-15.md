# RunPod Feature → Estate Improvement Map (2026-08-15)

## Current estate (verified live)
### Pods (long-lived, fixed cost — $33.84/day burn)
| Pod | GPU | Cost/hr | Role |
|---|---|---|---|
| sov-brain-a100-fresh2 | A100 80GB | $1.19 | Heavy-lift: board, merges, overnight queue |
| sov-repull (3090) | RTX 3090 | $0.22 | (unreachable) arena worker |

### Serverless endpoints (17 — the "clusters")
QUEUE_DELAY scaler, idle 10-120s, gpuCount 1 each:
- **Frontier (FlashBoot on):** sov6-qwen3-235b · sov6-deepseek-r1-671b · sov6-gpt-oss-120b · sov6-qwen3-30b-a3b
- **Mid:** sov4-llama33-70b · sov4-qwen3-30b · sov4-phi4-14b · sov4-gemma2-9b · sov4-mistral-7b · sov4-dream-7b
- **Small:** sov4-rwkv7-2.9b · sov4-olmoe-1b-7b · sov4-qwen35-4b · sov4-deepseek-r1-7b · sov-fallback-qwen25-3b
- **Cluster:** sov4-cluster-small · sov4-cluster-medium

## RUNPOD FEATURES WE'RE USING vs NOT (the improvement map)

| RunPod feature | Using? | How it improves the estate |
|---|---|---|
| **Pods** (long-lived) | ✅ A100, 3090 | Heavy-lift + interactive dev |
| **Serverless endpoints** (Queue/LB) | ✅ 17 endpoints | The cluster — scale-to-zero, pay-per-second, burst for arena/city jobs |
| **FlashBoot** | ✅ on 4 frontier | ~1-2s cold start on big models — turn ON for all sov4/sov5 too |
| **Hub** (prebuilt workers) | ⚠️ partial | Deploy prebuilt vLLM/Ollama workers instead of hand-rolled templates |
| **Model repository** | ❌ not used | Cache models once → reuse across endpoints (saves GB + cold-start time) |
| **send/receive** (file transfer) | ❌ not used | We use scp/git; runway send/receive is faster for pod→pod |
| **Network volumes** (persistent) | ⚠️ 100GB + new 2TB | Attach the 2TB K3 volume to a serverless endpoint — pays-per-use |
| **Container registry auth** | ⚠️ partial | ECR/private images without credential rotation |
| **ECR delegation** | ❌ not used | Scoped pull access, no stored creds — more secure |
| **Template system** | ✅ | Codify pod/endpoint config once, reuse |
| **Jobs (runsync/run)** | ✅ | Warm-invoke endpoints = pay-per-inference, no idle pod burn |
| **Billing scoping** | ⚠️ | Break down cost per-endpoint to find the burn |
| **GPU catalog / datacenter** | ✅ | Saw A100 sold out in all 10 DCs tonight |

## THE THREE COST/FEATURE LEVERS (recommended actions)

### 1. Move the overnight queue from PODE to SERVERLESS (save ~$28/day)
The A100 pod at $1.19/hr ICE when idle is our biggest waste. Serverless endpoints scale-to-zero:
- Board/overnight jobs should be **serverless runs** (runsync) — pay only for the inference seconds, cold-start amortized
- Keep ONE pod for interactive dev; move batch work to endpoints
- **Estimated: $33.84/day → under $10/day** (85% cut)

### 2. Turn FlashBoot ON for ALL endpoints
FlashBoot (already on the 4 sov6 frontier) gives ~1-2s cold starts. The 13 sov4 endpoints run FlashBoot-off → 30-60s cold starts on every warm-up → wasted compute. **One update call per endpoint.**

### 3. Attach the 2TB volume to a SERVERLESS K3 endpoint
We created volume `i4atujketp` for K3 tonight. Instead of a $1.19/hr idle A100 pod to hold it, attach it to a **serverless endpoint** that:
- cold-starts only when K3 inference is requested (pay-per-use)
- holds the 2TB K3 weights persistently
- **The K3 becomes a pay-per-inference API, not idle silicon**

## Also worth enabling (next tier)
- **Model repository** — pre-pull all 20 ollama models once, mount as snapshot on any new pod/endpoint (saves the 5-hr pulls we hit tonight)
- **ECR delegation** — when we push our own images, use scoped ECR pull (secure, no key rotation)
- **Hub deploy** — the `sov6-*` frontier endpoints could be flashed from RunPod's vLLM Hub worker rather than custom templates

## The "learning" — RunPod surface to study more
- **FlashBoot** + **Model Repository** = fast cold starts on any model, reused
- **Queue vs LoadBalancer** scaler types = burst handling
- **Storage** = container disk vs network volume vs model snapshot (right-fit per job)
- **Serverless jobs** = the run/runsync/status/cancel pattern for batch measurement
