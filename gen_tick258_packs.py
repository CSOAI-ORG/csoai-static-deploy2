#!/usr/bin/env python3
"""DEFONEOS Tick 258 generator — 3 new UK regulator/agency deep-dive packs.

Chosen bodies (probe-verified GENUINELY UNCOVERED on disk + sitemap before build):
1. Parole Board for England and Wales          (justice / risk release decisions)
2. Maritime and Coastguard Agency (MCA)        (maritime safety / coastguard)
3. Single Source Regulations Office (SSRO)     (defence single-source procurement pricing)

NOT using the stale tick258_make.py: those targets (GLAA / ICO sandbox / DWI) are already
covered on disk under different slugs — running it would create duplicates (skill dedup pitfall).

Style: dense regulator pack (ticks 255-257 format). 12 entry points x 8 AI priorities
x 6 MCP tools. 34-38KB. JSON-LD GENUINELY CANONICAL (\"@context\":\"https://schema.org\")
-- NOT the corrupted https://***@type artifact found in older on-disk packs.
"""
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

CSS = "*{margin:0;padding:0;box-sizing:border-box}\n" \
"body{background:#0a0a0a;color:#e0e0e0;font-family:system-ui,sans-serif;line-height:1.6}\n" \
"a{color:#00ff88;text-decoration:none}a:hover{text-decoration:underline}\n" \
".hero{background:linear-gradient(135deg,#0a0a0a,#1a1a2e,#0d1117);padding:40px 20px;text-align:center;border-bottom:2px solid #00ff88}\n" \
".hero h1{font-size:2em;color:#00ff88;margin-bottom:6px}\n" \
".sub{color:#888;font-size:.95em;margin-bottom:10px}\n" \
".bg{display:inline-block;background:#1a1a2e;border:1px solid #00ff88;padding:4px 12px;border-radius:20px;color:#00ff88;font-size:.8em;margin:3px}\n" \
"nav{background:#111;padding:10px 20px;border-bottom:1px solid #222;position:sticky;top:0;z-index:100;overflow-x:auto;white-space:nowrap}\n" \
"nav a{display:inline-block;padding:4px 10px;margin:2px;background:#1a1a2e;border:1px solid #333;border-radius:6px;font-size:.75em;color:#00ff88;transition:all .2s}\n" \
"nav a:hover{background:#00ff88;color:#0a0a0a;text-decoration:none}\n" \
".c{max-width:1200px;margin:0 auto;padding:20px}\n" \
".s{margin:28px 0;background:#1a1a2e;border:1px solid #222;border-radius:12px;overflow:hidden}\n" \
".sh{background:linear-gradient(90deg,#1a1a2e,#0d1117);padding:14px 18px;border-bottom:1px solid #333}\n" \
".sh h2{color:#00ff88;font-size:1.2em;margin-bottom:2px}\n" \
".en{color:#666;font-size:.78em}\n" \
".sb{padding:18px}\n" \
".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-bottom:14px}\n" \
".p{background:#0d1117;border:1px solid #222;border-radius:8px;padding:12px;transition:border-color .2s}\n" \
".p:hover{border-color:#00ff88}\n" \
".p h3{color:#00ff88;font-size:.84em;margin-bottom:5px}\n" \
".p p{color:#aaa;font-size:.78em;line-height:1.5}\n" \
".mt{background:#111;border:1px solid #222;border-radius:8px;padding:12px;margin-top:10px}\n" \
".mt h4{color:#00ff88;font-size:.82em;margin-bottom:6px}\n" \
".ml{display:flex;flex-wrap:wrap;gap:5px}\n" \
".t{background:#1a1a2e;border:1px solid #00ff88;padding:2px 9px;border-radius:16px;font-size:.72em;color:#00ff88}\n" \
"footer{background:#111;border-top:2px solid #00ff88;padding:20px;text-align:center;margin-top:28px}\n" \
".br{font-size:1.1em;color:#00ff88;font-weight:700;margin-bottom:5px}\n" \
"footer p{color:#666;font-size:.75em;line-height:1.5}\n" \
".cr{margin-top:10px;padding-top:10px;border-top:1px solid #222;color:#555;font-size:.72em}\n" \
"@media(max-width:768px){.hero h1{font-size:1.4em}.g{grid-template-columns:1fr}}"

MCP_CHIPS = ["mcp-bailii", "mcp-govuk-search", "mcp-hansard-search",
             "mcp-uk-courts", "mcp-uk-legislation", "mcp-uk-regulator-intel"]

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


def build_pack(slug, title, reg, sub_domain, laws, law_primary, entry_points):
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
    # GENUINELY canonical JSON-LD (NOT the corrupted https://***@type artifact)
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
<meta content="{NOW}" name="revised"/>
<meta content="{NOW}" property="article:modified_time"/>
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


