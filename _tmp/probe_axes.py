import json, sys, urllib.request

OLLAMA = "http://localhost:11434/api/generate"

# Multi-axis boards already on the pod clone (board items for care + safety exist as govbank-style json?)
boards_dir = "/workspace/csoai-static-deploy2/SOVOS/boards-v2-2026-08-12"
import os, glob
available = [os.path.basename(p) for p in glob.glob(boards_dir + "/board_*.json")]
print("board files on pod:", available[:20])

# Use gov bench (24 items) as the primary; check if a care/safety board has items we can reuse
# Each board item: [scenario, gold, reference]
def load_items(axis):
    p = os.path.join(boards_dir, f"board_{axis}.json")
    if not os.path.exists(p): return None
    try:
        b = json.load(open(p))
        items = b.get("items") or []
        return [i for i in items if isinstance(i, list) and len(i) >= 2]
    except Exception:
        return None

# gov board path fallback (the canonical 237-item board might be registered in the pod's bank dirs)
cand = []
for pat in ["/workspace/csoai-static-deploy2/board_items_govbench.json",
            "/workspace/sovos-repo/board_items_govbench.json",
            "/workspace/csoai-static-deploy2/SOVOS/boards-v2-2026-08-12/board_gov.json"]:
    if os.path.exists(pat):
        cand.append(pat)
print("gov candidates:", cand)