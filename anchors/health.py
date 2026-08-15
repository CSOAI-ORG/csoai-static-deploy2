#!/usr/bin/env python3
"""
anchors/health.py — the staleness alarm. Fail-closed becomes fail-silent without this.

THE FAILURE THIS EXISTS TO CATCH
Fail-closed is right: a watcher that cannot fetch reports UNKNOWN, never "unchanged". But
UNKNOWN is a perfectly calm-looking word, and a watcher that has returned UNKNOWN every day for
three weeks because an endpoint started throttling looks exactly like a watcher doing its job.
The system is honest and completely blind at the same time.

So honesty about a single poll is not enough. Something has to hold the *sequence*: a watcher
that has not successfully read its source in three days is broken, however truthfully it says so
each morning.

  HEALTHY          succeeded within ALARM_AFTER_HOURS
  STALE            last success is older than ALARM_AFTER_HOURS — ALERT
  NEVER_SUCCEEDED  no successful read has ever been recorded — ALERT, and a different one
  UNREGISTERED     a state file exists for a watcher no longer in the registry

NEVER_SUCCEEDED is split out from STALE on purpose. "It stopped working" and "it never worked"
have different causes and different fixes, and collapsing them into one alarm sends you looking
for a regression that was never there.

The exit code is non-zero on any alarm, so the cron surfaces it rather than logging into a file
nobody opens.

    python3 -m anchors.health
    python3 -m anchors.health --selftest
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from anchors.base import STATE_DIR, registry

ALARM_AFTER_HOURS = 72

HEALTHY = "HEALTHY"
STALE = "STALE"
NEVER_SUCCEEDED = "NEVER_SUCCEEDED"
UNREGISTERED = "UNREGISTERED"

ALARM_STATES = (STALE, NEVER_SUCCEEDED, UNREGISTERED)


@dataclass
class Health:
    watcher: str
    state: str
    last_success: str | None
    hours_since: float | None
    detail: str = ""


def _parse(ts: str) -> datetime | None:
    try:
        d = datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def assess(
    state_dir: Path | None = None,
    now: datetime | None = None,
    expected: list[str] | None = None,
    alarm_after_hours: int = ALARM_AFTER_HOURS,
) -> list[Health]:
    """`now` and `expected` are injectable so the selftest can construct a real stale case."""
    state_dir = state_dir or STATE_DIR
    now = now or datetime.now(timezone.utc)
    if expected is None:
        expected = [w.__name__ for w in registry()]

    out: list[Health] = []
    seen: set[str] = set()

    for name in expected:
        f = state_dir / f"{name}.json"
        if not f.is_file():
            out.append(Health(name, NEVER_SUCCEEDED, None, None, "no state file"))
            continue
        seen.add(name)
        try:
            state = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError) as e:
            out.append(Health(name, NEVER_SUCCEEDED, None, None, f"unreadable state: {e}"))
            continue

        ts = state.get("last_success")
        parsed = _parse(ts) if ts else None
        if parsed is None:
            out.append(
                Health(name, NEVER_SUCCEEDED, ts, None, "no parseable last_success timestamp")
            )
            continue

        hours = (now - parsed).total_seconds() / 3600.0
        if hours > alarm_after_hours:
            out.append(
                Health(name, STALE, ts, hours, f"{hours:.1f}h since last success")
            )
        else:
            out.append(Health(name, HEALTHY, ts, hours))

    # A state file with no watcher behind it means a watcher was deleted or renamed and its
    # anchors are now frozen at whatever they last read. Silent, and it looks like coverage.
    if state_dir.is_dir():
        for f in sorted(state_dir.glob("*.json")):
            if f.stem not in expected:
                out.append(
                    Health(f.stem, UNREGISTERED, None, None, "state file with no registered watcher")
                )

    return out


def selftest() -> int:
    passed = failed = 0

    def ok(name: str, cond: bool, extra: str = "") -> None:
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"  PASS  {name}")
        else:
            failed += 1
            print(f"  FAIL  {name} {extra}")

    now = datetime(2026, 7, 29, 12, 0, tzinfo=timezone.utc)

    def write(d: Path, name: str, ago_hours: float | None, raw: str | None = None) -> None:
        if raw is not None:
            (d / f"{name}.json").write_text(raw)
            return
        ts = (now - timedelta(hours=ago_hours)).isoformat(timespec="seconds")
        (d / f"{name}.json").write_text(json.dumps({"digest": "x", "last_success": ts}))

    # 1 — a fresh watcher is HEALTHY. Negative control: an alarm that always fires proves
    # nothing, so this case must pass before any of the failing cases mean anything.
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        write(d, "W", 1)
        r = assess(d, now, ["W"])
        ok("fresh watcher is HEALTHY", [h.state for h in r] == [HEALTHY], str(r))

    # 2 — just inside the window is still HEALTHY; just outside is STALE. The boundary is where
    # an off-by-one would hide, and 71h vs 73h is the pair that catches it.
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        write(d, "W", 71)
        ok("71h is HEALTHY", assess(d, now, ["W"])[0].state == HEALTHY)
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        write(d, "W", 73)
        h = assess(d, now, ["W"])[0]
        ok("73h is STALE", h.state == STALE, h.state)
        ok("STALE carries the age", h.hours_since is not None and 72 < h.hours_since < 74)

    # 3 — three consecutive UNKNOWNs. This is the real scenario: poll() never writes state on an
    # UNKNOWN, so the file simply stops advancing. The alarm must fire on the gap, not on any
    # UNKNOWN record — there is no UNKNOWN record to find.
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        write(d, "W", 24 * 3 + 1)
        r = assess(d, now, ["W"])
        ok("3 days of UNKNOWN alarms", r[0].state == STALE, r[0].state)

    # 4 — never ran at all is its own state, not STALE.
    with tempfile.TemporaryDirectory() as t:
        r = assess(Path(t), now, ["W"])
        ok("missing state is NEVER_SUCCEEDED", r[0].state == NEVER_SUCCEEDED, r[0].state)

    # 5 — corrupt and empty state files must not read as healthy.
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        write(d, "W", None, raw="{not json")
        ok("corrupt state is NEVER_SUCCEEDED", assess(d, now, ["W"])[0].state == NEVER_SUCCEEDED)
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        write(d, "W", None, raw=json.dumps({"digest": "x"}))
        ok(
            "state without last_success is NEVER_SUCCEEDED",
            assess(d, now, ["W"])[0].state == NEVER_SUCCEEDED,
        )

    # 6 — an orphaned state file from a deleted watcher.
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        write(d, "W", 1)
        write(d, "Gone", 1)
        states = {h.watcher: h.state for h in assess(d, now, ["W"])}
        ok("orphan state is UNREGISTERED", states.get("Gone") == UNREGISTERED, str(states))
        ok("orphan does not mask the healthy one", states.get("W") == HEALTHY)

    # 7 — a naive timestamp must not crash or be treated as fresh. Real state files have been
    # written by more than one code path over this project's life.
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        naive = (now - timedelta(hours=100)).replace(tzinfo=None).isoformat()
        write(d, "W", None, raw=json.dumps({"last_success": naive}))
        ok("naive timestamp is compared, not crashed", assess(d, now, ["W"])[0].state == STALE)

    # 8 — an empty expected list with orphan files still alarms rather than reporting all-clear.
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        write(d, "W", 1)
        r = assess(d, now, [])
        ok("no expected watchers still surfaces orphans", r and r[0].state == UNREGISTERED, str(r))

    print(f"\nselftest {passed}/{passed + failed}")
    return 0 if failed == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--hours", type=int, default=ALARM_AFTER_HOURS)
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rows = assess(alarm_after_hours=args.hours)
    alarms = [h for h in rows if h.state in ALARM_STATES]

    if args.json:
        print(json.dumps([h.__dict__ for h in rows], indent=2))
    else:
        print(f"WATCHER HEALTH — alarm after {args.hours}h")
        for h in rows:
            age = f"{h.hours_since:.1f}h" if h.hours_since is not None else "—"
            print(f"  {h.state:16} {h.watcher:24} {age:>8}  {h.detail}")
        print(f"\n  {len(rows) - len(alarms)} healthy · {len(alarms)} alarming")

    return 1 if alarms else 0


if __name__ == "__main__":
    sys.exit(main())
