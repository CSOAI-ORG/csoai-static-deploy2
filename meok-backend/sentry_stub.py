#!/usr/bin/env python3
"""
SOV3 Sovereign Crash Reporter
=================================
Logs to /tmp/sov3_crashes.log. No foreign API. SIGIL-stamped.
"""
import json, time, traceback
from datetime import datetime
from pathlib import Path

LOG = Path("/tmp/sov3_crashes.log")
SIGIL_QUEUE = Path("/tmp/sov3_crash_sigils.log")


def report(error_type, error_msg, context=None):
    """Report a sovereign crash."""
    ts = datetime.now().isoformat()
    entry = {
        "ts": ts,
        "type": error_type,
        "error": error_msg,
        "context": context or {},
        "traceback": traceback.format_exc(),
    }
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def emit_sigil(line):
    """Emit sovereign SIGIL to live chain."""
    import urllib.request
    try:
        payload = json.dumps({"jsonrpc":"2.0","id":"cr","method":"tools/call",
                              "params":{"name":"sov_sigil_emit","arguments":{"line":line,"op":"C"}}}).encode()
        req = urllib.request.Request("http://localhost:3101/mcp", data=payload,
                                      headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        return None


if __name__ == "__main__":
    report("test", "Sentry stub working", {"ts": "manual-test"})
    sigil = emit_sigil("C|crash_reporter_init|T2026-06-29T12_00_BST. sentry_stub_LIVE. sovereign_crash_logging_ready. empire_10/10.")
    print(f"Sovereign crash reporter initialized. SIGIL: {sigil}")
