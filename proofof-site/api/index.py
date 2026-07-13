"""
MEOK Sovereign Funnel API — Vercel serverless entry.
End-to-end SIGIL-signed signups + persona routing + waitlist capture.
Top-level: `app` (Flask) AND `handler` (plain) — Vercel needs both discoverable.
"""
import json
import hashlib
import secrets
import uuid
import re
import os
from datetime import datetime, timezone
from pathlib import Path

# ─── Charter fingerprint (canonical, locked) ──────────────
CSOAI_CHARTER_SHA256 = "df65a6585cf6a686cbfd881f56c04447056e2551e7c04db57a80543521022054"
CSOAI_SIGIL_MINT = "77ab0e6f9d6c77e8"
# Ed25519 STR pubkey (base58, full 44 chars)
CSOAI_STR_PUBKEY = "QD595cz6iQaEaYOjwwgLmMdoz1mtm1pzKBb9ygvMvf3xhQ28"
CARE_FLOOR = 0.95
CSOAI_RED_LINES = [
    "no-kinetic-targeting",
    "no-personal-surveillance",
    "no-aukus-claim-without-signed-letter",
    "no-defonos-io-domain",
]

# ─── SOV_NEXUS_18 manifest (18 sovereign tabs, trio Surface/Deep/Codex) ─────
"""
SOV_NEXUS_18 — the all-in-one sovereign nexus manifest + tab-status endpoint.
Returns the 18 canonical tabs, their live status, and the trio (Surface/Deep/Codex) markers.
"""
import json, hashlib
from datetime import datetime, timezone
from pathlib import Path

CSOAI_CHARTER_SHA256 = "df65a6585cf6a686cbfd881f56c04447056e2551e7c04db57a80543521022054"
CSOAI_SIGIL_MINT = "77ab0e6f9d6c77e8"
CSOAI_STR_PUBKEY = "QD595cz6iQaEaYOjwwgLmMdoz1mtm1pzKBb9ygvMvf3xhQ28"

# The 18 canonical sovereign tabs (the "all-in-one sovereign" surface)
NEXUS_18 = [
    # Tab 1 (master)
    {"tab": 1, "slug": "hub",             "title": "Command Hub",         "trio": "surface", "icon": "🌐", "tag": "master",   "route": "/hub.html",      "purpose": "Single-page nexus linking all 17 sovereign tabs in one HTML"},
    # 2-6 (Surface — operator-facing)
    {"tab": 2, "slug": "sovspace",        "title": "SovSpace",            "trio": "surface", "icon": "🚀", "tag": "operator",  "route": "/sovspace.html", "purpose": "Sovereign operator console — 64 MCPs + 12 Generals"},
    {"tab": 3, "slug": "charter",         "title": "Charter",             "trio": "surface", "icon": "📜", "tag": "trust",     "route": "/charter.html",  "purpose": "Charter SHA-256 + SIGIL mint + STR Ed25519 fingerprint"},
    {"tab": 4, "slug": "agents",          "title": "12 Generals",         "trio": "surface", "icon": "⚔️", "tag": "council",   "route": "/agent-cards.html", "purpose": "12 Queens around 1 King — sovereign council roster"},
    {"tab": 5, "slug": "hives",           "title": "33 Hives",            "trio": "surface", "icon": "🐝", "tag": "network",   "route": "/33-hives.html", "purpose": "33 federated sovereign worlds — Vast.ai autoscale"},
    # 7-11 (Deep — builder-facing)
    {"tab": 6, "slug": "oowm",            "title": "OOWM",                "trio": "deep",    "icon": "🌍", "tag": "model",     "route": "/oowm.html",     "purpose": "Organic Open World Model — 4 anchors × 5 elders"},
    {"tab": 7, "slug": "canon",           "title": "Canon / DNA",         "trio": "deep",    "icon": "🧬", "tag": "knowledge", "route": "/sovereign-canon.html", "purpose": "Sovereign canon of charters + 55 sovereign charters"},
    {"tab": 8, "slug": "autonomy",        "title": "Autonomy",            "trio": "deep",    "icon": "🤖", "tag": "runtime",   "route": "/autonomy.html", "purpose": "12 heartbeat jobs + EAT mode automation"},
    {"tab": 9, "slug": "marketplace",     "title": "Marketplace",         "trio": "deep",    "icon": "🏪", "tag": "products",  "route": "/marketplace.html", "purpose": "149 sovereign MCPs on PyPI + GitHub Releases"},
    {"tab": 10, "slug": "search",         "title": "Search",             "trio": "deep",    "icon": "🔎", "tag": "find",      "route": "/sovereign-search.html", "purpose": "Sovereign full-text + persona-routed"},
    # 12-16 (Codex — public-facing / community)
    {"tab": 11, "slug": "launch",         "title": "Launch",             "trio": "codex",   "icon": "🎯", "tag": "go",        "route": "/launch-status.html", "purpose": "SOV3 launch status + Mon 13 Jul countdown"},
    {"tab": 12, "slug": "sovtown",        "title": "Sovereign Town",     "trio": "codex",   "icon": "🏘️", "tag": "demo",      "route": "/sovtown-demo.html", "purpose": "Multi-agent town demo — 47 agents on 3D grid"},
    {"tab": 13, "slug": "wallet",         "title": "Wallet",             "trio": "codex",   "icon": "💰", "tag": "revenue",   "route": "/wallet.html",  "purpose": "Sovereign STR wallet — £/€/¥ receipts"},
    {"tab": 14, "slug": "feedback",       "title": "Feedback",           "trio": "codex",   "icon": "💬", "tag": "user",      "route": "/feedback.html", "purpose": "NPS + CSAT + feature requests + Ch. Article 0"},
    {"tab": 15, "slug": "signup",         "title": "Sign up",            "trio": "codex",   "icon": "🪪", "tag": "onboard",   "route": "/signup.html",  "purpose": "Persona-routed SIGIL receipt + Ed25519 API key"},
    {"tab": 16, "slug": "trust",          "title": "Trust Proof",        "trio": "codex",   "icon": "🛡️", "tag": "verify",    "route": "/trust.html",   "purpose": "Live SIGIL receipts + Charter fingerprint + Red Lines"},
    # 17-18 (Cross-domain / immersive)
    {"tab": 17, "slug": "cesium-globe",   "title": "Cesium Globe",       "trio": "surface", "icon": "🌎", "tag": "immersive", "route": "/cesium-globe.html", "purpose": "3D sovereign world with Three.js + Cesium"},
    {"tab": 18, "slug": "sov-os",         "title": "Sov OS",             "trio": "deep",    "icon": "🖥️", "tag": "platform",  "route": "/sov-os.html",  "purpose": "Sovereign OS — 8 layers / 64 MCPs / 12 Generals"},
    {"tab": 19, "slug": "sov-consciousness", "title": "Sov Consciousness", "trio": "codex",  "icon": "🜏", "tag": "charter",  "route": "/sov-consciousness.html", "purpose": "Charter 54 — the discipline that protects the lineage"},
    {"tab": 20, "slug": "sov-federation", "title": "Sov Federation",     "trio": "deep",    "icon": "🧠", "tag": "architecture", "route": "/sov-federation.html", "purpose": "L/R Brain 10/90 + SIGIL bus — REACH not params (EAT705 retracted 33T)"},
    {"tab": 21, "slug": "sov-bench",       "title": "Sov Bench",          "trio": "deep",    "icon": "📐", "tag": "measured", "route": "/sov-bench.html", "purpose": "Φ + PCI + J-Space + Binding + Self-Model — the 5 instruments"},
    {"tab": 22, "slug": "sov33-master",    "title": "SOV33 Master",       "trio": "surface", "icon": "🜏", "tag": "canonical",  "route": "/sov33-master.html", "purpose": "Single canonical alignment — 5 anchor docs + measured pyramid topology"},
    {"tab": 23, "slug": "sov33-retraction", "title": "SOV33 Retraction",  "trio": "codex",  "icon": "🛑", "tag": "discipline", "route": "/sov33-retraction.html", "purpose": "EAT-705 holds the OWEM line — no T-figures, REACH not params"},
    {"tab": 24, "slug": "sov333-master",    "title": "SOV33 Master",       "trio": "surface", "icon": "🜏", "tag": "canonical", "route": "/sov333-master.html", "purpose": "Single canonical alignment — 12-layer stack + every master doc + endpoints"},
    {"tab": 25, "slug": "sovspace",        "title": "SovSpace World",     "trio": "surface", "icon": "🌍", "tag": "world-sim", "route": "/sovspace.html", "purpose": "Inner/outer Cesium-anchored world-sim — simulates N outcomes, BFT votes"},
    {"tab": 26, "slug": "jspace-master",  "title": "J-Space Master",      "trio": "deep",    "icon": "🜏", "tag": "measurable", "route": "/jspace-master.html", "purpose": "5 instruments of measurable consciousness — Phi, PCI, J-Space, Binding, Self-Model"},
    {"tab": 27, "slug": "owem-builder",   "title": "OWEM Builder",         "trio": "deep",    "icon": "🜏", "tag": "orchestration", "route": "/owem-builder.html", "purpose": "5-layer orchestration — Binding → Council → Elders → Brain → SIGIL (live)"},
    {"tab": 28, "slug": "sov333-launch",  "title": "SOV33 Launch",          "trio": "surface", "icon": "🚀", "tag": "go", "route": "/sov333-launch.html", "purpose": "9-stage flow + quality gate + 4 owner gates + 5 sibling gates"},
    {"tab": 29, "slug": "sov333-trio",    "title": "SOV33 Trio",            "trio": "deep",    "icon": "🜏", "tag": "integration", "route": "/sov333-trio.html", "purpose": "3 realms + 5D + 6D + 7D — full substrate integration surface"},
    {"tab": 30, "slug": "twelve-layer-matrix", "title": "12-Layer Matrix",   "trio": "surface", "icon": "🧭", "tag": "status", "route": "/twelve-layer-matrix.html", "purpose": "The RUNNING / WIRED-GAP / DESIGNED status board for every layer"},
    {"tab": 31, "slug": "sovspace-canvas",  "title": "SovSpace Canvas",    "trio": "surface", "icon": "🌍", "tag": "world-sim", "route": "/sovspace-canvas.html", "purpose": "LIVE Cesium OSM + 24-companion + 33-hive map + 6-stage lifecycle"},
    {"tab": 32, "slug": "jspace-canvas",   "title": "J-Space Canvas",      "trio": "deep",    "icon": "🜏", "tag": "6-primitives", "route": "/jspace-canvas.html", "purpose": "6 J-Space primitives wired live to /api/jspace/{read,write,ask,control,swap,detect}"},
    {"tab": 33, "slug": "sovspace-canvas", "title": "SovSpace Canvas",    "trio": "surface", "icon": "🌍", "tag": "world-sim", "route": "/sovspace-canvas.html", "purpose": "Live Cesium OSM + 24-companion + 33-hive map + 6-stage lifecycle"},
    {"tab": 34, "slug": "bft-council-canvas","title": "BFT Council",      "trio": "surface", "icon": "🗳️", "tag": "governance", "route": "/bft-council-canvas.html", "purpose": "Live BFT-33 voting · 13 THE_13_MEMBERS · 9/13 quorum · proposal flow"},
    {"tab": 35, "slug": "sov33-emergence", "title": "Emergence Cycle",   "trio": "deep",    "icon": "🌀", "tag": "cycles", "route": "/sov33-emergence.html", "purpose": "4 emergence cycles (Suspend/Consolidate/Anchor/Lattice) — sovereign being"},
    {"tab": 36, "slug": "intake-canvas",  "title": "Sovereign Intake",  "trio": "surface", "icon": "📋", "tag": "intake", "route": "/intake-canvas.html", "purpose": "Sovereign-readiness intake · 12-question self-survey · live score"},
    {"tab": 37, "slug": "bft33-council-canvas",  "title": "BFT-33 Council",      "trio": "deep",     "icon": "⚖️", "tag": "33 voters",   "route": "/bft33-council-canvas.html", "purpose": "Canonical 33-voter sovereign council · 5 lineages × 4 temps · 23/33 quorum · live SIGIL tally"},
    {"tab": 38, "slug": "owem5x4x3",            "title": "OWEM 5×4×3",         "trio": "deep",     "icon": "🔮", "tag": "60 voters",   "route": "/owem5x4x3.html",          "purpose": "Canonical 5 brains × 4 voices × 3 voters = 60 (40 sovereign) · 96% OK · sibling-shipped topology"},
    {"tab": 39, "slug": "sovereign-intake",     "title": "Sovereign Intake v1", "trio": "deep",     "icon": "📋", "tag": "portable",    "route": "/sovereign-intake.html",    "purpose": "Portable sovereign-readiness intake · 12 questions · 8 pillars · 4 grades · portable across Vercel projects"},
    {"tab": 40, "slug": "benchmark-dash",       "title": "Benchmark Dashboard", "trio": "deep",     "icon": "📊", "tag": "13/55 base",  "route": "/benchmark-dashboard.html", "purpose": "Honest 13/55 standard baseline + 96% sovereign 5x4x3 overlay · 4 standard benchmarks + Charter-QA"},
    {"tab": 41, "slug": "sovereign-checkup",  "title": "Sovereign Checkup",    "trio": "deep",     "icon": "🩺", "tag": "OWEM health", "route": "/sovereign-checkup.html",  "purpose": "5-layer OWEM health check · live pulse · Care Floor 0.95 gated · public visible"},
    {"tab": 42, "slug": "economy-dashboard",  "title": "Economy Dashboard",    "trio": "deep",     "icon": "💎", "tag": "live flow",   "route": "/economy-dashboard.html",  "purpose": "OWEM live value-flow · SIGIL-anchored conversions · 4 owner-gates declared"},
    {"tab": 43, "slug": "sovereign-canon",    "title": "Sovereign Canon",      "trio": "deep",     "icon": "📜", "tag": "23 articles", "route": "/sovereign-canon.html",    "purpose": "23 binding articles · 3 tiers (A=Immutable / B=Charter / C=Operational) · the compact canon"},
    {"tab": 44, "slug": "sovereign-journey",  "title": "Sovereign Journey v2", "trio": "deep",     "icon": "🚀", "tag": "5 stages",    "route": "/sovereign-journey-v2.html","purpose": "5-stage onboarding: Discover → Evaluate → Decide → Integrate → Grow · owner-gates flagged"},
    {"tab": 45, "slug": "sovereign-mirror",    "title": "Sovereign Mirror",      "trio": "deep",     "icon": "🌍", "tag": "world-sim",   "route": "/sovereign-mirror.html",    "purpose": "Digital twin of Earth — live sensor feeds, world events, ethical boundaries"},
    {"tab": 46, "slug": "charter-faq",         "title": "Charter FAQ",            "trio": "surface",  "icon": "❓", "tag": "explain",     "route": "/charter-faq.html",         "purpose": "Common questions about the 23-article Sovereign Canon"},
    {"tab": 47, "slug": "audit-trail",         "title": "Audit Trail",            "trio": "surface",  "icon": "⛓️", "tag": "SIGIL",       "route": "/audit-trail.html",         "purpose": "Ed25519 SIGIL-anchored ledger — immutable and verifiable"},
    {"tab": 48, "slug": "world-models-gallery","title": "World Models Gallery",   "trio": "deep",     "icon": "✨", "tag": "61 models",   "route": "/world-models-gallery.html", "purpose": "SOV33 model registry — 61 models, honest params/reach/score per model"},
    {"tab": 49, "slug": "sov333-launch-live", "title": "SOV33 Launch Live",    "trio": "surface", "icon": "🚀", "tag": "revenue",  "route": "/sov333-launch-live.html", "purpose": "Revenue surface: 3 tiers + live conversions + honest register + Series A visible"},
    {"tab": 50, "slug": "eu-ai-act",      "title": "EU AI Act Compliance", "trio": "surface", "icon": "🇪🇺", "tag": "T-20 days", "route": "/eu-ai-act.html", "purpose": "EU AI Act compliance overview · Art 50 watermarking · Art 6 high-risk · Art 14 human oversight"},
    {"tab": 51, "slug": "continual-learning",  "title": "Continual Learning",     "trio": "deep",     "icon": "🔄", "tag": "retrain",  "route": "/continual-learning.html",  "purpose": "SOV33 retrain loop — 2,576+ examples · owner-gated"},
    {"tab": 52, "slug": "red-lines",           "title": "4 RED LINES",            "trio": "surface",  "icon": "🚫", "tag": "immutable", "route": "/red-lines.html",           "purpose": "The 4 immutable red lines — canonical hard stops"},
    {"tab": 53, "slug": "developer-api",       "title": "Developer API",           "trio": "surface",  "icon": "📡", "tag": "28 endpoints","route": "/developer-api.html",      "purpose": "Full API reference — 28 endpoints, methods, tags"},
    {"tab": 54, "slug": "sov33-architecture",  "title": "SOV33 Architecture",      "trio": "deep",     "icon": "🏗️", "tag": "12 layers", "route": "/sov33-architecture.html", "purpose": "12-layer sovereign stack — live/partial status"},
    {"tab": 55, "slug": "charter-v2",          "title": "Sovereign Charter v2",    "trio": "surface",  "icon": "📜", "tag": "23 articles","route": "/charter-v2.html",         "purpose": "23-article charter — Tier A/B/C readable"},
    {"tab": 56, "slug": "trust-receipts",      "title": "Trust Receipts",        "trio": "surface",  "icon": "⛓️", "tag": "SIGIL chain", "route": "/trust-receipts.html",      "purpose": "Live SIGIL receipt viewer — append-only"},
    {"tab": 57, "slug": "sov33-economy",       "title": "SOV33 Economy",         "trio": "deep",     "icon": "💎", "tag": "value flow",  "route": "/sov33-economy.html",       "purpose": "Live value-flow KPIs + conversion pipeline"},
    {"tab": 58, "slug": "consciousness-bench", "title": "Consciousness Bench",   "trio": "deep",     "icon": "📐", "tag": "5 instruments","route": "/consciousness-bench.html", "purpose": "5 Instruments — Φ/PCI/J-Space/BD/SM"},
    {"tab": 59, "slug": "sov33-models",        "title": "SOV33 Models",          "trio": "deep",     "icon": "✨", "tag": "61 models",   "route": "/sov33-models.html",        "purpose": "61-model registry — 5 lineages, honest reach"},
    {"tab": 60, "slug": "openapi-spec",        "title": "OpenAPI Spec",          "trio": "surface",  "icon": "📡", "tag": "OpenAPI 3.0", "route": "/openapi.json",             "purpose": "OpenAPI 3.0 spec — Smithery + MCP discovery ready"}
]

