import urllib.request, ssl, hashlib, ssl

ctx = ssl._create_unverified_context()
UA = {"User-Agent": "Mozilla/5.0 JEEVES-tick280-verify"}
BASE = "https://feat-sandbox-arena-seam.csoai-site.pages.dev"
packs = ["saas-student-awards-agency-scotland",
         "nipb-northern-ireland-policing-board",
         "scra-scottish-childrens-reporter-administration"]

def md5b(data):
    return hashlib.md5(data).hexdigest()

def fetch(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return -1, str(e).encode()

ok = True
for p in packs:
    fn = f"defoneos-{p}-ai-deep-dive-pack.html"
    for tgt in (fn, fn + ".llm.json"):
        code, body = fetch("/" + tgt)
        src = open(tgt, "rb").read()
        smd5 = md5b(src)
        live = md5b(body) if isinstance(body, bytes) and body else None
        match = (live == smd5) if live else False
        if code != 200:
            ok = False
        print(f"{tgt}: HTTP {code} src={smd5[:8]} live={str(live)[:8]} {'MATCH' if match else 'DIFF'}")

# sitemap checks
for sm in ("sitemap.xml", "sitemap-ai.xml"):
    code, body = fetch("/" + sm)
    txt = body.decode(errors="replace") if isinstance(body, bytes) else ""
    slugs = all(f"{p}-ai-deep-dive-pack.html" in txt for p in packs)
    n = txt.count("<ns0:loc>")
    print(f"{sm}: HTTP {code} urls={n} all3_present={slugs}")
    ok = ok and code == 200 and slugs

print("VERIFY", "PASS" if ok else "FAIL")