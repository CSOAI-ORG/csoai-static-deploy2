"""
sov33-layers/common/sovereign_core.py
======================================
Shared Charter + Sigil + Care Floor utilities for all 12 SOV33 layers.

Honesty register: this is the substrate. Every layer uses this. None
of the heavy ops (model inference, network calls, file system writes
beyond ~/.sovereign/) happen without going through the care floor.
"""

import hashlib
import json
import os
import secrets
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

try:
    from nacl.signing import SigningKey
    HAVE_NACL = True
except ImportError:
    HAVE_NACL = False


CSOAI_CHARTER_SHA = "df65a6585cf6a686cbfd881f56c04447056e2551e7c04db57a80543521022054"
CSOAI_SIGIL_ROOT = "77ab0e6f9d6c77e8"
CARE_FLOOR = 0.95
SOVEREIGN_HOME = Path.home() / ".sovereign"
SOVEREIGN_HOME.mkdir(parents=True, exist_ok=True)


def _get_key(layer: str) -> "SigningKey":
    """Per-layer Ed25519 keypair. Created on first use, chmod 600."""
    key_path = SOVEREIGN_HOME / f"{layer}_key.json"
    if key_path.exists():
        return SigningKey(key_path.read_bytes())
    k = SigningKey.generate()
    key_path.write_bytes(k.encode())
    key_path.chmod(0o600)
    return k


def _chain_read(layer_log_name: str) -> str:
    """Return the digest of the most recent record in the layer's chain."""
    log = SOVEREIGN_HOME / layer_log_name
    if not log.exists() or log.stat().st_size == 0:
        return "0" * 64
    last_line = log.read_text().strip().split("\n")[-1]
    return json.loads(last_line).get("digest", "0" * 64)


def care_floor_check(value: float, op: str) -> bool:
    """Care floor 0.95. Returns True if action is allowed."""
    if value < CARE_FLOOR:
        return False
    return True


def mint_op(
    layer: str,
    op: str,
    intent: str,
    body: dict,
    care_value: float = 1.0,
    force_log: bool = False,
) -> dict:
    """Mint a sovereign op. By default the care floor vetoes low scores
    (raises RuntimeError). Pass force_log=True to record the veto anyway,
    so the audit trail captures every probe regardless of outcome."""
    vetoed = care_value < CARE_FLOOR
    if vetoed and not force_log:
        raise RuntimeError(f"Care Floor vetoed: {op} care={care_value}")
    prev_digest = _chain_read(f"layer{layer}_chain.jsonl")
    ts = datetime.now(timezone.utc).isoformat()
    body_json = json.dumps(body, sort_keys=True, default=str)
    body_hash = hashlib.sha256(body_json.encode()).hexdigest()
    digest_input = f"L{layer}|{op}|{intent}|{ts}|{body_hash}|{prev_digest}|{CSOAI_CHARTER_SHA}".encode()
    digest = hashlib.sha256(digest_input).hexdigest()

    sig_hex = ""
    if HAVE_NACL:
        try:
            sig_hex = _get_key(layer).sign(digest_input).signature.hex()
        except Exception:
            sig_hex = hashlib.sha256(digest_input + b"fallback").hexdigest()[:128]
    else:
        sig_hex = hashlib.sha256(digest_input + b"fallback").hexdigest()[:128]

    rec = {
        "layer": layer,
        "op": op,
        "ts": ts,
        "intent": intent,
        "body_hash": body_hash,
        "digest": digest,
        "signature": sig_hex[:128],
        "prev_digest": prev_digest,
        "charter_sha": CSOAI_CHARTER_SHA,
        "care_value": care_value,
        "vetoed": vetoed,
    }
    log_path = SOVEREIGN_HOME / f"layer{layer}_chain.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(rec) + "\n")

    rec["audit_url"] = f"https://proofof.ai/audit/{digest}"
    return rec


def chain_length(layer: str) -> int:
    """Return the number of ops recorded for a given layer."""
    log_path = SOVEREIGN_HOME / f"layer{layer}_chain.jsonl"
    if not log_path.exists():
        return 0
    with open(log_path) as f:
        return sum(1 for _ in f)


def latest(layer: str) -> Optional[dict]:
    """Return the latest record on the chain (or None)."""
    log_path = SOVEREIGN_HOME / f"layer{layer}_chain.jsonl"
    if not log_path.exists() or log_path.stat().st_size == 0:
        return None
    last_line = log_path.read_text().strip().split("\n")[-1]
    return json.loads(last_line)


def audit_brief(layer: str) -> dict:
    """Compact audit state for a layer."""
    n = chain_length(layer)
    last = latest(layer)
    return {
        "layer": layer,
        "chain_length": n,
        "last_digest": last.get("digest", "0" * 64)[:24] + "..." if last else "none",
        "last_ts": last.get("ts") if last else None,
        "care_floor": CARE_FLOOR,
        "charter": CSOAI_CHARTER_SHA[:16] + "...",
    }
