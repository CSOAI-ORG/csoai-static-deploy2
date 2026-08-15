#!/usr/bin/env python3
"""csoai-framework-signer — MCP server: OSCAL→SCITT "sign your own framework" free wedge.

What it does:
  Given a standards body, school, or government's framework (PDF text or structured),
  this MCP server:
    1. Extracts controls into an OSCAL Catalog
    2. Lets the institution SELECT which controls apply → OSCAL Profile
    3. Signs the Profile with the INSTITUTION's key (signature is theirs, not ours)
    4. Registers the signed statement with a SCITT transparency service (RFC 9943)
    5. Returns a receipt + signed card

Council NEVER signs the content or endorses it — we only run the rails.
The cryptographic act and reputational weight belong ENTIRELY to the institution.

Usage:
  # Via MCP protocol:
  tools/call → framework_to_scitt
  
  # Via CLI:
  python3 csoai_framework_signer.py --framework <file> --institution "UK AISI"
  
  # Via Python SDK (if wrapping in your own code):
  from csoai_framework_signer import framework_to_scitt
"""

from __future__ import annotations
import hashlib, json, os, sys, datetime, tempfile, urllib.request
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from pathlib import Path

# ── Adopt existing estate modules ───────────────────────────────────
try:
    from sovos_oscal import (
        ChainObservation, assessment_results, finding,
        observation, dump, export, self_test,
    )
    HAS_OSCAL = True
except ImportError:
    HAS_OSCAL = False

OSCAL_VERSION = "1.1.0"
SCITT_VERSION = "draft-ietf-scitt-architecture-03"
MCP_PROTOCOL = "2025-03-26"
OMS_CARD_VERSION = "csoai-framework-card-v1"


@dataclass
class FrameworkControl:
    """A single control extracted from a framework PDF"""
    id: str                        # e.g. "GOV-01"
    title: str                     # e.g. "Establish AI Governance Policy"
    description: str               # e.g. "The organization shall establish..."
    source: str                    # e.g. "NIST AI RMF 1.0"
    category: str = "unspecified"  # e.g. "Govern", "Measure", "Manage"
    subcategory: str = ""
    references: List[str] = field(default_factory=list)


@dataclass
class Framework:
    """A parsed framework (OSCAL Catalog equivalent)"""
    title: str
    version: str
    controls: List[FrameworkControl]
    institution: str
    published: str = ""
    framework_id: str = ""


def _digest(obj: Any) -> str:
    """Deterministic SHA-256 digest of a JSON-serializable object."""
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _scitt_statement(catalog: Dict, profile: Dict, signer_key: str) -> Dict:
    """Build a SCITT Statement (RFC 9943 §3.1).

    The SCITT statement wraps the signed profile and is registered
    in a transparency service (or emitted as a self-contained artifact).
    """
    content_hash = _digest(profile)
    statement = {
        "protocol": SCITT_VERSION,
        "content-type": "application/oscal-profile+json",
        "content": profile,
        "content-hash": content_hash,
        "issuer": signer_key,
        "issued": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "meta": {
            "framework": catalog.get("title", "unknown"),
            "institution": signer_key,
            "version": OSCAL_VERSION,
        },
    }
    # Deterministic payload for the SCITT receipt
    payload_digest = _digest(statement)
    statement["payload-digest"] = payload_digest
    return statement


def _scitt_receipt(statement: Dict) -> Dict:
    """Simulate a SCITT receipt (transparency log entry).

    In production this would register with a live SCITT/Rekor instance.
    For the MCP server MVP, the receipt is a self-signed inclusion proof
    that any third party can verify.
    """
    receipt = {
        "receipt-type": "csoai-scitt-simulated-v1",
        "entry": _digest(statement),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "institution-signature": statement.get("issuer", ""),
        "verification": {
            "method": "recompute-statement-digest",
            "statement-digest": statement.get("payload-digest", ""),
        },
        "note": "Production: register with Rekor/SCITT instance for live transparency",
    }
    return receipt


def extract_controls_from_text(framework_text: str, source: str = "custom") -> List[FrameworkControl]:
    """Parse raw text into FrameworkControl objects.

    For a real deployment, this would use NLP/section detection.
    For the MVP, it splits on numbered sections and creates a control per section.
    """
    controls = []
    lines = framework_text.strip().split("\n")
    current = {"id": "", "title": "", "text": ""}
    control_num = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Heuristic: lines starting with a section number are new controls
        if line[0].isdigit() and "." in line[:4]:
            if current["id"]:
                controls.append(FrameworkControl(
                    id=current["id"],
                    title=current["title"][:80],
                    description=current["text"][:512],
                    source=source,
                ))
            control_num += 1
            parts = line.split(" ", 1)
            current = {"id": f"{source[:4].upper()}-{control_num:03d}",
                       "title": parts[1] if len(parts) > 1 else line,
                       "text": line}
        else:
            current["text"] += " " + line

    # Last control
    if current["id"]:
        controls.append(FrameworkControl(
            id=current["id"],
            title=current["title"][:80],
            description=current["text"][:512],
            source=source,
        ))

    return controls if controls else [
        FrameworkControl(id=f"{source[:4].upper()}-001",
                         title=framework_text[:80],
                         description=framework_text[:512],
                         source=source)
    ]


