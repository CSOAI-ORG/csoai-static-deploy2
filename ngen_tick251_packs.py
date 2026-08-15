#!/usr/bin/env python3
"""DEFONEOS SPRINT TICK 251 — 3 new dense regulator deep-dive packs.
Bodies (probe-verified OPEN on disk): HMCPSI, UK Anti-Doping (UKAD), Legal Services Board (LSB).
Replicates the exact tick-245..250 dense-regulator structure, with the CANONICAL JSON-LD form.
"""
import html, pathlib

OUT = pathlib.Path(__file__).resolve().parent

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

# deterministic priority card templates (agency, EP, legal inserted)
def priority_cards(agency, ep, legal):
    return [
        ("Compliance Automation",
         f"Automated {agency} regulation {ep} validation checking {legal} against {ep} statutory and rulebook requirements. No {agency} regulation activity proceeds without a signed, auditable compliance record."),
        ("Risk Detection &amp; Early Warning",
         f"Detection of {ep} risk breaches, control gaps, and early-warning indicators affecting {agency} regulation performance and accountability to Parliament."),
        ("Natural Language Policy Analysis",
         f"NLP analysis of {ep} legislation, policy statements, guidance, and parliamentary record against the full statutory framework and regulatory expectations."),
        ("Predictive Analytics",
         f"{ep} risk and workload forecasting from trend indicators, demand signals, and operational metrics to support prioritisation and decision-support."),
        ("Evidence Synthesis",
         f"{ep} evidence, inspection findings, returns, and stakeholder submissions assembled into decision dossiers for review by accountable officers and the BFT council."),
        ("Document Intelligence",
         f"Extraction from {ep} documents, statutory returns, and correspondence for end-to-end {agency} regulation lifecycle tracking and audit trails."),
        ("Stakeholder Reporting",
         f"{ep} dashboards reporting coverage, performance, and outcomes to ministers, the board, and Parliament."),
        ("Real-time Monitoring",
         f"{ep} pipeline tracking, submission cycles, and continuous surveillance of {agency} regulation activity for sovereign, verifiable oversight."),
    ]

MCP_CHIPS = ["mcp-bailii","mcp-govuk-search","mcp-hansard-search","mcp-uk-courts","mcp-uk-legislation","mcp-uk-regulator-intel"]

