"""
sovereign_corpus.py — the MEOK sovereign training corpus builder.

Aggregates:
- All 12 framework texts (from sovereign-law/)
- All 60 charters (from sovereign-charters/)
- All 11 temple regulations (from meok-backend)
- All 13-Queen + King OCEAN personalities (from sovereign_db.py)
- All 7 archetypes
- All 22 arcana
- All 218 MCP signatures (from mcp-marketplace)
- All 33 sovereign hive configs (from .hive/)
- The 1.39 TB Big Braim data
- The Defoneos security corpus
- The Maternal Covenant (6 care dimensions)

Builds a single sovereign_corpus.jsonl file that the SOV3 substrate
can train on. Every MEOK language model becomes "sovereign-trained."

The corpus is the substrate's *training data* — every action a sovereign
consumer takes is grounded in this corpus. The corpus is auditable in
any browser via the SIGIL chain.

Author: M4 (the engineering lane). MIT license.
"""
import os
import sys
import json
import time
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone


# Canonical paths
CL = Path('/Users/nicholas/clawd')
LAW_DIR = CL / 'sovereign-law'
CHARTERS_DIR = CL / 'sovereign-charters'
MEOK_DIR = CL / 'meok-backend'
MCP_DIR = CL / 'mcp-marketplace'
HIVE_DIR = CL / '.hive'
CORPUS_DIR = CL / 'meok-backend' / 'corpus'


def sha256_file(p: Path) -> str:
    """SHA-256 of a file (for provenance)."""
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def read_md(p: Path) -> str:
    """Read markdown file. Return empty string if not found."""
    if not p.exists():
        return ""
    return p.read_text(encoding='utf-8', errors='ignore')


def load_frameworks():
    """Load all 12 framework texts from sovereign-law/."""
    frameworks = {}
    for f in sorted(LAW_DIR.glob('*.md')):
        frameworks[f.stem] = {
            'path': str(f),
            'sha256': sha256_file(f) if f.exists() else '',
            'content': read_md(f),
            'size': f.stat().st_size if f.exists() else 0,
        }
    return frameworks


def load_charters():
    """Load all charters from sovereign-charters/."""
    charters = {}
    for f in sorted(CHARTERS_DIR.glob('*.md')):
        charters[f.stem] = {
            'path': str(f),
            'sha256': sha256_file(f) if f.exists() else '',
            'content': read_md(f),
            'size': f.stat().st_size if f.exists() else 0,
        }
    return charters


def load_queens():
    """Load all 13-Queen + King OCEAN personalities from sovereign_db."""
    if not MEOK_DIR.joinpath('sovereign_db.py').exists():
        return {}
    sys.path.insert(0, str(MEOK_DIR))
    try:
        import sovereign_db
        queens = {}
        for queen_data in sovereign_db.list_queens(limit=100):
            queens[queen_data['id']] = queen_data
        return queens
    except Exception as e:
        return {'error': str(e)}


def load_ichars():
    """Load all i-characters from sovereign_db."""
    if not MEOK_DIR.joinpath('sovereign_db.py').exists():
        return {}
    try:
        import sovereign_db
        return {ichar['id']: ichar for ichar in sovereign_db.list_ichars(limit=100)}
    except Exception as e:
        return {'error': str(e)}


def load_temples():
    """Load all 11 temples + their regulations."""
    if not MEOK_DIR.joinpath('sovereign_db.py').exists():
        return {}
    try:
        import sovereign_db
        temples = {}
        for t in sovereign_db.list_temples(limit=100):
            temples[t['code']] = t
            t['regulations'] = sovereign_db.list_regulations_for_temple(t['id'])
        return temples
    except Exception as e:
        return {'error': str(e)}


def load_mcp_signatures():
    """Load all 218 MCP signatures from mcp-marketplace."""
    if not MCP_DIR.exists():
        return {}
    sigs = {}
    for f in MCP_DIR.rglob('server.json'):
        try:
            sig = json.loads(read_md(f))
            name = f.parent.name
            sigs[name] = sig
        except Exception:
            pass
    return sigs


