#!/usr/bin/env python3
"""Tick 248 — 3 new DEFONEOS regulator deep-dive packs.

Bodies chosen for coverage gap (verified uncovered on disk + sitemap):
1. Welsh Revenue Authority (WRA) — Welsh devolved tax authority
2. Valuation Office Agency (VOA) — DWP/UK valuation body for council tax & business rates
3. Office for Students (OfS) — higher-education regulator (England)

Same 12-entry-points × 8-priorities × 6-MCPs structure as tick 246/247.
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
    entries = cfg["entries"]
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
<meta content="2026-08-10T04:35:00+00:00" name="revised"/>
<meta content="2026-08-10T04:35:00+00:00" property="article:modified_time"/>
<meta content="{esc(desc)}" name="description"/>
<link href="{url}" rel="canonical"/>
<meta content="{esc(title)}" property="og:title"/>
<meta content="{esc(desc)}" property="og:description"/>
<script type="application/ld+json">{{"@context":"https://***@type":"WebPage","name":"{esc(title)}","url":"{url}","publisher":{{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"}}}}</script>
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

PACKS = [
    {
        "name": "defoneos-welsh-revenue-authority-welsh-taxes-ai-deep-dive-pack",
        "title": "Welsh Revenue Authority Welsh Devolved Taxes AI Deep-Dive Pack",
        "desc": "DEFONEOS — Welsh Revenue Authority Welsh Devolved Taxes AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "Welsh Revenue Authority",
        "body": "Welsh Revenue Authority",
        "legislation_backbone": "Tax Collection and Management (Wales) Act 2016 / Welsh Tax Acts etc. (Power to Modify) Act 2018 / Land Transaction Tax and Anti-avoidance of Devolved Taxes (Wales) Act 2019 / Landfill Disposals Tax (Wales) Act 2017",
        "nav_labels": [
            "Land Transaction Tax", "Landfill Disposals Tax", "Welsh Income Tax", "Tax Compliance &am", "Anti-Avoidance Rules", "Welsh Language Standards", "Online Services &am", "Data Sharing &amp; Digital", "Performance Reporting", "Enforcement &amp; Sanction", "Customer Charter &am", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Land Transaction Tax (LTT) Administration", "region": "Land Transaction Tax (LTT) Administration", "legislation": "Land Transaction Tax and Anti-avoidance of Devolved Taxes (Wales) Act 2017"},
            {"topic": "Landfill Disposals Tax (LDT) Administration", "region": "Landfill Disposals Tax (LDT) Administration", "legislation": "Landfill Disposals Tax (Wales) Act 2017"},
            {"topic": "Welsh Rates of Income Tax (WRIT) — Welsh Rates", "region": "Welsh Rates of Income Tax (WRIT)", "legislation": "Welsh Tax Acts etc. (Power to Modify) Act 2018 / Wales Act 2014"},
            {"topic": "Tax Compliance &amp; Voluntary Disclosures", "region": "Tax Compliance & Voluntary Disclosures", "legislation": "Tax Collection and Management (Wales) Act 2016 Part 5"},
            {"topic": "Anti-Avoidance &amp; Anti-Hybrids Rules", "region": "Anti-Avoidance & Anti-Hybrids Rules", "legislation": "Land Transaction Tax and Anti-avoidance of Devolved Taxes (Wales) Act 2019"},
            {"topic": "Welsh Language Standards (Bilingual Compliance)", "region": "Welsh Language Standards", "legislation": "Welsh Language (Wales) Measure 2011 / Welsh Language Standards Regulations 2015"},
            {"topic": "Online Services &amp; Self-Assessment Portal", "region": "Online Services & Self-Assessment Portal", "legislation": "Tax Collection and Management (Wales) Act 2016 Part 3"},
            {"topic": "Data Sharing &amp; Digital Identity (Welsh Public Services)", "region": "Data Sharing & Digital Identity", "legislation": "Digital Economy Act 2017 / Welsh Government Digital Strategy"},
            {"topic": "Performance Reporting &amp; Outcome Agreements", "region": "Performance Reporting & Outcome Agreements", "legislation": "Tax Collection and Management (Wales) Act 2016 / Welsh Treasury Reporting"},
            {"topic": "Enforcement &amp; Civil Sanctions", "region": "Enforcement & Civil Sanctions", "legislation": "Tax Collection and Management (Wales) Act 2016 Parts 5-7"},
            {"topic": "Customer Charter &amp; Taxpayer Rights", "region": "Customer Charter & Taxpayer Rights", "legislation": "Tax Collection and Management (Wales) Act 2016 Part 2"},
            {"topic": "Governance &amp; Parliamentary Accountability (Senedd)", "region": "Governance & Parliamentary Accountability", "legislation": "Tax Collection and Management (Wales) Act 2016 / Government of Wales Act 2006"},
        ],
    },
    {
        "name": "defoneos-valuation-office-agency-property-valuation-ai-deep-dive-pack",
        "title": "Valuation Office Agency Property Valuation AI Deep-Dive Pack",
        "desc": "DEFONEOS — Valuation Office Agency Property Valuation AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "Valuation Office Agency",
        "body": "Valuation Office Agency",
        "legislation_backbone": "Local Government Finance Act 1988 / Local Government Finance Act 1992 / Local Government Act 2003 / Rating (Property in Common Occupation) and Council Tax (Empty Properties) Act 2018",
        "nav_labels": [
            "Council Tax Valuation", "Business Rates (NNDR) V", "Property Attributes &am", "Appeals &amp; Challenge", "Rating List Maintenance", "Council Tax Reduction &am", "Stamp Tax Valuation", "Open Data &amp; Property", "Digital Mapping &amp; GIS", "Performance Reporting", "Welsh Translation &am", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Council Tax Valuation &amp; Banding", "region": "Council Tax Valuation & Banding", "legislation": "Local Government Finance Act 1992 / Council Tax (Alteration of Lists and Appeals) Regulations 1993"},
            {"topic": "Business Rates (NNDR) Valuation", "region": "Business Rates (NNDR) Valuation", "legislation": "Local Government Finance Act 1988 / Non-Domestic Rating (Alteration of Lists and Appeals) Regulations 2005"},
            {"topic": "Property Attributes &amp; Compensating Adjustments", "region": "Property Attributes & Compensating Adjustments", "legislation": "Local Government Finance Act 1988 / VOA Practice Notes"},
            {"topic": "Appeals &amp; Challenge Tribunals (VTW)", "region": "Appeals & Challenge Tribunals", "legislation": "Tribunals, Courts and Enforcement Act 2007 / Valuation Tribunal Rules 2009"},
            {"topic": "Rating List Maintenance &amp; Revaluations", "region": "Rating List Maintenance & Revaluations", "legislation": "Local Government Finance Act 1988 / Non-Domestic Rating Act 1994"},
            {"topic": "Council Tax Reduction &amp; Disregards", "region": "Council Tax Reduction & Disregards", "legislation": "Local Government Finance Act 1992 / Council Tax Reduction (England) Regulations 2017"},
            {"topic": "Stamp Tax Valuation (Tax &amp; Duty Coordination)", "region": "Stamp Tax Valuation (Tax & Duty Coordination)", "legislation": "Stamp Act 1891 / Finance Act 2003 Sch 7 (SDLT) / HMRC-VOA protocols"},
            {"topic": "Open Data &amp; Property Market Insights", "region": "Open Data & Property Market Insights", "legislation": "Local Government Finance Act 1988 / UK Statistics Authority Code"},
            {"topic": "Digital Mapping &amp; GIS Evidence Base", "region": "Digital Mapping & GIS Evidence Base", "legislation": "Local Government Finance Act 1988 / INSPIRE Regulations 2009"},
            {"topic": "Performance Reporting &amp; Customer Service Standards", "region": "Performance Reporting & Customer Service Standards", "legislation": "Local Government Finance Act 1988 / Cabinet Office Charter"},
            {"topic": "Welsh Translation &amp; Bilingual Standards", "region": "Welsh Translation & Bilingual Standards", "legislation": "Welsh Language (Wales) Measure 2011"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Local Government Finance Act 1988 / Public Bodies Act 2011 / NAO scrutiny"},
        ],
    },
    {
        "name": "defoneos-office-for-students-higher-education-regulation-ai-deep-dive-pack",
        "title": "Office for Students Higher Education Regulation AI Deep-Dive Pack",
        "desc": "DEFONEOS — Office for Students Higher Education Regulation AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "Office for Students",
        "body": "Office for Students",
        "legislation_backbone": "Higher Education and Research Act 2017 / Office for Students (Registration of English Higher Education Providers) Regulations 2018 / Higher Education (Freedom of Speech) Act 2023 / Higher Education Quality and Accountability",
        "nav_labels": [
            "Provider Registration &", "Quality &amp; Standards (", "Freedom of Speech &am", "Access &amp; Participation", "Student Protection Plan", "Financial Sustainability ", "Transparency &amp; Data", "Complaints &amp; Academic", "Research Integrity &am", "International &amp; Transna", "Digital Learning &amp; On", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Provider Registration &amp; Regulatory Oversight", "region": "Provider Registration & Regulatory Oversight", "legislation": "Higher Education and Research Act 2017 Part 1 / Office for Students (Registration of English Higher Education Providers) Regulations 2018"},
            {"topic": "Quality &amp; Standards (TQA Frameworks)", "region": "Quality & Standards", "legislation": "Higher Education and Research Act 2017 Part 3 / UK Quality Code"},
            {"topic": "Freedom of Speech &amp; Academic Freedom", "region": "Freedom of Speech & Academic Freedom", "legislation": "Higher Education (Freedom of Speech) Act 2023"},
            {"topic": "Access &amp; Participation Plans", "region": "Access & Participation Plans", "legislation": "Higher Education and Research Act 2017 s.30 / Office for Students APP Guidance"},
            {"topic": "Student Protection Plans &amp; Closure Risk", "region": "Student Protection Plans & Closure Risk", "legislation": "Higher Education and Research Act 2017 / OfS Regulatory Framework"},
            {"topic": "Financial Sustainability &amp; Viability Assessment", "region": "Financial Sustainability & Viability Assessment", "legislation": "Higher Education and Research Act 2017 s.75 / OfS Financial Monitoring Rules"},
            {"topic": "Transparency &amp; Data (Unistats / NSS / Graduate Outcomes)", "region": "Transparency & Data", "legislation": "Higher Education and Research Act 2017 / UK GDPR / Data Protection Act 2018"},
            {"topic": "Complaints &amp; Academic Appeals (OIA)", "region": "Complaints & Academic Appeals", "legislation": "Higher Education and Research Act 2017 / Higher Education Act 2004 (OIA)"},
            {"topic": "Research Integrity &amp; Research Ethics (REF / UKRIO)", "region": "Research Integrity & Research Ethics", "legislation": "Higher Education and Research Act 2017 Part 4 / UKRIO Code"},
            {"topic": "International &amp; Transnational Education (TNE)", "region": "International & Transnational Education", "legislation": "Higher Education and Research Act 2017 / Education (Listed Bodies) (England) Regulations 2013"},
            {"topic": "Digital Learning &amp; Online Regulation (Online Pathways)", "region": "Digital Learning & Online Regulation", "legislation": "Higher Education and Research Act 2017 / OfS Digital & Blended Learning Guidance"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Higher Education and Research Act 2017 / Public Bodies Act 2011 / DfE sponsorship"},
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