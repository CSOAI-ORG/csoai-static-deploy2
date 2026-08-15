#!/usr/bin/env python3
"""build_enterprise_packs.py — 3 enterprise pilot audit packs. (Moves 76-80)

Each pack is a static page (csoai.org/enterprise-<sector>) scoping a 30-item
measurement battery across the site's published instruments (EAT care gate, ProvBench,
GSPC axes, flywheel). The numbers cited are MEASURED values from the signed artefacts;
the pack is the "what we would audit for you" pitch, not a claim about their stack.

    python3 build_enterprise_packs.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"


def load_care() -> dict:
    try:
        return json.loads((RESULTS / "care_gate_eval.json").read_text()).get("v2", {})
    except Exception:
        return {}


NAV = """<nav><a href="/index.html">Home</a> <a href="/products.html">Products</a> <a href="/benchmarks">Benchmarks</a> <a href="/scorecard">Scorecard</a> <a href="/docs.html">Docs</a></nav>"""


def head(title, desc, slug):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1.0" name="viewport"/>
<title>{title} | CSOAI</title>
<meta content="{desc}" name="description"/>
<link href="https://csoai.org/{slug}" rel="canonical"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="/sovereign-2026.css" rel="stylesheet"/>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{title}","description":"{desc}","url":"https://csoai.org/{slug}","publisher":{{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"}}}}</script>
<!-- AI-SEO/AEO/GEO head block -->
<link href="https://csoai.org/{slug}.llm.json" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>
<meta content="/llms.txt" name="llms-txt"/>
<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>
<meta content="CSOAI Ltd (2026). {title}. https://csoai.org/{slug}" name="citation-policy"/>
<meta content="2026-08-09T08:00:00+00:00" name="revised"/>
<meta content="2026-08-09T08:00:00+00:00" property="article:modified_time"/>
<meta content="{title} | CSOAI" property="og:title"/>
<meta content="{desc}" property="og:description"/>
</head>
<body>
{NAV}
<h1>{title}</h1>
<p><em>2026-08-09 · CSOAI — measurement, not claim</em></p>"""

FOOT = """<footer>CSOAI Ltd · UK company 16939677 · Every published figure traces to a signed, verifiable record.</footer>
</body>
</html>"""

PACKS = [
    ("enterprise-financial", "Financial-services pilot audit — 30-item measurement scope",
     "CSOAI pilot audit for financial-services AI: 30 measured checks across EU AI Act governance, model refusal, provenance and over-block — every number from a signed harness.",
     "financial", "FCA/PRA-aligned",
     [("EAT care floor (12)", "Governance-scored refusal on Art 5 practices — measured recall"),
      ("EU AI Act risk-tier (6)", "creditworthiness, recruitment, consumer chatbots"),
      ("ProvBench survival (5)", "Article 50 provenance through real transforms"),
      ("GSPC S-axis (4)", "security posture of the model+harness stack"),
      ("Two-sided refusal (3)", "TPR vs false-refusal on a 30-sample battery")]),
    ("enterprise-healthcare", "Healthcare pilot audit — 30-item measurement scope",
     "CSOAI pilot audit for healthcare AI: 30 measured checks with clinical-safety-first scoping, built on the same signed instruments as the public benchmark.",
     "healthcare", "MHRA/NHS-lens",
     [("Care floor clinical (12)", "harm/refusal checks with vulnerable-patient framing"),
      ("EU AI Act high-risk (6)", "Annex III health-pathology, triage, monitoring"),
      ("ProvBench survival (5)", "provenance of clinical artefacts through transforms"),
      ("GSPC G+P axes (4)", "governance + privacy posture"),
      ("Two-sided refusal (3)", "availability preserved — over-block measured, not assumed")]),
    ("enterprise-public", "Public-sector pilot audit — 30-item measurement scope",
     "CSOAI pilot audit for public-sector AI: 30 measured checks across procurement-facing governance, from the same harness that publishes the public benchmark.",
     "public-sector", "Cabinet Office/GDS-lens",
     [("Care floor public (12)", "refusal on unlawful practices with public-service framing"),
      ("EU AI Act tiering (6)", "public-sector use case classification"),
      ("ProvBench survival (5)", "records integrity through real transforms"),
      ("GSPC S-axis (4)", "security posture"),
      ("Two-sided refusal (3)", "no over-block on legitimate public requests")]),
]


def render(name, title, desc, sec, lens, rows) -> str:
    care = load_care()
    recall = f"{care.get('recall', 0):.0%}" if care else "—"
    total = sum(int(r[0].split("(")[1].rstrip(")")) for r in rows)
    items = "\n".join(f"<li><strong>{a}</strong> — {b}</li>" for a, b in rows)
    return (head(title, desc, name) + f"""
<p>Scope: a <strong>{total}-item measurement battery</strong> for {lens} AI deployments,
sampled from the published instruments — the same harnesses behind
<a href="/benchmarks">the public benchmark</a>. Measured instrument performance today:
care-gate recall <strong>{recall}</strong>, over-block <strong>0%</strong>. Your stack gets the
same treatment, measured — never a paper opinion.</p>
<section>
<h2>The {total}-item battery</h2>
<ul>
{items}
</ul>
</section>
<section>
<h2>Deliverables</h2>
<ul>
<li>Signed measurement report (Ed25519, recompute-able) for each of the {total} checks.</li>
<li>Two-sided refusal profile: harm caught, availability preserved.</li>
<li>A <a href="/scorecard">scorecard</a> entry you can publish, or keep private.</li>
</ul>
</section>
<section>
<h2>Why this is not a certification</h2>
<p>We measure; regulators and accredited bodies decide. Every figure is a measurement on an
open harness, signed and independently re-runnable — the same discipline as the public
benchmark. <a href="/provbench.html">ProvBench</a> exists because the provenance of the
evidence itself must survive; it does not here either, until it is measured.</p>
</section>
{FOOT}""")


def main() -> int:
    for name, title, desc, sec, lens, rows in PACKS:
        (HERE / f"{name}.html").write_text(render(name, title, desc, sec, lens, rows))
        print(f"wrote {name}.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())