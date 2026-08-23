import json, pathlib, re, hashlib, html as htmllib
from collections import Counter

V7 = pathlib.Path("/Users/nicholas/clawd/oowm-v7-e2e")
DEPLOY2 = pathlib.Path("/Users/nicholas/clawd/csoai-static-deploy2")
seed = json.loads((V7 / "oowm_seed_1000.json").read_text())
H = {hashlib.md5(d["t"][:400].encode()).hexdigest() for d in seed}

def strip_html(raw):
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = htmllib.unescape(raw)
    raw = re.sub(r"\s+", " ", raw)
    return raw.strip()

def classify(fname):
    n = fname.lower()
    if any(k in n for k in ["defra", "ea-", "env", "flood", "water", "climate", "nature", "pollution"]): return "quant"
    if any(k in n for k in ["dwp", "benefit", "care", "pension", "allowance", "universal-credit", "child"]): return "mom"
    if any(k in n for k in ["mod-", "defence", "defense", "nuclear", "cyber", "army", "navy", "royal", "space", "submarine"]): return "king"
    if any(k in n for k in ["hmrc", "tax", "customs", "treasury"]): return "quant"
    if any(k in n for k in ["fca", "ofgem", "bank", "financial", "energy", "ofcom", "telecom"]): return "king"
    if any(k in n for k in ["moj", "justice", "court", "prison", "prosec", "sfo"]): return "council"
    if any(k in n for k in ["nhs", "health", "medical", "medicines"]): return "mom"
    if any(k in n for k in ["dsit", "ai-safety", "science", "research"]): return "oowm"
    if any(k in n for k in ["dcms", "culture", "media", "sport", "gambling"]): return "free"
    if any(k in n for k in ["home-office", "border", "immigration", "police", "asylum"]): return "king"
    if any(k in n for k in ["council", "bft", "seal", "governance", "procurement"]): return "council"
    return "king"

def chunk(text, size=250):
    text = text.replace(". ", ".|").replace("? ", "?|").replace("! ", "!|")
    parts = text.split("|")
    chunks, cur = [], ""
    for p in parts:
        if len(cur) + len(p) + 1 > size and cur:
            chunks.append(cur.strip())
            cur = p
        else:
            cur = (cur + " " + p).strip()
    if cur:
        chunks.append(cur.strip())
    return [c for c in chunks if len(c) >= 40]

fused = []
seen = set()

def add(s, d, t, cap=None):
    if cap is not None and sum(1 for x in fused if x["s"] == s) >= cap:
        return
    t = t[:400]
    k = hashlib.md5(t.encode()).hexdigest()
    if k in H or k in seen:
        return
    seen.add(k)
    fused.append({"s": s, "d": d, "t": t})

# DEFONEOS packs: 523 html pages
pages = sorted(DEPLOY2.glob("defoneos-*.html"))
added = 0
for p in pages:
    raw = p.read_text(encoding="utf-8", errors="ignore")
    txt = strip_html(raw)
    if len(txt) < 120:
        continue
    dom = classify(p.name)
    src = "defoneos"
    chunks = chunk(txt)
    for c in chunks:
        add(src, dom, c, cap=20000)
    added += 1

print("pages mined:", added, "of", len(pages))
print("new docs:", len(fused))
from collections import Counter as C
print("by domain:", dict(C(x["d"] for x in fused)))
out = V7 / "oowm_seed_1000.json"
seed_full = seed + fused
out.write_text(json.dumps(seed_full, ensure_ascii=False))
print("FINAL TOTAL:", len(seed_full), "docs,", round(out.stat().st_size / 1e6, 1), "MB")