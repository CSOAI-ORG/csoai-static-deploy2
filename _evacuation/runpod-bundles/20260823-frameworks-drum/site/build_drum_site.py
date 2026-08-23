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
KINDS = ["framework", "charter", "regulation", "article", "sector", "benchmark"]
PAGES = {"framework": "frameworks.html", "charter": "charters.html", "regulation": "regulations.html", "article": "articles.html", "sector": "sectors.html", "benchmark": "benchmarks.html"}
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
        "{eat_box}"
        "<script type='application/ld+json'>{\"@context\":\"https://schema.org\",\"@type\":\"WebPage\",\"name\":\"FRAMEWORKS DRUM\"}</script></body></html>")


def measured_panel():
    """Fused measured-compliance panel (gauge + contamination + arena) on the board overview.
    Doctrine: internal-codename models (sov33/oowm/…) are NEVER shown on a public surface."""
    try:
        import json as _j
        m = _j.load(open(os.path.join(SITE, "..", "feeds", "measured_compliance.json"), encoding="utf-8"))
        g = m.get("measured_gauge", {}); c = m.get("contamination_register", {}); a = m.get("measured_arena_elo", {})
        INTERNAL = ("sov3", "sov33", "oowm", "sigil", "horus", "liquid-kan", "maternal", "byzantine", "bft", "ceasai")
        top = [t for t in a.get("top", []) if not any(x in (t.get("model", "") or "").lower() for x in INTERNAL)][:3]
        top_html = " · ".join(f"{t.get('model','')} ({t.get('elo')})" for t in top) or "public models not shown (internal estate models excluded)"
        axes = g.get("axes", [])
        mean = g.get("mean_of_axes", 0)
        # EU AI Act GPAI evidence (in force since 2 Aug 2026)
        gpai = ""
        try:
            gp = _j.load(open(os.path.join(SITE, "..", "feeds", "gpai_compliance_map.json"), encoding="utf-8"))
            ready = sum(1 for o in gp.get("obligations", []) if "READY" in o.get("status", "") or "MEASURED" in o.get("status", ""))
            gpai = f" EU-AI-Act GPAI evidence: {ready}/{len(gp.get('obligations', []))} obligations READY/MEASURED (in force since 2026-08-02)."
        except Exception:
            pass
        return (f"<div class='note'><b>Measured-compliance gauge:</b> {g.get('live_records',0)} live records, "
                f"{g.get('signed_cards',0)} signed cards, {len(axes)} axes, mean "
                f"{round(mean,4) if isinstance(mean,(int,float)) else '—'}. "
                f"Contamination register: {c.get('benchmarks',0)} benchmarks ({c.get('resistant',0)} designed-resistant, "
                f"{c.get('high',0)} high-leak). Arena Elo (our pillars, not market): {top_html}.{gpai} "
                f"<b>Measurement, not certification.</b></div>")
    except Exception:
        return ""


def status_box():
    """Surface the honest EAT 7-box mission state on the board (counts + feeds + designation only)."""
    try:
        import json as _j
        eat = _j.load(open(os.path.join(SITE, "..", "feeds", "eat_7box.json"), encoding="utf-8"))
        st = eat.get("status", "n/a")
        true = [k for k, b in eat.get("boxes", {}).items() if b.get("ok") is True]
        partial = [k for k, b in eat.get("boxes", {}).items() if b.get("ok") == "partial"]
        low = [k for k, b in eat.get("boxes", {}).items() if b.get("ok") is False]
        return (f"<p class='note'><b>EAT 7-box mission:</b> {st}. true={','.join(sorted(true))} "
                f"· partial={','.join(sorted(partial))} · false={','.join(sorted(low))}. "
                f"<a href='https://frameworks-drum.pages.dev'><b>Measurement, not certification.</b></a></p>")
    except Exception:
        return ""



def clean(text):
    out = str(text or "")
    for c in sorted(INTERNAL, key=len, reverse=True):
        out = re.sub(rf"(?i)\b{re.escape(c)}\b", "[internal]", out)
        out = re.sub(rf"(?i){re.escape(c)}(?=[-_0-9])", "[internal]", out)
    return html.escape(out)


