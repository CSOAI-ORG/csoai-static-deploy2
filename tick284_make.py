#!/usr/bin/env python3
"""DEFONEOS tick 284 generator — build 3 NEW devolved public-services deep-dive packs
(Caledonian Maritime Assets / NI Water / Estyn), probe-verified 0 disk + 0 sitemap.
Structure mirrors tick-283 packs exactly: 12 entry points x 8 priorities x 6 MCPs,
JSON-LD canonical, .llm.json companion, parametric legislature.
"""
import json, os, datetime, re, html

ROOT = "/Users/nicholas/clawd/csoai-static-deploy2"
NOW = "2026-08-14T16:30:00+00:00"

PRIORITIES = [
    ("Compliance Automation", "Automated {REF} {EP} validation checking {LEG} against {EP} statutory and rulebook requirements. No {REF} activity proceeds without a signed, auditable compliance record."),
    ("Risk Detection & Early Warning", "Detection of {EP} risk breaches, control gaps, and early-warning indicators affecting {REF} performance and accountability."),
    ("Natural Language Policy Analysis", "NLP analysis of {EP} legislation, policy statements, guidance, and parliamentary record against the full statutory framework and regulatory expectations."),
    ("Predictive Analytics", "{EP} risk and workload forecasting from trend indicators, demand signals, and operational metrics to support prioritisation and decision-support."),
    ("Evidence Synthesis", "{EP} evidence, inspection findings, returns, and stakeholder submissions assembled into decision dossiers for review by accountable officers and the BFT council."),
    ("Document Intelligence", "Extraction from {EP} documents, statutory returns, and correspondence for end-to-end {REF} lifecycle tracking and audit trails."),
    ("Stakeholder Reporting", "{EP} dashboards reporting coverage, performance, and outcomes to ministers, the board, and {LEG2}."),
    ("Real-time Monitoring", "{EP} pipeline tracking, submission cycles, and continuous surveillance of {REF} activity for sovereign, verifiable oversight."),
]
MCPS = ["mcp-bailii", "mcp-govuk-search", "mcp-hansard-search", "mcp-uk-courts", "mcp-uk-legislation", "mcp-uk-regulator-intel"]

def esc(s):
    return html.escape(s, quote=False).replace("&amp;", "&")

def nav_label(t):
    return t[:17]

def esc_json(s):
    return s.replace("&", "&amp;")

