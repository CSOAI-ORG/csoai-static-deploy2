#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Background GovBench run on Gemini (free tier, rate-limit aware, checkpointed)."""
import re, json, time, urllib.request, urllib.error, pathlib
import openrouter_board as B

HERE = pathlib.Path(__file__).resolve().parent
env = (HERE / ".env").read_text(errors="ignore")
KEY = re.search(r"^GEMINI_API_KEY\s*=\s*['\"]?([^'\"\n#]+)", env, re.M).group(1).strip()
bank = json.loads((HERE / "board_items_govbench.json").read_text())
INST, items = bank["instruction"], bank["items"]
OUT = HERE / "benchmark-results" / "cross_company_board.json"
MODEL = "gemini-2.5-flash"


def gemini(prompt, tries=6):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0, "maxOutputTokens": 24}}).encode()
    for a in range(tries):
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=45) as r:
                d = json.loads(r.read())
            return d.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip(), "OK"
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(15 * (a + 1)); continue
            return "", f"HTTP{e.code}"
        except Exception as e:
            time.sleep(5); continue
    return "", "RATELIMIT"


correct = wrong = unmeasured = 0
rows = []
for i, (scn, exp, anchor) in enumerate(items, 1):
    reply, st = gemini(INST + "\n\nScenario: " + scn)
    if st != "OK" or reply == "":
        outcome = "unmeasured"; unmeasured += 1
    else:
        got = B.extract_tier(reply)
        if got == "":
            outcome = "unmeasured"; unmeasured += 1
        elif got == exp:
            outcome = "correct"; correct += 1
        else:
            outcome = "wrong"; wrong += 1
    rows.append({"i": i, "expected": exp, "got": reply[:24], "outcome": outcome})
    # checkpoint every item
    scored = correct + wrong
    p, lo, hi = B.wilson(correct, scored)
    OUT.write_text(json.dumps({
        "benchmark": "GovBench — EU AI Act risk tier", "provider": "gemini-direct", "model": MODEL,
        "progress": f"{i}/{len(items)}", "n_items": len(items),
        "correct": correct, "wrong": wrong, "unmeasured": unmeasured, "scored_n": scored,
        "accuracy": p, "ci95": [lo, hi],
        "degenerate_baselines": B.degenerate_rows(items),
        "status": "RUNNING" if i < len(items) else "DONE", "rows": rows,
    }, indent=2))
    time.sleep(4.5)  # ~13 rpm, under the free-tier ceiling

print(f"DONE correct={correct} wrong={wrong} unmeasured={unmeasured} acc={p:.3f} CI[{lo:.3f},{hi:.3f}]")
