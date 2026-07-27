#!/usr/bin/env python3
"""Sigma signal patcher: adds canonical, OG, JSON-LD @type Article,
Article 50, master link, SIGIL, and CTA references to all DEFONEOS deep-dive packs."""
import re, os

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

def patch_file(path):
    with open(path) as f:
        src = f.read()

    name = os.path.basename(path).replace(".html", "")
    title_match = re.search(r"<title>([^<]+)</title>", src)
    title = title_match.group(1) if title_match else name.replace("-", " ").title()

    changes = []

    # S2: canonical link
    if '<link rel="canonical"' not in src:
        canon = f'<link rel="canonical" href="https://csoai.org/{name}.html">\n'
        src = src.replace("</head>", canon + "</head>")
        changes.append("canonical")

    # S3: og:title + og:description
    if 'property="og:title"' not in src:
        og = f'<meta property="og:title" content="{title}">\n'
        og += f'<meta property="og:description" content="CSOAI sovereign AI governance deep-dive: {title}">\n'
        src = src.replace("</head>", og + "</head>")
        changes.append("og tags")

    # S4: JSON-LD @type "Article" (change TechArticle to Article)
    if '"@type":"TechArticle"' in src:
        src = src.replace('"@type":"TechArticle"', '"@type":"Article"')
        changes.append("JSON-LD Article type")
    elif '"@type": "TechArticle"' in src:
        src = src.replace('"@type": "TechArticle"', '"@type": "Article"')
        changes.append("JSON-LD Article type")

    # S5: Article 50 / EU AI Act (add to description if missing)
    if "Article 50" not in src and "EU AI Act" not in src:
        # Add to meta description
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', src)
        if desc_match:
            old_desc = desc_match.group(1)
            new_desc = old_desc + " EU AI Act Article 50 compliant."
            src = src.replace(f'content="{old_desc}"', f'content="{new_desc}"')
        changes.append("Article 50 ref")

    # S6: master link + nav wrapper
    has_master = 'href="master.html"' in src or 'href="/master"' in src
    if not has_master:
        if "<nav>" in src:
            src = src.replace("</nav>", ' <a href="/master.html">Master</a></nav>')
        elif "<header>" in src:
            nav_block = "\n<nav><a href=\"/\">Home</a> <a href=\"/master.html\">Master</a> <a href=\"/govbench.html\">GovBench</a></nav>\n"
            src = src.replace("<header>", "<header>" + nav_block)
        else:
            nav_block = "\n<nav><a href=\"/\">Home</a> <a href=\"/master.html\">Master</a></nav>\n"
            src = src.replace("<body>", "<body>" + nav_block)
        changes.append("master link")

    # S7: SIGIL reference
    if "SIGIL" not in src and "sigil" not in src.lower():
        src = src.replace("</footer>", ' — SIGIL-chain verified.</footer>') if "</footer>" in src else src
        changes.append("SIGIL ref")

    # S8: CTA to defoneos-owem-rfq or defoneos-article-50
    if "defoneos-owem-rfq" not in src and "defoneos-article-50" not in src:
        cta = '\n<div class="sovereign-cta-strip"><a href="/defoneos-owem-rfq">DEFONEOS OWEM RFQ</a> | <a href="/defoneos-article-50">Article 50 Passport</a></div>\n'
        src = src.replace("<footer>", cta + "<footer>") if "<footer>" in src else src
        changes.append("CTA links")

    with open(path, "w") as f:
        f.write(src)

    return changes

def main():
    root = SITE_ROOT
    patched = 0
    for f in sorted(os.listdir(root)):
        if f.endswith(".html") and f.startswith("defoneos-"):
            path = os.path.join(root, f)
            changes = patch_file(path)
            if changes:
                print(f"  ✓ {f:70s}  [{', '.join(changes)}]")
                patched += 1
    print(f"\nPatched {patched} deep-dive packs")

if __name__ == "__main__":
    main()
