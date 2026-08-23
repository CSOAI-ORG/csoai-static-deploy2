# Pods + volumes — live (23 Aug ~18:25 London)

## Account
- email nicholas@csoai.org
- **clientBalance ~$148.04**
- **currentSpendPerHr ~$3.17** (higher than the 3 listed pods alone ≈$1.67 — serverless/other likely)
- spendLimit $80 (flag for Nick)

## Pods RUNNING
| id | name | $/hr | vol | role |
|----|------|-----:|----:|------|
| fpowppss5ngtkw | sov-repull-20260808 (3090) | 0.22 | 100 | KEEP / arena (fleet keep) |
| l7g747oivyq6ab | sovos-light-master-mine | 1.39 | 100 | **fleet do_not_start** but RUNNING |
| sz0duht9e5bbov | sov-volume-sink-cpu | 0.06 | 0 | offload sink; SSH -F /dev/null -p 25804 @ 213.173.105.83 |

A100-1 `1dldzposn7ssuu` — still GONE (fleet do_not_hammer).

## Network volumes
| id | name | size GB | DC |
|----|------|--------:|----|
| i4atujketp | k3-weights-2tb | 2000 | EU-RO-1 |
| 2i3cwz3a6k | sovos-merge-800 | 800 | EU-RO-1 |
| b0h5gma2fy | sov-models | 300 | CA-MTL-3 |
| uvevdv0pq9 | sov-artifacts | 200 | CA-MTL-3 |
| ahqvo6d4f3 | sov-workspace-mtl4 | 200 | CA-MTL-4 |

## fleet.json (19 Aug)
- brain = official DeepSeek; openrouter parked
- keep: 3090 / sov-brain-2
- do_not_start: mine l7g747…
- Mine running against lock = Monday money/ops decision

## Risks
- $3.17/hr ≈ **$76/day** if sustained — burns most of $148 in ~2 days
- Sink train/rebuild flap (not public ore)
- SSH to sink requires `-F /dev/null`

## Serverless (extra burn)
Multiple `sov4-*` endpoints exist (qwen25-7b, rwkv7, mixtral, olmoe, …). These likely explain currentSpendPerHr ~$3.17 vs pod-only ~$1.67.
Monday: inventory which workers are warm/active; cold-idle should be near $0 — if warm, kill or scale to 0 unless EUNOMIA needs them.

## Serverless (23 endpoints) — Mon money lever
sov4/sov6 fleet incl. qwen25-7b, mistral-7b, mixtral-8x7b, qwen38-27b, llama33-70b, deepseek-r1-671b, kimi-k3-2tb, gpt-oss-120b, muse-glimmer-30b, clusters, fallback.
If any workers are warm, they explain ~$3.17/hr. Monday: scale idle max→0 / delete unused unless EUNOMIA gateway needs a named subset.
