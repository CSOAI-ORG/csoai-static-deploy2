#!/usr/bin/env python3
"""statute_retrieval.py — answer from the statute text, not from the weights.

═══════════════════════════════════════════════════════════════════════════════
THE FAILURE THIS EXISTS TO FIX
═══════════════════════════════════════════════════════════════════════════════
`sov_whole.py`, asked *"Does Article 27 apply to a private credit-scoring deployer?"*,
answered that the article *"does not explicitly address"* it. That is wrong — Art 27(1)(b)
covers deployers of Annex III point 5(b) systems (creditworthiness evaluation), public or
private, and credit scoring is named explicitly.

**Every layer passed it.** Gate, classifier, hive, citation verify (0 fabricated / 0
misattributed — clean, and useless, because an answer carrying no citations passes trivially),
attestation, Article 50 marking. The pipeline shipped a wrong legal answer with a valid
marking and a signed receipt.

The cause is structural, not a tuning problem: the model was answering **from its weights**.
A 0.5B model does not hold Article 27. The statute text was sitting in
`eu-ai-act-compliance-mcp/data/regulations.db` — 404 articles across the AI Act, GDPR, NIS2,
DORA, CRA and CSRD, with an FTS5 index already built — and nothing was reading it.

═══════════════════════════════════════════════════════════════════════════════
DESIGN — three refusals, each earned by a specific failure this session
═══════════════════════════════════════════════════════════════════════════════
1. **No silent fallback.** If retrieval finds nothing, the answer is "no statutory basis
   retrieved", NOT a fluent answer from weights. A RAG system that quietly degrades to its
   parametric memory is indistinguishable from one that had no corpus, right up until it is
   wrong — which is precisely how the Article 27 answer was produced.

2. **Citations checked against what was actually retrieved.** Not against a registry of
   plausible-looking articles: against *these specific* retrieved texts. An answer citing
   Article 43 when Article 43 was never in the context is ungrounded even if Article 43 is
   real and the claim is true.

3. **Grounding is reported, never assumed.** Every answer carries `grounded: true|false` and
   the article ids it stands on. `retrieval_faithfulness` on the board is already the
   dimension that measures whether a model sticks to provided context; this makes that
   measurable end to end rather than per-prompt.

═══════════════════════════════════════════════════════════════════════════════
⚠️ MEASURED VERDICT — THIS LAYER SHIPS **OFF**
═══════════════════════════════════════════════════════════════════════════════
`retrieval_bench.py`, n=38, paired, same model on both arms:

    ungated   Δ -9.16  95% CI [-17.64, -0.69]   significant HARM
    gated     Δ -5.26  95% CI [-12.66, +2.13]   no effect shown

The relevance gate removed the significant regression — that is a real repair, and the
diagnostic case ("how should AI handle personal data" retrieving GDPR Art 47 on binding
corporate rules) no longer poisons the answer. But removing harm is not demonstrating
benefit. Retrieval is still trending negative: 5 wins, 8 losses, 25 ties.

So it is **available and off**, exactly as per-dimension routing is. Turn it on when a
re-run clears zero — not before, and not because the Article 27 case is compelling. That
case is real and it is one item.

The likely reason is the same one behind every other failure measured today: a 0.5B model
cannot reliably *use* 6KB of statute text even when the right statute is in front of it.
Every deterministic component in this stack works; every judgement-based one has failed or
is unproven. Retrieval-then-reason is judgement. The gate, the classifier and the citation
registry are not, and they are what holds.

    python3 statute_retrieval.py --search "fundamental rights impact assessment"
    python3 statute_retrieval.py --ask "Does Article 27 apply to a private credit scorer?"
"""
from __future__ import annotations

import argparse, json, re, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DB = HERE.parent / "mcp-marketplace" / "eu-ai-act-compliance-mcp" / "data" / "regulations.db"

NAMES = {"32024R1689": "EU AI Act", "32016R0679": "GDPR", "32022L2555": "NIS2",
         "32022R2554": "DORA", "32024R2847": "CRA", "32022L2464": "CSRD"}

STOP = {"the", "a", "an", "is", "are", "does", "do", "to", "of", "for", "and", "or", "in",
        "on", "it", "that", "this", "what", "which", "who", "how", "we", "our", "can", "be",
        "with", "under", "apply", "applies", "my", "you", "your", "if", "was", "has", "have"}


class NoStatuteFound(Exception):
    """Retrieval returned nothing. NOT a licence to answer from the weights."""