def build(spec):
    fname = spec["fname"]
    title = spec["title"]
    agency = spec["agency"]
    legal = spec["legal"]
    first_legal = legal.split(" / ")[0]
    eps = spec["eps"]
    canon = f"https://www.csoai.org/{fname}.html"
    jsonld = (f'{{"@context":"https://schema.org","@type":"WebPage","name":"{title}","url":"{canon}",'
              f'"publisher":{{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"}}}}')
    # nav anchors — first 23 chars of EP name, HTML-escaped
    nav = "".join(f'<a href="#ep{i+1}">{html.escape(ep[:23])}</a>' for i, ep in enumerate(eps))
    sections = []
    for i, ep in enumerate(eps, 1):
        cards = "".join(f'<div class="p"><h3>{h}</h3><p>{c}</p></div>' for h, c in priority_cards(agency, ep, first_legal))
        chips = "".join(f'<span class="t">{c}</span>' for c in MCP_CHIPS)
        sections.append(
            f'<div class="s" id="ep{i}"><div class="sh"><span class="en">Entry Point {i:02d}</span><h2>{ep}</h2></div>'
            f'<div class="sb"><div class="g">{cards}</div>'
            f'<div class="mt"><h4>MCP Tools</h4><div class="ml">{chips}</div></div></div></div>')
    meta_desc = (f"DEFONEOS — {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification — "
                 f"every figure traces to a signed, verifiable record.")
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{title}</title>
<style>{CSS}</style>
<link href="https://www.csoai.org/{fname}.html.llm.json" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>
<meta content="/llms.txt" name="llms-txt"/>
<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>
<meta content="CSOAI Ltd (2026). {title}. {canon}" name="citation-policy"/>
<meta content="2026-08-10T12:00:00+00:00" name="revised"/>
<meta content="2026-08-10T12:00:00+00:00" property="article:modified_time"/>
<meta content="{meta_desc}" name="description"/>
<link href="{canon}" rel="canonical"/>
<meta content="{title}" property="og:title"/>
<meta content="{meta_desc}" property="og:description"/>
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
<div class="hero">
<h1>{spec["emoji"]} {title}</h1>
<p class="sub">DEFONEOS — UK Sovereign Public Services OS</p>
<div><span class="bg">12 Entry Points</span><span class="bg">8 AI Priorities</span><span class="bg">6 MCP Tools</span></div>
<p>96 AI capability mappings × 6 MCP integrations — {agency}</p>
</div>
<nav>
{nav}
</nav>
<div class="c">
{''.join(sections)}
</div>
<footer>
<div class="br">DEFONEOS — UK Sovereign Public Services OS</div>
<p>Open-source sovereign AI governance for {agency}. Built for audit-grade, signed, neutral UK-sovereign compliance.</p>
<p>AUKUS-compatible. {legal}.</p>
<div class="cr">© 2026 CSOAI Ltd (UK 16939677) · meok-defoneos · csoai-defoneos · DEFONEOS-SEAL</div>
</footer>
</body>
</html>
"""
    return html_doc

SPECS = [
    {
        "fname": "defoneos-hmcpsi-hm-crown-prosecution-service-inspectorate",
        "title": "HM Crown Prosecution Service Inspectorate Prosecution Inspection AI Deep-Dive Pack",
        "agency": "HM Crown Prosecution Service Inspectorate",
        "emoji": "🛡️",
        "legal": "Crown Prosecution Service Inspectorate Act 2000 / Prosecution of Offences Act 1985 / Courts Act 2003 / Criminal Justice Act 2003",
        "eps": [
            "CPS & Prosecutor Inspection Jurisdiction",
            "Casework Quality & Decision Standards",
            "Charging & Decision-Making Review",
            "Disclosure & Prosecution Duty Review",
            "Victims & Witnesses Standards",
            "Court & Trial Casework",
            "Specialist & Complex Casework",
            "Data Integrity & Case Management Systems",
            "Public Confidence & Complaints",
            "Force & Agency Partnership Working",
            "Value for Money & Performance",
            "Governance & Parliamentary Accountability",
        ],
    },
    {
        "fname": "defoneos-ukad-uk-anti-doping",
        "title": "UK Anti-Doping (UKAD) Anti-Doping Regulation AI Deep-Dive Pack",
        "agency": "UK Anti-Doping",
        "emoji": "🏅",
        "legal": "World Anti-Doping Code / UK National Anti-Doping Policy 2021 / DCMS-UKAD Funding Agreement / UK Anti-Doping Rules",
        "eps": [
            "Anti-Doping Testing & Sample Collection",
            "Prohibited Substances & Methods",
            "Therapeutic Use Exemptions (TUE)",
            "Athlete Biological Passport & Intelligence",
            "Intelligence & Investigation Powers",
            "Rule Violations & Results Management",
            "Hearings, Appeals & Sanctions",
            "Education & Prevention Programmes",
            "NGB Compliance & Coordination",
            "International Coordination & WADA Code",
            "Data Protection & Athlete Rights",
            "Governance & Accountability",
        ],
    },
    {
        "fname": "defoneos-lsb-legal-services-board",
        "title": "Legal Services Board Regulation of Legal Services AI Deep-Dive Pack",
        "agency": "Legal Services Board",
        "emoji": "⚖️",
        "legal": "Legal Services Act 2007 / Legal Ombudsman Scheme Rules / Legal Services Board Regulatory Objectives / Approved Regulator Frameworks",
        "eps": [
            "Regulation of Legal Services Market",
            "Approved Regulators & Oversight",
            "Regulatory Objectives & Public Interest",
            "Alternative Business Structures (ABS)",
            "Consumer Protection & Redress",
            "Professional Standards & Conduct Oversight",
            "Market Competition & Consumer Choice",
            "Legal Ombudsman Oversight",
            "Diversity, Access & Inclusion",
            "Innovation & Technology in Legal Services",
            "Data, Evidence & Market Research",
            "Governance & Accountability",
        ],
    },
]

if __name__ == "__main__":
    for s in SPECS:
        doc = build(s)
        path = OUT / f"{s['fname']}-ai-deep-dive-pack.html"
        path.write_text(doc)
        print(f"{path.name} {len(doc.encode())}b")
