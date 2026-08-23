#!/usr/bin/env python3
"""Build the drum's FULL front end — every item as browsable content, all pages.

Emits a doctrine-clean multi-page site:
  index.html       overview (stats, sectors, nav) — the board
  frameworks.html  ALL frameworks, fully browsable
  charters.html    ALL charters
  regulations.html ALL regulations
  articles.html    ALL articles
  sectors.html     ALL sectors
  drum.html        alias of index (old deploy surface stays valid)
  drum.llm.json    LLM summary
No JS cap — every item is pre-rendered (content pages, not a capped table). Doctrine-clean.

Run: python3 site/build_drum_site.py   (regenerated with the catalog; wired into overnight + build)
"""
import datetime
import html
import json
import os
import re
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(PACK, "site")
CATALOG = os.path.join(PACK, "catalog.json")
INTERNAL = ["sov3", "sov33", "oowm", "sigil", "horus", "liquid-kan", "maternal", "byzantine", "bft", "ceasai"]
KINDS = ["framework", "charter", "regulation", "article", "sector"]
PAGES = {"framework": "frameworks.html", "charter": "charters.html", "regulation": "regulations.html", "article": "articles.html", "sector": "sectors.html"}
HEAD = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FRAMEWORKS DRUM — {title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://csoai.org/drum">
<style>
 body{{font-family:system-ui,-apple-system,sans-serif;max-width:1040px;margin:2rem auto;padding:0 1.2rem;color:#0f172a;line-height:1.6}}
 h1{{font-size:2rem;margin:0 0 .25rem}} .lede{{color:#5a5e66;max-width:760px}}
 nav a{{margin-right:1rem;color:#0a8a3f;text-decoration:none}}
 .stats{{display:flex;gap:1rem;flex-wrap:wrap;margin:1.2rem 0}} .stat{{background:#f7f8fa;border:1px solid #e6e8ec;border-radius:.5rem;padding:.7rem 1.1rem;text-align:center}}
 .stat b{{display:block;font-size:1.4rem}} .stat span{{font-size:.72rem;color:#5a5e66;text-transform:uppercase;letter-spacing:.05em}}
 .sector{{background:#fef3c7;border-left:4px solid #d97706;border-radius:.4rem;padding:.8rem 1rem;margin:.6rem 0}}
 .sector h3{{margin:0 0 .2rem}} .sector p{{margin:.2rem 0;font-size:.9rem}} .sector .meta{{color:#92400e;font-size:.8rem}}
 table{{width:100%;border-collapse:collapse;font-size:.82rem;margin-top:.6rem}} th,td{{border:1px solid #e6e8ec;padding:.35rem .5rem;text-align:left;vertical-align:top}}
 th{{background:#f0f9ff;font-weight:600}} .note{{color:#5a5e66;font-size:.85rem;margin-top:2rem;border-top:1px solid #e6e8ec;padding-top:1rem}}
</style></head><body>
"""
FOOT = ("<p class='note'><b>Honest register:</b> reference index — describes and sources; it does not certify or score trust. "
        "Measurement, not certification. Data via MCP (drum_search/drum_get/drum_crosswalk) + feeds/reg_events.json.</p>"
        "<script type='application/ld+json'>{\"@context\":\"https://schema.org\",\"@type\":\"WebPage\",\"name\":\"FRAMEWORKS DRUM\"}</script></body></html>")


def clean(text):
    out = str(text or "")
    for c in sorted(INTERNAL, key=len, reverse=True):
        out = re.sub(rf"(?i)\b{re.escape(c)}\b", "[internal]", out)
        out = re.sub(rf"(?i){re.escape(c)}(?=[-_0-9])", "[internal]", out)
    return html.escape(out)


def kind_page(items, kind, counts):
    rows = "".join(
        f"<tr><td>{clean(i['name'])}</td><td>{clean(i.get('region') or '—')}</td>"
        f"<td>{'yes' if i.get('binding') is True else ('no' if i.get('binding') is False else '—')}</td>"
        f"<td>{clean(i.get('status') or '—')}</td></tr>"
        for i in items)
    nav = "".join(f'<a href="/{PAGES[k]}">{k}s ({counts[k]})</a>' for k in KINDS if k in counts)
    counts_html = "".join(f'<div class="stat"><b>{counts[k]}</b><span>{k}</span></div>' for k in KINDS if k in counts)
    return (HEAD.format(title=f"{kind}s ({len(items)})", desc=f"All {kind}s ({len(items)}) in the reference index — measurement, not certification.")
            + f"<h1>FRAMEWORKS DRUM</h1><nav><a href='/index.html'>Overview</a>{nav}</nav>"
            + f"<p class='lede'>All {kind}s in the reference index — sorted, sourced. Reference index; measurement, not certification.</p>"
            + f"<div class='stats'>{counts_html}</div>"
            + f"<table><thead><tr><th>Name</th><th>Region</th><th>Binding</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>"
            + FOOT)


def main():
    cat = json.load(open(CATALOG))
    items = [i for i in cat["items"] if not i.get("internal")]
    counts = {}
    for i in items:
        counts[i["kind"]] = counts.get(i["kind"], 0) + 1
    sectors = [i for i in items if i.get("kind") == "sector"]
    nav = "".join(f'<a href="/{k}.html">{k}s ({counts[k]})</a>' for k in KINDS if k in counts)
    counts_html = "".join(f'<div class="stat"><b>{counts[k]}</b><span>{k}</span></div>' for k in KINDS if k in counts)
    sector_html = "".join(
        f'<div class="sector"><h3>{clean(s["name"])}</h3><p>{clean(s.get("description") or "")}</p>'
        f'<p class="meta">Status: {clean(s.get("status") or "—")}</p></div>' for s in sectors)
    overview = (HEAD.format(title="the reference index", desc="Living reference index of AI frameworks, charters, regulations, articles, sectors.")
                + f"<h1>FRAMEWORKS DRUM</h1><nav>{nav}</nav>"
                + "<p class='lede'>The living <b>reference index</b> of every AI framework, charter, regulation, article, and sector mined by the estate — sorted, sourced, queryable over MCP/A2A. This is the <b>reference index</b>; the measured trust gauge is a separate, measured instrument.</p>"
                + f"<div class='stats'>{counts_html}</div>"
                + f"<p>Generated {datetime.date.today().isoformat()} · {len(items)} public items. Browse each kind as a content page, or query over MCP.</p>"
                + "<h2>Sectors</h2>" + sector_html + FOOT)
    out = {"index.html": overview}
    for k in KINDS:
        if k in counts:
            out[PAGES[k]] = kind_page([i for i in items if i["kind"] == k], k, counts)

    os.makedirs(SITE, exist_ok=True)
    for name, doc in out.items():
        with open(os.path.join(SITE, name), "w", encoding="utf-8") as fh:
            fh.write(doc)
    with open(os.path.join(SITE, "drum.html"), "w", encoding="utf-8") as fh:
        fh.write(out["index.html"])
    llm = {"title": "FRAMEWORKS DRUM — the reference index", "type": "LLMPageSummary",
           "summary": f"{len(items)} public items across {len(counts)} kinds, {len(sectors)} sectors; doctrine-clean; MCP/A2A queryable; content pages: index + frameworks/charters/regulations/articles/sectors",
           "counts": counts, "sector_count": len(sectors), "pages": list(out.keys())}
    with open(os.path.join(SITE, "drum.llm.json"), "w", encoding="utf-8") as fh:
        json.dump(llm, fh, indent=1)
    print(f"site: {len(out)} content pages ({', '.join(out.keys())}) — {len(items)} public items")


if __name__ == "__main__":
    sys.exit(main())
