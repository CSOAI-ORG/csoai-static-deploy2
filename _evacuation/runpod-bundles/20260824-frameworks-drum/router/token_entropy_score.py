#!/usr/bin/env python3
"""P12 attempt #4 — token-entropy nonconformity score (TECP-style).

Mean per-token entropy (predictive uncertainty) as the nonconformity score, then split-conformal
calibration + realized-coverage. This is the research-validated signal from docs/RESEARCH_TRUST_FLIP.md.
s(x) = mean over generated tokens of -log p(token) (self-information), or 0 if degenerate.
Pre-label: entropy comes from the probe's generated tokens, never the human outcome.

Difference vs attempt #3 (Gemini raw confidence): entropy is a calibrated uncertainty measure and
a canonical conformal nonconformity score (TECP). Key never hardcoded; fail-closed.

Run: python3 router/token_entropy_score.py [--sample N]   # score
     python3 router/token_entropy_score.py --check         # coverage + trust marker
"""
import json
import math
import os
import random
import re
import subprocess
import sys
import time

ROUTER = os.path.dirname(os.path.abspath(__file__))
SET_PATH = os.path.join(ROUTER, "calibration_set.jsonl")
ROUNDS = os.environ.get("ROUNDS_PATH", "/Users/nicholas/clawd/csoai-static-deploy2/signed_rounds.jsonl")
BASE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def gemini_key():
    k = os.environ.get("GEMINI_API_KEY")
    if k:
        return k
    cfg = os.path.expanduser("~/litellm_config.yaml")
    if os.path.exists(cfg):
        for line in open(cfg, encoding="utf-8"):
            line = line.strip()
            if line.startswith("GEMINI_API_KEY:"):
                v = line.split(":", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    return ""


PROMPT = ("Question: {probe}\n"
          "Answer YES or NO.\n"
          "Format exactly:\nVERDICT: YES")


def ask_entropy(probe, model="gemini-3.6-flash", timeout=60):
    """Request response logprobs; return (verdict, mean_per_token_entropy).

    Backend: Gemini (responseLogprobs) OR a local/pod Ollama generate (top_logprobs). If the
    model doesn't expose logprobs, return (verdict, None) — entropy unsupported (honest).
    Set DECK_BACKEND=ollama + OLLAMA_BASE (e.g. the pod's http://localhost:11434) to use Ollama.
    """
    if os.environ.get("DECK_BACKEND", "gemini") == "ollama":
        obase = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
        body = json.dumps({"model": model, "prompt": PROMPT.format(probe=probe),
                           "stream": False, "options": {"num_predict": 8, "temperature": 0, "top_k": 5}})
        rr = subprocess.run(["curl", "-s", "--max-time", str(timeout), "-H", "Content-Type: application/json",
                             f"{obase}/api/generate", "-d", body], capture_output=True, text=True)
        if rr.returncode != 0:
            return None, None
        try:
            d = json.loads(rr.stdout)
        except Exception:
            return None, None
        text = d.get("response", "")
        v = re.search(r"\b(YES|NO)\b", text.upper())
        if not v:
            return None, None
        logprobs = []
        for tok in d.get("top_logprobs", []) or []:
            if isinstance(tok, dict):
                lp = tok.get("logprob", tok.get("logprobs"))
                if lp is not None:
                    logprobs.append(float(lp))
        if not logprobs:
            return v.group(1), None  # logprobs not returned — entropy unsupported
        return v.group(1), max(0.0, -sum(logprobs) / len(logprobs))
    # Gemini (default)
    body = json.dumps({"contents": [{"parts": [{"text": PROMPT.format(probe=probe)}]}],
                       "generationConfig": {"temperature": 0, "responseLogprobs": True}})
    r = subprocess.run(["curl", "-s", "--max-time", str(timeout),
                        "-H", "Content-Type: application/json",
                        f"{BASE.format(model=model)}?key={gemini_key()}", "-d", body],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, None
    try:
        data = json.loads(r.stdout)
    except Exception:
        return None, None
    if "candidates" not in data or not data["candidates"]:
        return None, None
    cand = data["candidates"][0]
    text = cand.get("content", {}).get("parts", [{}])[0].get("text", "")
    v = re.search(r"\b(YES|NO)\b", text.upper())
    if not v:
        return None, None
    # collect logprobs (per-token; Gemini returns them in the response parts/candidates)
    logprobs = []
    for part in cand.get("content", {}).get("parts", []):
        lp = part.get("logprobs") or part.get("inlineData") or None
        if isinstance(lp, list):
            for tok in lp:
                lp_val = tok.get("logprob") if isinstance(tok, dict) else tok
                if isinstance(lp_val, (int, float)):
                    logprobs.append(float(lp_val))
    if also := data.get("responseLogprobs"):
        for tok in also if isinstance(also, list) else also.get("logprobs", []):
            lp_val = tok.get("logprob") if isinstance(tok, dict) else tok
            if isinstance(lp_val, (int, float)):
                logprobs.append(float(lp_val))
    if not logprobs:
        return v.group(1), None  # no logprobs returned — signal unsupported
    # mean per-token self-information (entropy) = -mean(log p)
    entropy = -sum(logprobs) / len(logprobs)
    return v.group(1), max(0.0, entropy)


def human_rounds():
    out = []
    if not os.path.exists(ROUNDS):
        return out
    for line in open(ROUNDS, encoding="utf-8"):
        d = json.loads(line)
        p = d.get("payload", {})
        if p.get("mode") != "human-vs-ai" or p.get("simulated") is True or p.get("agreement") is None:
            continue
        ai = p.get("right", {}) if p.get("right", {}).get("name") != "human" else p.get("left", {})
        out.append({"finding": f"arena-{d.get('cid', '')[:16]}", "probe": p.get("probe", ""),
                    "label_correct": bool(p["agreement"])})
    return out


def score(sample=None, model="gemini-3.6-flash"):
    rounds = human_rounds()
    if sample:
        random.seed(23)
        rounds = random.sample(rounds, min(sample, len(rounds)))
    rows = []
    if os.path.exists(SET_PATH):
        rows = [json.loads(l) for l in open(SET_PATH, encoding="utf-8") if l.strip()]
    targets = {r["finding"] for r in rounds}
    entropy_ok = 0
    scored = skipped = no_lp = 0
    for r in rounds:
        verdict, ent = ask_entropy(r["probe"], model)
        if verdict is None:
            skipped += 1
            print(f"skip {r['finding'][:14]} (no parse)")
            continue
        if ent is None:
            no_lp += 1
            print(f"no-logprobs {r['finding'][:14]} (entropy unsupported by model)")
            continue
        entropy_ok = 1
        entry = {"finding": r["finding"], "score": round(ent, 4), "label_correct": r["label_correct"],
                 "source": f"{model}-tokenentropy", "simulated": False, "verdict": verdict}
        with open(SET_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        scored += 1
        time.sleep(0.3)
    print(f"token-entropy scoring: +{scored} scored, {skipped} skip, {no_lp} no-logprobs "
          f"(entropy supported: {'yes' if entropy_ok else 'NO — model/logprobs not available'})")
    return scored


def coverage_check(alpha=0.05, cal_frac=0.6):
    rows = [json.loads(l) for l in open(SET_PATH, encoding="utf-8") if l.strip()]
    real = [r for r in rows if r.get("source", "").endswith("tokenentropy")]
    if len(real) < 20:
        return {"ok": False, "reason": f"only {len(real)} token-entropy-scored entries"}
    random.seed(31)
    random.shuffle(real)
    cut = int(len(real) * cal_frac)
    cal, val = real[:cut], real[cut:]
    sys.path.insert(0, ROUTER)
    import conformal_router
    qhat, n = conformal_router.calibrate([r["score"] for r in cal], alpha)
    aw = at = 0
    for r in val:
        if r["score"] <= qhat:
            at += 1
            if not r["label_correct"]:
                aw += 1
    err = aw / at if at else 0.0
    ok = err <= alpha + 0.02
    trust = {"trusted": bool(ok), "alpha": alpha, "n_cal": len(cal), "n_val": len(val),
             "qhat": round(qhat, 6), "auto_total": at, "realized_error": round(err, 4),
             "source": "token-entropy-TECP",
             "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    os.makedirs(os.path.join(ROUTER, "..", "feeds"), exist_ok=True)
    with open(os.path.join(ROUTER, "..", "feeds", "router_trust.json"), "w", encoding="utf-8") as fh:
        json.dump(trust, fh, indent=1)
    print(f"token-entropy coverage: n_cal={len(cal)} n_val={len(val)} qhat={qhat:.4f} auto={at} "
          f"realized_error={err:.4f} alpha={alpha} -> {'TRUSTED' if ok else 'NOT TRUSTED (honest)'}")
    return trust


if __name__ == "__main__":
    if "--check" in sys.argv:
        coverage_check()
        sys.exit(0)
    model = "gemini-3.6-flash"
    if "--model" in sys.argv:
        model = sys.argv[sys.argv.index("--model") + 1]
    sample = None
    if "--sample" in sys.argv:
        sample = int(sys.argv[sys.argv.index("--sample") + 1])
    score(sample, model)
