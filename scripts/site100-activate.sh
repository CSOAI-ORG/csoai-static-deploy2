#!/bin/bash
# SITE100-ACTIVATE — activate on-disk domain site builds via GitHub Pages.
# Doctrine: fail-closed (no secrets pushed), additive only (no deletion), verified live.
# Each site: repo CSOAI-ORG/<name>-site on main branch -> Pages enabled -> github.io 200.
set -uo pipefail
ORG="CSOAI-ORG"
LOG="$HOME/clawd/site100-activation.log"
echo "=== SITE100 ACTIVATION $(date -u +%FT%TZ) ===" | tee -a "$LOG"

# <name> <deploy-dir>
SITES=(
  "loopfactory|loopfactory-deploy"
  "landlaw|landlaw-deploy"
  "commercialvehicle|commercialvehicle-deploy"
  "pokerhud|pokerhud-deploy"
  "diyhelp|diyhelp-deploy"
  "planthire|planthire-deploy"
  "koikeeper|koikeeper-deploy"
  "biasdetectionof|biasdetectionof-deploy"
  "suicidestop|suicidestop-deploy"
  "optimobile|optimobile-deploy"
  "cobolbridge|cobolbridge-deploy"
  "accountabilityof|accountabilityof-deploy"
  "dataprivacyof|dataprivacyof-deploy"
  "ethicalgovernanceof|ethicalgovernanceof-deploy"
  "transparencyof|transparencyof-deploy"
  "socialmediamanager|socialmediamanager-deploy"
)

scan_secrets() { # dir -> 0 clean / 1 dirty
  local d="$1"
  grep -rIl -e "PRIVATE KEY" -e "sk_live" -e "sk-" -e "AKIA" -e "api[_-]key[[:space:]]*[:=]" -e "token[[:space:]]*[:=][[:space:]]*[A-Za-z0-9]\{20,\}" -e "\.env" "$d" 2>/dev/null | grep -v -e "\.well-known/mcp.json" -e "agent-card.json" -e "agent.json" -e "llms.txt" | head -3
}

activate() {
  local name="$1" dir="$2"
  local repo="$name-site" src="$HOME/clawd/$dir"
  echo "--- $name ---" | tee -a "$LOG"
  [ -d "$src" ] || { echo "SKIP: no $src" | tee -a "$LOG"; return 1; }
  [ -f "$src/index.html" ] || { echo "SKIP: no index.html in $src" | tee -a "$LOG"; return 1; }
  local dirty; dirty=$(scan_secrets "$src")
  if [ -n "$dirty" ]; then
    echo "SKIP: secret scan flagged: $dirty" | tee -a "$LOG"
    return 1
  fi
  if gh repo view "$ORG/$repo" --json name --jq .name >/dev/null 2>&1; then
    echo "repo exists: $repo" | tee -a "$LOG"
  else
    gh repo create "$ORG/$repo" --public --confirm 2>&1 | tee -a "$LOG" || { echo "FAIL create $repo" | tee -a "$LOG"; return 1; }
  fi
  local tmp; tmp=$(mktemp -d)
  cp -R "$src"/. "$tmp"/ 2>/dev/null
  # strip any stray git state so only static content lands on main
  rm -rf "$tmp/.git" "$tmp/node_modules" 2>/dev/null
  cd "$tmp" || return 1
  git init -q -b main
  git add -A
  git -c user.name="CSOAI-ORG" -c user.email="cs-oai-org@users.noreply.github.com" commit -qm "site: $name static build"
  if ! git push -q "https://github.com/$ORG/$repo.git" main 2>>"$LOG"; then
    echo "FAIL push $repo" | tee -a "$LOG"
    cd / && rm -rf "$tmp"; return 1
  fi
  # enable Pages (idempotent; ignore if already enabled)
  gh api -X POST "repos/$ORG/$repo/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>>"$LOG" || true
  echo "pushed + pages enabled: https://$ORG.github.io/$repo/" | tee -a "$LOG"
  cd / && rm -rf "$tmp"
}

for s in "${SITES[@]}"; do
  name="${s%%|*}"; dir="${s##*|}"
  activate "$name" "$dir"
done
echo "=== DONE $(date -u +%FT%TZ) ===" | tee -a "$LOG"
