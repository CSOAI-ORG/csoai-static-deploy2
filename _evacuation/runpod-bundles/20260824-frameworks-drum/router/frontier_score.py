#!/usr/bin/env python3
"""P12 attempt #3 — frontier-model confidence score (Gemini, via the estate's litellm key).

A single strong model's CALIBRATED CONFIDENCE is a much better nonconformity score than
small-model disagreement (which failed: realized error 0.53). s(x) = 1 - confidence,
pre-label (confidence comes from the probe, never the human outcome).

Key source: ~/litellm_config.yaml (estate-configured GEMINI_API_KEY). Fail-closed:
no key / no parse => probe skipped, never fabricated. Cost: ~$0.01 for 79 probes (flash).

Run:  python3 router/frontier_score.py [--model gemini-3.6-flash] [--sample N]
      python3 router/frontier_score.py --check   # realized-coverage + trust marker
"""
import json
import os
import random
import re
import subprocess
import sys
import time

ROUTER = os.path.dirname(os.path.abspath(__file__))
SET_PATH = os.path.join(ROUTER, "calibration_set.jsonl")
ROUNDS = "/Users/nicholas/clawd/csoai-static-deploy2/signed_rounds.jsonl"
BASE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def gemini_key():
    """Key NEVER hardcoded/committed: env first, else the estate litellm config (local file)."""
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
          "Answer YES or NO, then give your confidence 0.0-1.0.\n"
          "Format exactly:\nVERDICT: YES\nCONFIDENCE: 0.87")


def ask_gemini(probe, model="gemini-3.6-flash", timeout=60):
    body = json.dumps({"contents": [{"parts": [{"text": PROMPT.format(probe=probe)}]}],
                       "generationConfig": {"temperature": 0}})
    r = subprocess.run(["curl", "-s", "--max-time", str(timeout),
                        "-H", "Content-Type: application/json",
                        f"{BASE.format(model=model)}?key={gemini_key()}", "-d", body],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, None
    try:
        text = json.loads(r.stdout)["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return None, None
    v = re.search(r"\b(YES|NO)\b", text.upper())
    c = None
    cm = re.search(r"(?:CONFIDENCE|confidence)[^\d]*([01]\.\d+|0?\.\d+)", text)
    if not cm:
        cm = re.search(r"\b([01]\.\d+|0?\.\d+)\b", text)  # any 0.x / 1.0 float
    if not cm:
        pm = re.search(r"(\d{1,3})\s*%", text)
        if pm:
            c = min(1.0, int(pm.group(1)) / 100.0)
    else:
        c = float(cm.group(1))
    if not v or c is None or not (0.0 <= c <= 1.0):
        return None, None
    return v.group(1), c


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
    # SAFETY NET (ledger #14): back up before superseding — never wipe on a failed run.
    backup_path = SET_PATH + ".backup.jsonl"
    if rows:
        with open(backup_path, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    kept = [r for r in rows if r["finding"] not in targets]
    if len(kept) != len(rows):
        with open(SET_PATH, "w", encoding="utf-8") as fh:
            for r in kept:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"superseded {len(rows) - len(kept)} prior entries for {len(targets)} findings (backup kept)")
    scored = skipped = 0
    for r in rounds:
        verdict, conf = ask_gemini(r["probe"], model)
        if verdict is None or conf is None:
            skipped += 1
            print(f"skip {r['finding'][:14]} (no parse)")
            continue
        s = round(1 - conf, 4)  # nonconformity = low confidence
        entry = {"finding": r["finding"], "score": s, "label_correct": r["label_correct"],
                 "source": f"{model}-confidence", "simulated": False,
                 "confidence": conf, "verdict": verdict}
        with open(SET_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        scored += 1
        time.sleep(0.3)
    # FAIL-CLOSED RESTORE (ledger #14): if nothing scored (quota/API down) and a backup
    # exists, restore it — the set must never be left wiped by a failed run.
    if scored == 0 and os.path.exists(backup_path):
        os.replace(backup_path, SET_PATH)
        print("RESTORED prior calibration set (scored 0 — API/quota failure); nothing lost")
    print(f"frontier scoring: +{scored} scored, {skipped} skipped (fail-closed)")
    return scored


def coverage_check(alpha=0.05, cal_frac=0.6):
    rows = [json.loads(l) for l in open(SET_PATH, encoding="utf-8") if l.strip()]
    measured = [r for r in rows if not r.get("simulated") and not r.get("score_proxy")]
    real = [r for r in measured if r.get("source", "").startswith("gemini-")]
    if len(real) < 20:
        return {"ok": False, "reason": f"only {len(real)} gemini-scored entries"}
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
             "source": "gemini-3.6-flash-confidence",
             "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    os.makedirs(os.path.join(ROUTER, "..", "feeds"), exist_ok=True)
    with open(os.path.join(ROUTER, "..", "feeds", "router_trust.json"), "w", encoding="utf-8") as fh:
        json.dump(trust, fh, indent=1)
    print(f"frontier coverage: n_cal={len(cal)} n_val={len(val)} qhat={qhat:.4f} auto={at} "
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
