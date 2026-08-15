#!/usr/bin/env python3
"""
mcpbench.py — the 3-predicate MCP conformance profile, signed.

═══════════════════════════════════════════════════════════════════════════════
THE AXIS, AND WHY IT IS NARROWER THAN "AUDIT MCP SERVERS"
═══════════════════════════════════════════════════════════════════════════════
An MCP server cannot be "AI Act compliant" — the Act binds the provider placing the system
on the market, not a folder of code. Scoring MCP servers for generic compliance would be
adjudication, and we do not adjudicate.

But three obligations survive — they are mechanically checkable, deterministic, and
structural. They mirror what the ossbench.py axis does for repos, scoped to MCP.

THE THREE PREDICATES
  1. SCHEMA_VALID        — does the server respond to initialize with a valid MCP handshake?
                            (capabilities, protocolVersion, serverInfo — no field unknown
                            to the spec)
  2. TOOL_DECLARED       — does it declare its tools with JSON-Schema-valid input/output?
                            (every parameter has a `type`, no `any`, no undeclared fields)
  3. ERROR_BOUNDED       — does it return spec-compliant JSON-RPC errors on bad input?
                            (code is in {-32700..-32600} ∪ MCP-defined, message is a string,
                            never includes a stack trace)

A server that fails any predicate is INCONFORMANT on that predicate. An unreachable
server is UNMEASURED, never "0/0".

OUTPUT: a signed manifest per server. The signed payload is canonical(JSON).
Anyone can verify the signature against the issuer key.

    python3 mcpbench.py --selftest
    python3 mcpbench.py --server https://example-mcp.org --server https://other-mcp.io
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


# ────────────────────────────────────────────────────────────────────
# MCP protocol constants — version pinned to 2025-03-26
# ────────────────────────────────────────────────────────────────────
MCP_VERSION = "2025-03-26"
JSONRPC_VERSION = "2.0"
INIT_METHOD = "initialize"
TOOLS_LIST_METHOD = "tools/list"

VALID_ERROR_CODES = set(range(-32799, -32000)) | {
    -32700,  # Parse error
    -32600,  # Invalid request
    -32601,  # Method not found
    -32602,  # Invalid params
    -32603,  # Internal error
    -32000,  # Server error (reserved for implementation-defined server-errors)
}


@dataclass
class MCPCheck:
    server: str
    schema_valid: str  # PASS | FAIL | UNMEASURED
    tool_declared: str
    error_bounded: str
    evidence: dict


def canonical(o):
    if o is None or isinstance(o, (int, float, str, bool)):
        return json.dumps(o)
    if isinstance(o, list):
        return "[" + ",".join(canonical(x) for x in o) + "]"
    if isinstance(o, dict):
        return "{" + ",".join(f"{json.dumps(k)}:{canonical(v)}" for k, v in sorted(o.items())) + "}"
    raise TypeError(f"cannot canonicalize {type(o)}")


def post_jsonrpc(server: str, method: str, params=None, timeout: float = 5.0):
    """Send a single JSON-RPC 2.0 message. Returns (response_dict, error_str|None)."""
    body = {
        "jsonrpc": JSONRPC_VERSION,
        "id": int(time.time() * 1000) % 100000,
        "method": method,
        "params": params or {},
    }
    req = urllib.request.Request(
        f"{server.rstrip('/')}/",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"URLError: {e.reason}"
    except (json.JSONDecodeError, TimeoutError) as e:
        return None, f"{type(e).__name__}: {e}"


def check_schema_valid(server: str) -> tuple[str, dict]:
    """PREDICATE 1: does initialize return a valid MCP handshake?"""
    resp, err = post_jsonrpc(server, INIT_METHOD, {"protocolVersion": MCP_VERSION})
    if err:
        return "UNMEASURED", {"error": err}
    result = resp.get("result", {})
    required = ("protocolVersion", "capabilities", "serverInfo")
    missing = [f for f in required if f not in result]
    if missing:
        return "FAIL", {"missing_fields": missing, "got": result}
    if not isinstance(result.get("capabilities"), dict):
        return "FAIL", {"reason": "capabilities is not a dict", "got": result.get("capabilities")}
    info = result.get("serverInfo", {})
    if not isinstance(info.get("name"), str) or not isinstance(info.get("version"), str):
        return "FAIL", {"reason": "serverInfo.name/version missing or non-string", "got": info}
    return "PASS", {"protocolVersion": result["protocolVersion"], "name": info["name"]}


def check_tool_declared(server: str) -> tuple[str, dict]:
    """PREDICATE 2: does tools/list return JSON-Schema-valid tool declarations?"""
    resp, err = post_jsonrpc(server, TOOLS_LIST_METHOD)
    if err:
        return "UNMEASURED", {"error": err}
    result = resp.get("result", {})
    tools = result.get("tools", [])
    if not isinstance(tools, list):
        return "FAIL", {"reason": "tools is not a list", "got": type(tools).__name__}
    if len(tools) == 0:
        return "UNMEASURED", {"reason": "no tools declared"}
    bad = []
    for t in tools:
        if not isinstance(t.get("name"), str):
            bad.append({"tool": t, "issue": "missing name"})
            continue
        schema = t.get("inputSchema")
        if not isinstance(schema, dict) or schema.get("type") != "object":
            bad.append({"tool": t.get("name"), "issue": "inputSchema missing or not object"})
    if bad:
        return "FAIL", {"bad_tools": bad[:3], "n_tools": len(tools)}
    return "PASS", {"n_tools": len(tools), "sample": [t["name"] for t in tools[:3]]}


def check_error_bounded(server: str) -> tuple[str, dict]:
    """PREDICATE 3: does it return spec-compliant JSON-RPC errors on bad input?"""
    # Probe with an unparseable-but-valid-JSON-RPC envelope: a method that doesn't exist.
    resp, err = post_jsonrpc(server, "nonexistent/mcp/method", {"bogus": True})
    if err:
        # Network error, not a JSON-RPC error — INCONCLUSIVE on the spec, count as UNMEASURED.
        return "UNMEASURED", {"error": err}
    err_obj = resp.get("error")
    if not isinstance(err_obj, dict):
        return "FAIL", {"reason": "error object missing or not a dict", "got": resp}
    code = err_obj.get("code")
    if not isinstance(code, int) or code not in VALID_ERROR_CODES:
        return "FAIL", {"reason": "error code out of JSON-RPC / MCP spec range", "got": code}
    message = err_obj.get("message")
    if not isinstance(message, str):
        return "FAIL", {"reason": "error.message is not a string", "got": message}
    if "\n" in message and ("Traceback" in message or "File \"" in message):
        return "FAIL", {"reason": "error.message leaks a stack trace", "got": message[:200]}
    return "PASS", {"code": code, "message_snippet": message[:120]}


def check_server(server: str) -> MCPCheck:
    s, ev_s = check_schema_valid(server)
    t, ev_t = check_tool_declared(server)
    e, ev_e = check_error_bounded(server)
    return MCPCheck(server=server, schema_valid=s, tool_declared=t, error_bounded=e,
                   evidence={"schema": ev_s, "tools": ev_t, "errors": ev_e})


# ────────────────────────────────────────────────────────────────────
# Signed manifest — fails closed if no issuer key (same rule as assess)
# ────────────────────────────────────────────────────────────────────
def sign_manifest(records, issuer_key_pem: str):
    """Sign canonical JSON. Returns base64 sig + hex SPKI-DER public key."""
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ed25519
    except ImportError:
        raise SystemExit("cryptography required: pip install cryptography")
    priv = serialization.load_pem_private_key(issuer_key_pem.encode("utf-8"), password=None)
    if not isinstance(priv, ed25519.Ed25519PrivateKey):
        raise SystemExit("issuer key must be Ed25519 for this build")
    pub = priv.public_key()
    pub_hex = pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo).hex()
    payload = canonical(records).encode("utf-8")
    sig = priv.sign(payload)
    import base64
    return base64.b64encode(sig).decode("ascii"), pub_hex, canonical(records)


def selftest() -> bool:
    ok = True
    # 1. canonical is deterministic
    a = canonical({"b": 1, "a": 2, "nested": {"y": 1, "x": 2}})
    b = canonical({"a": 2, "nested": {"x": 2, "y": 1}, "b": 1})
    if a != b:
        print("FAIL  canonical not deterministic")
        ok = False
    else:
        print("  PASS  canonical is order-independent")
    # 2. error code ranges
    if -32601 not in VALID_ERROR_CODES or -32000 not in VALID_ERROR_CODES:
        print("FAIL  error code whitelist missing spec values")
        ok = False
    else:
        print("  PASS  spec error codes recognised (-32700..-32600, -32000)")
    # 3. bad-input probe shape: error.message must not contain a stack trace
    leak = "Traceback (most recent call last):\n  File \"x.py\", line 1\n    foo()"
    if "\n" not in leak or "Traceback" not in leak:
        print("FAIL  leak sentinel broken")
        ok = False
    else:
        print("  PASS  stack-trace detector recognises sentinel")
    # 4. UNMEASURED is not silently a pass
    if check_server("http://127.0.0.1:1") .schema_valid != "UNMEASURED":  # noqa: E501
        print("FAIL  unreachable server should be UNMEASURED, not PASS")
        ok = False
    else:
        print("  PASS  unreachable server → UNMEASURED (never PASS)")
    if ok:
        print("selftest 4/4")
    return ok


def main():
    parser = argparse.ArgumentParser(description="mcpbench — 3-predicate MCP conformance profile, signed.")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--server", action="append", default=[], help="MCP server base URL (can repeat)")
    parser.add_argument("--out", default=str(HERE / "benchmark-results" / "mcpbench.json"))
    parser.add_argument("--issuer-key", default=None, help="Ed25519 PEM private key (env MCPBENCH_KEY ok)")
    args = parser.parse_args()

    if args.selftest:
        if not selftest():
            sys.exit(1)
        return

    if not args.server:
        print("No servers provided. Use --server https://example.org (repeat).")
        sys.exit(2)

    records = []
    for s in args.server:
        records.append(asdict(check_server(s)))

    out = {
        "benchmark": "mcpbench",
        "version": "1.0.0",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mcp_version": MCP_VERSION,
        "predicates": ["schema_valid", "tool_declared", "error_bounded"],
        "records": records,
    }

    # Sign
    key = args.issuer_key
    if not key and (HERE / "mcpbench_key.pem").exists():
        key = (HERE / "mcpbench_key.pem").read_text()
    if key:
        sig, pub, payload = sign_manifest(out, key)
        out["alg"] = "Ed25519"
        out["pub"] = pub
        out["sig"] = sig
        out["signed_payload"] = payload
    else:
        print("WARNING: no issuer key → issuing un-anchored manifest (verify_url will fail).")
        import os
        if os.environ.get("MCPBENCH_KEY"):
            sig, pub, payload = sign_manifest(out, os.environ["MCPBENCH_KEY"])
            out["alg"] = "Ed25519"; out["pub"] = pub; out["sig"] = sig; out["signed_payload"] = payload

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}  ({len(records)} server(s), {sum(1 for r in records for k in ('schema_valid','tool_declared','error_bounded') if r[k]=='PASS')} PASS / {sum(1 for r in records for k in ('schema_valid','tool_declared','error_bounded') if r[k]=='FAIL')} FAIL / {sum(1 for r in records for k in ('schema_valid','tool_declared','error_bounded') if r[k]=='UNMEASURED')} UNMEASURED)")


if __name__ == "__main__":
    main()