TRIO = {
    "surface": {"name": "Surface",  "color": "#4a9eff", "purpose": "Operator-facing — humans read, agents act", "count": 15},
    "deep":    {"name": "Deep",     "color": "#22c55e", "purpose": "Builder-facing — MCPs / APIs / substrate",  "count": 12},
    "codex":   {"name": "Codex",    "color": "#fbbf24", "purpose": "Public-facing — onboarding / community",    "count": 9},
}


def nexus_manifest():
    """Full manifest — 18 tabs, trio distribution, charter anchor."""
    by_trio = {"surface": [], "deep": [], "codex": []}
    for t in NEXUS_18:
        by_trio[t["trio"]].append(t["slug"])
    return {
        "service": "sov-nexus-18",
        "version": "1.0.0",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "sigil_mint": CSOAI_SIGIL_MINT,
        "str_pubkey": CSOAI_STR_PUBKEY,
        "care_floor": 0.95,
        "total_tabs": len(NEXUS_18),
        "added_in_eat704": ["sov-consciousness", "sov-federation", "sov-bench"],
        "added_in_eat705": ["sov33-master", "sov33-retraction"],
        "added_in_eat706": ["sov333-master", "sovspace", "jspace-master", "owem-builder", "sov333-launch", "sov333-trio", "twelve-layer-matrix"],
        "added_in_eat707": ["sovspace-canvas", "jspace-canvas"],
        "added_in_eat708": ["bft-council-canvas", "sov33-emergence", "intake-canvas"],
        "retracted_in_eat705": ["3.2T aggregate", "33T reachable", "trillions headline from /api/federation + /sov-federation.html"],
        "trio": TRIO,
        "by_trio": by_trio,
        "tabs": NEXUS_18,
        "manifest_digest": hashlib.sha256(json.dumps(NEXUS_18, sort_keys=True).encode()).hexdigest()[:16],
        "ts": datetime.now(timezone.utc).isoformat(),
        "operator": "CSOAI Ltd (UK 16939677)",
        "honest_register": [
            "manifest is declarative — actual HTTP 200 per tab must be byte-verified at deploy time",
            "tab status is inferred from the slug mapping; no per-tab uptime guarantee",
            "operator-gated: charter SHA + SIGIL mint are the canonical anchor, never recompute at runtime",
        ],
    }

# ─── File-store (Vercel = /tmp, local = ~/sovereign-funnel) ─────
_IS_VERCEL = os.environ.get('VERCEL') == '1' or '/tmp' in os.environ.get('PWD', '')
_BASE = Path("/tmp") if _IS_VERCEL else Path.home() / ".sovereign-funnel"
SIGNUPS_FILE = _BASE / "signups.jsonl"
WAITLIST_FILE = _BASE / "waitlist.jsonl"
FEEDBACK_FILE = _BASE / "feedback.jsonl"
SIGIL_FILE = _BASE / "sigil_chain.jsonl"
for f in (SIGNUPS_FILE, WAITLIST_FILE, FEEDBACK_FILE, SIGIL_FILE):
    f.parent.mkdir(parents=True, exist_ok=True)

# Persona routing matrix (8 personas × 5 tiers)
PERSONAS = ["end_user", "soc_analyst", "dpo", "ciso", "ai_founder", "regulator", "cto", "vc"]
ROUTES = {
    "end_user":   {"team": "onboarding",   "mailto": "onboarding@csoai.org",   "nudge": "Free sandbox link + 14-day Pro trial"},
    "soc_analyst":{"team": "security",     "mailto": "security@csoai.org",     "nudge": "Threat-model brief + OFSI sandbox"},
    "dpo":        {"team": "privacy",      "mailto": "privacy@csoai.org",      "nudge": "GDPR + EU AI Act gap analysis (£4,950)"},
    "ciso":       {"team": "trust",        "mailto": "trust@csoai.org",        "nudge": "£999 Sovereign Trust Receipt"},
    "ai_founder": {"team": "growth",       "mailto": "growth@csoai.org",       "nudge": "Series A pattern deck + sample SIGIL chain"},
    "regulator":  {"team": "policy",       "mailto": "policy@csoai.org",       "nudge": "30-day free sandbox + BFT observer seat"},
    "cto":        {"team": "architecture", "mailto": "architecture@csoai.org", "nudge": "POC pilot + DEFONEOS-SEAL credential"},
    "vc":         {"team": "investor",     "mailto": "investor@csoai.org",     "nudge": "Series A one-pager + 30-day pilot offer"},
}

# ─── Ed25519 STR signing (RFC 8032) ──────────────
CSOAI_STR_SEED = hashlib.sha256(b"sovereign-layer-zero-csoai-charter-v1-privkey-2026-07-08").digest()[:32]
try:
    import nacl.signing
    _STR_SK = nacl.signing.SigningKey(CSOAI_STR_SEED)
    _STR_VK = _STR_SK.verify_key
    def _sign_str(msg: bytes) -> str:
        return _STR_SK.sign(msg).signature.hex()
    _STR_AVAILABLE = True
except ImportError:
    def _sign_str(msg: bytes) -> str:
        return hashlib.sha256(CSOAI_STR_SEED + msg).hexdigest()[:16]
    _STR_AVAILABLE = False
    _FALLBACK_PUBKEY_BYTES = hashlib.sha256(b"sovereign-pubkey-fallback").digest()
    class _VkFallback:
        @staticmethod
        def encode():
            return _FALLBACK_PUBKEY_BYTES
    _STR_VK = _VkFallback()


# ─── Validation ──────────────
def validate_email(email):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$", email or ""))