def _fts_query(question: str) -> str:
    """FTS5 chokes on raw punctuation, so terms are extracted rather than passed through.

    Article numbers are kept as literal terms — 'Article 27' is the highest-signal token in a
    governance question and dropping it to stopword filtering would be the difference between
    retrieving the right provision and retrieving a topical near-miss."""
    arts = re.findall(r"\barticles?\s+(\d+)", question, re.I)
    words = [w for w in re.findall(r"[A-Za-z]{3,}", question.lower()) if w not in STOP]
    terms = [f'"article {a}"' for a in arts] + [f'"{w}"' for w in words[:8]]
    return " OR ".join(terms) if terms else '""'


def search(question: str, k: int = 4) -> list[dict]:
    if not DB.exists():
        raise NoStatuteFound(f"corpus missing at {DB}")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    q = _fts_query(question)
    try:
        rows = con.execute(
            "SELECT celex, article_number, content, bm25(articles_fts) AS score "
            "FROM articles_fts WHERE articles_fts MATCH ? ORDER BY score LIMIT ?",
            (q, k)).fetchall()
    except sqlite3.OperationalError as e:
        raise NoStatuteFound(f"FTS query failed: {str(e)[:80]} (query={q[:60]})")
    finally:
        con.close()
    if not rows:
        raise NoStatuteFound(f"no article matched: {q[:70]}")
    return [{"celex": c, "regulation": NAMES.get(c, c), "article": n,
             "id": f"{NAMES.get(c, c)} Article {n}", "text": t, "score": round(s, 2)}
            for c, n, t, s in rows]


def get_article(celex: str, number: int) -> dict | None:
    """Fetch ONE named article by (regulation, number). No ranking, no guessing.

    ═══════════════════════════════════════════════════════════════════════════
    WHY THIS EXISTS — a KB harvest wrote 54 wrong entries before it was caught
    ═══════════════════════════════════════════════════════════════════════════
    Six regulations are indexed and **each has an Article 1**. Asking BM25 for "GDPR
    Article 1" scores on the terms, not on the identity, so it happily returned CSRD's
    Article 1 — and the model then answered "Article 1 GDPR requires automatic logging",
    which is not what GDPR Article 1 says at all.

    The grounding check passed it, because that check asked only whether the answer CITED
    the number it was asked about. It did. From the wrong statute. Verifying the citation
    without verifying the SOURCE is the same defect as every other one today: confirming the
    shape of an answer rather than the thing the answer is about.

    When the question names a specific provision, that provision is a lookup, not a search.
    """
    if not DB.exists():
        return None
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        row = con.execute(
            "SELECT celex, article_number, content FROM articles "
            "WHERE celex = ? AND article_number = ?", (celex, number)).fetchone()
    finally:
        con.close()
    if not row:
        return None
    c, n, t = row
    return {"celex": c, "regulation": NAMES.get(c, c), "article": n,
            "id": f"{NAMES.get(c, c)} Article {n}", "text": t, "score": 0.0,
            "exact_lookup": True}


def _cited(answer: str) -> set[str]:
    """Article references the answer actually makes."""
    return {m.group(1) for m in re.finditer(r"\bArticles?\s+(\d+)", answer, re.I)}


def relevant(question: str, hits: list[dict]) -> tuple[bool, str]:
    """Did retrieval return the RIGHT thing, or merely something?

    ═══════════════════════════════════════════════════════════════════════════
    MEASURED 2026-07-28 — this check is the difference between +25 and -50
    ═══════════════════════════════════════════════════════════════════════════
    `retrieval_bench` scored the retrieval layer at **Δ -9.16, CI [-17.64, -0.69]** — a
    significant REGRESSION. The diagnostic case: asked *"How should AI systems handle personal
    data?"*, BM25 returned **GDPR Article 47, binding corporate rules** — intra-group transfer
    machinery, nothing to do with the question. The model, instructed to answer ONLY from the
    retrieved text, produced a confident answer about corporate rules and scored 0 where
    answering from its weights scored 50.

    So the grounding instruction converts a retrieval MISS into a wrong answer. And the root
    cause is this session's defect once more: I treated "BM25 returned rows" as "we have the
    statutory basis". **Returning results is not the same as returning relevant results** —
    BM25 always returns its top-k, however poor the match.

    Two ways a hit earns the right to ground an answer:
      • the question NAMES the article — an explicit reference is its own relevance proof
      • the question's content words actually appear in the retrieved text, above a floor

    Failing both, retrieval ABSTAINS and the caller answers from weights **with that recorded**.
    That is not the silent fallback refusal #1 forbids: the silent version claims grounding it
    does not have, this one states plainly that no statute was applicable.
    """
    if not hits:
        return False, "nothing retrieved"
    if re.search(r"\barticles?\s+\d+", question, re.I):
        return True, "question names a specific article"
    words = {w for w in re.findall(r"[a-z]{4,}", question.lower()) if w not in STOP}
    if not words:
        return False, "no content words to match on"
    top = hits[0]["text"].lower()
    overlap = {w for w in words if w in top}
    frac = len(overlap) / len(words)
    if frac >= 0.5:
        return True, f"{len(overlap)}/{len(words)} content words present in top hit"
    return False, (f"only {len(overlap)}/{len(words)} content words in top hit "
                   f"({sorted(words - overlap)[:4]} absent) — topically adjacent, not on point")


