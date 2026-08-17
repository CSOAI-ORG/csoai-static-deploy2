#!/usr/bin/env bash
# One-command reproducer for any published signed card.
# Usage: ./reproduce.sh release-proof-REL-001.json
set -e
CARD="${1:?usage: ./reproduce.sh <card.json>}"
echo "1. Fetching card..." 
curl -sSL "https://csoai.org/releases/$CARD" -o "$CARD"
echo "2. Verifying offline (public key only, zero network, zero secrets)..."
python3 - <<'PY'
import json, hashlib, sys
card = json.load(open(sys.argv[1] if False else "release-proof-REL-001.json")) if False else None
PY
python3 - "$CARD" <<'PY'
import json, hashlib, sys
card = json.load(open(sys.argv[1]))
body = card["body"]
cid = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
print("content_id recompute:", "MATCH" if cid == card["id"] else "MISMATCH")
try:
    from nacl.signing import VerifyKey
    VerifyKey(bytes.fromhex(card["pubkey"])).verify(card["id"].encode(), bytes.fromhex(card["signature"]))
    print("signature: VALID")
except ImportError:
    print("signature: install PyNaCl for the Ed25519 check (pip install pynacl)")
PY
echo "Full bundle + DOI: https://doi.org/10.5281/zenodo.21973003"
