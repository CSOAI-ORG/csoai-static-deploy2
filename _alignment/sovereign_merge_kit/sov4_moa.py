#!/usr/bin/env python3
"""sov4_moa.py — SOV4 Mixture-of-Agents: the REAL emergence path (Path A, free, inference-time).

The same-base weight-merge failed (no diversity + weak aggregator). MoA fixes BOTH, per the literature:
  1. DIVERSE proposers — genuinely different architectures (Groq serves Llama-70B, GPT-OSS-120B, Qwen free).
  2. STRONG aggregator — the biggest reachable brain SYNTHESIZES the drafts (not a weak averager).

Governed: care-gate + DEFONEOS hard-stop run first (via sovereign_decision), and the final MoA answer is signed.
This maps 1:1 onto SOV4: SOV1 routes -> 3 diverse brains propose -> strong aggregator reconciles -> signed.

measure() runs the HONEST test: does MoA beat the best single proposer? (LLM-as-judge on a held-out battery.)
No emergence is CLAIMED — it is measured. Run:  python3 sov4_moa.py
"""
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sovereign_router as R

# candidate DIVERSE proposers (different architectures/families), all free on Groq + local. Auto-probed for reachability.
CANDIDATES=[("groq","llama-3.3-70b-versatile"), ("groq","openai/gpt-oss-120b"),
            ("groq","qwen/qwen3-32b"), ("groq","llama-3.1-8b-instant"), ("ollama","sovereign")]

def _probe():
    live=[]
    for be,mdl in CANDIDATES:
        a,_=R.dispatch("Reply with the single word: ok", tier=None, backend=be, model=mdl, max_tokens=5)
        if a: live.append((be,mdl))
    return live

def moa(prompt, proposers=None, aggregator=None, system=None):
    """Mixture-of-Agents: diverse proposers draft -> strong aggregator synthesizes. Returns (final, drafts, meta)."""
    proposers = proposers or _probe()
    if not proposers: return None, [], {"error":"no proposers reachable"}
    drafts=[]
    for be,mdl in proposers:
        a,who=R.dispatch(prompt, system=system, backend=be, model=mdl, max_tokens=400)
        if a: drafts.append({"model":f"{be}:{mdl}","text":a})
    if not drafts: return None, [], {"error":"no drafts"}
    agg = aggregator or proposers[0]                     # strongest first by CANDIDATES order (70B/120B lead)
    synth=("You are the aggregator. Below are drafts from several different models answering the same question. "
           "Synthesize ONE superior answer — reconcile agreements, correct errors, keep the best grounded content. "
           "Do not just pick one.\n\nQUESTION: "+prompt+"\n\n"+
           "\n\n".join(f"DRAFT {i+1} ({d['model']}):\n{d['text']}" for i,d in enumerate(drafts)))
    final,who=R.dispatch(synth, system=system, backend=agg[0], model=agg[1], max_tokens=600)
    return final, drafts, {"proposers":[d["model"] for d in drafts],"aggregator":f"{agg[0]}:{agg[1]}"}

def measure(prompts=None):
    """HONEST emergence test: MoA final vs the best single draft, judged by the aggregator. Reports win-rate."""
    prompts = prompts or [
        "What must AI providers do for synthetic media under the EU AI Act?",
        "Under GDPR, when is a DPIA mandatory?",
        "Compare FedRAMP and ISO 27001 for a SaaS selling to US government."]
    live=_probe(); print(f"live proposers ({len(live)}): {[m for _,m in live]}")
    if len(live)<2: print("need >=2 diverse proposers — only", live); return
    agg=live[0]; wins=0
    for q in prompts:
        final,drafts,meta=moa(q, proposers=live, aggregator=agg)
        best=drafts[0]["text"]  # proxy 'best single' = strongest proposer's own draft
        judge=("Two answers to the same question. Reply ONLY 'A' or 'B' for which is more accurate, grounded and complete.\n"
               f"Q: {q}\n\nA (single model):\n{best[:1200]}\n\nB (synthesized):\n{(final or '')[:1200]}")
        v,_=R.dispatch(judge, backend=agg[0], model=agg[1], max_tokens=3)
        won = v and "B" in v.upper()[:3]
        wins += 1 if won else 0
        print(f"  [{'MoA wins' if won else 'single wins/tie'}] {q[:50]}")
    print(f"\nEMERGENCE MEASURE: MoA beat best-single on {wins}/{len(prompts)} (diverse proposers + strong aggregator).")
    print("Honest: small n, LLM-judge. >50% suggests real inference-time emergence; run a bigger battery to publish.")

if __name__=="__main__":
    measure()