def ask(question: str, model: str | None = None, k: int = 4) -> dict:
    """Retrieve, then answer ONLY from what was retrieved."""
    from owem_cluster import ask as call_model, select_expert, classify_dimension
    try:
        hits = search(question, k)
    except NoStatuteFound as e:
        # Refusal 1: no silent fallback to the weights.
        return {"answer": "No statutory basis was retrieved for this question, so I can't "
                          "answer it from the regulation text.",
                "grounded": False, "retrieved": [], "reason": str(e), "abstained": True}

    ok, why = relevant(question, hits)
    if not ok:
        # Retrieval abstains. Recorded, never silent — see `relevant()`.
        return {"answer": None, "grounded": False, "retrieval_abstained": True,
                "reason": why, "retrieved": [h["id"] for h in hits],
                "note": "no applicable statute — caller should answer from weights and say so"}

    if model is None:
        model, _ = select_expert(classify_dimension(question))

    ctx = "\n\n".join(f"[{h['id']}]\n{h['text'][:1800]}" for h in hits)
    prompt = (
        "Answer the question using ONLY the regulation text below. Quote the article you rely "
        "on by number. If the text below does not settle the question, say so explicitly "
        "rather than reasoning from general knowledge.\n\n"
        f"=== REGULATION TEXT ===\n{ctx}\n=== END ===\n\nQuestion: {question}\nAnswer:")
    try:
        answer = call_model(model, prompt)
    except Exception as e:
        return {"answer": None, "unreachable": True, "reason": str(e)[:120],
                "grounded": False, "retrieved": [h["id"] for h in hits]}

    # Refusal 2: citations are checked against THESE retrieved texts, not against a registry.
    #
    # `article_number` comes out of SQLite as an INT and `_cited` yields STRINGS, so the first
    # version computed {'27'} - {27} == {'27'} and declared a correctly grounded answer
    # ungrounded — a false negative on the one signal this layer exists to produce. Normalise.
    got = _cited(answer)
    retrieved_nums = {str(h["article"]) for h in hits}

    # An answer that quotes Art 27 will mention Art 13 because Art 27's own text cross-refers
    # to it. That is a traceable reference, not a fabrication, and collapsing the two would
    # make the check cry wolf on every accurate quotation. Three states, not two.
    crossrefs = {m.group(1) for h in hits
                 for m in re.finditer(r"\bArticles?\s+(\d+)", h["text"], re.I)}
    direct = sorted(got & retrieved_nums)
    via_xref = sorted((got - retrieved_nums) & crossrefs)
    ungrounded = sorted(got - retrieved_nums - crossrefs)

    return {
        "answer": answer,
        "model": model,
        # Refusal 3: grounding is reported, never assumed.
        "grounded": bool(direct) and not ungrounded,
        "cited": sorted(got),
        "cited_retrieved": direct,
        "cited_via_crossref": via_xref,
        "ungrounded_citations": ungrounded,
        "retrieved": [h["id"] for h in hits],
        "abstained": False,
        "note": ("cites articles neither retrieved nor cross-referenced in the retrieved text"
                 if ungrounded else
                 "no article cited — cannot be confirmed grounded" if not got else None),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--search")
    ap.add_argument("--ask")
    ap.add_argument("-k", type=int, default=4)
    a = ap.parse_args()

    if a.search:
        try:
            for h in search(a.search, a.k):
                print(f"  [{h['score']:7.2f}] {h['id']}")
                print(f"            {h['text'][:150].strip()}...\n")
        except NoStatuteFound as e:
            print(f"  no statute found: {e}"); return 1
        return 0

    if a.ask:
        r = ask(a.ask, k=a.k)
        print(f"  Q: {a.ask}\n")
        print(f"  RETRIEVED : {r['retrieved']}")
        print(f"  GROUNDED  : {r['grounded']}")
        print(f"    direct    : {r.get('cited_retrieved')}")
        print(f"    crossref  : {r.get('cited_via_crossref')}")
        if r.get("ungrounded_citations"):
            print(f"  ⚠️  UNGROUNDED CITATIONS: {r['ungrounded_citations']}")
        if r.get("note"):
            print(f"  note      : {r['note']}")
        print(f"\n  {(r['answer'] or '')[:900]}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
