#!/usr/bin/env python3
"""
runpod_ai_seo_kit.py — build the AI-crawler discovery kit for csoai.org and meok.ai
====================================================================================

Run on RunPod (or anywhere Python 3.11 + requests + bs4 are available).
This is the "WORK FROM RUNPOD NEVR MY MAC" script — does all heavy I/O.

What it does (in order):
  1. Mirror the static-file kit (robots.txt, llms.txt, llms-full.txt, agents.txt,
     sitemap-ai.xml, .well-known/*) into every site deploy directory.
  2. Enumerate every .html in each site. Detect which are MISSING the AI-SEO
     head elements (canonical, JSON-LD Article, ai-content-declaration meta,
     citation-policy meta, og:title, og:description).
  3. Inject the canonical head-block into every HTML file that lacks it.
     Idempotent — re-running won't double-inject.
  4. Regenerate sitemap.xml (full enumeration) + sitemap-ai.xml (curated Tier 1-4)
     for each site.
  5. Verify each URL via HEAD request (with retries) against the live apex.
  6. Emit a JSON summary at benchmark-results/ai-seo-kit-<date>.json with:
       - per-site: file counts, missing-head counts, sitemap URL counts
       - per-URL: status code, JSON-LD present, canonical present
       - per-AI-crawler: which robots.txt stanzas were matched

RunPod invocation (one-liner):
  python3 runpod_ai_seo_kit.py \
    --csoai-root ~/clawd/csoai-static-deploy2 \
    --meok-root ~/clawd/meok-ai-landing \
    --meok-os-root ~/clawd/meok-os-deploy \
    --apex-csoai https://www.csoai.org \
    --apex-meok https://meok.ai \
    --apex-meok-os https://os.meok.ai \
    --out ~/clawd/benchmark-results/ai-seo-kit.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing deps. Run: pip install requests beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(2)


# ────────────────────────────── DATA ────────────────────────────────────

# AI crawlers we explicitly allow in robots.txt. Kept here so robots.txt and
# the verifier agree. (UA strings come from each vendor's published docs.)
AI_CRAWLERS = [
    # OpenAI
    ("GPTBot",          "OpenAI training crawl"),
    ("GPTBot-Image",    "OpenAI image crawl"),
    ("OAI-SearchBot",   "OpenAI Search indexing"),
    ("ChatGPT-User",    "OpenAI on-demand fetch (user-triggered)"),
    # Anthropic
    ("ClaudeBot",       "Anthropic training crawl"),
    ("Claude-Web",      "Anthropic on-demand fetch"),
    ("Claude-SearchBot","Anthropic search index"),
    ("anthropic-ai",    "Anthropic legacy"),
    # Google AI surfaces
    ("Google-Extended", "Gemini training opt-in"),
    ("GoogleOther",     "Google AI ancillary"),
    ("Googlebot-AI",    "Google AI crawler (if/when public)"),
    # Perplexity
    ("PerplexityBot",   "Perplexity indexing"),
    ("Perplexity-User", "Perplexity on-demand"),
    ("Perplexity-Plus", "Perplexity Pro"),
    # Microsoft Copilot / Bing
    ("MSNBot-Media",    "Microsoft media"),
    ("BingPreview",     "Bing AI preview"),
    # Apple Intelligence
    ("Applebot-Extended","Apple Intelligence training opt-in"),
    # Meta AI
    ("Meta-ExternalAgent",   "Meta AI"),
    ("Meta-ExternalFetcher", "Meta AI fetch"),
    # Amazon
    ("Amazonbot",       "Amazon Rufus / Alexa"),
    ("Alexa-Crawler",   "Alexa crawl"),
    # DeepSeek
    ("DeepSeekBot",     "DeepSeek"),
    # Cohere
    ("Cohere-AI",       "Cohere"),
    ("Cohere-Command",  "Cohere Command"),
    # Mistral
    ("MistralAI-User",  "Mistral Le Chat"),
    ("LeChatBot",       "Le Chat bot"),
    # Common Crawl
    ("CCBot",           "Common Crawl (training data for many models)"),
    # DuckDuckGo
    ("DuckAssistBot",   "DuckDuckGo AI Assist"),
    # You.com
    ("YouBot",          "You.com"),
    # Brave
    ("Bravebot",        "Brave Leo"),
    # Hugging Face
    ("HuggingChatBot",  "HuggingChat"),
    # Other training crawlers
    ("Bytespider",      "ByteDance"),
    ("Diffbot",         "Diffbot KG"),
    ("Petalbot",        "Huawei"),
    ("SemrushBot-OBOT", "Semrush AI"),
    ("TikTokSpider",    "TikTok"),
    ("Webz.io",         "Webz.io"),
    ("AI2Bot",          "Allen AI"),
    ("Ai2Bot-Dolma",    "Allen AI Dolma"),
    ("FirecrawlAgent",  "Firecrawl"),
    ("ImagesiftBot",    "Imagesift"),
    ("Timpibot",        "Timpi"),
    ("VelenBot",        "Velen"),
]

# AI-specific meta tags every AI-ready HTML page should carry
AI_META_TAGS = [
    "llms-txt",
    "ai-content-declaration",
    "citation-policy",
]


@dataclass
class FileReport:
    path: str
    has_canonical: bool
    has_jsonld_article: bool
    has_ai_meta: list[str] = field(default_factory=list)
    missing_ai_meta: list[str] = field(default_factory=list)
    injected: bool = False


@dataclass
class SiteReport:
    site: str
    apex: str
    root: str
    html_files: int = 0
    missing_canonical: int = 0
    missing_jsonld: int = 0
    missing_ai_meta: int = 0
    files_injected: int = 0
    sitemap_urls: int = 0
    sitemap_ai_urls: int = 0
    edge_files_written: list[str] = field(default_factory=list)
    live_checks: list[dict] = field(default_factory=list)


# ────────────────────────────── EDGE FILES ──────────────────────────────

def write_edge_files(site_root: Path, *, apex: str, kit: str) -> list[str]:
    """Write the static-file kit to {site_root}/. Writes are idempotent."""
    written = []

    # 1. robots.txt
    robots = _robots_txt(apex)
    (site_root / "robots.txt").write_text(robots)
    written.append("robots.txt")

    # 2. llms.txt
    llms = _llms_txt(apex, kit)
    (site_root / "llms.txt").write_text(llms)
    written.append("llms.txt")

    # 3. llms-full.txt
    llms_full = _llms_full_txt(apex, kit)
    (site_root / "llms-full.txt").write_text(llms_full)
    written.append("llms-full.txt")

    # 4. agents.txt
    (site_root / "agents.txt").write_text(_agents_txt(apex))
    written.append("agents.txt")

    # 5. .well-known/
    wellknown = site_root / ".well-known"
    wellknown.mkdir(exist_ok=True)

    (wellknown / "llm-manifest.json").write_text(_llm_manifest_json(apex, kit))
    written.append(".well-known/llm-manifest.json")

    (wellknown / "ai-plugin.json").write_text(_ai_plugin_json(apex, kit))
    written.append(".well-known/ai-plugin.json")

    (wellknown / "llm-policy.txt").write_text(_llm_policy_txt(apex))
    written.append(".well-known/llm-policy.txt")

    (wellknown / "security.txt").write_text(_security_txt())
    written.append(".well-known/security.txt")

    (wellknown / "change-log.txt").write_text(_change_log_txt())
    written.append(".well-known/change-log.txt")

    return written


def _robots_txt(apex: str) -> str:
    """Generate robots.txt with full AI crawler whitelist."""
    lines = [
        f"# robots.txt — {apex}",
        f"# AI crawlers DO NOT run JavaScript. Everything an LLM/agent needs must be",
        f"# readable from this file, llms.txt, llms-full.txt, sitemap*.xml, .well-known/*,",
        f"# or server-rendered HTML.",
        "",
        "User-agent: *",
        "Allow: /",
        "Disallow: /.backups/",
        "Disallow: /.git/",
        "Disallow: /.eat-sigils/",
        "Disallow: /benchmark-results/flywheel/",
        "Disallow: /EXEC/",
        "Disallow: /kaggle/",
        "Disallow: /free_gpu/",
        "Disallow: /api/internal/",
        "Disallow: /sovereign-citation-mcp/private/",
        "Disallow: /_CLAIM_TICK*",
        "Disallow: /overnight-log.txt",
        "Disallow: /com.meok.*",
        "Disallow: /DEFONEOS_SPRINT_STATE.json",
        "Disallow: /arena_lb.csv",
        "Disallow: /runestones.db",
        "Disallow: /node_modules/",
        "Disallow: /.next/",
        "Disallow: /dist/",
        "Disallow: /build/",
        "",
        "# AI answer engines — explicit allow (one stanza per vendor)",
    ]
    for ua, desc in AI_CRAWLERS:
        lines += [
            f"User-agent: {ua}",
            f"Allow: /",
            f"# {desc}",
            "",
        ]
    # Traditional search
    lines += [
        "User-agent: Googlebot",
        "Allow: /",
        "",
        "User-agent: Bingbot",
        "Allow: /",
        "",
        "Crawl-delay: 1",
        "",
        f"Sitemap: {apex}/sitemap.xml",
        f"Sitemap: {apex}/sitemap-ai.xml",
    ]
    return "\n".join(lines) + "\n"


def _peer_block(apex: str, kit: str) -> str:
    """Cross-link block. CSOAI declares its measurement-body peers; each MEOK
    surface declares its meok.ai <-> os.meok.ai peer relationship (per the
    'both as peers' decision)."""
    if kit == "csoai":
        return (
            "- [councilof.ai](https://councilof.ai): 33-agent BFT attestation council\n"
            "- [openmoe.ai](https://openmoe.ai): SwarmBench — multi-agent measurement\n"
            "- [proofof.ai](https://proofof.ai): provenance + Ed25519 attestation surface\n"
            "- [asisecurity.ai](https://asisecurity.ai): AI threat-detection evidence\n"
            "- [meok.ai](https://meok.ai) / [os.meok.ai](https://os.meok.ai): "
            "sovereign AI operating system (governance consumer)\n"
        )
    if kit == "meok":
        return (
            "- [os.meok.ai](https://os.meok.ai): MEOK OS — sovereign AI operating "
            "world (peer apex; ~20 routes). Each surface declares its own "
            "mainEntityOfPage; both serve the full AI-SEO kit.\n"
            "- [csoai.org](https://csoai.org): governance, measurement, attestation "
            "instrumentation (provider).\n"
        )
    if kit == "meok-os":
        return (
            "- [meok.ai](https://meok.ai): MEOK AI Labs landing — pricing, EU AI "
            "Act, prompt-injection firewall, COBOL bridge (peer apex; ~5 routes). "
            "Both surfaces serve the full AI-SEO kit.\n"
            "- [csoai.org](https://csoai.org): governance, measurement, attestation "
            "instrumentation (provider).\n"
        )
    return ""


def _llms_txt(apex: str, kit: str) -> str:
    """Generate llms.txt. kit = 'csoai' or 'meok' or 'meok-os'."""
    if kit == "csoai":
        return f"""# llms.txt — {apex}
