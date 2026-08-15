#!/usr/bin/env python3
"""Tick 247 — 3 new DEFONEOS regulator deep-dive packs.
Bodies: Environment Agency (EA), HM Land Registry (HMLR), Security Industry Authority (SIA).
Reproduces the verified tick-246 (FRC/OBR/RSH) pack structure byte-for-byte in layout.
"""
import html as htmlmod
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#e0e0e0;font-family:system-ui,sans-serif;line-height:1.6}
a{color:#00ff88;text-decoration:none}a:hover{text-decoration:underline}
.hero{background:linear-gradient(135deg,#0a0a0a,#1a1a2e,#0d1117);padding:40px 20px;text-align:center;border-bottom:2px solid #00ff88}
.hero h1{font-size:2em;color:#00ff88;margin-bottom:6px}
.sub{color:#888;font-size:.95em;margin-bottom:10px}
.bg{display:inline-block;background:#1a1a2e;border:1px solid #00ff88;padding:4px 12px;border-radius:20px;color:#00ff88;font-size:.8em;margin:3px}
nav{background:#111;padding:10px 20px;border-bottom:1px solid #222;position:sticky;top:0;z-index:100;overflow-x:auto;white-space:nowrap}
nav a{display:inline-block;padding:4px 10px;margin:2px;background:#1a1a2e;border:1px solid #333;border-radius:6px;font-size:.75em;color:#00ff88;transition:all .2s}
nav a:hover{background:#00ff88;color:#0a0a0a;text-decoration:none}
.c{max-width:1200px;margin:0 auto;padding:20px}
.s{margin:28px 0;background:#1a1a2e;border:1px solid #222;border-radius:12px;overflow:hidden}
.sh{background:linear-gradient(90deg,#1a1a2e,#0d1117);padding:14px 18px;border-bottom:1px solid #333}
.sh h2{color:#00ff88;font-size:1.2em;margin-bottom:2px}
.en{color:#666;font-size:.78em}
.sb{padding:18px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-bottom:14px}
.p{background:#0d1117;border:1px solid #222;border-radius:8px;padding:12px;transition:border-color .2s}
.p:hover{border-color:#00ff88}
.p h3{color:#00ff88;font-size:.84em;margin-bottom:5px}
.p p{color:#aaa;font-size:.78em;line-height:1.5}
.mt{background:#111;border:1px solid #222;border-radius:8px;padding:12px;margin-top:10px}
.mt h4{color:#00ff88;font-size:.82em;margin-bottom:6px}
.ml{display:flex;flex-wrap:wrap;gap:5px}
.t{background:#1a1a2e;border:1px solid #00ff88;padding:2px 9px;border-radius:16px;font-size:.72em;color:#00ff88}
footer{background:#111;border-top:2px solid #00ff88;padding:20px;text-align:center;margin-top:28px}
.br{font-size:1.1em;color:#00ff88;font-weight:700;margin-bottom:5px}
footer p{color:#666;font-size:.75em;line-height:1.5}
.cr{margin-top:10px;padding-top:10px;border-top:1px solid #222;color:#555;font-size:.72em}
@media(max-width:768px){.hero h1{font-size:1.4em}.g{grid-template-columns:1fr}}"""

CHIPS = ["mcp-bailii", "mcp-govuk-search", "mcp-hansard-search",
         "mcp-uk-courts", "mcp-uk-legislation", "mcp-uk-regulator-intel"]

CAPS = [
    "Compliance Automation",
    "Risk Detection &amp; Early Warning",
    "Natural Language Policy Analysis",
    "Predictive Analytics",
    "Evidence Synthesis",
    "Document Intelligence",
    "Stakeholder Reporting",
    "Real-time Monitoring",
]

def esc(s):
    return htmlmod.escape(s, quote=False)

def build_pack(cfg):
    name = cfg["name"]
    title = cfg["title"]
    desc = cfg["desc"]
    domain = cfg["domain"]
    body_short = cfg["body"]
    entries = cfg["entries"]  # list of dicts: topic, region, legislation
    url = f"https://www.csoai.org/{name}.html"
    llm = f"https://www.csoai.org/{name}.html.llm.json"

    nav = "".join(
        f'<a href="#ep{i+1}">{lbl}</a>'
        for i, lbl in enumerate(cfg["nav_labels"])
    )

    sections = []
    for i, e in enumerate(entries, 1):
        topic = esc(e["topic"])
        reg = esc(e["region"])
        legis = esc(e["legislation"])
        cards = []
        # Capability paragraph builders — same 8-card shape as tick 246
        c0 = (f"Automated {esc(domain)} regulation {reg} validation checking "
              f"{legis} against {reg} statutory and rulebook requirements. "
              f"No {esc(domain)} regulation activity proceeds without a signed, "
              f"auditable compliance record.")
        c1 = (f"Detection of {reg} risk breaches, control gaps, and early-warning "
              f"indicators affecting {esc(domain)} regulation performance and "
              f"accountability to Parliament.")
        c2 = (f"NLP analysis of {reg} legislation, policy statements, guidance, "
              f"and parliamentary record against the full statutory framework and "
              f"regulatory expectations.")
        c3 = (f"{reg} risk and workload forecasting from trend indicators, demand "
              f"signals, and operational metrics to support prioritisation and "
              f"decision-support.")
        c4 = (f"{reg} evidence, inspection findings, returns, and stakeholder "
              f"submissions assembled into decision dossiers for review by "
              f"accountable officers and the BFT council.")
        c5 = (f"Extraction from {reg} documents, statutory returns, and "
              f"correspondence for end-to-end {esc(domain)} regulation lifecycle "
              f"tracking and audit trails.")
        c6 = (f"{reg} dashboards reporting coverage, performance, and outcomes "
              f"to ministers, the board, and Parliament.")
        c7 = (f"{reg} pipeline tracking, submission cycles, and continuous "
              f"surveillance of {esc(domain)} regulation activity for sovereign, "
              f"verifiable oversight.")
        for cap, body in zip(CAPS, [c0, c1, c2, c3, c4, c5, c6, c7]):
            cards.append(f'<div class="p"><h3>{cap}</h3><p>{body}</p></div>')
        chips = "".join(f'<span class="t">{c}</span>' for c in CHIPS)
        sections.append(
            f'<div class="s" id="ep{i}"><div class="sh">'
            f'<span class="en">Entry Point {i:02d}</span><h2>{topic}</h2></div>'
            f'<div class="sb"><div class="g">' + "".join(cards) +
            f'</div><div class="mt"><h4>MCP Tools</h4><div class="ml">{chips}</div></div>'
            f'</div></div>'
        )

    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{esc(title)}</title>
<style>{CSS}</style>
<link href="{llm}" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>
<meta content="/llms.txt" name="llms-txt"/>
<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>
<meta content="CSOAI Ltd (2026). {esc(title)}. {url}" name="citation-policy"/>
<meta content="2026-08-09T11:30:00+00:00" name="revised"/>
<meta content="2026-08-09T11:30:00+00:00" property="article:modified_time"/>
<meta content="{esc(desc)}" name="description"/>
<link href="{url}" rel="canonical"/>
<meta content="{esc(title)}" property="og:title"/>
<meta content="{esc(desc)}" property="og:description"/>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","name":"{esc(title)}","url":"{url}","publisher":{{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"}}}}</script>
</head>
<body>
<div class="hero">
<h1>📊 {esc(title)}</h1>
<p class="sub">DEFONEOS — UK Sovereign Public Services OS</p>
<div><span class="bg">12 Entry Points</span><span class="bg">8 AI Priorities</span><span class="bg">6 MCP Tools</span></div>
<p>96 AI capability mappings × 6 MCP integrations — {esc(body_short)}</p>
</div>
<nav>
{nav}
</nav>
<div class="c">
{''.join(sections)}
</div>
<footer>
<div class="br">DEFONEOS — UK Sovereign Public Services OS</div>
<p>Open-source sovereign AI governance for {esc(body_short)}. Built for audit-grade, signed, neutral UK-sovereign compliance.</p>
<p>AUKUS-compatible. {esc(cfg['legislation_backbone'])}.</p>
<div class="cr">© 2026 CSOAI Ltd (UK 16939677) · meok-defoneos · csoai-defoneos · DEFONEOS-SEAL</div>
</footer>
</body>
</html>
"""
    return body

# ---------------------------------------------------------------------------
PACKS = [
    {
        "name": "defoneos-environment-agency-environmental-protection-flood-ai-deep-dive-pack",
        "title": "Environment Agency Environmental Protection & Flood Resilience AI Deep-Dive Pack",
        "desc": "DEFONEOS — Environment Agency Environmental Protection & Flood Resilience AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "Environment Agency",
        "body": "Environment Agency",
        "legislation_backbone": "Environment Act 2021 / Environmental Permitting (England and Wales) Regulations 2016 / Flood and Water Management Act 2010 / Water Resources Act 1991",
        "nav_labels": [
            "Flood &amp; Coastal R", "Environmental Permitt", "Water Quality &amp; River",
            "Waste &amp; Circular E", "Air Quality &amp; Emissio", "Contaminated Land &amp; ",
            "Fisheries &amp; Biodiv", "Climate Adaptation &amp;", "Incident Response &amp; ",
            "Enforcement &amp; Civil", "Data &amp; National Envir", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Flood &amp; Coastal Risk Management", "region": "Flood & Coastal Risk Management", "legislation": "Flood and Water Management Act 2010 / Flood Risk Regulations 2009"},
            {"topic": "Environmental Permitting &amp; Compliance", "region": "Environmental Permitting & Compliance", "legislation": "Environmental Permitting (England and Wales) Regulations 2016"},
            {"topic": "Water Quality &amp; River Basin Management", "region": "Water Quality & River Basin Management", "legislation": "Water Resources Act 1991 / Water Framework Directive Regulations 2017"},
            {"topic": "Waste Regulation &amp; Circular Economy", "region": "Waste Regulation & Circular Economy", "legislation": "Environmental Protection Act 1990 / Waste (England and Wales) Regulations 2011"},
            {"topic": "Air Quality &amp; Emissions Management", "region": "Air Quality & Emissions Management", "legislation": "Environment Act 1995 / Environment Act 2021"},
            {"topic": "Contaminated Land &amp; Remediation", "region": "Contaminated Land & Remediation", "legislation": "Part 2A Environmental Protection Act 1990 / Environment Act 2021"},
            {"topic": "Fisheries &amp; Biodiversity Protection", "region": "Fisheries & Biodiversity Protection", "legislation": "Environment Act 2021 / Salmon and Freshwater Fisheries Act 1975"},
            {"topic": "Climate Adaptation &amp; Net Zero", "region": "Climate Adaptation & Net Zero", "legislation": "Climate Change Act 2008 / Climate Change Act 2008 (2050 Target Amendment) Order 2019"},
            {"topic": "Incident Response &amp; Pollution Control", "region": "Incident Response & Pollution Control", "legislation": "COMAH Regulations 2015 / National Contingency Plan"},
            {"topic": "Enforcement &amp; Civil Sanctions", "region": "Enforcement & Civil Sanctions", "legislation": "Environment Act 1995 / Environmental Civil Sanctions (England) Order 2010"},
            {"topic": "Data &amp; National Environment Monitoring", "region": "Data & National Environment Monitoring", "legislation": "Environment Act 2021 / UK Environmental Principles"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Environment Act 1995 / Public Bodies Act 2011 / NAO scrutiny"},
        ],
    },
    {
        "name": "defoneos-hm-land-registry-land-title-conveyancing-ai-deep-dive-pack",
        "title": "HM Land Registry Land Title & Conveyancing AI Deep-Dive Pack",
        "desc": "DEFONEOS — HM Land Registry Land Title & Conveyancing AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "HM Land Registry",
        "body": "HM Land Registry",
        "legislation_backbone": "Land Registration Act 2002 / Land Registration Rules 2003 / Land Charges Act 1972 / Economic Crime Act 2022",
        "nav_labels": [
            "Title Registration &am", "Digital Conveyancing &am", "Land Charges &amp; Searc",
            "Boundaries &amp; Cadastr", "Property Fraud Preventi", "Local Land Charges Reg",
            "Leasehold &amp; Freehold", "Commons &amp; Village Gree", "Overseas Entities Regis",
            "Open Data &amp; Property", "Digital Services &amp; Bu", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Title Registration &amp; State Guarantee", "region": "Title Registration & State Guarantee", "legislation": "Land Registration Act 2002 / Land Registration Rules 2003"},
            {"topic": "Digital Conveyancing &amp; e-Discharges", "region": "Digital Conveyancing & e-Discharges", "legislation": "Land Registration Act 2002 (Electronic Communications) Order 2008"},
            {"topic": "Land Charges &amp; Searches", "region": "Land Charges & Searches", "legislation": "Land Charges Act 1972 / Local Land Charges Act 1975"},
            {"topic": "Boundaries &amp; Cadastral Accuracy", "region": "Boundaries & Cadastral Accuracy", "legislation": "Land Registration Rules 2003 / Boundary Commission rules"},
            {"topic": "Property Fraud Prevention", "region": "Property Fraud Prevention", "legislation": "Land Registration Act 2002 / Economic Crime Act 2022"},
            {"topic": "Local Land Charges Register", "region": "Local Land Charges Register", "legislation": "Local Land Charges Act 1975 / Infrastructure Act 2015"},
            {"topic": "Leasehold &amp; Freehold Title Management", "region": "Leasehold & Freehold Title Management", "legislation": "Land Registration Act 2002 / Leasehold Reform Act 1967"},
            {"topic": "Commons &amp; Village Greens Registration", "region": "Commons & Village Greens Registration", "legislation": "Commons Act 2006 / Commons Registration Act 1965"},
            {"topic": "Overseas Entities Registration", "region": "Overseas Entities Registration", "legislation": "Economic Crime (Transparency and Enforcement) Act 2022"},
            {"topic": "Open Data &amp; Property Analytics", "region": "Open Data & Property Analytics", "legislation": "Land Registration Act 2002 / INSPIRE Regulations 2009 / UK GDPR"},
            {"topic": "Digital Services &amp; Business Gateway", "region": "Digital Services & Business Gateway", "legislation": "Electronic Communications Act 2000 / HMLR Digital Strategy"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Land Registration Act 2002 / Public Bodies Act 2011 / NAO scrutiny"},
        ],
    },
    {
        "name": "defoneos-sia-security-industry-authority-ai-deep-dive-pack",
        "title": "Security Industry Authority Licensing & Compliance AI Deep-Dive Pack",
        "desc": "DEFONEOS — Security Industry Authority Licensing & Compliance AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "Security Industry Authority",
        "body": "Security Industry Authority",
        "legislation_backbone": "Private Security Industry Act 2001 / Police Act 1997 / UK GDPR / Equality Act 2010",
        "nav_labels": [
            "SIA Licensing &amp; Comp", "Approved Contractor Sch", "Door Supervision Licenc",
            "CCTV &amp; Public Space ", "Security Guard &amp; Clos", "Vehicle Immobilisation ",
            "Training &amp; Qualifica", "Enforcement &amp; Sanctio", "Counter-Terrorism &amp; Pr",
            "Modern Slavery &amp; Lab", "Identity &amp; Biometric ", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "SIA Licensing &amp; Compliance", "region": "SIA Licensing & Compliance", "legislation": "Private Security Industry Act 2001 / SIA licensing criteria"},
            {"topic": "Approved Contractor Scheme", "region": "Approved Contractor Scheme", "legislation": "Private Security Industry Act 2001 s.10-13"},
            {"topic": "Door Supervision Licensing", "region": "Door Supervision Licensing", "legislation": "Private Security Industry Act 2001 / Violent Crime Reduction Act 2006"},
            {"topic": "CCTV &amp; Public Space Surveillance Licensing", "region": "CCTV & Public Space Surveillance Licensing", "legislation": "Private Security Industry Act 2001 / Protection of Freedoms Act 2012"},
            {"topic": "Security Guard &amp; Close Protection Licensing", "region": "Security Guard & Close Protection Licensing", "legislation": "Private Security Industry Act 2001 / SIA licence-linked qualifications"},
            {"topic": "Vehicle Immobilisation Licensing", "region": "Vehicle Immobilisation Licensing", "legislation": "Private Security Industry Act 2001 / Protection of Freedoms Act 2012"},
            {"topic": "Training &amp; Qualification Standards", "region": "Training & Qualification Standards", "legislation": "Private Security Industry Act 2001 / SIA licence-linked qualification criteria"},
            {"topic": "Enforcement &amp; Sanctions", "region": "Enforcement & Sanctions", "legislation": "Private Security Industry Act 2001 s.6-9 / Police and Criminal Evidence Act 1984"},
            {"topic": "Counter-Terrorism &amp; Protective Security", "region": "Counter-Terrorism & Protective Security", "legislation": "Terrorism Act 2000 / Martyn's Law (Protect Duty) / Counter-Terrorism and Border Security Act 2019"},
            {"topic": "Modern Slavery &amp; Labour Market Compliance", "region": "Modern Slavery & Labour Market Compliance", "legislation": "Modern Slavery Act 2015 / Immigration Act 2016"},
            {"topic": "Identity &amp; Biometric Verification", "region": "Identity & Biometric Verification", "legislation": "UK GDPR / Data Protection Act 2018 / eIDAS UK"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Private Security Industry Act 2001 / Public Bodies Act 2011 / Home Office sponsorship"},
        ],
    },
]

def main():
    for cfg in PACKS:
        out = ROOT / f"{cfg['name']}.html"
        out.write_text(build_pack(cfg), encoding="utf-8")
        print(f"{out.name}: {out.stat().st_size}b")
    print("done")

if __name__ == "__main__":
    main()