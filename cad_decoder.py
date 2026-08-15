#!/usr/bin/env python3
"""cad_decoder.py — Context-Aware Decoding for statute-grounded generation.

THE PROBLEM THIS FIXES
    retrieval_bench measured: statute retrieval makes answers WORSE (Δ -5.26).
    A 0.5B model cannot use statute even when the right statute is in front of it.
    The grounding instruction turns every BM25 miss into a confident wrong answer.

WHAT CAD DOES (Shi et al., arXiv 2305.14739, NAACL 2024)
    Contrastive decoding: amplify the difference between context-aware and
    context-unaware distributions. Force the model to weight retrieved statute
    over its baked-in prior.

    True CAD (logit-level):
        p_CAD(y_t) ∝ p(y_t | context, query, y_<t)^(1+α) / p(y_t | query, y_<t)^α

    Prompt-level CAD (what we can do with Ollama/no-logprobs APIs):
        1. Generate with context (statute text)
        2. Generate without context (model weights only)
        3. Compare: if answers agree → high confidence
        4. If answers disagree → prefer context answer, flag uncertainty
        5. If context answer cites the statute correctly → anchor-gate pass

ARCHITECTURE
    ask_with_cad(model, question, statute_context, α=0.5)
      → CADResponse with: answer, context_answer, bare_answer,
        agreement, citation_check, cad_verdict

    The α parameter controls contrastive weight:
      α=0.0 → pure context (no debiasing)
      α=0.5 → balanced (Shi et al. main result)
      α=1.0 → strong contrast

    For prompt-level CAD, α controls the agreement threshold:
      α=0.5 → answers must agree on ≥50% of key claims to be "consistent"

MEASURED STATUS: NOT YET BENCHMARKED
    Pre-registered prediction (written BEFORE running):
    CAD will improve retrieval on statute-answerable items by ≥5 points.
    If CI crosses zero after CAD, the retrieval layer remains dead.

    python3 cad_decoder.py --test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from owem_cluster import ask as call_model, select_expert


@dataclass
class CADResponse:
    """Result of a CAD-augmented inference."""
    question: str
    answer: str                    # The CAD-selected final answer
    context_answer: str            # Answer with statute context
    bare_answer: str               # Answer without context (weights only)
    agreement: float               # 0.0-1.0 agreement between context and bare
    citation_correct: bool         # Does the context answer cite retrieved statutes?
    cad_verdict: str               # "context_preferred" | "consistent" | "divergent" | "bare_fallback"
    alpha: float                   # The contrastive weight used
    model: str                     # Which model answered
    dimension: str                 # Which dimension was classified
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def _extract_key_claims(text: str) -> set[str]:
    """Extract key factual claims from an answer for comparison.
    
    A claim is a sentence that contains a substantive assertion:
    - mentions an article number
    - contains a legal requirement
    - makes a factual statement about regulation
    """
    claims = set()
    # Article references
    for m in re.finditer(r'[Aa]rticle\s+\d+[a-z]?(?:\([^)]+\))?', text):
        claims.add(m.group().lower().strip())
    # Key legal verbs
    for sentence in re.split(r'[.!]', text):
        s = sentence.strip()
        if len(s) > 20 and any(w in s.lower() for w in [
            'require', 'must', 'shall', 'prohibit', 'mandate',
            'comply', 'obligat', 'necessary', 'essential',
            'high-risk', 'deployer', 'provider', 'transparency'
        ]):
            claims.add(s.lower()[:100])
    return claims


def _agreement_score(context_answer: str, bare_answer: str) -> float:
    """Compute agreement between context and bare answers.
    
    Uses claim overlap: what fraction of context claims appear (or are
    compatible with) bare claims. This is the prompt-level proxy for
    logit-level contrastive decoding.
    """
    if not context_answer.strip() or not bare_answer.strip():
        return 0.0
    
    ctx_claims = _extract_key_claims(context_answer)
    bare_claims = _extract_key_claims(bare_answer)
    
    if not ctx_claims and not bare_claims:
        # Both answers have no extractable claims — compare raw similarity
        ctx_words = set(context_answer.lower().split())
        bare_words = set(bare_answer.lower().split())
        if not ctx_words or not bare_words:
            return 0.0
        return len(ctx_words & bare_words) / max(len(ctx_words), len(bare_words))
    
    if not ctx_claims:
        return 0.5  # Can't determine — neutral
    
    # How many context claims are supported by bare claims?
    supported = 0
    for claim in ctx_claims:
        for bare_claim in bare_claims:
            # Exact match or substantial overlap
            if claim == bare_claim:
                supported += 1
                break
            # Word overlap > 60%
            cw = set(claim.split())
            bw = set(bare_claim.split())
            if cw and bw and len(cw & bw) / max(len(cw), len(bw)) > 0.6:
                supported += 1
                break
    
    return supported / len(ctx_claims) if ctx_claims else 0.5


def _check_citations(answer: str, retrieved_articles: list[str]) -> bool:
    """Check if the answer correctly cites articles that were actually retrieved.
    
    This is the grounding check: an answer citing Article 43 when Article 43
    was never retrieved is ungrounded even if the citation is real.
    """
    if not retrieved_articles:
        return False
    
    cited_in_answer = set()
    for m in re.finditer(r'[Aa]rticle\s+(\d+)', answer):
        cited_in_answer.add(m.group(1))
    
    if not cited_in_answer:
        return False  # No citations at all — not grounded
    
    # At least one cited article must be in the retrieved set
    retrieved_nums = set()
    for art in retrieved_articles:
        m = re.search(r'(\d+)', art)
        if m:
            retrieved_nums.add(m.group(1))
    
    return bool(cited_in_answer & retrieved_nums)


def ask_with_cad(
    question: str,
    statute_context: str | None = None,
    retrieved_articles: list[str] | None = None,
    model: str | None = None,
    dimension: str | None = None,
    alpha: float = 0.5,
    timeout: int = 120,
) -> CADResponse:
    """Context-Aware Decoding: contrastive inference with/without context.
    
    Args:
        question: The governance question to answer
        statute_context: Retrieved statute text (if available)
        retrieved_articles: List of article IDs that were retrieved
        model: Ollama model to use (auto-selected if None)
        dimension: Governance dimension (auto-classified if None)
        alpha: Contrastive weight (0.0-1.0)
        timeout: Per-inference timeout in seconds
    
    Returns:
        CADResponse with the final answer and metadata
    """
    if model is None:
        model, _ = select_expert(dimension or "compliance")
    if dimension is None:
        from owem_cluster import classify_dimension
        dimension = classify_dimension(question)
    
    # ARM 1: Bare answer (model weights only)
    bare_prompt = f"Answer this governance question concisely.\n\nQuestion: {question}\nAnswer:"
    bare_answer = call_model(model, bare_prompt, timeout=timeout)
    
    if not statute_context:
        # No context available — bare answer is all we have
        return CADResponse(
            question=question,
            answer=bare_answer,
            context_answer="",
            bare_answer=bare_answer,
            agreement=1.0,
            citation_correct=False,
            cad_verdict="no_context",
            alpha=alpha,
            model=model,
            dimension=dimension,
        )
    
    # ARM 2: Context answer (statute-grounded)
    # The grounding instruction must be firm but not so strict that the model
    # refuses to answer when the text DOES cover the question. The previous
    # version ("If it does not settle, say 'not covered'") caused the model to
    # say "not covered" even when Article 27 explicitly covered credit scoring.
    context_prompt = (
        f"Based on the regulation text below, answer the question. "
        f"Cite the specific article. If the text is truly irrelevant, say so.\n\n"
        f"{statute_context}\n\n"
        f"Question: {question}\nAnswer:"
    )
    context_answer = call_model(model, context_prompt, timeout=timeout)
    
    # Compute agreement
    agreement = _agreement_score(context_answer, bare_answer)
    
    # Check citations
    citation_correct = _check_citations(
        context_answer, retrieved_articles or []
    )
    
    # CAD verdict
    if agreement >= (1.0 - alpha):
        # Answers are consistent — high confidence
        verdict = "consistent"
        final_answer = context_answer  # Prefer context (more grounded)
    elif citation_correct:
        # Context answer cites the right statute — trust it even if bare disagrees
        verdict = "context_preferred"
        final_answer = context_answer
    elif agreement < 0.3:
        # Answers strongly disagree — context may be misleading
        # Use context answer but flag uncertainty
        verdict = "divergent"
        final_answer = context_answer
    else:
        # Moderate disagreement — context answer with caveat
        verdict = "context_preferred"
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


def batch_cad(
    questions: list[dict],
    alpha: float = 0.5,
    model: str | None = None,
) -> list[CADResponse]:
    """Run CAD on a batch of questions with their contexts.
    
    Each question dict should have:
        - question: str
        - context: str (optional)
        - articles: list[str] (optional)
        - dimension: str (optional)
    """
    results = []
    for i, q in enumerate(questions):
        print(f"  [{i+1}/{len(questions)}] {q['question'][:60]}...", flush=True)
        try:
            resp = ask_with_cad(
                question=q["question"],
                statute_context=q.get("context"),
                retrieved_articles=q.get("articles"),
                model=model,
                dimension=q.get("dimension"),
                alpha=alpha,
            )
            results.append(resp)
            print(f"    verdict={resp.cad_verdict} agreement={resp.agreement:.2f} "
                  f"cite={resp.citation_correct}")
        except Exception as e:
            print(f"    ERROR: {e}")
    return results


# ── Self-test ────────────────────────────────────────────────────────────────

def selftest():
    """Quick self-test: one question with and without context."""
    print("  CAD DECODER — self-test\n")
    
    # A question where statute matters
    q = "Does Article 27 apply to a private credit-scoring deployer?"
    
    # Simulated statute context (the actual Art 27 text)
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
    print(f"  model: {model}")
    print(f"  question: {q}\n")
    
    resp = ask_with_cad(
        question=q,
        statute_context=ctx,
        retrieved_articles=["Article 27"],
        model=model,
        dimension="compliance",
    )
    
    print(f"  BARE ANSWER (weights only):")
    print(f"    {resp.bare_answer[:200]}")
    print(f"\n  CONTEXT ANSWER (statute-grounded):")
    print(f"    {resp.context_answer[:200]}")
    print(f"\n  CAD VERDICT: {resp.cad_verdict}")
    print(f"  AGREEMENT: {resp.agreement:.2f}")
    print(f"  CITATION CORRECT: {resp.citation_correct}")
    print(f"\n  FINAL ANSWER:")
    print(f"    {resp.answer[:200]}")
    
    return resp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="run self-test")
    ap.add_argument("--question", type=str, help="question to answer")
    ap.add_argument("--context", type=str, help="statute context")
    ap.add_argument("--model", type=str, help="Ollama model name")
    ap.add_argument("--alpha", type=float, default=0.5, help="contrastive weight")
    ap.add_argument("--json", action="store_true", help="JSON output")
    a = ap.parse_args()
    
    if a.test:
        selftest()
    elif a.question:
        resp = ask_with_cad(
            question=a.question,
            statute_context=a.context,
            model=a.model,
            alpha=a.alpha,
        )
        if a.json:
            print(json.dumps(asdict(resp), indent=2))
        else:
            print(f"  verdict: {resp.cad_verdict}")
            print(f"  agreement: {resp.agreement:.2f}")
            print(f"  citation_correct: {resp.citation_correct}")
            print(f"  answer: {resp.answer[:300]}")
    else:
        ap.print_help()
