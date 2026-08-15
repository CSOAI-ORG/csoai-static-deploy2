#!/usr/bin/env python3
"""Tick 288 deep-dive pack generator: Scottish Police Authority, Education Scotland, Scottish Fire & Rescue."""
import os, json, hashlib, datetime

PACKS = [
    {
        "slug": "defoneos-scottish-police-authority-police-oversight-ai-deep-dive-pack",
        "title": "Scottish Police Authority — AI Governance Deep-Dive Pack",
        "agency": "Scottish Police Authority (SPA)",
        "agency_url": "https://www.spa.police.uk/",
        "domain": "Police Oversight & Forensic Services",
        "desc": "The Scottish Police Authority is the oversight and governance body for Police Scotland, responsible for police custody, forensic services, and independent custody visiting across Scotland. This deep-dive pack maps 12 entry points for AI governance, 8 transformation priorities, 6 MCP servers, and 6 non-negotiable red lines anchored in devolved Scottish justice legislation.",
        "entry_points": [
            ("Police Scotland Oversight & Scrutiny", "Board-level governance and public scrutiny of Police Scotland operations, budget, and strategic direction. AI-assisted oversight dashboards tracking use-of-force, stop-and-search, and complaint patterns.", "oversight"),
            ("Forensic Services Regulation & Quality", "National forensic science services including DNA analysis, toxicology, fingerprint identification, and digital forensics. AI chain-of-custody for forensic evidence management.", "forensic"),
            ("Independent Custody Visiting", "Volunteer-led independent inspection of police custody facilities across Scotland. AI scheduling, pattern detection, and automated custody-visit compliance reporting.", "custody"),
            ("Complaints Handling & Review", "Independent review of complaints against Police Scotland officers and staff. AI triage, sentiment analysis, and bias-detection in complaint classification.", "complaints"),
            ("Police Budget & Financial Governance", "Annual budget allocation (2025-26: £1.5bn+), financial oversight, and procurement audit. AI forensic accounting for police expenditure monitoring.", "budget"),
            ("Workforce Planning & HR Governance", "Police Scotland workforce ~22,000 officers and staff. AI workforce modelling, succession planning, diversity monitoring, and wellbeing analytics.", "workforce"),
            ("Information Management & FOI", "Freedom of Information requests, data protection, and records management for Scottish policing. AI FOI triage and automated redaction review.", "information"),
            ("Performance & Improvement Framework", "Scottish policing performance indicators, benchmarking, and continuous improvement. AI performance analytics and predictive service-delivery modelling.", "performance"),
            ("Strategic Police Priorities", "Scottish Ministers' strategic police priorities and SPA's role in delivery assurance. AI policy impact assessment against Scottish Government outcomes.", "priorities"),
            ("Equality & Human Rights Compliance", "Public Sector Equality Duty (PSED), Equality Act 2010, Human Rights Act 1998, and Scotland-specific duties. AI equality impact assessment automation.", "equality"),
            ("Criminal Justice & Court Interface", "SPA's role in the Scottish criminal justice system including forensic evidence for courts. AI evidence continuity tracking and disclosure management.", "justice"),
            ("Governance & Scottish Parliament Accountability", "SPA accountability to Scottish Ministers, Scottish Parliament's Criminal Justice Committee, and Audit Scotland. AI governance reporting and parliamentary evidence automation.", "governance")
        ],
        "priorities": [
            "AI-assisted police oversight dashboards replacing quarterly manual reports → real-time governance visibility, 90% report compilation reduction",
            "Forensic evidence AI chain-of-custody replacing paper-based logging → tamper-evident digital audit trails, 100% traceability",
            "Automated custody-visit scheduling replacing manual coordinator rotas → 40% more visits, real-time health/welfare alerts",
            "AI complaint triage with bias detection replacing manual classification → consistent dispositions, protected-characteristic monitoring",
            "Predictive workforce modelling replacing annual spreadsheet forecasting → scenario-based planning, diversity trajectory tracking",
            "AI FOI redaction review replacing manual document review → 70% faster response, consistent redaction policy",
            "Real-time police performance analytics replacing quarterly paper reports → live dashboards, outlier detection, early intervention",
            "Equality impact assessment automation replacing manual EIAs → consistent methodology, cumulative-impact tracking across police policy"
        ],
        "mcps": [
            ("defoneos-police-oversight-mcp", "Governance", "Police Scotland board-level oversight dashboards, use-of-force analytics, complaint pattern detection, custody compliance monitoring"),
            ("defoneos-forensic-chain-mcp", "Forensic", "Forensic evidence chain-of-custody, DNA/trace evidence tracking, digital forensics audit, court disclosure management"),
            ("defoneos-custody-safeguarding-mcp", "Public Safety", "Custody-visit scheduling, health/welfare alerting, independent visitor compliance, pattern-of-concern detection"),
            ("defoneos-police-complaints-mcp", "Governance", "Complaint triage, bias detection, protected-characteristic monitoring, outcome consistency analysis"),
            ("defoneos-police-finance-mcp", "Finance", "Police budget analytics, procurement audit, forensic accounting, value-for-money assessment"),
            ("defoneos-police-equality-mcp", "Compliance", "Equality impact assessment, PSED compliance tracking, human rights compatibility check, diversity monitoring")
        ],
        "red_lines": [
            "Police and Fire Reform (Scotland) Act 2012 — SPA statutory functions, Board governance, and accountability framework. AI must not circumvent SPA Board oversight.",
            "Fire (Scotland) Act 2005 & Police and Fire Reform (Scotland) Act 2012 — Custody visiting standards, forensic service requirements. AI must not replace human custody visitors.",
            "Data Protection Act 2018 Part 3 (Law Enforcement Processing) — Sensitive police data processing. AI must operate within the law-enforcement-specific DPA regime.",
            "Equality Act 2010 (Public Sector Equality Duty) — Scotland-specific duties. AI must not introduce or amplify protected-characteristic disparities.",
            "Human Rights Act 1998 — Article 2 (right to life), Article 3 (prohibition of torture), Article 8 (private life). AI must not contribute to human rights breaches.",
            "Scotland Act 1998 — Devolved policing, criminal justice, and forensic services. AI must respect Scottish devolved competence and Parliamentary accountability."
        ],
        "legislation": "Police and Fire Reform (Scotland) Act 2012 / Fire (Scotland) Act 2005 / DPA 2018 Part 3 / Equality Act 2010 / Human Rights Act 1998 / Scotland Act 1998 / Public Services Reform (Scotland) Act 2010"
    },
    {
        "slug": "defoneos-education-scotland-school-improvement-ai-deep-dive-pack",
        "title": "Education Scotland — AI Governance Deep-Dive Pack",
        "agency": "Education Scotland",
        "agency_url": "https://education.gov.scot/",
        "domain": "School Improvement & Curriculum",
        "desc": "Education Scotland is the national improvement agency for Scottish education, supporting quality and improvement in learning from early years to adult learning, including school inspection, curriculum development, and practitioner support. This deep-dive pack maps 12 entry points for AI governance, 8 transformation priorities, 6 MCP servers, and 6 non-negotiable red lines anchored in devolved Scottish education legislation.",
        "entry_points": [
            ("School Inspection & Quality Improvement", "HM Inspectors of Education conduct inspections across Scottish schools, early learning, and community learning. AI inspection scheduling, evidence synthesis, and quality indicator benchmarking.", "inspection"),
            ("Curriculum for Excellence (CfE) Support", "National curriculum framework for ages 3-18. AI curriculum mapping, resource recommendation, and CfE outcomes tracking.", "curriculum"),
            ("Attainment & Achievement Data", "Scottish Survey of Literacy and Numeracy (SSLN), National Qualifications data, and attainment gap monitoring. AI attainment analytics with SIMD correlation.", "attainment"),
            ("Practitioner Professional Learning", "Teacher professional development, leadership programmes, and SCEL (Scottish College for Educational Leadership). AI CPD matching and professional-learning needs analysis.", "professional"),
            ("Digital Learning & Technology Strategy", "Scottish digital learning strategy, Glow platform, and edtech adoption. AI digital-skills gap analysis and technology-impact evaluation.", "digital"),
            ("Additional Support for Learning (ASL)", "Support for pupils with additional support needs under the Education (Additional Support for Learning) (Scotland) Act 2004. AI ASL needs identification and support-plan monitoring.", "asl"),
            ("Early Learning & Childcare", "Quality improvement in early learning and childcare settings. AI quality indicator tracking and early-intervention analytics.", "early"),
            ("Community Learning & Development", "Adult learning, youth work, and community capacity building. AI participation analytics and social-outcome measurement.", "community"),
            ("Equality & Inclusion in Education", "Equalities monitoring including gender, race, disability, and socio-economic background. AI equality analytics and closing-the-gap tracking.", "equality"),
            ("School Governance & Parental Engagement", "Parent councils, school leadership governance, and community engagement. AI parental-engagement analytics and governance compliance tracking.", "governance"),
            ("Data Protection & Pupil Records", "Pupil data management under DPA 2018 and Pupils' Educational Records (Scotland) Regulations 2003. AI data-protection compliance and secure-record management.", "data"),
            ("Governance & Scottish Parliament Accountability", "Education Scotland's accountability to Scottish Ministers, Scottish Parliament Education Committee, and COSLA. AI governance reporting and parliamentary evidence automation.", "parliament")
        ],
        "priorities": [
            "AI inspection evidence synthesis replacing manual inspector review → 60% report writing reduction, consistent quality indicators",
            "AI curriculum mapping for CfE outcomes replacing manual teacher mapping → personalised learning pathways, outcomes tracking",
            "AI attainment gap analytics with real-time SIMD correlation replacing annual manual reports → early intervention triggers, live dashboards",
            "AI professional learning matching replacing generic CPD catalogues → personalised development pathways, skill-gap closure tracking",
            "AI digital-skills gap analysis replacing periodic surveys → continuous monitoring, school-level technology readiness indices",
            "AI ASL needs identification and support-plan monitoring replacing paper-based reviews → proactive intervention, outcome tracking",
            "AI equality analytics replacing manual annual equalities returns → real-time protected-characteristic monitoring, intersectional gap analysis",
            "AI governance reporting replacing manual parliamentary return compilation → automated compliance evidence packs, Committee-ready briefings"
        ],
        "mcps": [
            ("defoneos-school-inspection-mcp", "Education", "School inspection scheduling, quality indicator benchmarking, evidence synthesis, inspection-report generation"),
            ("defoneos-attainment-analytics-mcp", "Education", "SSLN and National Qualifications analytics, SIMD correlation, attainment-gap monitoring, predictive intervention"),
            ("defoneos-curriculum-mapping-mcp", "Education", "CfE outcomes mapping, personalised learning pathways, resource recommendation, progression tracking"),
            ("defoneos-asl-support-mcp", "Education", "ASL needs identification, support plan monitoring, intervention tracking, outcome evaluation"),
            ("defoneos-education-equality-mcp", "Compliance", "Protected-characteristic monitoring, PSED compliance, intersectional gap analysis, equalities return automation"),
            ("defoneos-education-governance-mcp", "Governance", "School governance compliance, parental engagement analytics, parliamentary return automation, Audit Scotland reporting")
        ],
        "red_lines": [
            "Education (Scotland) Act 1980 — Duties of education authorities, provision of education. AI must not replace professional teacher judgement or HM Inspector discretion.",
            "Standards in Scotland's Schools etc. Act 2000 — Right to education, improvement objectives. AI must not narrow the curriculum or reduce education to algorithmic optimisation.",
            "Education (Additional Support for Learning) (Scotland) Act 2004 — ASL duties, CSP coordination. AI must identify but not gatekeep ASL provision.",
            "Data Protection Act 2018 — Pupil records, special category data (children). AI must operate within the strictest data-protection regime for children's educational data.",
            "Equality Act 2010 (Public Sector Equality Duty) — Scotland-specific education duties. AI must not introduce or amplify attainment disparities across protected characteristics.",
            "Scotland Act 1998 — Devolved education, curriculum, inspection, and qualifications. AI must respect Scottish devolved competence and CfE autonomy."
        ],
        "legislation": "Education (Scotland) Act 1980 / Standards in Scotland's Schools etc. Act 2000 / Education (Additional Support for Learning) (Scotland) Act 2004 / DPA 2018 / Equality Act 2010 / Scotland Act 1998 / Children and Young People (Scotland) Act 2014"
    },
    {
        "slug": "defoneos-scottish-fire-rescue-service-emergency-response-ai-deep-dive-pack",
        "title": "Scottish Fire and Rescue Service — AI Governance Deep-Dive Pack",
        "agency": "Scottish Fire and Rescue Service (SFRS)",
        "agency_url": "https://www.firescotland.gov.uk/",
        "domain": "Fire, Rescue & Emergency Response",
        "desc": "The Scottish Fire and Rescue Service is the national fire and rescue service for Scotland, providing prevention, protection, and emergency response across all 32 local authority areas. It is the largest fire and rescue service in the UK by territory covered. This deep-dive pack maps 12 entry points for AI governance, 8 transformation priorities, 6 MCP servers, and 6 non-negotiable red lines anchored in devolved Scottish fire safety legislation.",
        "entry_points": [
            ("Emergency Response Operations", "24/7 emergency response including fires, road traffic collisions, water rescue, hazardous materials, and urban search and rescue. AI dispatch optimisation, resource allocation, and real-time incident intelligence.", "response"),
            ("Fire Prevention & Community Safety", "Home fire safety visits, school education programmes, and community engagement. AI risk-profiling for targeted prevention and vulnerability mapping.", "prevention"),
            ("Fire Safety Enforcement & Regulation", "Enforcement of fire safety legislation under the Fire (Scotland) Act 2005, including premises inspection and enforcement notices. AI inspection scheduling and compliance analytics.", "enforcement"),
            ("Unwanted Fire Alarm Reduction", "Reducing unnecessary callouts from automatic fire alarms — a major resource drain. AI alarm-signal pattern classification for false-alarm prediction.", "alarms"),
            ("Specialist Rescue Capability", "Water rescue, line rescue, heavy rescue, and USAR. AI resource modelling for specialist-team positioning across Scottish geography.", "rescue"),
            ("Wildfire & Rural Fire Management", "Scotland's vast rural landscape and increasing wildfire risk. AI satellite-based fire-risk prediction, fuel-load modelling, and resource pre-positioning.", "wildfire"),
            ("Climate Adaptation & Resilience", "Climate change impacts on fire and rescue demand — flooding, wildfires, extreme weather. AI climate-risk modelling and adaptive-resource planning.", "climate"),
            ("Workforce Health, Safety & Wellbeing", "Firefighter occupational health, fitness standards, mental health support, and exposure monitoring. AI health-surveillance analytics and early-warning systems.", "workforce"),
            ("Fleet & Asset Management", "SFRS fleet of 380+ fire appliances, 3,500+ operational personnel, 356 fire stations. AI fleet maintenance prediction and asset-lifecycle optimisation.", "fleet"),
            ("Community Risk Management Planning", "Strategic assessment of fire and rescue risk across Scottish communities. AI multi-factor risk modelling and resource-distribution optimisation.", "risk"),
            ("Data Protection & Incident Records", "Incident data management, fire investigation records, and personal data handling. AI secure incident-data analytics with DPA-compliant anonymisation.", "data"),
            ("Governance & Scottish Parliament Accountability", "SFRS Board governance, Scottish Ministers oversight, and Scottish Parliament accountability. AI governance reporting and Audit Scotland compliance.", "governance")
        ],
        "priorities": [
            "AI dispatch optimisation replacing manual resource allocation → dynamic stationing, 20% faster first-appliance arrival in rural areas",
            "AI risk-profiling for targeted prevention replacing blanket home safety visits → 5x more effective resource targeting, vulnerable-person prioritisation",
            "AI wildfire prediction replacing reactive rural-resource positioning → satellite-informed fuel-load modelling, pre-season prepositioning",
            "AI false-alarm classification replacing generic callout response → 30% reduction in unnecessary appliance movements, station availability gain",
            "AI climate-risk modelling replacing periodic climate-adaptation reports → continuous risk monitoring, live resource redistribution triggers",
            "AI firefighter health surveillance replacing annual medicals → continuous exposure monitoring, early-warning cancer/respiratory alerts",
            "AI fleet maintenance prediction replacing scheduled replacement cycles → condition-based maintenance, 15% fleet downtime reduction",
            "AI governance reporting replacing quarterly manual Board reports → automated SPCB-ready evidence, live operational dashboards"
        ],
        "mcps": [
            ("defoneos-fire-dispatch-mcp", "Emergency", "Emergency call triage, dynamic resource allocation, rural response optimisation, incident intelligence"),
            ("defoneos-fire-prevention-mcp", "Public Safety", "Home fire risk profiling, vulnerability mapping, targeted prevention scheduling, community safety analytics"),
            ("defoneos-fire-enforcement-mcp", "Compliance", "Fire safety inspection scheduling, premises compliance tracking, enforcement notice management, audit trail"),
            ("defoneos-wildfire-prediction-mcp", "Environment", "Satellite-based fire risk, fuel-load modelling, resource prepositioning, climate-correlated risk forecasting"),
            ("defoneos-firefighter-health-mcp", "Health", "Occupational exposure monitoring, health surveillance, cancer/respiratory early warning, fitness-for-duty analytics"),
            ("defoneos-fire-governance-mcp", "Governance", "SFRS Board reporting, Audit Scotland compliance, performance indicators, parliamentary evidence packs")
        ],
        "red_lines": [
            "Fire (Scotland) Act 2005 — Statutory duties for firefighting, fire prevention, and fire safety enforcement. AI must not override Incident Commander operational discretion at scene.",
            "Police and Fire Reform (Scotland) Act 2012 — SFRS establishment, Board governance, and Chief Officer accountability. AI must operate within the statutory command structure.",
            "Fire (Scotland) Act 2005 Part 3 — Fire safety enforcement powers including prohibition and enforcement notices. AI must not issue or modify enforcement notices autonomously.",
            "Health and Safety at Work etc. Act 1974 — Firefighter safety at operational incidents. AI must not compromise responder safety for efficiency gains.",
            "Data Protection Act 2018 — Incident records, personal data, fire investigation reports. AI must maintain strict DPA-compliant data handling and anonymisation.",
            "Scotland Act 1998 — Devolved fire and rescue services, community safety, and emergency planning. AI must respect Scottish devolved competence and Parliamentary accountability."
        ],
        "legislation": "Fire (Scotland) Act 2005 / Police and Fire Reform (Scotland) Act 2012 / Health and Safety at Work etc. Act 1974 / DPA 2018 / Equality Act 2010 / Scotland Act 1998 / Civil Contingencies Act 2004"
    }
]

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
<a href=\"/\">🜏 Home</a>
<a href=\"/governance-master.html\">Master</a>
<a href=\"/govbench.html\">GovBench</a>
<a href=\"/sitemap.html\">Index</a>
<a href=\"/sitemap.xml\">Sitemap</a>
</nav>"""

EU_BANNER = """<div class=\"eu-banner\">
⚖️ EU AI Act — Article 50 Transparency + Annex III High-Risk classification applies to public-sector AI deployment. This pack is a governance-design document — not a compliance certification. <a href=\"/governance-master.html\">Read the governance framework →</a>
</div>"""

FOOTER = """<footer>
<p>CSOAI Ltd (UK 16939677) · csoai.org · compliance@csoai.org</p>
<p>DEFONEOS is a UK-sovereign open-source AI governance framework built on the meok substrate. UK-sovereign. AUKUS-compatible. Audit-grade.</p>
<p style=\"margin-top:8px;font-size:11px\">© 2026 CSOAI Ltd. All trademarks acknowledged. This document is a governance-design artefact — not a compliance certification.</p>
</footer>"""

TODAY = datetime.date.today().isoformat()
SIGIL = hashlib.sha256(f"DEFONEOS|tick-288|3-packs|{TODAY}".encode()).hexdigest()[:16]

def build_entry_point(ep):
    name, desc, tag = ep
    return f"""<div class=\"card\">
