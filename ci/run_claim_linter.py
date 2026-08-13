#!/usr/bin/env python3
"""G4 claim-linter CI gate: fail on any count-conflation against the numbers registry.

Exit 0 = clean (or only expected historical-record hits), 1 = a real conflation
was found that needs fixing before merge. Mirrors the G3 counter-canon gate.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "SOVOS" / "agents"))

from claim_linter import lint, load_registry  # noqa: E402

def main() -> int:
    registry = load_registry(ROOT / "SOVOS" / "GSPC_NUMBERS_REGISTRY.json")
    contrad, files = lint(ROOT / "SOVOS", registry)
    # FORBIDDEN public-codename hits are ALWAYS real (legal/brand): fail CI
    real = [c for c in contrad if c["pattern"].startswith("FORBIDDEN") or "superseded" not in c["canonical_or_note"]]
    if real:
        for x in real[:25]:
            print(f"::error::CONFLATION {x['file']}: {x['pattern']} -> {x['canonical_or_note']}")
            print(f"  ...{x['hit']}")
        print(f"claim-linter: {len(files)} scanned, {len(contrad)} hits, {len(real)} real conflation — FAIL")
        return 1
    print(f"claim-linter: {len(files)} files scanned, {len(contrad)} informational ({len(files)} clean) — PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())