"""sov33_rho_gate.py — error-correlation gate for fusion (the emergence precondition).
Measures whether the 3 brains fail DIFFERENTLY (low rho = fusion helps) or TOGETHER (high rho = fusion hurts).
Gate the emergence claim on this: NO fusion win claim unless measured rho is low enough.
Source: arXiv 2606.27288 (67-model study) — lever is failure-mode heterogeneity, not model count."""
import numpy as np

def error_correlation(brain_correct):
    names = list(brain_correct)
    errs = {n: 1 - np.array(brain_correct[n], dtype=float) for n in names}
    pairs = {}
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            a, b = errs[names[i]], errs[names[j]]
            rho = 0.0 if (a.std()==0 or b.std()==0) else float(np.corrcoef(a,b)[0,1])
            pairs[f"{names[i]}|{names[j]}"] = round(rho,3)
    mean_rho = round(float(np.mean(list(pairs.values()))),3) if pairs else None
    if mean_rho is None: verdict="insufficient brains"
    elif mean_rho<0.3: verdict="LOW rho — decorrelated, fusion has headroom (emergence possible)"
    elif mean_rho<0.6: verdict="MODERATE rho — measure fused-vs-best carefully"
    else: verdict="HIGH rho — brains fail together, fusion a NET LIABILITY (do NOT claim emergence)"
    return {"pairwise_rho":pairs,"mean_rho":mean_rho,"verdict":verdict}