def kind_page(items, kind, counts):
    # contamination column only for benchmarks (anti-Goodhart disclosure, plan P3)
    extra_col = ""
    contam = {}
    if kind == "benchmark":
        try:
            contam = {c["id"]: c for c in json.load(open(os.path.join(PACK, "feeds", "benchmark_contamination.json")))["benchmarks"]}
        except Exception:
            pass
    def contam_cell(kind, i):
        if kind != "benchmark":
            return ""
        c = contam.get(i["id"], {})
        lvl = c.get("level", "—")
        tag = f"<span style='padding:.1rem .35rem;border-radius:.3rem;font-size:.7rem;color:#fff;background:#{('b91c1c' if lvl=='high' else ('d97706' if lvl=='medium' else ('15803d' if lvl=='low' else '#64748b')))}'>{lvl}</span>"
        return f"<td>{tag}</td>"
    rows = "".join(
        f"<tr><td>{clean(i['name'])}</td><td>{clean(i.get('region') or '—')}</td>"
        f"<td>{'yes' if i.get('binding') is True else ('no' if i.get('binding') is False else '—')}</td>"
        f"<td>{clean(i.get('status') or '—')}</td>{contam_cell(kind, i)}</tr>"
        for i in items)
    head_cols = "<th>Name</th><th>Region</th><th>Binding</th><th>Status</th>"
    if kind == "benchmark":
        head_cols += "<th>Contam.</th>"
    nav = "".join(f'<a href="/{PAGES[k]}">{k}s ({counts[k]})</a>' for k in KINDS if k in counts)
    counts_html = "".join(f'<div class="stat"><b>{counts[k]}</b><span>{k}</span></div>' for k in KINDS if k in counts)
    return (HEAD.format(title=f"{kind}s ({len(items)})", desc=f"All {kind}s ({len(items)}) in the reference index — measurement, not certification.")
            + f"<h1>FRAMEWORKS DRUM</h1><nav><a href='/index.html'>Overview</a><a href='/about.html'>About</a>{nav}</nav>"
            + f"<p class='lede'>All {kind}s in the reference index — sorted, sourced, searchable. Reference index; measurement, not certification.</p>"
            + f"<div class='stats'>{counts_html}</div>"
            + f"<p><input id='drumQ' oninput='drumFilter(this.value)' placeholder='Search {kind}s…' style='width:100%;max-width:420px;padding:.5rem .7rem;border:1px solid #cbd5e1;border-radius:.4rem;font-size:.85rem'></p>"
            + f"<table id='drumTab'><thead><tr>{head_cols}</tr></thead><tbody>{rows}</tbody></table>"
            + "<script>function drumFilter(q){q=q.toLowerCase();document.querySelectorAll('#drumTab tbody tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)>=0?'':'none';});}</script>"
            + FOOT.replace("{eat_box}", status_box()))


def main():
    cat = json.load(open(CATALOG))
    items = [i for i in cat["items"] if not i.get("internal")]
    counts = {}
    for i in items:
        counts[i["kind"]] = counts.get(i["kind"], 0) + 1
    sectors = [i for i in items if i.get("kind") == "sector"]
    nav = "".join(f'<a href="/{PAGES[k]}">{k}s ({counts[k]})</a>' for k in KINDS if k in counts)
    counts_html = "".join(f'<div class="stat"><b>{counts[k]}</b><span>{k}</span></div>' for k in KINDS if k in counts)
    sector_html = "".join(
        f'<div class="sector"><h3>{clean(s["name"])}</h3><p>{clean(s.get("description") or "")}</p>'
        f'<p class="meta">Status: {clean(s.get("status") or "—")}</p></div>' for s in sectors)
    overview = (HEAD.format(title="the reference index", desc="Living reference index of AI frameworks, charters, regulations, articles, sectors.")
                + f"<h1>FRAMEWORKS DRUM</h1><nav><a href='/index.html'>Overview</a><a href='/about.html'>About</a>{nav}</nav>"
                + "<p class='lede'>The living <b>reference index</b> of every AI framework, charter, regulation, article, and sector mined by the estate — sorted, sourced, queryable over MCP/A2A. This is the <b>reference index</b>; the measured trust gauge is a separate, measured instrument.</p>"
                + f"<div class='stats'>{counts_html}</div>"
                + f"<p>Generated {datetime.date.today().isoformat()} · {len(items)} public items. Browse each kind as a content page, or query over MCP.</p>"
                + measured_panel()
                + "<h2>Sectors</h2>" + sector_html + FOOT.replace("{eat_box}", status_box()))
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
