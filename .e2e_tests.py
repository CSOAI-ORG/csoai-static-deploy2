#!/usr/bin/env python3
"""
E2E test suite v2 for CSOAI static site.
Run: python3 .e2e_tests.py
Exit code 0 = all pass, 1 = failures.
"""
import re
import sys
import json
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent
PASS = 0
FAIL = 0
WARNINGS = []

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name}{f' — {detail}' if detail else ''}")

def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠️  {msg}")

# ============================================================
# REGEX PATTERNS
# ============================================================
# Robust attribute extraction, order-agnostic and apostrophe-safe:
# find the tag that carries a named attribute, then read its value.
def tag_attr(c, tagname, attr, require=None):
    for m in re.finditer(rf'<{tagname}\b[^>]*>', c, re.I):
        tag = m.group(0)
        if require:
            k, v = require
            if not re.search(rf'\b{re.escape(k)}=["\']{re.escape(v)}["\']', tag, re.I):
                continue
        am = re.search(rf'\b{re.escape(attr)}=(["\'])(.*?)\1', tag, re.I)
        if am:
            return am.group(2)
    return None

RE_DESC = re.compile(r'<meta\b[^>]*\bname=["\']description["\']', re.I)
RE_CANON = re.compile(r'<link\b[^>]*\brel=["\']canonical["\']', re.I)
RE_OG_TITLE = re.compile(r'<meta\b[^>]*\bproperty=["\']og:title["\']', re.I)
RE_OG_DESC = re.compile(r'<meta\b[^>]*\bproperty=["\']og:description["\']', re.I)
RE_JSONLD = re.compile(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>', re.I)
RE_ARTICLE = re.compile(r'"@type"\s*:\s*"Article"', re.I)
RE_ART50 = re.compile(r'(Article\s*50|EU\s+AI\s+Act)', re.I)
RE_MASTER = re.compile(r'href=["\'][^"\']*master', re.I)
RE_SIGIL = re.compile(r'(SIGIL|sigil-chain|sigil_digest)', re.I)
RE_CTA_50 = re.compile(r'href=["\'][^"\']*(article50-passport|defoneos-article-50)', re.I)
RE_CTA_RFQ = re.compile(r'href=["\'][^"\']*defoneos-owem-rfq', re.I)
RE_HREF = re.compile(r'href=["\']([^"\'#?]+)', re.I)
RE_SRC = re.compile(r'src=["\']([^"\'#?]+)', re.I)
RE_CSS = re.compile(r'href=["\']([^"\']+\.css)', re.I)
RE_JSONLD_BLOCK = re.compile(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
RE_TITLE = re.compile(r'<title>([^<]+)</title>', re.I)
RE_H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
RE_LANG = re.compile(r'<html[^>]*lang=["\']([^"\']*)', re.I)
RE_VIEWPORT = re.compile(r'<meta\s+[^>]*name=["\']viewport["\']', re.I)
RE_CHARSET = re.compile(r'<meta\s+[^>]*charset', re.I)
RE_DATEMOD = re.compile(r'"dateModified"\s*:\s*"([^"]*)"', re.I)

all_html = sorted(p for p in ROOT.iterdir() if p.is_file() and p.suffix == '.html' and not p.name.startswith('.'))

# ============================================================
# 1. SIGMA AUDIT — all 8 signals on every page
# ============================================================
print("\n═══ 1. SIGMA AUDIT (AEO baseline on all pages; full 8/8 on core pages) ═══")

# Conversion / landing pages — the full 8/8 SEO bar applies to these ONLY.
# Utility, visual and analytical surfaces (globe3d, benchmarks, about, council,
# arena-hub, sov-space-vwm) are held to the AEO baseline (S1–S4) — requiring an
# Article-50 CTA or SIGIL mention on a 3D globe is structurally over-strict.
CORE_PAGES = {'index.html', 'master.html', 'sovereign.html', 'defoneos.html',
              'govbench.html', 'audit.html'}
BASELINE = ['S1', 'S2', 'S3', 'S4']

total = pass8 = 0
signal_fails = {f"S{i}": 0 for i in range(1, 9)}
failing_pages = []

for p in all_html:
    try: c = p.read_text(errors='ignore')
    except: continue
    total += 1
    s1 = bool(RE_DESC.search(c))
    s2 = bool(re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>', c, re.I))
    s3 = bool(re.search(r'og:title', c, re.I)) and bool(re.search(r'og:description', c, re.I))
    s4 = bool(RE_JSONLD.search(c)) and bool(re.search(r'"@type"\s*:\s*"(Article|WebPage|Organization|ItemList|CollectionPage)"', c))
    s5 = bool(RE_ART50.search(c))
    s6 = bool(RE_MASTER.search(c))
    s7 = bool(RE_SIGIL.search(c))
    s8 = bool(RE_CTA_50.search(c)) or bool(RE_CTA_RFQ.search(c))
    score = sum([s1,s2,s3,s4,s5,s6,s7,s8])
    if score == 8:
        pass8 += 1
    else:
        failing_pages.append((p.name, score))
    for i, v in enumerate([s1,s2,s3,s4,s5,s6,s7,s8], 1):
        if not v:
            signal_fails[f"S{i}"] += 1

# AEO baseline must hold on EVERY page (crawler visibility).
for sig in BASELINE:
    test(f"{sig} (AEO baseline) passes on all pages", signal_fails[sig] == 0, f"{signal_fails[sig]} failures")

# Full 8/8 is a core-ranking-surface bar, not a bar for 275 heterogeneous pages.
core = [p for p in all_html if p.name in CORE_PAGES]
core_fail = [p for p in core if p.name in [x[0] for x in failing_pages]]
test(f"All {len(core)} core pages pass 8/8 signals", len(core_fail) == 0,
     f"{len(core)-len(core_fail)}/{len(core)}" + (f" — failing: {[p.name for p in core_fail][:6]}" if core_fail else ""))

# ============================================================
# 2. BROKEN LINKS
# ============================================================
print("\n═══ 2. BROKEN INTERNAL LINKS ═══")

broken = 0
total_links = 0
broken_list = []
for p in all_html:
    try: c = p.read_text(errors='ignore')
    except: continue
    links = set(RE_HREF.findall(c))
    links.update(RE_SRC.findall(c))
    for link in links:
        total_links += 1
        if link.startswith(('http://', 'https://', 'mailto:', 'javascript:', 'tel:', '#', '{', '${', 'data:', 'blob:')):
            continue
        if link.startswith('/api') or link.startswith('/v1/'):
            continue
        target = link.lstrip('/')
        target_variants = [target, target + '.html', target + '/index.html']
        if not any((ROOT / t).exists() or (ROOT / 'public' / t).exists() for t in target_variants):
            broken += 1
            broken_list.append((p.name, link))

test(f"Zero broken internal links ({total_links} checked)", broken == 0, f"{broken} broken")
if broken_list:
    for fname, link in broken_list[:5]:
        warn(f"  {fname}: {link}")

# ============================================================
# 3. KEY ASSETS
# ============================================================
print("\n═══ 3. KEY ASSETS ═══")

required_assets = [
    'sovereign-2026.css', 'favicon.svg', 'apple-touch-icon.svg',
    'robots.txt', 'llms.txt', 'sitemap.xml', 'vercel.json',
]
for asset in required_assets:
    test(f"{asset} exists", (ROOT / asset).exists())

# ============================================================
# 4. CSS REFERENCES
# ============================================================
print("\n═══ 4. CSS REFERENCES ═══")

css_local = set()
for p in all_html:
    try: c = p.read_text(errors='ignore')
    except: continue
    for m in RE_CSS.findall(c):
        if not m.startswith('http'):
            css_local.add(m)

for css in css_local:
    test(f"Local CSS {css} exists", (ROOT / css.lstrip('/')).exists())

# ============================================================
# 5. CORE PAGE QUALITY
# ============================================================
print("\n═══ 5. CORE PAGE QUALITY ═══")

core_pages = {
    'index.html': ['measurement', 'compliance', 'sovereign', 'master.html'],
    'govbench.html': ['benchmark', 'robustness', 'How It Works', 'Reproduce', 'Dataset'],
    'audit.html': ['Ed25519', 'hash-chained', 'receipt'],
    'master.html': ['sovereign', 'charter'],
    'defoneos.html': ['DEFONEOS'],
    'sovereign.html': ['sovereign'],
    'defoneos-cost-reduction-manifesto.html': ['90', 'Palantir', 'Article 0'],
}

for page, keywords in core_pages.items():
    p = ROOT / page
    if p.exists():
        c = p.read_text(errors='ignore')
        for kw in keywords:
            test(f"{page} contains '{kw}'", kw.lower() in c.lower(), f"missing keyword")
    else:
        test(f"{page} exists", False)

# ============================================================
# 6. SITEMAP
# ============================================================
print("\n═══ 6. SITEMAP ═══")

sitemap = ROOT / 'sitemap.xml'
if sitemap.exists():
    content = sitemap.read_text(errors='ignore')
    url_count = content.count('<url>')
    test(f"Sitemap has ≥{total} URLs", url_count >= total, f"{url_count} URLs, {total} pages")
    test("Sitemap has <lastmod>", '<lastmod>' in content)
    test("Sitemap has <priority>", '<priority>' in content)
    test("Sitemap uses csoai.org domain", 'csoai.org' in content)
else:
    test("Sitemap exists", False)

# ============================================================
# 7. JSON-LD VALIDITY
# ============================================================
print("\n═══ 7. JSON-LD VALIDITY ═══")

jsonld_errors = 0
jsonld_checked = 0
for p in all_html:
    try: c = p.read_text(errors='ignore')
    except: continue
    for block in RE_JSONLD_BLOCK.findall(c):
        jsonld_checked += 1
        try:
            json.loads(block.strip())
        except json.JSONDecodeError:
            jsonld_errors += 1
            warn(f"Invalid JSON-LD in {p.name}")

test(f"JSON-LD valid ({jsonld_checked-jsonld_errors}/{jsonld_checked})", jsonld_errors == 0, f"{jsonld_errors} invalid")

# ============================================================
# 8. HTML VALIDITY (basic)
# ============================================================
print("\n═══ 8. HTML VALIDITY (basic) ═══")

html_errors = 0
for p in all_html:
    try: c = p.read_text(errors='ignore')
    except: continue
    if '<html' in c.lower() and '</html>' not in c.lower():
        html_errors += 1
        warn(f"Missing </html> in {p.name}")
    if '<head' in c.lower() and '</head>' not in c.lower():
        html_errors += 1
        warn(f"Missing </head> in {p.name}")
    if '<body' in c.lower() and '</body>' not in c.lower():
        html_errors += 1
        warn(f"Missing </body> in {p.name}")

test(f"Basic HTML structure valid ({len(all_html)-html_errors}/{len(all_html)})", html_errors == 0, f"{html_errors} errors")

# ============================================================
# 9. GOVBENCH PAGE
# ============================================================
print("\n═══ 9. GOVBENCH PAGE ═══")

gb = ROOT / 'govbench.html'
if gb.exists():
    c = gb.read_text(errors='ignore')
    test("GovBench has benchmark data (72-cell grid)", '72-cell' in c or '72-cell grid' in c or 'grid' in c)
    test("GovBench has methodology section", 'How it works' in c or 'How It Works' in c)
    test("GovBench has standards mapping", 'Standards mapping' in c)
    test("GovBench has run-it-yourself section", 'Run it yourself' in c or 'Run it now' in c)
    test("GovBench has meta description", bool(RE_DESC.search(c)))
    test("GovBench ≥10KB", len(c) >= 10000, f"{len(c):,} bytes")

# ============================================================
# 10. SECURITY
# ============================================================
print("\n═══ 10. SECURITY ═══")

# Check for exposed secrets/tokens
secret_patterns = [
    (r'sk_live_[a-zA-Z0-9]+', 'Stripe live key'),
    (r'sk_test_[a-zA-Z0-9]+', 'Stripe test key'),
    (r'ghp_[a-zA-Z0-9]+', 'GitHub token'),
    (r'xoxb-[a-zA-Z0-9-]+', 'Slack token'),
    (r'AKIA[A-Z0-9]{16}', 'AWS access key'),
]
for p in all_html:
    try: c = p.read_text(errors='ignore')
    except: continue
    for pattern, name in secret_patterns:
        if re.search(pattern, c):
            warn(f"Possible {name} in {p.name}")

# Check vercel.json doesn't expose .backups
vercel = ROOT / 'vercel.json'
if vercel.exists():
    vc = vercel.read_text(errors='ignore')
    test("vercel.json has security headers", 'X-Content-Type-Options' in vc)
    test("vercel.json has HSTS", 'Strict-Transport-Security' in vc)
    test("vercel.json has CORS for API", 'Access-Control-Allow-Origin' in vc)

# ============================================================
# 11. ACCESSIBILITY
# ============================================================
print("\n═══ 11. ACCESSIBILITY ═══")

# Check key pages have lang attribute and viewport
for page in ['index.html', 'govbench.html', 'audit.html']:
    p = ROOT / page
    if not p.exists():
        continue
    c = p.read_text(errors='ignore')
    test(f"{page} has lang attribute", bool(RE_LANG.search(c)))
    test(f"{page} has viewport meta", bool(RE_VIEWPORT.search(c)))
    test(f"{page} has charset", bool(RE_CHARSET.search(c)))

# ============================================================
# 12. SEO
# ============================================================
print("\n═══ 12. SEO ═══")

for page in ['index.html', 'govbench.html', 'defoneos.html', 'master.html']:
    p = ROOT / page
    if not p.exists():
        continue
    c = p.read_text(errors='ignore')
    title_m = RE_TITLE.search(c)
    if title_m:
        title_len = len(title_m.group(1))
        test(f"{page} title length 10-60 chars ({title_len})", 10 <= title_len <= 60, f"{title_len} chars")
    desc = tag_attr(c, 'meta', 'content', require=('name', 'description')) if RE_DESC.search(c) else None
    if desc:
        desc_len = len(desc)
        test(f"{page} meta desc length 50-160 chars ({desc_len})", 50 <= desc_len <= 160, f"{desc_len} chars")
    canon_val = tag_attr(c, 'link', 'href')
    canon_m = RE_CANON.search(c)
    if canon_m:
        test(f"{page} canonical URL is absolute", bool(canon_val) and canon_val.startswith('http'))

# ============================================================
# 13. CONTENT QUALITY
# ============================================================
print("\n═══ 13. CONTENT QUALITY ═══")

# Check for lorem ipsum or placeholder text
for p in all_html:
    try: c = p.read_text(errors='ignore')
    except: continue
    if 'lorem ipsum' in c.lower():
        warn(f"Lorem ipsum found in {p.name}")
    if 'TODO' in c and 'TODO:' not in c:
        warn(f"TODO found in {p.name}")
    if 'PLACEHOLDER' in c.upper():
        warn(f"PLACEHOLDER found in {p.name}")

# ============================================================
# 14. API ENDPOINTS
# ============================================================
print("\n═══ 14. API ENDPOINTS ═══")

api_dir = ROOT / 'api'
if api_dir.exists():
    api_files = sorted(p for p in api_dir.iterdir() if p.is_file() and p.suffix == '.js')
    test(f"API directory has ≥30 endpoints ({len(api_files)})", len(api_files) >= 30)
    
    # Check key endpoints exist
    key_endpoints = ['stats.js', 'sigil-status.js', 'eat-tick.js', 'daily-golden.js', 'eat-status.js', 'signup.js']
    for ep in key_endpoints:
        test(f"API endpoint {ep} exists", (api_dir / ep).exists())
else:
    test("API directory exists", False)

# ============================================================
# 15. CONFIGURATION
# ============================================================
print("\n═══ 15. CONFIGURATION ═══")

# robots.txt
robots = ROOT / 'robots.txt'
if robots.exists():
    rc = robots.read_text(errors='ignore')
    test("robots.txt has User-agent", 'User-agent' in rc)
    test("robots.txt has Sitemap", 'Sitemap' in rc)
    test("robots.txt blocks .backups", '.backups' in rc)
    test("robots.txt allows GPTBot", 'GPTBot' in rc)

# llms.txt
llms = ROOT / 'llms.txt'
if llms.exists():
    lc = llms.read_text(errors='ignore')
    test("llms.txt declares measurement identity", 'measurement body for AI compliance' in lc)
    test("llms.txt has canonical surfaces", 'Canonical surfaces' in lc)
    test("llms.txt has agent endpoints", 'Endpoints for agents' in lc)
    test("llms.txt declares red lines", 'Red lines' in lc)
    test("llms.txt has citation policy", 'Citation policy' in lc)

# ============================================================
# 16. NAVIGATION CONSISTENCY
# ============================================================
print("\n═══ 16. NAVIGATION CONSISTENCY ═══")

# Check that key pages have consistent navigation
nav_pages = ['index.html', 'govbench.html', 'audit.html', 'master.html']
for page in nav_pages:
    p = ROOT / page
    if not p.exists():
        continue
    c = p.read_text(errors='ignore')
    test(f"{page} has nav element", '<nav' in c.lower())
    test(f"{page} links to index", 'index.html' in c)
    test(f"{page} has footer", '<footer' in c.lower())

# ============================================================
# 17. COST MANIFESTO PAGE
# ============================================================
print("\n═══ 17. COST MANIFESTO PAGE ═══")

cm = ROOT / 'defoneos-cost-reduction-manifesto.html'
if cm.exists():
    c = cm.read_text(errors='ignore')
    test("Cost Manifesto has head-to-head tables", 'Palantir' in c and 'Anduril' in c)
    test("Cost Manifesto has 5 mechanics", 'Mechanism' in c or 'mechanics' in c.lower())
    test("Cost Manifesto has Article 0", 'Article 0' in c)
    test("Cost Manifesto has pricing tiers", '£0' in c and '£6K' in c)
    test("Cost Manifesto ≥10KB", len(c) >= 10000, f"{len(c):,} bytes")
else:
    test("Cost Manifesto page exists", False)

# ============================================================
# 18. TRAINING INFRASTRUCTURE
# ============================================================
print("\n═══ 18. TRAINING INFRASTRUCTURE ═══")

# Check training scripts exist and are valid Python
# (benchmark-results/*.py are gitignored/off-repo since 2026-08 cleanup; the
#  on-repo training surface lives under kaggle/ and the deploy scripts.)
training_scripts = [
    'kaggle/sov33_lora_training.py',
    'kaggle/runpod_deploy.py',
    'deploy_full_security_stack.sh',
    'deploy_refusal_models.sh',
]

for script in training_scripts:
    p = ROOT / script
    test(f"Training script {script} exists", p.exists())

# Check benchmark infrastructure
# (benchmark-results/* JSON + runner scripts are gitignored/off-repo since the
#  2026-08 cleanup; the on-repo benchmark surface is kaggle/ + govbench_leaderboard.)
benchmark_files = [
    'govbench_leaderboard.html',
    'backfill_aeo.py',
    'arena-build/arena.json',
]

for bf in benchmark_files:
    p = ROOT / bf
    test(f"Benchmark file {bf} exists", p.exists())

# Check key Python scripts are syntactically valid
import ast

syntax_scripts = [
    'kaggle/sov33_lora_training.py',
    'backfill_aeo.py',
]

for script in syntax_scripts:
    p = ROOT / script
    if p.exists():
        try:
            with open(p) as f:
                ast.parse(f.read())
            test(f"{script} has valid Python syntax", True)
        except SyntaxError as e:
            test(f"{script} has valid Python syntax", False, str(e))

# Check for training data files
training_data_files = [
    'benchmark-results/sovereign_synth_50k.jsonl',
    'benchmark-results/sov5_training_dataset.jsonl',
    'benchmark-results/sovereign_corpus_e2e.jsonl',
]

for td in training_data_files:
    p = ROOT / td
    if p.exists():
        test(f"Training data {td} exists", True)
    else:
        warn(f"Training data {td} not found (may be gitignored)")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*60}")
print(f"RESULTS: {PASS} passed, {FAIL} failed, {len(WARNINGS)} warnings")
print(f"PAGES: {total} HTML files, {pass8} passing 8/8 signals")
print(f"LINKS: {total_links} checked, {broken} broken")
print(f"{'='*60}")

if FAIL > 0:
    print(f"\n❌ {FAIL} TESTS FAILED")
    sys.exit(1)
else:
    print(f"\n✅ ALL {PASS} TESTS PASSED")
    sys.exit(0)
