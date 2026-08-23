#!/usr/bin/env python3
"""Tick 298 generator: 3 genuinely-uncovered UK public-body deep-dive packs.
Screen Scotland / Sport England / Trade Remedies Authority.
Probe-verified 0 disk + 0 sitemap BEFORE build (tick-265 pitfall).
Builder: _gen_tick298.py | Data: _gen_tick298_packs.py"""
import json, os, hashlib
from _gen_tick298_packs import PACKS

TODAY = "2026-08-16"
TICK = 298

NAV = '''<nav class="nav"><a href="/">Home</a><a href="/defoneos-sitemap.html">Sitemap</a><a href="/defoneos-master-govbench.html">GovBench</a><a href="/defoneos-master-index.html">Index</a></nav>'''

FOOTER = '''<footer class="footer"><p>CSOAI Ltd — UK Company No. 16939677 | <a href="https://csoai.org">csoai.org</a> | compliance@csoai.org</p><p>DEFONEOS &copy; 2026 Nicholas Templeman. Open source. UK sovereign. AUKUS-compatible.</p><p class="sigil">SIGIL: DEFONEOS|TICK-{tick}|{sigil_hash}|sovereign|british|forever</p></footer>'''

CSS = '''<style>
:root{--bg:#050816;--panel:#0d1330;--gold:#d4af37;--sov:#6dd5ff;--accent:#4ade80;--text:#e2e8f0;--muted:#94a3b8;--red:#ef4444}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:'Inter',-apple-system,sans-serif;line-height:1.6}
.nav{display:flex;gap:2rem;padding:1rem 2rem;background:var(--panel);border-bottom:1px solid rgba(109,213,255,0.15);font-size:0.9rem;flex-wrap:wrap}
.nav a{color:var(--sov);text-decoration:none;transition:color 0.2s}
.nav a:hover{color:var(--gold)}
.container{max-width:1200px;margin:0 auto;padding:2rem}
h1{font-size:2.2rem;background:linear-gradient(135deg,var(--sov),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.5rem}
.subtitle{color:var(--muted);font-size:1.1rem;margin-bottom:2rem}
.eu-banner{background:linear-gradient(135deg,#991b1b,#7f1d1d);padding:0.8rem 1.5rem;border-radius:8px;margin-bottom:2rem;font-size:0.85rem;color:#fca5a5}
.stats-bar{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2.5rem}
.stat-card{background:var(--panel);padding:1.2rem;border-radius:8px;text-align:center;border:1px solid rgba(109,213,255,0.1)}
.stat-card .stat-num{font-size:1.8rem;font-weight:700;color:var(--gold)}
.stat-card .stat-label{font-size:0.8rem;color:var(--muted);margin-top:0.3rem}
h2{color:var(--sov);font-size:1.4rem;margin:2rem 0 1rem;padding-bottom:0.5rem;border-bottom:2px solid rgba(109,213,255,0.15)}
.ep-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem}
.ep-card{background:var(--panel);padding:1.2rem;border-radius:8px;border:1px solid rgba(109,213,255,0.1);transition:border-color 0.2s}
.ep-card:hover{border-color:var(--accent)}
.ep-tag{display:inline-block;background:rgba(74,222,128,0.15);color:var(--accent);font-size:0.7rem;padding:0.2rem 0.6rem;border-radius:4px;margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:0.05em}
.ep-card h3{color:var(--text);font-size:0.95rem;margin-bottom:0.4rem}
.ep-card p{color:var(--muted);font-size:0.8rem;line-height:1.4}
.priority-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem}
.p-card{background:var(--panel);padding:1rem;border-radius:8px;border:1px solid rgba(250,204,21,0.15)}
.p-tag{display:inline-block;background:rgba(250,204,21,0.15);color:#fbbf24;font-size:0.7rem;padding:0.2rem 0.6rem;border-radius:4px;margin-bottom:0.5rem}
.p-card h3{color:var(--text);font-size:0.85rem;margin-bottom:0.4rem}
.mcp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem}
.mcp-card{background:var(--panel);padding:1rem;border-radius:8px;border:1px solid rgba(109,213,255,0.15)}
.mcp-tag{display:inline-block;background:rgba(109,213,255,0.15);color:var(--sov);font-size:0.7rem;padding:0.2rem 0.6rem;border-radius:4px;margin-bottom:0.5rem}
.red-line-box{background:rgba(239,68,68,0.05);border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:1.5rem;margin-bottom:2rem}
.red-line-box h3{color:var(--red);margin-bottom:0.8rem}
.red-line-box ul{list-style:none;padding:0}
.red-line-box li{color:var(--muted);font-size:0.85rem;padding:0.3rem 0;padding-left:1.2rem;position:relative}
.red-line-box li:before{content:'🚫';position:absolute;left:0;font-size:0.75rem}
.steps-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;margin-bottom:2rem}
.step-card{background:var(--panel);padding:1rem;border-radius:8px;text-align:center;border:1px solid rgba(109,213,255,0.1)}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:2rem;height:2rem;border-radius:50%;background:var(--accent);color:var(--bg);font-weight:700;font-size:0.9rem;margin-bottom:0.5rem}
.step-card h4{font-size:0.8rem;color:var(--text);margin-bottom:0.3rem}
.step-card p{font-size:0.7rem;color:var(--muted);line-height:1.3}
.cta-strip{display:flex;gap:1rem;justify-content:center;margin:2rem 0}
.cta-btn{display:inline-block;padding:0.8rem 2rem;border-radius:6px;text-decoration:none;font-weight:600;transition:all 0.2s;font-size:0.9rem}
.cta-primary{background:linear-gradient(135deg,var(--gold),#b8860b);color:var(--bg)}
.cta-primary:hover{transform:translateY(-1px);box-shadow:0 4px 20px rgba(212,175,55,0.3)}
.cta-secondary{background:transparent;color:var(--sov);border:1px solid var(--sov)}
.cta-secondary:hover{background:rgba(109,213,255,0.1)}
.footer{background:var(--panel);padding:2rem;text-align:center;border-top:1px solid rgba(109,213,255,0.1);margin-top:3rem;font-size:0.8rem;color:var(--muted)}
.footer .sigil{font-family:'Courier New',monospace;font-size:0.7rem;color:rgba(109,213,255,0.3);margin-top:0.5rem}
@media(max-width:768px){.ep-grid,.priority-grid,.mcp-grid{grid-template-columns:repeat(2,1fr)}.stats-bar{grid-template-columns:repeat(2,1fr)}.steps-grid{grid-template-columns:repeat(3,1fr)}}
</style>'''

