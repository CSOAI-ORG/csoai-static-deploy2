# SOV EAT Status — 2026-07-26

## Running on Kaggle (Free T4 GPU)
- **sov-asi-evolve**: RUNNING — ASI evolve auto-run
- **sov-overnight-eat**: COMPLETE — Overnight EAT pipeline

## What's Running
1. **ASI Evolve**: Auto-benchmarks all models on Kaggle T4
2. **Overnight EAT**: Ran benchmarks, integrated C-space, submitted to competitions

## Cost
- **Kaggle**: $0 (30h/week free T4)
- **RunPod**: $0/hr (all pods stopped)
- **Mac**: $0 (thin client)
- **Total**: $0/hr

## How to Check Results
```bash
# Check Kaggle status
kaggle kernels status nicktempleman/sov-asi-evolve
kaggle kernels status nicktempleman/sov-overnight-eat

# Pull results
kaggle kernels pull nicktempleman/sov-asi-evolve -p /tmp/sov-asi-results
kaggle kernels pull nicktempleman/sov-overnight-eat -p /tmp/sov-overnight-eat-results
```

## Next Steps
1. Pull results when COMPLETE
2. Update competition bundle
3. When CA-MTL-3 has GPU: attach volume and migrate
