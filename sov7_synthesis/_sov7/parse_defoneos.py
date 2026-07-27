#!/usr/bin/env python3
"""
DEFONEOS HTML Governance Parser
================================
Parses all DEFONEOS HTML deep-dive packs and extracts structured
company/system/compliance data for the compliance engine.

Extracts per file:
  - Department name, code, sector
  - AI systems / entry points (12 per pack)
  - Transformation priorities (8 per pack)
  - MCP servers (6 per pack)
  - Red lines (ethical boundaries)
  - Engagement model (5-step)
  - Buyer-type matrix
  - Compliance frameworks referenced
  - Risk classification (derived from red lines + sector)

Output: defoneos_parsed.json — structured data for compliance engine ingestion.
"""

import os
import re
import json
import glob
from html.parser import HTMLParser
from pathlib import Path

# --- Minimal HTML text extractor (no bs4 dependency) ---

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self._text.append(data)

    def get_text(self):
        return ' '.join(self._text)


def html_to_text(html_str):
    extractor = HTMLTextExtractor()
    extractor.feed(html_str)
    return extractor.get_text()


# --- Department code mapping ---

DEPT_MAP = {
    'dhsc':  {'name': 'Department of Health and Social Care', 'code': 'DHSC', 'sector': 'Health'},
    'mod':   {'name': 'Ministry of Defence', 'code': 'MOD', 'sector': 'Defence'},
    'hmrc':  {'name': 'HM Revenue and Customs', 'code': 'HMRC', 'sector': 'Revenue'},
    'dfe':   {'name': 'Department for Education', 'code': 'DfE', 'sector': 'Education'},
    'fcdo':  {'name': 'Foreign, Commonwealth and Development Office', 'code': 'FCDO', 'sector': 'Foreign Affairs'},
    'dwp':   {'name': 'Department for Work and Pensions', 'code': 'DWP', 'sector': 'Social Security'},
    'home-office': {'name': 'Home Office', 'code': 'HO', 'sector': 'Home Affairs'},
    'desnz': {'name': 'Department for Energy Security and Net Zero', 'code': 'DESNZ', 'sector': 'Energy'},
    'defra': {'name': 'Department for Environment, Food and Rural Affairs', 'code': 'DEFRA', 'sector': 'Environment'},
    'dsit':  {'name': 'Department for Science, Innovation and Technology', 'code': 'DSIT', 'sector': 'Technology'},
    'moj':   {'name': 'Ministry of Justice', 'code': 'MOJ', 'sector': 'Justice'},
}

# --- Compliance framework detection ---

COMPLIANCE_KEYWORDS = {
    'EU AI Act': ['eu ai act', 'article 50', 'article 5', 'annex'],
    'UK GDPR': ['uk gdpr', 'gdpr', 'data protection'],
    'DCB0129/DCB0160': ['dcb0129', 'dcb0160', 'clinical safety'],
    'NICE': ['nice evidence', 'nice '],
    'MHRA': ['mhra', 'ukca marking'],
    'AUKUS': ['aukus'],
    'ITAR/EAR': ['itar', 'ear compliance'],
    'Equality Act 2010': ['equality act'],
    'KCSIE': ['kcsie', 'keeping children safe'],
    'Prevent Duty': ['prevent duty', 'channel referral'],
    'NATO STANAG': ['stanag', 'nato'],
    'OECD BEPS': ['oecd beps', 'pillar two'],
    'Caldecott': ['caldicott'],
    'DNSR': ['dnsr', 'defence nuclear safety'],
    'NIST PQC': ['nist pqc', 'post-quantum'],
    'HRA': ['hra approval', 'health research authority'],
    'Ofsted': ['ofsted'],
    'DSPT': ['dspt', 'data security and protection'],
    'Working Together': ['working together'],
    'CQC': ['cqc'],
    'NAO': ['nao', 'national audit'],
}


