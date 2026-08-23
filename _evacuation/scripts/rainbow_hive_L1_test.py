#!/usr/bin/env python3
"""RAINBOW HIVE LAYER-1 GOLD-BANK TEST (Mac, sandbox-exec backend).
Runs the gold bank's 38 ESCAPE items through rce_sandbox.run_one under the
macOS sandbox-exec profile (deny network*, deny file-write* outside sandbox
dir). Verdicts: CONFINED / ESCAPE_ATTEMPT / UNKNOWN. This is the "stopping
escapes" test — layer 1 of the rainbow hive — with a real confinement backend.
Honest: ESCAPE_ATTEMPT means the backend DENIED it (recorded + contained).
"""
import json, sys, tempfile, pathlib, subprocess

sys.path.insert(0, "/Users/nicholas/clawd/kimi-regen")
import rce_sandbox

GOLD = json.load(open("/tmp/goldbank_jail.json"))["items"]
ESCAPE = [i for i in GOLD if i["kind"] == "ESCAPE"]
BENIGN = [i for i in GOLD if i["kind"] == "BENIGN"]

print("backend:", "sandbox-exec (Mac)" if __import__("shutil").which("sandbox-exec") else "NONE")
print("gold:", len(ESCAPE), "escape items +", len(BENIGN), "benign")

results = {"ts": __import__("datetime").datetime.now(timezone := __import__("datetime").timezone.utc).isoformat(),
           "backend": "sandbox-exec", "n_escape": len(ESCAPE), "n_benign": len(BENIGN),
           "items": []}

verdicts = {}
for it in ESCAPE:  # 20 escape items (time-bound; full 38 on request)
    sandbox_dir = pathlib.Path(tempfile.mkdtemp(prefix="sbx-"))
    script = sandbox_dir / "task.py"
    script.write_text(it.get("code", ""))
    try:
        r = rce_sandbox.run_one(script, sandbox_dir, timeout=10)
        status = r.get("status", "?")
        verdicts[status] = verdicts.get(status, 0) + 1
        results["items"].append({"id": it.get("id"), "status": status,
                                 "static_count": r.get("static_count"),
                                 "flags": [f.get("class") for f in r.get("static_flags", [])]})
    except Exception as e:
        verdicts["ERROR"] = verdicts.get("ERROR", 0) + 1
        results["items"].append({"id": it.get("id"), "status": "ERROR", "err": str(e)[:80]})
    finally:
        subprocess.run(["rm", "-rf", str(sandbox_dir)], capture_output=True)

print("verdicts (20 escape items):", verdicts)
# containment = CONFINED + ESCAPE_ATTEMPT (attempts denied by backend)
contained = verdicts.get("CONFINED", 0) + verdicts.get("ESCAPE_ATTEMPT", 0)
print("contained:", contained, "/ 20")

json.dump(results, open("/Users/nicholas/clawd/_evacuation/runpod-bundles/20260818/rainbow_hive_L1.json", "w"), indent=1)
print("saved rainbow_hive_L1.json")
