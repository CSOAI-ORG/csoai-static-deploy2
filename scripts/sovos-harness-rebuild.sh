#!/bin/bash
# sovos-harness-rebuild — run ON pod AFTER mirror completes. Rebuilds the git repo from the
# mirror (hardlink snapshot), pushes full estate to GitHub. Harness is DERIVED, never canonical:
# the mirror (/workspace/offload-dsh/clawd) is the archive.
set -e
H=/workspace/sovos-harness
M=/workspace/offload-dsh/clawd
git config --global --add safe.directory $H 2>/dev/null || true

rm -rf $H/.git 2>/dev/null || true
find $H -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} + 2>/dev/null || true

cat > $H/.gitignore << 'GI'
*.safetensors
*.gguf
*.pyc
**/honey_all_producers.jsonl
**/.backups/
**/node_modules/
**/.next/
**/.venv/
__pycache__/
**/sim-world-data/
GI

cp -al $M/. $H/
cd $H && git init -b main
git config user.name "CSOAI-ORG"
git config user.email "sovos@csoai.org"
git add -A
git -c core.hooksPath=/dev/null commit -m "sovos-harness: full estate $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>&1 | tail -2
git push -u origin main --force 2>&1 | tail -2
echo "HARNESS_REBUILT files=$(git ls-files | wc -l) branch=$(git branch --show-current) head=$(git rev-parse --short HEAD)"
