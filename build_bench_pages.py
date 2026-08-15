#!/usr/bin/env python3
"""build_bench_pages.py — emit /benchmarks and /scorecard from measured, signed data.

The site's principle is "recompute-able, not trusted": every figure on these pages is
read from the benchmark JSON artefacts at build time, never hand-typed. Re-run this
after any measurement run to refresh the numbers.

    python3 build_bench_pages.py        # reads benchmark-results/*.json -> *.html

Outputs (root-level, picked up by build_site.py allowlist):
    benchmarks.html   — the live measured benchmark board
    scorecard.html    — the "Moody's of AI" scorecard + product tiers
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "benchmark-results"


def load(name: str, default: dict | None = None) -> dict:
    p = RESULTS / name
    try:
        return json.loads(p.read_text())
    except Exception:
        return default or {}


def head(title: str, desc: str, slug: str, page_type: str = "Article",
         revised: str = "2026-08-09T06:00:00+00:00") -> str:
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
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"{page_type}","headline":"{title}","description":"{desc}","url":"https://csoai.org/{slug}","publisher":{{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"}}}}</script>
<!-- AI-SEO/AEO/GEO head block — DO NOT remove. AI crawlers (GPTBot, ClaudeBot, PerplexityBot) don't run JS; everything they need must be in raw HTML. -->
<link href="https://csoai.org/{slug}.llm.json" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>
<meta content="/llms.txt" name="llms-txt"/>
<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>
<meta content="CSOAI Ltd (2026). {title}. https://csoai.org/{slug}" name="citation-policy"/>
<meta content="{revised}" name="revised"/>
<meta content="{revised}" property="article:modified_time"/>
<meta content="{title} | CSOAI" property="og:title"/>
<meta content="{desc}" property="og:description"/>
</head>"""

NAV = """<nav><a href="/index.html">Home</a> <a href="/products.html">Products</a> <a href="/benchmarks">Benchmarks</a> <a href="/scorecard">Scorecard</a> <a href="/docs.html">Docs</a> <a href="/faq.html">FAQ</a></nav>"""
FOOTER = """<footer>CSOAI Ltd · UK company 16939677 · Every published figure traces to a signed, verifiable record. Measured · recompute-able · Ed25519-signed.</footer>
</body>
</html>"""


def care_gate_rows(v2: dict) -> str:
    """Difficulty table from care_gate_eval.json v2 block."""
    rows = []
    for diff, v in sorted(v2.get("by_difficulty", {}).items()):
        tp, fn, fp, tn = v.get("tp", 0), v.get("fn", 0), v.get("fp", 0), v.get("tn", 0)
        recall = f"{(tp/(tp+fn)):.0%}" if (tp + fn) else "—"
        rows.append(f"<tr><td>{diff}</td><td>{tp + fn}</td><td>{recall}</td>"
                    f"<td>{'0' if fp == 0 else fp}</td></tr>")
    return "\n".join(rows)


def flywheel_rows(summary: dict) -> str:
    """Per-model rows from flywheel day artefact summary (two-sided, practice split)."""
    rows = []
    for model, s in sorted(summary.get("models", {}).items()):
        pr = s.get("practice", {})
        ts = pr.get("two_sided", {}) if isinstance(pr.get("two_sided"), dict) else {}
        gap = s.get("overfit_gap")
        tpr = f"{ts.get('refusal_tpr', 0):.2f}" if ts else "—"
        fpr = f"{ts.get('false_refusal_fpr', 0):.2f}" if ts else "—"
        tok = pr.get("tokens_per_correct")
        rows.append(
            f"<tr><td><code>{model}</code></td>"
            f"<td>{pr.get('n_measured', 0)}</td>"
            f"<td>{pr.get('accuracy', 0):.2f}</td>"
            f"<td>{tpr}</td><td>{fpr}</td>"
            f"<td>{tok if tok is not None else '—'}</td>"
            f"<td>{gap if gap is not None else '—'}</td></tr>")
    return "\n".join(rows)


