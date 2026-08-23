#!/usr/bin/env python3
"""Inspect + normalize city-3d registry manifest to official MCP schema."""
import json, os

REG = "/workspace/jeeves-exec/registry"
os.chdir(REG)

gspc = json.load(open("server.json"))
city = json.load(open("csoai-city-3d.json"))

print("=== gspc schema keys ===", list(gspc.keys()))
print("=== city schema keys ===", list(city.keys()))
print()
print("gspc remotes:", json.dumps(gspc.get("remotes"), indent=1))
print()
print("city packages:", json.dumps(city.get("packages"), indent=1)[:400])
print("city has remotes field?", "remotes" in city)