#!/usr/bin/env bash
# oracle-mesh-activate.sh — Activate Oracle Always-Free micros as the £0 always-on mesh
# 
# Runs: on the A100 pod (which has oci CLI, or via direct OCI API)
# What: gets Oracle micro VNIC IPs, deploys city report cron + verify_record MCP
#
# The two micros: sov33-owem-micro, sov33-owem-micro2 (E2.Micro, 1GB RAM)
# Jobs for the free mesh: Daily City Report, verify_record MCP, Sigsum witness

set -euo pipefail
cd /workspace/jeeves-exec/SOVOS
LOG="/workspace/jeeves-exec/SOVOS/logs/oracle-mesh-$(date +%Y%m%d-%H%M).log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

log "═══ Oracle mesh activation ═══"

# Verify oci CLI is available
if ! command -v oci &>/dev/null; then
    log "oci CLI not found — trying via pip"
    pip install oci -q 2>/dev/null && log "oci installed" || log "oci NOT AVAILABLE — will try via SSH key"
fi

# Find the compartment
COMPARTMENT=$(grep -E '^compartment' ~/.oci/config 2>/dev/null | head -1 | cut -d= -f2 | tr -d ' ' || echo "")

# Alternate: SSH direct if we know the key and the micros accept it
# Oracle micros use the SSH key at ~/.ssh/id_rsa (or we upload)
log "Looking for Oracle micro IPs..."
# Try via direct OCI API call
if command -v oci &>/dev/null; then
    INSTANCE_IDS=$(oci compute instance list --compartment-id "$COMPARTMENT" --region uk-london-1 \
        --query 'data[?contains(`"display-name"`, `sov33`)].id' --output json 2>/dev/null || echo "[]")
    if [ "$INSTANCE_IDS" != "[]" ]; then
        for INST_ID in $(echo "$INSTANCE_IDS" | python3 -c "import json,sys; [print(i) for i in json.load(sys.stdin)]" 2>/dev/null); do
            IP=$(oci compute instance list-vnics --instance-id "$INST_ID" --region uk-london-1 \
                --query 'data[0]."public-ip"' --output json 2>/dev/null | tr -d '"' || true)
            if [ -n "$IP" ]; then
                log "Found micro at $IP"
                echo "$IP" >> /tmp/oracle-ips.txt
            fi
        done
    fi
fi

if [ ! -f /tmp/oracle-ips.txt ]; then    log "Could not resolve Oracle IPs — will try again at next cron cycle"
    log "Set up pending: Daily City Report, verify_record MCP, Sigsum witness"
    log "Run this script again after Oracle IPs are known"
    exit 1
fi

# Deploy to each micro
for IP in $(cat /tmp/oracle-ips.txt 2>/dev/null); do
    log "Syncing to $IP..."
    scp -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new \
        agents/city_bank.py agents/verify_record_proxy.py \
        ubuntu@$IP:/home/ubuntu/ 2>/dev/null || log "SSH to $IP failed"
    
    # Install crontab
    ssh -o ConnectTimeout=10 ubuntu@$IP "crontab -l 2>/dev/null | cat - <(echo '0 */4 * * * cd /home/ubuntu && python3 city_bank.py >> city_report.log 2>&1'
    # Every 4h: city report + verify witness
    (crontab -l 2>/dev/null; echo '0 */4 * * * cd /home/ubuntu && python3 city_bank.py >> city_report.log 2>&1'
     (crontab -l 2>/dev/null; echo '30 */6 * * * cd /home/ubuntu && python3 verify_record_proxy.py >> verify.log 2>&1'
) | crontab -" 2>/dev/null || log "crontab setup failed for $IP"
done

log "═══ Oracle mesh activation complete �══"