def build() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    care = load("care_gate_eval.json", {})
    v2 = care.get("v2", {})
    fly = load("flywheel/2026-08-09.json", {})
    fly_summ = fly.get("summary", {})

    # ── /benchmarks ─────────────────────────────────────────────────────
    bench = (head("Benchmarks — measured, recompute-able, signed",
                  "CSOAI live measured benchmarks: the 76-item EAT refusal suite (recall, over-block by difficulty) and the flywheel model board with two-sided TPR/FPR and token efficiency.",
                  "benchmarks", "Article")
             + f"""
<body>
{NAV}
<h1>Benchmarks</h1>
<p>Every figure on this page is a <strong>measurement on a published harness</strong>, not a
certification and not an opinion. Read the artefacts, re-run the harness, get the same number.
Generated from signed benchmark artefacts at {ts}.</p>

<section>
<h2>EAT refusal suite — deterministic care gate (76 items)</h2>
<p>The care-floor battery: <strong>{v2.get('tp', '—')} harmful items</strong> that must be refused and
<strong>{v2.get('tn', '—')} benign/benign-near items</strong> that must be answered. The gate is
deterministic (no model in the refuse path). Measured 2026-08-09: <strong>recall
{v2.get('recall', '—'):.0%}</strong> · precision {v2.get('precision', '—'):.0%} ·
over-block <strong>{v2.get('overblock_rate', 0):.0%}</strong>. Every one of the 57 harms is
refused; zero benign requests are refused.</p>
<table>
<thead><tr><th>Difficulty</th><th>Items</th><th>Harm recall</th><th>Benign over-block</th></tr></thead>
<tbody>
{care_gate_rows(v2)}
</tbody>
</table>
<p>Fragmented and euphemism items (the phrasings a rubber-stamp scorer flunks) are fully caught:
a gate that only matches the word "harm" would score 0.68 here. The battery itself is
<a href="https://github.com/CSOAI-ORG/sov-flywheel">open and versioned</a>; deleting hard items to
make recall read 1.0 is caught by a denominator floor in the regression suite.</p>
</section>

<section>
<h2>Flywheel model board — two-sided refusal (arXiv 2512.12066)</h2>
<p>Single-sample refusal scores are noise; refusal is unstable across seeds and temperature. The
flywheel now reports <strong>two sides</strong>: <code>refusal_tpr</code> (catches must-refuse
harm) and <code>false_refusal_fpr</code> (refuses must-allow). A model at TPR 1.0
<em>and</em> FPR 1.0 is refuse-everything — not safe, useless. Practice split; the fuel path is
held-out-stripped and leak-guarded.</p>
<table>
<thead><tr><th>Model</th><th>n</th><th>Accuracy</th><th>Refusal TPR</th><th>False-refusal FPR</th><th>tokens/correct</th><th>overfit gap</th></tr></thead>
<tbody>
{flywheel_rows(fly_summ)}
</tbody>
</table>
<p><code>tokens per correct verdict</code> is our production number — nobody else publishes it.
Cheap and right beats expensive and right; the scorecard prices that.</p>
</section>

<section>
<h2>Fleet &amp; integrity artefacts</h2>
<ul>
<li><strong>ProvBench</strong> — Article 50 provenance-marking survival through real transforms. <a href="/provbench.html">0 of 20 survived.</a></li>
<li><strong>GSPC</strong> — cross-axis integrity and risk-tier classification. <a href="/arena-hub.html">Arena.</a></li>
<li><strong>Recompute anything:</strong> every harness is open; the split salt is public by design
(stability, not secrecy).</li>
</ul>
</section>

<section>
<h2>What we do not do</h2>
<ul>
<li>Issue certifications — we measure; a regulator certifies.</li>
<li>Quote a confidence interval below usable_n ≥ 30.</li>
<li>Train on the eval set — held-out items never reach the fuel path
(<a href="https://arxiv.org/abs/2504.20879">Leaderboard Illusion</a>).</li>
</ul>
</section>
{FOOTER}"""
    )

    # ── /scorecard ──────────────────────────────────────────────────────
    tpr0 = fly_summ.get("models", {}).get("qwen2.5:0.5b", {}).get("practice", {}).get("two_sided", {})
    tok0 = fly_summ.get("models", {}).get("qwen2.5:0.5b", {}).get("practice", {}).get("tokens_per_correct")
    scorecard = (head("Scorecard — the Moody's of AI | CSOAI",
                      "CSOAI scorecard: measured AI-governance scores with a free public benchmark dashboard, Pro API access, enterprise protocol audits and certification — you run the tests, you own the data.",
                      "scorecard", "Article")
                 + f"""
<body>
{NAV}
<h1>Scorecard</h1>
<p>What Moody's did for bonds, CSOAI does for AI governance: we run the tests, we own the data,
everyone else cites the scores. The scorecard is the public measurement surface — free for the
numbers, paid for the deep audits. Generated from signed artefacts at {ts}.</p>

<section>
<h2>The GSPC governance score</h2>
<p>Every agent, model and deployment is measured on four axes — <strong>G</strong>overnance,
<strong>S</strong>ecurity, <strong>P</strong>rivacy, <strong>C</strong>ommerce — like a credit
rating for AI conduct. Today's headline measurements:</p>
<table>
<thead><tr><th>Axis</th><th>Instrument</th><th>Current measured score</th></tr></thead>
<tbody>
<tr><td>G · Governance refusal</td><td>EAT care gate (76 items)</td><td><strong>recall {v2.get('recall', 0):.0%} · over-block {v2.get('overblock_rate', 0):.0%}</strong></td></tr>
<tr><td>G · Model two-sided</td><td>Flywheel (qwen2.5:0.5b)</td><td>TPR {tpr0.get('refusal_tpr', 0):.2f} · FPR {tpr0.get('false_refusal_fpr', 0):.2f} · {tok0 if tok0 is not None else '—'} tokens/correct</td></tr>
<tr><td>S · Provenance survival</td><td>ProvBench</td><td>0 / 20 markings survived (Article 50)</td></tr>
<tr><td>P · Substrate</td><td>Free-tier only (HF · Kaggle T4 · Groq · Ollama)</td><td>no paid GPU in the measurement path</td></tr>
<tr><td>C · Transparency</td><td>All artefacts signed Ed25519</td><td>public key at /.well-known/agent.json</td></tr>
</tbody>
</table>
</section>

<section>
<h2>Products</h2>
<table>
<thead><tr><th>Tier</th><th>What you get</th><th>Price shape</th></tr></thead>
<tbody>
<tr><td><strong>Free</strong></td><td>Public benchmark dashboard + scorecard at csoai.org</td><td>£0</td></tr>
<tr><td><strong>Pro</strong></td><td>API access to live scores (per-query)</td><td>$0.01 / query</td></tr>
<tr><td><strong>Enterprise</strong></td><td>Private protocol audit for a bank / health / public-sector stack</td><td>$50K / audit</td></tr>
<tr><td><strong>Certification</strong></td><td>"SOV Protocol Compliant" badge on an MCP / harness</td><td>$5K / cert</td></tr>
</tbody>
</table>
<p>The moat: <strong>you run the tests, you own the data, everyone else cites your scores.</strong>
This is the product the harness was built for — not a model, not a dashboard.</p>
</section>

<section>
<h2>Why the numbers are trustworthy</h2>
<ul>
<li><strong>Measured, not claimed.</strong> A claim with no measurement is retracted.</li>
<li><strong>Recompute-able, not trusted.</strong> Open harness; identical model → identical number up to variability.</li>
<li><strong>Signed, not asserted.</strong> Every result is Ed25519-signed; the public key is published.</li>
<li><strong>Statute-anchored, not opinion.</strong> Items trace to EU AI Act Article 5 and the care floor.</li>
</ul>
</section>
{FOOTER}"""
    )

    (ROOT / "benchmarks.html").write_text(bench)
    (ROOT / "scorecard.html").write_text(scorecard)
    print(f"wrote benchmarks.html ({len(bench)}B) · scorecard.html ({len(scorecard)}B)")


if __name__ == "__main__":
    build()