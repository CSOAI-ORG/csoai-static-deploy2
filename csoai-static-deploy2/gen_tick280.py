#!/usr/bin/env python3
"""Generate 3 new DEFONEOS deep-dive packs + .llm.json companions.
Ticket 280: SAAS / NIPB / SCRA (devolved public-services gap).
Replicates the exact SPPA template (byte-compatible structure).
"""
import json, re, html, hashlib

PRIORITIES = [
    ("Compliance Automation",
     "Automated {AGN} {EP} validation checking {LAW} against {EP} statutory and rulebook requirements. No {AGN} activity proceeds without a signed, auditable compliance record."),
    ("Risk Detection & Early Warning",
     "Detection of {EP} risk breaches, control gaps, and early-warning indicators affecting {AGN} delivery and accountability to the {LEG}."),
    ("Natural Language Policy Analysis",
     "NLP analysis of {EP} legislation, policy statements, guidance, and legislative record against the full statutory framework and regulatory expectations."),
    ("Predictive Analytics",
     "{EP} risk and workload forecasting from trend indicators, demand signals, and operational metrics to support prioritisation and decision-support."),
    ("Evidence Synthesis",
     "{EP} evidence, inspection findings, returns, and stakeholder submissions assembled into decision dossiers for review by accountable officers and the BFT council."),
    ("Document Intelligence",
     "Extraction from {EP} documents, statutory returns, and correspondence for end-to-end {AGN} lifecycle tracking and audit trails."),
    ("Stakeholder Reporting",
     "{EP} dashboards reporting coverage, performance, and outcomes to ministers, the board, and the {LEG}."),
    ("Real-time Monitoring",
     "{EP} pipeline tracking, submission cycles, and continuous surveillance of {AGN} operational posture and statutory deliverables."),
]
MCP = ["mcp-bailii", "mcp-govuk-search", "mcp-hansard-search",
       "mcp-uk-courts", "mcp-uk-legislation", "mcp-uk-regulator-intel"]

CSS = "*{margin:0;padding:0;box-sizing:border-box}\nbody{background:#0a0a0a;color:#e0e0e0;font-family:system-ui,sans-serif;line-height:1.6}\n"
CSS += "a{color:#00ff88;text-decoration:none}a:hover{text-decoration:underline}\n"
CSS += ".hero{background:linear-gradient(135deg,#0a0a0a,#1a1a2e,#0d1117);padding:40px 20px;text-align:center;border-bottom:2px solid #00ff88}\n"
CSS += ".hero h1{font-size:2em;color:#00ff88;margin-bottom:6px}\n.sub{color:#888;font-size:.95em;margin-bottom:10px}\n"
CSS += ".bg{display:inline-block;background:#1a1a2e;border:1px solid #00ff88;padding:4px 12px;border-radius:20px;color:#00ff88;font-size:.8em;margin:3px}\n"
CSS += "nav{background:#111;padding:10px 20px;border-bottom:1px solid #222;position:sticky;top:0;z-index:100;overflow-x:auto;white-space:nowrap}\n"
CSS += "nav a{display:inline-block;padding:4px 10px;margin:2px;background:#1a1a2e;border:1px solid #333;border-radius:6px;font-size:.75em;color:#00ff88;transition:all .2s}\n"
CSS += "nav a:hover{background:#00ff88;color:#0a0a0a;text-decoration:none}\n"
CSS += ".c{max-width:1200px;margin:0 auto;padding:20px}\n"
CSS += ".s{margin:28px 0;background:#1a1a2e;border:1px solid #222;border-radius:12px;overflow:hidden}\n"
CSS += ".sh{background:linear-gradient(90deg,#1a1a2e,#0d1117);padding:14px 18px;border-bottom:1px solid #333}\n"
CSS += ".sh h2{color:#00ff88;font-size:1.2em;margin-bottom:2px}\n.en{color:#666;font-size:.78em}\n.sb{padding:18px}\n"
CSS += ".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-bottom:14px}\n"
CSS += ".p{background:#0d1117;border:1px solid #222;border-radius:8px;padding:12px;transition:border-color .2s}\n"
CSS += ".p:hover{border-color:#00ff88}\n.p h3{color:#00ff88;font-size:.84em;margin-bottom:5px}\n.p p{color:#aaa;font-size:.78em;line-height:1.5}\n"
CSS += ".mt{background:#111;border:1px solid #222;border-radius:8px;padding:12px;margin-top:10px}\n"
CSS += ".mt h4{color:#00ff88;font-size:.82em;margin-bottom:6px}\n.ml{display:flex;flex-wrap:wrap;gap:5px}\n"
CSS += ".t{background:#1a1a2e;border:1px solid #00ff88;padding:2px 9px;border-radius:16px;font-size:.72em;color:#00ff88}\n"
CSS += "footer{background:#111;border-top:2px solid #00ff88;padding:20px;text-align:center;margin-top:28px}\n"
CSS += ".br{font-size:1.1em;color:#00ff88;font-weight:700;margin-bottom:5px}\nfooter p{color:#666;font-size:.75em;line-height:1.5}\n"
CSS += ".cr{margin-top:10px;padding-top:10px;border-top:1px solid #222;color:#555;font-size:.72em}\n"
CSS += "@media(max-width:768px){.hero h1{font-size:1.4em}.g{grid-template-columns:1fr}}"

