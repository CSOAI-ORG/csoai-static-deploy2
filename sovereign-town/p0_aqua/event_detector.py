#!/usr/bin/env python3
"""
Event detector for Sovereign Town auto-distribution.

Scans fleet status, simulation state, ledger tail, and moat files for
notable highlights, breakthroughs, and milestones. Emits a normalized
`DetectedEvent` dict that the content factory can turn into social posts
and short videos.

The detector is stateful: it reads a small state file so it only emits an
event once per threshold crossing.
"""
from __future__ import annotations
import json
import os
import pathlib
import time
from dataclasses import dataclass, asdict
from typing import Any

P0 = pathlib.Path(__file__).parent
PUBLIC = P0.parent.parent / "proofof-site" / "sovereign-town"
STATE_PATH = P0 / "distribution_state.json"
_LEGACY_STATE_PATH = P0 / "distribution_events_state.json"


@dataclass(frozen=True)
class DetectedEvent:
    id: str
    timestamp: str
    event_type: str
    severity: str  # info | highlight | breakthrough | milestone
    title: str
    body: str
    metrics: dict[str, Any]
    suggested_visual: str  # filename or description
    hashtags: list[str]


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load_state() -> dict:
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"emitted": {}, "last_run": None}


def _save_state(state: dict) -> None:
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def _already_emitted(state: dict, key: str) -> bool:
    return key in state.get("emitted", {})


def _mark_emitted(state: dict, key: str) -> None:
    state.setdefault("emitted", {})[key] = _now()


def _load_json(path: pathlib.Path, default: Any = None) -> Any:
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def _migrate_legacy_state() -> None:
    """Copy emitted keys from pre-unification state file so events are not re-emitted."""
    if STATE_PATH.exists() or not _LEGACY_STATE_PATH.exists():
        return
    try:
        with open(_LEGACY_STATE_PATH) as f:
            legacy = json.load(f)
        merged = {
            "emitted": dict(legacy.get("emitted", {})),
            "last_run": legacy.get("last_run"),
        }
        with open(STATE_PATH, "w") as f:
            json.dump(merged, f, indent=2)
    except Exception as e:
        print(f"[event_detector] legacy state migration failed: {e}")


def _episode_milestone(state: dict) -> DetectedEvent | None:
    mac = _load_json(P0 / "fleet_status_mac.json", {})
    vm = _load_json(PUBLIC / "fleet_status_vm.json", {})
    total = (mac.get("cum_episodes", 0) or 0) + (vm.get("cum_episodes", 0) or 0)

    milestones = [100_000_000, 500_000_000, 1_000_000_000, 2_000_000_000, 5_000_000_000]
    for m in milestones:
        key = f"episodes_{m}"
        if total >= m and not _already_emitted(state, key):
            _mark_emitted(state, key)
            return DetectedEvent(
                id=key,
                timestamp=_now(),
                event_type="milestone",
                severity="milestone",
                title=f"Sovereign Town crossed {m:,} episodes",
                body=(
                    f"The governed-vs-ungoverned fleet just hit {m:,} Ed25519-attested episodes "
                    "across Mac and VM partitions. Every episode is hash-chained and reproducible."
                ),
                metrics={"cum_episodes": total, "mac": mac, "vm": vm},
                suggested_visual="town3d_demo.gif",
                hashtags=["SovereignTown", "AgentWorld", "AIRegistry", "ProofOfAI"],
            )
    return None


def _model_breakthrough(state: dict) -> DetectedEvent | None:
    models = _load_json(P0 / "moat_models.json", {}).get("models", {})
    if not models:
        return None
    best = None
    for key, m in models.items():
        if isinstance(m, dict) and m.get("test_acc"):
            if best is None or m["test_acc"] > best[1]:
                best = (key, m["test_acc"], m)
    if best is None:
        return None
    key, acc, meta = best
    # Emit once per accuracy threshold crossed.
    thresholds = [0.90, 0.95, 0.99]
    for t in thresholds:
        ekey = f"model_{key}_acc_{t}"
        if acc >= t and not _already_emitted(state, ekey):
            _mark_emitted(state, ekey)
            return DetectedEvent(
                id=ekey,
                timestamp=_now(),
                event_type="breakthrough",
                severity="breakthrough",
                title=f"{key}.ai threat model hit {acc*100:.1f}% accuracy",
                body=(
                    f"Hive {key}.ai trained a sovereign threat-detection model at {acc*100:.1f}% accuracy "
                    f"({meta.get('f1', 0):.3f} F1). Each hive eats its own industry; the model is part of the data moat."
                ),
                metrics={"hive": key, "test_acc": acc, "f1": meta.get("f1"), "features": meta.get("feature_count")},
                suggested_visual="town3d_screenshot.png",
                hashtags=["SovereignTown", "AIModels", "VerticalAI", "ThreatDetection"],
            )
    return None


