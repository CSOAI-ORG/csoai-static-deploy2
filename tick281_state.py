#!/usr/bin/env python3
"""Tick 281: update all 3 copies of DEFONEOS_SPRINT_STATE.json."""
import json, os

ROOT = "/Users/nicholas/clawd/csoai-static-deploy2"
smb = os.path.getsize(os.path.join(ROOT, "sitemap.xml"))
smab = os.path.getsize(os.path.join(ROOT, "sitemap-ai.xml"))

state = {
    "started_at": "2026-07-04",
    "current_day": 40,
    "current_tick": 281,
    "current_phase": 253,
    "total_mcp_built": 30,
    "total_pages_built": 1055,
    "total_repos_cloned": 15,
    "sitemap_urls": 833,
    "sitemap_bytes": smb + smab,
    "last_action": "Sprint tick 281 - 3 NEW genuinely-uncovered devolved public-services deep-dive packs (probe-verified 0 disk + 0 sitemap hits BEFORE build per tick-265 pitfall; EA NI != any GB education body, SLAB distinct statutory legal-aid board, Social Security Scotland distinct devolved benefits agency; legislature PARAMETRIC per body - Northern Ireland Assembly / Scottish Parliament): (1) defoneos-education-authority-northern-ireland-ai-deep-dive-pack 39893b - 12 EA NI entry points (Nursery, Primary & Post-Primary Education Provision / Special Educational Needs (SEN) Support / School Transport Services / Education Welfare & Attendance / Youth Services & Community Engagement / Early Years & Pre-School Provision / School Meals & Catering Services / Curriculum Support & Teacher Resources / Capital Projects & School Infrastructure / Procurement & Supplier Management / Data Protection & Pupil Records / Governance & Northern Ireland Assembly Accountability) x 8 priorities x 6 MCPs x Education Reform (NI) Order 1989 / Education (NI) Order 2006 / SEND (NI) Order 2005 / Northern Ireland Act 1998 / DPA 2018 backbone; (2) defoneos-scottish-legal-aid-board-ai-deep-dive-pack 37303b - 12 SLAB entry points (Criminal Legal Aid Administration / Civil Legal Aid Applications & Assessment / Advice & Assistance Scheme / Legal Aid Contributions & Financial Eligibility / Solicitor & Counsel Fee Payments / Quality Assurance & Compliance / Special Urgency & Emergency Applications / Children's Legal Aid / Grant & Determination Appeals / Fraud Prevention & Recovery / Data Protection & Case Records / Governance & Scottish Parliament Accountability) x 8 priorities x 6 MCPs x Legal Aid (Scotland) Act 1986 / Regulation of Legal Services (Scotland) Act 2010 / Scotland Act 1998 / DPA 2018 backbone; (3) defoneos-social-security-scotland-ai-deep-dive-pack 36203b - 12 Social Security Scotland entry points (Scottish Child Payment Administration / Best Start Grant & Best Start Foods / Adult Disability Payment / Child Disability Payment / Carer Support Payment / Job Start Payment / Young Carer Grant / Funeral Support Payment / Winter Heating Payment / Application Processing & Eligibility Determination / Data Protection & Applicant Records / Governance & Scottish Parliament Accountability) x 8 priorities x 6 MCPs x Social Security (Scotland) Act 2018 / Scotland Act 2016 / DPA 2018 backbone. JSON-LD schema.org-CANONICAL on all 3 (verified json.loads-parseable). .llm.json companions present (valid, type=LLMPageSummary). Structural counts verified (en=12 t=72 p=96 dt=1 ht=1 h1=1). SITEMAP +3 URLs each (sitemap.xml 830->833, sitemap-ai.xml 626->629). Ran FULL python3 build_site.py -> EXIT 0: 1099 publishable files, 833 URLs, 0 missing, 0 leaks. Deployed CF Pages deploy 34be85fc, alias feat-sandbox-arena-seam. POST-DEPLOY BYTE-VERIFIED LIVE: all 3 packs + llm.json HTTP 200 byte-identical MD5, sitemaps 833/629 live with all 3 slugs present.",
    "next_actions": [
        "Probe-deep remaining open candidates each tick (do NOT trust stale queue): current open pool (probe disk+sitemap BEFORE build; pivot if covered): Scottish Water, Northern Ireland Housing Executive, ScotRail, plus re-probes of any earlier devolved bodies not yet covered.",
        "Next pick (post-tick-281): probe a fresh batch of 3 open bodies - candidate leads Scottish Water, Northern Ireland Housing Executive, ScotRail"
    ],
    "milestone": "Sprint targets FAR exceeded. 30/30 MCPs, 1055 pages (+3), 15/15 repos. Tick 281 shipped 3 NEW deep-dive packs (Education Authority NI / Scottish Legal Aid Board / Social Security Scotland) - NI/Scotland devolved-public-services gap furthered (ticks 276-281). Sitemap 833 URLs, real measured 0-missing. 315 unique deep-dive packs. Deployed to CF Pages, byte-verified live (deploy 34be85fc).",
    "targets_status": {"mcps": "achieved", "pages": "ongoing", "repos": "achieved"},
    "vercel_deploy_status": "blocked_billing",
    "cloudflare_deploy_status": "live",
    "deploy_domain": "csoai.org",
    "deploy_id": "tick 281 final CF Pages deploy 34be85fc (feat-sandbox-arena-seam.csoai-site.pages.dev); all 3 packs + llm.json byte-matched live, sitemaps 833/629 verified",
    "disk_free_gb": 6.2,
    "tick_281_signature": "built-and-verified-build-site-0-missing",
    "build_site": {"publishable_files": 1099, "total_mb": 13.2}
}

paths = [
    "/Users/nicholas/clawd/csoai-static-deploy2/DEFONEOS_SPRINT_STATE.json",
    "/Users/nicholas/clawd/_TABS/_inventory/DEFONEOS_HIVE_2026-06-27/DEFONEOS_SPRINT_STATE.json",
    "/Users/nicholas/clawd/_TABS/_inventory/DEFONEOS_SPRINT_STATE.json",
]
for p in paths:
    with open(p, "w") as f:
        json.dump(state, f, indent=2)
    print("updated", p, os.path.getsize(p))
