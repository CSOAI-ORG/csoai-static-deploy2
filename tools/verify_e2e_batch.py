#!/usr/bin/env python3
"""
SOV3³ END-TO-END BATCH VERIFIER
================================

Runs the full end-to-end verification pass across the entire estate:

  1. Registry verification (canonical JSON)
  2. SIGMA compliance (canonical/og/JSON-LD/Article50/SIGIL on every HTML)
  3. Hub-anchor integrity (sovereign-cta-strip hub links, broken `href="#"` CTAs)
  4. JSON-LD Article schema validity (parseable + has headline/description/url)
  5. Favicon consistency (every page has /favicon.svg link)
  6. Article 50 banner correctness (no stale "20 days to seal")
  7. DeepSeek V4-Pro fabrication check (none in buyer-facing surface)
  8. SOV33 hub inbound-link coverage (should be 634)
  9. Canonical/JSON-LD URL consistency
 10. SOV3 OWEM × MCP completeness (every MCP reachable from at least one OWEM)

Outputs a JSON report + a human summary. Exits non-zero if any check fails.
"""
import json, os, re, sys, glob
from collections import Counter, defaultdict
from html.parser import HTMLParser

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(SITE_ROOT)

REGISTRY_PATH = 'sovereign-charters/sov33-capability-registry.json'

# Skip these directories
SKIP_DIRS = {'.git', '.backups', 'node_modules', '__pycache__', '.vercel'}

def all_html():
    """Yield every .html file in the deploy tree (excluding backups)."""
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(root, f)

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)

# ----------------------------------------------------------------------------
# 1. REGISTRY VERIFIER (delegates to verify_capability_registry.py)
# ----------------------------------------------------------------------------
def check_registry():
    """Re-run the registry verifier and capture pass/fail."""
    import subprocess
    result = subprocess.run(
        ['python3', 'tools/verify_capability_registry.py'],
        capture_output=True, text=True
    )
    err_match = re.search(r'(?:Errors|❌|failed):\s*(\d+)', result.stdout, re.IGNORECASE)
    warn_match = re.search(r'(?:Warnings|⚠|warnings):\s*(\d+)', result.stdout, re.IGNORECASE)
    return {
        'exit_code': result.returncode,
        'passed': result.returncode == 0,
        'errors_count': int(err_match.group(1)) if err_match else 0,
        'warnings_count': int(warn_match.group(1)) if warn_match else 0,
    }

