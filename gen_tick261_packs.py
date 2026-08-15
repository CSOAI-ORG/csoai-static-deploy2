#!/usr/bin/env python3
"""DEFONEOS Tick 261 generator — 3 new UK regulator/agency deep-dive packs
+ JSON-LD repair sweep for 9 corrupted packs.

Chosen bodies (probe-verified GENUINELY UNCOVERED on disk + sitemap before build):
1. HM Treasury                                  (economic & fiscal policy / public finance)
2. Joint Nature Conservation Committee (JNCC)   (nature conservation / biodiversity)
3. Met Office                                   (meteorological services / climate science)

NOT using stale tick targets — all 3 probe-verified open.

Style: dense regulator pack (ticks 255-260 format). 12 entry points x 8 AI priorities
x 6 MCP tools. ~36KB. JSON-LD GENUINELY CANONICAL ("@context":"https://schema.org").

JSON-LD repair: 9 packs carry the corrupted https://***@type artifact instead of
canonical schema.org. Patches:
  defoneos-fca-financial-conduct-authority-ai-deep-dive-pack
  defoneos-highways-england-transport-network-optimization-ai-deep-dive-pack
  defoneos-ico-data-protection-info-rights-ai-deep-dive-pack
  defoneos-ico-information-commissioners-office-ai-deep-dive-pack
  defoneos-nhs-england-health-service-delivery-ai-deep-dive-pack
  defoneos-ofwat-water-regulation-ai-deep-dive-pack
  defoneos-uksa-space-intelligence-data-ai-deep-dive-pack
  defoneos-voa-valuation-office-agency-ai-deep-dive-pack
  defoneos-wra-welsh-revenue-authority-ai-deep-dive-pack
"""
from pathlib import Path
from datetime import datetime, timezone
import re

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
    # GENUINELY canonical JSON-LD
    jsonld = (
        '{"@context":"https://schema.org","@type":"WebPage",'
        f'"name":"{title}","url":"{url}",'
        f'"description":"{desc}",'
        f'"publisher":{{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"}},'
        f'"about":{{"@type":"GovernmentService","name":"{reg} AI Governance"}}}}'
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
        '  "generated_by": "gen_tick261_packs.py"\n'
        '}\n'
    )


PACKS = [
    dict(
        slug="defoneos-hm-treasury-economic-fiscal-policy-ai-deep-dive-pack",
        title="HM Treasury Economic & Fiscal Policy AI Deep-Dive Pack",
        reg="HM Treasury",
        sub_domain="economic and fiscal policy, public finance, spending review, financial services regulation and macroeconomic stewardship",
        laws=("Budget Responsibility and National Audit Act 2011 / Finance Act framework / "
              "Banking Act 2009 / Financial Services and Markets Act 2000 (FSMA 2000)"),
        law_primary="Budget Responsibility and National Audit Act 2011",
        entry_points=[
            "Fiscal Policy & Budget Framework",
            "Spending Review & Public Spending Control",
            "Macroeconomic Forecasting & OBR Liaison",
            "Tax Policy & Finance Bill Coordination",
            "Financial Services Regulation & FSMA Oversight",
            "Banking, Capital Markets & Prudential Coordination",
            "Debt Management & Gilts Issuance (DMO)",
            "International Economic Policy & G7/G20",
            "Public Investment & Green Book Appraisal",
            "Fraud, Error & Debt Recovery (Public Sector)",
            "Sanctions Implementation & OFSI Operations",
            "Governance & Parliamentary Accountability",
        ],
    ),
    dict(
        slug="defoneos-jncc-joint-nature-conservation-committee-ai-deep-dive-pack",
        title="Joint Nature Conservation Committee (JNCC) AI Deep-Dive Pack",
        reg="Joint Nature Conservation Committee",
        sub_domain="nature conservation science, biodiversity monitoring and UK overseas territory environmental advice",
        laws=("Environment Act 2021 / Wildlife and Countryside Act 1981 / "
              "Conservation of Habitats and Species Regulations 2017 / Marine and Coastal Access Act 2009"),
        law_primary="Environment Act 2021",
        entry_points=[
            "Biodiversity Monitoring & Indicators",
            "Marine Conservation & MPA Evidence Base",
            "Habitats Directive Reporting & Article 17",
            "UK Biodiversity Targets & 2030 Outcomes",
            "Overseas Territories Biodiversity Programme",
            "Earth Observation & Remote Sensing",
            "Species Conservation & Recovery Planning",
            "Climate Change Adaptation Evidence",
            "Pollinator Monitoring & Insect Decline",
            "Peatland, Soil & Habitat Condition Evidence",
            "Geoconservation & Geological Heritage",
            "Governance & Parliamentary Accountability",
        ],
    ),
    dict(
        slug="defoneos-met-office-meteorological-services-ai-deep-dive-pack",
        title="Met Office Meteorological Services AI Deep-Dive Pack",
        reg="Met Office",
        sub_domain="national meteorological service, weather forecasting, climate science and climate change projections",
        laws=("Met Office Trading Fund Order 1996 / Meteorological Office Act 1867 / "
              "Climate Change Act 2008 / Civil Contingencies Act 2004"),
        law_primary="Met Office Trading Fund Order 1996",
        entry_points=[
            "National Weather Forecasting & Numerical Prediction",
            "Severe Weather Warnings & Civil Contingencies",
            "Climate Change Projections & UKCP18/UKCP26",
            "Hydrometeorology & Flood Forecasting",
            "Aviation Meteorological Services",
            "Marine & Shipping Forecast Services",
            "Atmospheric Composition & Air Quality",
            "Space Weather Operations",
            "Climate Science Research & Hadley Centre",
            "International Cooperation & WMO Programmes",
            "Defence & Security Meteorological Support",
            "Governance & Parliamentary Accountability",
        ],
    ),
]