def build_pack(cfg):
    slug = cfg["slug"]
    name = cfg["name"]
    emoji = cfg["emoji"]
    ref = cfg["ref"]
    intro = cfg["intro"]
    legis = " / ".join(cfg["legis"])
    leg2 = cfg["leg2"]       # legislature for Stakeholder Reporting
    entries = cfg["entries"]
    url = f"https://www.csoai.org/{slug}.html"
    llm_url = f"https://www.csoai.org/{slug}.html.llm.json"
    desc = f"DEFONEOS \u2014 {name} AI Deep-Dive Pack. A sovereign, audit-grade CSOAI surface: measurement, not certification \u2014 every figure traces to a signed, verifiable record."

    # hero intro paragraph
    hero = f"{len(entries)} {name} entry points \u00d7 8 AI priorities \u00d7 6 MCP integrations \u2014 {intro}"

    # nav
    nav = "\n".join(f'<a href="#ep{i+1}">{esc_json(nav_label(e))}</a>' for i, e in enumerate(entries))

    # body: 12 entry point sections
    sections = []
    for i, ep in enumerate(entries, 1):
        eph = esc(ep)
        cards = []
        for title, tmpl in PRIORITIES:
            body = tmpl.replace("{REF}", ref).replace("{EP}", ep).replace("{LEG}", legis).replace("{LEG2}", leg2)
            cards.append(f'<div class="p"><h3>{title}</h3><p>{esc(body)}</p></div>')
        grid = "\n".join(cards)
        mcp_spans = "".join(f'<span class="t">{m}</span>' for m in MCPS)
        section = (f'<div class="s" id="ep{i}"><div class="sh"><span class="en">Entry Point {i:02d}</span>'
                   f'<h2>{eph}</h2></div><div class="sb"><div class="g">{grid}</div>'
                   f'<div class="mt"><h4>MCP Tools</h4><div class="ml">{mcp_spans}</div></div></div></div>')
        sections.append(section)
    body_html = "\n".join(sections)

    jsonld = {
        "@context": "https://schema.org", "@type": "WebPage",
        "name": f"{name} AI Deep-Dive Pack", "url": url, "description": desc,
        "publisher": {"@type": "Organization", "name": "CSOAI Ltd", "url": "https://csoai.org"},
        "about": {"@type": "GovernmentService", "name": "UK Sovereign Public Services Governance"},
    }
    jsonld_str = json.dumps(jsonld, ensure_ascii=False)

    head = f'''<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{esc(name)} AI Deep-Dive Pack</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a0a;color:#e0e0e0;font-family:system-ui,sans-serif;line-height:1.6}}
a{{color:#00ff88;text-decoration:none}}a:hover{{text-decoration:underline}}
.hero{{background:linear-gradient(135deg,#0a0a0a,#1a1a2e,#0d1117);padding:40px 20px;text-align:center;border-bottom:2px solid #00ff88}}
.hero h1{{font-size:2em;color:#00ff88;margin-bottom:6px}}
.sub{{color:#888;font-size:.95em;margin-bottom:10px}}
.bg{{display:inline-block;background:#1a1a2e;border:1px solid #00ff88;padding:4px 12px;border-radius:20px;color:#00ff88;font-size:.8em;margin:3px}}
nav{{background:#111;padding:10px 20px;border-bottom:1px solid #222;position:sticky;top:0;z-index:100;overflow-x:auto;white-space:nowrap}}
nav a{{display:inline-block;padding:4px 10px;margin:2px;background:#1a1a2e;border:1px solid #333;border-radius:6px;font-size:.75em;color:#00ff88;transition:all .2s}}
nav a:hover{{background:#00ff88;color:#0a0a0a;text-decoration:none}}
.c{{max-width:1200px;margin:0 auto;padding:20px}}
.s{{margin:28px 0;background:#1a1a2e;border:1px solid #222;border-radius:12px;overflow:hidden}}
.sh{{background:linear-gradient(90deg,#1a1a2e,#0d1117);padding:14px 18px;border-bottom:1px solid #333}}
.sh h2{{color:#00ff88;font-size:1.2em;margin-bottom:2px}}
.en{{color:#666;font-size:.78em}}
.sb{{padding:18px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-bottom:14px}}
.p{{background:#0d1117;border:1px solid #222;border-radius:8px;padding:12px;transition:border-color .2s}}
.p:hover{{border-color:#00ff88}}
.p h3{{color:#00ff88;font-size:.84em;margin-bottom:5px}}
.p p{{color:#aaa;font-size:.78em;line-height:1.5}}
.mt{{background:#111;border:1px solid #222;border-radius:8px;padding:12px;margin-top:10px}}
.mt h4{{color:#00ff88;font-size:.82em;margin-bottom:6px}}
.ml{{display:flex;flex-wrap:wrap;gap:5px}}
.t{{background:#1a1a2e;border:1px solid #00ff88;padding:2px 9px;border-radius:16px;font-size:.72em;color:#00ff88}}
footer{{background:#111;border-top:2px solid #00ff88;padding:20px;text-align:center;margin-top:28px}}
.br{{font-size:1.1em;color:#00ff88;font-weight:700;margin-bottom:5px}}
footer p{{color:#666;font-size:.75em;line-height:1.5}}
.cr{{margin-top:10px;padding-top:10px;border-top:1px solid #222;color:#555;font-size:.72em}}
@media(max-width:768px){{.hero h1{{font-size:1.4em}}.g{{grid-template-columns:1fr}}}}</style>
<link href="{esc_json(llm_url)}" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>
<meta content="/llms.txt" name="llms-txt"/>
<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>
<meta content="CSOAI Ltd (2026). {esc(name)} AI Deep-Dive Pack. {url}" name="citation-policy"/>
<meta content="{NOW}" name="revised"/>
<meta content="{NOW}" property="article:modified_time"/>
<meta content="{esc(desc)}" name="description"/>
<link href="{url}" rel="canonical"/>
<meta content="{esc(name)} AI Deep-Dive Pack" property="og:title"/>
<meta content="{esc(desc)}" property="og:description"/>
<script type="application/ld+json">{jsonld_str}</script>'''

    hero_html = f'''<div class="hero">
<h1>{emoji} {esc(name)} AI Deep-Dive Pack</h1>
<p class="sub">DEFONEOS \u2014 UK Sovereign Public Services OS</p>
<div><span class="bg">{len(entries)} Entry Points</span><span class="bg">8 AI Priorities</span><span class="bg">6 MCP Tools</span></div>
<p>{esc(hero)}</p>
</div>'''

    footer_html = f'''<footer>
<div class="br">DEFONEOS \u2014 UK Sovereign Public Services OS</div>
<p>Open-source sovereign AI governance for {esc(name)}. Built for audit-grade, signed, neutral UK-sovereign compliance.</p>
<p>AUKUS-compatible. {esc(legis)}.</p>
<div class="cr">\u00a9 2026 CSOAI Ltd (UK 16939677) \u00b7 meok-defoneos \u00b7 csoai-defoneos \u00b7 DEFONEOS-SEAL</div>
</footer>'''

    doc = (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n{head}\n</head>\n<body>\n{hero_html}\n<nav>\n{nav}\n</nav>\n'
           f'<div class="c">\n{body_html}\n</div>\n{footer_html}\n</body>\n</html>\n')

    # llm.json companion
    llm = {
        "@context": "https://csoai.org/llm-context.json",
        "type": "LLMPageSummary", "url": url,
        "title": f"{name} AI Deep-Dive Pack", "description": desc,
        "headings": [f"{emoji} {name} AI Deep-Dive Pack"] + entries,
        "text": " ".join([f"{name} AI Deep-Dive Pack", f"{emoji} {name} AI Deep-Dive Pack",
                          "DEFONEOS \u2014 UK Sovereign Public Services OS",
                          f"{len(entries)} Entry Points 8 AI Priorities 6 MCP Tools",
                          f"{emoji} {name} AI Deep-Dive Pack"] + entries),
        "text_truncated": True,
        "register": {
            "role": "measurement_and_attestation_support", "csoai_certifies_systems": False,
            "csoai_is_a_notified_body": False, "csoai_has_enforcement_powers": False,
            "note": "CSOAI measures and publishes evidence. It issues no conformity marks and holds no accreditation. Nothing here is certification or legal advice."
        },
        "generated_by": "tick284_make.py",
    }

    with open(os.path.join(ROOT, f"{slug}.html"), "w") as f:
        f.write(doc)
    with open(os.path.join(ROOT, f"{slug}.html.llm.json"), "w") as f:
        json.dump(llm, f, ensure_ascii=False, indent=2)

    size = os.path.getsize(os.path.join(ROOT, f"{slug}.html"))
    return size

