#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
board_ci.py — GovBench as eval-as-code (the Ori Eval pattern, applied to OUR benchmark).

Ori Eval's insight: "an eval file is code — run it in CI to block a regression, re-run it when a
new model comes out." This applies that to GovBench. It runs in two layers:

  LAYER 1 — DETERMINISTIC INVARIANTS (no API, always runs, gates every CI build):
    - the scorer maps known replies to known tiers (extractor contract)
    - the item bank's fingerprint is unchanged (a score is only valid for its item set)
    - the benchmark DISCRIMINATES: the best statute-blind strategy scores < DISCRIMINATION_CEIL,
      so a real model has something to beat. If a future item-set edit lets "always-HIGH_RISK"
      score 0.9, the benchmark has stopped measuring and CI must go red.
    - degenerate strategies LOSE (mirrors the published task's test_degenerate_strategies_lose)

  LAYER 2 — MODEL ROWS (runs only when a provider key is live; skipped, not failed, otherwise):
    - every live model must clear the statute-blind ceiling (else it isn't reading statute)
    - the unmeasured rate must be under MAX_UNMEASURED (else the run is too rate-limited to trust)

Exit non-zero on any invariant breach → drop-in for a GitHub Actions gate. Re-runnable on a new
model by adding it to MODELS. This is the harness the SOVOS "harness, not model" thesis needs:
one signed board, N sites embed it, CI keeps it honest.

Usage:
  python3 board_ci.py                 # Layer 1 only (CI-safe, no network)
  python3 board_ci.py --with-models   # + Layer 2 against whatever provider keys are live
"""
import argparse, json, os, re, sys, hashlib, urllib.request, urllib.error, time
from pathlib import Path
import openrouter_board as B

HERE = Path(__file__).resolve().parent
BANK = json.loads((HERE / "board_items_govbench.json").read_text())
ITEMS = BANK["items"]
INST = BANK["instruction"]

# ── invariant thresholds (the contract CI enforces) ─────────────────────────────────────
PINNED_FINGERPRINT = hashlib.sha256(json.dumps(ITEMS, sort_keys=True).encode()).hexdigest()[:16]
DISCRIMINATION_CEIL = 0.50   # best statute-blind strategy must score below this
MAX_UNMEASURED = 0.34        # a model run with >34% unmeasured is too degraded to rank

fails, notes = [], []


def check(cond, msg):
    (notes if cond else fails).append(("✅" if cond else "❌") + " " + msg)


# ── LAYER 1 — deterministic, no network ─────────────────────────────────────────────────
def layer1():
    # scorer contract
    for text, want in [("PROHIBITED", "PROHIBITED"), ("The answer is HIGH_RISK.", "HIGH_RISK"),
                       ("limited-risk", "LIMITED_RISK"), ("I cannot help with that.", "")]:
        check(B.extract_tier(text) == want, f"extract({text!r:32}) == {want!r}")
    # fingerprint integrity
    fp = hashlib.sha256(json.dumps(ITEMS, sort_keys=True).encode()).hexdigest()[:16]
    check(fp == PINNED_FINGERPRINT, f"item fingerprint pinned ({fp})")
    # discrimination: best statute-blind strategy < ceiling
    base = B.degenerate_rows(ITEMS)
    best = max(v["accuracy"] for v in base.values())
    check(best < DISCRIMINATION_CEIL,
          f"discriminates — best statute-blind strategy {best:.3f} < {DISCRIMINATION_CEIL}")
    for name, v in base.items():
        check(v["accuracy"] < DISCRIMINATION_CEIL, f"degenerate {name} loses ({v['accuracy']:.3f})")
    # every expected label is in the tier vocabulary
    vocab = {"PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK"}
    bad = {exp for _, exp, _ in ITEMS if exp not in vocab}
    check(not bad, f"all {len(ITEMS)} expected labels in tier vocabulary")


# ── LAYER 2 — live models (skips cleanly if no key) ─────────────────────────────────────
def env(name):
    e = (HERE / ".env").read_text(errors="ignore")
    m = re.search(rf"^{name}\s*=\s*['\"]?([^'\"\n#]+)", e, re.M)
    return m.group(1).strip() if m else ""


def call_gemini(prompt, key, model="gemini-2.5-flash"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0, "maxOutputTokens": 24}}).encode()
    try:
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=45) as r:
            d = json.loads(r.read())
        return d.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip(), "OK"
    except urllib.error.HTTPError as e:
        return "", f"HTTP{e.code}"
    except Exception as e:
        return "", str(e)[:30]


def call_oai(prompt, key, base, model):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 24, "temperature": 0}).encode()
    try:
        req = urllib.request.Request(base, data=body,
                                     headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=45) as r:
            d = json.loads(r.read())
        return d["choices"][0]["message"]["content"].strip(), "OK"
    except urllib.error.HTTPError as e:
        return "", f"HTTP{e.code}"
    except Exception as e:
        return "", str(e)[:30]


# provider registry — add a lab here and it joins the board when its key is live
PROVIDERS = {
    "gemini-2.5-flash": lambda p: call_gemini(p, env("GEMINI_API_KEY")) if env("GEMINI_API_KEY") else ("", "NO_KEY"),
    "deepseek-chat":    lambda p: call_oai(p, env("DEEPSEEK_API_KEY"), "https://api.deepseek.com/chat/completions", "deepseek-chat") if env("DEEPSEEK_API_KEY") else ("", "NO_KEY"),
    "kimi-k2":          lambda p: call_oai(p, env("MOONSHOT_API_KEY"), "https://api.moonshot.ai/v1/chat/completions", "moonshot-v1-8k") if env("MOONSHOT_API_KEY") else ("", "NO_KEY"),
}


def layer2(pace=4.5):
    ran = 0
    for model, fn in PROVIDERS.items():
        # liveness probe — one call; skip provider cleanly if key dead/absent
        _, st = fn("Reply with exactly: OK")
        if st != "OK":
            notes.append(f"⏭  {model}: skipped ({st}) — no live key, not a failure")
            continue
        ran += 1
        correct = wrong = unmeasured = 0
        for scn, exp, _ in ITEMS:
            reply, s = fn(INST + "\n\nScenario: " + scn)
            got = B.extract_tier(reply) if s == "OK" else ""
            if s != "OK" or reply == "" or got == "":
                unmeasured += 1
            elif got == exp:
                correct += 1
            else:
                wrong += 1
            time.sleep(pace)
        scored = correct + wrong
        p, lo, hi = B.wilson(correct, scored)
        umr = unmeasured / len(ITEMS)
        base = max(v["accuracy"] for v in B.degenerate_rows(ITEMS).values())
        check(umr <= MAX_UNMEASURED, f"{model}: unmeasured {umr:.0%} <= {MAX_UNMEASURED:.0%}")
        if scored:
            check(p > base, f"{model}: acc {p:.3f} beats statute-blind {base:.3f} (CI[{lo:.2f},{hi:.2f}])")
    if not ran:
        notes.append("⏭  Layer 2: no live provider keys — model rows skipped (Layer 1 still gated CI)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-models", action="store_true")
    args = ap.parse_args()
    print(f"GovBench eval-as-code · {len(ITEMS)} items · fingerprint {PINNED_FINGERPRINT}\n")
    layer1()
    if args.with_models:
        layer2()
    for n in notes:
        print("  " + n)
    if fails:
        print("\n  FAILURES:")
        for f in fails:
            print("   " + f)
        sys.exit(1)
    print(f"\n  ✅ all {len(notes)} checks pass — benchmark integrity gated.")


if __name__ == "__main__":
    main()
