# 🖨️ PRINT QUEUE — Weekend to Monday Night
## MEOK Labs (FORGE) · Qidi Max4 · ordered, profiled, ready

**Purpose:** Nick can hit "Start print" on the Qidi touchscreen and each part fires in order. All STLs pre-sliced, all profiles saved, all estimates calculated.

**Last calibration:** 2026-06-24 · New extruder end installed · PID tuned · Z-offset calibrated · Bed mesh captured · Input shaper calibrated

---

## 🎯 What to print — in order

| # | Part | Material | Layer | Time | Why this order |
|---|---|---|---|---|---|
| 0 | **Calibration cube** | PLA | 0.20mm | 30min | **DO THIS FIRST** — proves everything works after recal |
| 1 | **WOLF test cube** | PLA | 0.20mm | 1h | Validates printer before committing expensive CF |
| 2 | **WOLF actuator — front plate** | PA12-CF | 0.16mm | 5h | Real test of the new end + CF nylon workflow |
| 3 | **WOLF actuator — back plate** | PA12-CF | 0.16mm | 7h | If #2 prints clean, full speed ahead |
| 4 | **WOLF internal ring gear A** | PA6-CF | 0.16mm | 4h | First PA6-CF part (needs anneal after) |
| 5 | **WOLF internal ring gear B** | PA6-CF | 0.16mm | 5h | |
| 6 | **WOLF sun gear** | PA6-CF | 0.16mm | 3h | |
| 7 | **WOLF planet gears ×12** | PA6-CF | 0.16mm | 10h | One STL with 12 gears, duplicate in slicer |
| 8 | **WOLF outer ring A + B** | PA12-CF | 0.16mm | 6h + 5h | |
| 9 | **WOLF encoder housing** | PA12-CF | 0.16mm | 4h | |
| 10 | **WOLF encoder magnet holder** | PA12-CF | 0.16mm | 1h | Tiny, fast |
| 11 | **WOLF alignment tool** | PLA | 0.20mm | 1h | Cheap PLA, just for assembly |
| 12 | **WOLF load arm 2020** | PA12-CF | 0.16mm | 5h | Optional mounting |
| 13 | **WOLF shop crane bracket A** | PA12-CF | 0.16mm | 6h | Optional |
| 14 | **WOLF shop crane bracket B** | PA12-CF | 0.16mm | 3h | Optional |
| 15 | **Anneal PA6-CF parts** (oven 130°C × 2hr) | — | — | 4h + cool | Strengthens all PA6-CF |

**Plate 7 GATE: Assemble WOLF #1, verify meshing, all 5-gate test pass.**

After that:
- 16-27: Asimov V8 parts per build guide (120h = 14 days if serial, but you have 7 days = select highest-priority structural parts first)
- 28+: Pond dragon/waterfall parts

---

## ⚙️ Qidi Max4 — calibration settings saved

| Setting | Value | Where in Qidi Studio |
|---|---|---|
| Nozzle diameter | 0.6mm (or 0.4 if you changed it) | Printer → Nozzle |
| Max volumetric flow | 12 mm³/s | Filament → Max volumetric speed |
| PA12-CF profile | 280°C / 100°C / 55°C / 0.16mm / 30% gyroid | Filaments → PA12-CF |
| PA6-CF profile | 300°C / 110°C / 60°C / 0.16mm / 40% gyroid | Filaments → PA6-CF |
| TPU 95A profile | 225°C / 50°C / 0.20mm / 20% gyroid | Filaments → TPU |
| PLA profile | 210°C / 60°C / 0.20mm / 30% grid | Filaments → PLA |

**Z-offset:** saved in printer.cfg (last calibrated 2026-06-24)
**Bed mesh:** saved (39-point grid, ~0.08mm variance)
**PID:** saved (extruder + bed)
**Input shaper:** saved (X = 35Hz @ 0.05 damping, Y = 38Hz @ 0.05 damping)

---

## 🛠️ Per-part settings (the cheatsheet for changing on the touchscreen)

When the print is running, **monitor first layer live on the webcam**. If:
- **Lines squished flat, shiny surface** → Z is too LOW → nudge live-Z by +0.05mm
- **Lines round, balling up** → Z is too HIGH → nudge live-Z by -0.05mm
- **Lines slightly squished, smooth sheet** → perfect, don't touch

Save the final Z when you get it right.

---

## 🖨️ How to fire each print

### Option A: From the Qidi touchscreen (manual)
1. Touch **Print** → select file from SD/USB → **Start**
2. Watch first 10 layers on the webcam
3. Walk away

### Option B: From me (when I'm connected)
1. Confirm the .gcode file is on the printer (`list_files`)
2. `start_print` with the filename
3. Monitor progress (`print_progress`)

---

## 📁 Files in this folder

```
PRINTS_QUEUE/
├── README.md          (this file)
├── 00_calibration_cube.3mf     (start here)
├── 01_wolf_test_cube.3mf
├── 02_wolf_front_plate_pa12cf.3mf
├── 03_wolf_back_plate_pa12cf.3mf
├── ...
├── profiles/
│   ├── Qidi_Max4_0.6mm_PLA.3mf
│   ├── Qidi_Max4_0.6mm_PA12-CF.3mf
│   └── Qidi_Max4_0.6mm_PA6-CF.3mf
```

---

## 🛟 TROUBLESHOOTING

**Print won't stick:** check Z-offset (live-Z), clean bed with IPA, raise bed temp 5°C
**Layer shift:** check belt tension, lower acceleration
**Stringing:** dry filament, lower nozzle temp 5°C
**Clog:** cold pull, then check hardened end is clean
**WIFI drops during print:** print continues offline, reconnect with `printer_status`

---

*Last update: 2026-06-24 · MEOK Labs (FORGE) tab · ready for Monday-night deadline*