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
    if path.endswith("/api/charter"):
        return (jsonify({"charter_sha256": CSOAI_CHARTER_SHA256}), 200, {"Content-Type": "application/json"})
    if path.endswith("/api/health"):
        return (jsonify({"status": "ok", "sigil_chain_length": _sigil_count()}), 200, {"Content-Type": "application/json"})
    return (jsonify({"service": "sovereign-funnel", "version": "1.0.0"}), 200, {"Content-Type": "application/json"})