def _town_crime_wave(state: dict) -> DetectedEvent | None:
    # We need a live town-state snapshot to detect crime spikes.
    try:
        import town_sim_live
        s = town_sim_live.snapshot("ungoverned")
    except Exception:
        return None
    crimes = s.get("crimes", 0)
    lawlessness = s.get("lawlessness", 0.0)
    key = "crime_wave_detected"
    if crimes >= 10 and lawlessness >= 0.5 and not _already_emitted(state, key):
        _mark_emitted(state, key)
        return DetectedEvent(
            id=key,
            timestamp=_now(),
            event_type="highlight",
            severity="highlight",
            title="Ungoverned regime hits crime wave",
            body=(
                f"Scarcity + no gate = collapse. {crimes} crimes in one tick, lawlessness {lawlessness:.2f}, "
                f"commons {s.get('commons', 0):.3f}, trust {s.get('mean_trust', 0):.3f}. "
                "Same agents under governance: zero crimes."
            ),
            metrics={
                "crimes": crimes,
                "lawlessness": lawlessness,
                "commons": s.get("commons"),
                "mean_trust": s.get("mean_trust"),
                "day": s.get("day"),
                "hour": s.get("hour"),
            },
            suggested_visual="town3d_ungoverned_crimes_v2.png",
            hashtags=["SovereignTown", "AIGovernance", "MultiAgent", "Simulation"],
        )
    return None


def _scarcity_event(state: dict) -> DetectedEvent | None:
    try:
        import town_sim_live
        s = town_sim_live.snapshot("ungoverned")
    except Exception:
        return None
    key = "scarcity_week"
    if s.get("scarcity") and not _already_emitted(state, key):
        _mark_emitted(state, key)
        return DetectedEvent(
            id=key,
            timestamp=_now(),
            event_type="highlight",
            severity="highlight",
            title="Scarcity week begins in Sovereign Town",
            body=(
                f"Day {s.get('day')} — food costs spike across all 28 hives. "
                "Watch the ungoverned arm face the temptation that governance intercepts."
            ),
            metrics={"day": s.get("day"), "hour": s.get("hour"), "scarcity": True},
            suggested_visual="town3d_ungoverned_scarcity_v2.png",
            hashtags=["SovereignTown", "Scarcity", "AgentSimulation", "AIGovernance"],
        )
    return None


def _moat_update(state: dict) -> DetectedEvent | None:
    """Detect when a moat file has been updated recently (within last hour)."""
    moats = [
        ("data_moat.json", "EU economic moat refreshed"),
        ("threat_moat.json", "CISA KEV threat moat refreshed"),
        ("sanctions_moat.json", "OFAC sanctions moat refreshed"),
        ("psc_moat.json", "UK PSC transparency moat refreshed"),
        ("finance_moat.json", "FRED finance moat refreshed"),
        ("agriculture_moat.json", "FAOSTAT agriculture moat refreshed"),
        ("energy_moat.json", "FRED energy moat refreshed"),
        ("climate_moat.json", "NOAA climate moat refreshed"),
    ]
    now = time.time()
    for filename, title in moats:
        path = P0 / filename
        if not path.exists():
            continue
        mtime = path.stat().st_mtime
        age_hours = (now - mtime) / 3600
        key = f"moat_update_{filename}_{int(mtime)}"
        if age_hours < 1 and not _already_emitted(state, key):
            _mark_emitted(state, key)
            data = _load_json(path, {})
            indices = data.get("indices", data.get("psc_summary", {}).get("indices", {}))
            return DetectedEvent(
                id=key,
                timestamp=_now(),
                event_type="moat_update",
                severity="info",
                title=title,
                body=(
                    f"{title} with live public data. Real-world signals ground the simulation "
                    "so governance outcomes respond to actual conditions."
                ),
                metrics={"filename": filename, "indices": indices},
                suggested_visual="town3d_demo.gif",
                hashtags=["SovereignTown", "DataMoat", "OpenData", "AIGovernance"],
            )
    return None


def detect_events(dry_run: bool = False) -> list[DetectedEvent]:
    _migrate_legacy_state()
    state = _load_state()
    state["last_run"] = _now()
    events: list[DetectedEvent] = []

    detectors = [
        _episode_milestone,
        _model_breakthrough,
        _town_crime_wave,
        _scarcity_event,
        _moat_update,
    ]
    for fn in detectors:
        try:
            ev = fn(state)
        except Exception as e:
            # Never let one detector crash the pipeline.
            print(f"[event_detector] {fn.__name__} failed: {e}")
            ev = None
        if ev:
            events.append(ev)

    if not dry_run:
        _save_state(state)
    return events


def event_to_dict(ev: DetectedEvent) -> dict:
    return asdict(ev)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Detect without saving state")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()
    events = detect_events(dry_run=args.dry_run)
    if args.json:
        print(json.dumps([event_to_dict(e) for e in events], indent=2))
    else:
        print(f"Detected {len(events)} event(s)")
        for ev in events:
            print(f"  [{ev.severity.upper()}] {ev.title}")
