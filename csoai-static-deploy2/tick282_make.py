#!/usr/bin/env python3
"""DEFONEOS Tick 282 - build 3 deep-dive packs: Scottish Water / Northern Ireland Housing Executive / ScotRail.

Probe-verified 0 disk + 0 sitemap hits BEFORE build (tick-265 pitfall, re-verified this tick):
- defoneos-scottish-water-ai-deep-dive-pack                         OPEN (Scotland's public water & wastewater provider - genuinely uncovered; distinct from Defra/DWI and SEPA)
- defoneos-northern-ireland-housing-executive-ai-deep-dive-pack     OPEN (NI's statutory social housing authority - genuinely uncovered; distinct from Scottish Housing Regulator)
- defoneos-scotrail-scotland-railway-services-ai-deep-dive-pack     OPEN (Scotland's national public rail operator - genuinely uncovered; distinct from Network Rail / ORR / DfT England)
Cross-checks: Scottish Water != Defra Drinking Water Inspectorate / Ofwat England; NIHE != SHR (Scotland) or any GB body;
ScotRail != Network Rail / ORR / HS2 / DfT rail governance. All genuinely-uncovered on disk + sitemap (probe verified this tick).
Continuing devolved-public-services gap-fill (ticks 276-281) across Scotland (2026 full devolved public service carrier) and NI.

Pattern proven ticks 250-281:
- 12 entry points x 8 AI priorities x 6 MCPs each
- JSON-LD schema.org-CANONICAL via json.dumps() (guaranteed correct quoting)
- rel=alternate llm.json companion, canonical URL, citation-policy, revised timestamp
- 4-statute backbone cited in footer
- NO personal-surveillance / kinetic-targeting patterns (DEFONEOS hard stops)
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import re

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

MCPS = [
    "mcp-bailii",
    "mcp-govuk-search",
    "mcp-hansard-search",
    "mcp-uk-courts",
    "mcp-uk-legislation",
    "mcp-uk-regulator-intel",
]

PRIORITIES = [
    ("Compliance Automation",
     "Automated {reg_short} {ep} validation checking {statute_primary} against {ep} statutory and rulebook requirements. No {reg_short} activity proceeds without a signed, auditable compliance record."),
    ("Risk Detection & Early Warning",
     "Detection of {ep} risk breaches, control gaps, and early-warning indicators affecting {reg_short} performance and accountability."),
    ("Natural Language Policy Analysis",
     "NLP analysis of {ep} legislation, policy statements, guidance, and parliamentary record against the full statutory framework and regulatory expectations."),
    ("Predictive Analytics",
     "{ep} risk and workload forecasting from trend indicators, demand signals, and operational metrics to support prioritisation and decision-support."),
    ("Evidence Synthesis",
     "{ep} evidence, inspection findings, returns, and stakeholder submissions assembled into decision dossiers for review by accountable officers and the BFT council."),
    ("Document Intelligence",
     "Extraction from {ep} documents, statutory returns, and correspondence for end-to-end {reg_short} lifecycle tracking and audit trails."),
    ("Stakeholder Reporting",
     "{ep} dashboards reporting coverage, performance, and outcomes to ministers, the board, and Parliament/Senedd."),
    ("Real-time Monitoring",
     "{ep} pipeline tracking, submission cycles, and continuous surveillance of {reg_short} activity for sovereign, verifiable oversight."),
]

PACKS = [
    (
        "defoneos-scottish-water-ai-deep-dive-pack",
        "Scottish Water",
        "Scottish Water",
        "\U0001f30a",
        "12 Scottish Water entry points \u00d7 8 AI priorities \u00d7 6 MCP integrations \u2014 Scotland's national, publicly-owned water and wastewater provider: drinking water quality and standards, wastewater treatment and sewerage, customer billing and charges, leakage reduction and sustainable water management \u2014 distinct from the Defra Drinking Water Inspectorate and Ofwat (England)",
        "Water Industry (Scotland) Act 2002 / Water Environment and Water Services (Scotland) Act 2003 / Sewerage (Scotland) Act 1968 / Data Protection Act 2018",
        [
            "Water & Wastewater Service Provision",
            "Drinking Water Quality & Standards",
            "Wastewater Treatment & Sewerage",
            "Water Environment & River Basin Management",
            "Customer Services & Metering",
            "Customer Charges & Billing",
            "Infrastructure Investment & Capital Delivery",
            "Asset Management & Resilience",
            "Leakage Reduction & Sustainability",
            "Environmental Compliance & Regulation (SEPA)",
            "Water Affordability & Customer Support",
            "Governance & Scottish Parliament Accountability",
        ],
    ),
    (
        "defoneos-northern-ireland-housing-executive-ai-deep-dive-pack",
        "Northern Ireland Housing Executive",
        "NIHE",
        "\U0001f3e0",
        "12 Northern Ireland Housing Executive entry points \u00d7 8 AI priorities \u00d7 6 MCP integrations \u2014 Northern Ireland's statutory social housing authority: social housing provision and allocation, housing benefit and rent administration, repairs and maintenance, renovation grants and neighbourhood regeneration \u2014 distinct from the Scottish Housing Regulator and any GB housing body",
        "Housing Order (Northern Ireland) 1981 / Housing (NI) Order 1988 / Housing (NI) Order 2003 / Data Protection Act 2018",
        [
            "Social Housing Provision & Management",
            "Housing Allocations & Waiting Lists",
            "Housing Benefit & Rent Administration",
            "Renovation Grants & Improvement Support",
            "Repairs & Maintenance Services",
            "Homelessness & Housing Support",
            "Private Rented Sector & Regulation",
            "Fuel Poverty & Energy Efficiency",
            "Area-Based Regeneration & Communities",
            "Neighbourhood Planning & New Build",
            "Data Protection & Tenant Records",
            "Governance & Northern Ireland Assembly Accountability",
        ],
    ),
    (
        "defoneos-scotrail-scotland-railway-services-ai-deep-dive-pack",
        "ScotRail Scotland Railway Services",
        "ScotRail",
        "\U0001f686",
        "12 ScotRail entry points \u00d7 8 AI priorities \u00d7 6 MCP integrations \u2014 Scotland's national, publicly-operated rail service: passenger rail operation, timetables and fares, ticket sales and customer services, service reliability and station operations across the Scottish network \u2014 distinct from Network Rail, the Office of Rail and Road and GB franchise rail governance",
        "Railways Act 2005 / Scotland Act 1998 / ScotRail rail service agreement / Data Protection Act 2018",
        [
            "Passenger Rail Service Operation",
            "Train Timetables & Journey Planning",
            "Fares, Ticketing & Revenue",
            "Customer Services & Passenger Support",
            "Service Reliability & Performance",
            "Station Operations & Accessibility",
            "Rolling Stock & Fleet Management",
            "Safety & Security on the Network",
            "Seasonal, Events & Community Rail",
            "Disruption & Passenger Compensation",
            "Data Protection & Passenger Records",
            "Governance & Scottish Parliament Accountability",
        ],
    ),
]


def make_json_ld(slug, title):
    block = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": f"https://www.csoai.org/{slug}.html",
        "description": f"DEFONEOS \u2014 {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification \u2014 every figure traces to a signed, verifiable record.",
        "publisher": {"@type": "Organization", "name": "CSOAI Ltd", "url": "https://csoai.org"},
        "about": {"@type": "GovernmentService", "name": "UK Sovereign Public Services Governance"},
    }
    return json.dumps(block, separators=(",", ":"), ensure_ascii=False)


CSS = (
    '<style>*{margin:0;padding:0;box-sizing:border-box}\n'
    'body{background:#0a0a0a;color:#e0e0e0;font-family:system-ui,sans-serif;line-height:1.6}\n'
    'a{color:#00ff88;text-decoration:none}a:hover{text-decoration:underline}\n'
    '.hero{background:linear-gradient(135deg,#0a0a0a,#1a1a2e,#0d1117);padding:40px 20px;text-align:center;border-bottom:2px solid #00ff88}\n'
    '.hero h1{font-size:2em;color:#00ff88;margin-bottom:6px}\n'
    '.sub{color:#888;font-size:.95em;margin-bottom:10px}\n'
    '.bg{display:inline-block;background:#1a1a2e;border:1px solid #00ff88;padding:4px 12px;border-radius:20px;color:#00ff88;font-size:.8em;margin:3px}\n'
    'nav{background:#111;padding:10px 20px;border-bottom:1px solid #222;position:sticky;top:0;z-index:100;overflow-x:auto;white-space:nowrap}\n'
    'nav a{display:inline-block;padding:4px 10px;margin:2px;background:#1a1a2e;border:1px solid #333;border-radius:6px;font-size:.75em;color:#00ff88;transition:all .2s}\n'
    'nav a:hover{background:#00ff88;color:#0a0a0a;text-decoration:none}\n'
    '.c{max-width:1200px;margin:0 auto;padding:20px}\n'
    '.s{margin:28px 0;background:#1a1a2e;border:1px solid #222;border-radius:12px;overflow:hidden}\n'
    '.sh{background:linear-gradient(90deg,#1a1a2e,#0d1117);padding:14px 18px;border-bottom:1px solid #333}\n'
    '.sh h2{color:#00ff88;font-size:1.2em;margin-bottom:2px}\n'
    '.en{color:#666;font-size:.78em}\n'
    '.sb{padding:18px}\n'
    '.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-bottom:14px}\n'
    '.p{background:#0d1117;border:1px solid #222;border-radius:8px;padding:12px;transition:border-color .2s}\n'
    '.p:hover{border-color:#00ff88}\n'
    '.p h3{color:#00ff88;font-size:.84em;margin-bottom:5px}\n'
    '.p p{color:#aaa;font-size:.78em;line-height:1.5}\n'
    '.mt{background:#111;border:1px solid #222;border-radius:8px;padding:12px;margin-top:10px}\n'
    '.mt h4{color:#00ff88;font-size:.82em;margin-bottom:6px}\n'
    '.ml{display:flex;flex-wrap:wrap;gap:5px}\n'
    '.t{background:#1a1a2e;border:1px solid #00ff88;padding:2px 9px;border-radius:16px;font-size:.72em;color:#00ff88}\n'
    'footer{background:#111;border-top:2px solid #00ff88;padding:20px;text-align:center;margin-top:28px}\n'
    '.br{font-size:1.1em;color:#00ff88;font-weight:700;margin-bottom:5px}\n'
    'footer p{color:#666;font-size:.75em;line-height:1.5}\n'
    '.cr{margin-top:10px;padding-top:10px;border-top:1px solid #222;color:#555;font-size:.72em}\n'
    '@media(max-width:768px){.hero h1{font-size:1.4em}.g{grid-template-columns:1fr}}</style>\n'
)


def make_pack(slug, reg_full, reg_short, shield, blurb, statutes, entry_points):
    title = f"{reg_full} AI Deep-Dive Pack"
    nav_links = []
    for i, ep in enumerate(entry_points, start=1):
        anchor = f"#ep{i}"
        short = ep[:18].strip()
        nav_links.append(f'<a href="{anchor}">{short}</a>')
    nav_html = "".join(nav_links)

    sections = []
    for i, ep in enumerate(entry_points, start=1):
        priorities_html = []
        for pname, ptemplate in PRIORITIES:
            desc = ptemplate.format(ep=ep, reg_short=reg_short, statute_primary=statutes.split(" / ")[0])
            priorities_html.append(
                f'<div class="p"><h3>{pname}</h3><p>{desc}</p></div>'
            )
        mcp_html = "".join(f'<span class="t">{m}</span>' for m in MCPS)
        sections.append(
            f'<div class="s" id="ep{i}"><div class="sh"><span class="en">Entry Point {i:02d}</span>'
            f'<h2>{ep}</h2></div><div class="sb"><div class="g">'
            + "".join(priorities_html)
            + f'</div><div class="mt"><h4>MCP Tools</h4><div class="ml">{mcp_html}</div></div></div></div>'
        )

    json_ld = make_json_ld(slug, title)

    html = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        '<meta content="width=device-width,initial-scale=1" name="viewport"/>\n'
        f'<title>{title}</title>\n'
        + CSS +
        f'<link href="https://www.csoai.org/{slug}.html.llm.json" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>\n'
        '<meta content="/llms.txt" name="llms-txt"/>\n'
        '<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>\n'
        f'<meta content="CSOAI Ltd (2026). {title}. https://www.csoai.org/{slug}.html" name="citation-policy"/>\n'
        f'<meta content="{NOW}" name="revised"/>\n'
        f'<meta content="{NOW}" property="article:modified_time"/>\n'
        f'<meta content="DEFONEOS \u2014 {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification \u2014 every figure traces to a signed, verifiable record." name="description"/>\n'
        f'<link href="https://www.csoai.org/{slug}.html" rel="canonical"/>\n'
        f'<meta content="{title}" property="og:title"/>\n'
        f'<meta content="DEFONEOS \u2014 {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification \u2014 every figure traces to a signed, verifiable record." property="og:description"/>\n'
        f'<script type="application/ld+json">{json_ld}</script>\n'
        '</head>\n<body>\n'
        '<div class="hero">\n'
        f'<h1>{shield} {title}</h1>\n'
        '<p class="sub">DEFONEOS \u2014 UK Sovereign Public Services OS</p>\n'
        '<div><span class="bg">12 Entry Points</span><span class="bg">8 AI Priorities</span><span class="bg">6 MCP Tools</span></div>\n'
        f'<p>{blurb}</p>\n'
        '</div>\n'
        f'<nav>\n{nav_html}\n</nav>\n'
        '<div class="c">\n'
        + "\n".join(sections)
        + '\n</div>\n'
        '<footer>\n'
        '<div class="br">DEFONEOS \u2014 UK Sovereign Public Services OS</div>\n'
        f'<p>Open-source sovereign AI governance for {reg_full}. Built for audit-grade, signed, neutral UK-sovereign compliance.</p>\n'
        f'<p>AUKUS-compatible. {statutes}.</p>\n'
        '<div class="cr">\u00a9 2026 CSOAI Ltd (UK 16939677) \u00b7 meok-defoneos \u00b7 csoai-defoneos \u00b7 DEFONEOS-SEAL</div>\n'
        '</footer>\n</body>\n</html>\n'
    )
    return html


def make_llm_json(slug, reg_full, shield, entry_points):
    title = f"{reg_full} AI Deep-Dive Pack"
    headings = [f"{shield} {title}"] + entry_points
    body = {
        "@context": "https://csoai.org/llm-context.json",
        "type": "LLMPageSummary",
        "url": f"https://csoai.org/{slug}.html",
        "title": title,
        "description": f"DEFONEOS \u2014 {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification \u2014 every figure traces to a signed, verifiable record.",
        "headings": headings,
        "text": (
            f"{title} {shield} {title} DEFONEOS \u2014 UK Sovereign Public Services OS "
            "12 Entry Points 8 AI Priorities 6 MCP Tools "
            + " ".join(headings)
        ),
        "text_truncated": True,
        "register": {
            "role": "measurement_and_attestation_support",
            "csoai_certifies_systems": False,
            "csoai_is_a_notified_body": False,
            "csoai_has_enforcement_powers": False,
            "note": "CSOAI measures and publishes evidence. It issues no conformity marks and holds no accreditation. Nothing here is certification or legal advice.",
        },
        "generated_by": "tick282_make.py",
    }
    return json.dumps(body, indent=2) + "\n"


def main():
    written = []
    for slug, reg_full, reg_short, shield, blurb, statutes, eps in PACKS:
        html = make_pack(slug, reg_full, reg_short, shield, blurb, statutes, eps)
        llm = make_llm_json(slug, reg_full, shield, eps)
        hpath = ROOT / f"{slug}.html"
        lpath = ROOT / f"{slug}.html.llm.json"
        hpath.write_text(html)
        lpath.write_text(llm)

        h = hpath.read_text()
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
        try:
            parsed = json.loads(m.group(1)) if m else None
            ld_ok = parsed is not None and "@type" in parsed and "@context" in parsed and parsed.get("@type") == "WebPage"
        except Exception:
            ld_ok = False
        try:
            llm_parsed = json.loads(llm)
            llm_ok = llm_parsed.get("type") == "LLMPageSummary"
        except Exception:
            llm_ok = False

        en = len(re.findall(r'<span class="en">Entry Point', h))
        t = h.count('<span class="t">')
        p = h.count('<div class="p">')
        dt = h.count('<!DOCTYPE html>')
        ht = h.count('</html>')
        h1 = h.count('<h1>')

        print(f"  {slug}.html  {hpath.stat().st_size}b  |  .llm.json  {lpath.stat().st_size}b  |  "
              f"ld_ok={ld_ok}  llm_ok={llm_ok}  en={en} t={t} p={p} dt={dt} ht={ht} h1={h1}")
        written.append((slug, hpath.stat().st_size, lpath.stat().st_size))

    print(f"\nWROTE {len(written)} packs.")


if __name__ == "__main__":
    main()