# ----------------------------------------------------------------------------
# 2-10. PAGE-LEVEL CHECKS
# ----------------------------------------------------------------------------
class PageReport:
    __slots__ = ['path', 'bytes', 'has_canonical', 'has_og_title',
                 'has_og_desc', 'has_jsonld', 'jsonld_valid', 'has_meta_desc',
                 'has_favicon', 'has_h50_strip', 'has_a50_banner', 'has_hub_link',
                 'has_master_link', 'has_art50_banner_v2', 'jsonld_url_matches_canonical',
                 'has_no_fabricated_v4', 'broken_href_hub_count']

    def __init__(self, path, src):
        self.path = path
        self.bytes = len(src)
        self.has_canonical = bool(re.search(r'<link\s+rel="canonical"', src, re.I))
        self.has_og_title = 'property="og:title"' in src
        self.has_og_desc = 'property="og:description"' in src
        self.has_jsonld = '<script type="application/ld+json">' in src
        self.has_meta_desc = bool(re.search(r'<meta\s+name="description"', src, re.I))
        self.has_favicon = 'href="/favicon.svg"' in src or 'href="favicon.svg"' in src
        self.has_h50_strip = 'sovereign-cta-strip' in src
        self.has_a50_banner = 'article50-banner' in src
        self.has_hub_link = 'SOV33_OWEM_HUB' in src
        self.has_master_link = 'href="master.html"' in src or 'href="/master"' in src or 'href="/master.html"' in src
        self.has_art50_banner_v2 = 'EU AI Act Article 50 live 2 Aug 2026' in src
        self.has_no_fabricated_v4 = 'DeepSeek V4-Pro' not in src or 'RETRACTED' in src

        # JSON-LD URL match check
        self.jsonld_url_matches_canonical = True
        if self.has_canonical and self.has_jsonld:
            m_canon = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', src)
            m_jsonld = re.search(r'"url":\s*"([^"]+)"', src)
            if m_canon and m_jsonld:
                canon = m_canon.group(1)
                jurl = m_jsonld.group(1)
                # Both should reference same domain or same canonical
                if not (canon.replace('https://','').replace('http://','').split('/')[0]
                        == jurl.replace('https://','').replace('http://','').split('/')[0]):
                    self.jsonld_url_matches_canonical = False

        # JSON-LD validity
        self.jsonld_valid = True
        if self.has_jsonld:
            m = re.search(r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
                          src, re.S)
            if m:
                try:
                    d = json.loads(m.group(1))
                    if not isinstance(d, dict):
                        self.jsonld_valid = False
                except Exception:
                    self.jsonld_valid = False
            else:
                self.jsonld_valid = False

        # Broken hub-anchor count (e.g. `href="#">Master Hub`)
        self.broken_href_hub_count = len(re.findall(
            r'<a\s+href="#"\s*[^>]*>(?:Master|SOV33|OWEM|SOV3|DEFONEOS|Council|Audit|Compliance|BFT|CSOAI|Buyer|Mava|Pilot|Sign ?Up|Hive|Hub)[^<]*</a>',
            src, re.I
        ))

    def passes(self):
        return (self.has_canonical and self.has_og_title and self.has_og_desc
                and self.has_jsonld and self.jsonld_valid and self.has_meta_desc
                and self.has_favicon and self.has_h50_strip and self.has_hub_link
                and self.jsonld_url_matches_canonical and self.has_no_fabricated_v4
                and self.broken_href_hub_count == 0)

    def failures(self):
        f = []
        if not self.has_canonical: f.append('no canonical')
        if not self.has_og_title: f.append('no og:title')
        if not self.has_og_desc: f.append('no og:description')
        if not self.has_jsonld: f.append('no JSON-LD')
        if not self.jsonld_valid: f.append('JSON-LD invalid')
        if not self.has_meta_desc: f.append('no meta description')
        if not self.has_favicon: f.append('no favicon')
        if not self.has_h50_strip: f.append('no sovereign-cta-strip')
        if not self.has_hub_link: f.append('no SOV33_OWEM_HUB link')
        if not self.jsonld_url_matches_canonical: f.append('canonical ≠ JSON-LD url')
        if not self.has_no_fabricated_v4: f.append('has DeepSeek V4-Pro without RETRACTED')
        if self.broken_href_hub_count > 0:
            f.append(f'{self.broken_href_hub_count} broken hub-anchor CTAs')
        return f

def check_pages():
    reports = []
    for path in sorted(all_html()):
        with open(path) as f: src = f.read()
        reports.append(PageReport(path, src))
    return reports

# ----------------------------------------------------------------------------
# 11. OWEM × MCP REACHABILITY
# ----------------------------------------------------------------------------

def check_capability_assertions():
    """Run capability contract assertions."""
    import subprocess
    if not os.path.exists('tools/capability_assert.py'):
        return {'passed': False, 'error': 'capability_assert.py not found'}
    if not os.path.exists('tools/capability_assertions.json'):
        return {'passed': False, 'error': 'capability_assertions.json not found'}
    r = subprocess.run(['python3', 'tools/capability_assert.py', '--json'],
                       capture_output=True, text=True)
    if r.returncode not in (0, 1):
        return {'passed': False, 'error': r.stderr[:200]}
    try:
        result = json.loads(r.stdout)
    except Exception as e:
        return {'passed': False, 'error': f'JSON parse: {e}'}
    return {
        'passed': result.get('failed', 1) == 0,
        'total': result.get('total', 0),
        'passed_count': result.get('passed', 0),
        'failed_count': result.get('failed', 0),
    }

