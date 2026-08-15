#!/usr/bin/env python3
"""temporal_gap_audit.py — GF-04: deterministic agentic temporal-gap audit.

Audits the LAG between when an agent acts and when its governance/evidence
record reflects it. Deterministic (Law 1): parses timestamps and computes
deltas — no LLM-as-judge.

The three gap classes, each measurable from ordinary ledger/artifact data:

  ACTION_TO_RECORD — delta between an event's OBSERVED timestamp and the
    timestamp embedded in the record that claims it. A survey run stamped
    at 12:00 with data captured at 08:00 is a +4h action-to-record gap.

  ANCHOR_STALENESS — delta between an artifact's `anchored_at`/`issued_at`
    and either its own embedded data timestamp or the corpus anchor it cites.
    A pack anchored 5 days after the provision text it references is a
    staleness gap that can silently invalidate evidence.

  UPDATE_GAP — time between the newest and oldest timestamp observed across
    a set of records that purport to be a single state (e.g., a board built
    from cells measured at 09:00, 11:00 and 14:00). Wide spread on one board
    means the board collates temporally-heterogeneous data.

Each finding is an indicator with evidence (the exact timestamps), never a
verdict — investigation step, not accusation. Pairs naturally with
corpus_anchor.py drift (a provision moving is the canonical trigger for
re-auditing everything anchored to it).

Input: any JSON / JSONL with timestamp-ish fields — auto-discovered by key
name (ts, time, t, issued_at, anchored_at, watched_at, timestamp, generated_at,
last_run, modified). Add explicit fields with --event-time/--record-time if the
defaults miss.

    python3 temporal_gap_audit.py --files results/*.json [--out report.json]
    python3 temporal_gap_audit.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.0"

TS_KEYS = ("ts", "t", "time", "timestamp", "issued_at", "anchored_at",
           "watched_at", "generated_at", "last_run", "last_modified",
           "modified", "date", "measured_at", "recorded_at", "event_time")


def _parse_ts(v) -> float | None:
    if v is None:
        return None
    s = str(v)
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception:
        m = re.search(r"\d{4}-\d{2}-\d{2}[T ][0-9:.]+", s)
        if m:
            try:
                return datetime.fromisoformat(m.group(0).replace("Z", "+00:00").replace(" ", "T")).timestamp()
            except Exception:
                return None
        return None


def _collect_timestamps(obj, keys: set[str]) -> list[tuple[str, float]]:
    """Deep-scan a JSON object for timestamp-keyed values; returns (key, ts)."""
    out: list[tuple[str, float]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys:
                ts = _parse_ts(v)
                if ts is not None:
                    out.append((k, ts))
            out.extend(_collect_timestamps(v, keys))
    elif isinstance(obj, list):
        for item in obj:
            out.extend(_collect_timestamps(item, keys))
    return out


def audit(files: list[Path], extra_keys: list[str] | None = None) -> dict:
    keys = set(TS_KEYS)
    if extra_keys:
        keys.update(extra_keys)

    findings: list[dict] = []
    per_file: list[dict] = []

    for f in files:
        if not f.exists():
            per_file.append({"file": str(f), "status": "missing"})
            continue
        try:
            raw = f.read_text()
            try:
                data = json.loads(raw) if raw.lstrip().startswith(("[", "{")) else None
                if data is None:  # JSONL fallback
                    data = [json.loads(l) for l in raw.splitlines() if l.strip()]
            except Exception:
                data = [json.loads(l) for l in raw.splitlines() if l.strip()]
        except Exception as e:
            per_file.append({"file": str(f), "status": "unreadable", "error": str(e)[:120]})
            continue
        keys_cols = _collect_timestamps(data, keys)
        if not keys_cols:
            per_file.append({"file": str(f), "status": "no_timestamps",
                             "note": "no timestamp-keyed fields found — temporal audit impossible (UNKNOWN, not zero)"})
            continue
        times = sorted(t for _, t in keys_cols)
        f_min, f_max = times[0], times[-1]
        span = f_max - f_min
        # named common fields for the gap classes
        issued = next((ts for k, ts in keys_cols if k in ("issued_at", "generated_at", "timestamp")), None)
        anchored = next((ts for k, ts in keys_cols if k in ("anchored_at", "watched_at")), None)
        event = next((ts for k, ts in keys_cols if k in ("ts", "t", "event_time", "measured_at", "recorded_at")), None)

        if issued is not None and event is not None and issued - event > 3600:
            findings.append({
                "indicator": "ACTION_TO_RECORD", "file": f.name,
                "hours": round((issued - event) / 3600, 2),
                "event_at": datetime.fromtimestamp(event, tz=timezone.utc).isoformat(),
                "recorded_at": datetime.fromtimestamp(issued, tz=timezone.utc).isoformat(),
                "note": "record issued >1h after the event it claims — evidence lag",
            })
        if anchored is not None and event is not None and anchored - event > 24 * 3600:
            findings.append({
                "indicator": "ANCHOR_STALENESS", "file": f.name,
                "days": round((anchored - event) / 86400, 2),
                "event_at": datetime.fromtimestamp(event, tz=timezone.utc).isoformat(),
                "anchored_at": datetime.fromtimestamp(anchored, tz=timezone.utc).isoformat(),
                "note": "anchored >24h after data it cites — pack may silently expire",
            })
        if 3600 < span <= 24 * 3600:
            findings.append({
                "indicator": "UPDATE_GAP", "file": f.name,
                "hours": round(span / 3600, 2),
                "note": "single-state artifact spans >1h of measurements — temporally heterogeneous board",
            })
        per_file.append({
            "file": str(f), "status": "audited", "timestamps_seen": len(keys_cols),
            "span_s": round(span, 1),
            "span_h": round(span / 3600, 2),
        })

    return {
        "detector": f"temporal_gap_audit v{VERSION}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": len(files),
        "findings_count": len(findings),
        "findings": findings,
        "per_file": per_file,
        "frame": ("Indicators, never verdicts. Deterministic timestamp-delta analysis "
                  "(Law 1); a file with no timestamps is UNKNOWN, not 'no gap'."),
    }


def selftest() -> int:
    import tempfile
    scenarios = {
        "action_record.json": {"ts": "2026-08-09T08:00:00Z", "issued_at": "2026-08-09T12:00:00Z", "kind": "survey"},
        "anchor_stale.json": {"measured_at": "2026-08-01T09:00:00Z", "anchored_at": "2026-08-05T09:00:00Z"},
        "update_gap.json": {"generated_at": "2026-08-03T09:00:00Z", "cells": [
            {"ts": "2026-08-01T09:00:00Z"}, {"ts": "2026-08-03T08:00:00Z"}]},
        "benign.json": {"t": "2026-08-09T10:00:01Z", "recorded_at": "2026-08-09T10:00:02Z"},
    }
    with tempfile.TemporaryDirectory() as td:
        paths = []
        for name, row in scenarios.items():
            p = Path(td) / name
            p.write_text(json.dumps(row))
            paths.append(p)
        res = audit(paths)
    kinds = {f["indicator"] for f in res["findings"]}
    need = {"ACTION_TO_RECORD", "ANCHOR_STALENESS", "UPDATE_GAP"}
    ok = need <= kinds
    print(f"  indicators: {sorted(kinds)}")
    print(f"  selftest {'PASS' if ok else 'FAIL'}" + ("" if ok else f" missing {need - kinds}"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="+", help="json/jsonl files to audit")
    ap.add_argument("--keys", nargs="+", default=None, help="additional timestamp key names")
    ap.add_argument("--out", help="write report to path")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.files:
        print("use --files <paths...> or --selftest")
        return 2
    files = [Path(f) for f in args.files]
    if len(files) == 1 and "*" in str(files[0]):
        import glob as _glob
        files = [Path(f) for f in sorted(_glob.glob(str(files[0])))]
    report = audit(files, args.keys)
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2))
        print(f"-> {args.out}")
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())