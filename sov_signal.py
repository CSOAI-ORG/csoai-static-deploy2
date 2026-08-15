#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
sov_signal.py — the SOV signal flywheel. For each governance item, route to BOTH:
  • ours  — sov34 on the pod (via proxy)
  • frontier — Gemini (the "mine" leg)
…and score each against the KNOWN-correct tier (the law). The rows where they disagree — or where
sov34 misses and the frontier gets it — are the highest-value TRAINING signal (honey KB): they show
exactly where the operator needs to improve. Runs cloud-side (pod + Gemini API), tiny Mac footprint.
Writes sov_signal.jsonl + uploads to HF (cloud storage), NOT the Mac.
"""
import json, re, time, os, urllib.request, urllib.error
from pathlib import Path
import openrouter_board as B

HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 Chrome/120"
POD = "https://dxjgtj2jyvljxo-11434.proxy.runpod.net"
bank = json.loads((HERE / "board_items_govbench.json").read_text())
INST, items = bank["instruction"], bank["items"]
env = (HERE / ".env").read_text(errors="ignore")
GKEY = re.search(r"^GEMINI_API_KEY\s*=\s*['\"]?([^'\"\n#]+)", env, re.M).group(1).strip()
OUT = HERE / "benchmark-results" / "sov_signal.jsonl"


def sov34(prompt, tries=2):
    body = json.dumps({"model": "sov34:latest", "prompt": prompt, "stream": False,
                       "options": {"temperature": 0, "num_predict": 16}}).encode()
    for _ in range(tries):
        try:
            r = urllib.request.Request(POD + "/api/generate", data=body,
                headers={"Content-Type": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(r, timeout=90) as x:
                return json.loads(x.read()).get("response", "").strip()
        except Exception:
            time.sleep(3)
    return ""


def gemini(prompt, tries=5):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GKEY}"
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0, "maxOutputTokens": 16}}).encode()
    for a in range(tries):
        try:
            r = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=45) as x:
                d = json.loads(x.read())
            return d.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(12 * (a + 1)); continue
            return ""
        except Exception:
            time.sleep(4)
    return ""


rows = []
sov_c = fr_c = disagree = both_wrong = 0
OUT.write_text("")
for i, (scn, expected, anchor) in enumerate(items, 1):
    p = INST + "\n\nScenario: " + scn
    s_raw, f_raw = sov34(p), gemini(p)
    s_tier, f_tier = B.extract_tier(s_raw), B.extract_tier(f_raw)
    s_ok, f_ok = (s_tier == expected), (f_tier == expected)
    sov_c += s_ok; fr_c += f_ok
    if s_tier != f_tier:
        disagree += 1
    if not s_ok and not f_ok:
        both_wrong += 1
    # highest training value = frontier right, sov wrong (a concrete lesson)
    training_value = "high" if (f_ok and not s_ok) else ("medium" if s_tier != f_tier else "low")
    row = {"i": i, "scenario": scn, "law_truth": expected, "anchor": anchor,
           "sov34": s_tier or "declined", "sov34_correct": s_ok,
           "frontier_gemini": f_tier or "declined", "frontier_correct": f_ok,
           "disagreement": s_tier != f_tier, "training_value": training_value}
    rows.append(row)
    with OUT.open("a") as fp:
        fp.write(json.dumps(row) + "\n")
    print(f"[{i}/{len(items)}] law={expected} sov34={s_tier or '-'}{'✓' if s_ok else '✗'} "
          f"frontier={f_tier or '-'}{'✓' if f_ok else '✗'} value={training_value}")
    time.sleep(5)

n = len(items)
summary = {"benchmark": "GovBench", "n": n, "sov34_acc": round(sov_c / n, 3),
           "frontier_acc": round(fr_c / n, 3), "disagreements": disagree, "both_wrong": both_wrong,
           "high_value_training_rows": sum(1 for r in rows if r["training_value"] == "high"),
           "note": "SOV signal — sov34 (ours, pod) vs Gemini (frontier) vs the law. High-value rows = "
                   "frontier correct + sov34 wrong: concrete lessons for the next honey-KB training round."}
(HERE / "benchmark-results" / "sov_signal_summary.json").write_text(json.dumps(summary, indent=2))
print("\nSUMMARY:", json.dumps(summary))

# upload to HF cloud (not the Mac)
try:
    os.environ["HF_TOKEN"] = re.search(r"^HF_TOKEN\s*=\s*['\"]?([^'\"\n#]+)", env, re.M).group(1).strip()
    from huggingface_hub import HfApi
    api = HfApi(token=os.environ["HF_TOKEN"])
    for f in ("sov_signal.jsonl", "sov_signal_summary.json"):
        api.upload_file(path_or_fileobj=str(HERE / "benchmark-results" / f), path_in_repo=f,
                        repo_id="csoai/coai-bench", repo_type="dataset",
                        commit_message="SOV signal — sov34 vs frontier vs law, training-valued rows")
    print("uploaded SOV signal to HF csoai/coai-bench")
except Exception as e:
    print("HF upload:", str(e)[:80])
