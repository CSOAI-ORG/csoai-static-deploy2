import json, sys
sys.path.insert(0, "/workspace/csoai-static-deploy2")

# Audit board items integrity: frozen source, item count, recomputability fields
b = json.load(open("/workspace/csoai-static-deploy2/board_items_govbench.json"))
print("source:", b.get("source"))
print("frozen:", b.get("frozen"), "| type:", type(b.get("frozen")).__name__)
items = b.get("items", [])
print("items:", len(items))
# sample item structure
if items:
    print("sample item keys:", list(items[0].keys()))
    print("sample:", json.dumps(items[0])[:300])
# check answer formats present (deterministic gold labels)
import collections
ans_types = collections.Counter()
for it in items:
    ans_types[type(it.get("answer")).__name__] += 1
print("answer types:", dict(ans_types))

# audit: count instruction checks per axis marker
axis_markers = collections.Counter()
for it in items:
    axis_markers[str(it.get("axis", "unset"))[:12]] += 1
print("axis buckets:", dict(list(axis_markers.items())[:8]))