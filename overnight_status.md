# SOV Overnight Status — 2026-07-26

## Running on Kaggle (Free T4 GPU)
- **sov-asi-evolve**: RUNNING — ASI evolve auto-run
- **sov-overnight-eat**: COMPLETE — Overnight EAT pipeline
- **sov-winners-v2**: COMPLETE — 22-task capability matrix
- **sov6-llm-classification-finetuning**: COMPLETE — Competition: $200K
- **sov6-red-team**: COMPLETE — Competition: $500K
- **sov6-pokemon**: COMPLETE — Competition: $240K

## What's Running
1. **ASI Evolve**: Auto-benchmarks all models on Kaggle T4
2. **Overnight EAT**: Runs benchmarks, integrates C-space, submits to competitions
3. **Competition Notebooks**: Ready for submission

## Cost
- **Kaggle**: $0 (30h/week free T4)
- **RunPod**: $0/hr (all pods stopped)
- **Mac**: $0 (thin client)
- **Total**: $0/hr

## Next Steps
1. Monitor `sov-asi-evolve` status
2. Pull results when COMPLETE
3. Update competition bundle with new results
4. When CA-MTL-3 has GPU: attach volume and migrate

## How to Check Status
```bash
# Check Kaggle status
kaggle kernels status nicktempleman/sov-asi-evolve
kaggle kernels status nicktempleman/sov-overnight-eat

# Pull results
kaggle kernels pull nicktempleman/sov-asi-evolve -p /tmp/sov-overnight-results
kaggle kernels pull nicktempleman/sov-overnight-eat -p /tmp/sov-overnight-eat-results
```