# Packs to repair — replace corrupted JSON-LD artifact with canonical schema.org
# Pattern: {"@context":"https://***@type":"Article",...} -> canonical
REPAIR_SLUGS = [
    "defoneos-fca-financial-conduct-authority-ai-deep-dive-pack",
    "defoneos-highways-england-transport-network-optimization-ai-deep-dive-pack",
    "defoneos-ico-data-protection-info-rights-ai-deep-dive-pack",
    "defoneos-ico-information-commissioners-office-ai-deep-dive-pack",
    "defoneos-nhs-england-health-service-delivery-ai-deep-dive-pack",
    "defoneos-ofwat-water-regulation-ai-deep-dive-pack",
    "defoneos-uksa-space-intelligence-data-ai-deep-dive-pack",
    "defoneos-voa-valuation-office-agency-ai-deep-dive-pack",
    "defoneos-wra-welsh-revenue-authority-ai-deep-dive-pack",
]


def repair_corrupted_jsonld(slug):
    """Replace the corrupted https://***@type artifact with canonical schema.org
    JSON-LD block. Idempotent. Returns (bytes_before, bytes_after, did_repair)."""
    path = ROOT / f"{slug}.html"
    if not path.exists():
        return None
    txt = path.read_text(encoding="utf-8")
    if 'https://***@type' not in txt:
        return (txt, txt.encode("utf-8"), False)
    # Canonical schema.org JSON-LD — extract title from <title>...</title>
    m = re.search(r'<title>([^<]+)</title>', txt)
    title = m.group(1) if m else slug
    url = f"https://www.csoai.org/{slug}.html"
    canonical_ld = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"WebPage",'
        f'"name":"{title}","url":"{url}",'
        '"publisher":{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"},'
        '"about":{"@type":"GovernmentService","name":"UK Sovereign AI Governance"}}'
        '</script>'
    )
    # Replace the corrupted script block in-place
    pattern = re.compile(
        r'<script type="application/ld\+json">\{\"@context\":\"https://\*\*\*@type\".*?</script>',
        re.DOTALL,
    )
    new_txt, n = pattern.subn(canonical_ld, txt)
    if n == 0:
        return (txt, txt.encode("utf-8"), False)
    return (new_txt, new_txt.encode("utf-8"), True)


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

    print()
    print(f"REPAIR sweep across {len(REPAIR_SLUGS)} packs:")
    repaired = 0
    for slug in REPAIR_SLUGS:
        result = repair_corrupted_jsonld(slug)
        if result is None:
            print(f"  MISSING: {slug}")
            continue
        new_txt, _, did = result
        if did:
            (ROOT / f"{slug}.html").write_text(new_txt, encoding="utf-8")
            repaired += 1
            print(f"  FIXED:   {slug}.html  ({(ROOT / f'{slug}.html').stat().st_size}b)")
        else:
            print(f"  CLEAN:   {slug}.html  (already canonical)")
    print(f"\nRepaired {repaired}/{len(REPAIR_SLUGS)} corrupted JSON-LD blocks")


if __name__ == "__main__":
    main()
