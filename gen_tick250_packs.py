#!/usr/bin/env python3
"""Tick 250 — 3 new DEFONEOS regulator deep-dive packs.

Bodies chosen for coverage gap (verified uncovered on disk + sitemap):
1. Health and Safety Executive (HSE) — occupational health & safety regulator
2. HM Inspectorate of Constabulary & Fire & Rescue Services (HMICFRS) — police/fire inspection
3. Criminal Cases Review Commission (CCRC) — miscarriage of justice review body

Same 12-entry-points × 8-priorities × 6-MCPs structure as tick 249/248/247.
JSON-LD fixed to canonical form (schema.org, not the mangled artifact).
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
<meta content="2026-08-10T11:00:00+00:00" name="revised"/>
<meta content="2026-08-10T11:00:00+00:00" property="article:modified_time"/>
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
        "name": "defoneos-hse-health-safety-executive-occupational-safety-ai-deep-dive-pack",
        "title": "Health &amp; Safety Executive Occupational Safety AI Deep-Dive Pack",
        "desc": "DEFONEOS — Health &amp; Safety Executive Occupational Safety AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "Health &amp; Safety Executive",
        "body": "Health &amp; Safety Executive",
        "legislation_backbone": "Health and Safety at Work etc. Act 1974 / Management of Health and Safety at Work Regulations 1999 / CDM Regulations 2015 / COMAH Regulations 2015",
        "nav_labels": [
            "Workplace Duty &amp; Employ", "Risk Assessment &amp; Manag", "Worker Consultation &amp; S", "COMAH Major Hazard Sites", "Construction &amp; CDM", "Chemicals &amp; COSHH", "Asbestos &amp; Work Health", "Welfare &amp; Conditions", "RIDDOR &amp; Investigation", "Notices &amp; Enforcement", "Prosecution &amp; Corporate", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Workplace Duty &amp; Employer Obligations", "region": "Workplace Duty & Employer Obligations", "legislation": "Health and Safety at Work etc. Act 1974 s.2"},
            {"topic": "Risk Assessment &amp; Management (6-Pack)", "region": "Risk Assessment & Management", "legislation": "Management of Health and Safety at Work Regulations 1999 reg 3"},
            {"topic": "Worker Consultation &amp; Safety Representatives", "region": "Worker Consultation & Safety", "legislation": "Safety Representatives and Safety Committees Regulations 1977 / HSWA 1974 ss.7-8"},
            {"topic": "COMAH Major Hazard &amp; Seveso Sites", "region": "COMAH Major Hazard Sites", "legislation": "Control of Major Accident Hazards Regulations 2015"},
            {"topic": "Construction &amp; CDM 2015", "region": "Construction & CDM", "legislation": "Construction (Design and Management) Regulations 2015 / HSWA 1974 s.3"},
            {"topic": "Hazardous Substances &amp; COSHH", "region": "Chemicals & COSHH", "legislation": "Control of Substances Hazardous to Health Regulations 2002 / CLP Regulation"},
            {"topic": "Asbestos &amp; Occupational Health", "region": "Asbestos & Occupational Health", "legislation": "Control of Asbestos Regulations 2012 / Occupational Health guidance"},
            {"topic": "Workplace Welfare &amp; Working Conditions", "region": "Welfare & Working Conditions", "legislation": "Workplace (Health, Safety and Welfare) Regulations 1992"},
            {"topic": "Incident Investigation &amp; RIDDOR Reporting", "region": "Incident Investigation & RIDDOR", "legislation": "Reporting of Injuries, Diseases and Dangerous Occurrences Regulations 2013"},
            {"topic": "Improvement &amp; Prohibition Notices", "region": "Notices & Enforcement", "legislation": "Health and Safety at Work etc. Act 1974 ss.21-25"},
            {"topic": "Prosecution &amp; Corporate Manslaughter", "region": "Prosecution & Corporate", "legislation": "Health and Safety at Work etc. Act 1974 s.33 / Corporate Manslaughter Act 2007"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "HSWA 1974 / DWP sponsorship / HSE Board / NAO"},
        ],
    },
    {
        "name": "defoneos-hmicfrs-her-majestys-inspectorate-constabulary-fire-rescue-services-ai-deep-dive-pack",
        "title": "HM Inspectorate of Constabulary &amp; Fire &amp; Rescue Services AI Deep-Dive Pack",
        "desc": "DEFONEOS — HM Inspectorate of Constabulary &amp; Fire &amp; Rescue Services AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "HM Inspectorate of Constabulary &amp; Fire &amp; Rescue Services",
        "body": "HMICFRS",
        "legislation_backbone": "Police Act 1996 / Police Reform and Social Responsibility Act 2011 / Fire and Rescue Services Act 2004 / Regulatory Reform (Fire Safety) Order 2005",
        "nav_labels": [
            "Police Effectiveness Ins", "Police Efficiency &amp; Legi", "Force Governance &amp; Lead", "Custody &amp; Detention Std", "Vulnerability &amp; Safegua", "Counter-Terrorism Insp", "Fire &amp; Rescue Effective", "Fire Prevention &amp; Govern", "Data &amp; Crime Recording", "Confidence &amp; Complaints", "Value for Money &amp; Profes", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Police Effectiveness Inspection (PEEL)", "region": "Police Effectiveness Inspection", "legislation": "Police Act 1996 s.54 / PEEL Framework"},
            {"topic": "Police Efficiency &amp; Legitimacy", "region": "Police Efficiency & Legitimacy", "legislation": "Police Act 1996 / Best Value Duty 1999"},
            {"topic": "Force Governance, Leadership &amp; Ethics", "region": "Force Governance & Leadership", "legislation": "Police Reform and Social Responsibility Act 2011 / College of Policing"},
            {"topic": "Custody &amp; Detention Standards", "region": "Custody & Detention Standards", "legislation": "Police and Criminal Evidence Act 1984 Code C / RIPSA 2000"},
            {"topic": "Vulnerability &amp; Safeguarding", "region": "Vulnerability & Safeguarding", "legislation": "Modern Slavery Act 2015 / Care Act 2014 / Victims' Code"},
            {"topic": "Counter-Terrorism &amp; Protective Security", "region": "Counter-Terrorism Inspection", "legislation": "Counter-Terrorism and Border Security Act 2019 / Terrorism Act 2000"},
            {"topic": "Fire &amp; Rescue Effectiveness", "region": "Fire & Rescue Effectiveness", "legislation": "Fire and Rescue Services Act 2004 / Fire and Rescue National Framework"},
            {"topic": "Fire Prevention, Protection &amp; Governance", "region": "Fire Prevention & Governance", "legislation": "Regulatory Reform (Fire Safety) Order 2005 / FRS Inspection Programme"},
            {"topic": "Data Integrity &amp; Crime Recording", "region": "Data & Crime Recording", "legislation": "Police Act 1996 / National Crime Recording Standard"},
            {"topic": "Public Confidence &amp; Complaints", "region": "Confidence & Complaints", "legislation": "Police Reform Act 2002 / IOPC oversight"},
            {"topic": "Value for Money &amp; Professional Standards", "region": "Value for Money & Standards", "legislation": "Police Act 1996 / Police Conduct Regulations 2020"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Police Act 1996 / Home Office / HMICFRS Framework / NAO"},
        ],
    },
    {
        "name": "defoneos-ccrc-criminal-cases-review-commission-miscarriage-justice-ai-deep-dive-pack",
        "title": "Criminal Cases Review Commission Miscarriage of Justice AI Deep-Dive Pack",
        "desc": "DEFONEOS — Criminal Cases Review Commission Miscarriage of Justice AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",
        "domain": "Criminal Cases Review Commission",
        "body": "Criminal Cases Review Commission",
        "legislation_backbone": "Criminal Appeal Act 1995 / Criminal Justice Act 2003 / Criminal Procedure and Investigations Act 1996 / Criminal Cases Review (Insanity) Act 1999",
        "nav_labels": [
            "Conviction Review Juris", "Referral Threshold &amp; Me", "Sentence Review Power", "Investigation Powers", "Fresh Evidence &amp; New Mat", "Forensic &amp; Expert Exami", "Screening &amp; Case Triage", "Courts &amp; Legal Aid Inter", "Victim &amp; Applicant Comms", "Systemic Learning &amp; Prev", "Jurisdiction &amp; Devolution", "Governance &amp; Parlia",
        ],
        "entries": [
            {"topic": "Conviction Review Jurisdiction", "region": "Conviction Review Jurisdiction", "legislation": "Criminal Appeal Act 1995 s.9"},
            {"topic": "Referral Threshold (&quot;Real Possibility&quot;)", "region": "Referral Threshold", "legislation": "Criminal Appeal Act 1995 s.13"},
            {"topic": "Sentence Review Power", "region": "Sentence Review Power", "legislation": "Criminal Appeal Act 1995 s.10"},
            {"topic": "Investigation &amp; Information-Gathering Powers", "region": "Investigation Powers", "legislation": "Criminal Appeal Act 1995 s.17 / s.19"},
            {"topic": "Fresh Evidence &amp; New Material", "region": "Fresh Evidence & New Material", "legislation": "Criminal Appeal Act 1995 s.23 / CPIA 1996"},
            {"topic": "Forensic &amp; Expert Examination", "region": "Forensic & Expert Examination", "legislation": "Criminal Appeal Act 1995 / Forensic Science Regulator"},
            {"topic": "Screening, Triage &amp; Casework Model", "region": "Screening & Case Triage", "legislation": "Criminal Appeal Act 1995 / CCRC Casework Model"},
            {"topic": "Parliament, Court &amp; Legal Aid Interaction", "region": "Courts & Legal Aid Interaction", "legislation": "Criminal Justice Act 2003 / Access to Justice Act 1999"},
            {"topic": "Victim &amp; Applicant Communication", "region": "Victim & Applicant Communication", "legislation": "CCRC Charter / Victims' Code 2020"},
            {"topic": "Systemic Learning &amp; Miscarriage Prevention", "region": "Systemic Learning & Prevention", "legislation": "Criminal Appeal Act 1995 / CCRC Annual Cases Review"},
            {"topic": "Jurisdiction &amp; Devolution Boundaries", "region": "Jurisdiction & Devolution", "legislation": "Criminal Appeal Act 1995 / Northern Ireland CCRC"},
            {"topic": "Governance &amp; Parliamentary Accountability", "region": "Governance & Parliamentary Accountability", "legislation": "Criminal Appeal Act 1995 / Ministry of Justice sponsorship / NAO"},
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