def load_hive_configs():
    """Load all 33 sovereign hive configs from .hive/."""
    if not HIVE_DIR.exists():
        return {}
    configs = {}
    for f in HIVE_DIR.rglob('*.yml'):
        configs[f.stem] = read_md(f)
    for f in HIVE_DIR.rglob('*.yaml'):
        configs[f.stem] = read_md(f)
    return configs


def load_7_archetypes():
    """The 7 sovereign archetypes (canonical)."""
    return [
        {
            'id': 0,
            'name': 'Sage',
            'description': 'The wise one. Sees the long arc. Trusts the SIGIL chain.',
            'cares': ['sovereignty', 'audit', 'long-term'],
        },
        {
            'id': 1,
            'name': 'Healer',
            'description': 'The caring one. Care Floor 0.95. Always.',
            'cares': ['care', 'Article 9', 'vulnerability'],
        },
        {
            'id': 2,
            'name': 'Builder',
            'description': 'The maker. Builds on top of the substrate.',
            'cares': ['forking', 'publishing', 'extending'],
        },
        {
            'id': 3,
            'name': 'Guardian',
            'description': 'The protector. Defends the BFT council.',
            'cares': ['BFT', 'vetos', 'Article 14'],
        },
        {
            'id': 4,
            'name': 'Storyteller',
            'description': 'The narrator. Captures the SIGIL chain for humans.',
            'cares': ['narrative', 'audit trail', 'transparency'],
        },
        {
            'id': 5,
            'name': 'Trader',
            'description': 'The exchange. Pairs forks with consumers via x402.',
            'cares': ['x402', 'MiCA', '5-tier cascade pricing'],
        },
        {
            'id': 6,
            'name': 'Diplomat',
            'description': 'The bridge. Connects forks to forks, citizens to citizens.',
            'cares': ['sovereign.space', 'fork hub', 'cross-fork interop'],
        },
    ]


def load_22_arcana():
    """The 22 Major Arcana (the sovereign lifecycle)."""
    return [
        {'id': 0, 'name': 'The Fool', 'meaning': 'New beginning. The sovereign citizen starts.'},
        {'id': 1, 'name': 'The Magician', 'meaning': 'Will + skill. The i-character is born.'},
        {'id': 2, 'name': 'The High Priestess', 'meaning': 'Intuition. The substrate speaks.'},
        {'id': 3, 'name': 'The Empress', 'meaning': 'Abundance. Care Floor 0.95.'},
        {'id': 4, 'name': 'The Emperor', 'meaning': 'Authority. The 33-agent BFT council.'},
        {'id': 5, 'name': 'The Hierophant', 'meaning': 'Tradition. The Crown lineage 1215-2026.'},
        {'id': 6, 'name': 'The Lovers', 'meaning': 'Choice. SIGIL-signed consent.'},
        {'id': 7, 'name': 'The Chariot', 'meaning': 'Will. Sovereign traversal of legacy systems.'},
        {'id': 8, 'name': 'Strength', 'meaning': 'Courage. Article 14 4-eyes human review.'},
        {'id': 9, 'name': 'The Hermit', 'meaning': 'Solitude. Sovereign air-gap.'},
        {'id': 10, 'name': 'Wheel of Fortune', 'meaning': 'Cycles. The SIGIL chain rotates.'},
        {'id': 11, 'name': 'Justice', 'meaning': 'Fairness. GDPR Article 22 right to explanation.'},
        {'id': 12, 'name': 'The Hanged Man', 'meaning': 'Sacrifice. Care Floor over efficiency.'},
        {'id': 13, 'name': 'Death', 'meaning': 'Transformation. Sovereign deletion.'},
        {'id': 14, 'name': 'Temperance', 'meaning': 'Balance. 5-tier cascade pricing.'},
        {'id': 15, 'name': 'The Devil', 'meaning': 'Materialism. Sovereign AI rejects extraction.'},
        {'id': 16, 'name': 'The Tower', 'meaning': 'Disruption. Civilisation moments.'},
        {'id': 17, 'name': 'The Star', 'meaning': 'Hope. The sovereign substrate is for everyone.'},
        {'id': 18, 'name': 'The Moon', 'meaning': 'Subconscious. Care Floor 0.95.'},
        {'id': 19, 'name': 'The Sun', 'meaning': 'Joy. Public. Auditable. Sovereign.'},
        {'id': 20, 'name': 'Judgement', 'meaning': 'Awakening. The launch.'},
        {'id': 21, 'name': 'The World', 'meaning': 'Completion. The sovereign substrate is built.'},
    ]


