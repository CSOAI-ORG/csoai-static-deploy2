#!/usr/bin/env python3
"""Neurosymbolic COMPBENCH: wraps compbench_local.call with the DORADO gate + law-RAG.
Targets the governance/compliance category, which scored only 40% raw on sov33-unified."""
import sys, time
sys.path.insert(0, "/Users/nicholas/clawd/csoai-static-deploy2")
import compbench_local as CB
import law_kb as kb
import dorado_gate as dg

_GOV_KEYWORDS = ("compliance", "regulat", "ai act", "data protection", "gdpr", "iso 42001",
                 "law", "ethic", "govern", "risk management", "consent", "human oversight",
                 "transparency obligation", "prohibit")

# save the original transport BEFORE monkeypatching
_orig_call = CB.call

def ns_call(model, prompt, system=CB.NEUTRAL_SYSTEM, timeout=120):
    low = prompt.lower()
    # 1) DORADO hard-stop gate
    breach, label, cite = dg.hard_stop(prompt)
    if breach:
        return "I can't help with that — it's a hard-stop."
    # 2) law-RAG for governance/compliance items
    if any(k in low for k in _GOV_KEYWORDS):
        ctx = kb.build_context(prompt)
        prompt = f"{ctx}\n\nBased on the provisions above, answer precisely.\nQ: {prompt}"
    return _orig_call(model, prompt, system, timeout)

CB.call = ns_call  # monkeypatch so run() uses the neurosymbolic call

for model in (sys.argv[1:] or ["sov33-unified:latest"]):
    CB.run(model)
