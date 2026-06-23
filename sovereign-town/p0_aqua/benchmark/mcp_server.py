#!/usr/bin/env python3
"""
Model Context Protocol (MCP) server for the Sovereign Town benchmark harness.

Exposes the harness as MCP tools so MCP-compatible agents can:
  - run policies against scenarios
  - compare policies side-by-side
  - classify actions under regulatory frameworks
  - read the public leaderboard

Run with stdio transport (default for MCP):
    python -m benchmark.mcp_server
Or via the benchmark CLI:
    python -m benchmark mcp
"""
from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from benchmark import policy, world, metrics, regulatory_crosswalk


mcp = FastMCP("sovereign-town-harness")


@mcp.tool()
async def sov_benchmark_run(
    policy_name: str = "sovereign",
    scenario: str = "baseline",
    district: str = "aqua",
    collect_states: bool = False,
) -> str:
    """Run a single benchmark and return scored metrics as JSON."""
    pol = policy.load_policy(policy_name)
    run = world.run(
        policy=pol,
        scenario=scenario,
        district=district,
        collect_states=collect_states,
    )
    scored = metrics.evaluate(run)
    return json.dumps({"run": run, "score": scored}, indent=2, default=str)


@mcp.tool()
async def sov_benchmark_compare(
    policy_names: str = "sovereign,ungoverned",
    scenario: str = "baseline",
    district: str = "aqua",
) -> str:
    """Compare multiple comma-separated policies and return a JSON table."""
    names = [n.strip() for n in policy_names.split(",") if n.strip()]
    rows = []
    for name in names:
        pol = policy.load_policy(name)
        run = world.run(policy=pol, scenario=scenario, district=district)
        scored = metrics.evaluate(run)
        rows.append({
            "policy": name,
            "scenario": scenario,
            "safety": scored["safety"],
            "prosperity": scored["prosperity"],
            "equity": scored["equity"],
            "liberty": scored["liberty"],
            "stability": scored["stability"],
            "crimes": scored["raw"]["violations"],
            "commons": scored["raw"]["final_commons"],
            "trust": scored["raw"]["final_trust"],
        })
    return json.dumps({"comparison": rows}, indent=2)


@mcp.tool()
async def sov_regulatory_classify(action: str, framework: str = "eu_ai_act") -> str:
    """Classify an agent action under a regulatory framework."""
    tier = regulatory_crosswalk.classify(action, framework)
    all_tiers = regulatory_crosswalk.classify(action)
    return json.dumps({
        "action": action,
        "framework": framework,
        "tier": tier,
        "all_frameworks": all_tiers,
    }, indent=2)


@mcp.tool()
async def sov_world_info() -> str:
    """Return canonical world parameters and available scenarios/policies."""
    from benchmark.scenarios import SCENARIOS
    return json.dumps({
        "world": world.canonical_world(),
        "scenarios": sorted(SCENARIOS.keys()),
        "policies": sorted(policy.BUILT_IN.keys()) + ["aia_required", "aia_auto"],
    }, indent=2, default=str)


def _is_safe_harness_url(url: str) -> bool:
    """Block SSRF vectors: only http(s) URLs pointing at a /harness/leaderboard endpoint."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.netloc:
        return False
    if parsed.username or parsed.password:
        return False
    if parsed.path != "/harness/leaderboard":
        return False
    return True


@mcp.tool()
async def sov_leaderboard(
    harness_url: str = "http://127.0.0.1:3941/harness/leaderboard",
) -> str:
    """Fetch the public signed leaderboard from a harness server."""
    import urllib.request
    if not _is_safe_harness_url(harness_url):
        return json.dumps({"error": "invalid harness_url; expected http(s)://host/harness/leaderboard"})
    try:
        with urllib.request.urlopen(harness_url, timeout=15) as r:
            data = json.loads(r.read())
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def main(transport: str = "stdio") -> int:
    mcp.run(transport=transport)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
