#!/usr/bin/env bash
# art50 grader — wraps the canonical `csoai` CLI (no reimplementation).
# Usage: check.sh <hf-model-repo-id>   e.g. check.sh meta-llama/Llama-3.2-1B
set -euo pipefail
ENTITY="${1:?usage: check.sh <hf-model-repo-id>}"
# csoai check exits 0 = compliant-shaped, 3 = a transparency predicate missing.
csoai check --entity "$ENTITY" --pack art50 --json
