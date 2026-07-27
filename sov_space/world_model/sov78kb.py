#!/usr/bin/env python3
"""SOV-Space 78KB — TempleOS-Inspired Minimal Visual Engine

The entire SOV-space in ~78KB. TempleOS principles:
1. Everything compiles — JIT-compile reasoning into visual functions
2. Symbol table as visual engine — data IS the visual
3. Binary-as-pixels — each OWEM family output as visual pattern
4. Single address space — all families in one visual space
5. Tiny footprint — constraint breeds creativity

Architecture:
  - 1-bit canvas (640x480 = 38,400 bytes)
  - 12 OWEM families as 640x40 pixel strips
  - Each family's J-space output encoded as visual pattern
  - Honey fluid as pixel flow (SPH-like)
  - Dreams as branching fractals
  - BFT-33 council as 33-pixel vote bitmap
"""

import json
import hashlib
import math
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent.parent
FOREST = ROOT / "forest"
SOV_SPACE = ROOT / "benchmark-results" / "sov-space"
SOV_SPACE.mkdir(parents=True, exist_ok=True)


# ─── TempleOS-Inspired Constants ─────────────────────────────────────────────
WIDTH = 640
HEIGHT = 480
BITS_PER_BYTE = 8
TOTAL_BYTES = (WIDTH * HEIGHT) // BITS_PER_BYTE  # 38,400 bytes for 1-bit

# The 12 OWEM families — each gets a 640x40 pixel strip
FAMILY_STRIP_HEIGHT = 40
FAMILY_STRIPS = {
    "abstraction": 0, "aesthetics": 1, "agency": 2, "care": 3,
    "creation": 4, "destruction": 5, "embodiment": 6, "ethics": 7,
    "identity": 8, "logic": 9, "preservation": 10, "relationality": 11,
}
FAMILY_COLORS_1BIT = {
    "abstraction": 0x01,  # 00000001
    "aesthetics": 0x03,   # 00000011
    "agency": 0x07,       # 00000111
    "care": 0x0F,         # 00001111
    "creation": 0x1F,     # 00011111
    "destruction": 0x3F,  # 00111111
    "embodiment": 0x7F,   # 01111111
    "ethics": 0xFF,       # 11111111
    "identity": 0xFE,     # 11111110
    "logic": 0xFC,        # 11111100
    "preservation": 0xF8, # 11111000
    "relationality": 0xF0,# 11110000
}


