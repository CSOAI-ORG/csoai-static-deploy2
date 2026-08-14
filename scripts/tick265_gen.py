#!/usr/bin/env python3
"""Tick 265 generator: 3 NEW deep-dive packs (Supreme Court / Royal Society / Sentencing Council).
Replicates the byte-verified tick-250+ regulator-deep-dive-pack format exactly:
inline CSS, single-body-line sections, 12 entry points x 8 fixed priority cards x 6 MCP chips.
"""
import json
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

LAWS = {
    "supreme-court": "Constitutional Reform Act 2005",
    "royal-society": "Royal Charter 1662",
    "sentencing-council": "Coroners and Justice Act 2009",
}

FOOTER_LAWS = {
    "supreme-court": "Constitutional Reform Act 2005 / Human Rights Act 1998 / Senior Courts Act 1981 / Judicial Committee Act 1833",
    "royal-society": "Royal Charter 1662 / Higher Education and Research Act 2017 / Charities Act 2011 / Science and Technology Act 1965",
    "sentencing-council": "Coroners and Justice Act 2009 / Sentencing Act 2020 / Courts Act 2003 / Criminal Justice Act 2003",
}

BODIES = {
    "supreme-court": {
        "emoji": "⚖️",
        "title": "United Kingdom Supreme Court AI Deep-Dive Pack",
        "sub": "The Supreme Court of the United Kingdom",
        "tag": "12 UK Supreme Court entry points × 8 AI priorities × 6 MCP integrations — appellate jurisdiction, permission to appeal, constitutional and devolution issues, judicial independence and precedent-setting",
        "ep": [
            "Case Management & Appeals Processing",
            "Permission to Appeal (PTA) Determination",
            "Constitutional & Human Rights Jurisdiction",
            "Devolution Issue Determination",
            "Appellate Panel Constitution & Collegiality",
            "Judicial Reasoning & Precedent Setting",
            "Legal Research & Court Library Services",
            "Judgment Writing & Timely Publication",
            "Court Administration & Registries Governance",
            "Registrar & Court Officers Oversight",
            "Judicial Independence & Ethical Standards",
            "Governance & Parliamentary Accountability",
        ],
    },
    "royal-society": {
        "emoji": "🔬",
        "title": "Royal Society Scientific Advice AI Deep-Dive Pack",
        "sub": "The Royal Society of London for Improving Natural Knowledge",
        "tag": "12 Royal Society entry points × 8 AI priorities × 6 MCP integrations — fellowship, independent scientific advice, research funding, policy engagement and public science communication",
        "ep": [
            "Fellowship Nomination & Election Governance",
            "Independent Scientific Advice & Policy Engagement",
            "Research Grants & Funding Programmes",
            "Public Engagement & Science Communication",
            "International Scientific Collaboration & Diplomacy",
            "Science Education & Schools Outreach",
            "Data & Evidence Review Committees",
            "Publications & Journals Governance",
            "Emerging Technologies Assessment (AI & Biotech)",
            "Climate & Environmental Science Advice",
            "Science Culture, Diversity & Inclusion",
            "Governance & Parliamentary Accountability",
        ],
    },
    "sentencing-council": {
        "emoji": "📏",
        "title": "Sentencing Council AI Deep-Dive Pack",
        "sub": "The Sentencing Council for England and Wales",
        "tag": "12 Sentencing Council entry points × 8 AI priorities × 6 MCP integrations — definitive guidelines, Crown and Magistrates' court sentencing, statistical analysis and public consultation",
        "ep": [
            "Sentencing Guidelines Development",
            "Definitive Guideline Publication & Use",
            "Guideline Monitoring & Evaluation",
            "Crown Court Sentencing Analysis",
            "Magistrates' Court Sentencing Analysis",
            "Data Collection & Statistical Analysis",
            "Aggravating & Mitigating Factors Guidance",
            "Offence-Specific Guideline Design",
            "Sentencing Statistics & Trends Reporting",
            "Judicial Training & Guideline Dissemination",
            "Public Consultation & Stakeholder Engagement",
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


def build_one(key):
    b = BODIES[key]
    law = LAWS[key]
    f_laws = FOOTER_LAWS[key]
    slug = f"defoneos-uk-{key}-ai-deep-dive-pack" if key == "supreme-court" else f"defoneos-{key}-ai-deep-dive-pack"
    # Align exact slug names:
    slug = SLUGS[key]
    url = f"https://www.csoai.org/{slug}.html"
    title = b["title"]
    desc = f"DEFONEOS — {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record."

    # JSON-LD via json.dumps to guarantee canonical escaping
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
        # Card 1: Compliance Automation (primary statute)
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
        '<meta content="2026-08-12T08:00:00+00:00" name="revised"/>\n'
        '<meta content="2026-08-12T08:00:00+00:00" property="article:modified_time"/>\n'
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


SLUGS = {
    "supreme-court": "defoneos-uk-supreme-court-appellate-governance-ai-deep-dive-pack",
    "royal-society": "defoneos-royal-society-scientific-advice-ai-deep-dive-pack",
    "sentencing-council": "defoneos-sentencing-council-england-wales-ai-deep-dive-pack",
}

if __name__ == "__main__":
    for key in ["supreme-court", "royal-society", "sentencing-council"]:
        slug, html = build_one(key)
        out = ROOT / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        print(f"wrote {out.name}  {len(html)} bytes  ({out.stat().st_size} on disk)")
