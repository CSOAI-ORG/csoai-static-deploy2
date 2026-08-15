#!/usr/bin/env python3
"""
probe_ai_bots.py — verify each apex serves the kit to AI-crawler User-Agents
================================================================================

Run on RunPod (NOT Mac). AI crawlers may get different responses than human
browsers (WAF rules, content negotiation, geo-blocking). This script pretends
to be each bot and confirms:
  - HTTP 200 (not 403/429)
  - Content-Type is correct (text/plain, application/json, application/xml)
  - First 200 bytes of body are non-empty and start with the expected marker

Output: JSON written to the path in --out; console summary.

Usage:
  python3 probe_ai_bots.py \
    --apexes https://www.csoai.org,https://meok.ai,https://os.meok.ai \
    --out /workspace/probe-ai-bots-summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Iterable

try:
    import requests
except ImportError:
    print("pip install requests", file=sys.stderr)
    sys.exit(2)


# AI-bot User-Agent strings + expected content-type per path-type
# Sources: each vendor's published bot docs (Sept 2024 baseline)
BOTS = [
    ("GPTBot",
     "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/bot)"),
    ("ClaudeBot",
     "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"),
    ("PerplexityBot",
     "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot.html)"),
    ("Google-Extended",
     "Mozilla/5.0 (compatible; Google-Extended/1.0)"),
    ("CCBot",
     "Mozilla/5.0 (compatible; CCBot/2.0; +https://commoncrawl.org/big-data/big-data.html)"),
    ("OAI-SearchBot",
     "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)"),
    ("Applebot-Extended",
     "Mozilla/5.0 (compatible; Applebot-Extended/1.0)"),
    ("DuckAssistBot",
     "Mozilla/5.0 (compatible; DuckAssistBot/1.0; +https://duckduckgo.com/duckassistbot)"),
    ("Amazonbot",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Amazonbot/0.1 (+https://developer.amazon.com/support/amazonbot)"),
    ("Meta-ExternalAgent",
     "Mozilla/5.0 (compatible; Meta-ExternalAgent/1.1; +https://developers.facebook.com/docs/sharing/webmasters/crawler)"),
    ("DeepSeekBot",
     "Mozilla/5.0 (compatible; DeepSeekBot/1.0; +https://deepseek.com/bot)"),
    ("Cohere-AI",
     "Mozilla/5.0 (compatible; Cohere-AI/1.0; +https://cohere.com/bot)"),
]


# Paths the kit exposes + their expected content-type + first-byte marker
PATHS = [
    ("/llms.txt",                              "text/plain",        "# llms.txt —"),
    ("/llms-full.txt",                         "text/plain",        "# llms-full.txt —"),
    ("/robots.txt",                            "text/plain",        "User-agent:"),
    ("/sitemap.xml",                           "application/xml",   "<?xml"),
    ("/sitemap-ai.xml",                        "application/xml",   "<?xml"),
    ("/agents.txt",                            "text/plain",        "# agents.txt —"),
    ("/.well-known/llm-manifest.json",         "application/json",  '{"'),
    ("/.well-known/ai-plugin.json",            "application/json",  '{"'),
    ("/.well-known/llm-policy.txt",           "text/plain",        "User-agent:"),
    ("/.well-known/security.txt",              "text/plain",        "Contact:"),
    ("/.well-known/change-log.txt",            "text/plain",        "# change-log.txt"),
    ("/.well-known/agent-card.json",           "application/json",  '{"'),
]


@dataclass
class Probe:
    apex: str
    bot: str
    path: str
    status: int = 0
    content_type: str = ""
    first_bytes: str = ""
    expected_type: str = ""
    expected_marker: str = ""
    ok_status: bool = False
    ok_type: bool = False
    ok_marker: bool = False
    error: str = ""


def probe(apex: str, path: str, ua: str, expected_type: str,
          expected_marker: str, timeout: float = 10.0,
          retries: int = 1) -> Probe:
    p = Probe(apex=apex, bot=ua.split("(")[-1].split(";")[0].strip(),
              path=path, expected_type=expected_type,
              expected_marker=expected_marker)
    url = apex.rstrip("/") + path
    headers = {"User-Agent": ua, "Accept": "*/*"}
    last_err = ""
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, headers=headers, timeout=timeout,
                             allow_redirects=True)
            p.status = r.status_code
            p.content_type = r.headers.get("Content-Type", "").split(";")[0].strip()
            p.first_bytes = r.text[:200] if r.text else ""
            p.ok_status = r.ok
            p.ok_type = expected_type in p.content_type
            p.ok_marker = p.first_bytes.startswith(expected_marker)
            if r.ok:
                return p
        except requests.RequestException as e:
            last_err = str(e)
        time.sleep(0.5 * (2 ** attempt))
    p.error = last_err
    return p


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apexes", default="https://www.csoai.org,https://meok.ai,https://os.meok.ai")
    p.add_argument("--out", default="/workspace/probe-ai-bots-summary.json")
    p.add_argument("--timeout", type=float, default=10.0)
    args = p.parse_args()

    apexes = [a.strip() for a in args.apexes.split(",") if a.strip()]
    probes: list[Probe] = []
    total = len(apexes) * len(PATHS) * len(BOTS)
    print(f"[probe] {total} probes across {len(apexes)} apexes × "
          f"{len(PATHS)} paths × {len(BOTS)} bots", flush=True)

    for apex in apexes:
        for path, etype, marker in PATHS:
            for bot_name, ua in BOTS:
                r = probe(apex, path, ua, etype, marker, timeout=args.timeout)
                probes.append(r)
                status_icon = "✓" if (r.ok_status and r.ok_type and r.ok_marker) else "✗"
                print(f"  {status_icon} {apex:25} {bot_name:18} {path:40} "
                      f"→ HTTP {r.status} ({r.content_type})", flush=True)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "apexes": apexes,
        "bots": [name for name, _ in BOTS],
        "paths": [p for p, _, _ in PATHS],
        "total_probes": len(probes),
        "ok_status": sum(1 for r in probes if r.ok_status),
        "ok_type": sum(1 for r in probes if r.ok_type),
        "ok_marker": sum(1 for r in probes if r.ok_marker),
        "probes": [asdict(r) for r in probes],
    }

    with open(args.out, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n[probe] {summary['ok_status']}/{summary['total_probes']} HTTP 200")
    print(f"[probe] {summary['ok_type']}/{summary['total_probes']} correct content-type")
    print(f"[probe] {summary['ok_marker']}/{summary['total_probes']} correct first-byte marker")
    print(f"[probe] summary written to {args.out}")

    # Exit non-zero if any tier-1 path returns non-200 to any bot
    failures = [r for r in probes if not r.ok_status]
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())