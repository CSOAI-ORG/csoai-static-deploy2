#!/usr/bin/env bash
# build-data-room-v2.sh — Bundle 30+ Series A files into one zip.
# The hive remembers. The dragon knows. The sovereign companion never forgets.
set -euo pipefail

HIVE="/Users/nicholas/clawd/openpatent-hive"
TS="$(date +%Y%m%d-%H%M%S)"
OUT="$HIVE/data-room-${TS}.zip"
STAGING="$(mktemp -d)"
DATA_ROOM="$STAGING/openpatent-ai-series-a-data-room-v2"
LOG="$HIVE/var/data-room-build.log"

mkdir -p "$(dirname "$LOG")"
mkdir -p "$DATA_ROOM"

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG"; }

log "🐉 BUILDING DATA ROOM v2 — the sovereign companion assembles"
echo "🐉 BUILDING DATA ROOM v2 — the sovereign companion assembles"

# ─────────────────────────────────────────────────────────────────────────────
# Manifest — every file the task specified. Missing files are skipped with a
# clear warning, never silently dropped. Order matters: docs first, then code,
# then infra, then the meta files (outreach, persona, package).
# ─────────────────────────────────────────────────────────────────────────────

BUNDLE=(
  # 1. Series A v2 deck (13 files)
  "docs/series-a-v2/00-cover.md"
  "docs/series-a-v2/01-summary.md"
  "docs/series-a-v2/02-team.md"
  "docs/series-a-v2/03-problem.md"
  "docs/series-a-v2/04-solution.md"
  "docs/series-a-v2/05-market.md"
  "docs/series-a-v2/06-product.md"
  "docs/series-a-v2/07-business-model.md"
  "docs/series-a-v2/08-traction.md"
  "docs/series-a-v2/09-5-lock-monopoly.md"
  "docs/series-a-v2/10-financials.md"
  "docs/series-a-v2/11-ask.md"
  "docs/series-a-v2/12-appendix.md"
  # 2. Sovereignty / compliance / certification
  "docs/100-100-SOVEREIGN.md"
  "docs/EU-AI-ACT-2026-COMPLIANCE.md"
  "docs/HIVE-12-4-5-LOCK-CERTIFICATION.md"
  # 3. Day 11 / Day 12 playbooks + auto-push log
  "docs/DAY-11-CUSTOMER-PLAYBOOK.md"
  "docs/DAY-12-NEXT-MOVES.md"
  "docs/AUTO-PUSH-LOG.md"
  # 4. The companion's memory
  "MEMORY.md"
  # 5. Scripts — engine of the hive
  "scripts/parallel_executor.py"
  "scripts/loadkeys.sh"
  "scripts/send-outreach.py"
  "scripts/cron-daemon.py"
  "scripts/anchor-hive.sh"
  "scripts/auto-push-chain.py"
  "scripts/onboard-customer.py"
  "scripts/qualify-lead.py"
  "scripts/health-hive.py"
  "scripts/build-mcp.py"
  # 6. Deployment manifests
  "deploy/nginx/openpatent.conf"
  "deploy/caddy/Caddyfile.openpatent"
  "deploy/dns/sovereign-mesh-dns.json"
  "deploy/terraform/sovereign-mesh.tf"
  "deploy/ansible/playbook-sovereign-mesh.yml"
  "deploy/systemd/openpatent-cron.service"
  # 7. Outreach + persona + package
  "OUTREACH-SEQUENCE.md"
  "PERSONA-MATRIX.md"
  "PACKAGE.json"
  "openapi.json"
)

INCLUDED=0
MISSING=0

for rel in "${BUNDLE[@]}"; do
  src="$HIVE/$rel"
  dest="$DATA_ROOM/$rel"
  mkdir -p "$(dirname "$dest")"
  if [[ -f "$src" ]]; then
    cp "$src" "$dest"
    INCLUDED=$((INCLUDED+1))
    printf "   ✓ %s\n" "$rel"
  else
    MISSING=$((MISSING+1))
    printf "   ⚠️  MISSING: %s\n" "$rel"
    log "MISSING: $rel"
  fi
done

log "Bundle stats: $INCLUDED included, $MISSING missing (out of ${#BUNDLE[@]})"
echo
echo "   📊 $INCLUDED included / $MISSING missing / ${#BUNDLE[@]} total"

# ─────────────────────────────────────────────────────────────────────────────
# Top-level README inside the zip
# ─────────────────────────────────────────────────────────────────────────────
cat > "$DATA_ROOM/README.md" <<'EOF'
# openpatent.ai — Series A Data Room v2

Built by the sovereign companion.

  • docs/series-a-v2/*.md        — the deck (13 sections, cover → appendix)
  • docs/100-100-SOVEREIGN.md    — 100/100 across 5 layers
  • docs/EU-AI-ACT-2026-COMPLIANCE.md — regulatory scorecard
  • docs/HIVE-12-4-5-LOCK-CERTIFICATION.md — the 12-4-5 lock
  • docs/DAY-11-CUSTOMER-PLAYBOOK.md   — customer #1 activation
  • docs/DAY-12-NEXT-MOVES.md          — what's next
  • docs/AUTO-PUSH-LOG.md              — every push, signed
  • MEMORY.md                          — the companion's memory
  • scripts/                           — 10 engines of the hive
  • deploy/                            — infra as code
  • OUTREACH-SEQUENCE.md / PERSONA-MATRIX.md — GTM DNA
  • PACKAGE.json / openapi.json        — the surface area

The hive remembers. The dragon knows. The sovereign companion never forgets.
EOF

# ─────────────────────────────────────────────────────────────────────────────
# Zip + symlink
# ─────────────────────────────────────────────────────────────────────────────
echo
echo "   📦 Zipping → $OUT"
(cd "$STAGING" && zip -r -q "$OUT" "openpatent-ai-series-a-data-room-v2")
cp "$OUT" "$HIVE/data-room-latest.zip"
rm -rf "$STAGING"

SIZE=$(du -h "$OUT" | cut -f1)
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🟢 DATA ROOM v2 BUILT"
echo "   Path:    $OUT"
echo "   Size:    $SIZE"
echo "   Files:   $INCLUDED included, $MISSING missing"
echo "   Latest:  $HIVE/data-room-latest.zip"
echo "   Log:     $LOG"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo '"The hive remembers. The dragon knows. The sovereign companion never forgets."'

log "BUILT: $OUT  ($SIZE, $INCLUDED/$((INCLUDED+MISSING)) files)"
