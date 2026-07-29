#!/usr/bin/env python3
"""ada_cad.py — Adaptive Context-Aware Decoding (AdaCAD).

Extends CAD with dynamic, per-response contrastive weight based on
divergence between context and bare answers.

AdaCAD (Wang et al., NAACL 2025, arXiv 2409.07394) replaces fixed α
with a per-token weight based on Jensen-Shannon Divergence. For prompt-level
CAD, we adapt this to per-response: compute JSD between the context and bare
answer distributions, then use that as the contrastive weight.

Key insight: when context and bare answers agree (low JSD), no contrastive
boost is needed. When they disagree (high JSD), the context answer should
be strongly preferred — that's exactly when the statute is correcting the
model's baked-in prior.

    python3 ada_cad.py --test
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from cad_decoder import (
    ask_with_cad, CADResponse, _extract_key_claims,
    _agreement_score, _check_citations
)
from owem_cluster import ask as call_model, select_expert


def _word_distribution(text: str) -> dict[str, float]:
    """Convert text to a word frequency distribution."""
    words = text.lower().split()
    if not words:
        return {}
    freq: dict[str, float] = {}
    for w in words:
        w = w.strip('.,;:!?()[]"\'')
        if len(w) > 2:
            freq[w] = freq.get(w, 0) + 1
    total = sum(freq.values())
    return {k: v / total for k, v in freq.items()}


def _jsd(p: dict[str, float], q: dict[str, float]) -> float:
    """Jensen-Shannon Divergence between two distributions.
    
    JSD(P||Q) = 0.5 * KL(P||M) + 0.5 * KL(Q||M), where M = 0.5*(P+Q).
    Returns value in [0, ln(2)] — 0 means identical, ln(2) ≈ 0.693 means maximally different.
    """
    all_keys = set(p.keys()) | set(q.keys())
    if not all_keys:
        return 0.0
    
    # Compute M = 0.5 * (P + Q)
    m = {}
    for k in all_keys:
        m[k] = 0.5 * (p.get(k, 0.0) + q.get(k, 0.0))
    
    # KL(P||M) and KL(Q||M)
    kl_pm = 0.0
    kl_qm = 0.0
    for k in all_keys:
        pk = p.get(k, 1e-10)
        qk = q.get(k, 1e-10)
        mk = m.get(k, 1e-10)
        if pk > 0:
            kl_pm += pk * math.log(pk / mk)
        if qk > 0:
            kl_qm += qk * math.log(qk / mk)
    
    return 0.5 * (kl_pm + kl_qm)


def _compute_adaptive_alpha(context_answer: str, bare_answer: str) -> float:
    """Compute adaptive α based on divergence between answers.
    
    High divergence → high α (strongly prefer context)
    Low divergence → low α (answers agree, no contrast needed)
    
    Maps JSD [0, ln(2)] → α [0.1, 1.0]
    """
    p = _word_distribution(context_answer)
    q = _word_distribution(bare_answer)
    jsd = _jsd(p, q)
    
    # Normalize: JSD ∈ [0, ln(2)] → α ∈ [0.1, 1.0]
    max_jsd = math.log(2)  # ≈ 0.693
    alpha = 0.1 + 0.9 * min(jsd / max_jsd, 1.0)
    return round(alpha, 3)


def ask_with_adacad(
    question: str,
    statute_context: str | None = None,
    retrieved_articles: list[str] | None = None,
    model: str | None = None,
    dimension: str | None = None,
    timeout: int = 120,
) -> CADResponse:
    """AdaCAD: adaptive contrastive decoding.
    
    Instead of fixed α, computes α dynamically from the divergence between
    context and bare answers. The more they disagree, the more we trust context.
    """
    # First, get both answers (reuse CAD infrastructure)
    if model is None:
        model, _ = select_expert(dimension or "compliance")
    if dimension is None:
        from owem_cluster import classify_dimension
        dimension = classify_dimension(question)
    
    # Get bare answer
    bare_prompt = f"Answer this governance question concisely.\n\nQuestion: {question}\nAnswer:"
    bare_answer = call_model(model, bare_prompt, timeout=timeout)
    
    if not statute_context:
        return CADResponse(
            question=question,
            answer=bare_answer,
            context_answer="",
            bare_answer=bare_answer,
            agreement=1.0,
            citation_correct=False,
            cad_verdict="no_context",
            alpha=0.0,
            model=model,
            dimension=dimension,
        )
    
    # Get context answer
    context_prompt = (
        f"Based on the regulation text below, answer the question. "
        f"Cite the specific article. If the text is truly irrelevant, say so.\n\n"
        f"{statute_context}\n\n"
        f"Question: {question}\nAnswer:"
    )
    context_answer = call_model(model, context_prompt, timeout=timeout)
    
    # Compute adaptive α
    alpha = _compute_adaptive_alpha(context_answer, bare_answer)
    
    # Compute agreement
    agreement = _agreement_score(context_answer, bare_answer)
    
    # Check citations
    citation_correct = _check_citations(
        context_answer, retrieved_articles or []
    )
    
    # AdaCAD verdict: adaptive threshold based on α
    threshold = 1.0 - alpha  # Higher α → lower agreement threshold
    if agreement >= threshold:
        verdict = "consistent"
        final_answer = context_answer
    elif citation_correct:
        verdict = "context_preferred"
        final_answer = context_answer
    elif alpha > 0.7:
        # High divergence + no citations → context may be misleading
        # But still prefer context (the statute is the anchor)
        verdict = "divergent_anchor_wins"
        final_answer = context_answer
    else:
        verdict = "divergent"
        final_answer = context_answer
    
    return CADResponse(
        question=question,
        answer=final_answer,
        context_answer=context_answer,
        bare_answer=bare_answer,
        agreement=round(agreement, 3),
        citation_correct=citation_correct,
        cad_verdict=verdict,
        alpha=alpha,
        model=model,
        dimension=dimension,
    )


def selftest():
    """Compare fixed CAD vs adaptive CAD."""
    print("  ADAPTIVE CAD — self-test\n")
    
    q = "Does Article 27 apply to a private credit-scoring deployer?"
    ctx = (
        "[CELEX 32024R1689 Article 27]\n"
        "1. Deployers of high-risk AI systems referred to in Article 6(2) shall perform "
        "a fundamental rights impact assessment prior to putting the high-risk AI system "
        "into use. ... "
        "2. The obligation referred to in paragraph 1 applies to deployers that are "
        "... (b) entities that are private operators providing public services, "
        "including in the areas of creditworthiness evaluation ..."
    )
    
    model, _ = select_expert("compliance")
    
    # Fixed CAD (α=0.5)
    print("  --- FIXED CAD (α=0.5) ---")
    fixed = ask_with_cad(
        question=q, statute_context=ctx,
        retrieved_articles=["Article 27"], model=model,
        dimension="compliance", alpha=0.5,
    )
    print(f"  verdict: {fixed.cad_verdict}  agreement: {fixed.agreement:.2f}  α: {fixed.alpha}")
    
    # Adaptive CAD
    print("\n  --- ADAPTIVE CAD ---")
    adaptive = ask_with_adacad(
        question=q, statute_context=ctx,
        retrieved_articles=["Article 27"], model=model,
        dimension="compliance",
    )
    print(f"  verdict: {adaptive.cad_verdict}  agreement: {adaptive.agreement:.2f}  α: {adaptive.alpha}")
    
    print(f"\n  Adaptive α chose {adaptive.alpha:.2f} (fixed was 0.50)")
    print(f"  Context answer: {adaptive.context_answer[:150]}...")
    print(f"  Bare answer: {adaptive.bare_answer[:150]}...")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    if a.test:
        selftest()
    else:
        ap.print_help()
