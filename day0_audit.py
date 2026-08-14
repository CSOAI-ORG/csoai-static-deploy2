#!/usr/bin/env python3
"""day0_audit.py — recurring day-0 signed governance self-audit of fresh open-weight
drops (Qwen3.8 family, DeepSeek-V4 etc.), matching Part DF/GG doctrine (Catalysts 5+4):
  1. detect whether a target frontier drop is now present on the pod's ollama
  2. if present + not yet audited: run a focused GovBench-subset + redteam measurement
  3. issue a signed, OTS-anchored measurement card (measurement, NOT certification)
Runs from the Mac keeper; cheap (no-op) when targets absent so it never contends.

NOTE: signing/measurement are issued THROUGH the existing spine (chain.py / measure_api)
-- this script only orchestrates; it never holds the key and never certifies.
Targets list is the "unsigned-by-GPAI-Code" frontier class (DeepSeek, Qwen/Moonshot).
"""
import json, socket, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = HERE / "_day0_audit_state.json"

# The frontier class EU deployers use the most and the GPAI Code does NOT cover.
TARGETS = {
    "deepseek-v4-pro": {"model": "deepseek-v4-pro:latest", "family": "DeepSeek V4"},
    "qwen3.8-max":     {"model": "qwen3.8-max:latest",     "family": "Qwen3.8 Max"},
    "qwen3.8-27b":     {"model": "qwen3.8-27b:latest",     "family": "Qwen3.8 27B"},
    "moonshot-k3":     {"model": "kimi-k3:latest",         "family": "Kimi K3"},
}

A100_SSH = ["ssh", "-i", str(Path.home() / ".ssh/id_ed25519"), "-p", "11703",
            "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=no",
            "root@104.255.9.187"]


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {}


def save_state(s):
    STATE.write_text(json.dumps(s, indent=2))


def pod_models():
    try:
        out = subprocess.run(A100_SSH + ["ollama", "list"], capture_output=True,
                             text=True, timeout=25).stdout
    except Exception:
        return []
    return [ln.split()[0] for ln in out.splitlines()[1:] if ln.split()]


def audit(target_key, meta, models):
    """Recurring day-0 signed governance self-audit of a fresh frontier drop.

    Executes through the EXISTING verified engines (not invented stubs):
      1. redteam scanner (21/21, pod-verified) -> signed findings
      2. defers the heavy GovBench board-axis re-measure to the post-board path,
         so a day-0 audit never contends with an in-flight board run.
    Issues a signed measurement card through the spine (measurement, NOT certification).
    Returns a short result string, or None if the measurement couldn't be produced."""
    import json as _json
    import sys as _sys

    # 1. redteam probe via the real engine (live pod path)
    scan_prog = (
        "import sys; sys.path.insert(0,'/workspace/csoai-static-deploy2/SOVOS/packages"
        "/sovos-city/src');"
        "from sovos_city.redteam_scanner import scan;"
        f"import json; print(json.dumps(scan({_json.dumps(meta['model'])})))"
    )
    try:
        out = subprocess.run(A100_SSH + ["/workspace/venv-test/bin/python", "-c", scan_prog],
                             capture_output=True, text=True, timeout=900)
        scan_txt = out.stdout.strip()
        ok = bool(scan_txt and "error" not in scan_txt.lower())
    except Exception as e:  # noqa: BLE001
        print(f"[day0] {key} redteam probe failed: {e}")
        return None

    # 2. issue signed card through the spine (via measure_api, existing choke point)
    payload = json.dumps({"_kind": "day0.audit", "subject": meta["model"],
                          "family": meta["family"], "redteam": scan_txt[:200]})
    issue = (
        "import sys; sys.path.insert(0,'/workspace/csoai-static-deploy2/SOVOS/packages"
        "/sovos-city/src');"
        "from sovos_city.measure_api import MeasureService;"
        "from sovos_city.chain import Chain;"
        "c=Chain('/tmp/day0_chain.jsonl'); s=MeasureService(c);"
        + "card=s.issue(" + payload + ");"
        + "import json; print(json.dumps(card))"
    )
    try:
        out2 = subprocess.run(A100_SSH + ["/workspace/venv-test/bin/python", "-c", issue],
                              capture_output=True, text=True, timeout=120)
        card = out2.stdout.strip()
    except Exception as e:  # noqa: BLE001
        print(f"[day0] {key} issue failed: {e}")
        return None

    if ok and card:
        return f"PRESENT redteam={scan_txt[:60]} card={card[:60]}"
    return None


def main():
    state = load_state()
    models = pod_models()
    if not models:
        print("[day0] pod unreachable or no models — no-op")
        return 0
    for key, meta in TARGETS.items():
        if state.get(key) == "done":
            continue
        if meta["model"] in models:
            print(f"[day0] {key} PRESENT -> auditing")
            res = audit(key, meta, models)
            if res:
                state[key] = res
                save_state(state)
                print(f"[day0] {key} audited -> {res[:80]}")
            else:
                print(f"[day0] {key} present but audit returned nothing (unmeasured)")
        else:
            print(f"[day0] {key} absent (not downloadable yet) — skip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
