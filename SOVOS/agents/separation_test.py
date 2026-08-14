"""Per-axis separation test: is the 'winner' actually separated?
Three tests per axis:
1. Winner vs majority baseline (Wilson CI disjoint?)
2. Winner vs best BASE model (Wilson CIs disjoint? else TIE)
3. McNemar on discordant pairs (winner vs best base) where computable
Honest claim = disjoint CIs or significant McNemar. Everything else = TIE.
"""
import json, math, collections

BASES = {"gemma3:12b","llama3.2:3b","qwen2.5:3b","qwen2.5:0.5b-instruct","mistral:7b","deepseek-r1:8b"}

def wilson(k,n,z=1.959964):
    if n<1: return (0,1)
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n)
    m=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return (max(0,(c-m)/d), min(1,(c+m)/d))

def mcnemar(b,c):
    # exact binomial on discordant pairs
    n=b+c
    if n==0: return None
    k=min(b,c)
    from math import comb
    p=2*sum(comb(n,i) for i in range(0,k+1))/(2**n)
    return min(1.0,p)

axes=['gov','agi','asi','prv','xr','det','art5','care','mcp','oss','mach','swarm','affect']
print(f"{'axis':7s} {'winner':28s} {'acc':>6s} {'CI':>15s} | vs baseline | vs best base (tie?) | McNemar p")
real_wins=[]; ties=[]
for ax in axes:
    b=json.load(open(f'/Users/nicholas/clawd/csoai-static-deploy2/SOVOS/boards-v2-2026-08-12/board_{ax}.json'))
    rows=[json.loads(l) for l in open(f'/Users/nicholas/clawd/csoai-static-deploy2/SOVOS/boards-v2-2026-08-12/peritem_{ax}.jsonl') if l.strip()]
    per=collections.defaultdict(lambda:[0,0])
    disc=collections.defaultdict(lambda:[0,0,0])  # pair -> [b10, c01, total]
    peritem=collections.defaultdict(dict)
    for r in rows:
        if str(r.get('transport_error','')).startswith('TRANSPORT'): continue
        m=r['model']; ok=bool(r.get('correct'))
        per[m][1]+=1; per[m][0]+=ok
        peritem[r['item']][m]=ok
    rank=sorted(per.items(), key=lambda kv:-kv[1][0]/max(1,kv[1][1]))
    win, (wk,wn) = rank[0]
    wacc=wk/wn; wci=wilson(wk,wn)
    base=b['majority_baseline']
    vs_base = "CLEAR" if wci[0]>base else "not-clear"
    others=[(m,kn) for m,kn in rank if m!=win]
    bases=[(m,kn) for m,kn in others if m in BASES] or others[:1]
    verdict="(no other)"; mc_p=None
    if bases:
        bm,(bk,bn)=bases[0]
        bci=wilson(bk,bn)
        sep = wci[0]>bci[1] or bci[0]>wci[1]
        # discordant pairs
        b10=c01=0
        for it,res in peritem.items():
            if win in res and bm in res:
                if res[win] and not res[bm]: b10+=1
                elif res[bm] and not res[win]: c01+=1
        mc_p=mcnemar(b10,c01)
        sig = mc_p is not None and mc_p<0.05
        # DECIDED RULE (2026-08-13): McNemar p<0.05 on discordant pairs is the
        # PRIMARY test (paired, more powerful). CI-disjoint alone is NOT
        # sufficient when McNemar is computable (swarm lesson: low-discrimination
        # bank gave disjoint CIs but p=1.0). Nor is CI-disjoint REQUIRED
        # (affect lesson: McNemar p=0.0078 real while CIs overlap). CI shown
        # as supporting annotation only.
        separated = sig
        ci_note = "CI-disjoint" if sep else "CI-overlap"
        verdict = f"SEPARATED vs {bm} ({ci_note})" if separated else f"TIE vs {bm} ({ci_note})"
        (real_wins if separated else ties).append(ax)
    print(f"{ax:7s} {win:28s} {wacc:6.3f} [{wci[0]:.3f},{wci[1]:.3f}] | {vs_base:9s} | {verdict:34s} | {('%.4f'%mc_p) if mc_p is not None else 'n/a'}")
print()
print(f"REAL separated wins: {len(real_wins)} {real_wins}")
print(f"TIES (winner is point-estimate only): {len(ties)} {ties}")
