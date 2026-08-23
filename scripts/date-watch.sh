#!/bin/bash
# Date-watch: daily reminder of the estate's hard clocks (canon HS.6 / TODAY war plan)
D=$(date -u +%F)
echo "=== DATE WATCH $D ==="
python3 - <<'PY'
from datetime import date
t = date.today()
checks = [
    ("RealPDE Track 2 form (NICK)", date(2026,8,20)),
    ("arXiv endorsement (Moon, NICK)", date(2026,8,27)),
    ("DRCF consultation", date(2026,9,2)),
    ("NeMo Gym v0.6.0", date(2026,9,2)),
    ("Growth Lab window", date(2026,9,27)),
    ("OpenAI Evals read-only", date(2026,10,31)),
    ("OpenAI Evals GONE", date(2026,11,30)),
    ("Art 50 grace ends", date(2026,12,2)),
    ("Illinois SB 315 effective", date(2027,1,1)),
]
for name, d in checks:
    dd = (d - t).days
    flag = "🔴" if dd <= 3 else ("🟡" if dd <= 14 else "🟢")
    if name.startswith("RealPDE"):
        print("  ✅ " + name + " — SUBMITTED (owner-confirmed 19 Aug)")
    else:
        print(f"  {flag} {name}: {dd}d ({d})")
PY
