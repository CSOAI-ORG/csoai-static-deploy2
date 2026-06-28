"""meok_sovereign_defence_mcp — Sovereign Defence MCP (defensive only).

5 tools for defence-aware sovereign operations:

  1. sov_threat_assess     - score a threat (1-10)
  2. sov_iwc_calculate     - Information Warfare Capacity calculation
  3. sov_jsp936_audit      - JSP 936 audit (NATO assurance standard)
  4. sov_c2_route          - C2 (Command & Control) routing
  5. sov_doctrine          - retrieve defensive doctrine (no offensive ops)

Reference: Kimi DefneOS intel, this is DEFENSIVE ONLY.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False

VERSION = "0.1.0"
PROTOCOL = "sovereign-defence/0.1"

# === DEFENSIVE DOCTRINE (no offensive ops) ===
DEFENSIVE_DOCTRINE = {
    "motto": "Defend. Detect. Deny. Deceive. Defeat. — Never Offend.",
    "principles": [
        "Hardened perimeters only.",
        "Zero-trust identity for every agent + human.",
        "Signed audit trail for every action.",
        "BFT consensus on any external write.",
        "Human approval required for kinetic or legal-binding actions.",
        "Defensive deception (honeypots, tarpits) is allowed.",
        "Offensive action: NOT in scope. Refer to allied/state forces.",
    ],
    "jsp_936_audit_pillars": [
        "Identify critical functions and dependencies",
        "Assess threats and vulnerabilities",
        "Document and review resilience plans",
        "Test, exercise, and validate responses",
        "Manage incidents with traceable decisions",
    ],
}


def _load_key():
    if not _HAS_CRYPTO:
        raise RuntimeError("cryptography library required")
    path = os.environ.get("SOV_DEF_KEY") or os.path.expanduser("~/.meok/sov_def_key.pem")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return Ed25519PrivateKey.from_private_bytes(f.read())
    priv = Ed25519PrivateKey.generate()
    with open(path, "wb") as f:
        f.write(priv.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption()))
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return priv


def _sign(payload):
    body = {k: v for k, v in payload.items() if k not in ("kid", "sig", "verify_url")}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    priv = _load_key()
    sig = priv.sign(canonical)
    pub = priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return {**payload, "kid": base64.b64encode(pub).decode(), "sig": base64.b64encode(sig).decode()}


def sov_threat_assess(description: str, *, evidence: Optional[dict] = None) -> dict:
    """Score a threat from 1 (negligible) to 10 (existential)."""
    text = description.lower()
    score = 1
    factors = []

    if re.search(r"\b(cyber|malware|ransomware|breach|exfil)\b", text):
        score += 3
        factors.append("cyber_dimension: +3")
    if re.search(r"\b(physical|breach|intruder|attack|kinetic)\b", text):
        score += 4
        factors.append("physical_dimension: +4")
    if re.search(r"\b(insider|compromise|social)\b", text):
        score += 2
        factors.append("insider_dimension: +2")
    if re.search(r"\b(critical|infrastructure|grid|water|health)\b", text):
        score += 2
        factors.append("critical_infrastructure: +2")
    if re.search(r"\b(ai|autonomous|agent|llm|model)\b", text):
        score += 1
        factors.append("ai_dimension: +1")
    if evidence and evidence.get("active_exploitation"):
        score += 1
        factors.append("active_exploitation: +1")

    score = min(score, 10)
    if score >= 8:
        level = "critical"
    elif score >= 5:
        level = "high"
    elif score >= 3:
        level = "medium"
    else:
        level = "low"

    payload = {
        "protocol": PROTOCOL,
        "version": VERSION,
        "threat_score": score,
        "threat_level": level,
        "factors": factors,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    signed = _sign(payload)
    signed["verify_url"] = f"https://proofof.ai/defence/threat/{signed['threat_score']}"
    return signed


def sov_iwc_calculate(scans_per_day: int, detected_threats: int, neutralised: int) -> dict:
    """Information Warfare Capacity = (detected + neutralised) / scans."""
    if scans_per_day == 0:
        return {"error": "scans_per_day must be > 0"}
    detection_rate = detected_threats / scans_per_day
    neutralisation_rate = neutralised / max(detected_threats, 1)
    iwc = (detected_threats * 0.4 + neutralised * 0.6) / scans_per_day

    if iwc >= 0.8:
        capacity = "sovereign"
    elif iwc >= 0.5:
        capacity = "robust"
    elif iwc >= 0.3:
        capacity = "developing"
    else:
        capacity = "exposed"

    payload = {
        "protocol": PROTOCOL,
        "version": VERSION,
        "iwc": round(iwc, 4),
        "capacity": capacity,
        "detection_rate": round(detection_rate, 4),
        "neutralisation_rate": round(neutralisation_rate, 4),
        "scans_per_day": scans_per_day,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    signed = _sign(payload)
    signed["verify_url"] = f"https://proofof.ai/defence/iwc/{signed['iwc']}"
    return signed


def sov_jsp936_audit(organisation: str, pillars: dict) -> dict:
    """Audit an organisation against JSP 936 (NATO assurance standard)."""
    if not all(p in pillars for p in DEFENSIVE_DOCTRINE["jsp_936_audit_pillars"]):
        return {"error": "missing pillars", "required": DEFENSIVE_DOCTRINE["jsp_936_audit_pillars"]}

    scores = []
    gaps = []
    for pillar, evidence in pillars.items():
        score = 0
        if isinstance(evidence, dict):
            score += 5 if evidence.get("documented") else 0
            score += 3 if evidence.get("tested") else 0
            score += 2 if evidence.get("incident_history") else 0
        elif evidence:
            score = 7
        scores.append({"pillar": pillar, "score": score, "max": 10})
        if score < 6:
            gaps.append({"pillar": pillar, "current": score, "target": 8})

    overall = sum(s["score"] for s in scores) / len(scores) if scores else 0
    if overall >= 8:
        assurance = "sovereign"
    elif overall >= 6:
        assurance = "robust"
    elif overall >= 4:
        assurance = "developing"
    else:
        assurance = "exposed"

    payload = {
        "protocol": PROTOCOL,
        "version": VERSION,
        "organisation": organisation,
        "scores": scores,
        "overall_score": round(overall, 2),
        "assurance_level": assurance,
        "gaps": gaps,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    signed = _sign(payload)
    signed["verify_url"] = f"https://proofof.ai/defence/jsp936/{organisation}"
    return signed


def sov_c2_route(asset_id: str, destination: str, *, priority: str = "normal", requires_approval: bool = True) -> dict:
    """C2 (Command & Control) routing for a defensive asset. Returns the route + approval status."""
    if requires_approval and priority in ("high", "critical"):
        approval = "pending_council_vote"
    else:
        approval = "auto_approved" if not requires_approval else "pending_officer"

    route = {
        "asset_id": asset_id,
        "destination": destination,
        "priority": priority,
        "approval": approval,
        "hops": [
            {"hop": 1, "via": "m2-mac", "latency_ms": 5},
            {"hop": 2, "via": "tunnel:sov3-mac-vm", "latency_ms": 12},
            {"hop": 3, "via": "vm-meok-backend", "latency_ms": 8},
        ],
        "total_latency_ms": 25,
    }

    payload = {
        "protocol": PROTOCOL,
        "version": VERSION,
        "route": route,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    signed = _sign(payload)
    signed["verify_url"] = f"https://proofof.ai/defence/c2/{asset_id}"
    return signed


def sov_doctrine() -> dict:
    """Return the defensive doctrine."""
    payload = {
        "protocol": PROTOCOL,
        "version": VERSION,
        "doctrine": DEFENSIVE_DOCTRINE,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    signed = _sign(payload)
    signed["verify_url"] = "https://proofof.ai/defence/doctrine"
    return signed


def register_mcp_tools(mcp):
    mcp.tool(name="sov_threat_assess", description="Score a threat 1-10.")(sov_threat_assess)
    mcp.tool(name="sov_iwc_calculate", description="Information Warfare Capacity calculation.")(sov_iwc_calculate)
    mcp.tool(name="sov_jsp936_audit", description="JSP 936 (NATO assurance) audit.")(sov_jsp936_audit)
    mcp.tool(name="sov_c2_route", description="C2 (Command & Control) routing for a defensive asset.")(sov_c2_route)
    mcp.tool(name="sov_doctrine", description="Return the defensive doctrine (no offensive ops).")(sov_doctrine)


def serve():
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("meok-sovereign-defence")
    register_mcp_tools(mcp)
    mcp.run()


if __name__ == "__main__":
    serve()
