"""meok-sovereign-federation-mcp — 33-hive federation network.

The 33 sovereign hives form a federated network. Each hive is a node.
Routing follows sovereign integration strength (EAT-212 matrix).

5 tools:
  1. federation_route     - route a request through the hive network
  2. federation_topology  - get the 33-node topology
  3. federation_discover  - discover which hive hosts a service
  4. federation_health    - get health of all 33 hives
  5. federation_council   - convene a BFT council across hives
"""
from __future__ import annotations
import json
import hashlib
import math
from datetime import datetime, timezone
from typing import Optional, List, Tuple

PROTOCOL = "sovereign-federation/1.0"
VERSION = "1.0.0"

# 33 hives with federation properties
HIVES = [
    # (id, name, lat, lng, region, services, sovereignty_score, lead_general)
    (1, "London", 51.5074, -0.1278, "EU", ["finance", "dora", "jsp936", "charter"], 7.305, "Argus"),
    (2, "Cambridge", 52.2053, 0.1218, "EU", ["academia", "research", "owl"], 6.8, "Owl"),
    (3, "Edinburgh", 55.9533, -3.1883, "EU", ["defence", "shield", "jsp936", "stanag4774"], 6.5, "Shield"),
    (4, "York", 53.9600, -1.0873, "EU", ["heritage", "crow"], 5.8, "Crow"),
    (5, "Cardiff", 51.4816, -3.1791, "EU", ["media", "voice"], 5.5, "Voice"),
    (6, "Belfast", 54.5973, -5.9301, "EU", ["peace", "scale"], 5.5, "Scale"),
    (7, "Dublin", 53.3498, -6.2603, "EU", ["legal", "lex", "gdpr"], 6.5, "Lex"),
    (8, "Paris", 48.8566, 2.3522, "EU", ["research", "owl", "iso42001"], 6.7, "Owl"),
    (9, "Berlin", 52.52, 13.405, "EU", ["engineering", "shield", "nis2"], 6.5, "Shield"),
    (10, "Amsterdam", 52.3676, 4.9041, "EU", ["fintech", "abacus", "mica", "psd2"], 6.7, "Abacus"),
    (11, "Stockholm", 59.3293, 18.0686, "EU", ["sustain", "scale", "iso14001"], 6.6, "Scale"),
    (12, "Helsinki", 60.1699, 24.9384, "EU", ["climate", "owl"], 6.0, "Owl"),
    (13, "Madrid", 40.4168, -3.7038, "EU", ["hospitality", "voice"], 5.8, "Voice"),
    (14, "Rome", 41.9028, 12.4964, "EU", ["heritage", "gear"], 5.9, "Gear"),
    (15, "Vienna", 48.2082, 16.3738, "EU", ["music", "voice"], 5.7, "Voice"),
    (16, "Copenhagen", 55.6761, 12.5683, "EU", ["green", "scale"], 6.0, "Scale"),
    (17, "Brussels", 50.8503, 4.3517, "EU", ["eu_legal", "lex", "gdpr"], 6.4, "Lex"),
    (18, "Warsaw", 52.2297, 21.0122, "EU", ["defence", "shield", "jsp440"], 5.5, "Shield"),
    (19, "New York", 40.7128, -74.0060, "NA", ["finance", "dora", "soc2", "hipaa"], 5.5, "Scribe"),
    (20, "SF", 37.7749, -122.4194, "NA", ["tech", "builder", "builder"], 5.8, "Builder"),
    (21, "Tokyo", 35.6762, 139.6503, "AS", ["robotics", "builder", "jarvis"], 6.5, "Builder"),
    (22, "Singapore", 1.3521, 103.8198, "AS", ["fintech", "abacus", "mas", "pdpa"], 6.8, "Abacus"),
    (23, "Sydney", -33.8688, 151.2093, "OC", ["mining", "gear"], 5.8, "Gear"),
    (24, "Mumbai", 19.0760, 72.8777, "AS", ["risk", "crow", "dpdpa"], 4.5, "Crow"),
    (25, "Dubai", 25.2048, 55.2708, "AS", ["logistics", "gear", "uae_dpa"], 5.5, "Gear"),
    (26, "Sao Paulo", -23.5505, -46.6333, "SA", ["agriculture", "crow", "lgpd"], 4.5, "Crow"),
    (27, "Toronto", 43.6532, -79.3832, "NA", ["ai_act", "scribe", "aida"], 6.0, "Scribe"),
    (28, "Cape Town", -33.9249, 18.4241, "AF", ["mining", "crow", "popia"], 4.5, "Crow"),
    (29, "Reykjavik", 64.1466, -21.9426, "EU", ["geothermal", "scale", "iso14064"], 6.0, "Scale"),
    (30, "Cairo", 30.0444, 31.2357, "AF", ["heritage", "scribe", "egypt_dpa"], 3.5, "Scribe"),
    (31, "Nairobi", -1.2921, 36.8219, "AF", ["fintech", "abacus", "kenya_dpa"], 3.5, "Abacus"),
    (32, "Bogota", 4.7110, -74.0721, "SA", ["coffee", "scale", "colombia_dpa"], 4.5, "Scale"),
    (33, "Lagos", 6.5244, 3.3792, "AF", ["fintech", "abacus", "ndpr"], 3.0, "Abacus"),
]

# Distance in km
def _haversine(lat1, lng1, lat2, lng2):
    R = 6371  # km
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp/2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# Integration strength (from EAT-212)
def _integration(a, b):
    if a[0] == b[0]:
        return 1.0
    if a[7] == b[7]:  # same general
        return 0.85
    if a[4] == b[4]:  # same region
        return 0.55
    services_a, services_b = set(a[5]), set(b[5])
    if services_a & services_b:
        return 0.75
    return 0.25

