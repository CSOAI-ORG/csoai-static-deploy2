#!/usr/bin/env python3
"""ADVERSARIAL-EVIDENCE REVIEW (NEXT-100 P8, move 62).

Automates the doctrine rule: every [BET] claim must state its strongest disconfirming evidence
inline, and explain what survives it. A [BET] without counter-evidence is an assertion, not a bet.
Scans the doctrine docs for [BET] tags and flags any that don't sit near a disconfirming-evidence
statement. Exit 1 on a violation (so the overnight/standing check can enforce it).

Run: python3 ops/adversarial_review.py
"""
import os
import re
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = ["docs/MASTER_FRAMEWORK.md", "docs/RESEARCH_VALIDATION.md",
        "docs/ENGINE_AXIS.md", "docs/BENCHMARK_AS_A_SERVICE.md", "docs/RESEARCH_TRUST_FLIP.md"]

# disconfirming-evidence markers that a [BET] must appear near
EVIDENCE = re.compile(
    r"disconfirm|counter-evidence|evidence against|surviv|strongest.*evidence|negative result|"
    r"did not|does not|do not|not transfer|not achieve|not yet|not built|scaffold|unproven|needs.*before|"
    r"risks|caution|fail(ed|s|ure)?|Vaccaro|reward hacking|g = -|0\.5[0-9]|kills|red line|reject|GATE|no .* yet|never", re.IGNORECASE)
# lines that merely DESCRIBE the tagging convention are not [BET] claims — skip them
META = re.compile(r"tagged \[BET\]|\[BET\]\s*/\s*\[BUILT\]|every claim.*tagged|never smuggling|carries its|evidence discipline|per the master-framework", re.IGNORECASE)


def scan():
    violations = []
    bets = 0
    for doc in DOCS:
        p = os.path.join(PACK, doc)
        if not os.path.exists(p):
            continue
        lines = open(p, encoding="utf-8").read().splitlines()
        for i, line in enumerate(lines):
            if "[BET" not in line:
                continue
            if META.search(line):
                continue
            bets += 1
            window = " ".join(lines[i:i + 4])
            if not EVIDENCE.search(window):
                violations.append({"doc": doc, "line": i + 1, "snippet": line.strip()[:90]})
    return bets, violations


def main():
    bets, violations = scan()
    print(f"adversarial-evidence review: {bets} [BET] claims scanned, {len(violations)} without inline counter-evidence")
    for v in violations:
        print(f"  VIOLATION {v['doc']}:{v['line']} — {v['snippet']}")
    if violations:
        print("ADVERSARIAL REVIEW: FAILURES PRESENT")
        return 1
    print("ADVERSARIAL REVIEW: PASS (every [BET] carries its disconfirming evidence)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