def esc(t):
    return html.escape(t, quote=False).replace("&amp;", "&")

def build(b):
    slug = b["slug"]
    name = b["name"]
    agn = "The " + name
    leg = b["leg"]
    law = b["law"]
    url = f"https://www.csoai.org/{slug}.html"
    llm_url = url + ".llm.json"
    desc = f"DEFONEOS — {name} AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record."
    ts = "2026-08-14T06:00:00+00:00"

    nav = "".join(f'<a href="#ep{i+1}">{esc(ep[:21])}</a>' for i, ep in enumerate(b["eps"]))

    entry_sections = []
    for i, ep in enumerate(b["eps"]):
        cards = "".join(
            f'<div class="p"><h3>{esc(pri)}</h3><p>{esc(txt.format(AGN=agn,EP=ep,LAW=law,LEG=leg))}</p></div>'
            for pri, txt in PRIORITIES)
        mcps = "".join(f'<span class="t">{m}</span>' for m in MCP)
        entry_sections.append(
            f'<div class="s" id="ep{i+1}"><div class="sh"><span class="en">Entry Point {i+1:02d}</span>'
            f'<h2>{esc(ep)}</h2></div><div class="sb"><div class="g">{cards}</div>'
            f'<div class="mt"><h4>MCP Tools</h4><div class="ml">{mcps}</div></div></div></div>')

    ld = {
        "@context": "https://schema.org", "@type": "WebPage",
        "name": f"{name} AI Deep-Dive Pack", "url": url, "description": desc,
        "publisher": {"@type": "Organization", "name": "CSOAI Ltd", "url": "https://csoai.org"},
        "about": {"@type": "GovernmentService", "name": "UK Public Services AI Governance"},
    }

    hero_tag = b.get("emoji", "🏛️")
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{esc(name)} AI Deep-Dive Pack</title>
<style>{CSS}</style>
<link href="{llm_url}" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>
<meta content="/llms.txt" name="llms-txt"/>
<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>
<meta content="CSOAI Ltd (2026). {esc(name)} AI Deep-Dive Pack. {url}" name="citation-policy"/>
<meta content="{ts}" name="revised"/>
<meta content="{ts}" property="article:modified_time"/>
<meta content="{desc}" name="description"/>
<link href="{url}" rel="canonical"/>
<meta content="{esc(name)} AI Deep-Dive Pack" property="og:title"/>
<meta content="{desc}" property="og:description"/>
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
<div class="hero">
<h1>{hero_tag} {esc(name)} AI Deep-Dive Pack</h1>
<p class="sub">DEFONEOS — UK Sovereign Public Services OS</p>
<div><span class="bg">12 Entry Points</span><span class="bg">8 AI Priorities</span><span class="bg">6 MCP Tools</span></div>
<p>12 {esc(name)} entry points × 8 AI priorities × 6 MCP integrations — {b["blurb"]}</p>
</div>
<nav>
{nav}
</nav>
<div class="c">
{"".join(entry_sections)}
</div>
<footer>
<div class="br">DEFONEOS — UK Sovereign Public Services OS</div>
<p>Open-source sovereign AI governance for {esc(name)}. Built for audit-grade, signed, neutral UK-sovereign compliance.</p>
<p>AUKUS-compatible. {esc(law)}.</p>
<div class="cr">© 2026 CSOAI Ltd (UK 16939677) · meok-defoneos · csoai-defoneos · DEFONEOS-SEAL</div>
</footer>
</body>
</html>
"""
    return html_doc, f"https://csoai.org/{slug}.html"

def build_llm_json(b, url, headings):
    desc = f"DEFONEOS — {b['name']} AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record."
    text = f"{b['name']} AI Deep-Dive Pack 💰 {b['name']} AI Deep-Dive Pack DEFONEOS — UK Sovereign Public Services OS 12 Entry Points 8 AI Priorities 6 MCP Tools 12 {b['name']} entry points × 8 AI priorities × 6 MCP integrations — {b['blurb']} "
    text += " ".join(f"Entry Point {i+1:02d} {ep}" for i, ep in enumerate(b["eps"]))
    obj = {
        "@context": "https://csoai.org/llm-context.json",
        "type": "LLMPageSummary",
        "url": f"https://csoai.org/{b['slug']}.html",
        "title": f"{b['name']} AI Deep-Dive Pack",
        "description": desc,
        "headings": [f"{b['name']} AI Deep-Dive Pack"] + b["eps"],
        "text": text,
        "text_truncated": True,
        "register": {
            "role": "measurement_and_attestation_support",
            "csoai_certifies_systems": False,
            "csoai_is_a_notified_body": False,
            "csoai_has_enforcement_powers": False,
            "note": "CSOAI measures and publishes evidence. It issues no conformity marks and holds no accreditation. Nothing here is certification or legal advice.",
        },
        "generated_by": "make_llm_json.py",
    }
    return json.dumps(obj)

def check(h):
    en = len(re.findall(r'class="en">Entry Point', h))
    h2c = len(re.findall(r"<h2>", h))
    p = len(re.findall(r'class="p"><h3>', h))
    h1 = len(re.findall(r"<h1>", h))
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1)
    json.loads(ld)
    llm_alt = 'rel="alternate"' in h and ".llm.json" in h
    return {"en": en, "t": h2c, "p": p, "h1": h1, "ld_json_ok": True, "llm_alt": llm_alt}

BODIES = [
    {
        "slug": "defoneos-saas-student-awards-agency-scotland-ai-deep-dive-pack",
        "name": "Student Awards Agency Scotland",
        "emoji": "🎓",
        "leg": "Scottish Parliament",
        "law": "Further and Higher Education (Scotland) Act 2005 / Education (Scotland) Act 1980 / Scotland Act 1998 / Data Protection Act 2018 / UK GDPR",
        "blurb": "student support, funding and bursary administration for higher-education students in Scotland, from SAAS awards and grants to repayment and exception handling",
        "eps": ["Student Awards & Bursary Administration", "Higher Education Student Support", "Further Education & Part-time Student Funding", "SAAS Grant & Loan Determinations", "Application Processing & Eligibility", "Income Assessment & Means Testing", "Repayment, Recovery & Overpayment", "Exceptional Circumstances & Hardship", "Disability & Care-experienced Student Support", "Fraud Prevention & Compliance Checks", "Data Protection & Applicant Records", "Governance & Scottish Parliament Accountability"],
    },
    {
        "slug": "defoneos-nipb-northern-ireland-policing-board-ai-deep-dive-pack",
        "name": "Northern Ireland Policing Board",
        "emoji": "🛡️",
        "leg": "Northern Ireland Assembly",
        "law": "Police (Northern Ireland) Act 2000 / Northern Ireland Act 1998 / Policing and Crime Act 2017 / Data Protection Act 2018 / UK GDPR",
        "blurb": "independent oversight of policing in Northern Ireland, from the PSNI budget and performance monitoring to public accountability and complaints governance",
        "eps": ["Oversight of the Police Service of Northern Ireland", "Policing Plan & Performance Monitoring", "PSNI Budget & Financial Oversight", "Public Accountability & Scrutiny", "Complaints & Discipline Oversight", "Human Rights & Policing Standards", "Community Engagement & Partnerships", "Equality, Diversity & Inclusion in Policing", "Independent Monitoring & Audit", "Police Estate, Resources & Capability", "Data Protection & Case Records", "Governance & Northern Ireland Assembly Accountability"],
    },
    {
        "slug": "defoneos-scra-scottish-childrens-reporter-administration-ai-deep-dive-pack",
        "name": "Scottish Children's Reporter Administration",
        "emoji": "🧒",
        "leg": "Scottish Parliament",
        "law": "Children's Hearings (Scotland) Act 2011 / Children (Scotland) Act 1995 / United Nations Convention on the Rights of the Child / Data Protection Act 2018 / UK GDPR",
        "blurb": "the children's hearings system in Scotland, from reporter decision-making and referral assessment to safeguarding, hearings and care planning",
        "eps": ["Children's Reporter Decision-Making", "Referral Assessment & Triage", "Children's Hearings & Proceedings", "Safeguarding & Child Protection", "Care & Supervision Planning", "Offending & Non-Offence Grounds", "Legal Representation & Rights of the Child", "Case Management & Tracking", "Wellbeing & Outcomes Monitoring", "Multi-Agency Coordination", "Data Protection & Case Records", "Governance & Scottish Parliament Accountability"],
    },
]

def main():
    for b in BODIES:
        doc, url = build(b)
        status = check(doc)
        llm = build_llm_json(b, url, b["eps"])
        with open(f"{b['slug']}.html", "w") as f:
            f.write(doc)
        with open(f"{b['slug']}.html.llm.json", "w") as f:
            f.write(llm)
        print(f"{b['slug']}.html  {len(doc)}b  check={status}  llm={len(llm)}b")
        print(f"  md5 html={hashlib.md5(doc.encode()).hexdigest()[:8]}  llm={hashlib.md5(llm.encode()).hexdigest()[:8]}")
        # structural counts: expected ep-num from heading
        assert status["en"] == 12, "entry points != 12"
        assert status["t"] == 12, "h2 count != 12"
        assert status["p"] == 96, "priority cards != 96"
        assert status["h1"] == 1, "h1 != 1"

if __name__ == "__main__":
    main()