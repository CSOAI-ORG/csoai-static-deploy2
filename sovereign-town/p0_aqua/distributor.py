#!/usr/bin/env python3
"""
Distribution queue for Sovereign Town auto-distribution.

This module does NOT post directly to social networks (that requires OAuth
secrets Nick must approve). Instead it writes draft posts and rendered videos
to a queue directory where they can be reviewed or auto-published later.

Supported platforms (stubs): X/Twitter, LinkedIn, YouTube.
"""
from __future__ import annotations
import json
import os
import pathlib
import shutil
import time
from dataclasses import asdict
from typing import Any

from content_factory import ContentPackage

P0 = pathlib.Path(__file__).parent
QUEUE_DIR = P0 / "distribution_queue"
ARCHIVE_DIR = P0 / "distribution_archive"


def _ensure_dirs() -> None:
    QUEUE_DIR.mkdir(exist_ok=True)
    ARCHIVE_DIR.mkdir(exist_ok=True)


def queue_package(pkg: ContentPackage, video_path: pathlib.Path | None = None) -> pathlib.Path:
    """Write a content package to the review queue."""
    _ensure_dirs()
    ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    slug = f"{ts}_{pkg.event.id}"
    pkg_dir = QUEUE_DIR / slug
    pkg_dir.mkdir(exist_ok=True)

    manifest = {
        "queued_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": {
            "id": pkg.event.id,
            "title": pkg.event.title,
            "type": pkg.event.event_type,
            "severity": pkg.event.severity,
        },
        "x_post": asdict(pkg.x_post),
        "linkedin_post": asdict(pkg.linkedin_post),
        "video": {
            "title": pkg.video.title,
            "description": pkg.video.description,
            "tags": pkg.video.tags,
            "scenes": pkg.video.scenes,
        },
    }
    with open(pkg_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    # Copy visual asset references into the queue dir for easy review.
    for post in (pkg.x_post, pkg.linkedin_post):
        src = P0 / post.visual
        if src.exists():
            shutil.copy2(src, pkg_dir / src.name)

    if video_path and video_path.exists():
        shutil.copy2(video_path, pkg_dir / video_path.name)
        manifest["video_path"] = str(video_path.name)

    return pkg_dir


def list_queue() -> list[pathlib.Path]:
    _ensure_dirs()
    return sorted(QUEUE_DIR.iterdir())


def archive(slug_dir: pathlib.Path) -> None:
    """Move a queued package to the archive after publication."""
    shutil.move(str(slug_dir), str(ARCHIVE_DIR / slug_dir.name))


# --- Platform stubs: these require OAuth credentials and Nick's approval ---

def publish_x(text: str, media_path: pathlib.Path, credentials: dict[str, str] | None = None) -> dict[str, Any]:
    if credentials is None:
        return {"status": "draft", "platform": "x", "note": "No credentials provided; content queued for review."}
    # TODO: integrate with X API v2 using credentials
    return {"status": "published", "platform": "x"}


def publish_linkedin(text: str, media_path: pathlib.Path, credentials: dict[str, str] | None = None) -> dict[str, Any]:
    if credentials is None:
        return {"status": "draft", "platform": "linkedin", "note": "No credentials provided; content queued for review."}
    # TODO: integrate with LinkedIn API
    return {"status": "published", "platform": "linkedin"}


def publish_youtube(title: str, description: str, tags: list[str], video_path: pathlib.Path, credentials: dict[str, str] | None = None) -> dict[str, Any]:
    if credentials is None:
        return {"status": "draft", "platform": "youtube", "note": "No credentials provided; content queued for review."}
    # TODO: integrate with YouTube Data API v3 using credentials
    return {"status": "published", "platform": "youtube"}


if __name__ == "__main__":
    print("Distribution queue directory:", QUEUE_DIR)
    print("Archive directory:", ARCHIVE_DIR)
    print("Queue length:", len(list_queue()))
