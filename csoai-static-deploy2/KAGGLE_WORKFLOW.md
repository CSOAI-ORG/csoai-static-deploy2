# SOV Kaggle-First Workflow

## Principle
All GPU work runs on Kaggle T4 (free, 30h/week). Mac is a thin client for editing and syncing only.

## Daily Workflow

### 1. Edit scripts on Mac
```bash
# Edit capability matrix, training scripts, etc.
vim benchmark-results/run_capability_matrix.py
```

### 2. Deploy to Kaggle
```bash
# Push to Kaggle
kaggle kernels push -p /tmp/sov-kaggle-<name>
```

### 3. Check results
```bash
# Pull results
kaggle kernels pull nicktempleman/sov-<name> -p /tmp/sov-results
```

### 4. Sync to RunPod (when GPU available)
```bash
# Only when CA-MTL-3 has GPU availability
python3 runpod_sync.py
```

## Active Kaggle Kernels

| Kernel | Status | Purpose |
|--------|--------|---------|
| `nicktempleman/sov-winners-v2` | COMPLETE | Full 22-task capability matrix |
| `nicktempleman/sov-capability-matrix` | COMPLETE | 6-task capability matrix |
| `nicktempleman/sov-full-master` | COMPLETE | Full master with J-space + games |

## Cost

- **Kaggle**: $0 (30h/week free T4)
- **Mac**: $0 (thin client)
- **RunPod**: $0 (all pods stopped)
- **Total**: $0/hr

## Next Steps

1. Run `sov-winners-v2` on Kaggle with `sov6-gemma-owem-v2` model
2. Pull results and update competition bundle
3. Deploy to competitions (llm-classification-finetuning, etc.)
4. When CA-MTL-3 has GPU: attach volume and do full migration
