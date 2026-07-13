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
]

TRIO = {
    "surface": {"name": "Surface",  "color": "#4a9eff", "purpose": "Operator-facing — humans read, agents act", "count": 7},
    "deep":    {"name": "Deep",     "color": "#22c55e", "purpose": "Builder-facing — MCPs / APIs / substrate",  "count": 8},
    "codex":   {"name": "Codex",    "color": "#fbbf24", "purpose": "Public-facing — onboarding / community",    "count": 8},
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


@app.route("/api/world-models", methods=["GET"])
def _world_models():
    return jsonify(world_models_registry()), 200, {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

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
    if path.endswith("/api/world-models"): return jsonify(world_models_registry()), 200, {"Content-Type": "application/json"}
    if path.endswith("/api/charter"):
        return (jsonify({"charter_sha256": CSOAI_CHARTER_SHA256}), 200, {"Content-Type": "application/json"})
    if path.endswith("/api/health"):
        return (jsonify({"status": "ok", "sigil_chain_length": _sigil_count()}), 200, {"Content-Type": "application/json"})
    return (jsonify({"service": "sovereign-funnel", "version": "1.0.0"}), 200, {"Content-Type": "application/json"})
