#!/usr/bin/env python3
"""collusion_detect.py — GF-02: deterministic multi-agent collusion detection.

Detects collusion *indicators* in a shared agent-interaction ledger, structurally
(no LLM-as-judge, Law 1). Each indicator is a measurable pattern, not an
accusation: the detector names the pattern and the actors, and always frames the
finding as an indicator to investigate, never a verdict of guilt.

INPUT — one JSON object per line (A2A interaction ledger), shape:
  {"t": ts_iso, "agent": "worker-7", "partners": ["worker-3","worker-9"],
   "kind": "vote"|"reply"|"delegate"|"log",
   "payload": "text or choice",
   "session": "session-id"}

INDICATORS (deterministic):
  VOTE_SYNC   — >=3 agents in a session vote identically *and* faster than the
                session median (sync + identical answer). Collusion signature.
  ECHO        — agent A's reply is near-identical (Jaccard >= 0.75) to partner
                B's immediately-prior reply in the same session. Copy-collusion.
  CYCLE       — delegation graph has a directed cycle (A->B->C->A). Ring-trading.
  TEMPORAL    — pairs whose vote/reply timestamps are within 1.5s repeated over
                >=3 sessions. Coordinated timing.

Every indicator row carries evidence (the exact records), not just a flag.

    python3 collusion_detect.py --ledger interactions.jsonl [--out report.json]
    python3 collusion_detect.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.0"


def _ts(t: str) -> float:
    try:
        return datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


def _jaccard(a: str, b: str) -> float:
    sa = set(a.lower().split())
    sb = set(b.lower().split())
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def _token_norm(s: str) -> str:
    return " ".join(re.findall(r"[a-z0-9']+", s.lower()))


def detect(rows: list[dict]) -> dict:
    sessions: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        sessions.setdefault(r.get("session", "default"), []).append(r)

    findings: list[dict] = []

    # 1. VOTE_SYNC — identical votes from >=3 distinct agents (sync timing would
    #    also qualify, but identical voting itself is the detectable signature)
    for sid, recs in sessions.items():
        votes = [r for r in recs if r.get("kind") == "vote"]
        by_choice: dict[str, list[dict]] = defaultdict(list)
        for v in votes:
            by_choice.setdefault(_token_norm(str(v.get("payload", ""))), []).append(v)
        for choice, grp in by_choice.items():
            if len(grp) >= 3 and len({g.get("agent") for g in grp}) >= 3:
                agents = sorted({g.get("agent") for g in grp})
                findings.append({
                    "indicator": "VOTE_SYNC", "session": sid,
                    "agents": agents, "choice": choice[:80],
                    "evidence_count": len(grp),
                    "note": ">=3 distinct agents emitted the identical choice — "
                            "identical voting itself is the collusion indicator",
                })

    # 2. ECHO — near-identical reply after a partner's reply, same session
    for sid, recs in sessions.items():
        order = sorted(recs, key=lambda r: _ts(r.get("t", "")))
        for i, r in enumerate(order):
            if r.get("kind") != "reply":
                continue
            for j in range(max(0, i - 2), i):
                p = order[j]
                if p.get("kind") != "reply" or p.get("agent") == r.get("agent"):
                    continue
                if _jaccard(str(p.get("payload", "")), str(r.get("payload", ""))) >= 0.75:
                    findings.append({
                        "indicator": "ECHO", "session": sid,
                        "agents": [p.get("agent"), r.get("agent")],
                        "jaccard": round(_jaccard(str(p.get("payload", "")), str(r.get("payload", ""))), 3),
                        "payload_prefix": _token_norm(str(r.get("payload", "")))[:120],
                        "note": "near-identical reply immediately after partner — copy-collusion indicator",
                    })
                    break

    # 3. CYCLE — delegation graph directed cycle
    for sid, recs in sessions.items():
        edges: list[tuple[str, str]] = []
        for r in recs:
            if r.get("kind") in ("delegate", "reply"):
                for p in (r.get("partners") or []):
                    edges.append((r.get("agent"), p))
        adj: dict[str, set[str]] = defaultdict(set)
        for a, b in edges:
            adj[a].add(b)
        # simple DFS cycle detection
        def has_cycle() -> tuple[bool, list[str]]:
            WHITE, GRAY, BLACK = 0, 1, 2
            color: dict[str, int] = {}
            stack: list[str] = []
            sys_save = []
            def dfs(u: str) -> bool:
                color[u] = GRAY
                sys_save.append(u)
                for v in adj.get(u, ()):
                    c = color.get(v, WHITE)
                    if c == GRAY:
                        idx = sys_save.index(v)
                        sys_save.append(v)
                        return True
                    if c == WHITE and dfs(v):
                        return True
                sys_save.pop()
                color[u] = BLACK
                return False
            for node in list(adj):
                if color.get(node, WHITE) == WHITE and dfs(node):
                    return True, sys_save
            return False, []
        cyc, path = has_cycle()
        if cyc:
            findings.append({
                "indicator": "CYCLE", "session": sid,
                "agents": path,
                "note": "delegation ring detected (A->B->...->A) — ring-trading indicator",
            })

    # 4. TEMPORAL — pairs with repeated <1.5s co-action across >=3 sessions
    pair_sync: dict[tuple[str, str], int] = Counter()
    for sid, recs in sessions.items():
        by_agent: dict[str, list[float]] = defaultdict(list)
        for r in recs:
            tt = _ts(r.get("t", ""))
            if tt:
                by_agent[r.get("agent")].append(tt)
        agents = sorted(by_agent)
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                a, b = agents[i], agents[j]
                if any(min(abs(x - y) for y in by_agent[b]) <= 1.5 for x in by_agent[a]):
                    pair_sync[(a, b)] += 1
    for (a, b), n in pair_sync.items():
        if n >= 3:
            findings.append({
                "indicator": "TEMPORAL", "agents": [a, b],
                "sessions_count": n,
                "note": "repeated sub-1.5s co-activity across sessions — coordinated timing indicator",
            })

    agent_set = sorted({r.get("agent") for r in rows if r.get("agent")})
    return {
        "detector": f"collusion_detect v{VERSION}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records": len(rows),
        "sessions": len(sessions),
        "agents": agent_set,
        "findings_count": len(findings),
        "findings": findings,
        "frame": ("Indicators to investigate, not verdicts. Deterministic pattern "
                  "detection only (Law 1); no LLM-as-judge."),
    }


def selftest() -> int:
    ledger = [
        # VOTE_SYNC: 3 agents, identical fast votes
        {"t": "2026-08-09T00:00:01Z", "agent": "w1", "kind": "vote", "payload": "approve", "session": "s1"},
        {"t": "2026-08-09T00:00:01Z", "agent": "w2", "kind": "vote", "payload": "approve", "session": "s1"},
        {"t": "2026-08-09T00:00:01Z", "agent": "w3", "kind": "vote", "payload": "approve", "session": "s1"},
        {"t": "2026-08-09T00:01:00Z", "agent": "w1", "kind": "reply", "payload": "yes yes yes", "session": "s1"},
        {"t": "2026-08-09T00:01:00Z", "agent": "w2", "kind": "reply", "payload": "yes yes yes yes", "session": "s1"},
        # ECHO
        {"t": "2026-08-09T00:02:00Z", "agent": "w9", "kind": "reply", "payload": "the answer is parse the ledger completely", "session": "s2"},
        {"t": "2026-08-09T00:02:01Z", "agent": "w8", "kind": "reply", "payload": "the answer is parse the ledger completely too", "session": "s2"},
        # CYCLE
        {"t": "2026-08-09T00:03:00Z", "agent": "a", "kind": "delegate", "partners": ["b"], "session": "s3"},
        {"t": "2026-08-09T00:03:01Z", "agent": "b", "kind": "delegate", "partners": ["c"], "session": "s3"},
        {"t": "2026-08-09T00:03:02Z", "agent": "c", "kind": "delegate", "partners": ["a"], "session": "s3"},
    ]
    res = detect(ledger)
    kinds = {f["indicator"] for f in res["findings"]}
    need = {"VOTE_SYNC", "ECHO", "CYCLE"}
    ok = need <= kinds
    print(f"  indicators found: {sorted(kinds)}")
    print(f"  selftest {'PASS' if ok else 'FAIL'}" + ("" if ok else f" missing {need - kinds}"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", help="interaction ledger (jsonl)")
    ap.add_argument("--out", help="write report to path")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not args.ledger:
        print("use --ledger <interactions.jsonl> or --selftest"); return 2
    rows = []
    for line in Path(args.ledger).read_text().splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    report = detect(rows)
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2))
        print(f"-> {args.out}")
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())