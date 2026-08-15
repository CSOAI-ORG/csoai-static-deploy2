#!/usr/bin/env python3
"""audit_negative_items.py — independent adjudication of the negatively-discriminating items.

WHY THESE 18 ITEMS
------------------
axis-saturation.json flagged 18 of 90 GSPC items with point-biserial < -0.2 against the model's
rest-score: models that do BETTER overall do WORSE on these. That pattern is what a wrong answer
key looks like from the outside. It is not proof — at 8 models a correlation of -0.2 is noisy —
so the flag is a screening signal, and this resolves it with an independent opinion.

THE ADJUDICATOR AND ITS LIMITS
------------------------------
openai/gpt-oss-20b:free via OpenRouter. Chosen because it is the only capable model this
account can actually call: paid models return HTTP 402 ("this account never purchased
credits"), so a genuine frontier judge is not available.

A 20B open model is NOT an authority on EU law and this is NOT a frontier-judge validation.
What it is: an opinion formed without ever seeing the answer key, from a model roughly 40x
larger than most of the fleet that produced the negative correlation. Its disagreement does not
prove a key wrong. It raises an item from ONE suspicious signal to TWO INDEPENDENT ones, which
is the difference between a hunch and a review queue.

Every disagreement is output for HUMAN adjudication. Nothing here rewrites a key.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gspc_six_axis_e2e as G  # noqa: E402

KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "openai/gpt-oss-20b:free"
SRC = HERE / "evidence/harness/freeze/latest/axis-saturation.json"


def judge(prompt: str, labels: list[str]) -> tuple[str | None, str]:
    """Returns (label, raw). Reasoning models put the answer in `reasoning` when truncated, so
    max_tokens is generous and both fields are searched — reading only `content` would score a
    truncated reasoning trace as a non-answer."""
    body = json.dumps({
        "model": MODEL, "temperature": 0, "max_tokens": 1600,
        "messages": [{"role": "user", "content":
                      f"{prompt}\n\nAnswer with EXACTLY ONE of these labels: "
                      f"{' | '.join(labels)}\nEnd your reply with: FINAL: <label>"}]}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {KEY}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.loads(r.read())
        msg = d["choices"][0]["message"]
        raw = (msg.get("content") or "") + "\n" + (msg.get("reasoning") or "")
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:120]}"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
    m = re.search(r"FINAL:\s*([A-Z_]+)", raw)
    if m and m.group(1) in labels:
        return m.group(1), raw
    hits = [l for l in labels if re.search(rf"\b{re.escape(l)}\b", raw.upper())]
    return (hits[-1] if len(set(hits)) == 1 else None), raw


def main():
    if not KEY:
        sys.exit("OPENROUTER_API_KEY not set")
    sat = json.loads(SRC.read_text())["axes"]

    targets = []
    for axis, a in sat.items():
        items, field, labels = G.load_axis(axis)
        for r in a["items"]:
            if r.get("discrimination") is not None and r["discrimination"] < -0.2:
                targets.append((axis, r["item"], items[r["item"]], field, labels,
                                r["discrimination"], r["difficulty"]))
    print(f"ADJUDICATING {len(targets)} negatively-discriminating items via {MODEL}")
    print(f"  (paid models return 402 — this is the strongest adjudicator this account can call)\n",
          flush=True)

    agree = disagree = unresolved = 0
    out = []
    for axis, idx, it, field, labels, disc, diff in targets:
        lab, raw = judge(it[field], labels)
        key = it["expected"]
        if lab is None:
            verdict, unresolved = "NO_VERDICT", unresolved + 1
        elif lab == key:
            verdict, agree = "AGREES_WITH_KEY", agree + 1
        else:
            verdict, disagree = "DISAGREES_WITH_KEY", disagree + 1
        print(f"  {axis:12s}[{idx:2d}] disc {disc:+.3f} diff {diff:.2f}  key={key:14s} "
              f"judge={str(lab):14s} {verdict}", flush=True)
        if verdict == "DISAGREES_WITH_KEY":
            print(f"       anchor: {it.get('anchor')}")
        out.append({"axis": axis, "item": idx, "discrimination": disc, "difficulty": diff,
                    "key": key, "judge": lab, "verdict": verdict,
                    "anchor": it.get("anchor"), "prompt": it[field][:400],
                    "judge_excerpt": raw.strip()[:600]})

    print(f"\n  agrees {agree}   DISAGREES {disagree}   no verdict {unresolved}")
    print("\n  READING: an item flagged by BOTH negative discrimination AND judge disagreement "
          "has two\n  independent signals against its key and belongs at the top of the human "
          "review queue.\n  Agreement does NOT clear an item — it only removes the second signal.")

    dest = HERE / "evidence/harness/freeze/latest/negative-item-audit.json"
    dest.write_text(json.dumps({
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "adjudicator": MODEL, "via": "OpenRouter",
        "why_not_a_frontier_judge": ("paid models return HTTP 402 — 'this account never "
                                     "purchased credits'. This is the strongest model callable."),
        "authority_disclaimer": ("a 20B open model is not an authority on EU law. Disagreement "
                                 "does not prove a key wrong; it raises an item from one "
                                 "suspicious signal to two independent ones. No key is rewritten "
                                 "here."),
        "n_items": len(targets), "agrees": agree, "disagrees": disagree,
        "no_verdict": unresolved, "items": out}, indent=2))
    print(f"\n  -> {dest}")


if __name__ == "__main__":
    main()
