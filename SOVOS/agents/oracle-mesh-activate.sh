#!/usr/bin/env bash
# oracle-mesh-activate.sh — Activate Oracle Always-Free micros as the £0 always-on mesh
set -euo pipefail
cd /workspace/jeeves-exec/SOVOS
LOG="/workspace/jeeves-exec/SOVOS/logs/oracle-mesh-$(date +%Y%m%d-%H%M).log"
COMPARTMENT="${1:-}"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }
log "═══ Oracle mesh activation ═══"

# Try to find compartment from config if not provided
if [ -z "$COMPARTMENT" ]; then
    COMPARTMENT=$(grep -E '^compartment' ~/.oci/config 2>/dev/null | head -1 | cut -d= -f2 | tr -d ' ' || echo "tenancy")
    if [ "$COMPARTMENT" = "tenancy" ]; then
        COMPARTMENT=$(grep 'tenancy' ~/.oci/config | head -1 | cut -d= -f2 | tr -d ' ')
    fi
fi

# Get instance IPs via OCI CLI
if command -v oci &>/dev/null; then
    INSTANCE_IDS=$(oci compute instance list --compartment-id "$COMPARTMENT" --region uk-london-1 \
        --query 'data[?contains(`"display-name"`, `sov33`) || contains(`"display-name"`, `micro`)].id' \
        --output json 2>/dev/null || echo "[]")
    if [ "$(echo "$INSTANCE_IDS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo 0)" -gt 0 ]; then
        for INST_ID in $(echo "$INSTANCE_IDS" | python3 -c "import json,sys; [print(i) for i in json.load(sys.stdin)]" 2>/dev/null); do
            IP=$(oci compute instance list-vnics --instance-id "$INST_ID" --region uk-london-1 \
                --query 'data[0]."public-ip"' --output json 2>/dev/null | tr -d '"' || true)
            if [ -n "$IP" ] && [ "$IP" != "null" ]; then
                log "Oracle micro found: $IP"
                echo "$IP" >> /tmp/oracle-ips.txt
            fi
        done
    fi
fi

if [ ! -s /tmp/oracle-ips.txt ]; then
    log "Could not resolve Oracle IPs this cycle — will retry next autonomous tick"
    log "Oracle route: export COMPARTMENT_OCID=ocid1.compartment.oc1..XXXXX && bash $0 \$COMPARTMENT_OCID"
    exit 1
fi

# Set up jobs on each reachable micro
for IP in $(sort -u /tmp/oracle-ips.txt 2>/dev/null); do
    log "Connecting to $IP..."
    ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 ubuntu@$IP "
        echo 'Connected to \$(hostname)'
        # Install python3 + city deps
        which python3 || (apt-get update -qq && apt-get install -y -qq python3 python3-pip)
        # Deploy city report cron (every 4h)
        crontab -l 2>/dev/null | cat - <(echo '0 */4 * * * cd \\\$HOME && python3 -c \"import urllib.request,json; print(json.dumps({\\\\"oracle_city\\\":True,\\\\"ts\\\":\\\"\\\"+__import__(\\\\\"datetime\\\\\").datetime.now().isoformat()}))\" >> city_report.log 2>&1') | sort -u | crontab -
        echo 'Cron deployed'
    " 2>&1 | tee -a "$LOG" || log "Failed to reach $IP via SSH"
done

log "═══ Oracle mesh activation cycle complete ═══"