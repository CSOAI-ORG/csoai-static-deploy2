# Sovereign IoT & Physical AI — iOK Farm White Paper

**CSOAI Ltd (UK 16939677) · MIT licensed · 28 Jun 2026**

---

## The iOK Farm Story

A 6.5-acre farm in Sutton St James (52.7917, -0.0500), Yorkshire, UK.
The physical home of the sovereign substrate:

- **13m × 12m koi pond** (234,000 litres) — the physical proof
- **4 bead filters + 2 Evolution Aqua UVs** — the water system
- **ESP32 + Atlas Scientific EZO-pH + EZO-DO** — the sensors
- **8 malamutes** (Misty, Zeus, Luna, Storm, Puma, Kita, Lamb, Bear) — the guardians
- **1 Qidi Max4 3D printer** — the fabrication tool
- **135ft microgreens tunnel** — the food system

The koi pond is sovereign. The Malamutes guard the perimeter. The
MCP stack makes this farm a real-world deployment of the sovereign
substrate.

## Sovereign IoT Stack

| MCP | iOK Farm Use | Tests |
|---|---|---|
| iot | ESP32 sensors + MQTT + emergency stop | 12 |
| pond | 13m×12m koi pond + care floor + 9 malamutes | 13 |
| globe | 33-hive geo-located registry (iok-pond-001 is hive-33) | 18 |
| satellite | 6 free Earth observation sources for the farm | 10 |
| honour | Maternal Covenant (16 care probes) | 15 |
| memory | Episodic pond readings + care actions | 12 |
| immortal | Bitcoin-anchored eternal pond history | 11 |

## Koi Care Floor (5 parameters, 0 violations)

| Parameter | Min | Max | Current | Status |
|---|---|---|---|---|
| pH | 6.5 | 8.5 | 7.4 | ✓ within range |
| DO (mg/L) | 5.0 | 12.0 | 8.2 | ✓ within range |
| Temp (°C) | 4 | 30 | 22.1 | ✓ within range |
| Ammonia (mg/L) | 0 | 0.02 | 0.001 | ✓ within range |
| Nitrite (mg/L) | 0 | 0.5 | 0.05 | ✓ within range |

If any parameter crosses the care floor, **auto-emergency action**:
- pH crash / ammonia spike → water_change_solenoid_open (FREE, no approval)
- O2 drop → aerator_full (FREE, no approval)
- koi distress → alert + feed_koi + medicate (BFT council)

## IoT Devices

| Device | Type | Sensors | Actuators |
|---|---|---|---|
| iok-pond-001 | esp32 | pH, DO, temp, humidity | 9 (pumps, UVs, feeder, aerator, solenoid) |
| iok-tunnel-001 | esp32 | temp, humidity, soil_moisture, co2 | 3 (light, pump, fan) |
| iok-pond-camera-001 | rpi | camera, motion | — |

## The MCP Bridge Architecture

```
iOK Farm (UK)            M2 Mac (Sov Space)         SOV3 Substrate
ESP32 sensors     -->    UE5 → SOV3 bridge    -->    12 sovereign MCPs
MQTT broker        -->    FastAPI :8765        -->    167 tests pass
(pond, tunnel, cam)      (22 MCPs importable)        (Ed25519 signed)
```

## Economics

- **Hardware cost:** £15-20/ESP32 + £50-100/sensor = **£500-1,000 for 5 ESP32s**
- **Bridge cost:** £0-30/mo (cloud GPU hour if needed, free M2 Mac)
- **MCP stack:** **£0 (free tier)** for iOK Farm scale
- **vs commercial alternative:** £2,000-5,000/mo (AWS IoT Core, Azure IoT Hub)

## How to Get Started

```bash
pip install meok-sovereign-iot-mcp meok-sovereign-pond-mcp

# Pond status
sovereign pond status
# → 12 koi, 9 malamutes, 13m × 12m

# Log a reading (from ESP32)
sovereign pond log --ph 7.4 --do_mgL 8.2 --temp_C 22.1 --humidity 65.0
# → healthy: true, no violations

# EMERGENCY (FREE, no approval)
sovereign pond emergency ph_crash
# → auto_action: water_change_solenoid_open

# Register a new sensor
sovereign iot register "iok-new-sensor-001" "esp32" "New sensor" "iOK Farm" "Sensors" "pH,DO" "iok-pond-001"
# → device_id registered, Ed25519-signed
```

## About CSOAI

CSOAI Ltd (UK 16939677). MIT-licensed. The dragon never lies.

**Verify at https://proofof.ai** · **GitHub: https://github.com/CSOAI-ORG**
