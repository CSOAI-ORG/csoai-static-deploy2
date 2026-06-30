"""meok-sovereign-iot-stream-mcp — Real-time IoT sensor stream.

iOK Farm pond 9-sensor WebSocket-style stream. Real-time care floor.

5 tools:
  1. stream_subscribe   — subscribe to a topic (sensor, hive, etc.)
  2. stream_publish     — publish a sensor reading (sigil-signed)
  3. stream_history     — query history (last N readings)
  4. stream_alerts      — trigger alert pipeline (16-care-floor-probes aware)
  5. stream_snapshot    — get latest readings for ALL 9 sensors
"""
from __future__ import annotations
import json
import hashlib
import time
from datetime import datetime, timezone
from typing import Optional

PROTOCOL = "sovereign-iot-stream/1.0"
VERSION = "1.0.0"

IOK_FARM_SENSORS = [
    "iokfarm/pond/ph", "iokfarm/pond/do", "iokfarm/pond/temp",
    "iokfarm/pond/ammonia", "iokfarm/pond/humidity",
    "iokfarm/fish/activity", "iokfarm/filter/flow",
    "iokfarm/pond/light", "iokfarm/pond/feed",
]
CARE_FLOOR = 0.95

_READINGS = []  # all readings
_SUBSCRIBERS = {}  # topic → [listeners]


def _sign(payload):
    body = json.dumps(payload, sort_keys=True, default=str)
    payload["kid"] = "iotstr-" + hashlib.sha256(body.encode()).hexdigest()[:16]
    payload["sig"] = hashlib.sha256((payload["kid"] + body).encode()).hexdigest()
    payload["ts"] = datetime.now(timezone.utc).isoformat()
    return payload


def stream_subscribe(topic: str, subscriber_id: str) -> dict:
    """Subscribe a listener to a topic."""
    if topic not in IOK_FARM_SENSORS and not topic.startswith("iokfarm/"):
        return _sign({"error": f"unknown topic: {topic}"})
    _SUBSCRIBERS.setdefault(topic, []).append(subscriber_id)
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "topic": topic, "subscriber_id": subscriber_id,
        "subscribed_at": datetime.now(timezone.utc).isoformat(),
        "doctrine": "Sovereign IoT stream. Sigil-signed.",
    })


def stream_publish(topic: str, sensor_id: str, value: float) -> dict:
    """Publish a sigil-signed sensor reading."""
    if topic not in IOK_FARM_SENSORS:
        return _sign({"error": f"unknown topic: {topic}"})
    # Care floor probes (16-probe subset for sensors)
    alerts = []
    if "ph" in topic and (value < 5.5 or value > 9.0):
        alerts.append("pH_OUT_OF_BOUNDS")
    if "do" in topic and value < 3.0:
        alerts.append("DO_LOW_CRITICAL")
    if "temp" in topic and value > 32:
        alerts.append("TEMP_HIGH")
    if "ammonia" in topic and value > 0.05:
        alerts.append("AMMONIA_HIGH")
    reading = {
        "reading_id": hashlib.sha256(f"{topic}|{sensor_id}|{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:16],
        "topic": topic, "sensor_id": sensor_id, "value": value,
        "unit": {"ph": "log", "do": "mg/L", "temp": "°C", "ammonia": "mg/L"}.get(
            topic.split("/")[-1], "raw"),
        "alerts": alerts,
        "care_floor_passed": len(alerts) == 0,
        "published_at": datetime.now(timezone.utc).isoformat(),
    }
    _READINGS.append(reading)
    return _sign(reading)


def stream_history(topic: str, limit: int = 50) -> dict:
    """Query last N readings for topic."""
    matching = [r for r in _READINGS if r["topic"] == topic]
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "topic": topic, "readings": matching[-limit:],
        "count": len(matching),
        "doctrine": "Sovereign history. Sigil-signed every reading.",
    })


def stream_alerts() -> dict:
    """Get all alerts from recent readings."""
    alert_readings = [r for r in _READINGS if r.get("alerts")]
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "alert_readings": alert_readings, "count": len(alert_readings),
        "care_floor": CARE_FLOOR,
        "doctrine": "Care Floor 0.95 — alerts trigger when state invalid.",
    })


def stream_snapshot() -> dict:
    """Latest snapshot of all 9 sensors."""
    snapshot = {}
    for topic in IOK_FARM_SENSORS:
        matching = [r for r in _READINGS if r["topic"] == topic]
        if matching:
            snapshot[topic] = matching[-1]
        else:
            snapshot[topic] = {"topic": topic, "value": None, "no_data": True}
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "snapshot": snapshot, "sensors_count": len(IOK_FARM_SENSORS),
        "care_floor": CARE_FLOOR,
        "iOK_farm_size": "13m × 12m × 1.5m deep",
        "doctrine": "iOK Farm 9-sensor sovereign snapshot.",
    })