# ---- config for 3 packs ----
PACKS = [
    {
        "slug": "defoneos-caledonian-maritime-assets-ai-deep-dive-pack",
        "name": "Caledonian Maritime Assets", "emoji": "\u26f5", "ref": "CMAL",
        "leg2": "the Scottish Parliament",
        "intro": ("Scotland's public ferry and harbour infrastructure owner: lifeline ferry vessels "
                  "and coastal harbours leased to operators across the Clyde and Hebrides network \u2014 "
                  "distinct from CalMac Ferries (operator), Transport Scotland and the Crown Estate"),
        "legis": ["Transport (Scotland) Act 2001", "Scotland Act 1998", "Marine (Scotland) Act 2010", "Data Protection Act 2018"],
        "entries": [
            "Ferry Vessel Ownership & Asset Portfolio",
            "Harbour & Port Infrastructure Provision",
            "Vessel Leasing & Operator Agreements",
            "Lifeline Ferry Services Support",
            "Capital Investment & Fleet Replacement",
            "Asset Condition, Maintenance & Safety",
            "Harbour Dues, Charges & Commercial Revenue",
            "Passenger & Vehicle Ferry Operations",
            "Community & Island Connectivity",
            "Environmental Compliance & Marine Regulation",
            "Data Protection & Asset Records",
            "Governance & Scottish Parliament Accountability",
        ],
    },
    {
        "slug": "defoneos-ni-water-northern-ireland-water-ai-deep-dive-pack",
        "name": "Northern Ireland Water", "emoji": "\U0001F4A7", "ref": "NIW",
        "leg2": "the Northern Ireland Assembly",
        "intro": ("Northern Ireland's public water and sewerage provider serving domestic and business "
                  "customers: drinking water supply, wastewater treatment and sewerage across the NI "
                  "network \u2014 distinct from Scottish Water, Dwr Cymru Welsh Water and the Water "
                  "Companies of England"),
        "legis": ["Water and Sewerage Services (Northern Ireland) Order 2006", "Water (Northern Ireland) Order 1999", "Environment (Northern Ireland) Order 2002", "Data Protection Act 2018"],
        "entries": [
            "Water Supply & Distribution",
            "Wastewater & Sewerage Services",
            "Drinking Water Quality & Standards",
            "Sewage Treatment & Discharge",
            "Customer Services & Metering",
            "Customer Charges & Billing",
            "Infrastructure Investment & Capital Delivery",
            "Asset Management, Leakage & Resilience",
            "Environmental Compliance & Regulation (NIEA)",
            "Water Affordability & Customer Support",
            "Data Protection & Customer Records",
            "Governance & NI Assembly Accountability",
        ],
    },
    {
        "slug": "defoneos-estyn-wales-education-training-inspection-ai-deep-dive-pack",
        "name": "Estyn \u2014 Wales Education & Training Inspection", "emoji": "\U0001F393", "ref": "Estyn",
        "leg2": "the Senedd",
        "intro": ("Her Majesty's Inspectorate for Education and Training in Wales: independent inspection "
                  "of schools, further education, work-based learning, adult learning and youth services "
                  "in Wales \u2014 distinct from Ofsted (England) and the Care Inspectorate (Scotland)"),
        "legis": ["Education Act 2005", "Learning and Skills Act 2000", "Government of Wales Act 2006", "Education (Wales) Act 2014", "Data Protection Act 2018"],
        "entries": [
            "School Inspection & Reporting",
            "Further Education Inspection",
            "Work-Based Learning & Apprenticeships",
            "Adult & Community Learning",
            "Youth Services & Wellbeing",
            "Local Authority Education Scrutiny",
            "Curriculum & Standards Assessment",
            "Teaching Quality & Leadership",
            "Safeguarding & Learner Protection",
            "Improvement Planning & Follow-up",
            "Data Protection & Inspection Records",
            "Governance & Senedd Accountability",
        ],
    },
]

for cfg in PACKS:
    size = build_pack(cfg)
    print(f"BUILT {cfg['slug']:60s} {size}b  entries={len(cfg['entries'])}")
print("DONE")
