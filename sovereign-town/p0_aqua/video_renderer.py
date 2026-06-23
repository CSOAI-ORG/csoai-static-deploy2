#!/usr/bin/env python3
"""
Video renderer for Sovereign Town auto-distribution.

Renders a short MP4 from a VideoStoryboard using ffmpeg and PIL overlays.
No external TTS is used; captions appear as burned-in text. Audio can be
added later by the distributor if a music bed is available.

Output: distribution_videos/YYYY-MM-DD_event-id.mp4
"""
from __future__ import annotations
import os
import pathlib
import subprocess
import tempfile
from datetime import datetime
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from content_factory import VideoStoryboard

P0 = pathlib.Path(__file__).parent
VIDEO_DIR = P0 / "distribution_videos"
FONT_SIZE = 28
TITLE_FONT_SIZE = 36


def _find_font() -> str | None:
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/opt/homebrew/Library/Fonts/Arial.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def _overlay_caption(image_path: pathlib.Path, caption: str, title: str | None = None, output_path: pathlib.Path | None = None) -> pathlib.Path:
    img = Image.open(image_path).convert("RGBA")
    # Resize to 1080p landscape if needed
    target_w, target_h = 1920, 1080
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Dark gradient bar at bottom
    for i in range(220):
        alpha = int(180 * (i / 220))
        draw.line([(0, target_h - 220 + i), (target_w, target_h - 220 + i)], fill=(0, 0, 0, alpha))

    font_path = _find_font()
    try:
        caption_font = ImageFont.truetype(font_path, FONT_SIZE) if font_path else ImageFont.load_default()
        title_font = ImageFont.truetype(font_path, TITLE_FONT_SIZE) if font_path else ImageFont.load_default()
    except Exception:
        caption_font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    margin = 60
    y = target_h - 180
    if title:
        draw.text((margin, y - 50), title, font=title_font, fill=(212, 168, 67, 255))
    draw.text((margin, y + 10), caption, font=caption_font, fill=(255, 255, 255, 255))

    composed = Image.alpha_composite(img, overlay)
    composed = composed.convert("RGB")

    if output_path is None:
        output_path = image_path.parent / (image_path.stem + "_captioned.jpg")
    composed.save(output_path, quality=92)
    return output_path


def render_video(storyboard: VideoStoryboard, event_id: str) -> pathlib.Path:
    VIDEO_DIR.mkdir(exist_ok=True)
    date_prefix = datetime.utcnow().strftime("%Y-%m-%d")
    out_path = VIDEO_DIR / f"{date_prefix}_{event_id}.mp4"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        scene_files = []
        for i, scene in enumerate(storyboard.scenes):
            visual = P0 / scene["visual"]
            if not visual.exists():
                # Fallback to a known visual
                visual = P0 / "town3d_screenshot.png"
            out_frame = tmp_path / f"scene_{i:03d}.jpg"
            _overlay_caption(visual, scene.get("caption", ""), title=storyboard.title if i == 0 else None, output_path=out_frame)
            # Duplicate frames to match duration at 12 fps
            duration = scene.get("duration", 3)
            for _ in range(duration * 12):
                scene_files.append(out_frame)

        # Write concat list for ffmpeg
        concat_path = tmp_path / "concat.txt"
        with open(concat_path, "w") as f:
            for frame in scene_files:
                f.write(f"file '{frame}'\n")

        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_path),
            "-vf", "fps=12,format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(out_path),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return out_path


def render_from_event(event_dict: dict[str, Any]) -> pathlib.Path | None:
    from content_factory import build_content
    from event_detector import DetectedEvent
    ev = DetectedEvent(**event_dict)
    pkg = build_content(ev)
    return render_video(pkg.video, ev.id)


if __name__ == "__main__":
    import json
    import event_detector
    events = event_detector.detect_events(dry_run=True)
    if not events:
        print("No events to render")
    for ev in events:
        path = render_from_event(event_detector.event_to_dict(ev))
        print(f"Rendered: {path} ({path.stat().st_size / 1024 / 1024:.2f} MB)")