class SOV78KB:
    """The entire SOV-space in ~78KB. TempleOS-inspired."""

    def __init__(self):
        self.canvas = bytearray(TOTAL_BYTES)  # 1-bit canvas
        self.bloodline = self._load_bloodline()
        self.honey = self._load_honey()
        self.fluid = self._load_fluid()

    def _load_bloodline(self):
        p = FOREST / "bloodline.json"
        return json.load(open(p)) if p.exists() else {"knowledge": []}

    def _load_honey(self):
        p = FOREST / "honey_chatml.jsonl"
        return [json.loads(l) for l in open(p)] if p.exists() else []

    def _load_fluid(self):
        p = FOREST / "sov_fluid.json"
        return json.load(open(p)) if p.exists() else {"events": []}

    # ─── Pixel Operations (1-bit) ─────────────────────────────────────────

    def set_pixel(self, x, y, value=1):
        """Set a single pixel on the 1-bit canvas."""
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            byte_idx = (y * WIDTH + x) // BITS_PER_BYTE
            bit_idx = (y * WIDTH + x) % BITS_PER_BYTE
            if value:
                self.canvas[byte_idx] |= (1 << bit_idx)
            else:
                self.canvas[byte_idx] &= ~(1 << bit_idx)

    def get_pixel(self, x, y):
        """Get a single pixel from the 1-bit canvas."""
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            byte_idx = (y * WIDTH + x) // BITS_PER_BYTE
            bit_idx = (y * WIDTH + x) % BITS_PER_BYTE
            return (self.canvas[byte_idx] >> bit_idx) & 1
        return 0

    # ─── Visual Encoding ──────────────────────────────────────────────────

    def encode_family_strip(self, family, knowledge_entries):
        """Encode a family's knowledge as a visual strip (640x40 pixels)."""
        if family not in FAMILY_STRIPS:
            return

        strip_y = list(FAMILY_STRIPS.keys()).index(family) * FAMILY_STRIP_HEIGHT
        pattern = FAMILY_STRIPS[family]

        # Create pattern based on knowledge density
        density = len(knowledge_entries) / max(1, len(self.bloodline.get("knowledge", [])))
        density_pixels = int(density * WIDTH)

        for x in range(WIDTH):
            for y in range(FAMILY_STRIP_HEIGHT):
                # Pattern: density-based fill with family signature
                if x < density_pixels:
                    # Knowledge present — encode as pattern
                    pattern_byte = (pattern >> (x % 8)) & 1
                    if pattern_byte:
                        self.set_pixel(x, strip_y + y, 1)
                else:
                    # No knowledge — encode as noise (water state)
                    if (x * 7 + y * 13 + hash(family) % 100) % 17 == 0:
                        self.set_pixel(x, strip_y + y, 1)

    def encode_honey_flow(self):
        """Encode honey fluid dynamics as pixel flow."""
        fluid = self.fluid.get("events", [])
        for i, event in enumerate(fluid[:100]):
            # Each event becomes a flowing pixel
            x = int((i / 100) * WIDTH)
            y = HEIGHT - FAMILY_STRIP_HEIGHT * len(FAMILY_STRIPS) - 10
            # Flow animation (static snapshot)
            self.set_pixel(x, y, 1)
            self.set_pixel(x, y + 1, 1)

    def encode_dream_branches(self, dreams):
        """Encode C-space dreams as branching fractals."""
        cx, cy = WIDTH // 2, HEIGHT // 2
        for dream in dreams:
            for branch in dream.get("branches", []):
                for depth, level in enumerate(branch):
                    for b, outcome in enumerate(level.get("outcomes", [])):
                        angle = (b / len(level["outcomes"])) * math.pi * 2
                        radius = 50 + depth * 30
                        x = int(cx + math.cos(angle) * radius)
                        y = int(cy + math.sin(angle) * radius)
                        # Draw branch node
                        self.set_pixel(x, y, 1)
                        self.set_pixel(x + 1, y, 1)
                        self.set_pixel(x, y + 1, 1)
                        # Draw connection to center
                        for t in range(10):
                            tx = int(cx + (x - cx) * t / 10)
                            ty = int(cy + (y - cy) * t / 10)
                            self.set_pixel(tx, ty, 1)

    def encode_bft_vote(self, tally):
        """Encode BFT-33 council vote as 33-pixel bitmap."""
        y = HEIGHT - 20
        approve = tally.get("approve", 0)
        amend = tally.get("amend", 0)
        reject = tally.get("reject", 0)
        total = approve + amend + reject

        for i in range(33):
            x = WIDTH // 2 - 16 + i
            if i < approve:
                # Green = approve (pixel ON)
                self.set_pixel(x, y, 1)
            elif i < approve + amend:
                # Yellow = amend (every other pixel)
                if i % 2 == 0:
                    self.set_pixel(x, y, 1)
            # Red = reject (pixel OFF)

    # ─── Full Render ──────────────────────────────────────────────────────

    def render(self):
        """Render the entire SOV-space onto the 1-bit canvas."""
        # Clear canvas
        self.canvas = bytearray(TOTAL_BYTES)

        # Encode each family's knowledge strip
        knowledge = self.bloodline.get("knowledge", [])
        families = {}
        for entry in knowledge:
            fam = entry.get("family", "unknown")
            families.setdefault(fam, []).append(entry)

        for family in FAMILY_STRIPS:
            self.encode_family_strip(family, families.get(family, []))

        # Encode honey flow
        self.encode_honey_flow()

        # Encode dreams
        cspace = SOV_SPACE / "cspace_dreams.json"
        if cspace.exists():
            dreams = json.load(open(cspace)).get("dreams", [])
            self.encode_dream_branches(dreams)

        # Encode BFT vote
        tally = {"approve": 28, "amend": 5, "reject": 0}
        self.encode_bft_vote(tally)

        return self.canvas

    def to_pbm(self):
        """Export canvas as PBM (Portable Bitmap) format."""
        header = f"P4\n{WIDTH} {HEIGHT}\n"
        return header.encode() + bytes(self.canvas)

    def save(self, path=None):
        """Save the rendered canvas."""
        if path is None:
            path = SOV_SPACE / "sov78kb.pbm"
        self.render()
        path.write_bytes(self.to_pbm())
        return path


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  SOV-SPACE 78KB — TempleOS-Inspired Visual Engine      ║")
    print("║  1-bit canvas · 640x480 · ~38KB                        ║")
    print("╚══════════════════════════════════════════════════════════╝")

    sov = SOV78KB()

    # Show knowledge state
    knowledge = sov.bloodline.get("knowledge", [])
    families = {}
    for entry in knowledge:
        fam = entry.get("family", "unknown")
        families.setdefault(fam, []).append(entry)

    print(f"\n─── KNOWLEDGE BASE ───")
    print(f"  Total entries: {len(knowledge)}")
    print(f"  Honey pairs: {len(sov.honey)}")
    print(f"  Fluid events: {len(sov.fluid.get('events', []))}")

    print(f"\n─── FAMILY STRIPS ───")
    for family in FAMILY_STRIPS:
        entries = families.get(family, [])
        state = "honey" if len(entries) > 10 else "milk" if len(entries) > 3 else "water"
        print(f"  {FAMILY_STRIPS[family]:08b} {family:20s} {state:6s} ({len(entries)} entries)")

    # Render
    path = sov.save()
    size = path.stat().st_size
    print(f"\n─── OUTPUT ───")
    print(f"  Canvas: {WIDTH}x{HEIGHT} @ 1-bit = {TOTAL_BYTES:,} bytes")
    print(f"  Saved: {path}")
    print(f"  File size: {size:,} bytes ({size/1024:.1f} KB)")
    print(f"\n  Open with any PBM viewer or convert to PNG:")
    print(f"    convert {path} sov78kb.png")


if __name__ == "__main__":
    main()