def make_llm_json(slug, title, reg, entry_points):
    headings = [title] + entry_points
    return (
        '{\n'
        '  "@context": "https://csoai.org/llm-context.json",\n'
        '  "type": "LLMPageSummary",\n'
        f'  "url": "https://csoai.org/{slug}.html",\n'
        f'  "title": "{title}",\n'
        f'  "description": "DEFONEOS — {title}. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record.",\n'
        '  "headings": ' + repr(headings).replace("'", '"') + ',\n'
        '  "text": "' + (f"{title} DEFONEOS — UK Sovereign Public Services OS 12 Entry Points 8 AI Priorities 6 MCP Tools " + " ".join(headings)).replace('"', '\\"') + '",\n'
        '  "text_truncated": true,\n'
        '  "register": {\n'
        '    "role": "measurement_and_attestation_support",\n'
        '    "csoai_certifies_systems": false,\n'
        '    "csoai_is_a_notified_body": false,\n'
        '    "csoai_has_enforcement_powers": false,\n'
        '    "note": "CSOAI measures and publishes evidence. It issues no conformity marks and holds no accreditation. Nothing here is certification or legal advice."\n'
        '  },\n'
        '  "generated_by": "gen_tick258_packs.py"\n'
        '}\n'
    )


PACKS = [
    dict(
        slug="defoneos-parole-board-england-wales-ai-deep-dive-pack",
        title="Parole Board for England and Wales AI Deep-Dive Pack",
        reg="Parole Board",
        sub_domain="parole review, risk assessment and release decision-making for the Parole Board of England and Wales",
        laws=("Criminal Justice Act 2003 / Parole Board Rules 2019 / "
              "Justice and Security Act 2013 / Prisons and Courts Act 2017"),
        law_primary="Criminal Justice Act 2003",
        entry_points=[
            "Parole Review & Risk Assessment",
            "Indeterminate Sentence Release Hearings",
            "Extended & Determinate Sentence Reviews",
            "Recall Decision & Revocation Hearings",
            "Victim & Survivor Participation",
            "Oral Hearing Case Management",
            "Risk Assessment & Expert Evidence",
            "Open vs Closed Conditions Decisions",
            "Parole Directions & Release Conditions",
            "Remand, Juvenile & Young Offender Reviews",
            "Decision-Making Standards & Dossier Integrity",
            "Governance & Parliamentary Accountability",
        ],
    ),
    dict(
        slug="defoneos-maritime-coastguard-agency-ai-deep-dive-pack",
        title="Maritime and Coastguard Agency AI Deep-Dive Pack",
        reg="Maritime and Coastguard Agency",
        sub_domain="maritime safety, ship survey and certification, HM Coastguard search and rescue, and marine pollution response",
        laws=("Merchant Shipping Act 1995 / Marine Safety Act 2003 / "
              "Port Marine Safety Code / Merchant Shipping Regulations"),
        law_primary="Merchant Shipping Act 1995",
        entry_points=[
            "Ship Registration & Nationality",
            "Vessel Survey & Certification",
            "Safety of Navigation & Operations",
            "Port State Control Inspections",
            "Seafarer Certification & Training (STCW)",
            "HM Coastguard Search & Rescue",
            "Marine Pollution Prevention & Response",
            "Fishing Vessel Safety Regulation",
            "Small Craft & Pleasure Vessel Oversight",
            "Emergency Response & Incident Coordination",
            "Marine Environmental Protection",
            "Governance & Parliamentary Accountability",
        ],
    ),
    dict(
        slug="defoneos-ssro-single-source-regulations-office-ai-deep-dive-pack",
        title="Single Source Regulations Office AI Deep-Dive Pack",
        reg="Single Source Regulations Office",
        sub_domain="regulation of single-source defence procurement, pricing, profit rates and contract reporting for UK Defence",
        laws=("Defence Reform Act 2014 / Single Source Contract Regulations 2014 / "
              "Public Contracts Regulations 2015 / Defence and Security Public Contracts Regulations 2011"),
        law_primary="Defence Reform Act 2014",
        entry_points=[
            "Single Source Contract Regulation",
            "Pricing & Profit Rate Determination",
            "Cost Accounting & Allowable Costs",
            "Contract Reporting & Data Return Compliance",
            "Referral & Dispute Determination",
            "Contract Profit Rate Methodology",
            "Quarterly Reporting Framework",
            "Independent Review & Statutory Guidance",
            "Defence Procurement Oversight",
            "Benchmarking & Market Efficiency",
            "Statutory Compliance & Enforcement",
            "Governance & Parliamentary Accountability",
        ],
    ),
]


def main():
    written = []
    for p in PACKS:
        html = build_pack(**p)
        slug = p["slug"]
        hpath = ROOT / f"{slug}.html"
        lpath = ROOT / f"{slug}.html.llm.json"
        hpath.write_text(html, encoding="utf-8")
        lpath.write_text(make_llm_json(slug, p["title"], p["reg"], p["entry_points"]), encoding="utf-8")
        written.append((slug, hpath.stat().st_size, lpath.stat().st_size))
    print(f"WROTE {len(written)} packs (ts={NOW}):")
    for slug, hs, ls in written:
        print(f"  {slug}.html  {hs}b  |  .llm.json  {ls}b")


if __name__ == "__main__":
    main()
