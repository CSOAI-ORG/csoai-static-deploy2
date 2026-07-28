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


def _cited(answer: str) -> set[str]:
    """Article references the answer actually makes."""
    return {m.group(1) for m in re.finditer(r"\bArticles?\s+(\d+)", answer, re.I)}


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
