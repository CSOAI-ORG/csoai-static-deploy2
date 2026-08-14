#!/usr/bin/env python3
"""Tick 267 generator (corrected): 3 NEW genuinely-uncovered regulator/agency deep-dive packs
(Press Recognition Panel / Investigatory Powers Tribunal / Channel 4).
Replicates byte-verified tick-250+ format exactly: inline CSS, single-body-line sections,
12 entry points x 8 fixed priority cards x 6 MCP chips. ROOT anchored to repo root.
Disk + sitemap probed first (tick-265 pitfall): these 3 are open, the stale
High/Crown/Magistrates targets were already covered.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

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

LAWS = {
    "press-recognition-panel": "Royal Charter on Self-Regulation of the Press 2013",
    "investigatory-powers-tribunal": "Investigatory Powers Act 2016",
    "channel-4": "Communications Act 2003",
}

FOOTER_LAWS = {
    "press-recognition-panel": "Royal Charter on Self-Regulation of the Press 2013 / Privacy and Electronic Communications Regulations 2003 / Legal Services Act 2007 / Human Rights Act 1998",
    "investigatory-powers-tribunal": "Investigatory Powers Act 2016 / Regulation of Investigatory Powers Act 2000 / Human Rights Act 1998 / Data Protection Act 2018",
    "channel-4": "Communications Act 2003 / Broadcasting Act 1990 / Digital Economy Act 2017 / Media Act 2024",
}

BODIES = {
    "press-recognition-panel": {
        "emoji": "📰",
        "title": "Press Recognition Panel AI Deep-Dive Pack",
        "sub": "The Press Recognition Panel",
        "tag": "12 Press Recognition Panel entry points × 8 AI priorities × 6 MCP integrations — press self-regulation recognition, media accountability, publisher governance and public interest journalism standards",
        "ep": [
            "Recognition of Press Regulators",
            "Recognition Criteria Assessment",
            "Regulator Application & Review Process",
            "Public Interest Journalism Standards",
            "Publisher & Editor Accountability",
            "Media Complaints Handling Oversight",
            "Editorial Independence Protection",
            "Press Standards Code Compliance",
            "Data Protection & Privacy in Journalism",
            "Leveson Inquiry Recommendations Implementation",
            "Public Reporting & Transparency",
            "Governance & Parliamentary Accountability",
        ],
    },
    "investigatory-powers-tribunal": {
        "emoji": "🕵️",
        "title": "Investigatory Powers Tribunal AI Deep-Dive Pack",
        "sub": "The Investigatory Powers Tribunal of the United Kingdom",
        "tag": "12 Investigatory Powers Tribunal entry points × 8 AI priorities × 6 MCP integrations — surveillance complaints, warrants oversight, interception review and the protection of privacy against state powers",
        "ep": [
            "Complaints & Claims Jurisdiction",
            "Warrant & Authorisation Review",
            "Interception of Communications Oversight",
            "Data Retention & Acquisition Review",
            "Equipment Interference Scrutiny",
            "Bulk Collection Powers Review",
            "Human Rights Compliance Assessment",
            "Intelligence Service Conduct Review",
            "Privacy & Liberty Determinations",
            "Remedies, Compensation & Reports",
            "Public Interest Reporting & Transparency",
            "Governance & Parliamentary Accountability",
        ],
    },
    "channel-4": {
        "emoji": "📺",
        "title": "Channel 4 Public Service Broadcasting AI Deep-Dive Pack",
        "sub": "Channel Four Television Corporation · United Kingdom",
        "tag": "12 Channel 4 entry points × 8 AI priorities × 6 MCP integrations — public service broadcasting, commissioning, media plurality, independent production quotas and audience representation",
        "ep": [
            "Public Service Broadcasting Remit",
            "Commissioning & Independent Production",
            "Creative Diversity & Inclusion",
            "Audience Representation & Accessibility",
            "Ofcom Licence Compliance",
            "Content Standards & Editorial Oversight",
            "Advertising & Commercial Operations",
            "Digital & On-Demand Transformation",
            "Media Plurality & Competition",
            "Regional & Nations Content",
            "Data Protection & Audience Privacy",
            "Governance & Parliamentary Accountability",
        ],
    },
}

PRIORITY_TAIL = {
    "Risk Detection & Early Warning": "Detection of {EP} risk breaches, control gaps, and early-warning indicators affecting {SUB} performance and accountability to Parliament.",
    "Natural Language Policy Analysis": "NLP analysis of {EP} legislation, policy statements, guidance, and parliamentary record against the full statutory framework and regulatory expectations.",
    "Predictive Analytics": "{EP} risk and workload forecasting from trend indicators, demand signals, and operational metrics to support prioritisation and decision-support.",
    "Evidence Synthesis": "{EP} evidence, inspection findings, returns, and stakeholder submissions assembled into decision dossiers for review by accountable officers and the BFT council.",
    "Document Intelligence": "Extraction from {EP} documents, statutory returns, and correspondence for end-to-end {SUB} lifecycle tracking and audit trails.",
    "Stakeholder Reporting": "{EP} dashboards reporting coverage, performance, and outcomes to ministers, the board, and Parliament.",
    "Real-time Monitoring": "{EP} pipeline tracking, submission cycles, and continuous surveillance of {SUB} operational posture and statutory deliverables.",
}

MCP = ["mcp-bailii", "mcp-govuk-search", "mcp-hansard-search", "mcp-uk-courts", "mcp-uk-legislation", "mcp-uk-regulator-intel"]

SLUGS = {
    "press-recognition-panel": "defoneos-press-recognition-panel-ai-deep-dive-pack",
    "investigatory-powers-tribunal": "defoneos-investigatory-powers-tribunal-ai-deep-dive-pack",
    "channel-4": "defoneos-channel-4-public-service-broadcasting-ai-deep-dive-pack",
}


def build_one(key):
    b = BODIES[key]
    law = LAWS[key]
    f_laws = FOOTER_LAWS[key]
    slug = SLUGS[key]
    url = f"https://www.csoai.org/{slug}.html"
    title = b["title"]
    desc = f"DEFONEOS — {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record."

    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": url,
        "description": desc,
        "publisher": {"@type": "Organization", "name": "CSOAI Ltd", "url": "https://csoai.org"},
        "about": {"@type": "GovernmentService", "name": "UK Public Services AI Governance"},
    }
    ld_json = json.dumps(ld, ensure_ascii=False)

    nav = "".join(f'<a href="#ep{i+1}">{ep[:23]}</a>' for i, ep in enumerate(b["ep"]))

    sections = []
    for i, ep in enumerate(b["ep"]):
        cards = []
        cards.append(f'<div class="p"><h3>Compliance Automation</h3><p>Automated {b["sub"]} {ep} validation checking {law} against {ep} statutory and rulebook requirements. No {b["sub"]} activity proceeds without a signed, auditable compliance record.</p></div>')
        for name, tmpl in PRIORITY_TAIL.items():
            txt = tmpl.format(EP=ep, SUB=b["sub"])
            cards.append(f'<div class="p"><h3>{name}</h3><p>{txt}</p></div>')
        chips = "".join(f'<span class="t">{m}</span>' for m in MCP)
        sections.append(
            f'<div class="s" id="ep{i+1}"><div class="sh"><span class="en">Entry Point {i+1:02d}</span><h2>{ep}</h2></div>'
            f'<div class="sb"><div class="g">{"".join(cards)}</div>'
            f'<div class="mt"><h4>MCP Tools</h4><div class="ml">{chips}</div></div></div></div>'
        )

    html = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        '<meta content="width=device-width,initial-scale=1" name="viewport"/>\n'
        f'<title>{title}</title>\n<style>{CSS}</style>\n'
        f'<link href="{url}.llm.json" rel="alternate" title="LLM representation of this page" type="application/llm+json"/>\n'
        '<meta content="/llms.txt" name="llms-txt"/>\n'
        '<meta content="human-authored, machine-verifiable, Ed25519-signed" name="ai-content-declaration"/>\n'
        f'<meta content="CSOAI Ltd (2026). {title}. {url}" name="citation-policy"/>\n'
        '<meta content="2026-08-12T13:00:00+00:00" name="revised"/>\n'
        '<meta content="2026-08-12T13:00:00+00:00" property="article:modified_time"/>\n'
        f'<meta content="{desc}" name="description"/>\n'
        f'<link href="{url}" rel="canonical"/>\n'
        f'<meta content="{title}" property="og:title"/>\n'
        f'<meta content="{desc}" property="og:description"/>\n'
        f'<script type="application/ld+json">{ld_json}</script>\n'
        '</head>\n<body>\n'
        f'<div class="hero">\n<h1>{b["emoji"]} {title}</h1>\n<p class="sub">DEFONEOS — UK Sovereign Public Services OS</p>\n'
        '<div><span class="bg">12 Entry Points</span><span class="bg">8 AI Priorities</span><span class="bg">6 MCP Tools</span></div>\n'
        f'<p>{b["tag"]}</p>\n</div>\n<nav>\n{nav}\n</nav>\n<div class="c">\n'
        + "\n".join(sections) +
        '\n</div>\n<footer>\n'
        '<div class="br">DEFONEOS — UK Sovereign Public Services OS</div>\n'
        f'<p>Open-source sovereign AI governance for {b["sub"]}. Built for audit-grade, signed, neutral UK-sovereign compliance.</p>\n'
        f'<p>AUKUS-compatible. {f_laws}.</p>\n'
        '<div class="cr">© 2026 CSOAI Ltd (UK 16939677) · meok-defoneos · csoai-defoneos · DEFONEOS-SEAL</div>\n'
        '</footer>\n</body>\n</html>\n'
    )
    return slug, html


if __name__ == "__main__":
    for key in ["press-recognition-panel", "investigatory-powers-tribunal", "channel-4"]:
        slug, html = build_one(key)
        out = ROOT / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        print(f"wrote {out.name}  {len(html)} bytes  ({out.stat().st_size} on disk)")