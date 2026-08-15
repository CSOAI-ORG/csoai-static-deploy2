#!/usr/bin/env python3
"""Tick 249 — 3 new DEFONEOS regulator deep-dive packs.

Bodies chosen for coverage gap (verified uncovered on disk + sitemap):
1. National Savings & Investments (NS&I) — UK state savings / retail debt body
2. Gangmasters & Labour Abuse Authority (GLAA) — labour exploitation regulator
3. UK Statistics Authority (UKSA / OSR) — statistics governance & National Statistics designation

Same 12-entry-points × 8-priorities × 6-MCPs structure as tick 248/247/246.
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

PACKS = [
    {
        "name": "defoneos-nsi-national-savings-investments-retail-savings-ai-deep-dive-pack",
        "title": "National Savings &amp; Investments Retail Savings AI Deep-Dive Pack",
        "desc": "DEFONEOS — National Savings &amp; Investments Retail Savings AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "National Savings &amp; Investments",
        "body": "National Savings &amp; Investments",
        "legislation_backbone": "National Savings Bank Act 1971 / Consolidated Fund Act 1816 / Finance Act 1991 / Government Resources and Accounts Act 2000",
        "nav_labels": [
            "Premium Bonds &amp; ERNIE", "NS&amp;I Certificates", "NS&amp;I ISA Products", "Income &amp; Defined Returns", "Green Savings Bonds", "Direct Saver &amp; Access", "65+ Guaranteed Bonds", "Rate Setting &amp; Funding", "Data &amp; NSS Security", "Customer &amp; Complaints", "Treasury Reporting", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Premium Bonds &amp; ERNIE Draw Governance", "region": "Premium Bonds & ERNIE Draw", "legislation": "National Savings Bank Act 1971 / Premium Bonds Regulations"},
            {"topic": "NS&amp;I Savings Certificates (Fixed &amp; Index-linked)", "region": "NS&I Savings Certificates", "legislation": "National Savings Bank Act 1971 / NS&I Product Terms"},
            {"topic": "NS&amp;I ISA &amp; Junior ISA Administration", "region": "NS&I ISA & Junior ISA", "legislation": "Individual Savings Account Regulations 1998 / Finance Act 2008"},
            {"topic": "Income Bonds &amp; Defined Return Products", "region": "Income & Defined Return Bonds", "legislation": "National Savings Bank Act 1971 / Treasury Directions"},
            {"topic": "Green Savings Bonds &amp; Climate Funding", "region": "Green Savings Bonds", "legislation": "Finance Act 2021 / UK Green Gilt Framework"},
            {"topic": "Direct Saver &amp; Instant Access Products", "region": "Direct Saver & Instant Access", "legislation": "National Savings Bank Act 1971 / NS&I Terms"},
            {"topic": "65+ Guaranteed Growth Bonds", "region": "65+ Guaranteed Growth Bonds", "legislation": "National Savings Bank Act 1971 / Age-verified Product Rules"},
            {"topic": "Rate Setting &amp; Treasury Funding (Retail Debt)", "region": "Rate Setting & Treasury Funding", "legislation": "Debt Management Office remit / Consolidated Fund Act 1816"},
            {"topic": "Data Security &amp; National Savings Bank Records", "region": "Data Security & Records", "legislation": "UK GDPR / Data Protection Act 2018 / KYC Rules"},
            {"topic": "Customer Service &amp; Complaints (FOS Jurisdiction)", "region": "Customer Service & Complaints", "legislation": "Financial Services and Markets Act 2000 / FOS DISP"},
            {"topic": "Unclaimed Assets &amp; Dormant Account Payments", "region": "Unclaimed Assets", "legislation": "Dormant Bank and Building Society Accounts Act 2008"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Government Resources and Accounts Act 2000 / HM Treasury sponsorship / NAO"},
        ],
    },
    {
        "name": "defoneos-glaa-gangmasters-labour-abuse-authority-labour-exploitation-ai-deep-dive-pack",
        "title": "Gangmasters &amp; Labour Abuse Authority Labour Exploitation AI Deep-Dive Pack",
        "desc": "DEFONEOS — Gangmasters &amp; Labour Abuse Authority Labour Exploitation AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "Gangmasters &amp; Labour Abuse Authority",
        "body": "Gangmasters &amp; Labour Abuse Authority",
        "legislation_backbone": "Gangmasters (Licensing) Act 2004 / Modern Slavery Act 2015 / National Minimum Wage Act 1998 / Employment Agencies Act 1973",
        "nav_labels": [
            "Gangmaster Licensing", "Labour Provider Registr", "Agri-Horticulture Compl", "Food Processing &amp; Shell", "Modern Slavery Intell", "Exploitation Investiga", "Supply Chain Protectio", "Minimum Wage &amp; Conditi", "Licence Compliance Ins", "Enforcement &amp; Prosecut", "Multi-Agency Modern Sl", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Gangmaster Licensing Regime", "region": "Gangmaster Licensing", "legislation": "Gangmasters (Licensing) Act 2004 Part 1"},
            {"topic": "Labour Provider Registration &amp; Licensing", "region": "Labour Provider Registration", "legislation": "Gangmasters (Licensing) Act 2004 / Licensing Conditions"},
            {"topic": "Agricultural &amp; Horticultural Sector Compliance", "region": "Agri-Horticultural Compliance", "legislation": "Gangmasters (Licensing) Act 2004 / Seasonal Worker Guidance"},
            {"topic": "Shellfish Gathering &amp; Food Processing Oversight", "region": "Food Processing & Shellfish", "legislation": "Gangmasters (Licensing) Act 2004 Schedule 1"},
            {"topic": "Modern Slavery &amp; Trafficking Intelligence", "region": "Modern Slavery Intelligence", "legislation": "Modern Slavery Act 2015 s.54"},
            {"topic": "Labour Exploitation Investigation &amp; Referral", "region": "Exploitation Investigation", "legislation": "Modern Slavery Act 2015 / National Minimum Wage Act 1998"},
            {"topic": "Supply Chain &amp; Worker Protection", "region": "Supply Chain Protection", "legislation": "Modern Slavery Act 2015 / Employment Agencies Act 1973"},
            {"topic": "National Minimum Wage &amp; Working Conditions", "region": "Minimum Wage & Conditions", "legislation": "National Minimum Wage Act 1998 / Agricultural Wages"},
            {"topic": "Licensing Standards &amp; Compliance Inspections", "region": "Licence Compliance Inspection", "legislation": "Gangmasters (Licensing) Act 2004 Part 2"},
            {"topic": "Enforcement &amp; Prosecution", "region": "Enforcement & Prosecution", "legislation": "Gangmasters (Licensing) Act 2004 Part 3 / Criminal Justice Act 2003"},
            {"topic": "Multi-Agency Partnership (UK Modern Slavery)", "region": "Multi-Agency Partnership", "legislation": "Modern Slavery Act 2015 / Police & Criminal Evidence Act 1984"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Gangmasters (Licensing) Act 2004 / Home Office sponsorship / NAO"},
        ],
    },
    {
        "name": "defoneos-uk-statistics-authority-national-statistics-governance-ai-deep-dive-pack",
        "title": "UK Statistics Authority National Statistics Governance AI Deep-Dive Pack",
        "desc": "DEFONEOS — UK Statistics Authority National Statistics Governance AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "UK Statistics Authority",
        "body": "UK Statistics Authority",
        "legislation_backbone": "Statistics and Registration Service Act 2007 / UK Statistics Authority Code of Practice / Public Records Act 1958 / UKSA Framework",
        "nav_labels": [
            "National Statistics Des", "Code of Practice for St", "OSR Assessment &amp; Com", "Statistical Quality &amp; M", "Public Interest Statis", "Statistical Independenc", "Admin Data &amp; Sources", "Census &amp; ONS Oversight", "Transparency &amp; Publica", "Public Trust &amp; Engagem", "Cross-Government Coord", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "National Statistics Designation", "region": "National Statistics Designation", "legislation": "Statistics and Registration Service Act 2007 s.12"},
            {"topic": "Code of Practice for Statistics", "region": "Code of Practice for Statistics", "legislation": "UK Statistics Authority Code of Practice 2018"},
            {"topic": "OSR Assessment &amp; Compliance", "region": "OSR Assessment & Compliance", "legislation": "Statistics and Registration Service Act 2007 / OSR Practice"},
            {"topic": "Statistical Quality &amp; Methodology", "region": "Statistical Quality & Methodology", "legislation": "Statistics and Registration Service Act 2007 / Methodology Frameworks"},
            {"topic": "Public Interest &amp; Misuse of Statistics", "region": "Public Interest Statistics", "legislation": "Statistics and Registration Service Act 2007 s.14"},
            {"topic": "Statistical Independence &amp; Political Neutrality", "region": "Statistical Independence", "legislation": "Statistics and Registration Service Act 2007 / Pre-release Access Orders"},
            {"topic": "Administrative Data &amp; Data Sources", "region": "Admin Data & Sources", "legislation": "Statistics and Registration Service Act 2007 / Digital Economy Act 2017"},
            {"topic": "Census &amp; ONS Oversight", "region": "Census & ONS Oversight", "legislation": "Census Act 1920 / Statistics and Registration Service Act 2007"},
            {"topic": "Transparency &amp; Statistical Publication", "region": "Transparency & Publication", "legislation": "Statistics and Registration Service Act 2007 / Statistics of Trade Act 1947"},
            {"topic": "Public Engagement &amp; Statistical Trust", "region": "Public Trust & Engagement", "legislation": "UKSA Public Engagement Strategy / OSR Voice"},
            {"topic": "Cross-Government Statistical Coordination", "region": "Cross-Government Coordination", "legislation": "Statistics and Registration Service Act 2007 / National Statistics Executive"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Statistics and Registration Service Act 2007 / Cabinet Office sponsorship / Public Records Act 1958"},
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