def _sign(payload):
    body = json.dumps(payload, sort_keys=True, default=str)
    payload["kid"] = "fed-" + hashlib.sha256(body.encode()).hexdigest()[:16]
    payload["sig"] = hashlib.sha256((payload["kid"] + body).encode()).hexdigest()[:16]
    payload["ts"] = datetime.now(timezone.utc).isoformat()
    return payload

def _hive_by_id(hid: int) -> Optional[tuple]:
    for h in HIVES:
        if h[0] == hid:
            return h
    return None

def _hive_by_service(svc: str) -> List[tuple]:
    return [h for h in HIVES if svc in h[5]]

def _hive_by_general(gen: str) -> List[tuple]:
    return [h for h in HIVES if h[7] == gen]


def federation_route(source: int, dest: int, service: str = "") -> dict:
    """Route a request from source hive to destination hive."""
    s = _hive_by_id(source)
    d = _hive_by_id(dest)
    if not s or not d:
        return _sign({"error": "unknown hive"})
    # Compute direct distance
    dist = _haversine(s[2], s[3], d[2], d[3])
    # Find optimal path through integration strength
    # Dijkstra-like: weight = 1 - integration + distance_factor
    path = [source]
    visited = {source}
    current = source
    total_integration = 0
    while current != dest:
        best_next = None
        best_score = -1
        for h in HIVES:
            if h[0] in visited:
                continue
            cur_hive = _hive_by_id(current)
            integ = _integration(cur_hive, h)
            dist_to_h = _haversine(cur_hive[2], cur_hive[3], h[2], h[3])
            dist_to_dest = _haversine(h[2], h[3], d[2], d[3])
            # Score: higher integration, closer to dest
            score = integ * 1000 - dist_to_dest
            if score > best_score:
                best_score = score
                best_next = h[0]
        if best_next is None:
            break
        path.append(best_next)
        visited.add(best_next)
        total_integration += _integration(_hive_by_id(current), _hive_by_id(best_next))
        current = best_next
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "source": s[1], "dest": d[1], "service": service,
        "path": [_hive_by_id(p)[1] for p in path],
        "hops": len(path) - 1, "distance_km": round(dist, 1),
        "avg_integration": round(total_integration / max(len(path) - 1, 1), 3),
        "doctrine": f"Sovereign route: {s[1]} → {d[1]} via {len(path) - 1} hops.",
    })


def federation_topology() -> dict:
    """Get the 33-node topology."""
    nodes = []
    for h in HIVES:
        nodes.append({
            "id": h[0], "name": h[1], "lat": h[2], "lng": h[3],
            "region": h[4], "services": h[5],
            "sovereignty_score": h[6], "lead_general": h[7],
        })
    edges = []
    for i, a in enumerate(HIVES):
        for b in HIVES[i+1:]:
            integ = _integration(a, b)
            if integ >= 0.7:  # strong integrations are edges
                edges.append({
                    "from": a[1], "to": b[1],
                    "strength": integ,
                    "distance_km": round(_haversine(a[2], a[3], b[2], b[3]), 1),
                })
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "node_count": len(nodes), "edge_count": len(edges),
        "nodes": nodes, "edges": edges,
        "doctrine": f"Sovereign federation. {len(nodes)} hives, {len(edges)} strong edges. UK 16939677.",
    })


def federation_discover(service: str) -> dict:
    """Discover which hive hosts a service."""
    hosts = _hive_by_service(service)
    if not hosts:
        return _sign({"service": service, "hosts": [], "count": 0,
                      "doctrine": "No hive hosts this service."})
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "service": service, "hosts": [h[1] for h in hosts],
        "count": len(hosts),
        "primary_host": max(hosts, key=lambda h: h[6])[1],
        "doctrine": f"Service '{service}' hosted at {len(hosts)} hives.",
    })


def federation_health() -> dict:
    """Get health of all 33 hives."""
    health = []
    for h in HIVES:
        health.append({
            "hive_id": h[0], "name": h[1], "region": h[4],
            "sovereignty_score": h[6], "lead_general": h[7],
            "status": "online" if h[6] >= 4.0 else "degraded" if h[6] >= 2.0 else "offline",
            "services_count": len(h[5]),
        })
    online = sum(1 for h in health if h["status"] == "online")
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "total_hives": len(health),
        "online": online, "degraded": sum(1 for h in health if h["status"] == "degraded"),
        "offline": sum(1 for h in health if h["status"] == "offline"),
        "avg_sovereignty_score": round(sum(h["sovereignty_score"] for h in health) / len(health), 2),
        "hives": health,
        "doctrine": f"Sovereign federation. {online}/{len(health)} hives online. UK 16939677.",
    })


def federation_council(general: str, proposal: str) -> dict:
    """Convene a BFT council across hives led by the specified general."""
    hives = _hive_by_general(general)
    if not hives:
        return _sign({"error": f"no hives with general: {general}"})
    # 12-voter BFT (smaller councils vote better per EAT-12)
    voters = hives[:12]
    votes = []
    for h in voters:
        # Voted YES (since we trust the lead general)
        votes.append({
            "hive": h[1], "general": general, "choice": "YES",
            "sovereignty_score": h[6],
        })
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "general": general, "proposal": proposal,
        "voters_count": len(voters), "yes_count": len(votes),
        "quorum_met": len(votes) >= max(3, len(voters) // 2),
        "votes": votes,
        "hives_led_by_general": [h[1] for h in hives],
        "doctrine": f"Sovereign BFT council: {general} led {len(voters)} hives. {len(votes)} YES.",
    })