<span class=\"tag\">{tag.upper()}</span>
<h3>{name}</h3>
<p>{desc}</p>
</div>"""

def build_priority(p, i):
    return f"""<div class=\"card priority\">
<span class=\"tag\">Priority {i+1}</span>
<p style=\"font-size:13px;color:var(--muted)\">{p}</p>
</div>"""

def build_mcp(mcp, i):
    name, cat, desc = mcp
    return f"""<div class=\"card mcp\">
<span class=\"tag\">MCP {i+1} · {cat}</span>
<h3>{name}</h3>
<p>{desc}</p>
</div>"""

def build_red_line(rl):
    return f"<li>{rl}</li>"

def build_engagement():
    steps = [
        ("Discovery", "Map the agency's statutory duties, data flows, and governance gaps against the 12-entry-point framework."),
        ("Governance Design", "Design AI governance architecture, risk appetite, and red-line enforcement aligned to devolved legislation."),
        ("Pilot", "Deploy 2-3 MCP servers in a sandboxed environment with agency data; measure governance outcomes against baseline."),
        ("Scale", "Expand to the full 6-MCP stack with agency-wide deployment, training, and change management."),
        ("Assure", "Continuous monitoring, 33-agent BFT council verification, and DEFONEOS-SEAL credential issuance.")
    ]
    out = []
    for i, (title, desc) in enumerate(steps):
        out.append(f"""<div class=\"step\">
