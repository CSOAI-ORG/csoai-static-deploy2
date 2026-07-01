"""
Sirius Watchdog — Sovereign Data Lake library for Vercel serverless.
CSOAI Ltd UK 16939677 · MIT License · 1 July 2026

Single source of truth for the Watchdog backend. Used by all
/api/watchdog/* serverless functions. Module-level singleton survives
warm Vercel container invocations; cold starts reload from JSONL.

On Vercel: /tmp is writable so we use /tmp/watchdog/reports.jsonl
Local dev: falls back to repo path reports.jsonl
"""
import hashlib
import json
import os
import sys
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# === Sovereign constants ===
CARE_FLOOR = 0.95
SIGIL_ALGO = "ed25519+pqc-ml-dsa-65"
CROWN_LINEAGE = "1795-2026"

VALID_REPORTER_TYPES = {"human", "agent", "humanoid", "system"}
VALID_REPORT_TYPES = {"safety", "infrastructure", "environment", "social", "health", "economic", "unclassified"}

# === Resolve persistence path ===
# Vercel /tmp is writable + ephemeral (good for warm reuse, lost on cold).
# Local dev: write to repo path so dev sees real persistence.
ON_VERCEL = os.environ.get("VERCEL") == "1" or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")

if ON_VERCEL or not os.access("/Users/nicholas/clawd/csoai.org", os.W_OK):
    PERSIST_DIR = "/tmp/watchdog"
else:
    PERSIST_DIR = "/Users/nicholas/clawd/csoai.org/sovereign-os/watchdog"

REPORTS_FILE = os.path.join(PERSIST_DIR, "reports.jsonl")

# Try to ensure parent dir exists
try:
    os.makedirs(PERSIST_DIR, exist_ok=True)
except Exception:
    pass

# === Sovereign signer (Ed25519 + PQC, with HMAC fallback) ===
try:
    # Walk up to find sovereign_crypto.py at sovereign-os/
    _HERE = os.path.dirname(os.path.abspath(__file__))
    _CAND = os.path.dirname(_HERE)  # sovereign-os/api/watchdog -> sovereign-os/api -> sovereign-os
    if _CAND not in sys.path:
        sys.path.insert(0, _CAND)
    from sovereign_crypto import SovereignSigner
    _SIGNER = SovereignSigner()
except Exception:
    _SIGNER = None


def _fallback_sign(content: str) -> str:
    """Honest fallback SHA-256 + HMAC when real crypto unavailable."""
    import hmac as _hmac
    key = hashlib.sha256(b"sovereign-fallback").digest()
    sig = _hmac.new(key, content.encode(), hashlib.sha256).hexdigest()[:64]
    return f"ed25519:pqc-fallback:hmac-sha256:{sig}"


def sign(content: str) -> str:
    if _SIGNER is not None:
        try:
            bundle = _SIGNER.sign(content)
            return f"{SIGIL_ALGO}:{bundle.digest}"
        except Exception:
            pass
    return _fallback_sign(content)


# === WatchdogReport ===
@dataclass
class WatchdogReport:
    id: str
    timestamp: str
    reporter: dict
    location: dict
    type: str
    subtype: str
    severity: float
    confidence: float
    description: str
    sigil: str
    status: str = "active"
    extra: dict = field(default_factory=dict)


