#!/usr/bin/env python3
"""Tick 291 deep-dive pack generator: Scottish Commission on Social Security,
sportscotland, Scottish Legal Complaints Commission.
Reuses tick-290 template (CSS/NAV/FOOTER/engagement identical — only PACKS change).
Writes sources to REPO ROOT (tick-290 fix): build_site.py wipes _site on each run,
so root sources get picked up by the allowlist and assembled into _site by the build.
Emits tick-291-sigil.json at root."""
import os, sys, json, hashlib, datetime

try:
    from _gen_tick291_packs import PACKS
except ImportError:
    print("ERROR: _gen_tick291_packs.py not found in same directory.", file=sys.stderr)
    sys.exit(1)

CSS = """<style>
:root{--bg:#050816;--panel:#0d1330;--gold:#d4af37;--sov:#6dd5ff;--accent:#f97316;--text:#e2e8f0;--muted:#94a3b8;--border:#1e2954;--danger:#ef4444;--green:#4ade80}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;line-height:1.6;min-height:100vh}
.eu-banner{background:linear-gradient(135deg,#991b1b,#7f1d1d);padding:12px 24px;text-align:center;font-size:13px;border-bottom:2px solid #dc2626}
.eu-banner a{color:#fca5a5}
nav{display:flex;gap:24px;padding:16px 24px;background:var(--panel);border-bottom:1px solid var(--border);flex-wrap:wrap}
nav a{color:var(--muted);text-decoration:none;font-size:14px}
nav a:hover{color:var(--sov)}
.container{max-width:1200px;margin:0 auto;padding:40px 24px}
h1{font-family:'Space Grotesk',monospace;font-size:2.2rem;background:linear-gradient(135deg,var(--gold),var(--sov));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
.subtitle{color:var(--muted);font-size:1rem;margin-bottom:32px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:40px}
.stat-card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:20px;text-align:center}
.stat-num{font-family:'Space Grotesk',monospace;font-size:2rem;color:var(--sov)}
.stat-label{color:var(--muted);font-size:13px;margin-top:4px}
h2{font-family:'Space Grotesk',monospace;font-size:1.5rem;color:var(--sov);margin:40px 0 20px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:20px}
.card .tag{display:inline-block;background:var(--accent);color:#000;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;margin-bottom:10px}
.card h3{font-size:1rem;margin-bottom:8px;color:#fff}
.card p{font-size:13px;color:var(--muted);line-height:1.5}
.priority .tag{background:var(--green)}
.mcp .tag{background:#fbbf24;color:#000}
.red-lines{border:1px solid var(--danger);border-radius:12px;padding:24px;margin-bottom:40px}
.red-lines h3{color:var(--danger);margin-bottom:16px;font-size:1.1rem}
.red-lines ul{list-style:none}
.red-lines li{padding:10px 0;border-bottom:1px solid var(--border);font-size:13px}
.red-lines li:last-child{border-bottom:none}
.red-lines li::before{content:'🚫 '}
.engagement{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:40px}
.engagement .step{flex:1;min-width:180px;background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:20px;text-align:center}
.engagement .step .num{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:var(--green);color:#000;font-weight:700;font-size:16px;margin-bottom:10px}
.engagement .step h4{font-size:14px;color:#fff;margin-bottom:6px}
.engagement .step p{font-size:12px;color:var(--muted)}
.cta{display:flex;gap:16px;flex-wrap:wrap;margin:40px 0}
.cta a{display:inline-block;padding:14px 28px;background:var(--gold);color:#000;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px}
.cta a.secondary{border:1px solid var(--gold);background:transparent;color:var(--gold)}
footer{background:var(--panel);border-top:1px solid var(--border);padding:24px;text-align:center;font-size:12px;color:var(--muted);margin-top:40px}
</style>"""

NAV = """<nav>
<a href="/">🜏 Home</a>
<a href="/governance-master.html">Master</a>
<a href="/govbench.html">GovBench</a>
<a href="/sitemap.html">Index</a>
<a href="/sitemap.xml">Sitemap</a>
</nav>"""

EU_BANNER = """<div class="eu-banner">
⚖️ EU AI Act — Article 50 Transparency + Annex III High-Risk classification applies to public-sector AI deployment. This pack is a governance-design document — not a compliance certification. <a href="/governance-master.html">Read the governance framework →</a>
</div>"""

FOOTER = """<footer>
<p>CSOAI Ltd (UK 16939677) · csoai.org · compliance@csoai.org</p>
<p>DEFONEOS is a UK-sovereign open-source AI governance framework built on the meok substrate. UK-sovereign. AUKUS-compatible. Audit-grade.</p>
<p style="margin-top:8px;font-size:11px">© 2026 CSOAI Ltd. All trademarks acknowledged. This document is a governance-design artefact — not a compliance certification.</p>
</footer>"""

TODAY = datetime.date.today().isoformat()
TICK = 291
SIGIL = hashlib.sha256(f"DEFONEOS|tick-{TICK}|3-packs|{TODAY}".encode()).hexdigest()[:16]

def build_entry_point(ep):
    name, desc, tag = ep
    return f"""<div class="card">
<span class="tag">{tag.upper()}</span>
<h3>{name}</h3>
<p>{desc}</p>
</div>"""

def build_priority(p, i):
    return f"""<div class="card priority">
<span class="tag">Priority {i+1}</span>
<p style="font-size:13px;color:var(--muted)">{p}</p>
</div>"""

def build_mcp(mcp, i):
    name, cat, desc = mcp
    return f"""<div class="card mcp">
<span class="tag">MCP {i+1} · {cat}</span>
<h3>{name}</h3>
<p>{desc}</p>
</div>"""

