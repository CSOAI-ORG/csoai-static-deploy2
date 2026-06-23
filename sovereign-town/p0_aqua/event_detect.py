#!/usr/bin/env python3
"""
Event detector compatibility shim for Sovereign Town auto-distribution.

This module previously contained a parallel detector implementation. It now
wraps `event_detector.py` (the canonical implementation) and emits the flat,
JSON-safe event dicts that `video_packager.py` expects.

State is tracked in `distribution_state.json` by `event_detector.py`.
"""
from __future__ import annotations
import json
import pathlib
from typing import Any

import event_detector

P0 = pathlib.Path(__file__).parent
PUBLIC = P0.parent.parent / "proofof-site" / "sovereign-town"

PRIORITY = {
    "milestone": 5,
    "breakthrough": 4,
    "highlight": 3,
    "moat_update": 2,
    "info": 1,
}


def _to_flat(ev: event_detector.DetectedEvent) -> dict[str, Any]:
    """Convert a canonical DetectedEvent into the legacy flat public format."""
    body = ev.body
    if ev.hashtags:
        tag_line = " ".join(f"#{h}" for h in ev.hashtags)
        if not body.endswith(tag_line):
            body = f"{body}\n\n{tag_line}"
    return {
        "event_id": ev.id,
        "type": ev.event_type,
        "title": ev.title,
        "priority": PRIORITY.get(ev.event_type, 1),
        "data": ev.metrics,
        "x_text": body,
    }


def detect_all(dry_run: bool = False) -> list[dict[str, Any]]:
    """Scan all sources and return a list of new events in flat public format."""
    events = event_detector.detect_events(dry_run=dry_run)
    flat = [_to_flat(ev) for ev in events]
    flat.sort(key=lambda e: e.get("priority", 0), reverse=True)
    return flat


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Detect without saving state")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()
    events = detect_all(dry_run=args.dry_run)
    if args.json:
        print(json.dumps(events, indent=2, default=str))
    else:
        print(f"Detected {len(events)} event(s)")
        for ev in events:
            print(f"  [{ev['type']}] {ev['title']}")
