# SOV Free-GPU Full Strategy

## Current State (2026-07-26)

### RunPod
- **Running**: 2 pods ($0.88/hr, $21.12/day)
  - `sov33-top-bench-2` (A40, CA-MTL-1) — JupyterLab running
  - `fresh-a40` (A40, EU-SE-1) — Ollama + model creation active
- **Stopped**: 12 pods (saved $1.32/hr today)
- **Network Volume**: `sov-artifacts` (200GB, CA-MTL-3) — provisioned, not yet used

### Free Tiers
- **Kaggle**: ✓ 5 notebooks active today, T4 GPU available
- **Oracle ARM**: ✓ Config exists, always-free CPU
- **Local Mac M4**: ✓ Available for CPU work
- **Modal**: ✗ Spend limit exceeded

### Artifacts on RunPod
- **sov33-top-bench-2**: 115MB csoai-static-deploy2, 35MB sovereign, 20MB sov33
- **fresh-a40**: 81GB .ollama models, 57GB qwen3-30b weights

## Strategy

### Phase 1: Consolidate (this session)
1. ✓ Stop 3 idle pods (saved $31.68/day)
2. Copy fresh-a40 models to sov33-top-bench-2
3. Copy sov33-top-bench-2 artifacts to network volume
4. Stop fresh-a40 (save $0.44/hr)

### Phase 2: Free-Tier Deployment
1. Deploy capability matrix to Kaggle T4
2. Deploy data synthesis to Oracle ARM
3. Run E2E checks on local M4

### Phase 3: Paid GPU (when needed)
1. Spin up H100 only for 32B+ model inference
2. Use A40 for training (already running)
3. Use network volume for persistent storage

## Cost Savings
- Stopped 3 idle pods: $31.68/day savings
- Using Kaggle instead of H100 for benchmarks: $3.50/hr savings
- Using Oracle ARM for data synthesis: $0.44/hr savings
- Network volume avoids re-downloading models: $0.07/hr storage

## Next Actions
1. Copy fresh-a40 models to sov33-top-bench-2
2. Deploy capability matrix to Kaggle
3. Stop fresh-a40 after copy
4. Run master stage on sov33-top-bench-2
