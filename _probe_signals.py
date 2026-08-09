import re
from pathlib import Path
ROOT=Path('.')
RE_DESC = re.compile(r'name="description"')
# mirror test thresholds for S1-S4
for p in sorted(ROOT.glob('*.html')):
    c=p.read_text(errors='ignore')
    s1 = bool(RE_DESC.search(c))
    s2 = bool(re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>', c, re.I))
    s3 = bool(re.search(r'og:title', c, re.I)) and bool(re.search(r'og:description', c, re.I))
    s4 = bool(re.search(r'application/ld\+json', c, re.I)) and bool(re.search(r'"@type"\s*:\s*"(Article|WebPage|Organization|ItemList|CollectionPage)"', c))
    if not all([s1,s2,s3,s4]):
        print(f"{p.name}: s1={s1} s2={s2} s3={s3} s4={s4}")
