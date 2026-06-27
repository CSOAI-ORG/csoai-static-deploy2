#!/bin/bash
# READY TO FIRE: Resend domain verify for mail.meok.ai
# Time: 30 seconds
# Pre-req: Click verify button in Resend dashboard
# After: API key at RESEND_API_KEY env
set -e
echo "Step 1: Open https://resend.com/domains"
echo "Step 2: Click verify next to meok.ai domain"
echo "Step 3: Copy API key → export RESEND_API_KEY=re_..."
echo ""
echo "After verify, send 5 design-partner emails:"
python3 ~/clawd/_intake/ready_to_fire/04_SEND_EMAILS.py
