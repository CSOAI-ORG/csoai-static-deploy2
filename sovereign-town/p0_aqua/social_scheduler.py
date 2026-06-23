#!/usr/bin/env python3
"""
Social scheduler for Sovereign Town auto-distribution.

Runs the event detector, renders content for each new event, and writes draft
posts + videos to the distribution queue. It does NOT publish without
credentials; publication is gated on Nick approving OAuth tokens.

Intended cron: every 10 minutes on the Mac.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from typing import Any

import event_detector
import content_factory
import video_renderer
import distributor


def run_once(dry_run: bool = False) -> dict[str, Any]:
    events = event_detector.detect_events(dry_run=dry_run)
    packages = []
    for ev in events:
        pkg = content_factory.build_content(ev)
        video_path = None
        try:
            video_path = video_renderer.render_video(pkg.video, ev.id)
        except Exception as e:
            print(f"[social_scheduler] video render failed for {ev.id}: {e}")
        if not dry_run:
            distributor.queue_package(pkg, video_path=video_path)
        packages.append({
            "event_id": ev.id,
            "title": ev.title,
            "video": str(video_path) if video_path else None,
            "x_text": pkg.x_post.text[:80] + "..." if len(pkg.x_post.text) > 80 else pkg.x_post.text,
        })
    return {"processed": len(events), "packages": packages}


def main() -> int:
    parser = argparse.ArgumentParser(description="Sovereign Town social scheduler")
    parser.add_argument("--dry-run", action="store_true", help="Detect and render but do not save state or queue")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()

    summary = run_once(dry_run=args.dry_run)
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"[social_scheduler] {summary['processed']} event(s) processed")
        for pkg in summary["packages"]:
            print(f"  - {pkg['title']}")
            print(f"    video: {pkg['video']}")
            print(f"    x: {pkg['x_text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
