#!/usr/bin/env python3
"""
Video packager for Sovereign Town auto-distribution.

Turns events from event_detect.py into short social/YouTube videos using
ffmpeg. Generates title/fact/metrics/outro cards with PIL when a rendered
visual is not already available.

Outputs:
  distribution_videos/YYYY-MM-DD_<event_id>.mp4
  post_queue.json (append-only list of queued posts)
"""
from __future__ import annotations
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception as exc:  # pragma: no cover
    raise RuntimeError("video_packager requires Pillow (PIL)") from exc

P0 = pathlib.Path(__file__).parent
OUTPUT_DIR = P0 / "distribution_videos"
QUEUE_PATH = P0 / "post_queue.json"

WIDTH, HEIGHT = 1280, 720
FPS = 30

THEME = {
    "milestone":   {"bg": "#1a1500", "accent": "#f4c430", "text": "#ffffff"},
    "breakthrough": {"bg": "#001220", "accent": "#38bdf8", "text": "#ffffff"},
    "highlight":   {"bg": "#1a0505", "accent": "#f87171", "text": "#ffffff"},
    "moat_update": {"bg": "#051a0d", "accent": "#34d399", "text": "#ffffff"},
    "default":     {"bg": "#0f0f12", "accent": "#a78bfa", "text": "#ffffff"},
}


def _find_font() -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, 48)
            except Exception:
                continue
    return ImageFont.load_default()


FONT = _find_font()
FONT_SMALL = FONT.font if hasattr(FONT, "font") else FONT
# We derive a smaller TrueType variant when possible.
if hasattr(FONT, "path"):
    try:
        FONT_SMALL = ImageFont.truetype(FONT.path, 28)
    except Exception:
        FONT_SMALL = FONT
else:
    FONT_SMALL = FONT


def _theme(event_type: str) -> dict:
    return THEME.get(event_type, THEME["default"])


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _wrap_lines(text: str, max_chars: int) -> list[str]:
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=max_chars) or [""])
    return lines


