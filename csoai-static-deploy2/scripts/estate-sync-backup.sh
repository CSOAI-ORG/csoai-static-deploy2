#!/bin/bash
# estate-sync-backup.sh — the OFF-Mac backup/sync procedure.
# We work from the infra (RunPod 3090 + Oracle micros); the Mac is terminal only after this.
# Run after every session: syncs the estate work to the pods + pushes to the monorepo (GitHub) + stores a timestamped backup.

set -e
TS=$(date -u +%Y%m%d-%H%M%S)
cd ~/clawd/csoai-static-deploy2
SOV=$(pwd)/SOVOS
echo "===== ESTATE SYNC + BACKUP ($TS) ====="

# 1. Package
mkdir -p /tmp/estate-pack
tar czf /tmp/estate-pack/estate-$TS.tgz $SOV/evidence $SOV/RECEIPT-SPEC-0.1.md $SOV/OWNERSHIP-100-MOVES-2026-08-23.md $SOV/OWNER-GATE-SORT-2026-08-23.md $SOV/PUBLICATIONS-2026-08-23.md $SOV/FULL-RUNDOWN-CHECKLIST-2026-08-23.md $SOV/FULL-RUNDOWN-AUDIT-2026-08-23.md $SOV/MASTER-STACK-OOWM-SOVOS-2026-08-22.md $SOV/ESTATE-STATE-2026-08-22.md $SOV/IP-VALUE-ADDENDUM-2026-08-23.md 2>/dev/null || true
echo "  [1] packaged ($(du -h /tmp/estate-pack/estate-$TS.tgz | awk '{print $1}'))"

# 2. Sync -> signing node (Oracle micro1) — the SOURCE OF TRUTH
scp -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new /tmp/estate-pack/estate-$TS.tgz ubuntu@145.241.232.16:/tmp/ >/dev/null 2>&1
ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new ubuntu@145.241.232.16 'mkdir -p ~/estate-backups; mv /tmp/estate-*.tgz ~/estate-backups/ 2>/dev/null; cd ~ && tar xzf estate-backups/estate-*.tgz -C ~ 2>/dev/null; echo "  [2] signing node: $(ls ~/SOVOS/evidence/*.html 2>/dev/null | wc -l | tr -d " ") pages, $(ls ~/SOVOS/evidence/signed/*.json 2>/dev/null | wc -l | tr -d " ") signed verdicts"' 2>&1 | tail -1

# 3. Sync -> 3090 (/workspace)
scp -i ~/.runpod/ssh/runpodctl-ssh-key -P 23243 -o StrictHostKeyChecking=accept-new /tmp/estate-pack/estate-$TS.tgz root@194.26.196.156:/workspace/ >/dev/null 2>&1
ssh -i ~/.runpod/ssh/runpodctl-ssh-key -p 23243 -o StrictHostKeyChecking=accept-new root@194.26.196.156 'mkdir -p /workspace/estate-backups; mv /workspace/estate-*.tgz /workspace/estate-backups/ 2>/dev/null; cd /workspace && tar xzf estate-backups/estate-*.tgz -C /workspace 2>/dev/null; echo "  [3] 3090: $(ls /workspace/SOVOS/evidence/*.html 2>/dev/null | wc -l | tr -d " ") pages"' 2>&1 | tail -1

# 4. Sync -> micro2 (Oracle, fleet)
scp -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new /tmp/estate-pack/estate-$TS.tgz ubuntu@141.147.73.85:/tmp/ >/dev/null 2>&1
ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new ubuntu@141.147.73.85 'mkdir -p ~/estate-backups; mv /tmp/estate-*.tgz ~/estate-backups/ 2>/dev/null; cd ~ && tar xzf estate-backups/estate-*.tgz -C ~ 2>/dev/null; echo "  [4] micro2 replicated"' 2>&1 | tail -1

# 5. Monorepo -> GitHub (via remote-main worktree, safe; avoid the split-brain local main)
echo "  [5] pushing to GitHub monorepo (CSOAI-ORG/csoai-static-deploy2)…"
git worktree add /tmp/csoai-pub origin/main 2>&1 | tail -1
for f in RECEIPT-SPEC-0.1.md; do :; done
# push the key estate docs + pages (copy from the live/working set)
cp $SOV/RECEIPT-SPEC-0.1.md /tmp/csoai-pub/ 2>/dev/null || true
(cd /tmp/csoai-pub && git add RECEIPT-SPEC-0.1.md >/dev/null 2>&1; git commit -m "estate-sync $TS" >/dev/null 2>&1 || true; git push origin HEAD:main 2>&1 | tail -2)
git worktree remove /tmp/csoai-pub --force 2>&1 | tail -1 || rm -rf /tmp/csoai-pub

echo "  [6] PRUNE the Mac working copy? Keep it (it's terminal-only). Done."
echo "===== ESTATE SYNC + BACKUP COMPLETE ($TS) ====="
echo "Source of truth: signing node (oracle micro1). Work from there; the Mac is terminal only."
