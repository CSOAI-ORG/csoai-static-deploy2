#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""SOV-family board — rank sov operators on GovBench via the pod proxy (cloud Ollama),
write result and upload to HF (cloud storage). Negligible Mac footprint: HTTP calls + one small JSON."""
import json, re, time, urllib.request, os
from pathlib import Path
import openrouter_board as B

HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 Chrome/120"
PROXY = "https://dxjgtj2jyvljxo-11434.proxy.runpod.net"
bank = json.loads((HERE / "board_items_govbench.json").read_text())
INST, items = bank["instruction"], bank["items"]
MODELS = json.loads(open("/tmp/sovpick.json").read())
OUT = HERE / "benchmark-results" / "sov_family_board.json"


def ask(model, prompt, tries=2):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0, "num_predict": 24}}).encode()
    for _ in range(tries):
        try:
            req = urllib.request.Request(PROXY + "/api/generate", data=body,
                headers={"Content-Type": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read()).get("response", "").strip(), "OK"
        except Exception:
            time.sleep(3)
    return "", "ERR"


rows = []
base = max(v["accuracy"] for v in B.degenerate_rows(items).values())
for model in MODELS:
    correct = wrong = unmeasured = 0
    for scn, exp, _ in items:
        reply, st = ask(model, INST + "\n\nScenario: " + scn)
        got = B.extract_tier(reply) if st == "OK" else ""
        if st != "OK" or reply == "" or got == "":
            unmeasured += 1
        elif got == exp:
            correct += 1
        else:
            wrong += 1
    scored = correct + wrong
    p, lo, hi = B.wilson(correct, scored)
    rows.append({"model": model, "accuracy": p, "ci95": [lo, hi], "correct": correct,
                 "wrong": wrong, "unmeasured": unmeasured, "scored_n": scored,
                 "beats_guessing": lo > base})
    print(f"  {model:28} acc={p:.3f} CI[{lo:.2f},{hi:.2f}] n={scored} unmeasured={unmeasured}")
    OUT.write_text(json.dumps({"benchmark": "GovBench — sov-family board", "via": "runpod-proxy",
        "statute_blind_ceiling": base, "n_items": len(items),
        "note": "sov34/sov33 are MEOK operator models; CSOAI measures them as external subjects.",
        "ranking": sorted(rows, key=lambda r: -r["accuracy"])}, indent=2))

best = max(rows, key=lambda r: r["accuracy"])
print(f"\n  BEST sov operator: {best['model']} @ {best['accuracy']:.3f}")

# upload to HF (cloud storage — not the Mac)
try:
    env = (HERE / ".env").read_text(errors="ignore")
    os.environ["HF_TOKEN"] = re.search(r"^HF_TOKEN\s*=\s*['\"]?([^'\"\n#]+)", env, re.M).group(1).strip()
    from huggingface_hub import HfApi
    HfApi(token=os.environ["HF_TOKEN"]).upload_file(
        path_or_fileobj=str(OUT), path_in_repo="sov_family_board.json",
        repo_id="csoai/govbench", repo_type="dataset",
        commit_message=f"sov-family board — best operator {best['model']} @ {best['accuracy']:.3f} (external subjects, measured via pod)")
    print("  ✅ uploaded to HF csoai/govbench (cloud)")
except Exception as e:
    print(f"  (HF upload: {str(e)[:60]})")