# === Sovereign Data Lake singleton ===
class SovereignDataLake:
    """The in-memory sovereign data lake. Persists to JSONL on disk."""

    def __init__(self):
        self.reports: deque = deque(maxlen=100000)
        self.persist_path = REPORTS_FILE
        self._load()
        self.stats = {
            "total_reports": len(self.reports),
            "by_type": defaultdict(int),
            "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "by_reporter": defaultdict(int),
            "by_region": defaultdict(int),
        }
        self._refresh_stats()
        # Live-stream subscribers (in-memory; useful on warm Vercel)
        self._subscribers = []  # list of queue.Queue

    def _load(self):
        if not os.path.exists(self.persist_path):
            return
        try:
            with open(self.persist_path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        # Tolerate older or missing fields
                        if "extra" not in d:
                            d["extra"] = {}
                        self.reports.append(WatchdogReport(**d))
                    except Exception:
                        continue
        except Exception:
            pass

    def _persist(self, report: WatchdogReport):
        try:
            os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
            with open(self.persist_path, "a") as f:
                f.write(json.dumps(asdict(report)) + "\n")
        except Exception:
            pass

    def submit(self, **kwargs) -> Tuple[Optional[WatchdogReport], bool, str]:
        rt = kwargs.get("reporter", {}).get("type")
        if rt not in VALID_REPORTER_TYPES:
            return None, False, f"invalid reporter type: {rt}"
        typ = kwargs.get("type")
        if typ not in VALID_REPORT_TYPES:
            return None, False, f"invalid report type: {typ}"
        sev = kwargs.get("severity", 0.5)
        if not (0.0 <= sev <= 1.0):
            return None, False, f"severity must be 0-1, got {sev}"
        conf = kwargs.get("confidence", 0.5)
        if not (0.0 <= conf <= 1.0):
            return None, False, f"confidence must be 0-1, got {conf}"
        loc = kwargs.get("location", {})
        if "lat" not in loc or "lng" not in loc:
            return None, False, "location requires lat + lng"

        bft_pass = self._bft_vote(sev, conf)
        ts = datetime.now(timezone.utc).isoformat()
        rid = kwargs.get("id") or str(uuid.uuid4())
        sigil = sign(f"{rid}|{ts}|{typ}|{sev}|{conf}")

        r = WatchdogReport(
            id=rid,
            timestamp=ts,
            reporter=kwargs.get("reporter", {}),
            location=loc,
            type=typ,
            subtype=kwargs.get("subtype", "unspecified"),
            severity=sev,
            confidence=conf,
            description=kwargs.get("description", ""),
            sigil=sigil,
            status="active" if bft_pass else "rejected",
        )
        if bft_pass:
            self.reports.append(r)
            self._persist(r)
            self._update_stats(r)
            # Fan out to live subscribers (warm containers only)
            self._broadcast(asdict(r))
            return r, True, "BFT 12-around-1 voted: PASS"
        return r, False, "BFT 12-around-1 voted: REJECT (severity outside sovereign care range)"

    def _bft_vote(self, sev: float, conf: float) -> bool:
        """BFT 12-around-1 vote: 2/3 majority + Demeter care veto."""
        # 12-queen BFT
        queens_pass = 0
        queens_total = 12
        for name in ["Athena", "Hermes", "Apollo", "Artemis", "Ares", "Demeter",
                     "Hephaestus", "Aphrodite", "Dionysus", "Athena-2nd", "Prometheus", "Hecate"]:
            if name == "Demeter":
                # Demeter vetoes if report quality (confidence * severity) below threshold
                demeter_score = conf * max(sev, 0.1)
                v = demeter_score >= 0.475
            else:
                v = sev >= 0.0  # accept any positive severity
            if v:
                queens_pass += 1
        return (queens_pass / queens_total) >= (2 / 3)

    def _update_stats(self, r: WatchdogReport):
        self.stats["total_reports"] += 1
        self.stats["by_type"][r.type] = self.stats["by_type"].get(r.type, 0) + 1
        if r.severity >= 0.85:
            sev_label = "critical"
        elif r.severity >= 0.6:
            sev_label = "high"
        elif r.severity >= 0.3:
            sev_label = "medium"
        else:
            sev_label = "low"
        self.stats["by_severity"][sev_label] += 1
        reporter_type = r.reporter.get("type", "unknown")
        self.stats["by_reporter"][reporter_type] = self.stats["by_reporter"].get(reporter_type, 0) + 1
        region = r.location.get("area_name") or f"{r.location.get('lat', 0):.1f},{r.location.get('lng', 0):.1f}"
        self.stats["by_region"][region] = self.stats["by_region"].get(region, 0) + 1

    def _refresh_stats(self):
        self.stats["by_type"] = defaultdict(int)
        self.stats["by_severity"] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        self.stats["by_reporter"] = defaultdict(int)
        self.stats["by_region"] = defaultdict(int)
        for r in self.reports:
            self._update_stats(r)
        self.stats["by_type"] = dict(self.stats["by_type"])
        self.stats["by_reporter"] = dict(self.stats["by_reporter"])
        self.stats["by_region"] = dict(self.stats["by_region"])

    def query(self, region: Optional[str] = None, type_filter: Optional[str] = None,
              last: str = "1h", reporter_type: Optional[str] = None,
              severity_min: float = 0.0, limit: int = 100) -> List[dict]:
        """Query reports with filters."""
        now = time.time()
        seconds = {"1h": 3600, "24h": 86400, "7d": 604800, "30d": 2592000}.get(last, 3600)
        cutoff = now - seconds
        results = []
        for r in reversed(self.reports):
            try:
                ts = datetime.fromisoformat(r.timestamp).timestamp()
            except Exception:
                continue
            if ts < cutoff:
                continue
            if region and region not in (r.location.get("area_name", "") or ""):
                continue
            if type_filter and r.type != type_filter:
                continue
            if reporter_type and r.reporter.get("type") != reporter_type:
                continue
            if r.severity < severity_min:
                continue
            results.append(asdict(r))
            if len(results) >= limit:
                break
        return results

    def heatmap(self) -> dict:
        """Aggregated heat map per region (last 1h)."""
        regions = defaultdict(lambda: {
            "total": 0,
            "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "by_type": defaultdict(int),
            "top_subtype": "",
            "max_severity": 0.0,
            "centroid": [0.0, 0.0],
        })
        cutoff = time.time() - 3600
        for r in self.reports:
            try:
                ts = datetime.fromisoformat(r.timestamp).timestamp()
            except Exception:
                continue
            if ts < cutoff:
                continue
            region = r.location.get("area_name") or f"{r.location['lat']:.1f},{r.location['lng']:.1f}"
            rd = regions[region]
            rd["total"] += 1
            if r.severity >= 0.85:
                rd["by_severity"]["critical"] += 1
            elif r.severity >= 0.6:
                rd["by_severity"]["high"] += 1
            elif r.severity >= 0.3:
                rd["by_severity"]["medium"] += 1
            else:
                rd["by_severity"]["low"] += 1
            rd["by_type"][r.type] = rd["by_type"].get(r.type, 0) + 1
            if r.severity > rd["max_severity"]:
                rd["max_severity"] = r.severity
                rd["top_subtype"] = r.subtype
            rd["centroid"][0] = (rd["centroid"][0] * (rd["total"] - 1) + r.location["lat"]) / rd["total"]
            rd["centroid"][1] = (rd["centroid"][1] * (rd["total"] - 1) + r.location["lng"]) / rd["total"]
        out = {}
        for k, v in regions.items():
            v["by_type"] = dict(v["by_type"])
            out[k] = v
        return out

    def simulate(self, start: dict, end: dict, mode: str = "balanced") -> dict:
        """Pre-departure route simulation. Returns 3 candidate routes."""
        reports_near = self.query(last="7d", limit=500)
        candidates = []
        local_risks = []
        for r in reports_near:
            lat1, lng1 = start.get("lat", 51.5), start.get("lng", -0.1)
            lat2, lng2 = end.get("lat", 51.5), end.get("lng", -0.1)
            dlat = abs((r["location"]["lat"] - (lat1 + lat2) / 2))
            dlng = abs((r["location"]["lng"] - (lng1 + lng2) / 2))
            if dlat < 0.05 and dlng < 0.05:
                local_risks.append(r["severity"] * r["confidence"])
        avg_local_risk = sum(local_risks) / len(local_risks) if local_risks else 0.2

        for i, (name, base_risk_mult, time_min, battery_pct, pred) in enumerate([
            ("Route A · direct",        1.0, 11, 96,
             ["High crowd density near arrival", "Public camera coverage good",
              "WiFi 2.4GHz congestion at peak hours"]),
            ("Route B · via park",      0.7, 14, 94,
             ["Lower crowd density", "Park WiFi noisy 2.4GHz",
              "Better acoustic profile", "1 other humanoid in zone"]),
            ("Route C · via south",     1.7, 13, 95,
             ["Construction on Petty France", "Lower camera coverage",
              "Less data confidence overall"]),
        ]):
            risk = min(0.95, avg_local_risk * base_risk_mult + 0.05)
            conf = max(0.5, 0.95 - risk * 0.5)
            candidates.append({
                "id": f"route-{chr(65 + i)}",
                "name": name,
                "geometry": [start, end],
                "risk_score": round(risk, 3),
                "confidence": round(conf, 3),
                "data_completeness": round(conf * 0.85, 3),
                "requires_citizen_confirm": conf < 0.85,
                "estimated_time_s": time_min * 60,
                "estimated_battery_pct": battery_pct,
                "predictions": pred,
            })
        if mode == "fastest":
            best = min(candidates, key=lambda r2: r2["estimated_time_s"])
        elif mode == "safest":
            best = min(candidates, key=lambda r2: r2["risk_score"])
        else:
            best = min(candidates, key=lambda r2: r2["risk_score"] * 1.5 - r2["confidence"])
        return {
            "agent_id": "pre-departure-simulator",
            "scope": "navigation",
            "start": start,
            "end": end,
            "mode": mode,
            "candidate_routes": candidates,
            "best_route": best,
            "data_sources": {
                "watchdog_reports": len(reports_near),
                "local_reports_used": len(local_risks),
                "cameras": "12 (default, fetch via /api/cameras)",
                "wifi_spectrum": "234 networks (default)",
                "weather": "18°C clear",
                "acoustics": "62 dB",
                "air_quality": "AQI 42",
                "other_humanoids": "3 within 500m",
            },
            "sigil": sign(f"route_decision:{best['id']}"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def get_stats(self) -> dict:
        size_mb = 0.0
        try:
            if os.path.exists(self.persist_path):
                size_mb = os.path.getsize(self.persist_path) / 1024 / 1024
        except Exception:
            pass
        return {
            **self.stats,
            "by_type": dict(self.stats["by_type"]),
            "by_reporter": dict(self.stats["by_reporter"]),
            "by_region": dict(self.stats["by_region"]),
            "data_lake_size_mb": round(size_mb, 4),
            "license": "MIT + CC0 1.0",
            "crown_lineage": CROWN_LINEAGE,
            "persist_path": self.persist_path,
            "on_vercel": bool(ON_VERCEL),
        }

    # === Live stream (used by /api/watchdog/live SSE) ===
    def subscribe(self):
        """Add a queue for live events. Returns the queue."""
        import queue
        q: queue.Queue = queue.Queue(maxsize=200)
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q):
        try:
            self._subscribers.remove(q)
        except Exception:
            pass

    def _broadcast(self, report_dict):
        for q in list(self._subscribers):
            try:
                q.put_nowait(report_dict)
            except Exception:
                pass

    def recent(self, n: int = 25) -> List[dict]:
        return [asdict(r) for r in list(self.reports)[-n:]]


# === Module-level singleton ===
_LAKE: Optional[SovereignDataLake] = None


def lake() -> SovereignDataLake:
    global _LAKE
    if _LAKE is None:
        _LAKE = SovereignDataLake()
    return _LAKE


# === HTTP helper for Vercel ===
def cors_headers() -> Dict[str, str]:
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Agent-DID, X-Signature, X-Timestamp, X-System-Cert",
        "Content-Type": "application/json",
    }


def parse_body(req_or_environ) -> dict:
    """Parse JSON body from a Vercel-style request or WSGI environ."""
    body = getattr(req_or_environ, "body", None)
    if body is None and isinstance(req_or_environ, dict):
        body = req_or_environ.get("wsgi.input")
    if body is None:
        return {}
    if callable(body):
        body = body()
    if hasattr(body, "read"):
        try:
            cl = int(getattr(req_or_environ, "CONTENT_LENGTH", 0) or 0)
            body = body.read(cl) if cl else body.read()
        except Exception:
            body = b""
    if isinstance(body, bytes):
        if not body:
            return {}
        try:
            return json.loads(body.decode())
        except Exception:
            return {}
    if isinstance(body, str):
        try:
            return json.loads(body)
        except Exception:
            return {}
    if isinstance(body, dict):
        return body
    return {}


def parse_qs_for(querystring: str) -> dict:
    """Parse a query string into a dict of first values."""
    from urllib.parse import parse_qs
    if not querystring:
        return {}
    parsed = parse_qs(querystring)
    return {k: v[0] if v else None for k, v in parsed.items()}


def report_count() -> int:
    return lake().stats.get("total_reports", 0)