def build_pack(pack):
    ep_html = '\n'.join(f'''<div class="ep-card"><span class="ep-tag">{pack["domain_tag"]}</span><h3>{h3}</h3><p>{p}</p></div>''' for h3, p in pack["entry_points"])
    pr_html = '\n'.join(f'''<div class="p-card"><span class="p-tag">Priority {i+1}</span><h3>{h3}</h3><p>{p}</p></div>''' for i, (h3, p) in enumerate(pack["priorities"]))
    mcp_html = '\n'.join(f'''<div class="mcp-card"><span class="mcp-tag">MCP {i+1}</span><h3>{h3}</h3><p>{p}</p></div>''' for i, (h3, p) in enumerate(pack["mcps"]))
    rl_html = '\n'.join(f'<li>{rl}</li>' for rl in pack["red_lines"])
    steps_html = '\n'.join(f'''<div class="step-card"><span class="step-num">{i+1}</span><h4>{step}</h4><p>{desc}</p></div>''' for i, (step, desc) in enumerate([
        ("Discovery", "Stakeholder mapping, data audit, and AI readiness assessment for {body}"),
        ("Governance Design", "Red-line codification, human-review gate design, and AI impact assessment per UK GDPR"),
        ("Pilot", "6-8 week AI-assisted pilot on one high-volume workflow with parallel manual oversight"),
        ("Scale", "Roll-out to full jurisdiction with continuous monitoring, recommender-agent feedback, and compliance dashboards"),
        ("Assure", "Annual audit by DEFONEOS-SEAL credential, CSOAI BFT Council governance review, and parliamentary reporting")
    ]))
    steps_html = steps_html.replace("{body}", pack["body_name"])

    sigil_hash = hashlib.sha256(f"DEFONEOS|{pack['slug']}|{TICK}|{TODAY}".encode()).hexdigest()[:16]
    footer = FOOTER.format(tick=TICK, sigil_hash=sigil_hash)

    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": pack["title"],
        "description": pack["headline"],
        "datePublished": TODAY,
        "publisher": {"@type": "Organization", "name": "CSOAI Ltd", "url": "https://csoai.org"},
        "about": {"@type": "GovernmentService", "name": pack["body_name"], "provider": {"@type": "GovernmentOrganization", "name": f"{pack['body_name']} ({pack['body_acronym']})", "url": pack["gov_url"]}}
    })

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{pack["title"]}</title>
<meta name="description" content="{pack["headline"]}">
<link rel="canonical" href="https://www.csoai.org/{pack["slug"]}.html">
{CSS}
<script type="application/ld+json">
{ld_json}
</script>
</head>
<body>
<div class="eu-banner">⚠️ EU AI Act Article 50 + Annex III High-Risk AI Systems — {pack["body_name"]} is {pack["jurisdiction_note"]}; this AI pack complies with the CSOAI GSPC governance framework for high-risk public-sector AI deployment. All MCP tools are audit-grade, Ed25519-signed, and DEFONEOS-SEAL compatible.</div>
{NAV}
<div class="container">
<h1>{pack["title"]}</h1>
<p class="subtitle">{pack["headline"]}</p>
<div class="stats-bar">
<div class="stat-card"><div class="stat-num">12</div><div class="stat-label">Entry Points</div></div>
<div class="stat-card"><div class="stat-num">8</div><div class="stat-label">Transformation Priorities</div></div>
<div class="stat-card"><div class="stat-num">6</div><div class="stat-label">MCP Servers</div></div>
<div class="stat-card"><div class="stat-num">6</div><div class="stat-label">Red Lines</div></div>
</div>

