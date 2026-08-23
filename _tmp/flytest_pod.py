import sys
sys.path.insert(0, "/workspace/csoai-static-deploy2")
for name in ("flywheel",):
    try:
        f = __import__(name)
        print("module:", f.__file__)
        if hasattr(f, "selftest"):
            r = f.selftest()
            print("selftest:", r)
        else:
            print("no selftest attr")
        print("HELD_OUT_FRACTION:", getattr(f, "HELD_OUT_FRACTION", "n/a"))
        print("has export_fuel:", hasattr(f, "export_fuel"))
    except Exception as e:
        import traceback; traceback.print_exc()

# GSPC board audit against fleet dashboard + board items
import json, glob
boards = glob.glob("/workspace/csoai-static-deploy2/boards-v2-2026-08-12/*.json") + glob.glob("/workspace/csoai-static-deploy2/board_*.json")
print("\nboard files found:", len(boards))
for b in boards[:6]:
    try:
        d = json.load(open(b))
        print(" -", b.split("/")[-1], "| keys:", list(d.keys())[:5])
    except Exception as e:
        print(" -", b, "ERR", str(e)[:60])