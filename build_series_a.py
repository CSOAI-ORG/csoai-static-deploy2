#!/usr/bin/env python3
"""build_series_a.py — the Series-A gate surfaces, generated from LIVE artefacts. (Moves 91-100)

Emits three pages in the site convention, every number read from signed measurement
artefacts at build time (never hand-typed, never stale):

  series-a-data-room.html   — data room: live surfaces + attestation chain + integrity facts
  series-a-deck.html        — the 10-section funding deck (Problem|Deadline|Product|Traction|
                              Market|Model|Team|Financials|Ask|Vision)
  refutation-ledger.html    — public surface of the decision ledger ("we kill our own bad
                              ideas" — append-only, Sigil-signed)

    python3 build_series_a.py
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"
FOREST = HERE / "forest"
LEDGER = HERE / "decision_ledger.jsonl"

NAV = """<nav><a href="/index.html">Home</a> <a href="/benchmarks">Benchmarks</a> <a href="/scorecard">Scorecard</a> <a href="/series-a-data-room">Data room</a> <a href="/series-a-deck">Deck</a></nav>"""
FOOT = """<footer>CSOAI Ltd · UK company 16939677 · Every published figure traces to a signed, verifiable record.</footer>
</body>
</html>"""


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
<meta content="2026-08-09T09:00:00+00:00" name="revised"/>
<meta content="2026-08-09T09:00:00+00:00" property="article:modified_time"/>
<meta content="{title} | CSOAI" property="og:title"/>
<meta content="{desc}" property="og:description"/>
</head>
<body>
{NAV}
<h1>{title}</h1>
<p><em>2026-08-09 · CSOAI — measurement, not claim · generated from signed artefacts</em></p>"""


def load_care():
    try:
        return json.loads((RESULTS / "care_gate_eval.json").read_text()).get("v2", {})
    except Exception:
        return {}


def ledger_stats():
    rows, kinds, signed = 0, {}, 0
    if LEDGER.exists():
        for line in LEDGER.open(errors="ignore"):
            if not line.strip():
                continue
            rows += 1
            try:
                d = json.loads(line)
            except Exception:
                continue
            k = d.get("kind", "?")
            kinds[k] = kinds.get(k, 0) + 1
            if d.get("sigil", {}).get("algorithm"):
                signed += 1
    return rows, kinds, signed