def build_red_line(rl):
    return f"<li>{rl}</li>"

def build_engagement():
    steps = [
        ("Discovery", "Map the body's statutory duties, data flows, and governance gaps against the 12-entry-point framework."),
        ("Governance Design", "Design AI governance architecture, risk appetite, and red-line enforcement aligned to devolved legislation."),
        ("Pilot", "Deploy 2-3 MCP servers in a sandboxed environment with body data; measure governance outcomes against baseline."),
        ("Scale", "Expand to the full 6-MCP stack with body-wide deployment, training, and change management."),
        ("Assure", "Continuous monitoring, 33-agent BFT council verification, and DEFONEOS-SEAL credential issuance.")
    ]
    out = []
    for i, (title, desc) in enumerate(steps):
        out.append(f"""<div class="step">
<div class="num">{i+1}</div>
<h4>{title}</h4>
<p>{desc}</p>
</div>""")
    return "".join(out)

def build_pack(p):
    slug = p["slug"]
    entry_html = "".join(build_entry_point(ep) for ep in p["entry_points"])
    priority_html = "".join(build_priority(pr, i) for i, pr in enumerate(p["priorities"]))
    mcp_html = "".join(build_mcp(m, i) for i, m in enumerate(p["mcps"]))
    red_html = "".join(build_red_line(rl) for rl in p["red_lines"])
    engage_html = build_engagement()

    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": p["title"],
        "description": p["desc"],
        "url": f"https://csoai.org/{slug}.html",
        "about": {"@type": "GovernmentService", "name": p["agency"], "url": p["agency_url"]},
        "provider": {"@type": "Organization", "name": "CSOAI Ltd", "legalName": "CSOAI Ltd"},
        "datePublished": TODAY
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{p['title']}</title>
<meta name="description" content="{p['desc'][:160]}">
<link rel="canonical" href="https://csoai.org/{slug}.html">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
{CSS}
</head>
<body>
{EU_BANNER}
{NAV}
<div class="container">
<h1>{p['title']}</h1>
<p class="subtitle">{p['domain']} · {p['agency']} · {TODAY}</p>

<div class="stats">
<div class="stat-card"><div class="stat-num">12</div><div class="stat-label">Entry Points</div></div>
<div class="stat-card"><div class="stat-num">8</div><div class="stat-label">Transformation Priorities</div></div>
<div class="stat-card"><div class="stat-num">6</div><div class="stat-label">MCP Servers</div></div>
<div class="stat-card"><div class="stat-num">6</div><div class="stat-label">Red Lines</div></div>
</div>

<h2>📋 12 Entry Points</h2>
<div class="grid">{entry_html}</div>

<h2>🎯 8 Transformation Priorities</h2>
<div class="grid">{priority_html}</div>

<h2>🔧 6 MCP Servers</h2>
<div class="grid">{mcp_html}</div>

<h2>🚫 6 Non-Negotiable Red Lines</h2>
<div class="red-lines">
<h3>Governance Red Lines — Anchored in Statute</h3>
<ul>{red_html}</ul>
</div>

<h2>⚡ 5-Step Engagement Model</h2>
<div class="engagement">{engage_html}</div>

<div class="cta">
<a href="/governance-master.html">📋 Request OWEM RFQ →</a>
<a href="/article-50.html" class="secondary">⚖️ Article 50 Passport →</a>
</div>

<p style="font-size:12px;color:var(--muted);margin-top:24px">Legislation backbone: {p['legislation']}</p>
<p style="font-size:12px;color:var(--muted);margin-top:8px">SIGIL: defoneos-tick{TICK}-{slug[:30]}-{SIGIL}</p>
</div>
{FOOTER}
<script type="application/ld+json">
{json.dumps(ld, indent=2)}
</script>
</body>
</html>"""

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    written = []

    for p in PACKS:
        html = build_pack(p)
        fname = f"{p['slug']}.html"
        with open(fname, "w") as f:
            f.write(html)
        sz = os.path.getsize(fname)
        written.append((fname, sz))

        # .llm.json companion
        llm = {
            "type": "LLMPageSummary",
            "url": f"https://csoai.org/{p['slug']}.html",
            "title": p["title"],
            "description": p["desc"],
            "agency": p["agency"],
            "domain": p["domain"],
            "entry_points": [ep[0] for ep in p["entry_points"]],
            "mcps": [m[0] for m in p["mcps"]],
            "legislation": p["legislation"],
            "generated": TODAY,
            "tick": TICK,
            "sigil": hashlib.sha256(html.encode()).hexdigest()[:16]
        }
        llm_name = f"{fname}.llm.json"
        with open(llm_name, "w") as f:
            json.dump(llm, f, indent=2)
        llm_sz = os.path.getsize(llm_name)
        written.append((llm_name, llm_sz))
        print(f"✓ {fname} ({sz:,}b) + .llm.json ({llm_sz}b)")

    print(f"\nTotal: {len(written)} files, {sum(sz for _, sz in written):,} bytes")

    sigil_data = {
        "tick": TICK, "date": TODAY, "packs_built": 3,
        "packs": [p["slug"] for p in PACKS],
        "sigil": SIGIL, "verify": sum(sz for _, sz in written)
    }
    sp = f"tick-{TICK}-sigil.json"
    with open(sp, "w") as f:
        json.dump(sigil_data, f, indent=2)
    print(f"✓ {sp} ({os.path.getsize(sp):,}b)")

if __name__ == "__main__":
    main()
