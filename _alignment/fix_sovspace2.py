#!/usr/bin/env python3
"""PR-16 sov-space-state.js single authoritative cleanup."""
import re

P = "/workspace/csoai-static-deploy2/api/sov-space-state.js"
s = open(P).read()

pairs = [
    # header
    ("// Returns the current sovereign substrate swarm state",
     "// Returns the current Council substrate swarm state"),
    ("// hidden state — the actual live vector is produced inside the SOV3\n// substrate (vm 35.242.143.249:3101). When reachable we attempt to fetch",
     "// hidden state — the actual live vector is produced inside the Council\n// substrate. When reachable we attempt to fetch"),
    ("// SOV_SPACE_HMAC_SECRET if set, otherwise the sovereign default key.",
     "// SOV_SPACE_HMAC_SECRET must be set."),
    # URL fallback: no dead VM IP
    ("const SOV3_URL = process.env.SOV3_URL || 'http://35.242.143.249:3101/mcp';",
     "const SUBSTRATE_URL = process.env.SOV_SPACE_URL || 'https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp';"),
    ("SOV3_URL", "SUBSTRATE_URL"),
    ("intuition_source = 'sov3-substrate-live';", "intuition_source = 'substrate-live';"),
    ("? 'Live substrate readout — intuition vector pulled from SOV3 intuition_status().'",
     "? 'Live substrate readout — intuition vector pulled from substrate intuition_status().'"),
    (": 'Substrate not reached from this serverless function. Intuition vector is a deterministic minute-seeded placeholder — the real vector lives on the SOV3 VM (35.242.143.249:3101) and is fetched via /mcp from the Mac-side runtime.'",
     ": 'Substrate not reached from this serverless function. Intuition vector is a deterministic minute-seeded placeholder.'"),
]

for old, new in pairs:
    if old in s:
        s = s.replace(old, new)

open(P, "w").write(s)

# verify
bad = re.findall(r"(?i)sovereign|sov3|35\.242\.|10\.0\.0\.1|sov-space-default|Mac-side|SOV3", s)
print(f"REMAINING HITS: {len(bad)} -> {bad[:5]}")
print("SUBSTRATE_URL refs:", s.count("SUBSTRATE_URL"))
print("done")