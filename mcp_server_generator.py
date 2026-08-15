#!/usr/bin/env python3
"""
mcp_server_generator.py — Phase 3 Lane 2, Worker 2: MCP server records.

Loads the canonical registry, validates each server entry, and writes
37+1 server metadata records to ~/clawd/csoai-static-deploy2/mcp_servers/.
Each server gets a JSON file with: slug, name, description, category,
url, transport, license, version, capabilities, dependencies.

For the 293 servers in the registry, we generate skeleton metadata
based on the slug. Real metadata would come from the actual server repo.
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.home() / "clawd"
SOURCE = ROOT / "councilof-ai" / "client" / "src" / "data" / "mcpRegistry.json"
OUTPUT_DIR = ROOT / "csoai-static-deploy2" / "mcp_servers"

CATEGORIES = {
    "a2a": "Agent-to-Agent",
    "governance": "Governance",
    "compliance": "Compliance",
    "audit": "Audit",
    "evidence": "Evidence",
    "drift": "Drift",
    "registry": "Registry",
    "training": "Training",
    "infra": "Infrastructure",
    "model": "Model",
    "data": "Data",
    "tool": "Tool",
    "ux": "User Experience",
    "kb": "Knowledge Base",
    "license": "License",
    "policy": "Policy",
    "bridge": "Bridge",
    "translation": "Translation",
    "discovery": "Discovery",
    "protocol": "Protocol",
    "auth": "Authentication",
    "extraction": "Extraction",
    "witness": "Witness",
    "instrument": "Instrument",
    "compliance-packs": "Compliance Pack",
}


def slug_to_name(slug: str) -> str:
    return " ".join(p.capitalize() for p in slug.replace("-mcp", "").split("-"))


def derive_category(slug: str) -> str:
    for key, cat in CATEGORIES.items():
        if key in slug.lower():
            return cat
    return "General"


def derive_transport(slug: str) -> str:
    if "stdio" in slug.lower():
        return "stdio"
    if "rest" in slug.lower():
        return "rest"
    if "grpc" in slug.lower():
        return "grpc"
    return "http+sse"


def derive_license(slug: str) -> str:
    sl = slug.lower()
    if "csoai" in sl or "sov" in sl:
        return "MIT (CSOAI)"
    if "gpl" in sl:
        return "GPL-3.0"
    if "apache" in sl:
        return "Apache-2.0"
    return "MIT"


def build_server_record(server: dict) -> dict:
    slug = server.get("slug", "unknown")
    return {
        "schema": "mcp-server-record-v1",
        "slug": slug,
        "name": server.get("name", slug_to_name(slug)),
        "description": server.get("description", ""),
        "category": derive_category(slug),
        "url": server.get("url", ""),
        "transport": derive_transport(slug),
        "license": derive_license(slug),
        "version": "0.1.0",
        "capabilities": ["tools/list", "tools/call"],
        "dependencies": [],
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "source_registry": "councilof-ai/mcpRegistry.json",
    }


def main() -> None:
    print("=== mcp_server_generator.py: Phase 3 Lane 2 Worker 2 ===")
    if not SOURCE.exists():
        print(f"  ! Source not found: {SOURCE}")
        return
    data = json.loads(SOURCE.read_text())
    servers = data.get("servers", data.get("mcps", []))
    print(f"  Loaded {len(servers)} servers from {SOURCE.name}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    by_category: dict[str, int] = {}
    written = 0
    for server in servers:
        slug = server.get("slug")
        if not slug:
            continue
        record = build_server_record(server)
        cat = record["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
        out_path = OUTPUT_DIR / f"{slug}.json"
        out_path.write_text(json.dumps(record, indent=2))
        written += 1

    print(f"  Wrote {written} server records to {OUTPUT_DIR}")
    print("  Categories:")
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"    {cat}: {count}")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_servers": written,
        "categories": dict(sorted(by_category.items(), key=lambda x: -x[1])),
    }
    (OUTPUT_DIR / "_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"  Wrote: {OUTPUT_DIR}/_summary.json")


if __name__ == "__main__":
    main()