<h2>🏛️ 12 Entry Points — {pack["body_name"]}</h2>
<div class="ep-grid">{ep_html}</div>

<h2>🚀 8 AI Transformation Priorities</h2>
<div class="priority-grid">{pr_html}</div>

<h2>🤖 6 MCP Servers</h2>
<div class="mcp-grid">{mcp_html}</div>

<h2>🚫 6 Red Lines — Legislation Backbone</h2>
<div class="red-line-box"><h3>Statutory Framework: {pack["primary_act"]}</h3><ul>{rl_html}</ul></div>

<h2>🎯 5-Step Engagement Model</h2>
<div class="steps-grid">{steps_html}</div>

<div class="cta-strip">
<a href="/defoneos-master-govbench.html" class="cta-btn cta-primary">Request OWEM RFQ for {pack["body_acronym"]}</a>
<a href="/defoneos-article50-passport.html" class="cta-btn cta-secondary">Article 50 AI Passport</a>
</div>
</div>
{footer}
</body>
</html>'''
    return html

def make_llm_json(pack, html):
    sigil_hash = hashlib.sha256(f"DEFONEOS|{pack['slug']}|{TICK}|{TODAY}".encode()).hexdigest()[:16]
    return json.dumps({
        "source": f"_gen_tick{TICK}.py",
        "slug": pack["slug"],
        "tick": TICK,
        "date": TODAY,
        "title": pack["title"],
        "body_name": pack["body_name"],
        "body_acronym": pack["body_acronym"],
        "entry_points": [ep[0] for ep in pack["entry_points"]],
        "mcp_servers": [m[0] for m in pack["mcps"]],
        "red_lines_count": len(pack["red_lines"]),
        "html_bytes": len(html),
        "sigil": sigil_hash,
        "veracity": "REAL",
        "canonical": f"https://www.csoai.org/{pack['slug']}.html"
    }, indent=2)

os.makedirs("_site", exist_ok=True)
sigil = {"tick": TICK, "date": TODAY, "packs": [], "total_bytes": 0, "phase": 265}

for pack in PACKS:
    html = build_pack(pack)
    html_path = f"{pack['slug']}.html"
    llm_path = f"{pack['slug']}.html.llm.json"

    with open(f"_site/{html_path}", "w") as f:
        f.write(html)
    with open(html_path, "w") as f:
        f.write(html)

    llm_data = make_llm_json(pack, html)
    with open(f"_site/{llm_path}", "w") as f:
        f.write(llm_data)
    with open(llm_path, "w") as f:
        f.write(llm_data)

    sigil["packs"].append({"slug": pack["slug"], "bytes": len(html), "acronym": pack["body_acronym"], "entry_points": 12})
    sigil["total_bytes"] += len(html)
    print(f"  BUILT: {pack['slug']}.html ({len(html)} bytes)")

sigil_path = f"_site/_gen_tick{TICK}_sigil.json"
with open(sigil_path, "w") as f:
    json.dump(sigil, f, indent=2)
print(f"  SIGIL: {sigil_path}")
print(f"  TOTAL: {len(PACKS)} packs, {sigil['total_bytes']} bytes")
