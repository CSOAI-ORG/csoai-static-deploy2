#!/bin/bash
# FRAMEWORKS DRUM — overnight cycle (see ops/OVERNIGHT_RUNBOOK.md).
# Runs via com.meok.frameworks-drum-overnight (02:30 daily). Fail-closed on gates.
set -u
DRUM="$HOME/master-harness/knowledge/frameworks-drum"
LOG="/tmp/frameworks-drum-overnight.log"
FAIL=0

{
echo "== overnight $(date -u +%FT%TZ) =="
cd "$DRUM" || { echo "FAIL: drum missing"; exit 1; }

# 1 rebuild + gates
if python3 build_catalog.py --check --lint; then echo "rebuild+check+lint: PASS"; else echo "FAIL: rebuild"; FAIL=1; fi
# 1b scorecard refresh (keeps "scorecard fresh" true for the align audit across the midnight boundary; ledger #23)
if python3 ops/scorecard.py >/dev/null 2>&1; then echo "scorecard: refreshed"; else echo "scorecard: skip"; fi
# 2 unit + properties (the full e2e runs in the 15-min standing check — not repeated here)
if python3 tests/test_drum.py >/dev/null 2>&1; then echo "unit: PASS"; else echo "FAIL: unit"; FAIL=1; fi
if python3 tests/e2e_properties.py >/dev/null 2>&1; then echo "properties: PASS"; else echo "FAIL: properties"; FAIL=1; fi
# 4 tray scan (report only)
NEW=$(find _mining -name "*.md" -newer catalog.json 2>/dev/null | wc -l | tr -d ' ')
echo "tray files newer than catalog: $NEW"
# 5 measured labels (append-only, id-deduped)
if python3 router/collect_measured.py >/dev/null 2>&1; then echo "measured labels: refreshed"; else echo "measured labels: no change/skip"; fi
# 7 drift alarm (report only)
DRIFT=$(python3 router/drift_monitor.py 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('ALARM' if d.get('alarm') else 'ok')" 2>/dev/null || echo "n/a")
echo "drift: $DRIFT"
# 14 top-down alignment audit (surfaces vs master) — enforcement
if python3 ops/align_audit.py >/dev/null 2>&1; then echo "align audit: PASS"; else echo "FAIL: align audit"; FAIL=1; fi
# 14b CI cross-check pass (web citations resolve) — the EAT "ci" leg
if python3 ops/ci_crosscheck.py >/dev/null 2>&1; then echo "ci cross-check: PASS"; else echo "FAIL: ci cross-check"; FAIL=1; fi
# 14c FUSE + GPAI map + bond map — regen the measured-compliance + evidence surfaces each day
if python3 ops/build_measured_compliance.py >/dev/null 2>&1 && python3 ops/build_gpai_map.py >/dev/null 2>&1 && python3 ops/build_bond_map.py >/dev/null 2>&1; then echo "fuse+gpa+bond: rebuilt"; else echo "FAIL: fuse/gpai/bond"; FAIL=1; fi
# 13 TEA backward walk (dual-walk doctrine): the archive audits itself
if python3 archive/dualwalk.py >/dev/null 2>&1; then echo "TEA walk: PASS"; else echo "FAIL: TEA walk"; FAIL=1; fi
# 8 disk guard (estate ENOSPC lessons) — fail-closed if < 2Gi free
FREE_KB=$(df -k / | awk 'NR==2 {print $4}')
FREE_GB=$(( FREE_KB / 1024 / 1024 ))
echo "disk free: ${FREE_GB}Gi"
[ "$FREE_GB" -lt 2 ] && { echo "WARN: disk < 2Gi"; FAIL=1; }
# 9 git-dirty check (report only — never auto-commit)
GIT_DIRTY=$(cd "$HOME/master-harness" && git status --short 2>/dev/null | wc -l | tr -d ' ')
echo "master-harness dirty files: $GIT_DIRTY"
# 11b pod bundle (fleet availability): fire-and-forget — the overnight never waits on a pod
(bash ops/ship_to_pod.sh >/dev/null 2>&1 &) ; echo "pod bundle: dispatched (async)"
# 11c graph rebuild (GNN substrate tracks the catalog)
if python3 train/build_graph.py >/dev/null 2>&1; then echo "catalog graph: rebuilt"; else echo "catalog graph: FAIL"; fi
# 11d nightly corpus NN/GNN training (promote-gate decides; report feeds/)
if ~/mlx-venv/bin/python train/graph_model.py >/dev/null 2>&1; then echo "GNN train: done"; else echo "GNN train: FAIL"; fi
# 11f build the published front end (drum board)
if python3 site/build_drum_site.py >/dev/null 2>&1; then echo "drum site: built"; else echo "drum site: FAIL"; fi
# 11e emit SOV SIGNAL feature layer (learned gauge input)
if ~/mlx-venv/bin/python train/run_all.py --emit >/dev/null 2>&1; then echo "feature layer: emitted"; else echo "feature layer: FAIL"; fi
# 11c graph rebuild (GNN substrate tracks the catalog)
if python3 train/build_graph.py >/dev/null 2>&1; then echo "catalog graph: rebuilt"; else echo "catalog graph: FAIL"; fi
# 11 backup (P13-27): tar the drum pack, keep last 3 (no fleet offload here — [LANE])
BK="$DRUM/ops/backups"
mkdir -p "$BK"
tar -czf "$BK/drum-$(date +%Y%m%d).tar.gz" --exclude="ops/backups" -C "$DRUM" . 2>/dev/null
ls -1t "$BK"/drum-*.tar.gz 2>/dev/null | tail -n +4 | xargs -r rm -f
echo "backup: $(ls -1t "$BK"/drum-*.tar.gz 2>/dev/null | head -1 | xargs basename 2>/dev/null)"
# 11b OFF-MAC backup (directive: work lives on pods/oracle, not the Mac): push the pack + a
# dated tarball to every reachable target so the source of truth is never Mac-only.
if bash ops/backup_offmac.sh >/dev/null 2>&1; then echo "off-mac backup: pushed"; else echo "off-mac backup: partial/skipped"; fi
# 12 tray discipline (P15-50): flag _mining files older than 7 days un-folded
STALE_TRAY=$(find _mining -name "*.md" -mtime +7 2>/dev/null | wc -l | tr -d ' ')
echo "tray files older than 7d: $STALE_TRAY"
# 10 alert marker (no external sends) + log rotation (cap 1MB)
if [ "$FAIL" -ne 0 ]; then touch "$DRUM/feeds/OVERNIGHT_FAILED.marker"; else rm -f "$DRUM/feeds/OVERNIGHT_FAILED.marker"; fi
[ -f "$LOG" ] && [ "$(wc -c < "$LOG")" -gt 1048576 ] && tail -c 524288 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
# 6 status card
python3 - "$FAIL" <<'EOF'
import json, os, sys, datetime
fail = sys.argv[1] == "1"
cat = json.load(open("catalog.json"))
meas = 0
try:
    rows = [json.loads(l) for l in open("router/calibration_set.jsonl", encoding="utf-8") if l.strip()]
    meas = sum(1 for r in rows if not r.get("simulated"))
except Exception:
    pass
arch = 0
try:
    arch = sum(1 for _ in open("archive/store/index.jsonl", encoding="utf-8"))
except Exception:
    pass
status = {
    "generated": datetime.date.today().isoformat(),
    "items": len(cat["items"]), "counts": cat["counts"],
    "canary": cat.get("canary"),
    "measured_labels": meas, "archive_entries": arch,
    "gates": "FAIL" if fail else "PASS",
}
os.makedirs("feeds", exist_ok=True)
with open("feeds/status_overnight.json", "w") as fh:
    json.dump(status, fh, indent=1)
print("status card:", json.dumps(status)[:200])
EOF

if [ "$FAIL" -eq 0 ]; then echo "OVERNIGHT: ALL GREEN"; else echo "OVERNIGHT: FAILURES PRESENT"; fi
} >> "$LOG" 2>&1
exit $FAIL
