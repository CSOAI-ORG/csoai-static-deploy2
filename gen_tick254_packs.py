#!/usr/bin/env python3
"""Tick 254 generator: 3 UK regulator deep-dive packs (DBS / OISC / PSA).

Replicates the tick-253 pack format exactly: inline CSS, 12 entry points,
8 priority cards per entry point, 6 MCP chips per entry point, canonical and
alternate links resolving to real filenames, schema.org JSON-LD.
"""
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

MCP_CHIPS = [
    "mcp-bailii", "mcp-govuk-search", "mcp-hansard-search",
    "mcp-uk-courts", "mcp-uk-legislation", "mcp-uk-regulator-intel",
]

CARDS = [
    ("Compliance Automation",
     "Automated {REG} regulation {EP} validation checking {LAW} against {EP} statutory and rulebook requirements. "
     "No {REG} regulation activity proceeds without a signed, auditable compliance record."),
    ("Risk Detection & Early Warning",
     "Detection of {EP} risk breaches, control gaps, and early-warning indicators affecting {REG} regulation performance and accountability to Parliament."),
    ("Natural Language Policy Analysis",
     "NLP analysis of {EP} legislation, policy statements, guidance, and parliamentary record against the full statutory framework and regulatory expectations."),
    ("Predictive Analytics",
     "{EP} risk and workload forecasting from trend indicators, demand signals, and operational metrics to support prioritisation and decision-support."),
    ("Evidence Synthesis",
     "{EP} evidence, inspection findings, returns, and stakeholder submissions assembled into decision dossiers for review by accountable officers and the BFT council."),
    ("Document Intelligence",
     "Extraction from {EP} documents, statutory returns, and correspondence for end-to-end {REG} regulation lifecycle tracking and audit trails."),
    ("Stakeholder Reporting",
     "{EP} dashboards reporting coverage, performance, and outcomes to ministers, the board, and Parliament."),
    ("Real-time Monitoring",
     "{EP} pipeline tracking, submission cycles, and continuous surveillance of {REG} regulation activity for sovereign, verifiable oversight."),
]


def entry_section(idx, title, reg, law):
    cards = "\n".join(
        f'<div class="p"><h3>{h}</h3><p>{p.format(REG=reg, EP=title, LAW=law)}</p></div>'
        for h, p in CARDS
    )
    chips = "\n".join(f'<span class="t">{c}</span>' for c in MCP_CHIPS)
    return (
        f'<div class="s" id="ep{idx}">'
        f'<div class="sh"><span class="en">Entry Point {idx:02d}</span><h2>{title}</h2></div>'
        f'<div class="sb"><div class="g">{cards}</div>'
        f'<div class="mt"><h4>MCP Tools</h4><div class="ml">{chips}</div></div>'
        f'</div></div>'
    )


