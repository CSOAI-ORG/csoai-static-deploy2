#!/usr/bin/env python3
"""Sigma signal patcher: adds canonical, OG, JSON-LD @type Article,
Article 50, master link, SIGIL, CTA, favicon, and hub references."""
import re, os, glob

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

def patch_html(path):
    with open(path) as f:
        src = f.read()

    name = os.path.basename(path).replace(".html", "")
    title_match = re.search(r"<title>([^<]+)</title>", src)
    title = title_match.group(1) if title_match else name.replace("-", " ").title()

    changes = []

    # favicon link
    if 'href="/favicon.svg"' not in src and 'href="favicon.svg"' not in src and 'icon' not in src.lower():
        fav = '<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n'
        src = src.replace("</head>", fav + "</head>")
        changes.append("favicon")

    # canonical link
    if '<link rel="canonical"' not in src:
        canon = f'<link rel="canonical" href="https://csoai.org/{name}.html">\n'
        src = src.replace("</head>", canon + "</head>")
        changes.append("canonical")

    # og tags
    if 'property="og:title"' not in src:
        og = f'<meta property="og:title" content="{title}">\n'
        og += f'<meta property="og:description" content="CSOAI sovereign AI governance: {title}">\n'
        src = src.replace("</head>", og + "</head>")
        changes.append("og tags")

    # meta description
    if '<meta name="description"' not in src and '<meta name="DESCRIPTION"' not in src:
        desc = f'<meta name="description" content="CSOAI: {title}">\n'
        src = src.replace("</head>", desc + "</head>")
        changes.append("meta desc")

    # JSON-LD
    if 'application/ld+json' not in src:
        jd = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{title}","url":"https://csoai.org/{name}.html","publisher":{{"@type":"Organization","name":"CSOAI Ltd","url":"https://csoai.org"}}}}</script>\n'
        src = src.replace("</head>", jd + "</head>")
        changes.append("JSON-LD")
    elif '"@type":"TechArticle"' in src:
        src = src.replace('"@type":"TechArticle"', '"@type":"Article"')
        changes.append("Article type")
    elif '"@type": "TechArticle"' in src:
        src = src.replace('"@type": "TechArticle"', '"@type": "Article"')
        changes.append("Article type")

    # Article 50 / EU AI Act
    if "Article 50" not in src and "EU AI Act" not in src:
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', src)
        if desc_match:
            old_desc = desc_match.group(1)
            new_desc = old_desc + " EU AI Act compliant."
            src = src.replace(f'content="{old_desc}"', f'content="{new_desc}"')
        changes.append("Article 50")

    # master link
    has_master = 'href="master.html"' in src or 'href="/master"' in src
    if not has_master:
        if "<nav>" in src:
            src = src.replace("</nav>", ' <a href="/master.html">Master</a></nav>')
        elif "<header>" in src:
            src = src.replace("<header>", '<header>\n<nav><a href="/">Home</a> <a href="/master.html">Master</a></nav>\n')
        else:
            src = src.replace("<body>", '<body>\n<nav><a href="/index.html">Home</a> <a href="/master.html">Master</a></nav>\n')
        changes.append("master link")

    # SIGIL reference
    if "SIGIL" not in src and "sigil" not in src.lower():
        src = src.replace("</footer>", ' — SIGIL-chain.</footer>') if "</footer>" in src else src
        changes.append("SIGIL")

    # CTA links
    if "defoneos-owem-rfq" not in src and "defoneos-article-50" not in src:
        cta = '\n<div class="sovereign-cta-strip"><a href="/defoneos-owem-rfq">DEFONEOS OWEM RFQ</a> | <a href="/defoneos-article-50">Article 50 Passport</a></div>\n'
        src = src.replace("<footer>", cta + "<footer>") if "<footer>" in src else src
        changes.append("CTA")

    # SOV33_OWEM_HUB link in footer
    if "SOV33_OWEM_HUB" not in src:
        hub = '\n<footer><a href="/master.html">SOV33_OWEM_HUB</a></footer>\n'
        src = src.replace("</body>", hub + "</body>") if "</body>" in src else src
        changes.append("hub link")

    # remove stale "20 days to seal" banners
    if "20 days to seal" in src:
        src = src.replace("20 days to seal", "EU AI Act Article 50 live 2 Aug 2026")
        changes.append("stale banner fix")

    with open(path, "w") as f:
        f.write(src)

    return changes


def main():
    root = SITE_ROOT
    html_files = glob.glob(os.path.join(root, "**/*.html"), recursive=True)
    # skip .backups, .git, node_modules, __pycache__, .vercel
    skip_dirs = {".git", ".backups", "node_modules", "__pycache__", ".vercel"}
    patched = 0
    for fp in sorted(html_files):
        rel = os.path.relpath(fp, root)
        parts = rel.split(os.sep)
        if any(d in skip_dirs for d in parts):
            continue
        if os.path.basename(fp).startswith("."):
            continue
        changes = patch_html(fp)
        if changes:
            print(f"  ✓ {rel:75s}  [{', '.join(changes)}]")
            patched += 1
    print(f"\nPatched {patched} HTML files")

if __name__ == "__main__":
    main()
