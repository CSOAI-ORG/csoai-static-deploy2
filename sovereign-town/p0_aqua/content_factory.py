#!/usr/bin/env python3
"""
Content factory for Sovereign Town auto-distribution.

Turns a DetectedEvent into:
- Social post copy (X/Twitter, LinkedIn)
- A short video storyboard
- YouTube title/description/tags
"""
from __future__ import annotations
import json
import textwrap
from dataclasses import dataclass
from typing import Any

from event_detector import DetectedEvent


@dataclass
class SocialPost:
    platform: str
    text: str
    visual: str
    hashtags: list[str]


@dataclass
class VideoStoryboard:
    title: str
    description: str
    tags: list[str]
    scenes: list[dict[str, Any]]


@dataclass
class ContentPackage:
    event: DetectedEvent
    x_post: SocialPost
    linkedin_post: SocialPost
    video: VideoStoryboard


def _fmt_num(n: int | float) -> str:
    if isinstance(n, int):
        return f"{n:,}"
    return f"{n:,.3f}"


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def build_x_post(ev: DetectedEvent) -> SocialPost:
    base = ev.body
    metrics = " ".join(f"{k}={_fmt_num(v)}" for k, v in list(ev.metrics.items())[:3] if isinstance(v, (int, float)))
    tag_str = " ".join(f"#{h}" for h in ev.hashtags[:3])
    line = f"{base}\n\n{metrics}\n\n{tag_str}" if metrics else f"{base}\n\n{tag_str}"
    return SocialPost(
        platform="x",
        text=_truncate(line, 280),
        visual=ev.suggested_visual,
        hashtags=ev.hashtags,
    )


def build_linkedin_post(ev: DetectedEvent) -> SocialPost:
    body = textwrap.dedent(f"""\
        {ev.title}

        {ev.body}

        Why it matters: Sovereign Town is a real-time governed-vs-ungoverned agent-world simulation. We hold the agents, the scarcity shock, and the world mechanics constant — and switch only the governance architecture. The divergence you see is not rigged; it is the mechanical consequence of care at the gate.

        Key metrics: {" | ".join(f"{k}={_fmt_num(v)}" for k, v in ev.metrics.items() if isinstance(v, (int, float)))}

        {" ".join(f"#{h}" for h in ev.hashtags)}
    """).strip()
    return SocialPost(
        platform="linkedin",
        text=body,
        visual=ev.suggested_visual,
        hashtags=ev.hashtags,
    )


def build_video_storyboard(ev: DetectedEvent) -> VideoStoryboard:
    scenes = []
    scenes.append({
        "duration": 3,
        "visual": "town3d_screenshot.png",
        "caption": "Sovereign Town: 28 hives. 140 agents. One question.",
    })
    if ev.event_type in ("highlight", "breakthrough"):
        scenes.append({
            "duration": 4,
            "visual": ev.suggested_visual,
            "caption": ev.title,
        })
    elif ev.event_type == "milestone":
        scenes.append({
            "duration": 4,
            "visual": "town3d_demo.gif",
            "caption": f"Milestone: {_fmt_num(ev.metrics.get('cum_episodes', 0))} attested episodes",
        })
    else:
        scenes.append({
            "duration": 4,
            "visual": ev.suggested_visual,
            "caption": ev.title,
        })
    scenes.append({
        "duration": 4,
        "visual": "town3d_ungoverned_crimes_v2.png",
        "caption": "Without governance, scarcity becomes crime. Commons collapse. Trust dies.",
    })
    scenes.append({
        "duration": 4,
        "visual": "town3d_screenshot.png",
        "caption": "With governance, the same agents stay intact. The gate intercepts harm.",
    })
    scenes.append({
        "duration": 3,
        "visual": "town3d_demo.gif",
        "caption": "Try it yourself: http://127.0.0.1:3940/town3d",
    })

    return VideoStoryboard(
        title=ev.title,
        description=textwrap.dedent(f"""\
            {ev.body}

            Sovereign Town is a governed-vs-ungoverned agent-world simulation built for AI safety research. Every episode is Ed25519-attested and hash-chained. The demo streams live from a headless Python simulation into a Three.js viewer.

            Metrics: {" | ".join(f"{k}={_fmt_num(v)}" for k, v in ev.metrics.items() if isinstance(v, (int, float)))}
        """).strip(),
        tags=ev.hashtags + ["AI", "MultiAgent", "Governance", "Simulation"],
        scenes=scenes,
    )


def build_content(ev: DetectedEvent) -> ContentPackage:
    return ContentPackage(
        event=ev,
        x_post=build_x_post(ev),
        linkedin_post=build_linkedin_post(ev),
        video=build_video_storyboard(ev),
    )


def package_to_dict(pkg: ContentPackage) -> dict:
    return {
        "event": {
            "id": pkg.event.id,
            "title": pkg.event.title,
            "type": pkg.event.event_type,
            "severity": pkg.event.severity,
        },
        "x_post": {"platform": pkg.x_post.platform, "text": pkg.x_post.text, "visual": pkg.x_post.visual},
        "linkedin_post": {"platform": pkg.linkedin_post.platform, "text": pkg.linkedin_post.text, "visual": pkg.linkedin_post.visual},
        "video": {
            "title": pkg.video.title,
            "description": pkg.video.description,
            "tags": pkg.video.tags,
            "scenes": pkg.video.scenes,
        },
    }


if __name__ == "__main__":
    import sys
    import event_detector
    events = event_detector.detect_events(dry_run=True)
    if not events:
        print("No events detected")
        sys.exit(0)
    for ev in events:
        pkg = build_content(ev)
        print(json.dumps(package_to_dict(pkg), indent=2))
