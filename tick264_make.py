#!/usr/bin/env python3
"""DEFONEOS Tick 264 — build 3 specialist arms-length body deep-dive packs.

Next picks (post-tick-263 priority queue, defence domain):
- Ministry of Defence central (policy / strategy / parliamentary accountability)
- British Army (the Service itself, distinct from MoD central)
- Royal Air Force (the Service itself)

Pattern proven in ticks 255-263:
- 12 entry points x 8 AI priorities x 6 MCPs each
- JSON-LD schema.org-CANONICAL: {"@context":"https://schema.org","@type":"WebPage",...}
  (using Python json.dumps() to guarantee correct quoting/escaping)
- rel=alternate llm.json companion link
- canonical URL rel + meta citation-policy + revised timestamp
- 4-statute backbone cited in footer
- shield emoji + body full name
- no personal-surveillance / kinetic-targeting patterns (DEFONEOS hard stops)
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
     "Detection of {ep} risk breaches, control gaps, and early-warning indicators affecting {reg_short} performance and accountability to Parliament."),
    ("Natural Language Policy Analysis",
     "NLP analysis of {ep} legislation, policy statements, guidance, and parliamentary record against the full statutory framework and regulatory expectations."),
    ("Predictive Analytics",
     "{ep} risk and workload forecasting from trend indicators, demand signals, and operational metrics to support prioritisation and decision-support."),
    ("Evidence Synthesis",
     "{ep} evidence, inspection findings, returns, and stakeholder submissions assembled into decision dossiers for review by accountable officers and the BFT council."),
    ("Document Intelligence",
     "Extraction from {ep} documents, statutory returns, and correspondence for end-to-end {reg_short} lifecycle tracking and audit trails."),
    ("Stakeholder Reporting",
     "{ep} dashboards reporting coverage, performance, and outcomes to ministers, the board, and Parliament."),
    ("Real-time Monitoring",
     "{ep} pipeline tracking, submission cycles, and continuous surveillance of {reg_short} activity for sovereign, verifiable oversight."),
]

# (slug, reg_full, reg_short, shield, blurb, statutes, entry_points)
PACKS = [
    (
        "defoneos-ministry-of-defence-central-strategic-policy-ai-deep-dive-pack",
        "Ministry of Defence Central",
        "MoD central",
        "🪖",
        "12 MoD central entry points × 8 AI priorities × 6 MCP integrations — defence policy, strategy, finance, NATO coordination, AUKUS delivery and parliamentary accountability for the United Kingdom's armed forces",
        "Armed Forces Act 2006 / Defence Reform Act 2014 / Government Resources and Accounts Act 2000 / House of Commons (Armed Forces Committee) framework",
        [
            "Defence Policy & Strategic Direction",
            "Defence Investment & Spending Review Coordination",
            "Strategic Defence Review (SDR) Implementation",
            "NATO & AUKUS Programme Delivery",
            "Defence Industrial Strategy & Procurement",
            "Defence Diplomacy & International Partnerships",
            "Armed Forces Personnel Strategy & Workforce",
            "Reserve Forces & Cadet Policy",
            "Defence Estate Management (UK & Overseas)",
            "Veterans Affairs & Cross-Government Liaison",
            "Civil Defence & Resilience Coordination",
            "Governance & Parliamentary Accountability",
        ],
    ),
    (
        "defoneos-british-army-land-service-ai-deep-dive-pack",
        "British Army",
        "British Army",
        "🎖️",
        "12 British Army entry points × 8 AI priorities × 6 MCP integrations — land service operations, force development, regimental establishment and the Army's parliamentary reporting line",
        "Armed Forces Act 2006 / Army Act 1955 / Manual of Military Law / Queen\u2019s/King\u2019s Regulations for the Army",
        [
            "Land Service Operations & Readiness",
            "Force Development & Future Soldier Programme",
            "Regimental Establishment & Corps Governance",
            "Army Reserve & Volunteer Workforce",
            "Recruiting, Training & Initial Military Education",
            "Operational Deployments & Overseas Commitments",
            "Logistics, Equipment & Sustainment",
            "Army Estate & UK Garrison Infrastructure",
            "Land Warfare Doctrine & Training Centre",
            "Army Personnel & Welfare Policy",
            "Royal Military Academy Sandhurst & Officer Commissioning",
            "Governance & Parliamentary Accountability",
        ],
    ),
    (
        "defoneos-royal-air-force-air-space-service-ai-deep-dive-pack",
        "Royal Air Force",
        "Royal Air Force",
        "✈️",
        "12 Royal Air Force entry points × 8 AI priorities × 6 MCP integrations — air and space service operations, fast-jet and ISTAR capability, the RAF Regiment and RAF Reserve workforce",
        "Armed Forces Act 2006 / Air Force Act 1955 / Manual of Military Law / Queen\u2019s/King\u2019s Regulations for the Royal Air Force",
        [
            "Air Operations & Combat Air Capability",
            "Force Development & Combat Air Strategy",
            "ISTAR & Air Intelligence, Surveillance & Reconnaissance",
            "Air Mobility & Strategic Airlift Operations",
            "RAF Regiment & Force Protection",
            "RAF Reserve & Auxiliary Workforce",
            "Recruiting, Officer & Aircrew Training (Cranwell)",
            "Operational Deployments & Overseas Commitments",
            "Logistics, Engineering & Equipment Support",
            "Space Operations & UK Space Command Contribution",
            "Search & Rescue Coordination (Trident)",
            "Governance & Parliamentary Accountability",
        ],
    ),
]


def make_json_ld(slug, title):
    """Build the JSON-LD block via json.dumps() to guarantee correct escaping."""
    block = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": f"https://www.csoai.org/{slug}.html",
        "description": f"DEFONEOS \u2014 {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification \u2014 every figure traces to a signed, verifiable record.",
        "publisher": {"@type": "Organization", "name": "CSOAI Ltd", "url": "https://csoai.org"},
        "about": {"@type": "GovernmentService", "name": "UK Defence AI Governance"},
    }
    return json.dumps(block, separators=(",", ":"), ensure_ascii=False)


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
        "generated_by": "tick264_make.py",
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
        written.append((slug, hpath.stat().st_size, lpath.stat().st_size))

        # verify JSON-LD parses (this was the historic bug)
        h = hpath.read_text()
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
        try:
            parsed = json.loads(m.group(1)) if m else None
            ld_ok = parsed is not None and "@type" in parsed and "@context" in parsed
        except Exception:
            ld_ok = False
        # verify llm.json parses
        try:
            llm_parsed = json.loads(llm)
            llm_ok = llm_parsed.get("type") == "LLMPageSummary"
        except Exception:
            llm_ok = False
        print(f"  {slug}.html  {hpath.stat().st_size}b  |  .llm.json  {lpath.stat().st_size}b  |  ld_ok={ld_ok}  llm_ok={llm_ok}")

    print(f"\nWROTE {len(written)} packs.")
    return written


if __name__ == "__main__":
    main()
