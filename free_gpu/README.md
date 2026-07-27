# Free-GPU Swarm Strategy

## Cost Hierarchy (cheapest first)

| Tier | Provider | GPU | Cost/hr | Limit | Use For |
|------|----------|-----|---------|-------|---------|
| 0 | Local Mac M4 | CPU | $0 | Always | Code editing, E2E checks |
| 0 | Oracle ARM | CPU | $0 | Always-free | Data synthesis, corpus building |
| 1 | Kaggle | T4 16GB | $0 | 30h/week | Benchmark runs, capability matrix |
| 1 | Modal | T4 16GB | $0 | ~30h/month | Small model training (spend limit hit) |
| 2 | RunPod 3090 | RTX 3090 24GB | $0.22 | On-demand | Medium model training |
| 2 | RunPod A40 | A40 48GB | $0.44 | On-demand | Large model training |
| 3 | RunPod H100 | H100 80GB | $3.50 | On-demand | 32B+ model inference |

## Current Status (2026-07-26)

- **Local M4**: ✓ Available, 1.6GB free disk
- **Oracle ARM**: ✓ Available, config exists
- **Kaggle**: ✓ Available, 5 notebooks active today
- **Modal**: ✗ Spend limit exceeded
- **RunPod**: ⚠ 5 pods running at $2.20/hr (need to stop idle ones)

## Strategy

1. **Stop idle RunPod pods** — save $52.80/day
2. **Deploy to Kaggle T4** — free benchmark runs
3. **Deploy to Oracle ARM** — free data synthesis
4. **Only spin up RunPod when needed** — H100 for 32B+ models, A40 for training
5. **Use network volume** — persistent storage across pod restarts

## Deploy Commands

```bash
# Deploy capability matrix to Kaggle
python3 free_gpu/kaggle_capability_deploy.py

# Deploy data synthesis to Oracle ARM
python3 free_gpu/oracle_synth_deploy.py

# Stop idle RunPod pods
python3 free_gpu/stop_idle_pods.py

# Check costs
python3 free_gpu/orchestrator.py costs
```

## Competitions to Enter

- **openai-gpt-oss-20b-red-teaming** ($500K) — red teaming
- **openai-to-z-challenge** ($500K) — research
- **pokemon-tcg-ai-battle-challenge-strategy** ($240K) — strategy game
- **llm-prompt-recovery** ($200K) — prompt recovery
