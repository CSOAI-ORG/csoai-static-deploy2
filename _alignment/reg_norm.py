#!/usr/bin/env python3
"""Normalize csoai-city-3d.json to official MCP registry server.schema (remotes shape = gspc)."""
import json, os

REG = "/workspace/jeeves-exec/registry"
os.chdir(REG)
p = "csoai-city-3d.json"
d = json.load(open(p))

# Build official-schema manifest mirroring gspc server.json
norm = {
    "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
    "name": d["name"],
    "description": d["description"],
    "repository": d["repository"],
    "version": d.get("version", "1.0.0"),
    "remotes": [
        {
            "type": "streamable-http",
            "url": "https://csoai-city-3d-mcp.nicholastempleman.workers.dev/mcp",
        }
    ],
}

backup = p + ".bak-packages"
open(backup, "w").write(json.dumps(d, indent=2))
open(p, "w").write(json.dumps(norm, indent=2))
print("normalized", p)
print("new keys:", list(norm.keys()))
print("wrote backup:", backup)