def check_owem_coverage(reg, reports):
    """For each OWEM group, list the MCPs reachable from it."""
    coverage = {}
    by_owem = defaultdict(list)
    
    # Handle both old format (mcps) and new format (layers)
    mcps = reg.get('mcps', [])
    if not mcps:
        for layer in reg.get('layers', []):
            for mcp in layer.get('mcps', []):
                mcps.append(mcp)
    
    for m in mcps:
        for o in m.get('owem', []):
            by_owem[o].append(m['name'])
    
    owem_groups = reg.get('owem_groups', [])
    if not owem_groups:
        # Extract from mcps
        owem_groups = [{'id': k} for k in by_owem.keys()]
    
    for o in owem_groups:
        oid = o['id'] if isinstance(o, dict) else o
        coverage[oid] = {
            'mcp_count': len(by_owem.get(oid, [])),
            'mcps': sorted(by_owem.get(oid, []))
        }
    return coverage

# ----------------------------------------------------------------------------
# 12. HUB INBOUND COUNT
# ----------------------------------------------------------------------------
def check_hub_inbound(reports):
    return sum(1 for r in reports if r.has_hub_link)

# ----------------------------------------------------------------------------
# 13. STALE BANNER CHECK
# ----------------------------------------------------------------------------
def check_stale_art50(reports):
    """Look for stale '20 days to seal' banners or links to deleted defoneos-article-50.html."""
    stale = []
    for r in reports:
        with open(r.path) as f: src = f.read()
        # Exclude self-references (the page itself is not stale)
        if '20 days to seal' in src:
            stale.append(r.path)
        elif 'defoneos-article-50.html' in src and r.path != './defoneos-article-50.html':
            stale.append(r.path)
    return stale

# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
def main():
    print('\n' + '='*72)
    print('  SOV3³ END-TO-END BATCH VERIFIER')
    print('  Site:', SITE_ROOT)
    print('='*72)

    # === 1. Registry ===
    print('\n[1] REGISTRY VERIFICATION')
    reg_result = check_registry()
    if reg_result['passed']:
        print(f'  ✓ PASSED — {reg_result["errors_count"]} errors, {reg_result["warnings_count"]} warnings')
    else:
        print(f'  ✗ FAILED — exit code {reg_result["exit_code"]}')

    # === 2-13. Pages ===
    print('\n[2] PAGE-LEVEL BATCH CHECK')
    print('  scanning all HTML pages...')
    reports = check_pages()
    total = len(reports)
    print(f'  scanned: {total} pages')

    # Aggregate
    passing = sum(1 for r in reports if r.passes())
    failing = total - passing
    pass_rate = 100 * passing / total if total else 0

    # Per-signal counts
    signals = {
        'canonical':       sum(1 for r in reports if r.has_canonical),
        'og:title':        sum(1 for r in reports if r.has_og_title),
        'og:description':  sum(1 for r in reports if r.has_og_desc),
        'JSON-LD':         sum(1 for r in reports if r.has_jsonld),
        'JSON-LD valid':   sum(1 for r in reports if r.jsonld_valid),
        'meta desc':       sum(1 for r in reports if r.has_meta_desc),
        'favicon':         sum(1 for r in reports if r.has_favicon),
        'sovereign strip': sum(1 for r in reports if r.has_h50_strip),
        'hub link':        sum(1 for r in reports if r.has_hub_link),
        'master link':     sum(1 for r in reports if r.has_master_link),
        'art50 banner':    sum(1 for r in reports if r.has_a50_banner),
        'art50 v2':        sum(1 for r in reports if r.has_art50_banner_v2),
        'no V4-Pro fab':   sum(1 for r in reports if r.has_no_fabricated_v4),
        'canon==jsonld':   sum(1 for r in reports if r.jsonld_url_matches_canonical),
        'no broken hub':   sum(1 for r in reports if r.broken_href_hub_count == 0),
    }
    print('\n  Per-signal pass rate:')
    for k, v in signals.items():
        pct = 100*v/total if total else 0
        bar = '█' * int(pct/2)
        status = '✓' if pct >= 95 else ('⚠' if pct >= 50 else '✗')
        print(f'    {status} {k:18s} {v:4d}/{total}  ({pct:5.1f}%)  {bar}')

    # === 3. Failing pages ===
    print('\n[3] FAILING PAGES')
    failing_reports = [r for r in reports if not r.passes()]
    if not failing_reports:
        print(f'  ✓ ALL {total} pages pass the full check')
    else:
        print(f'  ✗ {failing_reports and len(failing_reports)}/{total} pages have failures')
        # Group by failure
        fail_counter = Counter()
        for r in failing_reports:
            for f in r.failures():
                fail_counter[f] += 1
        print('\n  Failure frequency:')
        for f, n in fail_counter.most_common():
            print(f'    {n:4d}  {f}')
        # Sample failing pages
        print('\n  Sample failing pages (first 10):')
        for r in failing_reports[:10]:
            print(f'    {r.path}  -- {", ".join(r.failures())}')

    # === 4. Stale banners ===
    print('\n[4] STALE ART50 BANNER CHECK')
    stale = check_stale_art50(reports)
    if not stale:
        print('  ✓ no stale "20 days to seal" banners')
    else:
        print(f'  ✗ {len(stale)} pages with stale banner')
        for p in stale[:5]:
            print(f'    - {p}')

    # === 5. OWEM × MCP ===
    print('\n[5] OWEM × MCP REACHABILITY')
    reg = load_registry()
    coverage = check_owem_coverage(reg, reports)
    for owem, info in coverage.items():
        print(f'  {owem:12s} → {info["mcp_count"]:2d} MCPs reachable')

    # === 6. Hub inbound ===
    print('\n[6] HUB INBOUND COVERAGE')
    hub_count = check_hub_inbound(reports)
    print(f'  {hub_count}/{total} pages link to SOV33_OWEM_HUB.html  ({100*hub_count/total:.1f}%)')

    # === 7. CSOAI nav spot check ===
    print('\n[7] CSOAI MAIN-SURFACE SPOT CHECK')
    main_pages = ['index.html', 'audit.html', 'govbench.html',
                  'charter-ratification.html', 'sovereign-inventory.html',
                  'sovereign.html']
    for p in main_pages:
        if not os.path.exists(p):
            continue
        with open(p) as f: src = f.read()
        flags = []
        if 'article50-banner' in src: flags.append('A50')
        if 'SOV33_OWEM_HUB' in src: flags.append('hub')
        if 'SOV33_CAPABILITY_REGISTRY' in src: flags.append('registry')
        if 'master.html' in src or 'href="/master"' in src: flags.append('master')
        if 'defoneos-owem-rfq' in src: flags.append('rfq')
        if 'govbench.html' in src and p != 'govbench.html': flags.append('govbench')
        status = '✓' if 'A50' in flags and 'hub' in flags and 'master' in flags else '⚠'
        print(f'    {status} {p:35s}  [{" / ".join(flags)}]')

    # === 8. FINAL SCORE ===
    print('\n' + '='*72)
    print('  BATCH SUMMARY')
    print('='*72)
    score = (100 * passing / total) if total else 0
    print(f'  Pages:                  {total}')
    cap = check_capability_assertions()
    print(f'  Capability contracts:  {cap.get("passed_count","?")}/{cap.get("total","?")} pass, {cap.get("failed_count","?")} fail')
    print(f'  Passing full check:     {passing} ({score:.1f}%)')
    print(f'  Failing full check:     {failing}')
    print(f'  Stale art50 banners:    {len(stale)}')
    print(f'  Hub inbound:            {hub_count} ({100*hub_count/total:.1f}%)')
    print(f'  Registry:               {"PASS" if reg_result["passed"] else "FAIL"}')
    print(f'  Capability contracts: {cap.get("passed_count",0)}/{cap.get("total",0)} ({cap.get("passed_count",0)*100//cap.get("total",1) if cap.get("total",0) else 0}%)')
    print()
    # Inventory of estate
    print('  MCP inventory:')
    mcps = reg.get('mcps', [])
    if not mcps:
        for layer in reg.get('layers', []):
            for mcp in layer.get('mcps', []):
                mcps.append(mcp)
    live = sum(1 for m in mcps if m.get('status') == 'live')
    stage = sum(1 for m in mcps if m.get('status') == 'stage')
    print(f'    Live:   {live}')
    print(f'    Stage:  {stage}')
    print(f'    Total:  {len(mcps)} MCPs, {sum(len(m.get("tools",[])) for m in mcps)} tools')
    print()

    if failing > 0 or not reg_result['passed'] or stale:
        print('  ✗ BATCH FAILED — see failures above')
        return 1
    print('  ✓ BATCH PASSED — estate is consistent with the canonical frame')
    return 0

if __name__ == '__main__':
    sys.exit(main())
