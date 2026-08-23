# RUNPOD DRAIN RUNBOOK — get to $0/mo, lose nothing
_Staged 2026-07-28 (CC lane). Fires once Nick tops up. Deletes NOTHING until checksums verify._

## The leak
3 network volumes bill even with all 20 pods EXITED (~$0.07/GB/mo):

| Volume | Size | Datacenter | Drain pod boots in |
|---|---|---|---|
| `sov-models` | 300 GB | CA-MTL-3 | one A40 in CA-MTL-3 |
| `sov-artifacts` | 200 GB | CA-MTL-3 | (same pod — both mount here) |
| `sov-workspace-mtl4` | 200 GB | CA-MTL-4 | one A40 in CA-MTL-4 |

**700 GB total ≈ $49/mo bleeding.** Drain = one-time **~$0.20 of CPU-pod time**, then $0 forever.

## Can we skip the pod entirely? — TESTED 2026-07-28: NO (for these volumes)
RunPod's S3-compatible API (read a volume with no pod) exists **only in a few datacenters** —
`s3api-eu-ro-1 / us-ks-2 / eur-is-1` all resolve; **`s3api-ca-mtl-3` and `s3api-ca-mtl-4` = NXDOMAIN.**
Your volumes are datacenter-locked in Montreal, which has no S3 gateway. So a pod attach is required.
**Cost fix:** a copy job needs **no GPU** — boot the **cheapest CPU pod (~$0.02–0.10/hr)**, not an A40.

## Sequence (each volume)
1. **Top up ~$5** (buffer only — actual drain cost is cents). ← Nick, in progress.
2. **Web UI:** deploy **one CPU pod (cheapest tier)** in the volume's datacenter, **attach the volume**
   (mounts at `/workspace`), enable SSH. No GPU needed — CPU pods have the best availability anyway.
3. **Copy + verify (this repo):**
   ```bash
   # dry-run first — inventories + checksums the source, copies nothing
   VOL_NAME=sov-models POD_HOST=<pod-ip> POD_PORT=<port> bash runpod_drain.sh
   # then the real copy -> Oracle ARM (+ optional HF), re-checksums, reports 0 mismatches
   VOL_NAME=sov-models POD_HOST=<pod-ip> POD_PORT=<port> DRY_RUN=0 \
     ORACLE_DEST=/data/runpod-drain bash runpod_drain.sh
   ```
4. **Confirm** the script prints `✅ VERIFIED — safe to delete`. Manifests land in `DRAIN_MANIFEST_<vol>_<stamp>.{list,sha256,dest.sha256}`.
5. **Delete** the volume in the web UI — **only after** step 4 shows 0 mismatches. (Manual + confirmed; the script never deletes.)
6. Repeat for `sov-artifacts` (same CA-MTL-3 pod) and `sov-workspace-mtl4` (new CA-MTL-4 pod).
7. **Terminate the 20 exited pods** + delete volumes → RunPod dashboard reads **$0/mo**.

## Where it lands (all free, durable)
- **Oracle ARM** `145.241.232.16` (`/data/runpod-drain/<vol>`) — full-fidelity mirror, always-on, free. Primary.
- **HuggingFace** repos (optional, set `HF_REPO`+`HF_TOKEN`) — natural home for model weights + datasets.
- Going forward compute = **Kaggle T4 (30h/wk free)** + Oracle ARM + HF Spaces. Already where sov-asi-evolve / SOV6 comps run.

## Guardrails
- **Nothing deletes without a verified checksum match.** The script only ever reads + copies.
- Confirm Oracle `/data` has ≥700 GB free before draining (Oracle instance-2 had ~42 GB — may need the bigger instance or a HF push for the 300 GB `sov-models`).
- Egress from RunPod is free — no surprise transfer cost.
- Money + pod-boot stay **gated** — Nick fires steps 1–2; CC runs 3–4 and reports before any delete.