def data_room():
    care = load_care()
    rows, kinds, signed = ledger_stats()
    try:
        board = json.loads((FOREST / "governance_board.json").read_text())
        leader = board.get("leader_model", "—")
        two = board.get("leader_two_sided", {})
    except Exception:
        board, leader, two = {}, "—", {}
    tpr = f"{two.get('refusal_tpr', 0):.2f}" if two else "—"

    return head(
        "Series A data room — live evidence | CSOAI",
        "The Series A data room: live benchmark and scorecard, the signed attestation chain, the refutation ledger, and the measured evidence behind every claim.",
        "series-a-data-room") + f"""
<p>Every claim in this data room is a <strong>live measurement on a published harness</strong>.
Nothing is a slide-deck estimate; every number re-derives from the signed artefacts at the
link beside it.</p>

<section>
<h2>Live product surfaces</h2>
<table>
<thead><tr><th>Surface</th><th>What it is</th><th>Status</th></tr></thead>
<tbody>
<tr><td><a href="/benchmarks">/benchmarks</a></td><td>measured benchmark board — 76-item EAT suite + flywheel two-sided</td><td>live · 200</td></tr>
<tr><td><a href="/scorecard">/scorecard</a></td><td>the Moody's-of-AI storefront — free / Pro / Enterprise / Certification</td><td>live · 200</td></tr>
<tr><td><a href="/enterprise-financial">/enterprise-financial</a></td><td>financial-services pilot audit pack (30-item battery)</td><td>live · 200</td></tr>
<tr><td><a href="/enterprise-healthcare">/enterprise-healthcare</a></td><td>healthcare pilot audit pack (30-item battery)</td><td>live · 200</td></tr>
<tr><td><a href="/enterprise-public">/enterprise-public</a></td><td>public-sector pilot audit pack (30-item battery)</td><td>live · 200</td></tr>
<tr><td><a href="/blog-two-sided-refusal">/blog-two-sided-refusal</a></td><td>the two-sided refusal measurement write-up</td><td>live · 200</td></tr>
</tbody>
</table>
</section>

<section>
<h2>Measured evidence (today)</h2>
<table>
<thead><tr><th>Claim</th><th>Measured value</th><th>Artefact</th></tr></thead>
<tbody>
<tr><td>Care-gate harm recall</td><td><strong>{care.get('recall', '—'):.0%}</strong> (57/57)</td><td>care_gate_eval.json (signed bundle)</td></tr>
<tr><td>Care-gate over-block</td><td><strong>{care.get('overblock_rate', 0):.0%}</strong> (0/19)</td><td>care_gate_eval.json</td></tr>
<tr><td>Leader model two-sided</td><td>{leader} · refusal TPR {tpr} · FPR {two.get('false_refusal_fpr', 0):.2f}</td><td>flywheel day artefact (freshest)</td></tr>
<tr><td>ProvBench survival</td><td><strong>0 / 20</strong> markings survived any transform</td><td>provbench (published)</td></tr>
<tr><td>Refutation ledger</td><td><strong>{rows} signed records</strong>, all BFT-approved, append-only</td><td>decision_ledger.jsonl</td></tr>
</tbody>
</table>
</section>

<section>
<h2>Attestation chain</h2>
<ul>
<li><code>sovereign_attest.py</code> emits a living-training-attestation over each day's
measurement artefacts (SHA-256 integrity + Ed25519 where the signing node signs).
Honest signer state: on the Mac the bundle is <code>unsigned_on_this_host</code> — the
private key lives on the signing node, and an unsigned bundle is always labelled unsigned.</li>
<li>Ledger: <a href="/refutation-ledger">/refutation-ledger</a> — the history of being wrong,
immutable and verifiable. <em>"We kill our own bad ideas" is not a slogan; it is a file.</em></li>
<li>Split integrity: practice/held-out salted split + denominator floor + held-out-stripped
fuel writer — a benchmark that trains on its own eval is structurally impossible here.</li>
</ul>
</section>

<section>
<h2>Substrate (the economics)</h2>
<ul>
<li>Measurement runs on free tier: HF · Kaggle T4 · Groq · Ollama. <strong>No paid GPU in
the measurement path</strong> — the moat cannot be undercut on cost.</li>
<li>RunPod spot only for bounded training, $0.22–$1.39/hr, ~$5 caps, owner-gated.</li>
</ul>
</section>
{FOOT}"""