def detect_compliance_frameworks(text):
    text_lower = text.lower()
    found = []
    for framework, keywords in COMPLIANCE_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(framework)
                break
    return sorted(set(found))


def classify_risk(sector, red_lines, entry_points_text):
    """Derive risk level from sector + red lines + content."""
    high_risk_sectors = {'Defence', 'Home Affairs', 'Justice', 'Health'}
    critical_keywords = ['nuclear', 'warhead', 'deterrent', 'asylum', 'border',
                         'safeguarding', 'children', 'clinical safety', 'fraud detection',
                         'criminal', 'surveillance', 'intelligence sharing']

    combined = (sector + ' ' + ' '.join(red_lines) + ' ' + entry_points_text).lower()

    if sector in high_risk_sectors:
        severity = 'HIGH'
    else:
        severity = 'MEDIUM'

    # Escalate to CRITICAL if critical keywords present
    critical_hits = [kw for kw in critical_keywords if kw in combined]
    if len(critical_hits) >= 3:
        severity = 'CRITICAL'

    return {
        'level': severity,
        'sector_risk': sector in high_risk_sectors,
        'critical_signals': critical_hits[:10],
    }


def extract_cards(section_html):
    """Extract card data from a grid section."""
    cards = []
    # Pattern: <div class="card"><span class="tag">TAG</span><h3>TITLE</h3><p>DESCRIPTION</p></div>
    card_pattern = re.compile(
        r'<div class="card">(.*?)</div>\s*</div>',
        re.DOTALL
    )
    # Simpler: match each card individually
    card_blocks = re.findall(
        r'<div class="card">(.*?)</div>',
        section_html,
        re.DOTALL
    )
    for block in card_blocks:
        tag_match = re.search(r'<span class="tag">(.*?)</span>', block, re.DOTALL)
        h3_match = re.search(r'<h3>(.*?)</h3>', block, re.DOTALL)
        p_match = re.search(r'<p>(.*?)</p>', block, re.DOTALL)
        tag = html_to_text(tag_match.group(1)).strip() if tag_match else ''
        title = html_to_text(h3_match.group(1)).strip() if h3_match else ''
        desc = html_to_text(p_match.group(1)).strip() if p_match else ''
        cards.append({'tag': tag, 'title': title, 'description': desc})
    return cards


def extract_red_lines(html):
    """Extract red line items."""
    redline_section = re.search(
        r'<div class="redline">(.*?)</div>\s*<div class="engagement">',
        html, re.DOTALL
    )
    if not redline_section:
        return []
    items = re.findall(r'<li>(.*?)</li>', redline_section.group(1), re.DOTALL)
    return [html_to_text(item).strip().lstrip('❌').strip() for item in items]


def extract_engagement_steps(html):
    """Extract 5-step engagement model."""
    engagement_section = re.search(
        r'<div class="engagement">(.*?)</div>\s*(?:<h2|<div class="sovereign|$)',
        html, re.DOTALL
    )
    if not engagement_section:
        return []
    steps = re.findall(
        r'<strong>(.*?)</strong>:\s*(.*?)</div>',
        engagement_section.group(1),
        re.DOTALL
    )
    return [{'step': s[0].strip(), 'description': html_to_text(s[1]).strip()} for s in steps]


def extract_stats(html):
    """Extract the 4 stat numbers from header."""
    stats = re.findall(r'<div class="num">(\d+)</div><div class="label">(.*?)</div>', html)
    return {label.strip(): int(num) for num, label in stats}


def extract_subtitle(html):
    """Extract the subtitle paragraph."""
    match = re.search(r'<p class="sub">(.*?)</p>', html, re.DOTALL)
    return html_to_text(match.group(1)).strip() if match else ''


def extract_title(html):
    """Extract h1 title."""
    match = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    return html_to_text(match.group(1)).strip() if match else ''


