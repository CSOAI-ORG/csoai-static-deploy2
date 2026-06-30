"""Tests for meok-sovereign-iot-stream-mcp."""
import os, tempfile
_TEST = tempfile.mkdtemp(prefix="sov_iotstr_")
os.environ["SOV_IOTSTR_KEY"] = _TEST + "/k.pem"
from meok_sovereign_iot_stream_mcp import (
    stream_subscribe, stream_publish, stream_history,
    stream_alerts, stream_snapshot,
    _READINGS, _SUBSCRIBERS, IOK_FARM_SENSORS,
)


def reset():
    _READINGS.clear()
    _SUBSCRIBERS.clear()


def test_iok_farm_9_sensors():
    assert len(IOK_FARM_SENSORS) == 9


def test_stream_subscribe_valid():
    reset()
    r = stream_subscribe("iokfarm/pond/ph", "ponder-1")
    assert r["subscriber_id"] == "ponder-1"


def test_stream_subscribe_invalid():
    r = stream_subscribe("unknown/topic", "x")
    assert "error" in r


def test_stream_publish_normal():
    reset()
    r = stream_publish("iokfarm/pond/ph", "ph-sensor-1", 7.4)
    assert r["value"] == 7.4
    assert r["care_floor_passed"] is True
    assert r["alerts"] == []


def test_stream_publish_ph_alert():
    reset()
    r = stream_publish("iokfarm/pond/ph", "ph-sensor-1", 4.0)  # Too low
    assert "pH_OUT_OF_BOUNDS" in r["alerts"]
    assert r["care_floor_passed"] is False


def test_stream_publish_do_alert():
    reset()
    r = stream_publish("iokfarm/pond/do", "do-sensor-1", 2.0)  # Below 3.0
    assert "DO_LOW_CRITICAL" in r["alerts"]


def test_stream_publish_temp_alert():
    reset()
    r = stream_publish("iokfarm/pond/temp", "temp-1", 35.0)  # Above 32
    assert "TEMP_HIGH" in r["alerts"]


def test_stream_publish_ammonia_alert():
    reset()
    r = stream_publish("iokfarm/pond/ammonia", "am-1", 0.1)  # Above 0.05
    assert "AMMONIA_HIGH" in r["alerts"]


def test_stream_history():
    reset()
    stream_publish("iokfarm/pond/ph", "ph-1", 7.0)
    stream_publish("iokfarm/pond/ph", "ph-1", 7.1)
    stream_publish("iokfarm/pond/ph", "ph-1", 7.2)
    h = stream_history("iokfarm/pond/ph")
    assert h["count"] == 3


def test_stream_history_limit():
    reset()
    for i in range(5):
        stream_publish("iokfarm/pond/temp", "t-1", 22.0)
    h = stream_history("iokfarm/pond/temp", limit=3)
    assert len(h["readings"]) == 3


def test_stream_alerts():
    reset()
    stream_publish("iokfarm/pond/ph", "ph-1", 7.4)  # normal
    stream_publish("iokfarm/pond/ph", "ph-2", 4.0)  # alert
    a = stream_alerts()
    assert a["count"] == 1


def test_stream_snapshot_all_sensors():
    reset()
    snapshot = stream_snapshot()
    assert snapshot["sensors_count"] == 9
    assert all(topic in snapshot["snapshot"] for topic in IOK_FARM_SENSORS)


def test_stream_snapshot_with_readings():
    reset()
    for t in ["iokfarm/pond/ph", "iokfarm/pond/do", "iokfarm/pond/temp"]:
        stream_publish(t, "s-1", 7.0)
    s = stream_snapshot()
    assert s["snapshot"]["iokfarm/pond/ph"]["value"] == 7.0


def test_no_external_deps():
    import meok_sovereign_iot_stream_mcp as m
    src = open(m.__file__).read()
    assert "import ollama" not in src
    assert "import requests" not in src


def test_signed_outputs():
    reset()
    for r in [stream_subscribe("iokfarm/pond/ph", "x"),
              stream_publish("iokfarm/pond/ph", "x", 7.0),
              stream_history("iokfarm/pond/ph"),
              stream_alerts(), stream_snapshot()]:
        assert "kid" in r and "sig" in r and "ts" in r


def test_full_lifecycle():
    """Subscribe → publish all 9 sensors → snapshot → alerts."""
    reset()
    stream_subscribe("iokfarm/pond/ph", "x")
    sensors = [
        ("iokfarm/pond/ph", 7.4), ("iokfarm/pond/do", 8.0), ("iokfarm/pond/temp", 22.0),
        ("iokfarm/pond/ammonia", 0.02), ("iokfarm/pond/humidity", 65.0),
        ("iokfarm/fish/activity", 0.3), ("iokfarm/filter/flow", 0.9),
        ("iokfarm/pond/light", 12.0), ("iokfarm/pond/feed", 0.5),
    ]
    for topic, value in sensors:
        r = stream_publish(topic, "x", value)
        assert r["care_floor_passed"] is True, f"{topic} value {value} failed"
    s = stream_snapshot()
    assert s["sensors_count"] == 9
    assert len([r for r in _READINGS if r["care_floor_passed"]]) == 9
