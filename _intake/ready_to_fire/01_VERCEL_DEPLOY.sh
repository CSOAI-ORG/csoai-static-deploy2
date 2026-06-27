#!/bin/bash
# READY TO FIRE: vercel --prod for proofof.ai
# Time: 5 seconds
# Pre-req: You must have run `vercel login` once
set -e
cd ~/clawd/proofof-site
echo "Deploying proofof.ai..."
vercel --prod --yes --force
echo "✅ proofof.ai deployed"