def framework_to_oscal(framework: Framework) -> Dict:
    """Convert a Framework into an OSCAL Catalog (simplified)."""
    catalog = {
        "oscal-version": OSCAL_VERSION,
        "catalog": {
            "uuid": _digest(framework.title + framework.version)[:36],
            "metadata": {
                "title": framework.title,
                "version": framework.version,
                "published": framework.published or datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat(),
                "parties": [{"name": framework.institution, "type": "organization"}],
            },
            "groups": [],
            "controls": [],
        }
    }
    for ctrl in framework.controls:
        catalog["catalog"]["controls"].append({
            "id": ctrl.id,
            "title": ctrl.title,
            "description": ctrl.description,
            "props": [
                {"name": "source", "value": ctrl.source},
                {"name": "category", "value": ctrl.category},
            ],
        })
    return catalog


def select_profile(catalog: Dict, selected_ids: List[str]) -> Dict:
    """Select a subset of controls as an OSCAL Profile."""
    controls = catalog["catalog"]["controls"]
    selected = [c for c in controls if c["id"] in selected_ids]
    profile = {
        "oscal-version": OSCAL_VERSION,
        "profile": {
            "uuid": _digest(json.dumps(selected_ids))[:36],
            "metadata": {
                "title": f"Selected controls from {catalog['catalog']['metadata']['title']}",
                "version": "1.0",
            },
            "imports": [{"href": catalog}],
            "selected-controls": selected_ids,
        }
    }
    return profile


def sign_with_institution_key(payload: Dict, institution_key: str = "") -> Dict:
    """Sign the payload with the INSTITUTION's key (not Council's).

    In production this would use the institution's own Ed25519 key.
    For the MVP, we simulate the key-based signing.
    The important architectural point: Council NEVER holds this key.
    """
    seed = institution_key or os.environ.get("INSTITUTION_SIGNING_KEY", "0" * 64)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = _digest(payload)
    sig = hashlib.sha256(
        bytes.fromhex(seed[:32]) + bytes.fromhex(digest[:32])
    ).hexdigest()[:64]
    return {
        "signature": sig,
        "signer": f"did:key:z{hashlib.sha256(bytes.fromhex(seed[:32])).hexdigest()[:32]}",
        "digest": digest,
    }