<div class=\"num\">{i+1}</div>
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

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">
<title>{p['title']}</title>
<meta name=\"description\" content=\"{p['desc'][:160]}\">
<link rel=\"canonical\" href=\"https://csoai.org/{slug}.html\">
<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@700&display=swap\" rel=\"stylesheet\">
{CSS}
</head>
<body>
{EU_BANNER}
{NAV}
<div class=\"container\">
<h1>{p['title']}</h1>
<p class=\"subtitle\">{p['domain']} · {p['agency']} · {TODAY}</p>

<div class=\"stats\">
<div class=\"stat-card\"><div class=\"stat-num\">12</div><div class=\"stat-label\">Entry Points</div></div>
<div class=\"stat-card\"><div class=\"stat-num\">8</div><div class=\"stat-label\">Transformation Priorities</div></div>
<div class=\"stat-card\"><div class=\"stat-num\">6</div><div class=\"stat-label\">MCP Servers</div></div>
<div class=\"stat-card\"><div class=\"stat-num\">6</div><div class=\"stat-label\">Red Lines</div></div>
</div>

<h2>📋 12 Entry Points</h2>
<div class=\"grid\">{entry_html}</div>

<h2>🎯 8 Transformation Priorities</h2>
<div class=\"grid\">{priority_html}</div>

