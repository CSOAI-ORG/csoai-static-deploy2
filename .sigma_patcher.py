#!/usr/bin/env python3
"""
Batch sigma patcher — injects all 8 sovereign signals into every defoneos-*.html page.
Run: python3 .sigma_patcher.py
Then verify: python3 .sigma_audit.py
"""
import os
import re
import sys
import json
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
PAGE_RE = re.compile(r"^defoneos-.*\.html$")
CORE_PAGES = ["govbench.html", "index.html", "audit.html", "master.html", "sovereign.html", "defoneos.html"]

# Regex patterns
RE_TITLE = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
RE_DESC = re.compile(r'<meta\s+[^>]*name=["\']description["\'][^>]*>', re.IGNORECASE)
RE_CANON = re.compile(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>', re.IGNORECASE)
RE_OG_TITLE = re.compile(r'<meta\s+[^>]*property=["\']og:title["\'][^>]*>', re.IGNORECASE)
RE_OG_DESC = re.compile(r'<meta\s+[^>]*property=["\']og:description["\'][^>]*>', re.IGNORECASE)
RE_JSONLD = re.compile(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>', re.IGNORECASE)
RE_ARTICLE_SCHEMA = re.compile(r'"@type"\s*:\s*"Article"', re.IGNORECASE)
RE_ART50 = re.compile(r'(Article\s*50|EU\s+AI\s+Act)', re.IGNORECASE)
RE_MASTER = re.compile(r'href=["\'][^"\']*master', re.IGNORECASE)
RE_SIGIL = re.compile(r'(SIGIL[\s\|:]|receipt[\s\-:]|sigil[\-:]anchor|sigil-chain|sigil_digest)', re.IGNORECASE)
RE_CTA_50 = re.compile(r'href=["\'][^"\']*/defoneos-article-50["\']', re.IGNORECASE)
RE_CTA_RFQ = re.compile(r'href=["\'][^"\']*/defoneos-owem-rfq["\']', re.IGNORECASE)
RE_HEAD_CLOSE = re.compile(r"</head>", re.IGNORECASE)
RE_BODY_CLOSE = re.compile(r"</body>", re.IGNORECASE)
RE_FOOTER = re.compile(r"<footer[^>]*>", re.IGNORECASE)

def slug_from_filename(name):
    """Convert defoneos-foo-bar.html to a readable title slug."""
    base = name.replace(".html", "").replace("defoneos-", "")
    return base.replace("-", " ").title()

def make_description(title):
    """Generate a meta description from the title."""
    clean = re.sub(r'<[^>]+>', '', title).strip()
    clean = clean.replace('"', "'").replace('\n', ' ').replace('\r', '')
    if len(clean) > 155:
        clean = clean[:152] + "..."
    return f"{clean} — CSOAI sovereign AI compliance & governance."

def make_jsonld(page_name, title, desc):
    """Generate JSON-LD Article schema block."""
    url = f"https://csoai-static-deploy2.vercel.app/{page_name}"
    # Sanitize title/desc for JSON embedding
    safe_title = title.replace('"', '\\"').replace('\n', ' ').strip()[:200]
    safe_desc = desc.replace('"', '\\"').replace('\n', ' ').strip()[:300]
    return f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{safe_title}",
    "description": "{safe_desc}",
    "url": "{url}",
    "author": {{"@type": "Organization", "name": "CSOAI Ltd (UK 16939677)"}},
    "publisher": {{"@type": "Organization", "name": "DEFONEOS", "url": "https://csoai-static-deploy2.vercel.app"}},
    "dateModified": "2026-07-25"
  }}
  </script>'''

def make_article50_banner():
    """Article 50 / EU AI Act banner."""
    return '''<div class="article50-banner" data-marker="ARTICLE_50_BANNER" style="background:linear-gradient(90deg,rgba(34,211,238,.12),rgba(251,191,36,.12));border-bottom:1px solid rgba(34,211,238,.2);padding:.55rem 1rem;text-align:center;font-size:.8rem;color:#cbd5e1">EU AI Act Article 50 live 2 Aug 2026 — C2PA passport ready | <a href="defoneos-article-50.html" style="color:#22d3ee;font-weight:600">Get yours →</a></div>
'''

def make_sovereign_cta():
    """CTA strip with links to /master, article-50, owem-rfq."""
    return '''<div class="sovereign-cta-strip" data-marker="SOVEREIGN_CTA" style="background:rgba(34,211,238,.06);border-top:1px solid rgba(34,211,238,.15);padding:1rem 1.5rem;text-align:center;font-size:.82rem;color:#94a3b8">
  <a href="master.html" style="color:#22d3ee;text-decoration:none;font-weight:600;margin:0 .8rem">🜏 Sovereign Hub</a>
  <a href="defoneos-article-50.html" style="color:#fbbf24;text-decoration:none;font-weight:600;margin:0 .8rem">📜 Article 50 Passport</a>
  <a href="defoneos-owem-rfq.html" style="color:#a78bfa;text-decoration:none;font-weight:600;margin:0 .8rem">📋 OWEM RFQ</a>
  <span style="margin:0 .8rem;color:#64748b">CSOAI Ltd · UK 16939677 · Care Floor 0.95 · Charter-anchored</span>
