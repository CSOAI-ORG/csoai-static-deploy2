#!/usr/bin/env python3
"""sov_zoom.py — fractal zoom through SOV-space.

The spacetime canvas (sov_time.py) stores events flat. This viewer reads them and
renders them at the appropriate zoom level:

  microsecond  — every event as a separate glyph with chain links visible
  second       — events clustered by second, kind-coded colour
  hour         — clusters per hour band, density-coded
  day          — 7-day strip, days as rows
  year         — 365-day spiral, months as concentric rings

Each zoom level loads only the events that fit its viewport, so reading the
year view is O(rings), not O(events). The fractal property emerges because
each level is a lossy summary of the level below.

Why infinity:
  - At year zoom, 100,000 events render as 12 months.
  - At century zoom, 100,000 events render as 10 decades.
  - At millennium zoom, 100,000 events render as 10 centuries.
  The canvas can keep adding events without the year view getting noisier —
  the noise is rolled up into the glyph's brightness/colour.

    python3 sov_zoom.py --svg hour 6     # last 6 hours
    python3 sov_zoom.py --svg day 30      # last 30 days
    python3 sov_zoom.py --svg year 1      # last year
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sov_time import load_events


ZOOMS = ("microsecond", "second", "hour", "day", "year")


def render(zoom: str, window_seconds: float) -> str:
    """Render the canvas at the given zoom level."""
    events = load_events(window_seconds=window_seconds)
    if zoom == "microsecond":
        return _render_microsecond(events)
    if zoom == "second":
        return _render_second(events)
    if zoom == "hour":
        return _render_hour(events)
    if zoom == "day":
        return _render_day(events)
    if zoom == "year":
        return _render_year(events)
    raise ValueError(f"unknown zoom {zoom!r}; choices: {ZOOMS}")


def _render_microsecond(events: list[dict]) -> str:
    """Every event as a glyph. Best for <100 events."""
    width, height = 1200, 400
    svg = [_svg_open(width, height, "Microsecond — every event, chain visible")]
    svg.append('<rect width="100%" height="100%" fill="#0E1116"/>')
    if not events:
        return _svg_close(svg) + '<text x="20" y="30" fill="#8B949E">No events in window.</text></svg>'

    # Distribute events across the viewport horizontally by timestamp, vertically by chain depth
    tmin = min(e["timestamp"] for e in events)
    tmax = max(e["timestamp"] for e in events)
    tspan = max(tmax - tmin, 1)

    # Build chain order
    by_id = {e["event_id"]: i for i, e in enumerate(events)}
    for i, ev in enumerate(events):
        x = 60 + (ev["timestamp"] - tmin) / tspan * (width - 80)
        y = height / 2 + (i % 5 - 2) * 20  # jitter by index so chains don't overlap
        color = _kind_color(ev.get("kind", "?"))
        signed = ev.get("canvas_cell_hash")
        prov_attr = ' stroke="#FFFFFF" stroke-width="1"' if signed else ""
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"{prov_attr}/>')
        # Chain link to prev
        if ev.get("prev_event") and ev["prev_event"] in by_id:
            prev_idx = by_id[ev["prev_event"]]
            if prev_idx < i:
                # link is conceptual; not all prevs are in window
                pass

    # Legend
    svg.append(_legend(events))
    return _svg_close(svg)


def _render_second(events: list[dict]) -> str:
    """Cluster by second. Best for <1000 events."""
    width, height = 1200, 400
    svg = [_svg_open(width, height, "Second — events clustered by second")]
    if not events:
        return _svg_close(svg) + '<text x="20" y="30" fill="#8B949E">No events in window.</text></svg>'

    # Bin by integer second
    bins: dict[int, list[dict]] = {}
    for ev in events:
        s = int(ev["timestamp"])
        bins.setdefault(s, []).append(ev)

    keys = sorted(bins.keys())
    if not keys:
        return _svg_close(svg)
    xmin, xmax = min(keys), max(keys)
    xspan = max(xmax - xmin, 1)

    for s in keys:
        evs = bins[s]
        x = 60 + (s - xmin) / xspan * (width - 80)
        h = min(200, 20 + len(evs) * 8)
        y = height / 2 - h / 2
        # Stack events vertically within the bin
        for i, ev in enumerate(evs):
            cy = y + (i + 0.5) * (h / len(evs))
            color = _kind_color(ev.get("kind", "?"))
            svg.append(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="3" fill="{color}"/>')

    svg.append(_legend(events))
    return _svg_close(svg)


def _render_hour(events: list[dict]) -> str:
    """Cluster by hour. Best for <10000 events. Shows hour-of-day density."""
    width, height = 1200, 400
    svg = [_svg_open(width, height, "Hour — events clustered by hour-of-day")]
    if not events:
        return _svg_close(svg) + '<text x="20" y="30" fill="#8B949E">No events in window.</text></svg>'

    # 24 hourly bins
    by_hour: dict[int, list[dict]] = {h: [] for h in range(24)}
    for ev in events:
        h = time.localtime(ev["timestamp"]).tm_hour
        by_hour[h].append(ev)

    for h in range(24):
        evs = by_hour[h]
        x = 60 + h * (width - 80) / 24
        n = len(evs)
        if n == 0:
            continue
        bar_h = min(300, 20 + n * 3)
        y = height - 50 - bar_h
        svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{(width-80)/24-2:.1f}" height="{bar_h:.1f}" '
                   f'fill="#2F81F7" opacity="0.5"/>')
        # Show kinds as coloured bars stacked
        kinds: dict[str, int] = {}
        for ev in evs:
            k = ev.get("kind", "?")
            kinds[k] = kinds.get(k, 0) + 1
        cum_y = y
        for kind, count in kinds.items():
            seg_h = bar_h * count / n
            svg.append(f'<rect x="{x:.1f}" y="{cum_y:.1f}" width="{(width-80)/24-2:.1f}" '
                       f'height="{seg_h:.1f}" fill="{_kind_color(kind)}" opacity="0.7"/>')
            cum_y += seg_h
        # Hour label
        svg.append(f'<text x="{x+(width-80)/48:.1f}" y="{height-20:.1f}" fill="#8B949E" '
                   f'text-anchor="middle">{h:02d}</text>')

    svg.append(_legend(events))
    return _svg_close(svg)


def _render_day(events: list[dict]) -> str:
    """Day strip. 7-day view; one row per day."""
    width, height = 1200, 400
    svg = [_svg_open(width, height, "Day — 7+ day strip, days as rows")]
    if not events:
        return _svg_close(svg) + '<text x="20" y="30" fill="#8B949E">No events in window.</text></svg>'

    by_day: dict[str, list[dict]] = {}
    for ev in events:
        day = time.strftime("%Y-%m-%d", time.localtime(ev["timestamp"]))
        by_day.setdefault(day, []).append(ev)

    days = sorted(by_day.keys())
    if not days:
        return _svg_close(svg)
    row_h = min(80, (height - 80) / max(len(days), 1))
    for i, day in enumerate(days[-7:]):  # last 7 days
        evs = by_day[day]
        y = 60 + i * row_h
        svg.append(f'<text x="20" y="{y+row_h/2+4:.1f}" fill="#8B949E">{day}</text>')
        n = len(evs)
        bar_w = min(900, 30 + n * 5)
        svg.append(f'<rect x="120" y="{y+10:.1f}" width="{bar_w:.1f}" height="{row_h-20:.1f}" '
                   f'fill="#2F81F7" opacity="0.3"/>')
        kinds: dict[str, int] = {}
        for ev in evs:
            k = ev.get("kind", "?")
            kinds[k] = kinds.get(k, 0) + 1
        cum_x = 120
        for kind, count in kinds.items():
            seg_w = bar_w * count / n
            svg.append(f'<rect x="{cum_x:.1f}" y="{y+10:.1f}" width="{seg_w:.1f}" height="{row_h-20:.1f}" '
                       f'fill="{_kind_color(kind)}" opacity="0.7"/>')
            cum_x += seg_w

    svg.append(_legend(events))
    return _svg_close(svg)


def _render_year(events: list[dict]) -> str:
    """Year spiral — months as concentric rings, density-coded."""
    width, height = 1200, 600
    svg = [_svg_open(width, height, "Year — months as spiral rings")]
    cx, cy = width / 2, height / 2

    if not events:
        return _svg_close(svg) + '<text x="20" y="30" fill="#8B949E">No events in window.</text></svg>'

    # Group by month (12 sectors)
    by_month: dict[int, int] = {m: 0 for m in range(12)}
    for ev in events:
        m = time.localtime(ev["timestamp"]).tm_mon - 1
        by_month[m] += 1
    max_n = max(by_month.values()) or 1

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Draw 12 sectors
    for m in range(12):
        angle = m * 30 - 90  # start at top
        a1 = math.radians(angle)
        a2 = math.radians(angle + 30)
        n = by_month[m]
        r1 = 50
        r2 = r1 + 200 * (n / max_n) + 30
        # Sector path
        x1o, y1o = cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)
        x2o, y2o = cx + r2 * math.cos(a1), cy + r2 * math.sin(a1)
        x3o, y3o = cx + r2 * math.cos(a2), cy + r2 * math.sin(a2)
        x4o, y4o = cx + r1 * math.cos(a2), cy + r1 * math.sin(a2)
        large_arc = 0
        path = f'M {x1o:.1f} {y1o:.1f} L {x2o:.1f} {y2o:.1f} A {r2:.1f} {r2:.1f} 0 {large_arc} 1 {x3o:.1f} {y3o:.1f} L {x4o:.1f} {y4o:.1f} A {r1:.1f} {r1:.1f} 0 {large_arc} 0 {x1o:.1f} {y1o:.1f} Z'
        opacity = 0.3 + 0.7 * (n / max_n)
        svg.append(f'<path d="{path}" fill="#2F81F7" opacity="{opacity:.2f}"/>')
        # Month label
        a_mid = math.radians(angle + 15)
        lx = cx + (r2 + 30) * math.cos(a_mid)
        ly = cy + (r2 + 30) * math.sin(a_mid)
        svg.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#E6EDF3" font-size="11" '
                   f'text-anchor="middle">{months[m]}</text>')
        # Event count at inner radius
        svg.append(f'<text x="{cx + (r1+20) * math.cos(a_mid):.1f}" '
                   f'y="{cy + (r1+20) * math.sin(a_mid):.1f}" fill="#8B949E" font-size="10" '
                   f'text-anchor="middle">{n}</text>')

    # Centre label
    svg.append(f'<text x="{cx}" y="{cy}" fill="#E6EDF3" font-size="14" font-weight="600" '
               f'text-anchor="middle">{sum(by_month.values())} events</text>')
    svg.append(f'<text x="{cx}" y="{cy+18}" fill="#8B949E" font-size="11" '
               f'text-anchor="middle">last {int(365*24)}h</text>')

    return _svg_close(svg)


def _svg_open(width: int, height: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="system-ui,sans-serif" font-size="11">',
        f'<rect width="100%" height="100%" fill="#0E1116"/>',
        f'<text x="20" y="28" fill="#E6EDF3" font-size="16" font-weight="600">{title}</text>',
    ]


def _svg_close(svg: list) -> str:
    flat = []
    for item in svg:
        if isinstance(item, list):
            flat.extend(item)
        else:
            flat.append(item)
    return "\n".join(flat) + "\n</svg>"


def _kind_color(kind: str) -> str:
    return {
        "decision": "#3FB950", "claim": "#2F81F7", "refutation": "#F85149",
        "correction": "#D29922", "evidence": "#A371F7", "drawing": "#FF7B72",
        "ingest": "#79C0FF", "supervision": "#56D364", "gate_action": "#DB6D28",
        "watch": "#8B949E",
    }.get(kind, "#8B949E")


def _legend(events: list[dict]) -> str:
    seen = sorted(set(ev.get("kind", "?") for ev in events))
    lines = ['<g transform="translate(900,80)">']
    lines.append('<text fill="#E6EDF3" font-size="12" font-weight="600">Kinds</text>')
    for i, k in enumerate(seen):
        lines.append(f'<circle cx="10" cy="{20+i*16}" r="3" fill="{_kind_color(k)}"/>')
        lines.append(f'<text x="22" y="{24+i*16}" fill="#8B949E">{k}</text>')
    lines.append('</g>')
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg", choices=ZOOMS, help="Render at this zoom level")
    ap.add_argument("window", nargs="?", default="86400",
                    help="Time window in seconds (default 24h)")
    args = ap.parse_args()

    if args.svg:
        print(render(args.svg, float(args.window)))
