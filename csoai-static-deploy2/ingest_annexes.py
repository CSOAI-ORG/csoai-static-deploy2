#!/usr/bin/env python3
"""ingest_annexes.py — put the annexes into the corpus. They were never there.

═══════════════════════════════════════════════════════════════════════════════
THE GAP THIS CLOSES
═══════════════════════════════════════════════════════════════════════════════
Measured 2026-07-29 against `regulations.db` (404 articles, 6 instruments):

    "creditworth" anywhere in the corpus : 0
    annex rows                           : 0
    AI Act articles citing "Annex III"   : 20   (all dangling)

Article 27(1) scopes its duty to *"deployers of high-risk AI systems referred to in points
5 (b) and (c) of **Annex III**"*. The word *creditworthiness* lives in Annex III. So when
`sov_whole` answered "Article 27 does not explicitly address private credit-scoring
deployers", the corpus genuinely could not have told it otherwise — **the operative text was
not in the database.**

That reframes the whole retrieval result. `retrieval_bench` measured Δ -5.26 and we concluded
a 0.5B model cannot use statute. Part of that may instead be that we were feeding it statute
with the definitions cut out. Neither explanation is established; this removes one of them so
the next measurement can distinguish them.

It also means **CAD would have made the Article 27 case worse** — CAD suppresses the
parametric prior and amplifies context, and the prior was the only place the model could learn
that Annex III 5(b) means creditworthiness. Ingesting the annexes has to happen first or that
experiment tests the wrong thing.

═══════════════════════════════════════════════════════════════════════════════
SCHEMA — negative article_number, no migration
═══════════════════════════════════════════════════════════════════════════════
`articles` is `UNIQUE(celex, article_number)` with an INTEGER key, and an external-content
FTS5 index over it. Rather than migrate, annexes take **negative** numbers:

    Annex I -> -1 ... Annex XIII -> -13,  article_id = "ANNEX III"

Negative keys cannot collide with any article, sort clear of them, and are trivially
identifiable. `get_article()` keeps working unchanged; `get_annex()` is added alongside.

    python3 ingest_annexes.py --celex 32024R1689 --dry-run
    python3 ingest_annexes.py --celex 32024R1689 --write
"""
from __future__ import annotations

import argparse, re, ssl, sqlite3, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "mcp-marketplace" / "eu-ai-act-compliance-mcp" / "data" / "regulations.db"
EURLEX = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}"

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
         "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13}


class IngestFailed(Exception):
    """Could not obtain or parse the source. NOT an empty result set."""


def fetch(celex: str) -> str:
    import certifi
    ctx = ssl.create_default_context(cafile=certifi.where())
    req = urllib.request.Request(EURLEX.format(celex=celex),
                                 headers={"User-Agent": "csoai-corpus/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
            html = r.read().decode("utf-8", "replace")
    except Exception as e:
        # A network failure is UNMEASURED, not "no annexes found". The EUR-Lex monitor in
        # this estate reported "no updates detected" through 240 SSL failures for 75 days.
        raise IngestFailed(f"fetch failed for {celex}: {type(e).__name__}: {str(e)[:120]}")
    if len(html) < 50_000:
        raise IngestFailed(f"suspiciously small response for {celex}: {len(html)} chars")
    return html


def strip_tags(fragment: str) -> str:
    txt = re.sub(r"(?is)<(script|style).*?</\1>", " ", fragment)
    txt = re.sub(r"(?i)<br\s*/?>", "\n", txt)
    txt = re.sub(r"(?i)</(p|div|tr|li|h[1-6])>", "\n", txt)
    txt = re.sub(r"<[^>]+>", " ", txt)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#8217;", "'"), ("&#8216;", "'"),
                 ("&#8220;", '"'), ("&#8221;", '"'), ("&#160;", " ")):
        txt = txt.replace(a, b)
    txt = re.sub(r"[ \t\xa0]+", " ", txt)
    txt = re.sub(r"\n\s*\n\s*\n+", "\n\n", txt)
    return txt.strip()


def extract(html: str) -> list[tuple[int, str, str]]:
    """Return [(annex_int, label, text)], split on ANNEX headings in document order."""
    marks = [(m.start(), m.group(1).upper())
             for m in re.finditer(r"ANNEX\s+([IVXLC]{1,5})\b", html)]
    # Keep the LAST occurrence of each numeral — earlier ones are table-of-contents links.
    last: dict[str, int] = {}
    for pos, num in marks:
        if num in ROMAN:
            last[num] = pos
    if not last:
        raise IngestFailed("no ANNEX headings found in the source HTML")
    ordered = sorted(last.items(), key=lambda kv: kv[1])
    out = []
    for i, (num, pos) in enumerate(ordered):
        end = ordered[i + 1][1] if i + 1 < len(ordered) else len(html)
        text = strip_tags(html[pos:end])
        if len(text) < 120:
            continue                       # too short to be the real annex body
        out.append((ROMAN[num], f"ANNEX {num}", text))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--celex", default="32024R1689")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not DB.exists():
        print(f"  corpus missing at {DB}"); return 2
    print(f"  INGEST ANNEXES — {a.celex}\n")
    annexes = extract(fetch(a.celex))
    print(f"  extracted {len(annexes)} annexes")
    for n, label, text in annexes:
        print(f"    {label:12s} {len(text):7,d} chars   {text[:64]!r}")

    # The point of the whole exercise, checked explicitly.
    joined = "\n".join(t for _, _, t in annexes).lower()
    for probe in ("creditworth", "biometric", "employment"):
        print(f"\n  probe {probe!r:16s} present in extracted annexes: {probe in joined}")
    if "creditworth" not in joined:
        print("\n  ❌ 'creditworth' still absent — the extraction did not capture Annex III "
              "point 5(b). Refusing to write a corpus that would not answer the question "
              "this exists to answer.")
        return 1

    if a.dry_run or not a.write:
        print(f"\n  dry run — nothing written. Re-run with --write.")
        return 0

    con = sqlite3.connect(DB)
    ins = 0
    try:
        for n, label, text in annexes:
            con.execute(
                "INSERT OR REPLACE INTO articles (celex, article_number, article_id, "
                "content, content_length) VALUES (?,?,?,?,?)",
                (a.celex, -n, label, text, len(text)))
            ins += 1
        con.execute("INSERT INTO articles_fts(articles_fts) VALUES('rebuild')")
        con.commit()
    finally:
        con.close()

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    hits = con.execute("SELECT article_id FROM articles WHERE celex=? AND "
                       "lower(content) LIKE '%creditworth%'", (a.celex,)).fetchall()
    fts = con.execute("SELECT count(*) FROM articles_fts WHERE articles_fts MATCH "
                      "'creditworthiness'").fetchone()[0]
    con.close()
    print(f"\n  ✅ wrote {ins} annexes")
    print(f"  'creditworth' now appears in: {[h[0] for h in hits]}")
    print(f"  FTS index returns {fts} rows for 'creditworthiness'")
    if not hits or fts == 0:
        print(f"  ❌ written but not findable — FTS rebuild did not take.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
