"""Stamp crown-jewel CSOAI files as dated proof-of-existence via OpenTimestamps.

Steps (from IP plan §Stage-1 / §H TS-01..02):
  - compute sha256 of each file (file never leaves this machine)
  - commit that digest to an INDEPENDENT OTS calendar (see sovos_city.timestamping)
  - write the .ots proof beside a manifest, without claiming BTC-anchor until verified

Honesty: this is proof-of-existence-at-a-date, NOT Bitcoin-anchored verification
(calendar_commit vs btc_anchored are tracked separately; BTC-anchor is PENDING
unless a block is verified). Run from the repo root.
"""
import hashlib, json, sys, os
from pathlib import Path
sys.path.insert(0, "SOVOS/packages/sovos-city/src")
from sovos_city.timestamping import stamp_content_id

# Crown jewels: genuinely developed / analytical / unpublished-adjacent assets.
# We stamp the digest, not the content. Trade-secret content never leaves the machine.
CROWN_ITEMS = [
    "IP_REGISTRATION_2026-07-30.md",      # technical IP ledger (owned)
    "IP_NOTICE.md",                       # IP notice / rights reservation
    "_alignment/CATAPULT_MASTER_2026-08-14.md",   # strategy master
    "_alignment/IP_ASSET_REGISTER_2026-08-14.md", # this register
    "SOVOS/agents/board_v2.py",           # 14-axis board measurement core
]
OUT_DIR = Path("_ip/ots")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def stamp(path: str):
    p = Path(path)
    if not p.exists():
        return {"file": path, "state": "MISSING"}
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    anchor = stamp_content_id(digest, ots_dir=OUT_DIR)
    return {
        "file": path,
        "sha256": digest,
        "ots_file": Path(anchor.ots_path).name if anchor.ots_path else "",
        "state": anchor.state,
        "calendar": anchor.calendar_used,
        "note": anchor.note,
    }

results = [stamp(f) for f in CROWN_ITEMS]
manifest = {
    "purpose": "dated proof-of-existence for CSOAI crown-jewel assets (IP plan Stage-1/§H)",
    "generated": "2026-08-14",
    "honesty": "calendar_commit = existed at time T (independent OTS calendar); "
               "btc_anchored NOT claimed until a Bitcoin block is verified",
    "items": results,
}
mp = OUT_DIR / "manifest.json"
mp.write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))