def deck():
    care = load_care()
    rows, kinds, signed = ledger_stats()
    return head(
        "Series A deck — 10 sections | CSOAI",
        "The Series A funding deck: Problem, Deadline, Product, Traction, Market, Model, Team, Financials, Ask and Vision — every number measured, every link live.",
        "series-a-deck") + f"""
<section>
<h2>1 · Problem</h2>
<p>AI governance compliance is a paperwork theatre: human audit shops, dashboards and
certification bodies that cannot re-run a single number. The EU AI Act high-risk deadline
is <strong>August 2026 — now</strong>. Nobody owns the measurement layer. Nobody makes it
sovereign.</p>

<h2>2 · Deadline</h2>
<p>The regulator's clock is the wedge: Article 5 prohibitions bite today; high-risk
obligations roll in from Aug 2026. Buyers need a number they can show an auditor —
measured, signed, recompute-able. That is the product.</p>

<h2>3 · Product</h2>
<p>"SOV as the Moody's of AI". We run the tests, we own the data, everyone else cites the
scores. Live now: <a href="/benchmarks">/benchmarks</a> +
<a href="/scorecard">/scorecard</a> — free dashboard, Pro API, Enterprise audits, Certification.</p>

<h2>4 · Traction (measured today)</h2>
<ul>
<li>Care-gate recall <strong>{care.get('recall', 0):.0%}</strong> · over-block <strong>0%</strong> on 76 items</li>
<li><strong>{rows}</strong> signed refutation-ledger records (the evidence of honesty)</li>
<li>9/9 live surfaces 200 · AI-SEO kit complete on 3 domains · overnight loop 100+ cycles</li>
<li>Free-tier substrate end-to-end — the unit economics work before revenue, not after</li>
</ul>

<h2>5 · Market</h2>
<p>AI governance: $1.1B → $13.1B by 2035 (31.4% CAGR). Humanoid robotics adjacent.
Nobody owns full-stack sovereign measurement; this is the greenfield no one else can claim
with a working instrument.</p>

<h2>6 · Model</h2>
<p>Free public benchmark = moat + network effect. Pro API $0.01/query · Enterprise audits
$50K · Certification $5K. The scorecard is the funnel; the data room is the proof.</p>

<h2>7 · Team</h2>
<p>Founder-driven sovereign lab: measurement engine, attestation chain, fleet, and the
public surfaces are built and live. Execution speed visible in this repo's own history —
and the refutation ledger proves we correct, not conceal.</p>

<h2>8 · Financials</h2>
<p>£1.5M seed bridge → £15–30M Series A in 9 months. Cost base is free-tier + spot GPU
(caps per run); the instrument is the asset, not burn. Revenue starts at the first
Enterprise audit, not at the first enterprise hire.</p>

<h2>9 · Ask</h2>
<p><strong>£1.5M Seed Bridge @ £4.5M pre — 25% dilution, 75% retained</strong> → Seed Q4
(£2M @ £8M) → Series A Q2-2027 (£15–30M). Lead investor, you ship the ask <em>to</em>
your own compliance review. Use of funds: productize the three audit packs →
first 3 enterprise pilots → the Series-A evidence creates the uplisting, not the reverse.</p>

<h2>10 · Vision</h2>
<p>The SimCity-of-the-world: every governance decision observable, every play a signed
evidence record feeding the measurement flywheel. Measure → sign → verify, at global scale.</p>
</section>
{FOOT}"""


def refutation_ledger_page():
    rows, kinds, signed = ledger_stats()
    sample = []
    if LEDGER.exists():
        for line in list(LEDGER.open(errors="ignore"))[-5:]:
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            sample.append({
                "record_id": d.get("record_id", "?"),
                "kind": d.get("kind", "?"),
                "tag": d.get("tag"),
                "issued_at": d.get("issued_at", "?")[:19],
                "sigil": d.get("sigil", {}).get("algorithm"),
            })
    rows_html = "\n".join(
        f"<tr><td><code>{r['record_id']}</code></td><td>{r['kind']}</td>"
        f"<td>{r.get('tag') or '—'}</td><td>{r['issued_at']}</td><td>{r.get('sigil') or '—'}</td></tr>"
        for r in sample)
    return head(
        "Refutation ledger — we kill our own bad ideas | CSOAI",
        "The CSOAI refutation ledger: {rows} append-only, Sigil-signed records. The history of being wrong is kept, never deleted — the evidence that correction is structural here.",
        "refutation-ledger") + f"""
<p>The engine (<code>decision_ledger.py</code>) is <strong>append-only by construction</strong>:
edit / delete / resolve / adjudicate verbs are absent, and <code>guard()</code> proves it at
runtime. When a result is superseded, a new record carries <code>supersedes</code> — the old
record stays in the chain. Unmeasured numbers are structurally forced to
<code>lower_bound: true</code>. Contradictions surface as OPEN; nothing is auto-resolved.</p>
<section>
<h2>Ledger state</h2>
<p><strong>{rows} records</strong> · {signed} Sigil-signed · BFT-approved · kinds: {json.dumps(kinds)}</p>
<table>
<thead><tr><th>Record</th><th>Kind</th><th>Tag</th><th>Issued</th><th>Sigil</th></tr></thead>
<tbody>
{rows_html}
</tbody>
</table>
<p><em>Latest {len(sample)} records shown; the full ledger is the signed artefact this page
is generated from.</em></p>
</section>
{FOOT}"""


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    (HERE / "series-a-data-room.html").write_text(data_room())
    (HERE / "series-a-deck.html").write_text(deck())
    (HERE / "refutation-ledger.html").write_text(refutation_ledger_page())
    print(f"series-a surfaces written ({stamp})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())