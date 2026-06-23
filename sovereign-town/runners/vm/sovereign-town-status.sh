#!/bin/bash
# Sovereign Town — VM partition status reporter (Kimi-managed)
# Runs on Mac every 10 min via launchd, gathers VM state over SSH.

set -euo pipefail

LOG_DIR="/Users/nicholas/.kimi/logs/sovereign"
mkdir -p "$LOG_DIR"
OUT="$LOG_DIR/sovereign-town-status.md"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PUBLIC_DIR="/Users/nicholas/clawd/proofof-site/sovereign-town"
mkdir -p "$PUBLIC_DIR"

TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

ssh -o ConnectTimeout=5 meok-backend '
  cd /home/nicholas/sovereign-town/p0_aqua 2>/dev/null || exit 1
  pgrep -f "flywheel_forever.py" || echo ""
  echo "---FLEET---"
  cat fleet_status_vm.json 2>/dev/null || echo "{}"
  echo "---LEDGER---"
  tail -1 flywheel_ledger_vm.jsonl 2>/dev/null || echo ""
' > "$TMP" 2>&1 || {
  {
    echo "## VM partition — $TS"
    echo "- error: ssh failed: $(head -c 200 "$TMP")"
    echo
  } >> "$OUT"
  tail -n 200 "$OUT" > "$OUT.tmp" && mv "$OUT.tmp" "$OUT"
  exit 0
}

# Extract fleet JSON for public mirror
FLEET_JSON=$(/opt/homebrew/bin/python3.11 - "$TMP" <<'PY'
import json, sys
with open(sys.argv[1]) as f: raw = f.read()
parts = raw.split("---FLEET---\n")
rest = parts[1] if len(parts) > 1 else ""
parts2 = rest.split("---LEDGER---\n")
fleet_raw = parts2[0].strip() if parts2 else "{}"
try:
    fleet = json.loads(fleet_raw) if fleet_raw else {}
except Exception:
    fleet = {}
print(json.dumps(fleet))
PY
)
echo "$FLEET_JSON" > "$PUBLIC_DIR/fleet_status_vm.json"

/opt/homebrew/bin/python3.11 - "$TMP" "$TS" "$OUT" <<'PY'
import json, sys
raw_path, ts, out_path = sys.argv[1:4]
with open(raw_path) as f:
    raw = f.read()
parts = raw.split("---FLEET---\n")
pid = parts[0].strip()
rest = parts[1] if len(parts) > 1 else ""
parts2 = rest.split("---LEDGER---\n")
fleet_raw = parts2[0].strip()
ledger_raw = parts2[1].strip() if len(parts2) > 1 else ""
try:
    fleet = json.loads(fleet_raw) if fleet_raw else {}
except Exception:
    fleet = {"parse_error": fleet_raw}
try:
    ledger = json.loads(ledger_raw) if ledger_raw else None
except Exception:
    ledger = {"parse_error": ledger_raw}
out = {
    "ts": ts,
    "pid": pid or "DOWN",
    "fleet": fleet,
    "ledger_tail": ledger,
}
with open(out_path, "a") as f:
    f.write(f"## VM partition — {out['ts']}\n")
    f.write("- vm_data:\n")
    f.write(json.dumps(out, indent=2) + "\n\n")
PY

tail -n 200 "$OUT" > "$OUT.tmp" && mv "$OUT.tmp" "$OUT"
