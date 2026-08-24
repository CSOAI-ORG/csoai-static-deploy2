#!/usr/bin/env python3
"""Build the drum's knowledge/index pages (adds the authority/about page)."""
import datetime
import html
import json
import os
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(PACK, "site")
CATALOG = os.path.join(PACK, "catalog.json")


def about_html():
    """The public AUTHORITY / positioning page — the measured-compliance layer story."""
    contam = {}
    gauge = {}
    try:
        c = json.load(open(os.path.join(PACK, "feeds", "benchmark_contamination.json"), encoding="utf-8"))
        contam = {"benchmarks": len(c.get("benchmarks", [])),
                  "resistant": sum(1 for b in c.get("benchmarks", []) if b.get("designed_resistant")),
                  "high": sum(1 for b in c.get("benchmarks", []) if b.get("level") == "high")}
    except Exception:
        pass
    try:
        g = json.load(open(os.path.join(PACK, "feeds", "measured_compliance.json"), encoding="utf-8")).get("measured_gauge", {})
        gauge = {"records": g.get("live_records", 0), "signed": g.get("signed_cards", 0), "axes": len(g.get("axes", []))}
    except Exception:
        pass
    cat = json.load(open(CATALOG))
    n = len(cat["items"])
    body = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FRAMEWORKS DRUM — authority & method</title>
<link rel="canonical" href="https://frameworks-drum.pages.dev/about">
<style>body{{font-family:system-ui,-apple-system,sans-serif;max-width:760px;margin:2rem auto;padding:0 1.2rem;color:#0f172a;line-height:1.7}}
h1{{font-size:1.9rem;margin:0 0 .4rem}} h2{{font-size:1.2rem;margin:1.6rem 0 .4rem}} .lede{{color:#5a5e66}}
table{{border-collapse:collapse;font-size:.85rem;margin:.8rem 0}} th,td{{border:1px solid #e6e8ec;padding:.4rem .6rem;text-align:left}}
a{{color:#0a8a3f}}</style></head><body>
<h1>The measured compliance layer</h1>
<p class="lede">We do not certify. We <b>measure</b>. A reference index of every AI framework,
charter, regulation, and benchmark — and a <b>measured, signed, contamination-aware</b> evaluation layer over it.</p>
<p>The <b>EU AI Act GPAI obligations started 2 Aug 2026</b>. Regulators and enterprises now need
<b>verifiable evaluation evidence</b> — and the model industry is being caught <b>gaming
benchmarks</b>. A measured, contamination-aware evaluation layer is the direct answer.</p>
<h2>What we measure</h2>
<table><tr><th>Asset</th><th>What</th></tr>
<tr><td>Reference index</td><td>{n} sourced instruments (frameworks, charters, regulations, articles, sectors, benchmarks) over MCP/A2A</td></tr>
<tr><td>Measured gauge</td><td>{gauge.get('records',0)} live records, {gauge.get('signed',0)} signed cards, {gauge.get('axes',0)} axes (Fisher-Rao-style trust gauge)</td></tr>
<tr><td>Arena Elo</td><td>Bradley-Terry on our own measured pillars — not market Elo, not crowd-sourced</td></tr>
<tr><td>Contamination register</td><td>{contam.get('benchmarks',0)} benchmarks tracked ({contam.get('resistant',0)} designed-resistant, {contam.get('high',0)} high-leak) — the anti-Goodhart guard</td></tr></table>
<h2>The anti-Goodhart guard</h2>
<p>Benchmarks are being gamed. Our contamination register + designed-resistant probes + signed runs
are the honest counter. We report <b>measured, never certified</b> — unmeasured axes stay
UNMEASURED, and no score is inflated by contamination.</p>
<h2>Where it goes</h2>
<p>Compliance evidence for EU AI Act GPAI, a trust-conformal 90/10 router, a measured arena, and
data licensing of consented eval-transcripts. <b>Measurement, not certification.</b></p>
<p><a href="/index.html">← back to the index</a></p></body></html>"""
    os.makedirs(SITE, exist_ok=True)
    with open(os.path.join(SITE, "about.html"), "w", encoding="utf-8") as fh:
        fh.write(body)
    print("site: about.html (authority page) written")
    return 0


if __name__ == "__main__":
    sys.exit(about_html())