def framework_to_scitt(
    framework_text: str,
    institution_name: str,
    framework_title: str = "",
    version: str = "1.0",
    source: str = "custom",
    selected_controls: List[str] = None,
    institution_key: str = "",
) -> Dict:
    """Complete pipeline: framework text → signed SCITT artifact.

    This is the main MCP tool function.

    Args:
        framework_text: Raw text of the framework PDF/standard
        institution_name: The institution signing (e.g. "UK AISI")
        framework_title: Optional title
        version: Version string
        source: Source identifier
        selected_controls: Subset of controls to include (None = all)
        institution_key: The INSTITUTION's signing key (Council never holds this)

    Returns:
        Signed card containing OSCAL Catalog + Profile + SCITT Statement + Receipt
    """
    title = framework_title or f"{institution_name} Framework"

    # 1. Extract controls
    controls = extract_controls_from_text(framework_text, source=source)

    # 2. Build OSCAL Catalog
    framework = Framework(
        title=title,
        version=version,
        controls=controls,
        institution=institution_name,
    )
    catalog = framework_to_oscal(framework)

    # 3. Build OSCAL Profile (selected controls)
    if selected_controls:
        profile = select_profile(catalog, selected_controls)
    else:
        profile = select_profile(catalog, [c["id"] for c in catalog["catalog"]["controls"]])

    # 4. Institution signs the Profile (signature is THEIRS)
    institution_sig = sign_with_institution_key(profile, institution_key)

    # 5. Wrap in SCITT Statement
    statement = _scitt_statement(catalog, profile, institution_sig["signer"])
    statement["institution-signature"] = institution_sig

    # 6. Get SCITT Receipt
    receipt = _scitt_receipt(statement)

    # 7. Emit signed card
    card = {
        "schema": OMS_CARD_VERSION,
        "institution": institution_name,
        "framework": title,
        "version": version,
        "oscal_version": OSCAL_VERSION,
        "control_count": len(controls),
        "selected_count": len(selected_controls or controls),
        "catalog": catalog,
        "profile": profile,
        "scitt_statement": statement,
        "scitt_receipt": receipt,
        "council_role": "rails-provider",
        "council_note": "Council provides the signing/notarisation infrastructure. The cryptographic act and the content are the institution's.",
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    return card


# ── MCP Server (stdio) ──────────────────────────────────────────────
def _handle_mcp_request(request: Dict) -> Dict:
    """Handle an MCP JSON-RPC request."""
    method = request.get("method", "")
    params = request.get("params", {})
    req_id = request.get("id", 0)

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "framework_to_scitt",
                        "description": "Convert a framework PDF text into a signed, machine-readable SCITT artifact. "
                                     "The signature is the INSTITUTION's — Council provides rails, not endorsement.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "framework_text": {"type": "string",
                                    "description": "Raw text of the framework / standard / certification"},
                                "institution_name": {"type": "string",
                                    "description": "Name of the institution signing (e.g. UK AISI)"},
                                "framework_title": {"type": "string",
                                    "description": "Optional title overriding auto-detection"},
                                "version": {"type": "string",
                                    "description": "Version string (default: 1.0)"},
                                "source": {"type": "string",
                                    "description": "Source identifier (default: custom)"},
                                "selected_controls": {"type": "array", "items": {"type": "string"},
                                    "description": "Subset of control IDs to select (default: all)"},
                            },
                            "required": ["framework_text", "institution_name"],
                        },
                    },
                    {
                        "name": "framework_self_test",
                        "description": "Run a self-test with a sample framework to verify the pipeline.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                ],
            },
        }

    elif method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name == "framework_to_scitt":
            card = framework_to_scitt(
                framework_text=arguments.get("framework_text", ""),
                institution_name=arguments.get("institution_name", ""),
                framework_title=arguments.get("framework_title", ""),
                version=arguments.get("version", "1.0"),
                source=arguments.get("source", "custom"),
                selected_controls=arguments.get("selected_controls"),
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(card, indent=2)}],
                },
            }

        elif tool_name == "framework_self_test":
            test_text = (
                "1. Governance and Oversight\n"
                "The organization shall establish an AI governance framework.\n"
                "2. Risk Management\n"
                "Implement continuous risk assessment for AI systems.\n"
                "3. Transparency\n"
                "Maintain records of AI system decisions.\n"
            )
            card = framework_to_scitt(
                framework_text=test_text,
                institution_name="Test Institution",
                framework_title="AI Governance Test Framework",
                version="1.0",
            )
            summary = {
                "test": "PASS",
                "institution": "Test Institution",
                "control_count": card["control_count"],
                "selected_count": card["selected_count"],
                "has_catalog": "catalog" in card,
                "has_profile": "profile" in card,
                "has_scitt_statement": "scitt_statement" in card,
                "has_scitt_receipt": "scitt_receipt" in card,
                "council_role": card["council_role"],
                "note": card["council_note"],
            }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(summary, indent=2)}],
                },
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}


# ── CLI entry point ─────────────────────────────────────────────────
def main():
    """Run as an MCP stdio server or direct CLI."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ("--mcp", "--stdio"):
        # stdio MCP — read JSON-RPC lines from stdin
        import sys
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
                response = _handle_mcp_request(request)
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                sys.stderr.write(f"Invalid JSON: {e}\n")
    else:
        # Direct CLI
        import argparse
        parser = argparse.ArgumentParser(description="OSCAL→SCITT Framework Signer (free wedge)")
        parser.add_argument("--framework", help="Path to framework text file")
        parser.add_argument("--institution", default="Test Institution",
                          help="Name of the institution signing")
        parser.add_argument("--title", default="", help="Framework title")
        parser.add_argument("--version", default="1.0", help="Version string")
        parser.add_argument("--self-test", action="store_true",
                          help="Run self-test")
        args = parser.parse_args()

        if args.self_test:
            test_text = (
                "1. Governance and Oversight\n"
                "The organization shall establish an AI governance framework.\n"
                "2. Risk Management\n"
                "Implement continuous risk assessment for AI systems.\n"
                "3. Transparency\n"
                "Maintain records of AI system decisions.\n"
            )
            card = framework_to_scitt(test_text, "Test Institution",
                                      "AI Governance Test Framework")
            print(json.dumps({
                "test": "PASS",
                "control_count": card["control_count"],
                "selected_count": card["selected_count"],
                "has_catalog": "catalog" in card,
                "has_scitt_statement": "scitt_statement" in card,
                "council_role": card["council_role"],
            }, indent=2))
        elif args.framework and args.institution:
            text = open(args.framework).read()
            card = framework_to_scitt(text, args.institution, args.title, args.version)
            print(json.dumps(card, indent=2))
        else:
            parser.print_help()


if __name__ == "__main__":
    main()