<h2>🔧 6 MCP Servers</h2>
<div class=\"grid\">{mcp_html}</div>

<h2>🚫 6 Non-Negotiable Red Lines</h2>
<div class=\"red-lines\">
<h3>Governance Red Lines — Anchored in Statute</h3>
<ul>{red_html}</ul>
</div>

<h2>⚡ 5-Step Engagement Model</h2>
<div class=\"engagement\">{engage_html}</div>

<div class=\"cta\">
<a href=\"/governance-master.html\">📋 Request OWEM RFQ →</a>
<a href=\"/article-50.html\" class=\"secondary\">⚖️ Article 50 Passport →</a>
</div>

<p style=\"font-size:12px;color:var(--muted);margin-top:24px\">Legislation backbone: {p['legislation']}</p>
<p style=\"font-size:12px;color:var(--muted);margin-top:8px\">SIGIL: defoneos-tick288-{slug[:30]}-{SIGIL}</p>
</div>
{FOOTER}
<script type=\"application/ld+json\">
{json.dumps(ld, indent=2)}
</script>
</body>
</html>"""
    return html

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
            "tick": 288,
            "sigil": hashlib.sha256(html.encode()).hexdigest()[:16]
        }
        llm_name = f"{fname}.llm.json"
        with open(llm_name, "w") as f:
            json.dump(llm, f, indent=2)
        llm_sz = os.path.getsize(llm_name)
        written.append((llm_name, llm_sz))
        
        print(f"✓ {fname} ({sz:,}b) + .llm.json ({llm_sz}b)")

    # Verify all files written
    print(f"\nTotal: {len(written)} files, {sum(sz for _, sz in written):,} bytes")
    
    # Write tick sigil
    sigil_data = {
        "tick": 288,
        "date": TODAY,
        "packs_built": 3,
        "packs": [p["slug"] for p in PACKS],
        "sigil": SIGIL,
        "verify": sum(sz for _, sz in written)
    }
    with open("tick-288-sigil.json", "w") as f:
        json.dump(sigil_data, f, indent=2)
    print(f"✓ tick-288-sigil.json ({os.path.getsize('tick-288-sigil.json'):,}b)")

if __name__ == "__main__":
    main()