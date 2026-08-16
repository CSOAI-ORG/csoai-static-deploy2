#!/usr/bin/env python3
"""emit_world_cards.py — generate Council World event-nodes from signed-cards/.

Auto-spawn bridge: reads every signed card JSON under signed-cards/ (the
public evidence store) and emits a world-append JSON (one node per card).
The sov-world.html renderer can then either embed this list or fetch it
live — so every measurement that gets signed becomes a node in J-Space.

Card -> node mapping:
  card_type            -> kind (human-arena-gold-v1 -> card, etc.)
  content.<key>        -> value line
  content_id           -> clickable evidence id
  signature            -> live chain handle

Output: signed-cards/world-nodes.json (append-only, regenerated deterministically).
"""
from __future__ import annotations
import json, hashlib, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # repo root (SOVOS/agents -> repo)
CARDS_DIR = ROOT / "signed-cards"
OUT = CARDS_DIR / "world-nodes.json"

KIND_HINT = {
    "human-arena-gold-v1": "card",
    "sovos-honey-stratum-v1": "honey",
    "gspc-board": "board",
}
CITY_HINT = {
    "human": "Human",
    "honey": "Honey",
    "index": "Council",
    "board": "Board",
}


def h32(s: str) -> int:
    h = 2166136261
    for ch in s:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def main() -> int:
    nodes = []
    for card_path in sorted(CARDS_DIR.glob("**/*.json")):
        if card_path.name in ("index.json", "world-nodes.json", "content-index.json"):
            continue
        try:
            card = json.loads(card_path.read_text())
        except Exception:
            continue
        card_type = str(card.get("card_type", card_path.stem))
        kind = KIND_HINT.get(card_type, "card")
        city = CITY_HINT.get(str(card.get("source", "")), "Council")
        content = card.get("content", {})
        # build a one-line value
        if isinstance(content, dict):
            acc = content.get("accuracy")
            rows = content.get("rows")
            val = []
            if rows is not None:
                val.append(f"rows={rows}")
            if acc is not None:
                val.append(f"acc={acc}")
            if content.get("axes"):
                val.append(f"axes={content.get('axes')}")
            value = " · ".join(val) if val else (card_type)
        else:
            value = str(content)[:80]
        nodes.append({
            "id": card_path.stem,
            "kind": kind,
            "label": card_type,
            "ts": card.get("date", ""),
            "value": value,
            "content_id": str(card.get("content_id", ""))[:20],
            "signature": "signed" if card.get("signed") else "unsigned",
            "city": city,
        })
    # deterministic order
    nodes.sort(key=lambda n: (n["ts"], n["id"]))
    OUT.write_text(json.dumps({"kind": "council-world.nodes", "count": len(nodes),
                               "generated": datetime.now(timezone.utc).isoformat(),
                               "nodes": nodes}, indent=2))
    print(f"world-nodes.json: {len(nodes)} nodes -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())