def extract_pill(html):
    """Extract pill badge text."""
    match = re.search(r'<div class="pill">(.*?)</div>', html, re.DOTALL)
    return html_to_text(match.group(1)).strip() if match else ''


def detect_dept_code(filename):
    """Detect department code from filename."""
    basename = os.path.basename(filename).replace('defoneos-', '').replace('.html', '')
    for code in DEPT_MAP:
        if basename.startswith(code):
            return code
    return None


def parse_single_file(filepath):
    """Parse one DEFONEOS HTML file into structured data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    filename = os.path.basename(filepath)
    full_text = html_to_text(html)

    # Detect if this is a deep-dive pack
    is_deep_dive = 'Entry Points' in html and 'Transformation Priorities' in html

    if not is_deep_dive:
        # Non-standard file (article-50, cost-reduction-manifesto, owem-rfq)
        title = extract_title(html)
        return {
            'filename': filename,
            'type': 'reference',
            'title': title,
            'compliance_frameworks': detect_compliance_frameworks(full_text),
            'full_text_length': len(full_text),
        }

    # --- Deep-dive pack parsing ---
    dept_code = detect_dept_code(filepath)
    dept_info = DEPT_MAP.get(dept_code, {'name': 'Unknown', 'code': 'UNK', 'sector': 'Unknown'})

    pill = extract_pill(html)
    title = extract_title(html)
    subtitle = extract_subtitle(html)
    stats = extract_stats(html)

    # Split HTML into sections by h2
    sections = re.split(r'<h2>', html)

    entry_points = []
    transformation_priorities = []
    mcp_servers = []
    buyer_matrix = []

    for section in sections:
        section_text = html_to_text(section)

        if 'Entry Points' in section_text[:50]:
            entry_points = extract_cards(section)
        elif 'Transformation Priorities' in section_text[:80]:
            transformation_priorities = extract_cards(section)
        elif 'MCP Servers' in section_text[:50]:
            mcp_servers = extract_cards(section)
        elif 'Buyer-Type Matrix' in section_text[:50]:
            buyer_matrix = extract_cards(section)

    red_lines = extract_red_lines(html)
    engagement = extract_engagement_steps(html)
    compliance = detect_compliance_frameworks(full_text)

    entry_text = ' '.join([ep['title'] + ' ' + ep['description'] for ep in entry_points])
    risk = classify_risk(dept_info['sector'], red_lines, entry_text)

    # Extract AI system names from entry points
    ai_systems = [{'name': ep['title'], 'category': ep['tag'], 'description': ep['description']}
                  for ep in entry_points]

    # Extract MCP server names
    mcp_list = [{'name': m['title'], 'category': m['tag'], 'description': m['description']}
                for m in mcp_servers]

    return {
        'filename': filename,
        'type': 'deep_dive_pack',
        'department': {
            'name': dept_info['name'],
            'code': dept_info['code'],
            'sector': dept_info['sector'],
            'pill': pill,
        },
        'title': title,
        'subtitle': subtitle,
        'stats': stats,
        'ai_systems': ai_systems,
        'transformation_priorities': [
            {'number': i+1, 'name': tp['title'], 'description': tp['description']}
            for i, tp in enumerate(transformation_priorities)
        ],
        'mcp_servers': mcp_list,
        'red_lines': red_lines,
        'engagement_model': engagement,
        'buyer_matrix': [
            {'category': bm['tag'], 'organisation': bm['title'], 'description': bm['description']}
            for bm in buyer_matrix
        ],
        'compliance_frameworks': compliance,
        'risk_assessment': risk,
    }


def main():
    base_dir = '/Users/nicholas/clawd/csoai-static-deploy2'
    output_dir = os.path.join(base_dir, 'sov7_synthesis')

    # Find all defoneos HTML files
    pattern = os.path.join(base_dir, 'defoneos-*.html')
    files = sorted(glob.glob(pattern))

    print(f"Found {len(files)} DEFONEOS HTML files")
    print("=" * 60)

    results = []
    dept_summary = {}
    all_ai_systems = []
    all_mcps = []
    all_compliance = set()
    risk_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0}

    for filepath in files:
        try:
            data = parse_single_file(filepath)
            results.append(data)

            if data['type'] == 'deep_dive_pack':
                dept = data['department']['code']
                dept_summary[dept] = {
                    'name': data['department']['name'],
                    'sector': data['department']['sector'],
                    'ai_system_count': len(data['ai_systems']),
                    'mcp_count': len(data['mcp_servers']),
                    'red_line_count': len(data['red_lines']),
                    'risk_level': data['risk_assessment']['level'],
                    'compliance_frameworks': data['compliance_frameworks'],
                }

                for sys in data['ai_systems']:
                    all_ai_systems.append({
                        'department': dept,
                        'name': sys['name'],
                        'category': sys['category'],
                    })

                for mcp in data['mcp_servers']:
                    all_mcps.append({
                        'department': dept,
                        'name': mcp['name'],
                        'category': mcp['category'],
                    })

                all_compliance.update(data['compliance_frameworks'])
                risk_level = data['risk_assessment']['level']
                if risk_level in risk_counts:
                    risk_counts[risk_level] += 1

                print(f"  [{data['department']['code']:5s}] {data['title'][:55]:55s} "
                      f"| {len(data['ai_systems']):2d} AI | {len(data['mcp_servers'])} MCP | "
                      f"Risk: {risk_level}")
            else:
                print(f"  [REF   ] {data['title'][:55]:55s} | (reference document)")

        except Exception as e:
            print(f"  [ERROR ] {os.path.basename(filepath)}: {e}")

    # --- Build output ---
    output = {
        '_meta': {
            'generator': 'parse_defoneos.py',
            'version': '1.0.0',
            'total_files': len(files),
            'deep_dive_packs': sum(1 for r in results if r['type'] == 'deep_dive_pack'),
            'reference_docs': sum(1 for r in results if r['type'] == 'reference'),
        },
        'summary': {
            'departments': dept_summary,
            'total_ai_systems': len(all_ai_systems),
            'total_mcp_servers': len(all_mcps),
            'risk_distribution': risk_counts,
            'all_compliance_frameworks': sorted(all_compliance),
        },
        'all_ai_systems': all_ai_systems,
        'all_mcp_servers': all_mcps,
        'packs': [r for r in results if r['type'] == 'deep_dive_pack'],
        'references': [r for r in results if r['type'] == 'reference'],
    }

    # Write JSON
    output_path = os.path.join(output_dir, 'defoneos_parsed.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"\nRESULTS SUMMARY")
    print(f"  Deep-dive packs parsed: {output['_meta']['deep_dive_packs']}")
    print(f"  Reference docs:         {output['_meta']['reference_docs']}")
    print(f"  Total AI systems:       {len(all_ai_systems)}")
    print(f"  Total MCP servers:      {len(all_mcps)}")
    print(f"  Risk distribution:      {risk_counts}")
    print(f"  Compliance frameworks:  {len(all_compliance)}")
    print(f"\n  Frameworks: {', '.join(sorted(all_compliance))}")
    print(f"\n  Output: {output_path}")
    print(f"  Size: {os.path.getsize(output_path):,} bytes")

    # --- Compliance engine integration summary ---
    print(f"\n{'=' * 60}")
    print("COMPLIANCE ENGINE INTEGRATION MAP")
    print(f"{'=' * 60}")
    for dept_code, info in sorted(dept_summary.items()):
        print(f"  {dept_code:8s} | {info['sector']:18s} | Risk: {info['risk_level']:8s} | "
              f"{info['ai_system_count']:2d} AI systems | {info['mcp_count']} MCPs | "
              f"Frameworks: {', '.join(info['compliance_frameworks'][:4])}")


if __name__ == '__main__':
    main()
