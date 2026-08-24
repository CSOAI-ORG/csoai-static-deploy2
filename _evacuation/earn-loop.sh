#!/bin/bash
# productive CPU earn — measure/pack/index/MEOK-card/compose support
# CEO 2026-08-23: flap stays paused; no train; no mine; no new pods; no git thrash
set -u
LOG=/workspace/eat-logs/productive-earn.log
OUTDIR=/workspace/overnight-20260823/productive
HARNESS=/workspace/sovos-harness
CYCLE=0
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) earn-loop RESTART pid=$$ host=$(hostname)" | tee -a "$LOG"
cd "$HARNESS"
while true; do
  CYCLE=$((CYCLE+1))
  TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  LOAD=$(cut -d" " -f1-3 /proc/loadavg)
  echo "[$TS] cycle=$CYCLE load=$LOAD" | tee -a "$LOG"

  python3 domain-packs.py >>"$LOG" 2>&1
  python3 enterprise-packs.py >>"$LOG" 2>&1
  DOM_N=$(wc -l < domain-measurements.jsonl 2>/dev/null || echo 0)
  ENT_N=$(wc -l < enterprise-measurements.jsonl 2>/dev/null || echo 0)

  LIST=/tmp/agent-cards.list
  find "$HARNESS" -maxdepth 4 -type f -name agent-card.json 2>/dev/null > "$LIST" || true
  python3 - "$LIST" "$OUTDIR" >>"$LOG" 2>&1 <<'PY2'
import json, sys, time, hashlib
from pathlib import Path
lst, outdir = Path(sys.argv[1]), Path(sys.argv[2])
root = Path("/workspace/sovos-harness")
out = outdir / "card-inventory.jsonl"
rows = []
for line in lst.read_text().splitlines():
    p = Path(line)
    try:
        raw = p.read_bytes()
        data = json.loads(raw.decode("utf-8", errors="replace"))
        name = data.get("name") or data.get("id") or p.parent.name
        rel = str(p.relative_to(root)) if str(p).startswith(str(root)) else str(p)
        rows.append({
            "path": rel,
            "name": name,
            "bytes": len(raw),
            "sha256_12": hashlib.sha256(raw).hexdigest()[:12],
            "has_url": bool(data.get("url") or data.get("endpoint")),
            "skills": len(data.get("skills") or []),
            "signed_hint": bool(data.get("signature") or data.get("signatures") or data.get("attestations")),
            "inventoried_at": int(time.time()),
            "lane": "internal_unsigned_ok",
        })
    except Exception as e:
        rows.append({"path": str(p), "error": str(e)[:120], "inventoried_at": int(time.time())})
rows.sort(key=lambda r: r.get("path", ""))
with out.open("w") as f:
    for r in rows:
        f.write(json.dumps(r, sort_keys=True) + "\n")
summary = {
    "schema": "csoai.card-inventory/0.1",
    "count": len(rows),
    "signed_hint_n": sum(1 for r in rows if r.get("signed_hint")),
    "out": str(out),
    "ts": int(time.time()),
}
(outdir / "card-inventory-summary.json").write_text(json.dumps(summary, indent=2))
print("  card inventory: %d cards -> %s (signed_hint=%d)" % (summary["count"], out, summary["signed_hint_n"]))
PY2

  if [ -f scripts/generate-mcp-compose.py ]; then
    timeout 60 python3 scripts/generate-mcp-compose.py >>"$LOG" 2>&1       || echo "  compose regen: skip/timeout (logged)" | tee -a "$LOG"
  fi

  python3 - "$OUTDIR" >>"$LOG" 2>&1 <<'PY3'
import hashlib, json, time, sys
from pathlib import Path
d = Path(sys.argv[1])
idx = []
for p in sorted(d.iterdir()):
    if p.is_file() and p.name not in ("earn-index.json", "earn-loop.sh", "earn-loop.pid"):
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
        idx.append({"name": p.name, "bytes": p.stat().st_size, "sha16": h})
blob = {"schema": "csoai.productive-index/0.1", "ts": int(time.time()), "files": idx}
(d / "earn-index.json").write_text(json.dumps(blob, indent=2))
print("  index: %d files hashed -> earn-index.json" % len(idx))
PY3

  timeout 30 python3 /workspace/scitt-register.py >>"$LOG" 2>&1 || echo "  scitt: board fetch fail/timeout (logged)" | tee -a "$LOG"

  echo "[$TS] cycle=$CYCLE DONE domain_jsonl=$DOM_N enterprise_jsonl=$ENT_N" | tee -a "$LOG"
  sleep 120
done
