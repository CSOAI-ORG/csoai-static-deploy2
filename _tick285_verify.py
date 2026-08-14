import urllib.request, hashlib, ssl
ctx = ssl._create_unverified_context()
base_in = "https://f17c7070.csoai-site.pages.dev"
slugs = ["defoneos-forestry-land-scotland-ai-deep-dive-pack",
         "defoneos-highlands-islands-enterprise-ai-deep-dive-pack",
         "defoneos-belfast-harbour-ai-deep-dive-pack"]
def md5(b): return hashlib.md5(b).hexdigest()
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (tick285-verify)"})
    return urllib.request.urlopen(req, context=ctx, timeout=30).read()
ok = True
for s in slugs:
    for ext in [".html", ".html.llm.json"]:
        live = fetch(base_in + "/" + s + ext)
        local = open(s + ext, "rb").read()
        match = md5(live) == md5(local)
        ok = ok and match
        extra = ""
        if ext == ".html":
            d = live.decode(errors='ignore')
            extra = " h1=" + str("<h1>" in d) + " eps=" + str(d.count('class="en"'))
        print(f"{s[:38]:40s} {ext:12s} HTTP {len(live)}b  {match and 'BYTE-MATCH' or 'MISMATCH'}{extra}")
for sm in ["sitemap.xml","sitemap-ai.xml"]:
    live = fetch(base_in + "/" + sm)
    local = open(sm,"rb").read()
    m = md5(live)==md5(local)
    n = live.count(b"<ns0:loc>")
    sl = [x for x in slugs if x.encode() in live]
    print(f"{sm:14s} {len(live)}b  match={m}  loc={n}  new_slugs={sl}")
    ok = ok and m
live = fetch(base_in + "/tick-285-sigil.json")
local = open("tick-285-sigil.json","rb").read()
print("tick-285-sigil.json", len(live), "b", md5(live)==md5(local) and "BYTE-MATCH" or "MISMATCH")
print("ALL_OK" if ok else "SOME_FAIL")
