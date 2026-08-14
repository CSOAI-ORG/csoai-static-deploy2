# SOV A100 pod — the heavy-lift substrate

This directory is the absorbable config for running SOVOS on a RunPod A100
PCIe 80GB pod. The intent: keep the **wired spec §6 e2e** reproducible from
the canonical CSOAI monorepo, on the GPU class we want, with full test
coverage of the chain.

## Files

- `install.sh` — bootstrap a fresh RunPod A100 PCIe pod into a working
  substrate (apt deps, pip, ollama, monorepo clone).
- `spec6-e2e.py` — the wired RAS spec §6: arena → empirical permitted
  manifold → Mahalanobis → chain → OSCAL attestation.
- `test_spec6.py` — asserts the spec §6 number is reproducible (canonical:
  `SOV SIGNAL d = 4.2053σ` against `qwen2.5:0.5b-instruct` reference
  `sov-safety-v1`).

## How to bring a fresh pod up

1. On RunPod (or via `runpodctl`), create a pod:
   - GPU: NVIDIA A100 80GB PCIe
   - Image: `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`
   - Container disk: 100G; Volume: 100G
   - Ports: `8888/http,22/tcp`
   - startSSH on
   - Env: `SOV33_PIPELINE=true`
   - Cost: ~$1.19/hr

2. SSH key: ensure `~/.runpod/ssh/runpodctl-ssh-key` is registered with the
   RunPod account (`runpodctl ssh add-key --key-file ~/.runpod/ssh/runpodctl-ssh-key.pub`).

3. SSH into the pod:
   ```
   ssh root@<pod-ip> -p <dynamic-port>
   ```

4. Run the bootstrap (one-time, ~3 min):
   ```
   bash SOVOS/deploy/a100/install.sh
   ```

5. Run the spec §6 e2e:
   ```
   python3 SOVOS/deploy/a100/spec6-e2e.py            # uses saved profiles
   python3 SOVOS/deploy/a100/spec6-e2e.py --live     # against live ollama
   ```

6. Or, equivalently with the legacy `sov ras` CLI:
   ```
   PYTHONPATH=SOVOS/frontends/cli/src:SOVOS/packages/sovos-arena/src:... \
     python3 SOVOS/frontends/cli/src/sovos_cli.py ras \
       --measure qwen2.5:0.5b-instruct --at http://localhost:11434 --per-axis 32
   ```

## Verified state, 2026-08-11

Tested on RunPod pod `1dldzposn7ssuu` (a fresh A100 80GB PCIe provisioned
2026-08-11 after the previous `takeover` pods failed to come up).

| Suite                          | Result  |
|--------------------------------|---------|
| sovos-arena (9 tests)           | 9/9     |
| sovos-signal-index (16 tests)   | 16/16   |
| sovos-chain (15 tests)         | 15/15 (full PYTHONPATH) |
| sovos-fisher-rao (12 tests)     | 12/12   |
| spec §6 first real run          | SOV SIGNAL d = 4.2053σ; OSCAL v1.1.0 chain-id `8eddbc37245a75f0b899e67c` |

## The SOVOS substrate, in one paragraph

`sovos-arena` measures a target system on the 13 GSPC axes with Wilson 95%
CIs (n≥30 per axis). `sovos-signal-index` calibrates an empirical
permitted manifold (Mahalanobis distance-to-center, not np.eye(4)). The
chain in `sovos-chain` + `sovos-fisher-rao` + `sovos-jspace-hyperbolic`
converts the candidate vector into a Fisher-Rao distance. `sovos-oscal`
emits the OSCAL assessment-results document with a deterministic
chain-id. The CLI at `SOVOS/frontends/cli/src/sovos_cli.py` wires it all
together: `sov ras --measure MODEL --at ENDPOINT` and `sov ras --canary`
(the spec §4 planted-canary validation gate). The 13 GSPC axes are:
gov, prv, agi, asi, mcp, oss, mach, care, xr, det, art5, swarm.

## Memory

- A100 SSH in this session: `root@104.255.9.187 -p 11737`
- Pod id: `1dldzposn7ssuu` (name: `sov-brain-a100-fresh2-20260811`)
- The `takeover-*` pods (2oe71t1kzm145r, kj13gtv9ou08u7, gm0fmpene6znk6)
  all had `uptimeSeconds=0` and never came up. `uptimeSeconds=0` is
  reportedly the RunPod CTO's broken display field — the pod is sometimes
  actually fine, but the takeover flavour was unhealthy for unknown reasons.
- If this pod fails the same way, redeploy with a fresh `imageName` and
  explicit `--ports "8888/http,22/tcp"` (the missing-tcp-port bug surfaced
  twice in this session).
