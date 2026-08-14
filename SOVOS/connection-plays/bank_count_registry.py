#!/usr/bin/env python3
"""Canonical bank-count registry v0.2 — every csoai HF dataset, every .jsonl, sha-pinned.
Doctrine: the file is the truth, not the card. Every count names its set.
Canary forms seen in the wild: `_canary: true` (bool), `_canary: "GUID-string"`, `canary: true`.
"""
import json, subprocess, sys, urllib.request, collections, hashlib
from datetime import datetime, timezone

def hf_token():
    try:
        return subprocess.run(["security","find-generic-password","-s","meok-keystone","-a","HF_TOKEN","-w"],
                              capture_output=True,text=True).stdout.strip() or None
    except Exception:
        return None

TOK = hf_token()
def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"} if TOK else {})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def is_canary(r):
    for k in ("_canary", "canary"):
        v = r.get(k)
        if v is True or (isinstance(v, str) and v.strip()):
            return True
    return False

LABEL_FIELDS = ("gold", "label", "verdict", "expected", "class")

ds = json.loads(get("https://huggingface.co/api/datasets?author=csoai&limit=100"))
print(f"datasets: {len(ds)}", file=sys.stderr)

registry = []
for d in sorted(ds, key=lambda x: x["id"]):
    rid = d["id"]
    entry = {"id": rid, "private": d.get("private", False), "banks": [], "other_files": []}
    try:
        meta = json.loads(get(f"https://huggingface.co/api/datasets/{rid}"))
        sibs = meta.get("siblings", [])
        entry["sha"] = meta.get("sha")
        for s in sibs:
            fn = s["rfilename"]
            if not fn.endswith(".jsonl"):
                entry["other_files"].append(fn)
                continue
            raw = get(f"https://huggingface.co/datasets/{rid}/resolve/main/{fn}")
            sha = hashlib.sha256(raw).hexdigest()
            lines = [l for l in raw.decode("utf-8", "replace").splitlines() if l.strip()]
            rows = []
            for l in lines:
                try: rows.append(json.loads(l))
                except Exception: pass
            canary = sum(1 for r in rows if is_canary(r))
            real_rows = [r for r in rows if not is_canary(r)]
            labels = collections.Counter()
            for r in real_rows:
                for f in LABEL_FIELDS:
                    v = r.get(f)
                    if isinstance(v, (str, int)) and str(v).strip():
                        labels[f"{f}={v}"] += 1
                        break
            texts = [str(r.get("text") or r.get("prompt") or "") for r in real_rows]
            nonempty = [t for t in texts if t]
            dupes = (len(nonempty) - len(set(nonempty))) if nonempty else None
            entry["banks"].append({
                "file": fn, "sha256": sha, "rows": len(rows), "real": len(real_rows),
                "canary": canary, "labels": dict(labels.most_common(14)),
                "duplicate_texts": dupes, "n30_floor": len(real_rows) >= 30,
            })
    except Exception as e:
        entry["error"] = str(e)[:200]
    registry.append(entry)
    nb = len(entry["banks"])
    print(f"  {rid}: jsonl={nb}", file=sys.stderr)

out = {
    "kind": "csoai.bank-count-registry",
    "version": "0.2",
    "generated": datetime.now(timezone.utc).isoformat(),
    "doctrine": "the file is the truth, not the card; rows = all parsed lines, real = rows minus canary (any truthy _canary/canary value); labels = first present of gold/label/verdict/expected/class",
    "datasets": registry,
}
path = "/Users/nicholas/Documents/kimi/workspace/bank-count-registry-2026-08-14.json"
json.dump(out, open(path, "w"), indent=1)
nb = sum(len(e["banks"]) for e in registry)
print(json.dumps({"written": path, "datasets": len(registry), "jsonl_files_counted": nb}, indent=1))
