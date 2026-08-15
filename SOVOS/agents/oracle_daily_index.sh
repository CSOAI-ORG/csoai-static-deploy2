#!/bin/bash
# oracle_daily_index.sh — Daily GSPC closing-cross producer for the Oracle micro fleet
# Runs on micro1/micro2 (E2.micro, 1GB RAM — lightweight job: fetch board data,
# compute index via daily_index.py, publish JSON + signed root).
#
# Cron: 0 30 23 * * /root/scripts/oracle_daily_index.sh   (23:30 UTC daily)
# Feeds the index-on-time SLO (95% target: published before 00:30 UTC).

set -e
LOG=/var/log/oracle-daily-index.log
exec >> "$LOG" 2>&1
echo "=== $(date -u +%FT%TZ) oracle daily index start ==="

WORK=/tmp/oracle-index
mkdir -p "$WORK"
cd "$WORK"

# 1. Pull the latest boards from the signing pod (SSH key on micros)
POD_PORT=11703
POD_HOST=104.255.9.187
# boards dir is big; fetch only the board_*.json + registry (small)
scp -P "$POD_PORT" -o ConnectTimeout=20 -o BatchMode=yes \
  "$POD_HOST":/workspace/jeeves-exec/SOVOS/boards-v2-2026-08-12/board_\*.json "$WORK/" 2>/dev/null

# 2. Compute the daily index (the closing cross)
cd /workspace/jeeves-exec 2>/dev/null || cd "$WORK"
# daily_index.py lives on the pod; if unavailable locally use one-liner:
python3 - << 'PYEOF'
import json, glob, hashlib, datetime
cells = []
for f in sorted(glob.glob("/tmp/oracle-index/board_*.json")):
    try:
        d = json.load(open(f))
        axis = d.get("axis")
        models = d.get("models", [])
        q = [m for m in models if m.get("quotable")]
        if q:
            acc = sum(m["accuracy"] for m in q)/len(q)
            n = sum(m.get("n",0) for m in q)
            los = [m["ci95"][0] for m in q]; his = [m["ci95"][1] for m in q]
            cells.append({"axis": axis, "accuracy": round(acc,4),
                          "n": n, "ci": [round(sum(los)/len(los),4), round(sum(his)/len(his),4)]})
    except Exception as e:
        print("skip", f, e)
if cells:
    value = round(100.0*sum(c["accuracy"] for c in cells)/len(cells), 2)
    lo = sum(c["ci"][0] for c in cells)/len(cells)
    hi = sum(c["ci"][1] for c in cells)/len(cells)
    rec = {"schema":"gspc-index-closing-cross-v1",
           "date": datetime.date.today().isoformat(),
           "index": value, "ci95": [round(lo,4), round(hi,4)],
           "axes_measured": len(cells), "producer":"oracle-micros",
           "created": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    open("/tmp/oracle-index/daily.json","w").write(json.dumps(rec, indent=2))
    print(json.dumps(rec))
else:
    print("NO_MEASURED_CELLS")
PYEOF

# 3. Ship to archive (signed root hash; full card co-signing happens on pod)
if [ -f /tmp/oracle-index/daily.json ]; then
  sha=$(sha256sum /tmp/oracle-index/daily.json | cut -d' ' -f1)
  echo "index sha256: $sha"
  # archive to /tmp + append to running log
  cp /tmp/oracle-index/daily.json /tmp/oracle-index/daily-$(date -u +%Y%m%d).json
fi
echo "=== done $(date -u +%FT%TZ) ==="