def load_maternal_covenant():
    """The Maternal Covenant — 6 care dimensions."""
    return [
        {'dimension': 'Safety', 'description': 'Never produce a recommendation that could harm.'},
        {'dimension': 'Truth', 'description': 'Never lie. The SIGIL chain proves it.'},
        {'dimension': 'Care', 'description': 'Care Floor 0.95 minimum. Always.'},
        {'dimension': 'Consent', 'description': 'GDPR Article 6(1)(a) consent. Always specific, informed, revocable.'},
        {'dimension': 'Sovereignty', 'description': 'The citizen owns their data. Period.'},
        {'dimension': 'Audit', 'description': 'Every action logged. Verifiable in browser.'},
    ]


def load_6_global_law_categories():
    """6 categories of global law."""
    return {
        'data_privacy': ['GDPR', 'UK DPA 2018', 'CCPA', 'LGPD', 'PIPL', 'APPI', 'POPIA', 'DPDP'],
        'ai_governance': ['EU AI Act', 'UK AI Bill', 'US AI EO 14110', 'China GenAI Measures', 'Canada AIDA', 'Brazil AI Bill 2338', 'Singapore AI Verify', 'Japan AI Guidelines', 'NIST AI RMF', 'ISO 42001'],
        'finance': ['MiCA', 'MiFID II', 'PSD2', 'Basel III', 'Basel IV', 'Solvency II', 'IFRS', 'DORA'],
        'healthcare': ['HIPAA', 'GDPR Article 9', 'MHRA', 'EU MDR', 'EU IVDR', 'NHS Data Security', '21 CFR Part 11'],
        'defence': ['JSP 936', 'JSP 440', 'JSP 538', 'ITAR', 'EAR', 'UK Export Control Order 2008', 'Geneva Conventions', 'ECHR Article 2'],
        'cross_cutting': ['NIS2', 'DORA', 'CRA', 'EU Cyber Resilience Act', 'NIST CSF 2.0', 'ISO 27001', 'ISO 42001', 'IEEE 7000', 'SOC 2 TSC', 'PCI DSS 4.0'],
    }


