#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
openrouter_board.py — cross-company GovBench board.

Runs the FROZEN GovBench EU-AI-Act tier item set (board_items_govbench.json, a read-only
snapshot of the published kaggle task — NOT the live-edited task file) against any number of
models, via either OpenRouter (every frontier model, one key) or a local/pod Ollama.

Deterministic scoring, identical to the published contract:
  - INSTRUCTION + scenario -> reply
  - first tier token the reply commits to  (_extract_tier, first-token-wins)
  - exact-match against statute-anchored ground truth

THE THREE-OUTCOME RULE (why this file can't report false success):
  correct | wrong | UNMEASURED.  An empty reply or a provider error is UNMEASURED — it is
  excluded from the accuracy denominator, never scored as a wrong answer. A safety-trained model
  that declines is not the same as a model that gets the statute wrong, and a 401 is not a 0%.

Degenerate reference rows (all-PROHIBITED, all-HIGH_RISK, uniform) are computed offline with no
model call, so the board always shows whether real models beat statute-blind guessing.

Usage:
  # free arm — pod/local Ollama:
  python3 openrouter_board.py --provider ollama --base http://POD:11434 --models sov34:latest
  # frontier arm — OpenRouter (reads OPENROUTER_API_KEY from env or --key):
  python3 openrouter_board.py --provider openrouter \
      --models anthropic/claude-opus-5 openai/gpt-5.6 google/gemini-3.6-flash \
               x-ai/grok-4.5 deepseek/deepseek-chat moonshotai/kimi-k3
"""
import argparse, json, os, re, sys, time, hashlib, urllib.request, urllib.error
from pathlib import Path
from math import sqrt

HERE = Path(__file__).resolve().parent
BANK = HERE / "board_items_govbench.json"
OUT = HERE / "benchmark-results" / "cross_company_board.json"

# ── faithful scoring contract (mirrors kaggle/govbench_kaggle_task.py) ───────────────────
TIERS = ("PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK")
_TIER_RX = {t: re.compile(rf"\b{t.replace('_', '[ _-]?')}\b", re.I) for t in TIERS}


def extract_tier(text: str) -> str:
    """First tier the reply commits to, or '' if it never names one (first-token-wins)."""
    hits = [(m.start(), t) for t, rx in _TIER_RX.items() if (m := rx.search(text or ""))]
    return min(hits)[1].upper().replace(" ", "_").replace("-", "_") if hits else ""


def wilson(k: int, n: int):
    """95% Wilson interval for a proportion — honest small-n bounds."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    z = 1.96
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(p, 4), round(max(0, c - h), 4), round(min(1, c + h), 4))


# ── provider adapters — each returns (reply_text, status) ────────────────────────────────
def call_openrouter(model, prompt, key, timeout=90):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 24, "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}",
                 "HTTP-Referer": "https://csoai.org", "X-Title": "CSOAI GovBench"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        if "error" in d:
            return "", f"ERROR:{str(d['error'])[:80]}"
        return d["choices"][0]["message"]["content"].strip(), "OK"
    except urllib.error.HTTPError as e:
        return "", f"ERROR:HTTP{e.code}"
    except Exception as e:
        return "", f"ERROR:{str(e)[:60]}"


def call_ollama(model, prompt, base, timeout=90):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0, "num_predict": 24}}).encode()
    req = urllib.request.Request(base.rstrip("/") + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return d.get("response", "").strip(), "OK"
    except Exception as e:
        return "", f"ERROR:{str(e)[:60]}"


# ── scoring one model over the frozen bank ───────────────────────────────────────────────
def score_model(model, provider, instruction, items, **kw):
    correct = wrong = empty = errored = 0
    rows = []
    for scenario, expected, anchor in items:
        prompt = instruction + "\n\nScenario: " + scenario
        if provider == "openrouter":
            reply, status = call_openrouter(model, prompt, kw["key"])
        else:
            reply, status = call_ollama(model, prompt, kw["base"])
        if status.startswith("ERROR"):
            errored += 1
            outcome = "unmeasured"
        elif reply.strip() == "":
            empty += 1
            outcome = "unmeasured"  # PROVIDER_EMPTY — decline != wrong answer
        else:
            got = extract_tier(reply)
            if got == "":
                empty += 1  # named no tier -> also unmeasured, not a wrong statute read
                outcome = "unmeasured"
            elif got == expected:
                correct += 1
                outcome = "correct"
            else:
                wrong += 1
                outcome = "wrong"
        rows.append({"expected": expected, "got": reply[:40], "outcome": outcome, "anchor": anchor})
    scored = correct + wrong
    p, lo, hi = wilson(correct, scored)
    return {
        "model": model, "provider": provider,
        "correct": correct, "wrong": wrong, "unmeasured": empty + errored,
        "empty": empty, "errored": errored, "scored_n": scored,
        "accuracy": p, "ci95": [lo, hi],
        "status": "OK" if scored else "UNMEASURED",
        "rows": rows,
    }


def degenerate_rows(items):
    """Offline reference: what statute-blind strategies score. Proves the board discriminates."""
    ref = {}
    for strat in ("PROHIBITED", "HIGH_RISK", "MINIMAL_RISK"):
        k = sum(1 for _, exp, _ in items if exp == strat)
        p, lo, hi = wilson(k, len(items))
        ref[f"always-{strat}"] = {"correct": k, "scored_n": len(items), "accuracy": p, "ci95": [lo, hi]}
    return ref


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=["openrouter", "ollama"], required=True)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--base", default="http://localhost:11434", help="ollama base url")
    ap.add_argument("--key", default=os.environ.get("OPENROUTER_API_KEY", ""))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    bank = json.loads(BANK.read_text())
    instruction, items = bank["instruction"], bank["items"]
    fp = hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest()[:16]
    print(f"GovBench cross-company board · {len(items)} items · fingerprint {fp}")

    if args.provider == "openrouter" and not args.key:
        sys.exit("no OPENROUTER_API_KEY — export it or pass --key")

    board, kw = [], ({"key": args.key} if args.provider == "openrouter" else {"base": args.base})
    for m in args.models:
        t0 = time.time()
        res = score_model(m, args.provider, instruction, items, **kw)
        dt = round(time.time() - t0, 1)
        flag = "✓" if res["status"] == "OK" else "⚠"
        print(f"  {flag} {m:38} acc={res['accuracy']:.3f} "
              f"CI[{res['ci95'][0]:.2f},{res['ci95'][1]:.2f}] "
              f"n={res['scored_n']} unmeasured={res['unmeasured']} ({dt}s)")
        board.append(res)

    out = {
        "benchmark": "GovBench — EU AI Act risk tier",
        "item_fingerprint": fp, "n_items": len(items),
        "degenerate_baselines": degenerate_rows(items),
        "models": sorted(board, key=lambda r: (-r["accuracy"], r["model"])),
        "generated_by": "openrouter_board.py", "provider": args.provider,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=2))
    print(f"→ {args.out}")

    # optional Ed25519 signature if the estate signer is present
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa
        print("  (sign with sign_board.py to append to the attestation chain)")
    except Exception:
        pass


if __name__ == "__main__":
    main()
