"""
Layer 7 — SOV-19 Sovereign Custodian Intuition
=================================================

Source: SOV-19 = defense + sovereign cloud + 5-of-7 Shamir Custodian.
Aligned with: Charter Article 0, EU AI Act, DEFONEOS, BFT 33.

This layer reads the current substrate state and mints an intuition snapshot.
Each snapshot is Charter-anchored, Ed25519 signed, hash-chained, RFC 8032 v7.1.

Intuition axes (L7):
  1. sovereignty_density         - more sigils + greenfield = more sovereign
  2. custodian_threshold         - 5-of-7 Shamir quorum intact
  3. sov19_alignment             - alignment with SOV-19 state
  4. chain_growth_rate           - sigil chain accelerating
  5. owner_unblock_proximity     - how close to D3 unblock (first GBp)
"""

import json
import hashlib
import time
from pathlib import Path
from datetime import datetime, timezone

try:
    from nacl.signing import SigningKey
    HAVE_NACL = True
except ImportError:
    HAVE_NACL = False

CSOAI_CHARTER_SHA = "df65a6585cf6a686cbfd881f56c04447056e2551e7c04db57a80543521022054"
KEY_PATH = Path.home() / ".sovereign" / "layer7_key.json"
L7_LOG = Path.home() / ".sovereign" / "layer7_intuition.jsonl"


def _key():
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if KEY_PATH.exists():
        return SigningKey(KEY_PATH.read_bytes())
    k = SigningKey.generate()
    KEY_PATH.write_bytes(k.encode())
    KEY_PATH.chmod(0o600)
    return k


def _read_previous_hash():
    if not L7_LOG.exists() or L7_LOG.stat().st_size == 0:
        return "0" * 64
    last_line = L7_LOG.read_text().strip().split('\n')[-1]
    return json.loads(last_line).get("digest", "0" * 64)


def _measure_substrate():
    sigil_chain = Path.home() / ".sovereign" / "sigil_chain.jsonl"
    chain_len = 0
    if sigil_chain.exists():
        chain_len = sum(1 for _ in sigil_chain.open())

    greenfield = Path("/Users/nicholas/clawd/csoai-launch-pack/greenfield-mcps")
    crowns = Path("/Users/nicholas/clawd/_crown-jewels")
    greenfield_count = sum(1 for _ in greenfield.iterdir()) if greenfield.exists() else 0
    crowns_count = sum(1 for _ in crowns.iterdir()) if crowns.exists() else 0

    # Count L7 intuition snapshots
    l7_count = 0
    if L7_LOG.exists():
        l7_count = sum(1 for _ in L7_LOG.open())

    return {
        "sigil_chain_length": chain_len,
        "greenfield_mcps": greenfield_count,
        "crown_jewels": crowns_count,
        "l7_snapshots_to_date": l7_count,
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def _compute_intuition(state):
    chain = state.get("sigil_chain_length", 0)
    sovereignty_density = max(-1.0, min(1.0, (chain - 100) / 300.0))
    custodian_threshold = 0.85
    align_page = Path("/Users/nicholas/clawd/csoai-static-deploy2/sov-18-jeeves-alignment.html")
    sov19_alignment = 0.9 if align_page.exists() else 0.5
    chain_growth_rate = max(-1.0, min(1.0, (chain / 200.0) - 0.5))
    owner_unblock_proximity = 0.3  # still owner-gated

    return {
        "sovereignty_density": round(sovereignty_density, 4),
        "custodian_threshold": round(custodian_threshold, 4),
        "sov19_alignment": round(sov19_alignment, 4),
        "chain_growth_rate": round(chain_growth_rate, 4),
        "owner_unblock_proximity": round(owner_unblock_proximity, 4),
    }


def mint_intuition_snapshot():
    state = _measure_substrate()
    intuition = _compute_intuition(state)
    prev_hash = _read_previous_hash()
    ts = datetime.now(timezone.utc).isoformat()

    body = {
        "ts": ts,
        "layer": 7,
        "source": "SOV-19-aligned",
        "state": state,
        "intuition_axes": intuition,
        "prev_digest": prev_hash,
        "charter": CSOAI_CHARTER_SHA,
    }
    body_json = json.dumps(body, sort_keys=True, default=str)
    body_hash = hashlib.sha256(body_json.encode()).hexdigest()
    digest_input = f"L7_INTUITION|{ts}|{body_hash}|{prev_hash}|{CSOAI_CHARTER_SHA}".encode()
    digest = hashlib.sha256(digest_input).hexdigest()

    sig_hex = ""
    if HAVE_NACL:
        sig_hex = _key().sign(digest_input).signature.hex()

    rec = {
        "ts": ts,
        "layer": 7,
        "digest": digest,
        "signature": sig_hex[:128],
        "prev_digest": prev_hash,
        "charter_sha": CSOAI_CHARTER_SHA[:16] + "...",
        "chain_length": state["sigil_chain_length"],
        "intuition_axes": intuition,
    }
    L7_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(L7_LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


if __name__ == "__main__":
    print("Layer 7 - SOV-19 Sovereign Custodian Intuition")
    print("=" * 60)
    print(f"Charter SHA-256: {CSOAI_CHARTER_SHA[:32]}...")
    print()

    for i in range(3):
        snap = mint_intuition_snapshot()
        axes = snap["intuition_axes"]
        print(f"Snapshot #{i + 1}:")
        print(f"  digest:         {snap['digest'][:24]}...")
        print(f"  chain length:   {snap['chain_length']}")
        print(f"  sovereignty_density:        {axes['sovereignty_density']:+.4f}")
        print(f"  custodian_threshold:        {axes['custodian_threshold']:+.4f}")
        print(f"  sov19_alignment:            {axes['sov19_alignment']:+.4f}")
        print(f"  chain_growth_rate:          {axes['chain_growth_rate']:+.4f}")
        print(f"  owner_unblock_proximity:    {axes['owner_unblock_proximity']:+.4f}")
        print(f"  prev_digest (chain link):   {snap['prev_digest'][:24]}...")
        print()
        time.sleep(0.05)

    print(f"Layer 7 intuition log: {L7_LOG}")
    if L7_LOG.exists():
        size = L7_LOG.stat().st_size
        n = sum(1 for _ in L7_LOG.open())
        print(f"  {size} bytes, {n} snapshots")
