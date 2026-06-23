#!/usr/bin/env python3
"""
config.py — single source of truth for ports, hosts, paths, and security knobs.

All environment-variable overrides are read here so downstream modules import
constants instead of re-parsing env vars and hardcoding literals.
"""
from __future__ import annotations

import os
from pathlib import Path

P0 = Path(__file__).parent
REPO = P0.parent.parent

# ─── Service ports ───────────────────────────────────────────────────────────
DASHBOARD_PORT = int(os.environ.get("SOV_TOWN_DASHBOARD_PORT", "3940"))
HARNESS_PORT = int(os.environ.get("SOV_TOWN_HARNESS_PORT", "3941"))
MCP_SSE_PORT = int(os.environ.get("SOV_TOWN_MCP_SSE_PORT", "3942"))

# ─── Service URLs ────────────────────────────────────────────────────────────
DASHBOARD_URL = os.environ.get("SOV_TOWN_DASHBOARD_URL", f"http://127.0.0.1:{DASHBOARD_PORT}")
HARNESS_URL = os.environ.get("SOV_TOWN_HARNESS_URL", f"http://127.0.0.1:{HARNESS_PORT}")
MCP_URL = os.environ.get("SOV_TOWN_MCP_URL", f"http://127.0.0.1:{MCP_SSE_PORT}")

# ─── Project paths ───────────────────────────────────────────────────────────
OUT_DIR = P0
EU_DATA_DIR = REPO / "eu_data"
LABS_DIR = REPO / "meok-labs-engine" / "research" / "sovereign-town"
PUBLIC_DIR = REPO / "proofof-site" / "sovereign-town"
VERIFY_DIR = REPO / "sovereign-town" / "verify"
BENCHMARK_RUNS_DIR = P0 / "benchmark_runs"
PASSPORTS_DIR = P0 / "passports"

# ─── Security knobs ──────────────────────────────────────────────────────────
CORS_ORIGINS = [o.strip() for o in os.environ.get("SOV_TOWN_CORS_ORIGINS", "").split(",") if o.strip()]
MAX_BODY_BYTES = int(os.environ.get("SOV_TOWN_MAX_BODY_BYTES", "1048576"))
MAX_QUERY_LENGTH = int(os.environ.get("SOV_TOWN_MAX_QUERY_LENGTH", "4096"))
API_TOKEN = os.environ.get("SOV_TOWN_API_TOKEN")
KEY_PASSWORD = os.environ.get("SOV_TOWN_KEY_PASSWORD")

# ─── Harness rate limits ─────────────────────────────────────────────────────
HARNESS_MAX_RUNS_PER_MINUTE = int(os.environ.get("SOV_TOWN_HARNESS_MAX_RUNS_PER_MINUTE", "10"))
HARNESS_RATE_WINDOW_SECONDS = int(os.environ.get("SOV_TOWN_HARNESS_RATE_WINDOW_SECONDS", "60"))
HARNESS_MAX_MANIFESTS_PER_HOUR = int(os.environ.get("SOV_TOWN_HARNESS_MAX_MANIFESTS_PER_HOUR", "100"))

# ─── Observability ───────────────────────────────────────────────────────────
ACCESS_LOG = os.environ.get("SOV_TOWN_ACCESS_LOG", "0") == "1"
METRICS_WINDOW = int(os.environ.get("SOV_TOWN_METRICS_WINDOW", "10000"))

# ─── Cross-terminal bridges ──────────────────────────────────────────────────
FREELLMAPI_URL = os.environ.get("SOV_TOWN_FREELLMAPI_URL", "http://127.0.0.1:3001/v1/chat/completions")
FREELLMAPI_KEY = os.environ.get("SOV_TOWN_FREELLMAPI_KEY")
SOV3_MESH_URL = os.environ.get("SOV_TOWN_SOV3_MESH_URL", "http://127.0.0.1:3101/mcp")
SOV3_KEY = os.environ.get("SOV_TOWN_SOV3_KEY")
AETHELGARD_HIVE = os.environ.get("SOV_TOWN_AETHELGARD_HIVE", "finance")
