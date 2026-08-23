#!/bin/bash
# sovos-pod-provision — run ON the volume-sink pod (root@213.173.105.83:25804)
# Births the sovos-harness git repo on the volume, pushes to GitHub, wires remote EAT cron.
set -e
H=/workspace/sovos-harness
EATV=/workspace/offload-dsh/eatenv
TOKEN=$(python3 - << 'PY'
import re
s=open('/root/.config/gh/hosts.yml').read()
m=re.search(r'oauth_token:\s*(\S+)', s)
print(m.group(1) if m else '')
PY
)

cd $H
git config --global --add safe.directory /workspace/sovos-harness
if [ -d .git ]; then rm -rf .git; fi  # clean re-init (data preserved; repo metadata may be partial)
git init -b main
git config user.name "CSOAI-ORG"
git config user.email "sovos@csoai.org"
git add -A
git -c core.hooksPath=/dev/null commit -m "sovos-harness: estate monorepo snapshot $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>&1 | head -3 || true
git remote remove origin 2>/dev/null || true
git remote add origin "https://x-access-token:${TOKEN}@github.com/CSOAI-ORG/sovos-harness.git"
git push -u origin main 2>&1 | tail -3
echo "REPO_PUSH_DONE"

# Remote EAT wrapper (stdlib-only; python3.11):
mkdir -p /workspace/eat-logs
cat > /workspace/sovos-eat.sh << 'EOF'
#!/bin/bash
cd /workspace/sovos-harness/csoai-static-deploy2
python3 eat_all.py >> /workspace/eat-logs/eat-$(date -u +%Y%m%d).log 2>&1
echo "[$] remote eat cycle done" >> /workspace/eat-logs/eat-$(date -u +%Y%m%d).log
EOF
chmod +x /workspace/sovos-eat.sh

# Daily pod cron (03:00 UTC) + on-demand now:
(crontab -l 2>/dev/null | grep -v sovos-eat; echo "0 3 * * * /workspace/sovos-eat.sh") | crontab -
echo "EAT_CRON_WIRED"

# Remote training (CPU-safe, background): torch-cpu + transformers, corpus 12 -> retrain -> eval
$EATV/bin/pip install -q torch --index-url https://download.pytorch.org/whl/cpu 2>&1 | tail -1
$EATV/bin/pip install -q transformers 2>&1 | tail -1
cd /workspace/sovos-harness/csoai-static-deploy2
nohup $EATV/bin/python sov_minimal_train.py --steps 150 --output sov-minimal-output-v2 \
  >> /workspace/eat-logs/train-v2.log 2>&1 &
echo "TRAIN_LAUNCHED (bg pid $!)"

# Proof run: one full remote EAT cycle (background, log)
nohup /workspace/sovos-eat.sh >> /workspace/eat-logs/proof-eat-$(date -u +%Y%m%d-%H%M).log 2>&1 &
echo "EAT_PROOF_LAUNCHED"