def _render_card(title: str | None, body: str, event_type: str,
                 image_path: pathlib.Path | None = None) -> Image.Image:
    theme = _theme(event_type)
    img = Image.new("RGB", (WIDTH, HEIGHT), _hex_to_rgb(theme["bg"]))
    draw = ImageDraw.Draw(img)
    accent = _hex_to_rgb(theme["accent"])

    # Header bar
    draw.rectangle([0, 0, WIDTH, 12], fill=accent)

    if image_path and image_path.exists():
        try:
            vis = Image.open(image_path)
            if vis.mode != "RGB":
                vis = vis.convert("RGB")
            # Fit inside 1200x520 leaving margin
            vis.thumbnail((1200, 520), Image.Resampling.LANCZOS)
            vx = (WIDTH - vis.width) // 2
            vy = 40
            img.paste(vis, (vx, vy))
            text_top = vy + vis.height + 30
        except Exception:
            text_top = 80
    else:
        text_top = 120

    y = text_top
    if title:
        for line in _wrap_lines(title, 40):
            draw.text((WIDTH // 2, y), line, font=FONT, fill=_hex_to_rgb(theme["text"]), anchor="mm")
            y += 56
        y += 20

    for line in _wrap_lines(body, 70):
        draw.text((WIDTH // 2, y), line, font=FONT_SMALL, fill=_hex_to_rgb(theme["text"]), anchor="mm")
        y += 36

    # Footer brand
    draw.text((WIDTH // 2, HEIGHT - 40), "Sovereign Town · proofof.ai/sovereign-town",
              font=FONT_SMALL, fill=accent, anchor="mm")
    return img


def _build_scenes(event: dict) -> list[tuple[Image.Image, float]]:
    """Return (image, duration_seconds) scenes for an event."""
    event_type = event.get("type", "default")
    title = event.get("title", "Sovereign Town update")
    x_text = event.get("x_text", "")
    data = event.get("data", {})

    visual = event.get("visual") or data.get("suggested_visual")
    image_path = P0 / visual if visual else None

    scenes: list[tuple[Image.Image, float]] = []

    # Title card
    scenes.append((_render_card(None, title, event_type), 3.0))

    # Fact / X-text card
    if x_text:
        scenes.append((_render_card("What happened", x_text, event_type), 4.0))

    # Metrics card
    numeric = {k: v for k, v in data.items() if isinstance(v, (int, float))}
    if numeric:
        metric_lines = "\n".join(f"{k}: {v:,.3f}" if isinstance(v, float) else f"{k}: {v:,}"
                                  for k, v in list(numeric.items())[:5])
        scenes.append((_render_card("Key metrics", metric_lines, event_type), 3.0))

    # Visual asset
    if image_path and image_path.exists():
        scenes.append((_render_card(title, x_text or "Live simulation output", event_type, image_path), 4.0))

    # Outro
    scenes.append((_render_card(None, "Try the live demo at proofof.ai/sovereign-town", event_type), 3.0))

    return scenes


def _safe_id(event_id: str) -> str:
    return "".join(c if c.isalnum() or c in "_-" else "_" for c in event_id)


def _run_ffmpeg(scene_dir: pathlib.Path, list_file: pathlib.Path, output: pathlib.Path) -> None:
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-vf", "format=yuv420p",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output),
    ]
    env = os.environ.copy()
    env["PATH"] = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)


def package_event(event: dict, output_dir: pathlib.Path | str | None = None) -> dict[str, Any]:
    """Render one event to MP4 and append to the post queue."""
    out = pathlib.Path(output_dir) if output_dir else OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    event_id = _safe_id(event.get("event_id", "unknown"))
    date = time.strftime("%Y-%m-%d")
    mp4 = out / f"{date}_{event_id}.mp4"

    scenes = _build_scenes(event)
    if not scenes:
        raise RuntimeError(f"No scenes generated for event {event_id}")

    with tempfile.TemporaryDirectory(prefix="st_video_") as tmp:
        tmp_path = pathlib.Path(tmp)
        list_path = tmp_path / "scenes.txt"
        with open(list_path, "w") as f:
            for idx, (img, duration) in enumerate(scenes):
                frame_path = tmp_path / f"scene_{idx:03d}.png"
                img.save(frame_path, "PNG")
                f.write(f"file '{frame_path.as_posix()}'\n")
                f.write(f"duration {duration}\n")
            # concat demuxer needs a trailing file reference
            f.write(f"file '{tmp_path / f'scene_{len(scenes)-1:03d}.png'}'\n")

        _run_ffmpeg(tmp_path, list_path, mp4)

    result = {
        "event_id": event.get("event_id"),
        "type": event.get("type"),
        "title": event.get("title"),
        "video": str(mp4),
        "x_text": event.get("x_text"),
        "queued_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    # Only append to the persistent post queue when writing to the default output dir.
    if out == OUTPUT_DIR:
        _append_queue(result)
    return result


def package_all(events: list[dict], output_dir: pathlib.Path | str | None = None) -> list[dict[str, Any]]:
    """Render videos for every event and return the manifest list."""
    results = []
    for ev in events:
        try:
            results.append(package_event(ev, output_dir=output_dir))
        except Exception as e:
            print(f"[video_packager] failed to package {ev.get('event_id')}: {e}", file=sys.stderr)
    return results


def _append_queue(entry: dict) -> None:
    queue: list[dict] = []
    if QUEUE_PATH.exists():
        try:
            with open(QUEUE_PATH) as f:
                queue = json.load(f)
        except Exception:
            queue = []
    queue.append(entry)
    with open(QUEUE_PATH, "w") as f:
        json.dump(queue, f, indent=2)


def list_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    with open(QUEUE_PATH) as f:
        return json.load(f)


if __name__ == "__main__":
    import event_detect
    events = event_detect.detect_all()
    if not events:
        print("No events to package")
        sys.exit(0)
    packaged = package_all(events[:3])
    print(f"Packaged {len(packaged)} video(s)")
    for p in packaged:
        print(f"  {p['video']}")
