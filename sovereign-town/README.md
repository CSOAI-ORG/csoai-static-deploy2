# Sovereign Town — the governed agent-world + data/attestation engine

A governed-vs-ungoverned agent-world simulation that doubles as a **data-moat flywheel**, an **IP engine**,
a **compliance-intelligence looking-glass**, and an **agent-identity (passport) layer** — our answer to
emergence.ai. Built 2026-06-19. Honest scope: **in-simulation (P0/P1), public archetypes only**, defensive-only,
ledger-only money, honest counts (27 personas / 12-around-1 council / 271 MCPs). Master plan:
`../SOVEREIGN_TOWN_MASTER_PLAN_2026-06-19.md`; full spec: `../SOVEREIGN_TOWN_POC_2026-06-19.md` (§1-16).

## The kernel — start here
`sovereign_os.py` is the **Governance OS control-plane** that unifies everything below:
`status` (unified dashboard) · `ps` (hives = processes) · `syscall <agent> <action>` (passport-gated permission
layer) · `verify <passport>` · `signal <hive> <alarm|trail> <msg>` (event bus) · `boot`. One interface over the
sim, passports, gate, bus, vault, models, ledger, Labs.

## The pieces (all in `p0_aqua/`)
| file | what it does |
|---|---|
| `sovereign_os.py` | **the OS kernel** — unified control-plane (status/ps/syscall/verify/signal/boot) |
| `sim.py` | 28-district governed-vs-ungoverned engine (needs/gate/contagion/commons/trust, block_rate regimes) |
| `batch.py` | parallel corpus generation (~750K episodes/s/10 cores) |
| `flywheel_forever.py` | **the 24/7 daemon** — ever-advancing seeds, singleton-locked, per-host (`--seed-base`), Ed25519 ledger, auto train+report+pack |
| `train_all_hives.py` | one sovereign threat model per hive (~0.99 acc) → `models/` |
| `jurisdiction.py` | **the Looking Glass** — pre-compute outcomes per regulatory regime (EU/US/UK/none) |
| `hive_pack.py` | each hive **eats its own industry** → signed industry pack → MEOK Labs |
| `agent_passport.py` | **the key** — signed offline-verifiable agent identity (King + 28 hives) |
| `gate_access.py` | **Zero-Trust gate** — passport-checked runtime access (grant/deny/quarantine) |
| `pheromone_bus.py` | **fleet nervous system** — cross-hive alarm propagation + trail diffusion (Ed25519) |
| `report.py` | publish per-hive whitepapers → MEOK Labs index |
| `sign_lib.py` / `verify_chain.py` | Ed25519 sign + offline chain verification |
| `../verify/index.html` | **public verifier** — anyone verifies a passport/attestation in-browser, no server |

## Run it
```
cd p0_aqua
python3.11 flywheel_forever.py --seed-base 200000000 --sleep 300   # the 24/7 fleet (Mac partition)
python3.11 jurisdiction.py        # the looking glass (regime outcomes)
python3.11 hive_pack.py           # every hive eats its industry
python3.11 agent_passport.py      # issue + verify agent passports
python3.11 gate_access.py         # zero-trust gate demo
python3.11 pheromone_bus.py       # cross-hive coordination demo
```

## Fleet (24/7, 3 hosts, disjoint seeds → no duplicate data)
- **VM** `meok-backend` seed-base 0 (systemd-style nohup + `@reboot` cron) · **Mac** seed-base 200M · **Actions** seed-base 100M (nightly, on `main`).
- Stop: `pkill -f flywheel_forever` (Mac) / `ssh meok-backend pkill -f flywheel_forever` (VM). Status: `fleet_status_*.json`.

## Bright lines (non-negotiable — see spec §16)
Public data only · every output labelled SIMULATION/prediction (never assert a named real firm is non-compliant) ·
opt-IN before contacting any entity · regulators get anonymized/aggregate + wind-tunnel-the-RULE (not name-and-shame) ·
consent-vault not surveillance · space = governance lane (no ISS collection) · defensive-only (no offensive/"worm") ·
no real money without legal sign-off · honest counts.

## Gated on Nick (deploys/credentials/legal — never done silently)
- Submit GPU credit applications (NVIDIA/DO/MS — needs company identity).
- Public openpatent push (7 inventions live in local 6-layer registry; publishing IP is your decision).
- Deploy `verify/` + the showcase to Vercel; VM crash-watchdog cron (you authorized `@reboot` only).
