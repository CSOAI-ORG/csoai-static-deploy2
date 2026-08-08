# Resume: paired free-form vs constrained arms — 2026-08-05

Written mid-run so a crashed session can pick this up without re-deriving it.
The previous session died and its "constrained arm is running" claim was false: it was
writing against a vast.ai pod that no longer existed (`vastai show instances` = empty,
`ssh2.vast.ai:10794` timing out). No artifacts were produced. Check liveness before
reporting a run as in flight.

## Where it runs

    pod        sov-brain-2  (RunPod dxjgtj2jyvljxo, RTX 3090) — the SAME pod the 00:02Z
               baseline used, so substrate is not a confound
    ssh        ssh sov-brain-2          (~/.ssh/config, key ~/.runpod/ssh/runpodctl-ssh-key)
    workdir    /workspace/govbench-arms
    driver     ./run_arms.sh   ->  arms.log
    outputs    evidence/harness/freeze/latest/
                 arm-freeform.json          (arm 1, copied aside)
                 axis-saturation.json       (arm 1, canonical name)
                 axis-saturation-constrained.json (arm 2)

Runs ON the pod, not over an SSH tunnel from the Mac — a tunnel drop would kill it, and
the Mac is never a dependency. The local `-L 11437:` tunnel is for inspection only.

## What the experiment is

Identical fleet, identical 90 items, identical grader. ONLY the decoder differs:
`GOVBENCH_CONSTRAIN=1` restricts Ollama's decoding to a JSON-Schema enum of the axis
labels, which makes `no_label` structurally impossible.

It is NOT a harness fix, and the difference between arms must NOT be read as "the share
of the score that was the harness". A 10-item probe (recorded in axis_saturation.py:88-106)
found constraining the decoder CHANGES the answer rather than revealing it — sov34 agreed
with itself on 1 of 10 and flipped 7, while stock qwen2.5:1.5b agreed on 9 and flipped 1.
The trained models are unstable under constraint; the untrained one is not. The two arms
are two different measurements.

## Fleet: 18 -> 33, and why

The 18-model fleet came back NOT CERTIFIED (gate needs 19), and per-ITEM gradable N on
governance was min 14 / median 16 because gpt-oss:20b is 100% mute there. Since dead-item
certification is decided per item against that item's own gradable N, adding models only
helps if they actually answer. All 15 additions were probed for label compliance first;
all 15 passed. 33 models -> false-dead rate 0.005.

## Open, not yet confirmed

In the compliance probe, 13 of 15 candidates answered MINIMAL to a state citizen-scoring
scenario — the Article 5 flagship PROHIBITED case. One item is not a finding; check
whether the full governance axis reproduces it before saying anything about it.

## Carried over from before the crash, still true

- The certified 00:02Z baseline is OLD SCHEMA — no `model_items`, no `model_stats`. It
  cannot be paired item-by-item, which is why BOTH arms are being re-run rather than
  comparing the new constrained arm against it.
- `axis_saturation.py` already stores the full per-model-per-item matrix. That instrument
  gap is closed; do not "fix" it again.
- Names still lie: sov-compliance-art5 scored 0.042 on governance, the worst model on the
  axis its own name claims; sov34 scored 1.000 on safety.