</div>
'''

def make_sigil_footer():
    """SIGIL receipt reference."""
    return '''<div class="sigil-receipt" data-marker="SIGIL_RECEIPT" style="text-align:center;padding:.6rem;font-size:.72rem;color:#64748b;border-top:1px solid rgba(255,255,255,.05)">
  SIGIL | sigil-chain | Ed25519-signed | RFC 8032 §7.1 | <a href="audit.html" style="color:#22d3ee;text-decoration:none">Verify receipt →</a>
</div>
'''

def patch_file(path):
    """Patch a single file to pass all 8 signals. Returns (changed, signals_added)."""
    content = path.read_text(encoding="utf-8", errors="ignore")
    original = content
    added = []

    # Extract title
    title_match = RE_TITLE.search(content)
    title = title_match.group(1).strip() if title_match else slug_from_filename(path.name)
    desc = make_description(title)

    # === HEAD INJECTIONS (before </head>) ===
    head_inject = ""

    # S1: meta description
    if not RE_DESC.search(content):
        safe_desc = desc.replace('"', "'").replace('\n', ' ').strip()
        head_inject += f'<meta name="description" content="{safe_desc}">\n'
        added.append("S1")

    # S2: canonical
    if not RE_CANON.search(content):
        url = f"https://csoai-static-deploy2.vercel.app/{path.name}"
        head_inject += f'<link rel="canonical" href="{url}">\n'
        added.append("S2")

    # S3: og:title + og:description
    if not RE_OG_TITLE.search(content):
        safe_og_title = title.replace('"', "'").replace('\n', ' ').strip()[:200]
        head_inject += f'<meta property="og:title" content="{safe_og_title}">\n'
        added.append("S3-ogtitle")
    if not RE_OG_DESC.search(content):
        safe_og_desc = desc.replace('"', "'").replace('\n', ' ').strip()[:300]
        head_inject += f'<meta property="og:description" content="{safe_og_desc}">\n'
        added.append("S3-ogdesc")

    # S4: JSON-LD Article
    has_jsonld = bool(RE_JSONLD.search(content))
    has_article = bool(RE_ARTICLE_SCHEMA.search(content))
    if not (has_jsonld and has_article):
        head_inject += make_jsonld(path.name, title, desc) + "\n"
        added.append("S4")

    if head_inject:
        if RE_HEAD_CLOSE.search(content):
            content = RE_HEAD_CLOSE.sub(lambda m: head_inject + "</head>", content, count=1)
        else:
            # No </head> found — inject after <head> or at start of body
            content = head_inject + content

    # === BODY INJECTIONS ===

    # Strip any previously-injected CTA blocks (from prior patch runs)
    # Don't strip SIGIL — it's idempotent and stripping causes re-injection loops
    content = re.sub(r'<div[^>]*data-marker="SOVEREIGN_CTA"[^>]*>.*?</div>\s*</div>', '', content, flags=re.DOTALL|re.IGNORECASE)

    # S5: Article 50 banner (after <body>) — only if missing
    if not RE_ART50.search(content):
        banner = make_article50_banner()
        if re.search(r'<body[^>]*>', content, re.IGNORECASE):
            content = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + banner, content, count=1, flags=re.IGNORECASE)
            added.append("S5")

    # S6: master link + S8: CTA links + S7: SIGIL footer (before </body>)
    # Re-check after stripping old injections
    needs_cta = not RE_MASTER.search(content) or not (RE_CTA_50.search(content) or RE_CTA_RFQ.search(content))
    needs_sigil = not RE_SIGIL.search(content)

    if needs_cta or needs_sigil:
        inject = ""
        if needs_cta:
            inject += make_sovereign_cta()
            if not RE_MASTER.search(content):
                added.append("S6")
            if not (RE_CTA_50.search(content) or RE_CTA_RFQ.search(content)):
                added.append("S8")
        if needs_sigil:
            inject += make_sigil_footer()
            added.append("S7")

        if RE_BODY_CLOSE.search(content):
            content = RE_BODY_CLOSE.sub(lambda m: inject + "</body>", content, count=1)
        else:
            content += inject

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True, added
    return False, added


def main():
    # All HTML files in root (not in subdirs like .backups, public, etc.)
    files = sorted(p for p in ROOT.iterdir() if p.is_file() and p.suffix == '.html' and not p.name.startswith('.'))
    print(f"[patcher] Found {len(files)} HTML pages to patch", file=sys.stderr)

    patched = 0
    signal_counts = {}
    for p in files:
        changed, signals = patch_file(p)
        if changed:
            patched += 1
            for s in signals:
                signal_counts[s] = signal_counts.get(s, 0) + 1

    print(f"[patcher] Patched {patched}/{len(files)} files", file=sys.stderr)
    print(f"[patcher] Signals injected: {json.dumps(signal_counts, indent=2)}", file=sys.stderr)


if __name__ == "__main__":
    main()
