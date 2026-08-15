# Owner-Gate Infra Register — SORTED (2026-08-13, verified live)

Mined + sorted the four unattached/unblocked infrastructure items. Each row:
**Priority | Item | Current state (verified) | Action | Effort | Blocker | What it unblocks.**

---

## THE SORT (by impact ÷ effort ÷ urgency)

### 🥇 A-1 — Max impact, trivial effort, unblocks the shared store
| Item | Verified state | Action | Effort | Unblocks |
|---|---|---|---|---|
| **Attach `sovos-merge-800` (800GB) to the A100** | RunPod network volume exists (EU-RO-1); CLI-blocked; **web-UI attach**. A100 /runpod currently only 12G local (sovos-master + sovos-boards) | Owner: RunPod dashboard → volume → attach to `1dldzposn7ssuu` (EU match) | **~5 min (owner UI)** | The real shared store: all 13 board axes + cross-lab + seasons write to durable 800GB volume instead of 12G pod-local |
| **Attach `sov-models` (300GB) + `sov-artifacts` (200GB)** | Exist (CA-MTL-3, wrong DC for A100 — but readable via REST/SFTP) | Owner: web-UI attach to A100 or use as read-only mirror targets | ~10 min (owner UI) | Model + artifact durability off the pods |

### 🥈 A-2 — Legal exposure, 5 min each
| Item | Verified state | Action | Effort | Unblocks |
|---|---|---|---|---|
| **Delist/rename 5 `sov-*` HF models** | LIVE: sov34-1p5b, sov-gate-ft2, sov-refusal-lora, sov-ethics-art5, sov-compliance-art5 | HF token (rotate first per O2) → these 5 → rename or delist | ~10 min (owner) | Removes last public codename bleed; HF cleanup = spray-gate precondition |

### 🥉 A-3 — Chain of custody, medium effort
| Item | Verified state | Action | Effort | Unblocks |
|---|---|---|---|---|
| **MinIO TLS pin (C5)** | A100 :9000 healthy, HTTP only; public :9000 present from incident; master is single-pod | TLS termination + private buckets + least-priv keys BEFORE any shared-store external flow | ~30 min-1h (owner + lane) | Security-gates the shared store; BS.3 pin says "TLS before bytes" |

### 🕐 A-4 — Billing gate (owner's largest single action)
| Item | Verified state | Action | Effort | Unblocks |
|---|---|---|---|---|
| **Re-enable GCP billing briefly** | meok-backend unreachable; watcher armed + auto-fires on billing (watcher.log 05:07 "billing gate stands") | Owner: GCP billing on (~£2-5) → `launchctl kickstart` the 6 com.meok.* plists **OR let gcp-evac-watcher auto-evacuate** | ~5 min + wait | SOV3/:8077 substrate + evac completion + OLM brain + 32 crons + 189GB moat |

---

## DEPENDENCY CHAIN (why order matters)
```
A-1 volume attach → gives durable shared store
  └─ C5 TLS pin   → makes that store safe to expose
  └─ board/cross-lab/seasons write to volume (survive pod reprovision)
A-2 HF delist     → spray-gate precondition (no codename bleed)
A-4 GCP billing   → evac watcher auto-fires (independent; can be parallel)
```

## WHAT THE OWNER DOES (30-min owner batch, in order)
1. **RunPod web UI**: attach `sovos-merge-800` → A100 (it's the writer)
2. **HF**: rotate token (O2), then delist 5 `sov-*` models
3. **GCP**: re-enable billing (watcher handles evac automatically)
4. **Say the word → lane does**: C5 TLS pin on MinIO (after volume attached)

## What I CANNOT do (stood gates)
Web-UI volume attach · HF token rotation/delist · GCP billing / 6 plist kickstart.
All three are owner-only (auth/account surfaces). Everything else is lane-executable once those land.

## Not included (lower burn / already flowing)
- 3090 disk 79% (management mode, not blocked) · A1-hunter still hunting · arena R105 live
- G4 linter, Inspect bridge, cross-lab board — all shipped/committed this EAT.