def build_pack(slug, title, reg, sub_domain, laws, law_primary, entry_points, ts):
    full = f"{slug}.html"
    url = f"https://www.csoai.org/{full}"
    desc = (f"DEFONEOS — {title}. A sovereign, audit-grade CSOAI surface: "
            f"measurement, not certification — every figure traces to a signed, verifiable record.")
    nav = "".join(
        f'<a href="#ep{i+1}">{ep[:23]}</a>' for i, ep in enumerate(entry_points)
    )
    sections = "".join(
        entry_section(i + 1, ep, reg, law_primary) for i, ep in enumerate(entry_points)
    )
    jsonld = (
        '{"@context":"https://schema.org","@type":"WebPage",'
        f'"name":"{title}","url":"{url}",'
        f'"publisher":{{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"}}}}'
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{title}</title>
<style>{CSS}</style>
<link href="https://www.csoai.org/{full}.llm.json" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>
<meta content="/llms.txt" name="llms-txt"/>
<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>
<meta content="CSOAI Ltd (2026). {title}. {url}" name="citation-policy"/>
<meta content="{ts}" name="revised"/>
<meta content="{ts}" property="article:modified_time"/>
<meta content="{desc}" name="description"/>
<link href="{url}" rel="canonical"/>
<meta content="{title}" property="og:title"/>
<meta content="{desc}" property="og:description"/>
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
<div class="hero">
<h1>🛡️ {title}</h1>
<p class="sub">DEFONEOS — UK Sovereign Public Services OS</p>
<div><span class="bg">12 Entry Points</span><span class="bg">8 AI Priorities</span><span class="bg">6 MCP Tools</span></div>
<p>96 AI capability mappings × 6 MCP integrations — {sub_domain}</p>
</div>
<nav>
{nav}
</nav>
<div class="c">
{sections}
</div>
<footer>
<div class="br">DEFONEOS — UK Sovereign Public Services OS</div>
<p>Open-source sovereign AI governance for {reg}. Built for audit-grade, signed, neutral UK-sovereign compliance.</p>
<p>AUKUS-compatible. {laws}.</p>
<div class="cr">© 2026 CSOAI Ltd (UK 16939677) · meok-defoneos · csoai-defoneos · DEFONEOS-SEAL</div>
</footer>
</body>
</html>
"""


PACKS = [
    dict(
        slug="defoneos-dbs-disclosure-barring-service-safeguarding-ai-deep-dive-pack",
        title="Disclosure & Barring Service Safeguarding Checks AI Deep-Dive Pack",
        reg="Disclosure & Barring Service",
        sub_domain="DBS safeguarding check and barring decision regulation",
        laws=("Protection of Freedoms Act 2012 / Safeguarding Vulnerable Groups Act 2006 / "
              "Police Act 1997 / Data Protection Act 2018"),
        law_primary="Protection of Freedoms Act 2012",
        entry_points=[
            "DBS Check Types & Eligibility",
            "Standard & Enhanced Certificate Processing",
            "Barred Lists Management (Children & Adults)",
            "Safeguarding Decision-Making & Review",
            "Employer & Regulated Activity Checks",
            "Update Service & Portable Certificates",
            "Application Data & Identity Verification",
            "Criminal Record Data Handling & Accuracy",
            "Appeals, Disputes & Corrections",
            "Referral Handling & Disclosure Logic",
            "Counter-Signatory & Umbrella Body Oversight",
            "Governance & Parliamentary Accountability",
        ],
        ts="2026-08-10T20:00:00+00:00",
    ),
    dict(
        slug="defoneos-oisc-office-immigration-services-commissioner-ai-deep-dive-pack",
        title="Office of the Immigration Services Commissioner Regulation AI Deep-Dive Pack",
        reg="Office of the Immigration Services Commissioner",
        sub_domain="OISC immigration advice regulation",
        laws=("Immigration and Asylum Act 1999 / Immigration Act 2014 / "
              "Immigration Act 2016 / UK Borders Act 2007"),
        law_primary="Immigration and Asylum Act 1999",
        entry_points=[
            "Immigration Advice Regulation & Scope",
            "Adviser Registration & Competence",
            "Code of Standards Compliance",
            "Complaint Handling & Investigation",
            "Enforcement & Sanctions",
            "Unauthorised Advice & Consumer Harm",
            "Fee Charging & Transparency",
            "Casework Oversight & Quality Assurance",
            "Immigration Legal Framework Monitoring",
            "Consumer Protection & Vulnerable Clients",
            "Technology & Digital Services Standards",
            "Governance & Parliamentary Accountability",
        ],
        ts="2026-08-10T20:00:00+00:00",
    ),
    dict(
        slug="defoneos-psa-professional-standards-authority-health-care-ai-deep-dive-pack",
        title="Professional Standards Authority Health & Care Regulation Oversight AI Deep-Dive Pack",
        reg="Professional Standards Authority for Health and Social Care",
        sub_domain="PSA oversight of health and care regulators",
        laws=("NHS Reform and Health Care Professions Act 2002 / Health and Social Care Act 2012 / "
              "Care Standards Act 2000 / Health Act 1999"),
        law_primary="NHS Reform and Health Care Professions Act 2002",
        entry_points=[
            "Regulator Oversight & Accreditation",
            "Performance Review of Health Regulators",
            "Fitness to Practise Appeal Adjudication",
            "Right to Practise & Regulator Decisions",
            "Accredited Registers Programme",
            "Public Protection Standards",
            "Continuous Improvement & Risk Monitoring",
            "Complaints & Escalation Handling",
            "Cross-Regulator Consistency",
            "Evidence-Based Regulation & Research",
            "Digital & Data Standards in Regulation",
            "Governance & Parliamentary Accountability",
        ],
        ts="2026-08-10T20:00:00+00:00",
    ),
]


def main():
    for p in PACKS:
        html = build_pack(**p)
        out = ROOT / f"{p['slug']}.html"
        out.write_text(html, encoding="utf-8")
        print(f"{out.name}: {len(html.encode('utf-8'))} bytes")


if __name__ == "__main__":
    main()