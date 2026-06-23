#!/usr/bin/env python3
"""Publish a single, signed-ledger-backed status feed for Sovereign Town.

The flywheel writes a per-host snapshot (`fleet_status_<host>.json`) carrying the
host's cumulative episode count, crime tallies and the Ed25519 chain head of its
signed ledger. The public marketing surfaces (csoai.org, proofof.ai) used to
hard-code these numbers, so they drifted badly out of date.

This script reads the per-host snapshots, sums the *additive* fields (episodes and
crimes accumulate over disjoint seed windows), keeps the structural fields as-is
(28 hives / 140 personas / 29 passports are the same fleet on every host), attaches
each host's chain head + the issuer public key for offline verification, and writes
one combined `status.json` into every front-end that should display it.

Run it on a flywheel host (or from cron) after each publish; the front-ends fetch
`status.json` same-origin and fall back to baked-in values if it is missing.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOME = Path.home()

# Where the flywheel drops per-host snapshots (canonical published location).
SNAPSHOT_DIR = HOME / "clawd" / "proofof-site" / "sovereign-town"
HOSTS = ["mac", "vm"]

# Structural / verification inputs.
PASSPORTS_DIR = HERE / "passports"
ISSUER_PUBKEY_FILE = SNAPSHOT_DIR / "issuer-pubkey.txt"
CHARACTERS_FILE = HERE / "characters.json"
VERIFY_URL = "https://proofof.ai/sovereign-town"

# Every front-end that should show the same numbers.
PUBLISH_TARGETS = [
    SNAPSHOT_DIR / "status.json",
    HOME / "clawd" / "csoai.org" / "sovereign-town" / "status.json",
]


def load_host(host: str) -> dict | None:
    f = SNAPSHOT_DIR / f"fleet_status_{host}.json"
    if not f.exists():
        print(f"  ! missing snapshot: {f}", file=sys.stderr)
        return None
    return json.loads(f.read_text())


def count_passports() -> int:
    if not PASSPORTS_DIR.is_dir():
        return 0
    return len([p for p in PASSPORTS_DIR.glob("*.json")])


def count_personas() -> int:
    # The town population is 140 agents (see /api/town-state `total_agents`).
    # characters.json is keyed by hive, not persona, so it is not the source here.
    return 140


def build_status() -> dict:
    hosts = [(h, load_host(h)) for h in HOSTS]
    hosts = [(h, d) for h, d in hosts if d]
    if not hosts:
        sys.exit("No per-host snapshots found — is the flywheel publishing?")

    cum_episodes = sum(d.get("cum_episodes", 0) for _, d in hosts)
    governed = sum(d.get("governed_crimes", 0) for _, d in hosts)
    ungoverned = sum(d.get("ungoverned_crimes", 0) for _, d in hosts)
    # hives is the same fleet replicated per host, not additive.
    hives = max((d.get("hives", 0) for _, d in hosts), default=0)
    updated = max((d.get("updated", "") for _, d in hosts), default="")

    return {
        "cum_episodes": cum_episodes,
        "governed_crimes": governed,
        "ungoverned_crimes": ungoverned,
        "hives": hives,
        "personas": count_personas(),
        "passports": count_passports(),
        "hosts": [
            {
                "host": h,
                "cycle": d.get("cycle"),
                "cum_episodes": d.get("cum_episodes"),
                "ungoverned_crimes": d.get("ungoverned_crimes"),
                "chain_head": d.get("chain_head"),
                "updated": d.get("updated"),
            }
            for h, d in hosts
        ],
        "issuer_pubkey": (
            ISSUER_PUBKEY_FILE.read_text().strip()
            if ISSUER_PUBKEY_FILE.exists()
            else None
        ),
        "verify_url": VERIFY_URL,
        "updated": updated,
        "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def main() -> None:
    status = build_status()
    blob = json.dumps(status, indent=2) + "\n"
    for target in PUBLISH_TARGETS:
        if target.parent.is_dir():
            target.write_text(blob)
            print(f"  wrote {target}")
        else:
            print(f"  ! skip (no dir): {target}", file=sys.stderr)
    print(
        f"\nSovereign Town status: {status['cum_episodes']:,} episodes · "
        f"{status['governed_crimes']:,} governed crimes · "
        f"{status['ungoverned_crimes']:,} ungoverned · "
        f"{status['hives']} hives · {status['passports']} passports"
    )


if __name__ == "__main__":
    main()
