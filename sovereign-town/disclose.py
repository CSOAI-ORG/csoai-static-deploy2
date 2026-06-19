#!/usr/bin/env python3
"""
disclose.py — auto-file a Sovereign Town invention to openpatent.ai (one call).

Drops a disclosure JSON into the openpatent-hive vault; the running auto-disclose-watcher
(systemd/cron: openpatent-cron.service) anchors it into the audit chain with zero human-in-loop.

    python3 disclose.py "Invention title" "One-paragraph description of the novel method."
"""
import hashlib, json, os, sys
from datetime import datetime, timezone

VAULT = os.path.expanduser("~/clawd/openpatent-hive/vault/disclosures")

def disclose(title: str, desc: str, owner="nicholas@csoai.org", project="sovereign-town"):
    os.makedirs(VAULT, exist_ok=True)
    h = hashlib.sha256(title.encode()).hexdigest()
    rec = {"id": f"disc-{h[:12]}", "did": f"did:opatent:{h[:32]}", "owner_email": owner,
           "title": title, "use_case": desc, "project": project,
           "filed_at": datetime.now(timezone.utc).isoformat(), "status": "pending"}
    path = os.path.join(VAULT, f"disc-{h[:12]}.json")
    json.dump(rec, open(path, "w"), indent=2)
    return rec["id"], path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    did, path = disclose(sys.argv[1], sys.argv[2])
    print(f"filed {did} -> {path}\n(watcher will anchor it; or: cd ~/clawd/openpatent-hive && "
          f"python3 scripts/auto-disclose-watcher.py --once)")
