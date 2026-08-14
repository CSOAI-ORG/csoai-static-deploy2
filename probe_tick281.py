import re, os, glob

ROOT="/Users/nicholas/clawd/csoai-static-deploy2"

def urls(f):
    t=open(os.path.join(ROOT,f)).read()
    return re.findall(r'<ns0:loc>(.*?)</ns0:loc>', t)

sm=urls("sitemap.xml")
smai=urls("sitemap-ai.xml")
print("sitemap.xml locs:", len(sm))
print("sitemap-ai.xml locs:", len(smai))

cands = {
 "defoneos-education-authority-northern-ireland-ai-deep-dive-pack": "Education Authority NI",
 "defoneos-scottish-legal-aid-board-ai-deep-dive-pack": "Scottish Legal Aid Board",
 "defoneos-social-security-scotland-ai-deep-dive-pack": "Social Security Scotland",
 "defoneos-scottish-water-ai-deep-dive-pack": "Scottish Water",
 "defoneos-northern-ireland-housing-executive-ai-deep-dive-pack": "NI Housing Executive",
 "defoneos-scotrail-ai-deep-dive-pack": "ScotRail",
}
all_sm=set()
for u in sm+smai:
    m=re.search(r'/([^/]+)\.html$', u)
    if m: all_sm.add(m.group(1))

for slug,name in cands.items():
    ondisk=os.path.exists(os.path.join(ROOT,slug+".html"))
    insm=slug in all_sm
    print(f"{name:35s} disk={ondisk!s:5} sitemap={insm!s:5} -> {'COVERED skip' if (ondisk or insm) else 'OPEN'}")