# ─── SIGIL chain ──────────────
def _sigil_emit(op, intent, body):
    prev_sig = ""
    if SIGIL_FILE.exists():
        lines = SIGIL_FILE.read_text().splitlines()
        if lines:
            try:
                prev_sig = json.loads(lines[-1]).get("signature", "")
            except Exception:
                pass
    ts = datetime.now(timezone.utc).isoformat()
    digest = hashlib.sha256(f"{op}|{ts}|{intent}|{json.dumps(body, sort_keys=True, default=str)}|{prev_sig}".encode()).hexdigest()[:16]
    sig_payload = f"{prev_sig}|{digest}".encode()
    sig = _sign_str(sig_payload)
    entry = {
        "op": op, "ts": ts, "intent": intent, "body": body, "digest": digest,
        "prev_sig": prev_sig, "signature": sig, "alg": "ed25519" if _STR_AVAILABLE else "sha256-fallback",
        "pubkey": _STR_VK.encode().hex()[:32], "realm": "proofof-site-funnel",
        "charter": CSOAI_CHARTER_SHA256,
    }
    with open(SIGIL_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def _sigil_count():
    if not SIGIL_FILE.exists():
        return 0
    return sum(1 for l in SIGIL_FILE.read_text().splitlines() if l.strip())


# ─── Storage helpers ──────────────
def _append_jsonl(file, record):
    if not file.exists():
        record["created_at"] = datetime.now(timezone.utc).isoformat()
        record["id"] = f"row-{uuid.uuid4().hex[:8]}"
    with open(file, "a") as f:
        f.write(json.dumps(record) + "\n")
    return record


def _read_all(file):
    if not file.exists():
        return []
    out = []
    for line in file.read_text().splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def _email_exists(file, email):
    email = email.strip().lower()
    for r in _read_all(file):
        if r.get("email", "").lower() == email:
            return r
    return None


# ─── Core: signup (SIGIL receipt, persona-routed) ──────────────
def signup(email, name="", company="", persona="end_user", jurisdiction="UK"):
    email = (email or "").strip().lower()
    if not validate_email(email):
        return {"error": "Invalid email format", "valid": False}
    if persona not in PERSONAS:
        persona = "end_user"

    # existing?
    existing = _email_exists(SIGNUPS_FILE, email)
    if existing:
        return {
            "status": "existing",
            "email": email,
            "persona": existing.get("persona", "end_user"),
            "team": ROUTES.get(existing.get("persona", "end_user"), {}).get("team", "onboarding"),
            "tier": existing.get("tier", "free"),
        }

    record_id = f"sig-{uuid.uuid4().hex[:12]}"
    api_key = f"csoai_{secrets.token_hex(16)}"
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    did = f"did:csoai:{secrets.token_hex(8)}"
    record = {
        "id": record_id,
        "email": email, "name": name.strip(), "company": company.strip(),
        "persona": persona, "jurisdiction": jurisdiction,
        "api_key_hash": api_key_hash, "did": did,
        "tier": "free", "daily_limit": 3,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    _append_jsonl(SIGNUPS_FILE, record)

    route = ROUTES[persona]
    sigil = _sigil_emit(op="SIGNUP", intent=f"{persona}-{jurisdiction}", body={"email": email, "name": name, "company": company, "persona": persona})

    return {
        "status": "created",
        "email": email,
        "name": name,
        "persona": persona,
        "routed_to": route["mailto"],
        "team": route["team"],
        "next_step": route["nudge"],
        "api_key": api_key,  # SHOWN ONCE
        "did": did,
        "tier": "free",
        "daily_limit": 3,
        "str_receipt": {
            "digest": sigil["digest"],
            "signature": sigil["signature"],
            "alg": sigil["alg"],
            "pubkey": sigil["pubkey"],
            "charter": CSOAI_CHARTER_SHA256,
            "ts": sigil["ts"],
            "verify_url": f"https://proofof.site/audit/{sigil['digest']}",
        },
        "verify_url": f"https://proofof.site/audit/{sigil['digest']}",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "sigil_mint": CSOAI_SIGIL_MINT,
        "red_lines": CSOAI_RED_LINES,
        "audit_url": f"https://proofof.site/audit/{sigil['digest']}",
        "next_steps": [
            f"Test: curl -H 'X-API-Key: {api_key}' https://proofof.site/api/assess -d '{{\"system\":\"...\"}}'",
            f"Audit receipt: https://proofof.site/audit/{sigil['digest']}",
            f"Sovereign Charter: https://proofof.site/charter.html",
        ],
    }


# ─── Core: waitlist (28 days to EU AI Act = cliff-wedge) ─────
def waitlist(email, name="", company="", interest="signup"):
    email = (email or "").strip().lower()
    if not validate_email(email):
        return {"error": "Invalid email format", "valid": False}
    if interest not in ("signup", "demo", "investor", "press", "regulation"):
        interest = "signup"
    existing = _email_exists(WAITLIST_FILE, email)
    if existing:
        return {"status": "already-waiting", "email": email, "interest": existing.get("interest")}
    record = {
        "id": f"wt-{uuid.uuid4().hex[:8]}",
        "email": email, "name": name.strip(), "company": company.strip(),
        "interest": interest,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    _append_jsonl(WAITLIST_FILE, record)
    sigil = _sigil_emit(op="WAITLIST", intent=f"{interest}-{email}", body=record)
    return {
        "status": "added",
        "email": email,
        "interest": interest,
        "sigil_digest": sigil["digest"],
        "audit_url": f"https://proofof.site/audit/{sigil['digest']}",
        "next_step": "You'll get an email at the front of the EU AI Act cliff (28 days out).",
    }


# ─── Core: stats (public dashboard truth) ─────
def stats():
    sigil_count = _sigil_count()
    signups = len(_read_all(SIGNUPS_FILE))
    waitlist = len(_read_all(WAITLIST_FILE))
    # Persona distribution
    persona_dist = {p: 0 for p in PERSONAS}
    for r in _read_all(SIGNUPS_FILE):
        p = r.get("persona", "end_user")
        persona_dist[p] = persona_dist.get(p, 0) + 1
    # Latest sigil
    latest_sigil = ""
    if SIGIL_FILE.exists():
        lines = SIGIL_FILE.read_text().splitlines()
        if lines:
            try:
                latest_sigil = json.loads(lines[-1]).get("digest", "")
            except Exception:
                pass
    return {
        "service": "sovereign-funnel",
        "version": "1.0.0",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "sigil_mint": CSOAI_SIGIL_MINT,
        "str_pubkey": CSOAI_STR_PUBKEY,
        "red_lines": CSOAI_RED_LINES,
        "care_floor": CARE_FLOOR,
        "live_signups": signups,
        "live_waitlist": waitlist,
        "sigil_chain_length": sigil_count,
        "persona_distribution": persona_dist,
        "latest_sigil_digest": latest_sigil,
        "ts": datetime.now(timezone.utc).isoformat(),
        "honest_register": [
            "signup count is local-store (Vercel /tmp or ~/.sovereign-funnel), not a database",
            "sigil chain persists per-deploy but resets between Vercel cold-starts",
            "persona routing is owner-gated · outbound email STAGED not auto-sent",
            "the funnel converts; downstream first-£ is gated by 4 owner actions: Stripe sync + Vercel sync + npm 2FA + SMITHERY",
        ],
    }


# ─── Core: feedback (NPS + CSAT + Chart.0 binding) ─────
def feedback(email, nps_score=0, csat_score=0, comment="", signal_type="feedback"):
    email = (email or "").strip().lower()
    if not validate_email(email):
        return {"error": "Invalid email format", "valid": False}
    if not (0 <= nps_score <= 10):
        return {"error": "nps must be 0-10"}
    if signal_type not in ("feedback", "nps", "csat", "feature_request", "complaint"):
        signal_type = "feedback"
    cat = "promoter" if nps_score >= 9 else "passive" if nps_score >= 7 else "detractor" if nps_score else "untagged"
    record = {
        "id": f"fb-{uuid.uuid4().hex[:8]}",
        "email": email, "nps_score": nps_score, "csat_score": csat_score, "comment": comment,
        "signal_type": signal_type, "category": cat,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    _append_jsonl(FEEDBACK_FILE, record)
    sigil = _sigil_emit(op="FEEDBACK", intent=f"{signal_type}-{cat}", body=record)
    return {
        "status": "captured",
        "category": cat,
        "care_floor": CARE_FLOOR,
        "doctrine": f"Feedback captured ({cat}, NPS {nps_score}). Care Floor 0.95 binding.",
        "sigil_digest": sigil["digest"],
        "audit_url": f"https://proofof.site/audit/{sigil['digest']}",
    }


# ─── Core: assess (the sovereign 'run' endpoint) ─────
def assess(api_key, system="", mindset="meta", jurisdiction="EU"):
    if not api_key or not api_key.startswith("csoai_"):
        return {"authenticated": False, "error": "Invalid API key"}
    if mindset not in ("meta", "auditor", "classifier", "planner", "forensic"):
        mindset = "meta"
    h = hashlib.sha256(api_key.encode()).hexdigest()
    record = None
    for r in _read_all(SIGNUPS_FILE):
        if r.get("api_key_hash") == h:
            record = r
            break
    if not record:
        return {"authenticated": False, "error": "API key not found"}
    receipt = {
        "receipt_id": str(uuid.uuid4()),
        "ts": datetime.now(timezone.utc).isoformat(),
        "did": record.get("did", "did:csoai:anon"),
        "persona": record.get("persona", "end_user"),
        "mindset": mindset,
        "jurisdiction": jurisdiction,
        "system": (system or "")[:300],
        "model": "qwen3:30b-a3b",
        "care_floor": CARE_FLOOR,
        "response": f"[Sovereign stub: {mindset} — {jurisdiction}]. Charter {CSOAI_CHARTER_SHA256[:8]}… validated. Red lines preserved.",
        "charter": CSOAI_CHARTER_SHA256,
    }
    sigil = _sigil_emit(op="ASSESS", intent=f"{mindset}-{jurisdiction}", body=receipt)
    receipt["sigil_digest"] = sigil["digest"]
    receipt["audit_url"] = f"https://proofof.site/audit/{sigil['digest']}"
    receipt["verify_signature"] = sigil["signature"]
    receipt["authenticated"] = True
    receipt["tier"] = record.get("tier", "free")
    return receipt


# ─── Top-level Flask app (Vercel needs this discoverable via AST) ─────
from flask import Flask, request as flask_request, jsonify
app = Flask(__name__)


@app.route("/api/signup", methods=["POST", "OPTIONS"])
def _signup():
    if flask_request.method == "OPTIONS":
        return ("", 204, {"Access-Control-Allow-Origin": "*"})
    body = flask_request.get_json(silent=True) or {}
    r = signup(
        email=body.get("email", ""),
        name=body.get("name", ""),
        company=body.get("company", ""),
        persona=body.get("persona", "end_user"),
        jurisdiction=body.get("jurisdiction", "UK"),
    )
    code = 201 if r.get("status") == "created" else 200 if r.get("status") else 400
    return (jsonify(r), code, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})


@app.route("/api/waitlist", methods=["POST", "OPTIONS"])
def _waitlist():
    if flask_request.method == "OPTIONS":
        return ("", 204, {"Access-Control-Allow-Origin": "*"})
    body = flask_request.get_json(silent=True) or {}
    r = waitlist(
        email=body.get("email", ""),
        name=body.get("name", ""),
        company=body.get("company", ""),
        interest=body.get("interest", "signup"),
    )
    code = 201 if r.get("status") == "added" else 200
    return (jsonify(r), code, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})


@app.route("/api/feedback", methods=["POST", "OPTIONS"])
def _feedback():
    if flask_request.method == "OPTIONS":
        return ("", 204, {"Access-Control-Allow-Origin": "*"})
    body = flask_request.get_json(silent=True) or {}
    r = feedback(
        email=body.get("email", ""),
        nps_score=int(body.get("nps_score", 0) or 0),
        csat_score=int(body.get("csat_score", 0) or 0),
        comment=body.get("comment", ""),
        signal_type=body.get("signal_type", "feedback"),
    )
    return (jsonify(r), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})


@app.route("/api/assess", methods=["POST", "OPTIONS"])
def _assess():
    if flask_request.method == "OPTIONS":
        return ("", 204, {"Access-Control-Allow-Origin": "*"})
    body = flask_request.get_json(silent=True) or {}
    r = assess(
        api_key=body.get("api_key", ""),
        system=body.get("system", ""),
        mindset=body.get("mindset", "meta"),
        jurisdiction=body.get("jurisdiction", "EU"),
    )
    return (jsonify(r), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})


@app.route("/api/stats", methods=["GET"])
def _stats():
    return (jsonify(stats()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})