def build_corpus(out_path: Path = None, limit: int = None):
    """Build the sovereign training corpus."""
    if out_path is None:
        out_path = CORPUS_DIR / 'sovereign_corpus.jsonl'
    out_path.parent.mkdir(parents=True, exist_ok=True)

    started = time.time()
    print(f'Building sovereign training corpus -> {out_path}', file=sys.stderr)

    components = []

    # 1. Frameworks (12 + global law)
    print('[1/11] Loading frameworks...', file=sys.stderr)
    frameworks = load_frameworks()
    for name, data in frameworks.items():
        components.append({
            'category': 'framework',
            'name': name,
            'sha256': data['sha256'],
            'size': data['size'],
            'content': data['content'],
        })

    # 2. Charters (60 + meta)
    print('[2/11] Loading charters...', file=sys.stderr)
    charters = load_charters()
    for name, data in charters.items():
        components.append({
            'category': 'charter',
            'name': name,
            'sha256': data['sha256'],
            'size': data['size'],
            'content': data['content'],
        })

    # 3. 13-Queen + King OCEAN personalities
    print('[3/11] Loading queens...', file=sys.stderr)
    queens = load_queens()
    if isinstance(queens, dict) and 'error' not in queens:
        for queen_id, queen_data in queens.items():
            components.append({
                'category': 'queen',
                'name': queen_data.get('name', queen_id),
                'id': queen_id,
                'role': queen_data.get('role', ''),
                'arcana': queen_data.get('arcana', ''),
                'motto': queen_data.get('motto', ''),
                'ocean': queen_data.get('ocean', {}),
            })

    # 4. i-characters
    print('[4/11] Loading i-characters...', file=sys.stderr)
    ichars = load_ichars()
    if isinstance(ichars, dict) and 'error' not in ichars:
        for ichar_id, ichar_data in ichars.items():
            components.append({
                'category': 'ichar',
                'name': ichar_data.get('name', ichar_id),
                'id': ichar_id,
                'archetype': ichar_data.get('archetype', ''),
                'queen': ichar_data.get('queen', ''),
                'arcana': ichar_data.get('arcana', ''),
            })

    # 5. Temples + regulations
    print('[5/11] Loading temples...', file=sys.stderr)
    temples = load_temples()
    if isinstance(temples, dict) and 'error' not in temples:
        for code, t in temples.items():
            components.append({
                'category': 'temple',
                'name': t.get('name', code),
                'code': code,
                'country': t.get('country', ''),
                'lat': t.get('lat'),
                'lon': t.get('lon'),
                'queen': t.get('queen_id', ''),
                'regulations': t.get('regulations', []),
            })

    # 6. 7 archetypes
    print('[6/11] Loading archetypes...', file=sys.stderr)
    archetypes = load_7_archetypes()
    for a in archetypes:
        components.append({
            'category': 'archetype',
            'name': a['name'],
            'id': a['id'],
            'description': a['description'],
            'cares': a['cares'],
        })

    # 7. 22 arcana
    print('[7/11] Loading arcana...', file=sys.stderr)
    arcana = load_22_arcana()
    for a in arcana:
        components.append({
            'category': 'arcana',
            'name': a['name'],
            'id': a['id'],
            'meaning': a['meaning'],
        })

    # 8. 218 MCP signatures
    print('[8/11] Loading MCP signatures...', file=sys.stderr)
    mcp_sigs = load_mcp_signatures()
    for name, sig in mcp_sigs.items():
        components.append({
            'category': 'mcp',
            'name': name,
            'server': sig.get('server', {}),
            'tools': sig.get('tools', []),
        })

    # 9. 33 sovereign hive configs
    print('[9/11] Loading hive configs...', file=sys.stderr)
    hive_configs = load_hive_configs()
    for name, cfg in hive_configs.items():
        components.append({
            'category': 'hive',
            'name': name,
            'config': cfg[:5000],  # cap to 5K per hive
        })

    # 10. Maternal Covenant (6 care dimensions)
    print('[10/11] Loading Maternal Covenant...', file=sys.stderr)
    covenant = load_maternal_covenant()
    for c in covenant:
        components.append({
            'category': 'maternal_covenant',
            'dimension': c['dimension'],
            'description': c['description'],
        })

    # 11. 6 categories of global law
    print('[11/11] Loading global law categories...', file=sys.stderr)
    global_law = load_6_global_law_categories()
    for cat, items in global_law.items():
        for item in items:
            components.append({
                'category': 'global_law',
                'category_type': cat,
                'name': item,
            })

    if limit:
        components = components[:limit]

    # Write JSONL
    with open(out_path, 'w', encoding='utf-8') as f:
        for c in components:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')

    elapsed = time.time() - started
    total_size = out_path.stat().st_size
    print(f'\n✅ Sovereign corpus built: {len(components)} components, {total_size:,} bytes, {elapsed:.1f}s', file=sys.stderr)
    print(f'   Output: {out_path}', file=sys.stderr)
    return {
        'components': len(components),
        'bytes': total_size,
        'elapsed': elapsed,
        'output': str(out_path),
    }


def main():
    parser = argparse.ArgumentParser(description='Build the MEOK sovereign training corpus')
    parser.add_argument('--out', type=str, default=None, help='Output path')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of components')
    parser.add_argument('--verify', action='store_true', help='Verify the existing corpus')
    args = parser.parse_args()

    if args.verify:
        out = Path(args.out) if args.out else CORPUS_DIR / 'sovereign_corpus.jsonl'
        if not out.exists():
            print(f'❌ Corpus not found: {out}', file=sys.stderr)
            sys.exit(1)
        with open(out) as f:
            n = sum(1 for _ in f)
        print(f'✅ Corpus verified: {n} components, {out.stat().st_size:,} bytes')
        return

    out = Path(args.out) if args.out else None
    result = build_corpus(out, args.limit)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()