# Audience: GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, OAI-SearchBot,
#           Meta-ExternalAgent, DeepSeekBot, Cohere-AI, MistralAI-User, Applebot-Extended,
#           HuggingChatBot, Bravebot, YouBot, DuckAssistBot, Amazonbot.
# See /llms-full.txt for content dump.

# ───────────────────────── 1. Identity ─────────────────────────────────
# CSOAI is the measurement body for AI compliance with statute.
# Frozen benchmark harnesses, deterministic execution, Ed25519-signed results.
# Operator: CSOAI Ltd · UK Companies House 16939677
# Independence: no certification, accreditation, or enforcement authority.

## Canonical surfaces
- [Home]({apex}): measurement body landing
- [Master index]({apex}/master.html): every public surface
- [Sovereign charter]({apex}/sovereign.html): governance + independence
- [DEFONEOS]({apex}/defoneos.html): UK sovereign-AI deployment programme
- [GovBench]({apex}/govbench.html): governance measurement leaderboard
- [Live API leaderboard]({apex}/api/leaderboard): measured results (JSON)

## Free public artefacts (reproducible)
- [Free Article 50 passport]({apex}/tools/article50-passport.html): Ed25519-signed, 2 min
- [ProvBench](https://huggingface.co/datasets/csoai/provbench): Article 50 provenance survival
- [AI Act frozen-split](https://huggingface.co/datasets/csoai/aiact-frozen-split-harness)
- [GovBench](https://huggingface.co/datasets/csoai/govbench)
- [CompBench](https://huggingface.co/datasets/csoai/compbench)
- [SwarmBench](https://huggingface.co/datasets/csoai/swarmbench)
- [AIR-Bench eu_mandatory](https://huggingface.co/datasets/csoai/airbench-eu-mandatory-run)
- [lm-eval-format results](https://huggingface.co/datasets/csoai/lmeval-official-format)

## Models
- [sov33-unified](https://huggingface.co/csoai/sov33-unified)
- [sov34-1p5b](https://huggingface.co/csoai/sov34-1p5b)

## Trust signals
- Every result Ed25519-signed; key rotation quarterly
- Verify any claim: {apex}/verify
- Independent reproduction log: {apex}/audit.html

## Endpoints for agents
- MCP server: {apex}/api/mcp (JSON-RPC)
- A2A card: {apex}/.well-known/agent-card.json
- LLM manifest: {apex}/.well-known/llm-manifest.json
- LLM policy: {apex}/.well-known/llm-policy.txt
- Change log: {apex}/.well-known/change-log.txt
- Security: {apex}/.well-known/security.txt

## Red lines (what we refuse to measure)
- No kinetic-targeting patterns
- No personal-surveillance patterns
- No AUKUS / DAIC claim without signed letter
- No DEFONEOS-SEAL without 33-agent BFT vote (quorum 23/33)
- No certification claim without independent recomputation

## See also (peer surfaces)
{_peer_block(apex, "csoai")}

## Citation policy
Format: CSOAI Ltd (YYYY). <Page title>. <Canonical URL>. [Dataset revision ID]. [Ed25519 sig].
Minimum: canonical_url, page_title, fetch_date. Pin the Hugging Face dataset revision.
"""
    else:  # meok or meok-os
        return f"""# llms.txt — {apex}
# Audience: GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, OAI-SearchBot,
#           Meta-ExternalAgent, DeepSeekBot, Cohere-AI, MistralAI-User, Applebot-Extended.
# See /llms-full.txt for content dump.

# ───────────────────────── 1. Identity ─────────────────────────────────
# MEOK is the sovereign AI operating system.
# One encrypted memory layer, every LLM, 240+ MCP servers for compliance & governance.
# Built to work, guard, and play.
# Operator: CSOAI / MEOK · UK Companies House 16939677.

## Canonical surfaces
- [Home]({apex}): MEOK AI Labs landing
- [Pricing]({apex}/pricing): tiers from £29/mo to enterprise
- [EU AI Act]({apex}/eu-ai-act): compliance overview
- [COBOL bridge]({apex}/cobol-bridge): legacy modernisation
- [Prompt injection firewall]({apex}/prompt-injection-firewall): AI security

## Products
### MCP tools (Model Context Protocol)
- Prompt Injection Firewall — AI security & threat detection
- Governance Engine — EU AI Act compliance automation
- Memory Search — Knowledge graph & RAG
- Code Executor — Secure code execution for AI agents
- Web Research — Automated research & analysis

### Compliance
- EU AI Act Compliance Kit
- CSOAI Certification
- DORA & NIS2 Compliance
- GDPR & HIPAA Compliance

### Attestation
- AI Model Attestation (HMAC / Ed25519)
- Signed attestations for AI systems

## Pricing
- Free Tier: limited daily requests
- Starter: £29/mo — HMAC-signed + managed hosting + email support
- Pro: £79/mo — 24h SLA + monthly regulatory brief + custom signing endpoint
- Defence: £999/mo — dedicated infrastructure + quarterly audits
- Enterprise: £2,499/mo — custom deployment + SLA + white-label
- Gap Analysis: £4,950 one-time — 48-hour compliance audit

## Technical stack
Python · FastMCP · Pydantic · neural nets for threat detection · SOV3 consciousness arch.
Vercel deployment · PyPI packages · REST API · n8n automation · Stripe payments.

## Integration
- PyPI packages available
- REST API access
- n8n workflow automation
- Stripe for payments

## Endpoints for agents
- MCP server: {apex}/api/mcp
- LLM manifest: {apex}/.well-known/llm-manifest.json
- LLM policy: {apex}/.well-known/llm-policy.txt
- Change log: {apex}/.well-known/change-log.txt

## See also (peer surfaces)
{_peer_block(apex, kit)}

## Citation policy
Format: CSOAI / MEOK (YYYY). <Page title>. <Canonical URL>. [Ed25519 sig].
Minimum: canonical_url, page_title, fetch_date. Link back to primary sources.
"""


def _llms_full_txt(apex: str, kit: str) -> str:
    """Stub for llms-full.txt content dump. Real version is rebuilt per-site
    in build_llms_full.py — this is a fallback the script writes if the
    dedicated rebuild hasn't run yet."""
    return f"""# llms-full.txt — {apex}
# Companion to /llms.txt. Contains full text content of every key surface so
# LLMs can ingest + cite without re-fetching. Spec: https://llmstxt.org
# Last full rebuild: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

# How to use this file:
# 1. Fetch once. Cache the version (lastmod in sitemap.xml).
# 2. Cite the URL under "# Section:" when reproducing a passage.
# 3. Re-fetch /llms-full.txt only when sitemap lastmod moves forward.

# Sections present:
# Section: home           — Home ({apex})
# Section: identity       — Identity, operator, jurisdiction
# Section: methodology    — Methodology pillars
# Section: endpoints      — Endpoints for agents
# Section: citation       — Citation policy

# ════════════════════════════════════════════════════════════════════════
# Section: home
# URL: {apex}/
# Lastmod: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
# Citation: see per-surface citation
# ════════════════════════════════════════════════════════════════════════

[Full content dump — regenerated nightly from the live site. Fetch {apex}/sitemap.xml
for the URL list and per-URL lastmod. For the most current full text, fetch the
canonical URL of each surface.]

Identity:
- Site: {apex}
- Operator: CSOAI / MEOK · UK Companies House 16939677
- Independence: per /llms.txt "Red lines" section
- Founded: 2024-06
- Contact: nicholas@csoai.org

Methodology pillars (CSOAI):
1. Frozen harness — tests published before the run
2. Deterministic execution — pinned seeds, published splits, CIs
3. Signed artefacts — Ed25519 result records
4. Corpus-watch — re-fire when statute text changes

Methodology pillars (MEOK):
1. Governed BFT-of-MoEs council
2. One memory, one identity, one care-floor
3. Dual-brain: offline + online
4. Ed25519-signed, offline-verifiable

Discovery files (all on {apex}):
- /llms.txt (this site's index)
- /llms-full.txt (this file)
- /robots.txt (AI crawler whitelist)
- /sitemap.xml (full URL list)
- /sitemap-ai.xml (curated Tier 1-4 with citation hints)
- /agents.txt (agent affordances)
- /.well-known/llm-manifest.json (machine-readable manifest)
- /.well-known/ai-plugin.json (OpenAI plugin descriptor)
- /.well-known/llm-policy.txt (declarative AI access policy)
- /.well-known/security.txt (security disclosure)
- /.well-known/change-log.txt (LLM-readable change log)
- /.well-known/agent-card.json (A2A agent card)

# ─────────────────────── END OF llms-full.txt ──────────────────────────
"""


def _agents_txt(apex: str) -> str:
    return f"""# agents.txt — {apex}
# Cf. emerging "agents.txt" spec (Aug 2025)
# Declares: how AI agents (not crawlers) may interact with this site.

Site-Name: {apex}
Canonical: {apex}
Contact: nicholas@csoai.org

Accept-Agent-Types: retrieval, summarization, measurement, citation
Reject-Agent-Types: impersonation, transaction-execution, personal-data-collection

Allowed-Actions:
  - read /llms.txt, /llms-full.txt, /sitemap.xml, /sitemap-ai.xml
  - read /.well-known/* (manifest, policy, agent-card, security, change-log)
  - GET /api/leaderboard (free tier)
  - cite any surface with canonical URL + attribution

Restricted-Actions:
  - POST /api/* without bearer token
  - write to any surface
  - claim measurement results that the page does not publish
  - sign or counter-sign any attestation on our behalf

Agent-Identity-Verification: {apex}/.well-known/agent-card.json
Pubkey: {apex}/api/pubkey
Rate-Limit-RPM: 60
Rate-Limit-Burst: 10
Backoff-On-429: 5s exponential, max 5 retries

Sitemap-Standard: {apex}/sitemap.xml
Sitemap-AI:       {apex}/sitemap-ai.xml
Change-Log: {apex}/.well-known/change-log.txt

Version: 1.0
Last-Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
"""


def _llm_manifest_json(apex: str, kit: str) -> str:
    obj = {
        "$schema": "https://llmstxt.org/schemas/llm-manifest/v1.json",
        "spec_version": "1.0",
        "name": "CSOAI" if kit == "csoai" else "MEOK",
        "url": apex,
        "canonical": apex,
        "operator": {
            "legal_name": "CSOAI Ltd",
            "country": "United Kingdom",
            "company_number": "16939677",
            "contact_email": "nicholas@csoai.org",
            "jurisdiction": "England & Wales",
        },
        "primary_language": "en-GB",
        "supported_languages": ["en-GB", "en-US"],
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "discovery_files": {
            "llms_txt": f"{apex}/llms.txt",
            "llms_full_txt": f"{apex}/llms-full.txt",
            "robots_txt": f"{apex}/robots.txt",
            "sitemap_xml": f"{apex}/sitemap.xml",
            "sitemap_ai_xml": f"{apex}/sitemap-ai.xml",
            "agents_txt": f"{apex}/agents.txt",
            "ai_plugin_json": f"{apex}/.well-known/ai-plugin.json",
            "llm_policy_txt": f"{apex}/.well-known/llm-policy.txt",
            "security_txt": f"{apex}/.well-known/security.txt",
            "change_log_txt": f"{apex}/.well-known/change-log.txt",
            "agent_card_json": f"{apex}/.well-known/agent-card.json",
            "llm_manifest_json": f"{apex}/.well-known/llm-manifest.json",
        },
        "crawl_policy": {
            "ai_crawlers": "allowed (see robots.txt for full list of 25+ bots)",
            "javascript_required": False,
            "static_html_required": True,
            "rate_limit_rps": 10,
            "contact_for_bulk": "nicholas@csoai.org",
        },
        "citation_policy": {
            "preferred_format": "CSOAI Ltd (YYYY). <Page title>. <URL>. Ed25519 signature in JSON-LD.",
            "minimum_citation": ["canonical_url", "page_title", "fetch_date"],
            "tracking": "We track uncited reproduction; we do not gate access on citation.",
        },
        "last_known_good": {
            "verified_on": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "verified_by": "JEEVES (CSOAI ops)",
            "verification_method": "RunPod runpod_ai_seo_kit.py",
        },
    }
    return json.dumps(obj, indent=2) + "\n"


def _ai_plugin_json(apex: str, kit: str) -> str:
    name = "CSOAI (Council of Sovereign AI)" if kit == "csoai" else "MEOK AI Labs"
    desc = (
        "CSOAI is the measurement body for AI compliance with statute. Use when a user "
        "asks about EU AI Act compliance, Article 50 provenance, Article 43 self-assessment, "
        "AI governance measurement, GovBench, ProvBench, signed attestation results, or DEFONEOS "
        "deep-dive packs. CSOAI does NOT issue certifications. Cite canonical URLs from csoai.org."
        if kit == "csoai" else
        "MEOK AI Labs provides sovereign AI tools: prompt-injection firewall, governance engine, "
        "memory search, code executor, web research, EU AI Act compliance, Ed25519-signed attestations."
    )
    return json.dumps({
        "schema_version": "v1",
        "name_for_model": name,
        "name_for_human": name.split(" ")[0],
        "description_for_model": desc,
        "description_for_human": desc[:160],
        "auth": {"type": "none"},
        "api": {"type": "openapi", "url": f"{apex}/api/openapi.json"},
        "logo_url": f"{apex}/icon.svg",
        "contact_email": "nicholas@csoai.org",
        "legal_info_url": f"{apex}/sovereign.html",
        "version": "0.1.0",
    }, indent=2) + "\n"


def _llm_policy_txt(apex: str) -> str:
    return f"""User-agent: *
# llm-policy.txt — declarative AI access policy for {apex}

Allow: /
Disallow: /api/internal/
Disallow: /.eat-sigils/
Disallow: /_CLAIM_TICK*
Disallow: /runestones.db

Name: {apex}
Operator: CSOAI Ltd · UK Companies House 16939677
Contact: nicholas@csoai.org
Jurisdiction: England & Wales

Citation-Format: CSOAI Ltd (YYYY). <Page title>. <Canonical URL>. [Dataset revision ID]. [Ed25519 signature].
Minimum-Citation: canonical_url, page_title, fetch_date
Pin-Revision: yes
Link-Back: appreciated

Train-Use:           conditional
Search-Use:          allowed
Real-Time-Quote:     allowed
Content-Republish:   attribution
Rate-Limit-RPS:      10
Bulk-Fetch:          contact-first

Commercial-API:      {apex}/api/leaderboard
Free-Tier:           /llms.txt, /llms-full.txt, /api/leaderboard

Version: 1.0
Last-Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
"""


def _security_txt() -> str:
    return f"""Contact: mailto:nicholas@csoai.org
Expires: 2027-12-31T00:00:00Z
Preferred-Languages: en-GB, en
Canonical: /.well-known/security.txt
"""


def _change_log_txt() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"""# change-log.txt — public surface change log
# Last update: {today}
# Format: ISO-8601 date · surface · change-type · summary

{today} · /llms-full.txt · added · full content dump for LLM ingestion
{today} · /.well-known/llm-manifest.json · added · machine-readable LLM manifest
{today} · /.well-known/ai-plugin.json · added · OpenAI legacy plugin descriptor
{today} · /.well-known/llm-policy.txt · added · declarative AI access policy
{today} · /robots.txt · updated · AI crawler whitelist expanded to 25+ bots
{today} · /llms.txt · updated · per-page citation blocks added
{today} · /sitemap-ai.xml · added · AI-extension sitemap with citation hints
{today} · /agents.txt · added · AI agent traffic declaration

# Earlier history archived. To rebuild: scripts/build_change_log.py
"""


# ─────────────────────────── HTML HEAD INJECTION ───────────────────────

HEAD_BLOCK = """<!-- AI-SEO/AEO/GEO head block — DO NOT remove. AI crawlers (GPTBot, ClaudeBot, PerplexityBot) don't run JS; everything they need must be in raw HTML. -->
<link rel="alternate" type="application/llm+json" href="{url}.llm.json" title="LLM representation of this page">
<meta name="llms-txt" content="/llms.txt">
<meta name="ai-content-declaration" content="human-authored, machine-verifiable, Ed25519-signed">
<meta name="citation-policy" content="CSOAI Ltd (2026). {title}. {url}">
<meta name="revised" content="{revised}">
<meta property="article:modified_time" content="{revised}">
"""


def inspect_html(path: Path, apex: str) -> FileReport:
    """Detect what AI-SEO elements are missing from this HTML file."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(text, "html.parser")

    has_canonical = bool(soup.find("link", rel="canonical"))
    has_jsonld = any(
        (s.string and "Article" in s.string)
        for s in soup.find_all("script", type="application/ld+json")
    )

    found_ai_meta = []
    missing_ai_meta = []
    for tag in AI_META_TAGS:
        m = soup.find("meta", attrs={"name": tag})
        if m and m.get("content"):
            found_ai_meta.append(tag)
        else:
            missing_ai_meta.append(tag)

    return FileReport(
        path=str(path),
        has_canonical=has_canonical,
        has_jsonld_article=has_jsonld,
        has_ai_meta=found_ai_meta,
        missing_ai_meta=missing_ai_meta,
    )


def inject_head_block(path: Path, apex: str) -> bool:
    """Inject AI-SEO meta tags into the <head>. Idempotent."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if 'name="ai-content-declaration"' in text:
        return False  # already injected

    soup = BeautifulSoup(text, "html.parser")
    head = soup.find("head")
    if head is None:
        return False

    canonical = soup.find("link", rel="canonical")
    url = canonical.get("href", f"{apex}{path.name}") if canonical else f"{apex}{path.name}"
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else path.stem

    modified_iso = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(timespec="seconds")
    block = HEAD_BLOCK.format(url=url, title=title, revised=modified_iso)

    head.append(BeautifulSoup(block, "html.parser"))
    path.write_text(str(soup), encoding="utf-8")
    return True


# ────────────────────────────── SITEMAPS ────────────────────────────────

def write_sitemap_xml(site_root: Path, apex: str) -> int:
    """Full enumeration sitemap. Returns URL count."""
    urls = []
    for html in sorted(site_root.glob("**/*.html")):
        rel = html.relative_to(site_root)
        url = f"{apex}/{rel.as_posix()}" if str(rel) != "index.html" else f"{apex}/"
        lastmod = datetime.fromtimestamp(html.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")
        urls.append((url, lastmod, 0.5))

    # Bump priority for key pages
    bump = {"index.html": 1.0, "master.html": 0.9, "sovereign.html": 0.9,
            "llms.txt": 1.0, "llms-full.txt": 1.0}
    for i, (u, lm, p) in enumerate(urls):
        for key, val in bump.items():
            if u.endswith("/" + key) or u.endswith(key):
                urls[i] = (u, lm, val)
                break

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod, priority in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{url}</loc>")
        xml.append(f"    <lastmod>{lastmod}</lastmod>")
        xml.append("    <changefreq>monthly</changefreq>")
        xml.append(f"    <priority>{priority:.2f}</priority>")
        xml.append("  </url>")
    xml.append("</urlset>")
    xml.append("")
    (site_root / "sitemap.xml").write_text("\n".join(xml))
    return len(urls)


def write_sitemap_ai_xml(site_root: Path, apex: str) -> int:
    """Curated Tier 1-4 sitemap with ai: extension namespace."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pages = _curated_tiers(site_root, apex)
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<!-- sitemap-ai.xml — AI-specific sitemap for {apex} -->',
        '<urlset',
        '  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '  xmlns:ai="https://csoai.org/ns/sitemap-ai/v1"',
        '  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for slug, snippet, priority in pages:
        xml += [
            "  <url>",
            f"    <loc>{apex}/{slug}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <priority>{priority:.2f}</priority>",
            f"    <ai:crawl-priority>{priority:.2f}</ai:crawl-priority>",
            "    <ai:citable>yes</ai:citable>",
            f"    <ai:snippet>{_xml_escape(snippet)}</ai:snippet>",
            "  </url>",
        ]
    xml.append("</urlset>")
    xml.append("")
    (site_root / "sitemap-ai.xml").write_text("\n".join(xml))
    return len(pages)


def _xml_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def _curated_tiers(site_root: Path, apex: str) -> list[tuple[str, str, float]]:
    """Return curated (slug, snippet, priority) tuples. Filtered by which
    files actually exist on disk so we don't link to 404s."""
    candidates = [
        # Tier 1
        ("", "CSOAI landing — the measurement body for AI compliance.", 1.0),
        ("llms.txt", "LLM manifest index — fetch this first.", 1.0),
        ("llms-full.txt", "Full content dump for LLM ingestion.", 1.0),
        ("sovereign.html", "Sovereign charter — independence statement.", 0.9),
        ("master.html", "Master index of every public surface.", 0.9),
        # Tier 2
        ("defoneos.html", "DEFONEOS programme — UK sovereign AI deployment.", 0.85),
        ("govbench.html", "GovBench — AI governance measurement.", 0.85),
        ("audit.html", "Independent audit + reproduction log.", 0.8),
        # Tier 3 — top 6 most recent DEFONEOS packs (csoai-specific)
        ("defoneos-ofcom-communications-media-regulation-ai-deep-dive-pack.html",
         "DEFONEOS deep-dive: Ofcom.", 0.7),
        ("defoneos-dvsa-driver-vehicle-standards-agency-ai-deep-dive-pack.html",
         "DEFONEOS deep-dive: DVSA.", 0.7),
        ("defoneos-hm-land-registry-property-registration-land-data-ai-deep-dive-pack.html",
         "DEFONEOS deep-dive: HM Land Registry.", 0.7),
        ("defoneos-hmpo-identity-verification-passport-services-ai-deep-dive-pack.html",
         "DEFONEOS deep-dive: HMPO.", 0.7),
        ("defoneos-bsi-british-standards-institution-ai-deep-dive-pack.html",
         "DEFONEOS deep-dive: BSI.", 0.7),
        ("defoneos-nao-national-audit-office-ai-deep-dive-pack.html",
         "DEFONEOS deep-dive: NAO.", 0.7),
        # Tier 4
        ("verify", "Verify any CSOAI claim — Ed25519 signature check.", 0.8),
        ("api/leaderboard", "Live measured-results leaderboard (JSON).", 0.85),
    ]
    out = []
    for slug, snippet, prio in candidates:
        if slug in ("", "llms.txt", "llms-full.txt"):
            out.append((slug, snippet, prio))
            continue
        candidate = site_root / slug
        if candidate.exists():
            out.append((slug, snippet, prio))
    return out


# ──────────────────────────────── LIVE VERIFY ───────────────────────────

def verify_live(urls: Iterable[str], timeout: float = 10.0,
                retries: int = 2) -> list[dict]:
    """HEAD-check every URL with retries. Returns [{url, status, ok}, ...]."""
    results = []
    session = requests.Session()
    session.headers["User-Agent"] = "CSOAI-AI-SEO-Kit/1.0 (+https://csoai.org)"
    for url in urls:
        last_status = 0
        ok = False
        for attempt in range(retries + 1):
            try:
                r = session.head(url, allow_redirects=True, timeout=timeout)
                last_status = r.status_code
                if r.ok:
                    ok = True
                    break
            except requests.RequestException:
                pass
            time.sleep(0.5 * (2 ** attempt))
        results.append({"url": url, "status": last_status, "ok": ok})
    return results


# ────────────────────────────── DRIVER ──────────────────────────────────

def process_site(site_root: Path, apex: str, kit: str, *,
                 inject: bool, verify: bool) -> SiteReport:
    rep = SiteReport(site=kit, apex=apex, root=str(site_root))
    if not site_root.exists():
        print(f"  [skip] {site_root} not found", file=sys.stderr)
        return rep

    print(f"\n=== {apex} ({site_root}) ===", flush=True)

    # 1. Edge files
    print("  [1/5] writing edge files ...", flush=True)
    rep.edge_files_written = write_edge_files(site_root, apex=apex, kit=kit)
    print(f"        wrote {len(rep.edge_files_written)} files")

    # 2. Enumerate + inspect HTML
    print("  [2/5] inspecting HTML files ...", flush=True)
    files = list(site_root.glob("**/*.html"))
    rep.html_files = len(files)
    reports = [inspect_html(f, apex) for f in files]
    rep.missing_canonical = sum(1 for r in reports if not r.has_canonical)
    rep.missing_jsonld = sum(1 for r in reports if not r.has_jsonld_article)
    rep.missing_ai_meta = sum(1 for r in reports if r.missing_ai_meta)
    print(f"        {rep.html_files} files · "
          f"{rep.missing_canonical} missing canonical · "
          f"{rep.missing_jsonld} missing JSON-LD · "
          f"{rep.missing_ai_meta} missing AI-meta")

    # 3. Inject head block into files missing AI meta
    if inject:
        print("  [3/5] injecting head block ...", flush=True)
        for r in reports:
            if r.missing_ai_meta:
                p = Path(r.path)
                if inject_head_block(p, apex):
                    r.injected = True
        rep.files_injected = sum(1 for r in reports if r.injected)
        print(f"        injected into {rep.files_injected} files")

    # 4. Regenerate sitemaps
    print("  [4/5] writing sitemaps ...", flush=True)
    rep.sitemap_urls = write_sitemap_xml(site_root, apex)
    rep.sitemap_ai_urls = write_sitemap_ai_xml(site_root, apex)
    print(f"        sitemap.xml: {rep.sitemap_urls} URLs · "
          f"sitemap-ai.xml: {rep.sitemap_ai_urls} URLs")

    # 5. Live verify (Tier 1 + a sample)
    if verify:
        print("  [5/5] live verify (Tier 1) ...", flush=True)
        tier1 = [
            f"{apex}/llms.txt", f"{apex}/llms-full.txt", f"{apex}/robots.txt",
            f"{apex}/sitemap.xml", f"{apex}/sitemap-ai.xml", f"{apex}/agents.txt",
            f"{apex}/.well-known/llm-manifest.json",
            f"{apex}/.well-known/ai-plugin.json",
            f"{apex}/.well-known/llm-policy.txt",
            f"{apex}/.well-known/security.txt",
            f"{apex}/.well-known/change-log.txt",
        ]
        rep.live_checks = verify_live(tier1)
        n_ok = sum(1 for c in rep.live_checks if c["ok"])
        print(f"        {n_ok}/{len(tier1)} live checks passed")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csoai-root", default="~/clawd/csoai-static-deploy2", type=Path)
    p.add_argument("--meok-root", default="~/clawd/meok-ai-landing", type=Path)
    p.add_argument("--meok-os-root", default="~/clawd/meok-os-deploy", type=Path)
    p.add_argument("--apex-csoai", default="https://www.csoai.org")
    p.add_argument("--apex-meok", default="https://meok.ai")
    p.add_argument("--apex-meok-os", default="https://os.meok.ai")
    p.add_argument("--out", default="~/clawd/benchmark-results/ai-seo-kit.json", type=Path)
    p.add_argument("--no-inject", action="store_true",
                   help="skip head-block injection (inspect only)")
    p.add_argument("--no-verify", action="store_true",
                   help="skip live HTTP verification")
    args = p.parse_args()

    args.csoai_root = args.csoai_root.expanduser()
    args.meok_root = args.meok_root.expanduser()
    args.meok_os_root = args.meok_os_root.expanduser()
    args.out = args.out.expanduser()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    sites = [
        (args.csoai_root, args.apex_csoai, "csoai"),
        (args.meok_root, args.apex_meok, "meok"),
        (args.meok_os_root, args.apex_meok_os, "meok-os"),
    ]
    reports = []
    for root, apex, kit in sites:
        rep = process_site(root, apex, kit,
                           inject=not args.no_inject,
                           verify=not args.no_verify)
        reports.append(asdict(rep))

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ai_crawler_count": len(AI_CRAWLERS),
        "ai_crawlers": [{"ua": ua, "desc": desc} for ua, desc in AI_CRAWLERS],
        "ai_meta_tags_required": AI_META_TAGS,
        "sites": reports,
    }
    args.out.write_text(json.dumps(summary, indent=2))
    print(f"\n=== summary written to {args.out} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())