# Free GPU Options (2026-07-27)

## Currently Using
| Platform | GPU | Cost | Limit | Status |
|----------|-----|------|-------|--------|
| Kaggle | T4 16GB | $0 | 30h/week | ✅ 5 kernels active, 3 runs completed |
| GitHub | N/A | $0 | Unlimited | ✅ Repo pushed: CSOAI-ORG/csoai-static-deploy2 |
| RunPod | 3090/A40/H100 | $0.22-3.50/hr | On-demand | ⚠ All stopped (saving $52.80/day) |
| Local Mac M4 | Apple M4 | $0 | Always | ✅ 31GB free, LaunchAgent active |
| Oracle ARM | CPU only | $0 | Always-free | ⚠ Needs instance IP to deploy daemon |

## Newly Added
| Platform | GPU | Cost | Limit | Status |
|----------|-----|------|-------|--------|
| Google Colab | T4 16GB | $0 | ~12h/day | ✅ Notebooks ready in free_gpu/ |
| HuggingFace Spaces | T4 16GB | $0 | 2 concurrent | ✅ Config in huggingface/ |
| Lightning AI | T4 16GB | $0 | 22h/month | ✅ Studio config in free_gpu/ |

## Next Steps
1. Open colab notebooks in Google Drive and run
2. Deploy HuggingFace Space from huggingface/
3. Start Lightning studio: `lightning run app free_gpu/lightning_studio.py`
4. Deploy Oracle ARM daemon: `bash free_gpu/oracle_arm_setup.sh <instance-ip>`
5. Fix Vercel billing at https://vercel.com/dashboard to unblock deploys
6. Clean ~/.claude-science (33GB) when confident it's safe to remove