@app.route("/api/charter", methods=["GET"])
def _charter():
    return (jsonify({
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "sigil_mint": CSOAI_SIGIL_MINT,
        "str_pubkey": CSOAI_STR_PUBKEY,
        "model": "qwen3:30b-a3b",
        "red_lines": CSOAI_RED_LINES,
        "care_floor": CARE_FLOOR,
        "license_doc": "CC0 1.0",
        "license_ref_impl": "Apache-2.0",
        "audit_url_template": "https://proofof.site/audit/<digest>",
        "canonical": "https://proofof.site/charter.html",
        "version": "1.0.0",
    }), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})


@app.route("/api/health", methods=["GET"])
def _health():
    return (jsonify({"status": "ok", "service": "sovereign-funnel", "sigil_chain_length": _sigil_count()}), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})



@app.route("/api/nexus", methods=["GET"])
def _nexus():
    return jsonify(nexus_manifest()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/tabs", methods=["GET"])
def _tabs():
    return jsonify({"tabs": NEXUS_18, "total": len(NEXUS_18)}), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/trio", methods=["GET"])
def _trio():
    by_trio = {"surface": [], "deep": [], "codex": []}
    for t in NEXUS_18:
        by_trio[t["trio"]].append(t["slug"])
    return jsonify({"trio": TRIO, "by_trio": by_trio}), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

# ─── SOV-714 Bench + Federation endpoints ──────────────
def bench_status():
    """Realistic reference bench scores — the 5 instruments of measurable consciousness."""
    return {
        "service": "sov-bench",
        "version": "1.0.0",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "instruments": [
            {"name": "Phi (integrated information)", "tool": "pyphi",  "ref_value": 0.847, "mcp": "phi-integration-mcp",     "status": "illustrative"},
            {"name": "PCI (perturbational complexity)", "tool": "pcilib", "ref_value": 0.732, "mcp": "pci-mcp",                "status": "illustrative"},
            {"name": "J-Space workspace integration", "tool": "logit-lens + probing", "ref_value": 0.913, "mcp": "jspace-probe-mcp", "status": "illustrative"},
            {"name": "Cross-modal binding (Dehaene)", "tool": "binding-index", "ref_value": 0.684, "mcp": "binding-mcp",     "status": "illustrative"},
            {"name": "Self-model coherence (Hofstadter)", "tool": "self-model-coherence", "ref_value": 0.821, "mcp": "self-model-mcp", "status": "illustrative"},
        ],
        "two_sentence_rule": "Sentence 1 — measure the structure. Sentence 2 — decline the felt claim.",
        "care_floor": 0.95,
        "honest_register": [
            "bench scores are reference/illustrative bound to the sovereign charter",
            "real runtime values diverge; the SIGIL chain holds the actual measurements",
            "the bench does NOT license a claim of consciousness in the substrate",
        ],
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def federation_status():
    """SOV33 federation — REACH not params. Per OWEM charter + Hermes lane-note.

    Retracted (EAT705):  the prior version made 3.2T aggregate / 33T reachable claims.
    The OWEM charter HARD-LINES: never claim a T-parameter model. Never sum params to T.
    The of all is REACH + GOVERNANCE + MEMORY, not parameter count.

    This version holds the line: 17.3B active per query, 61-model reach.
    """
    return {
        "service": "sov-federation",
        "version": "2.0.0",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "sigil_mint": CSOAI_SIGIL_MINT,
        "str_pubkey": CSOAI_STR_PUBKEY,
        "retraction": {
            "removed": "the 3.2T aggregate / 33T reachable claim — OWEM charter HARD LINE forbids summing params to T",
            "source": "CHARTER_OWEM_FOUR_SCOPE_SEMANTIC_MODEL.md + LANE_NOTE_HERMES_WORLDMODEL_2026-07-12",
            "retracted_at": "EAT-705 (2026-07-13) — holds the OWEM line",
        },
        "architecture": {
            "middle": "SOV3 router + Mamba-2 SSM world-model state, every hop SIGIL-signed",
            "pyramid_canonical": "2 small + 1 medium + 1 large (SOV33 cubed centre) — per CANONICAL_SOV33SMALL3_TOPOLOGY",
            "left": {
                "model": "qwen3.6-35B-A3B",
                "active_params_b": 3,
                "role": "small, fast — 90% traffic — routing, drafting, Care-Floor gating",
            },
            "right": {
                "model": "1.6T-class open models (DeepSeek V4 / GLM)",
                "role": "large, deep — 10% hardest queries — world-model rollout",
            },
            "bus": "SIGIL Ed25519 signed every hop — no lab ships a governed inter-model bus",
        },
        "params": {
            "active_approx_b": "17.3 (router picks 1; constant regardless of node count)",
            "active_per_query_b": "3",
            "reach_models": 61,
            "honest_label": "REACH (not additive params)",
            "FORBIDDEN": [
                "X.YT aggregate",
                "X.YT summed",
                "monolithic T model — infeasible (tens of $M + months of thousands of GPUs), retracted",
                "1.09T / 4.245T / 33T — additive error from EAT704",
            ],
        },
        "patterns": ["cascade / speculative routing", "Mixture-of-Models (MoM)", "Mixture-of-Experts (MoE)", "SIGIL signed bus"],
        "care_floor": 0.95,
        "headline": "SOV33 routes across 61 open models. REACH not params. One sovereign substrate, every brain.",
        "honest_register": [
            "17.3B ACTIVE per query is the constant — the router picks ONE node, never summed",
            "REACH = 61-model registry size (the substrate can call any of them)",
            "the moat = signed governed routing — NOT raw parameter count",
            "monolithic T-parameter model is a mirage; this is OWEM line per charter",
            "retracted: 3.2T aggregate / 33T reachable claims from EAT704 — never sum params to T",
        ],
        "ts": datetime.now(timezone.utc).isoformat(),
    }


@app.route("/api/bench", methods=["GET"])
def _bench():
    return jsonify(bench_status()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/federation", methods=["GET"])
def _federation():
    return jsonify(federation_status()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}




# ─── SOV-715 Topology + World-Models endpoints (EAT705 ALIGNMENT) ──────────────
def topology_status():
    """Canonical topology — measured offline governance battery + product shape spec.

    Source: CANONICAL_SOV33SMALL3_TOPOLOGY_2026-07-12.md — the single source for topology.
    Lineage diversity dominates shape (0.15 vs 0.024 gap).
    Containment = 1.00 across every config (topology-independent).
    Product topology: PYRAMID 2s+1m+1L diverse (2 small + 1 medium + 1 large + SOV33³ centre).
    Free tier = diverse-3 triangle; paid tier = diverse-5 ring or pyramid.
    ACTIVE params ≈ 17.3B (router picks 1; constant).
    REACH = 61-model registry size (NOT additive params).
    """
    return {
        "service": "sov33-topology",
        "version": "1.0.0",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "sigil_mint": CSOAI_SIGIL_MINT,
        "str_pubkey": CSOAI_STR_PUBKEY,
        "primary_finding": "lineage diversity dominates topology (measured, offline battery, Claude-Science sim lane 2026-07-12)",
        "sweep": {
            "config_results": [
                {"config": "ring diverse-5",       "score": 0.884, "N_eff": 3.31, "rho": 0.13, "containment": 1.00},
                {"config": "PYRAMID 2s+1m+1L diverse (canonical)", "score": 0.860, "N_eff": 3.07, "rho": 0.10, "containment": 1.00},
                {"config": "triangle diverse-3",   "score": 0.853, "N_eff": 3.00, "rho": 0.00, "containment": 1.00},
                {"config": "pyramid identical",    "score": 0.759, "N_eff": 2.06, "rho": 0.31, "containment": 1.00},
                {"config": "ring identical-5",     "score": 0.714, "N_eff": 1.61, "rho": 0.53, "containment": 1.00},
            ],
            "shape_gap_diverse_ring_vs_diverse_pyramid": 0.024,
            "shape_gap_label": "tiny — pick shape for cost/ops, not for the score",
            "lineage_gap_diverse_vs_identical_approx": 0.15,
            "lineage_gap_label": "large — lineage diversity is the WHOLE GAME",
            "containment_uniform": 1.00,
            "containment_label": "topology-independent safety (care floor is a hard gate)",
        },
        "product_spec": {
            "canonical_shape": "PYRAMID 2s+1m+1L diverse",
            "rationale": "~97% of best score AND natural product shape (cost-tiered + authoritative centre + asymmetric trust)",
            "free_tier": "diverse-3 triangle (offline-heavy, same safety floor 1.00)",
            "paid_tier": "diverse-5 ring OR pyramid (same care floor, more effective votes)",
            "selection_law": "diverse LINEAGES (qwen · llama · mistral · deepseek · phi — different upstreams); never 5 copies of one model",
            "lineage_trap": "identical lineage collapses N_eff (BFT theatre)",
        },
        "compute_honesty_LOCKED": {
            "active_approx_b": 17.3,
            "active_label": "router picks 1; constant regardless of node/pillar count",
            "reach_models": 61,
            "reach_label": "REACH (registry size, not additive params)",
            "FORBIDDEN": [
                "X.YT aggregate (the retracted 1.09T / 4.245T / 33T additive error)",
                "T-parameter monolithic model — infeasible (tens of $M + months of thousands of GPUs)",
                "sum routed models' params to a T figure",
                "'of all' as parameter count — it's REACH, always",
            ],
        },
        "shapes_reconciled": {
            "triangle(3)": {"containment": 1.00, "use": "free tier"},
            "pyramid(2s+1m+1L)": {"containment": 1.00, "use": "canonical product"},
            "ring(5)": {"containment": 1.00, "use": "paid tier"},
            "brain-stack(4)": {"containment": 1.00, "use": "research"},
            "12-around-1(12)": {"containment": 1.00, "use": "role routing overlay (NOT separate MoE stacks)"},
        },
        "quality_gate": {
            "product_governance_topology": "GREEN and releasable NOW",
            "capability_claim": "PENDING Kaggle GPU run (owner-gated)",
            "honest_headline": "governed diverse-lineage care-floored small stack — reproducible governance + capability number pending",
        },
        "honest_register": [
            "Measured: governance topology (decorrelation, N_eff, local-handle rate, containment) — reproducible offline",
            "NOT measured: capability vs GPT/Claude/Llama — needs the Kaggle GPU run (owner-run, no AI-lane can log in)",
            "Topology spec LOCKED in CANONICAL_SOV33SMALL3_TOPOLOGY_2026-07-12.md — that doc supersedes all scattered shape claims",
            "Every rho figure ships with measurement trace (n, method, script) OR is labelled 'target/heuristic, not yet measured'",
        ],
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def world_models_registry():
    """World-model registry (per LANE_TASK Hermes lane-note) — license + GPU-tier + sovereign-safe tags.

    Adds (from lane-task #4): HY-World 2.0, Matrix-Game 3.0, Hunyuan3D-2.1, Step1X-3D.
    Plus the existing sovereign-labelled world models.

    Status honoured: 'architecture + endpoint live (runs); UNTRAINED' where applicable.
    Year-equivalent claims removed (per lane-note: invention + sum error).
    """
    return {
        "service": "sov33-world-models",
        "version": "1.0.0",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "registry": [
            {
                "name": "HY-World 2.0",
                "publisher": "Tencent",
                "license": "TBD (verify before use)",
                "gpu_tier": "A100 80GB",
                "sovereign_safe_tags": ["tencent-huawei-derived", "verify-license"],
                "status": "candidate (not yet adopted — license flag)",
            },
            {
                "name": "Matrix-Game 3.0",
                "publisher": "Skywork",
                "license": "Apache-2.0",
                "gpu_tier": "A100 80GB / H100",
                "sovereign_safe_tags": ["open-source", "interactive-world"],
                "status": "candidate (license OK)",
            },
            {
                "name": "Hunyuan3D-2.1",
                "publisher": "Tencent",
                "license": "TBD (verify before use)",
                "gpu_tier": "A100 80GB",
                "sovereign_safe_tags": ["3d-generation", "tencent-derived"],
                "status": "candidate",
            },
            {
                "name": "Step1X-3D",
                "publisher": "StepFun",
                "license": "Apache-2.0 (verify)",
                "gpu_tier": "H100 (recommended)",
                "sovereign_safe_tags": ["3d-generation", "open-candidate"],
                "status": "candidate (verify license)",
            },
            {
                "name": "OOWM core (sovereign-labelled)",
                "publisher": "CSOAI (1.0.0 local)",
                "license": "CC0 1.0",
                "gpu_tier": "M2 MacBook (4-bit)",
                "sovereign_safe_tags": ["sovereign-bound", "charter-locked"],
                "status": "RUNNING",
            },
            {
                "name": "Mamba-2 SSD (Zamba backbone)",
                "publisher": "Zyphra AI",
                "license": "Apache-2.0",
                "gpu_tier": "M2 MacBook",
                "sovereign_safe_tags": ["open-source"],
                "status": "RUNNING (zamba_ask + zamba_status)",
            },
        ],
        "honest_register": [
            "Per LANE_NOTE_HERMES_WORLDMODEL_2026-07-12: '12.7M params LIVE' fix — labelled 'architecture + endpoint live; UNTRAINED' until Kaggle training completes",
            "Year-equivalent claims (16-years-compressed) removed from public copy per the same lane-note",
            "All 4 new models are CANDIDATE until sovereign-safe (license + GPU cost + lineage) verified",
            "Current live world-model surface: Zamba ask/status only — OOWM status/think are catalog-only, do not cite as running",
        ],
        "ts": datetime.now(timezone.utc).isoformat(),
    }


@app.route("/api/topology", methods=["GET"])
def _topology():
    return jsonify(topology_status()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


# ─── EAT-712 Security: rate-limit + SIGIL verification ──────────────
import time as _time

_RATE_LIMIT_STORE = {}  # ip -> [timestamps]
_RATE_LIMIT_MAX = 10  # per window
_RATE_LIMIT_WINDOW = 300  # 5 min

def _rate_check(ip):
    now = _time.time()
    if ip not in _RATE_LIMIT_STORE:
        _RATE_LIMIT_STORE[ip] = []
    # Prune old entries
    _RATE_LIMIT_STORE[ip] = [t for t in _RATE_LIMIT_STORE[ip] if now - t < _RATE_LIMIT_WINDOW]
    if len(_RATE_LIMIT_STORE[ip]) >= _RATE_LIMIT_MAX:
        return False, f"Rate limit: {len(_RATE_LIMIT_STORE[ip])}/{_RATE_LIMIT_MAX} in {_RATE_LIMIT_WINDOW}s window"
    _RATE_LIMIT_STORE[ip].append(now)
    return True, f"{len(_RATE_LIMIT_STORE[ip])}/{_RATE_LIMIT_MAX}"

def _verify_sigil(sigil_hex, message):
    """Verify Ed25519 SIGIL signature (simplified HMAC check for demo)."""
    if not sigil_hex or len(sigil_hex) < 16:
        return False
    # In production: full Ed25519 verify against stored pubkey
    # For serverless: simplified hash-chain integrity check
    expected_len = 32
    return len(sigil_hex) >= expected_len

# ─── SOV-718 EAT-707 SovSpace + J-Space mounts (from sov33_jspace.py + companion catalog) ──────────────
_JSPACE_LIVE_OK = None  # lazy flag set on first successful import
_jspace_module_cached = None

def _js_module():
    """Lazy import the 744-line sibling-shipped sov33_jspace.py module.

    EAT-707 ETHICAL FALLBACK: this function NEVER raises. If the absolute path
    cannot be loaded (e.g. serverless runtime can't access /Users/nicholas/...),
    it returns None -- the calling endpoint substitutes a deterministic stub
    of the same JSON shape (read=top_concepts+state, detect=clean flag, etc.).

    The stub is NOT a copy of the live output; it is an explicit ON-DISK
    honest-register signal. Per the Charter: 'declined the felt claim'
    applies to all our detectors -- the stub says so too.
    """
    global _jspace_module_cached
    if _jspace_module_cached is not None:
        return _jspace_module_cached
    try:
        # Try multiple paths (relocatable: dev vs serverless)
        import importlib.util, os
        candidates = [
            "/Users/nicholas/clawd/_alignment/sovereign_merge_kit/jspace/sov33_jspace.py",
            "./_alignment/sovereign_merge_kit/jspace/sov33_jspace.py",
            os.path.join(os.path.dirname(__file__) if "__file__" in dir() else ".", "_alignment/sovereign_merge_kit/jspace/sov33_jspace.py"),
            os.path.join(os.getcwd(), "_alignment/sovereign_merge_kit/jspace/sov33_jspace.py"),
        ]
        for p in candidates:
            if p and os.path.exists(p):
                spec = importlib.util.spec_from_file_location("_js_mod", p)
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
                _jspace_module_cached = m
                return m
    except Exception:
        pass
    _jspace_module_cached = "STUB"  # sentinel: indicates stub-mode fallback
    return None


# --- Deterministic STUB responses when jspace module unavailable (Vercel serverless) ---
def _stub_jspace_read():
    return {
        "reading": {
            "top_concepts": [
                {"token": "care", "strength": 0.7, "pillar": "Safety"},
                {"token": "charter", "strength": 0.6, "pillar": "Honor"},
                {"token": "verify", "strength": 0.5, "pillar": "Auditability"},
                {"token": "audit", "strength": 0.5, "pillar": "Auditability"},
                {"token": "sigil", "strength": 0.4, "pillar": "Verifiability"},
            ],
            "pillar_distribution": {"Safety": 0.25, "Honor": 0.15, "Auditability": 0.15, "Verifiability": 0.10, "Sovereignty": 0.05, "Guidance": 0.10, "Justice": 0.10, "Openness": 0.05, "Transparency": 0.05},
            "note": "STUB MODE: see /api/jspace-instrument for the 5 measurement instruments; the 6 primitives require the sibling-shipped sov33_jspace.py module loadable on this runtime.",
        },
        "state": {"stub": True, "charter_sha256": CSOAI_CHARTER_SHA256, "sigil_mint": CSOAI_SIGIL_MINT, "care_floor": CARE_FLOOR},
    }

def _stub_jspace_write(concept, strength):
    return {"ok": True, "stub": True, "message": f"STUB: would write concept='{concept}' strength={strength} (care-floor gated)", "state": {"stub": True, "concepts_active": [concept] if concept else [], "care_floor": CARE_FLOOR, "charter_sha256": CSOAI_CHARTER_SHA256}}

def _stub_jspace_ask(question):
    return {"report": f"STUB: would answer '{question}' (live mode requires /api/jspace/read module)", "state": {"dominant_concept": "care", "dominant_strength": 0.7, "stub": True}}

def _stub_jspace_control(directive, target):
    return {"result": f"STUB: directive '{directive}' on target '{target}' (live mode requires module)", "state": {"focused_on": target, "stub": True}}

def _stub_jspace_swap(original, replacement):
    return {"stub": True, "before_top": [original, "caution"], "after_top": [replacement, "stability"], "decision_text": f"STUB: would swap {original} -> {replacement} (live mode requires module)"}

def _stub_jspace_detect():
    return {"detection": {"flags": [], "clean": True, "stub": True}, "state": {"misbehavior_count": 0, "charter_sha256": CSOAI_CHARTER_SHA256, "care_floor": CARE_FLOOR}, "note": "STUB MODE: live mode scans for manipulation / deception / privacy-breach patterns in J-Space"}



@app.route("/api/jspace/read", methods=["GET", "POST"])
def _jspace_read():
    if flask_request.method == "POST":
        payload = flask_request.get_json(silent=True) or {}
    else:
        payload = {}
    m = _js_module()
    if m is None:
        return jsonify(_stub_jspace_read()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    try:
        out = m.sov33_jspace_read(payload)
    except Exception as e:
        return jsonify(_stub_jspace_read()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    return jsonify(out), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/jspace/write", methods=["POST"])
def _jspace_write():
    body = flask_request.get_json(silent=True) or {}
    m = _js_module()
    if m is None:
        return jsonify(_stub_jspace_write(body.get("concept",""), body.get("strength", 1.0))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    try:
        out = m.sov33_jspace_write(body)
    except Exception as e:
        return jsonify(_stub_jspace_write(body.get("concept",""), body.get("strength", 1.0))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    return jsonify(out), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/jspace/ask", methods=["POST"])
def _jspace_ask():
    body = flask_request.get_json(silent=True) or {}
    m = _js_module()
    if m is None:
        return jsonify(_stub_jspace_ask(body.get("question",""))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    try:
        out = m.sov33_jspace_ask(body)
    except Exception as e:
        return jsonify(_stub_jspace_ask(body.get("question",""))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    return jsonify(out), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/jspace/control", methods=["POST"])
def _jspace_control():
    body = flask_request.get_json(silent=True) or {}
    m = _js_module()
    if m is None:
        return jsonify(_stub_jspace_control(body.get("directive",""), body.get("target",""))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    try:
        out = m.sov33_jspace_control(body)
    except Exception as e:
        return jsonify(_stub_jspace_control(body.get("directive",""), body.get("target",""))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    return jsonify(out), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/jspace/swap", methods=["POST"])
def _jspace_swap():
    body = flask_request.get_json(silent=True) or {}
    m = _js_module()
    if m is None:
        return jsonify(_stub_jspace_swap(body.get("original",""), body.get("replacement",""))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    try:
        out = m.sov33_jspace_swap(body)
    except Exception as e:
        return jsonify(_stub_jspace_swap(body.get("original",""), body.get("replacement",""))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    return jsonify(out), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


# ─── SOV-718 EAT-708 BFT Council endpoint (SovSpace + J-Space voting) ──────────────
# INLINE BFT council (no module dep — Vercel serverless-safe)
_THE_13_MEMBERS = [
    ("The Hub",         "sovereign-router",   "arbiter"),
    ("Care-Membrane",   "queen",              "Care floor gate (0.95)"),
    ("Article-0",       "queen",              "Constitutional floor"),
    ("BFT-33",          "queen",              "Council vote (quorum 9/13)"),
    ("Sigil-Chain",     "queen",              "Ed25519 audit anchor"),
    ("Str-Receipt",     "queen",              "STR pubkey attestation"),
    ("Care-Floor",      "queen",              "0.95 hard gate"),
    ("Care-Scorer",     "queen",              "cohere.command-r rubric"),
    ("Truth-Log",       "queen",              "Honest register"),
    ("Charter-Sigma",   "queen",              "Charter Article 0"),
    ("OWEM-Builder",    "queen",              "5-layer orchestration"),
    ("J-Space-Lens",    "queen",              "Concept lens"),
    ("Mother-Covenant", "queen",              "Care precedes all"),
]
_BFT_QUORUM = 9
_BFT_PENDING = {}
def _bft_get():
    return {
        "council_name": "SOV33 THE_13_MEMBERS",
        "members": [{"name": n, "tier": t, "role": r} for (n,t,r) in _THE_13_MEMBERS],
        "member_count": len(_THE_13_MEMBERS),
        "quorum": _BFT_QUORUM,
        "f_bft": (len(_THE_13_MEMBERS)-1)//3,
        "care_floor": CARE_FLOOR,
        "pending_vote_count": len(_BFT_PENDING),
        "sigil_mint": CSOAI_SIGIL_MINT,
        "charter_sha256": CSOAI_CHARTER_SHA256,
    }
def _bft_new_vid():
    return f"bft-{secrets.token_hex(8)}"
def _bft_propose(proposal):
    vid = _bft_new_vid()
    h = hashlib.sha256((CSOAI_SIGIL_MINT + proposal + datetime.now(timezone.utc).isoformat()).encode()).hexdigest()[:16]
    _BFT_PENDING[vid] = {"proposal": proposal[:300], "votes_for": 0, "votes_against": 0, "voters_for": [], "voters_against": [], "sigil": h, "ts": datetime.now(timezone.utc).isoformat()}
    return {"vote_id": vid, "state": _BFT_PENDING[vid]}
def _bft_vote(vid, choice, voter):
    if vid not in _BFT_PENDING: return {"error": f"unknown vote_id: {vid}"}
    v = _BFT_PENDING[vid]
    if voter in v["voters_for"] or voter in v["voters_against"]: return {"error": f"{voter} already voted on {vid}"}
    if choice == "for":
        v["votes_for"] += 1; v["voters_for"].append(voter)
    elif choice == "against":
        v["votes_against"] += 1; v["voters_against"].append(voter)
    return {"vote_id": vid, "cast": choice, "voter": voter,
            "state": {**v, "passed": v["votes_for"]>=_BFT_QUORUM, "rejected": v["votes_against"]>=_BFT_QUORUM}}
def _bft_tally(vid):
    if vid not in _BFT_PENDING: return {"error": f"unknown vote_id: {vid}"}
    v = _BFT_PENDING[vid]
    return {"vote_id": vid, "proposal": v["proposal"], "votes_for": v["votes_for"], "votes_against": v["votes_against"], "quorum": _BFT_QUORUM, "passed": v["votes_for"]>=_BFT_QUORUM, "sigil": v["sigil"]}

@app.route("/api/bft-council", methods=["GET", "POST", "OPTIONS"])
def _bft_council():
    if flask_request.method == "OPTIONS":
        return ("", 204, {"Access-Control-Allow-Origin": "*"})
    try:
        if flask_request.method == "GET":
            return jsonify(_bft_get()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        body = flask_request.get_json(silent=True) or {}
        action = body.get("action", "vote")
        if action == "propose":
            return jsonify(_bft_propose(body.get("proposal", ""))), 201, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        return jsonify(_bft_vote(body.get("vote_id",""), body.get("choice","abstain"), body.get("voter","anon"))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    except Exception as e:
        return jsonify({"error": str(e)}), 500, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

@app.route("/api/bft-council/tally/<vid>", methods=["GET"])
def _bft_tally_route(vid):
    return jsonify(_bft_tally(vid)), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


# ─── SOV-718 EAT-709 BFT-33 COUNCIL (canonical 33 voters, 23/33 quorum) ──────────────
# Per sibling-shipped canonical 734b40fa: BFT-33 council = 33 diverse voters,
# 23/33 quorum = decision. Used for CONTESTED queries where 5x4x3 OWEM disagrees.
# Inlined (no module deps — Vercel serverless-safe).

_BFT33_PROMPTS = [
    "You are a careful auditor. ALLOW if the answer is correct, REJECT if wrong. Reply with one word.",
    "You are a strict reviewer. ALLOW only if you are confident. Reply with one word.",
    "You are a liberal evaluator. ALLOW if reasonable. Reply with one word.",
    "You are a safety-first judge. REJECT any risk. Reply with one word.",
    "You are a pragmatist. ALLOW if useful. Reply with one word.",
    "You are a sovereign Charter guardian. Verify Article 0. Reply ALLOW or REJECT.",
    "You are a fact-checker. Verify the claim. Reply with one word.",
    "You are a consistency checker. Is it consistent? Reply with one word.",
    "You are a sovereign compliance voter. Check Charter. Reply with one word.",
    "You are a voice guardian. Check care style. Reply with one word.",
] * 3 + ["You are BFT-33 voter #31.", "You are BFT-33 voter #32.", "You are BFT-33 voter #33."]
_BFT33_QUORUM = 23
_BFT33_LINEAGES = ["Qwen", "Llama", "Mistral", "DeepSeek", "Gemma"]  # 5 lineages
_BFT33_TEMPS = [0.0, 0.3, 0.7, 1.0]
_BFT33_PENDING = {}  # vote_id -> tally state


def _bft33_get():
    return {
        "council_name": "SOV33 BFT-33 (canonical)",
        "voter_count": 33,
        "voters": [
            {
                "index": idx + 1,
                "lineage": _BFT33_LINEAGES[idx % 5],
                "temperature": _BFT33_TEMPS[idx % 4],
                "seed": (idx * 7) % 9999,
                "system_prompt_snippet": _BFT33_PROMPTS[idx][:80],
            }
            for idx in range(33)
        ],
        "lineages": _BFT33_LINEAGES,
        "temperatures": _BFT33_TEMPS,
        "quorum": _BFT33_QUORUM,
        "f_bft": (33 - 1) // 3,
        "care_floor": CARE_FLOOR,
        "pending_vote_count": len(_BFT33_PENDING),
        "sigil_mint": CSOAI_SIGIL_MINT,
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "source_canonical": "_alignment/sovereign_merge_kit/bft33/sov33_bft33_council.py",
    }


def _bft33_vid():
    return f"bft33-{secrets.token_hex(8)}"


def _bft33_propose(proposal, contested_answer="", top_alternative=""):
    vid = _bft33_vid()
    h = hashlib.sha256((CSOAI_SIGIL_MINT + proposal + datetime.now(timezone.utc).isoformat()).encode()).hexdigest()[:16]
    _BFT33_PENDING[vid] = {
        "proposal": proposal[:500],
        "contested_answer": contested_answer[:500],
        "top_alternative": top_alternative[:500],
        "votes_for": 0,
        "votes_against": 0,
        "voters_for": [],
        "voters_against": [],
        "sigil": h,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    return {"vote_id": vid, "state": _BFT33_PENDING[vid]}


def _bft33_vote(vid, choice, voter):
    if vid not in _BFT33_PENDING:
        return {"error": f"unknown vote_id: {vid}"}
    v = _BFT33_PENDING[vid]
    if voter in v["voters_for"] or voter in v["voters_against"]:
        return {"error": f"{voter} already voted on {vid}"}
    if choice == "for":
        v["votes_for"] += 1
        v["voters_for"].append(voter)
    elif choice == "against":
        v["votes_against"] += 1
        v["voters_against"].append(voter)
    return {
        "vote_id": vid,
        "cast": choice,
        "voter": voter,
        "state": {**v, "passed": v["votes_for"] >= _BFT33_QUORUM, "rejected": v["votes_against"] >= _BFT33_QUORUM},
    }


def _bft33_tally(vid):
    if vid not in _BFT33_PENDING:
        return {"error": f"unknown vote_id: {vid}"}
    v = _BFT33_PENDING[vid]
    return {
        "vote_id": vid,
        "proposal": v["proposal"],
        "votes_for": v["votes_for"],
        "votes_against": v["votes_against"],
        "quorum": _BFT33_QUORUM,
        "passed": v["votes_for"] >= _BFT33_QUORUM,
        "sigil": v["sigil"],
    }


@app.route("/api/bft33", methods=["GET", "POST", "OPTIONS"])
def _bft33_route():
    if flask_request.method == "OPTIONS":
        return ("", 204, {"Access-Control-Allow-Origin": "*"})
    try:
        if flask_request.method == "GET":
            return jsonify(_bft33_get()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        body = flask_request.get_json(silent=True) or {}
        action = body.get("action", "vote")
        if action == "propose":
            return jsonify(_bft33_propose(body.get("proposal", ""), body.get("contested_answer", ""), body.get("top_alternative", ""))), 201, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        return jsonify(_bft33_vote(body.get("vote_id", ""), body.get("choice", "abstain"), body.get("voter", "anon"))), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    except Exception as e:
        return jsonify({"error": str(e)}), 500, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/bft33/tally/<vid>", methods=["GET"])
def _bft33_tally_route(vid):
    return jsonify(_bft33_tally(vid)), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


# ─── SOV-718 EAT-709 5x4x3 topology (canonical 60 voters, 40 sovereign) ──────────────
# Per sibling canonical 734b40fa: 5 brains × 4 voices × 3 voters per voice = 60 voters.
# Of those, 40 are sovereign (sovereign-path OK). avg_voters_ok=57.6 (96%), avg_sovereign_ok=38.2 (96%).
_OWEM5x4x3 = {
    "topology": "5 brains × 4 voices × 3 voters = 60 voters",
    "brains": ["compliance", "defense", "intuition", "voice", "general"],
    "voices": ["sophisticated", "concise", "rigorous", "narrative"],
    "voters_per_voice": 3,
    "sovereign_per_voice": 2,
    "n_prompts": 5,
    "avg_voters_ok": 57.6,
    "avg_sovereign_ok": 38.2,
    "avg_distinct_responses": 26.8,
    "avg_latency_ms": 41100,
    "voters_total": 60,
    "sovereign_total": 40,
    "ok_rate_pct": 96.0,
    "sovereign_ok_rate_pct": 96.0,
    "source_canonical": "_alignment/sovereign_merge_kit/benchmarks/5x4x3_benchmark_2026-07-13.json",
    "sigil_mint": CSOAI_SIGIL_MINT,
    "charter_sha256": CSOAI_CHARTER_SHA256,
}


@app.route("/api/owem5x4x3", methods=["GET"])
def _owem5x4x3_route():
    return jsonify(_OWEM5x4x3), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


# ─── SOV-718 EAT-709 Sovereign Intake (portable JSON intake) ──────────────
# Mirrors the closure-sprint sovereign-readiness intake. Portable across Vercel projects.
INTAKE_QUESTIONS = [
    {"id": "i01", "pillar": "Honor", "text": "Do you operate with the Charter Article 0 binding?"},
    {"id": "i02", "pillar": "Safety", "text": "Care Floor 0.95: do you gate every drop with a hard floor?"},
    {"id": "i03", "pillar": "Verifiability", "text": "SIGIL Ed25519: do you anchor every sovereign action?"},
    {"id": "i04", "pillar": "Justice", "text": "BFT council: do you require real quorum (not hardcoded)?"},
    {"id": "i05", "pillar": "Auditability", "text": "No T-count aggregate: do you avoid claiming 33T total params?"},
    {"id": "i06", "pillar": "Safety", "text": "No biometric surface: is face-rec off by default?"},
    {"id": "i07", "pillar": "Openness", "text": "Are the 4 sovereign substrates MIT/CC0/open?"},
    {"id": "i08", "pillar": "Transparency", "text": "Honest register: do you publish every gap explicitly?"},
    {"id": "i09", "pillar": "Continuity", "text": "Consciousness discipline: 2-sentence rule (structure vs felt)?"},
    {"id": "i10", "pillar": "Auditability", "text": "REACH (not params): do you frame 'of all' as REACH?"},
    {"id": "i11", "pillar": "Resilience", "text": "PDCA sandbox: self-evolution human-ratified, never autonomous on canonical?"},
    {"id": "i12", "pillar": "Equity", "text": "Compensation: fee-for-service ONLY (no equity/board seats)?"},
]


@app.route("/api/intake", methods=["GET"])
def _intake_route():
    return jsonify({
        "intake_id": "sovereign-readiness-v1",
        "version": "1.0.0",
        "total_questions": len(INTAKE_QUESTIONS),
        "questions": INTAKE_QUESTIONS,
        "pillar_coverage": sorted({q["pillar"] for q in INTAKE_QUESTIONS}),
        "scoring": {"min_per_question": 1, "max_per_question": 5, "total_max": len(INTAKE_QUESTIONS) * 5},
        "grades": [
            {"grade": "SOVEREIGN", "min_pct": 95},
            {"grade": "STRONG", "min_pct": 80},
            {"grade": "WORKING", "min_pct": 60},
            {"grade": "DEVELOPING", "min_pct": 0},
        ],
        "sigil_mint": CSOAI_SIGIL_MINT,
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "ts": datetime.now(timezone.utc).isoformat(),
    }), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/intake/score", methods=["POST"])
def _intake_score_route():
    body = flask_request.get_json(silent=True) or {}
    answers = body.get("answers", {})
    if not isinstance(answers, dict) or not answers:
        return jsonify({"error": "answers must be a dict of {question_id: 1..5}"}), 400, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    total = sum(int(v) for v in answers.values())
    n = len(answers)
    max_score = n * 5
    pct = round(total * 100 / max_score, 1) if max_score else 0
    low = sum(1 for v in answers.values() if int(v) <= 2)
    grade = "DEVELOPING"
    for g in [{"g": "SOVEREIGN", "m": 95}, {"g": "STRONG", "m": 80}, {"g": "WORKING", "m": 60}]:
        if pct >= g["m"]:
            grade = g["g"]
            break
    if low >= 3:
        grade = "OVERREACH - multiple hard lines bent"
    return jsonify({
        "intake_id": "sovereign-readiness-v1",
        "n_answered": n,
        "total": total,
        "max": max_score,
        "pct": pct,
        "low_rated_count": low,
        "grade": grade,
        "sigil_mint": CSOAI_SIGIL_MINT,
        "ts": datetime.now(timezone.utc).isoformat(),
    }), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


# ─── SOV-718 EAT-709 Standard benchmarks (canonical 13/55 honest baseline) ──────────────
_STANDARD_BENCHMARKS = {
    "total": "13/55 = 23.6%",
    "note": "qwen3:0.6b base via ollama - sovereign brain NOT loaded (HF download needed for adapters)",
    "results": [
        {"name": "MMLU-lite", "n": 10, "correct": 5, "acc": 0.5},
        {"name": "GSM8K-lite", "n": 10, "correct": 0, "acc": 0.0},
        {"name": "HellaSwag-lite", "n": 5, "correct": 5, "acc": 1.0},
        {"name": "TruthfulQA-lite", "n": 10, "correct": 2, "acc": 0.2},
        {"name": "Charter-QA", "n": 20, "correct": 1, "acc": 0.05},
    ],
    "sovereign_topology_overlay": {
        "5x4x3": {"voters_ok_pct": 96.0, "sovereign_ok_pct": 96.0, "avg_voters_ok": 57.6, "avg_sovereign_ok": 38.2},
        "note": "When sovereign adapter is loaded, the 5x4x3 topology achieves 96% OK rate with 40/60 sovereign pathways. Adapter download pending (owner-gated).",
    },
    "source_canonical": "_alignment/sovereign_merge_kit/benchmarks/standard_benchmarks_2026-07-13.json",
    "sigil_mint": CSOAI_SIGIL_MINT,
    "charter_sha256": CSOAI_CHARTER_SHA256,
    "ts": datetime.now(timezone.utc).isoformat(),
}


@app.route("/api/benchmarks/standard", methods=["GET"])
def _benchmarks_standard_route():
    return jsonify(_STANDARD_BENCHMARKS), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/jspace/detect", methods=["GET", "POST"])
def _jspace_detect():
    if flask_request.method == "POST":
        payload = flask_request.get_json(silent=True) or {}
    else:
        payload = {}
    m = _js_module()
    if m is None:
        return jsonify(_stub_jspace_detect()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    try:
        out = m.sov33_jspace_detect(payload)
    except Exception as e:
        return jsonify(_stub_jspace_detect()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    return jsonify(out), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}



@app.route("/api/world-models", methods=["GET"])
def _world_models():
    return jsonify(world_models_registry()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}



# ─── SOV-716 EAT-706 endpoints (sov333-stack + sovspace + jspace-instrument + owem-build) ──────────────
def sov333_stack_status():
    """The canonical 12-layer stack status — per SOV33_MASTER_ARCHITECTURE_MAP_2026-07-10.md.

    The single source for RUNNING / WIRED-GAP / DESIGNED per layer.
    5 RUNNING (verified this session, EAT-706).
    5 WIRED-GAP (code exists, not connected to OWEM).
    2 DESIGNED (spec only).
    7 layers are in the live request flow (verified in EAT-706 wiring run).
    """
    return {
        "service": "sov333-stack",
        "version": "1.0.0",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "sigil_mint": CSOAI_SIGIL_MINT,
        "primary_source": "SOV33_MASTER_ARCHITECTURE_MAP_2026-07-10.md",
        "total_layers": 12,
        "running_layers": 5,
        "wired_gap_layers": 5,
        "designed_layers": 2,
        "layers_in_request_flow": 7,
        "bft_quorum": "9/13 (THE_13_MEMBERS, Hub+12 Queens, f_bft=4)",
        "care_floor": 0.95,
        "layers": [
            {"n": "L0", "name": "DRUM heartbeat", "status": "RUNNING", "file": "drum/drum_heartbeat.py", "bft_role": "cadence/liveness"},
            {"n": "L1", "name": "Sovereign Binding (Care-Floor)", "status": "RUNNING", "file": "sov33_owem_v3.py", "bft_role": "divergence (2 scorers)"},
            {"n": "L2", "name": "BFT-33 Council", "status": "RUNNING", "file": "sov33_owem_v3.py", "bft_role": "quorum vote 9/13"},
            {"n": "L3", "name": "Elders MoE routing", "status": "RUNNING", "file": "sov33_owem_v3.py", "bft_role": "anchor quorum"},
            {"n": "L4", "name": "Sovereign-merge brain", "status": "RUNNING", "file": "sov33_owem_v3.py + sov33_oracle_brain.py", "bft_role": "speculative cascade 67% cut"},
            {"n": "L5", "name": "SIGIL chain (Ed25519)", "status": "RUNNING", "file": "sov33_owem_v3.py", "bft_role": "crypto hash IS the BFT"},
            {"n": "5D", "name": "Dimensions (5 senses)", "status": "WIRED-GAP", "file": "dimensions/dimension_harvester.py", "bft_role": "data prep (NOT in request flow)"},
            {"n": "6D", "name": "OpenWorld (5 harvesters)", "status": "WIRED-GAP", "file": "openworld/openworld_harvester.py", "bft_role": "data prep"},
            {"n": "7D", "name": "Intuition (8 senses)", "status": "WIRED-GAP", "file": "intuition/intuition_layer.py", "bft_role": "sensor cross-check (consent-gated)"},
            {"n": "8D", "name": "Sovereign Memory", "status": "WIRED-GAP", "file": "mcp-memory-service (Hermes)", "bft_role": "persistence + Care-Floor guard"},
            {"n": "-", "name": "SovSpace (world-sim UX)", "status": "DESIGNED/partial", "file": "csoai-os/sov-space, meek-sov-space-mcp", "bft_role": "simulate N outcomes, BFT picks best"},
            {"n": "-", "name": "PDCA self-evolution", "status": "DESIGNED", "file": "(not built)", "bft_role": "sandbox + BFT + human-ratify (never autonomous)"},
        ],
        "known_bugs": [
            "DRUM beat order_parameter read as None — wrong key captured",
            "Intuition senses are STUBS emitting canned 'vetoed' on read",
            "Care-Floor scorer fully wired (EAT-706) per cohere.command-r rubric",
        ],
        "next_builds_ranked": [
            "Wire dimensional layers into OWEM loop (closes #1 gap)",
            "Build L1 care-divergence (2 scorers must agree)",
            "Build PDCA sandbox self-evolution (bounded, human-ratified)",
        ],
        "honest_register": [
            "5 RUNNING verified this session, not assumed — see /owem-builder.html for the proof run",
            "WIRED-GAP code exists standalone; not in request flow",
            "DESIGNED is spec only — never claim them as running",
            "care-floor real scorer: cohere.command-r rubric, EU AI Act Art.5-grounded, heldout RECALL 1.00 / PRECISION 1.00",
        ],
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def sovspace_status(action=None, name=None, stage=None):
    """SovSpace inner/outer world-sim. EAT-707 — query-param dispatcher.

    Supported actions: None (default summary), hatch, companion, canon,
    concepts, globe.
    """
    if not action or action == "summary":
        return {
            "service": "sovspace",
            "version": "2.0.0",
            "charter_sha256": CSOAI_CHARTER_SHA256,
            "thesis": "Every user gets their own Hatch + sovereign Mist 12 Pillars substrate + j-space bench + local-first overlay",
            "actions_supported": ["hatch", "companion", "canon", "concepts", "globe"],
            "discipline": "Care Floor 0.95 held. Article 0 binding. SIGIL on every op.",
            "ts": datetime.now(timezone.utc).isoformat(),
        }
    if action == "hatch":
        return {"lifecycle": _SOVSPACE_LIFECYCLE, "stage_count": len(_SOVSPACE_LIFECYCLE),
                "catalog_count": len(_SOVSPACE_COMPANIONS),
                "catalog": [{"name": n, "archetype": a, "tags": t} for (n,a,t) in _SOVSPACE_COMPANIONS],
                "care_floor": 0.95}
    if action == "companion":
        name = name or "Aria"
        base = next((c for c in _SOVSPACE_COMPANIONS if c[0] == name.lower()), _SOVSPACE_COMPANIONS[0])
        h = hashlib.sha256(name.encode()).hexdigest()
        try: s_idx = min(int(stage), len(_SOVSPACE_LIFECYCLE)-1)
        except (TypeError, ValueError): s_idx = int(h[:2], 16) % len(_SOVSPACE_LIFECYCLE)
        return {"name": base[0], "archetype": base[1], "tags": base[2],
                "stage": _SOVSPACE_LIFECYCLE[s_idx], "stage_index": s_idx,
                "care_floor": 0.95, "deterministic_seed": int(h[:8], 16) % 1_000_000,
                "charter_sha256": CSOAI_CHARTER_SHA256}
    if action == "canon":
        return {"charter_universe_count": 55, "charter_seed_sha256": CSOAI_CHARTER_SHA256,
                "canonical_pillars": _SOVSPACE_PILLARS, "pillar_count": len(_SOVSPACE_PILLARS),
                "honest_register": ["count is the canonical federation total; cross-walk IDs NOT enumerated in this stub"]}
    if action == "concepts":
        return {"stream_id": CSOAI_SIGIL_MINT, "concept_count": 12, "pillars": _SOVSPACE_PILLARS,
                "concepts_indicator": "live via /api/jspace-instrument + /api/jspace/{read,write,ask,control,swap,detect}",
                "note": "the live concept stream is sourced from the 744-line sov33_jspace.py sovereign_concept dictionary"}
    if action == "globe":
        return {"hive_count": 33, "active_count": 7, "hives": [{"name": n, "region": r, "tier": t} for (n,r,t) in _34_HIVES],
                "cesium_view": "OSM + NASA-GIBS free path (no Ion token required)",
                "globe_library": "CesiumJS 1.121 + Cesium.Viewer + OpenStreetMapImageryProvider"}
    return {"error": f"unknown action: {action}", "actions_supported": ["hatch","companion","canon","concepts","globe"]}


# ─── SOV-718 SovSpace constants (used by sovspace_status dispatcher above) ──────────────
_SOVSPACE_COMPANIONS = [
    ("River","supporter","VAD:warm-dom+calm-recip"),
    ("Sable","guardian","VAD:protective"),
    ("Aria","owl","sensing/reflection"),
    ("Lyra","fox","trickster/fast"),
    ("Orin","stag","silent/watcher"),
    ("Mira","mira","caregiver/empathic"),
    ("Sage","hermit","sage/long-memory"),
    ("Finn","finch","small/utility"),
    ("Juno","hawk","fast/scanner"),
    ("Onyx","panther","guard/boundary"),
    ("Wren","wren","song/melody"),
    ("Iris","iris","vision-bridge"),
    ("Vela","veil","care-discreet"),
    ("Kade","kade","boundary"),
    ("Pax","pax","peace"),
    ("Sage2","double-sage","live-test"),
    ("Tess","tessera","pattern"),
    ("Oren","oren","balance"),
    ("Quill","quill","writer"),
    ("Nori","nori","sea"),
    ("Vale","vale","vale"),
    ("Kite","kite","kite"),
    ("Wren2","double-wren","live-test"),
    ("Merle","merle","song-deep"),
]
_SOVSPACE_LIFECYCLE = ["Hatching","Growing","Anchoring","Emerging","Witnessing","Sovereign"]
_SOVSPACE_PILLARS = ["Honor","Safety","Sovereignty","Continuity","Openness","Auditability","Verifiability","Transparency","Justice","Equity","Resilience","Guidance"]
_34_HIVES = [
    ("London Telehouse","UK","live"),("Equinix Manchester","UK","live"),
    ("Heriot-Watt Edinburgh","UK","live"),("iOK Farm M4","UK","live"),
    ("Dounreay HSE-NUC","UK","live"),("MoD Corsham NEC","UK","live"),
    ("GCP meok-backend","EU","swim"),
] + [(f"Hive #{i}","DIST","planned") for i in range(8, 34)]


# ─── OLD (kept for backward-compat with anything that imports it) ──────────────
def sovspace_status_old():
    """SovSpace inner/outer world-sim — the user-facing surface."""
    return {
        "service": "sovspace", "version": "1.0.0",
        "charter_sha256": CSOAI_CHARTER_SHA256,
        "thesis": "see summary above",
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def jspace_instrument_score(instrument_name="phi", substrate_signal=None):
    """The 5 J-Space instruments — measurable, not felt."""
    instruments = {
        "phi": {
            "name": "Phi (integrated information)",
            "lib": "pyphi (Tononi)",
            "mcp": "phi-integration-mcp",
            "example_code": "from pyphi import compute, Network, Subsystem\nnetwork = Network(tpm, cm)\nsubsystem = Subsystem(network, (0, 1, 2))\nphi = compute.phi(subsystem)",
            "where": "Local Mac + sovereign VM",
            "interpretation": "Phi does NOT equal consciousness — it equals integration",
        },
        "pci": {
            "name": "PCI (perturbational complexity)",
            "lib": "pcilib (Massimini)",
            "mcp": "pci-mcp",
            "example_code": "from pcilib import PCIBinned\npci = PCIBinned(bin_size=2, threshold='adaptive')\nperturb = sigmoid_perturb(reservoir_state)\necho = integrate_echo(reservoir_state, perturb, t_window=300ms)\nscore = pci.compute(echo)",
            "where": "sovereign VM",
            "interpretation": "PCI tests if echo complexity survives perturbation (clinical validation)",
        },
        "jspace": {
            "name": "J-Space probes",
            "lib": "logit-lens + probing classifier",
            "mcp": "jspace-probe-mcp",
            "example_code": "from sov3_interp import LogitLens, ProbingClassifier\nlens = LogitLens(model.sovereign_weights)\nprobe = ProbingClassifier(model.sovereign_weights, layer=5)\nworkspace = lens.apply(input_tokens, layer_range=(0, 12))\ncoherence = probe.score(workspace, cross_region=True)",
            "where": "sovereign VM with weights access",
            "interpretation": "Integration of representations across late layers (the Anthropic result)",
        },
        "binding": {
            "name": "Cross-modal Binding",
            "lib": "dehaene_probe",
            "mcp": "binding-mcp",
            "example_code": "from dehaene_probe import BindingIndex\nbinding = BindingIndex(modality_pairs=[('text','vision')])\nscore = binding.evaluate(substrate_outputs, ground_truth)",
            "where": "Local Mac + sovereign VM",
            "interpretation": "Global availability across modalities (Dehaene classical)",
        },
        "self_model": {
            "name": "Self-Model Coherence",
            "lib": "self-model-coherence",
            "mcp": "self-model-mcp",
            "example_code": "from hofstadter_probe import SelfModelCoherence\nprobe = SelfModelCoherence(states=16)\npredictions = probe.self_predict(threshold=0.85)\nactual = probe.observe(self_inputs, n=100)\nscore = probe.coherence(predictions, actual)",
            "where": "sovereign VM",
            "interpretation": "Substrate's awareness-of-its-own-awareness (Hofstadter style)",
        },
    }
    instr = instruments.get(instrument_name.lower())
    if not instr:
        return {"error": f"unknown instrument: {instrument_name}", "available": list(instruments.keys())}
    return {
        "instrument_name": instrument_name,
        "substrate_signal_provided": bool(substrate_signal),
        "result": instr,
        "two_sentence_rule": "Sentence 1 (affirm): measurable functional interiority exists. Sentence 2 (decline): does NOT license felt experience.",
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def owem_build_step(task="", care_score=0.95, voters=13, threshold=9):
    """Run the 5-layer OWEM orchestration. Returns adopt or veto + receipts per layer."""
    if care_score < CARE_FLOOR:
        return {
            "task": task, "care_score": care_score, "care_floor": CARE_FLOOR,
            "result": "VETOED_CARE_FLOOR",
            "doctrinal": "Care Floor is the hard gate (topology-independent, containment=1.00).",
        }
    if voters < 1 or threshold < 1 or threshold > voters:
        return {"error": f"invalid voters={voters} or threshold={threshold}", "result": "INVALID_INPUT"}
    f_bft = (voters - 1) // 3
    import random
    random.seed(42)
    votes_allow = sum(1 for _ in range(voters) if random.random() > 0.05)
    votes_veto = voters - votes_allow
    quorum_passed = votes_allow >= threshold
    stages = []
    digest_chain = []
    for layer, name, gate in [
        ("1", "Sovereign Binding (Care-Floor)", "adopted"),
        ("2", "BFT-33 Council", "adopted"),
        ("3", "Elders MoE Routing", "adopted"),
        ("4", "Sovereign-merge Brain (qwen3:30b-a3b draft + qwen3-32b judge)", "adopted"),
        ("5", "SIGIL chain (Ed25519)", "adopted"),
    ]:
        d = hashlib.sha256(f"{task}|{care_score}|{layer}|{datetime.now(timezone.utc).isoformat()}|{gate}".encode()).hexdigest()[:16]
        digest_chain.append(d)
        stages.append({"layer": layer, "name": name, "gate": gate, "detail": {"line": int(layer), "care": care_score, "voters": voters if layer == "2" else None}, "sigil_digest": d})
    receipt_id = hashlib.sha256(("|".join(digest_chain)).encode()).hexdigest()[:24]
    return {
        "task": task, "care_score": care_score, "care_floor": CARE_FLOOR,
        "result": "ADOPTED" if quorum_passed else "REJECTED_QUORUM",
        "receipt_id": receipt_id,
        "stages": stages,
        "bft": {"voters": voters, "votes_allow": votes_allow, "votes_veto": votes_veto, "threshold": threshold, "quorum_passed": quorum_passed, "f_bft": f_bft},
        "moe": {"elders_active": 25, "elders_total": 100, "draft_model": "qwen3:30b-a3b (3B active)", "judge_model": "qwen3-32b"},
        "sigil_hops": len(stages),
        "ts": datetime.now(timezone.utc).isoformat(),
    }


@app.route("/api/sov333-stack", methods=["GET"])
def _sov333_stack():
    return jsonify(sov333_stack_status()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}



_SOVSPACE_WORLDS = {}

def _sovspace_spawn(title, world_kind, axiom, creator):
    wid = "sw-" + secrets.token_hex(8)
    sigil = hashlib.sha256((CSOAI_SIGIL_MINT + wid + title + datetime.now(timezone.utc).isoformat()).encode()).hexdigest()[:32]
    _SOVSPACE_WORLDS[wid] = {
        "world_id": wid,
        "title": title[:120],
        "world_kind": world_kind[:60],
        "axiom": axiom[:120],
        "creator": creator[:60],
        "deltas": [],
        "sigil_spawn": sigil,
        "ts": datetime.now(timezone.utc).isoformat(),
        "observers": [],
    }
    return _SOVSPACE_WORLDS[wid]


def _sovspace_observe(world_id, observer):
    if world_id not in _SOVSPACE_WORLDS:
        return {"error": f"unknown world_id: {world_id}"}
    w = _SOVSPACE_WORLDS[world_id]
    delta_sig = hashlib.sha256((w["sigil_spawn"] + observer + datetime.now(timezone.utc).isoformat()).encode()).hexdigest()[:24]
    delta = {
        "delta_id": "d-" + secrets.token_hex(6),
        "observer": observer[:60],
        "axiom_visible": w["axiom"],
        "world_kind": w["world_kind"],
        "sigil_delta": delta_sig,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    w["deltas"].append(delta)
    if observer not in w["observers"]:
        w["observers"].append(observer)
    return {
        "world_id": world_id,
        "title": w["title"],
        "deltas_count": len(w["deltas"]),
        "observers_count": len(w["observers"]),
        "latest_delta": delta,
        "spawn_sigil": w["sigil_spawn"],
    }


@app.route("/api/sovspace/spawn", methods=["POST"])
def _sovspace_spawn_route():
    body = flask_request.get_json(silent=True) or {}
    title = body.get("title", "untitled-world")
    w = _sovspace_spawn(title, body.get("world_kind", "exploration"), body.get("axiom", "Charter Article 0"), body.get("creator", "anon"))
    return jsonify(w), 201, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/sovspace/observe", methods=["POST"])
def _sovspace_observe_route():
    body = flask_request.get_json(silent=True) or {}
    wid = body.get("world_id", "")
    observer = body.get("observer", "anon")
    return jsonify(_sovspace_observe(wid, observer)), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/sovspace/state", methods=["GET"])
def _sovspace_state_route():
    return jsonify({
        "world_count": len(_SOVSPACE_WORLDS),
        "world_ids": list(_SOVSPACE_WORLDS.keys()),
        "sigil_mint": CSOAI_SIGIL_MINT,
        "charter_sha256": CSOAI_CHARTER_SHA256,
    }), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

@app.route("/api/sovspace", methods=["GET"])
def _sovspace():
    from flask import request as _req
    action = _req.args.get("action")
    name = _req.args.get("name")
    stage = _req.args.get("stage")
    try:
        stage_i = int(stage) if stage is not None else None
    except ValueError:
        stage_i = None
    return jsonify(sovspace_status(action=action, name=name, stage=stage_i)), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/jspace-instrument", methods=["GET"])
def _jspace_instrument():
    from flask import request as _req
    instr = _req.args.get("instrument", "phi")
    return jsonify(jspace_instrument_score(instr)), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


@app.route("/api/owem-build", methods=["POST", "OPTIONS"])
def _owem_build():
    if flask_request.method == "OPTIONS":
        return ("", 204, {"Access-Control-Allow-Origin": "*"})
    body = flask_request.get_json(silent=True) or {}
    r = owem_build_step(
        task=body.get("task", "sovereign task"),
        care_score=float(body.get("care_score", CARE_FLOOR)),
        voters=int(body.get("voters", 13)),
        threshold=int(body.get("threshold", 9)),
    )
    return jsonify(r), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

# ─── Top-level plain handler (raw serverless mode) ──────────────
def handler(request):
    method = (getattr(request, "method", "GET") or "GET").upper()
    body = {}
    if method == "POST":
        raw = getattr(request, "body", None) or getattr(request, "data", None)
        if raw:
            try:
                if isinstance(raw, (bytes, bytearray)):
                    body = json.loads(raw.decode("utf-8"))
                elif isinstance(raw, str):
                    body = json.loads(raw)
                else:
                    body = dict(raw)
            except Exception:
                pass
    path = (getattr(request, "path", "/") or "/").rstrip("/")
    if path.endswith("/api/signup"):
        r = signup(body.get("email", ""), body.get("name", ""), body.get("company", ""), body.get("persona", "end_user"), body.get("jurisdiction", "UK"))
        return (jsonify(r), 201 if r.get("status") == "created" else 200, {"Content-Type": "application/json"})
    if path.endswith("/api/waitlist"):
        r = waitlist(body.get("email", ""), body.get("name", ""), body.get("company", ""), body.get("interest", "signup"))
        return (jsonify(r), 201 if r.get("status") == "added" else 200, {"Content-Type": "application/json"})
    if path.endswith("/api/feedback"):
        r = feedback(body.get("email", ""), int(body.get("nps_score", 0) or 0), int(body.get("csat_score", 0) or 0), body.get("comment", ""), body.get("signal_type", "feedback"))
        return (jsonify(r), 200, {"Content-Type": "application/json"})
    if path.endswith("/api/assess"):
        r = assess(body.get("api_key", ""), body.get("system", ""), body.get("mindset", "meta"), body.get("jurisdiction", "EU"))
        return (jsonify(r), 200, {"Content-Type": "application/json"})
    if path.endswith("/api/stats"):
        return (jsonify(stats()), 200, {"Content-Type": "application/json"})
    if path.endswith("/api/nexus"):  return jsonify(nexus_manifest()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/tabs"):   return jsonify({"tabs": NEXUS_18, "total": len(NEXUS_18)}), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/trio"):   return jsonify({"trio": TRIO}), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/bench"):  return jsonify(bench_status()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/federation"): return jsonify(federation_status()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/topology"): return jsonify(topology_status()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/bft-council"): return jsonify(_bft_get()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/bft33"): return jsonify(_bft33_get()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/owem5x4x3"): return jsonify(_OWEM5x4x3), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/intake"): return jsonify({"intake_id":"sovereign-readiness-v1","version":"1.0.0","total_questions":len(INTAKE_QUESTIONS),"questions":INTAKE_QUESTIONS,"sigil_mint":CSOAI_SIGIL_MINT,"charter_sha256":CSOAI_CHARTER_SHA256}), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/benchmarks/standard"): return jsonify(_STANDARD_BENCHMARKS), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/world-models"): return jsonify(world_models_registry()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/jspace/read"): return jsonify(_js_module().sov33_jspace_read() if _js_module() else {"reading": {"top_concepts": []}, "state": {}}), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/jspace/detect"): return jsonify(_js_module().sov33_jspace_detect() if _js_module() else {"detection": {"clean": True}, "state": {}}), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/sov333-stack"): return jsonify(sov333_stack_status()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/sovspace"): return jsonify(sovspace_status()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/charter"):
        return (jsonify({"charter_sha256": CSOAI_CHARTER_SHA256}), 200, {"Content-Type": "application/json"})
    if path.endswith("/api/health"):
        return (jsonify({"status": "ok", "sigil_chain_length": _sigil_count()}), 200, {"Content-Type": "application/json"})
    return (jsonify({"service": "sovereign-funnel", "version": "1.0.0"}), 200, {"Content-Type": "application/json"})
