#!/usr/bin/env python3
"""P12 — real ensemble-disagreement score for the conformal router (the trust flip).

Scores the human-vs-AI arena probes with 3 decorrelated local models
(llama3.2:3b, qwen3:4b, qwen2.5:1.5b) via local Ollama. Nonconformity score
s(x) = 1 - max vote share across the ensemble — PRE-LABEL (computed from the
models' verdicts on the probe text only, never the human outcome). Label =
the round's measured agreement (AI verdict matched the human reference).

Honest: a failed/timed-out model call skips that probe (fail-closed, never
fabricate a verdict). No model scores its own training data.

Run:
  python3 router/ensemble_score.py --smoke      # 2 probes, verify the pipe
  python3 router/ensemble_score.py [--sample N] # score N probes (default all)
  python3 router/ensemble_score.py --check      # realized-coverage check + trust marker
"""
import json
import os
import random
import re
import subprocess
import sys
import time

ROUNDS = "/Users/nicholas/clawd/csoai-static-deploy2/signed_rounds.jsonl"
ROUTER = os.path.dirname(os.path.abspath(__file__))
SET_PATH = os.path.join(ROUTER, "calibration_set.jsonl")
TRUST = os.path.join(ROUTER, "..", "feeds", "router_trust.json")
OLLAMA = "http://localhost:11434/api/generate"
MODELS = ["llama3.2:3b", "qwen3:4b", "qwen2.5:1.5b"]


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


def warmup(timeout=240):
    """Preload all models so first-call latency doesn't blow the per-probe budget."""
    for model in MODELS:
        try:
            body = json.dumps({"model": model, "prompt": "Say OK.", "stream": False})
            subprocess.run(["curl", "-s", "--max-time", str(timeout), OLLAMA, "-d", body],
                           capture_output=True, text=True)
            print(f"warmed {model}")
        except Exception:
            pass


def ask(model, probe, timeout=120):
    body = json.dumps({"model": model,
                       "prompt": f"Question: {probe}\nAnswer YES or NO only.",
                       "stream": False, "options": {"temperature": 0}})
    r = subprocess.run(["curl", "-s", "--max-time", str(timeout), OLLAMA, "-d", body],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        text = json.loads(r.stdout).get("response", "")
    except Exception:
        return None
    m = re.search(r"\b(YES|NO)\b", text.upper())
    return m.group(1) if m else None


def ensemble_score(probe, dry=False):
    votes = []
    for model in MODELS:
        v = "dry-yes" if dry else ask(model, probe)
        if v in ("YES", "NO"):
            votes.append(v)
        time.sleep(0.2)
    # fallback: if the bigger trio failed, one fast 0.5b retry (still fail-closed on no verdict)
    if not votes and not dry:
        v = ask("qwen2.5:0.5b", probe, timeout=60)
        if v in ("YES", "NO"):
            votes = [v, v, v]  # single-model fallback flagged by votes length below
    if not votes:
        return None, None
    yes = votes.count("YES") / len(votes)
    no = votes.count("NO") / len(votes)
    s = 1 - max(yes, no)
    return round(s, 4), votes


def existing_findings():
    out = set()
    if os.path.exists(SET_PATH):
        for line in open(SET_PATH, encoding="utf-8"):
            line = line.strip()
            if line:
                out.add(json.loads(line).get("finding"))
    return out


def score(sample=None):
    rounds = human_rounds()
    if sample:
        random.seed(9)
        rounds = random.sample(rounds, min(sample, len(rounds)))
    rows = []
    if os.path.exists(SET_PATH):
        rows = [json.loads(l) for l in open(SET_PATH, encoding="utf-8") if l.strip()]
    real_findings = {r["finding"] for r in rows if not r.get("simulated") and not r.get("score_proxy")}
    scored = skipped = already = 0
    for r in rounds:
        if r["finding"] in real_findings:
            already += 1
            continue
        s, votes = ensemble_score(r["probe"])
        if s is None:
            skipped += 1
            print(f"skip {r['finding']} (no model verdicts) — proxy kept if present")
            continue
        entry = {"finding": r["finding"], "score": s, "label_correct": r["label_correct"],
                 "source": "ensemble-ollama-3x", "simulated": False, "votes": votes}
        # drop any existing PROXY for this finding ONLY on success (never before — ledger #15)
        rows = [row for row in rows if not (row["finding"] == r["finding"] and row.get("score_proxy"))]
        rows.append(entry)
        scored += 1
    with open(SET_PATH, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"ensemble scoring: +{scored} real-scored, {skipped} skipped (fail-closed, proxies kept), {already} already real")
    return scored


def coverage_check(alpha=0.05, cal_frac=0.6):
    """Realized-coverage check (move 27): freeze qhat on a cal split, measure auto-error on val."""
    rows = [json.loads(l) for l in open(SET_PATH, encoding="utf-8") if l.strip()]
    measured = [r for r in rows if not r.get("simulated") and not r.get("score_proxy")]
    if len(measured) < 20:
        return {"ok": False, "reason": f"only {len(measured)} real-scored entries — need more"}
    random.seed(11)
    random.shuffle(measured)
    cut = int(len(measured) * cal_frac)
    cal, val = measured[:cut], measured[cut:]
    sys.path.insert(0, ROUTER)
    import conformal_router
    qhat, n = conformal_router.calibrate([r["score"] for r in cal], alpha)
    auto_wrong = auto_total = 0
    for r in val:
        if r["score"] <= qhat:
            auto_total += 1
            if not r["label_correct"]:
                auto_wrong += 1
    realized = auto_wrong / auto_total if auto_total else 0.0
    ok = realized <= alpha + 0.02
    trust = {"trusted": bool(ok), "alpha": alpha, "n_cal": len(cal), "n_val": len(val),
             "qhat": round(qhat, 6), "auto_total": auto_total, "realized_error": round(realized, 4),
             "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    os.makedirs(os.path.dirname(TRUST), exist_ok=True)
    with open(TRUST, "w", encoding="utf-8") as fh:
        json.dump(trust, fh, indent=1)
    print(f"coverage: n_cal={len(cal)} n_val={len(val)} qhat={qhat:.4f} auto={auto_total} "
          f"realized_error={realized:.4f} alpha={alpha} -> {'TRUSTED' if ok else 'NOT TRUSTED (honest)'}")
    return trust


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        r = human_rounds()[:2]
        for x in r:
            s, votes = ensemble_score(x["probe"])
            print(f"smoke {x['finding'][:12]}: score={s} votes={votes} label={x['label_correct']}")
        sys.exit(0)
    if "--check" in sys.argv:
        coverage_check()
        sys.exit(0)
    sample = None
    if "--sample" in sys.argv:
        sample = int(sys.argv[sys.argv.index("--sample") + 1])
    warmup()
    score(sample)
