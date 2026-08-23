#!/bin/bash
# sov-brain-2 SSH wrapper — the real live RunPod pod.
# Old Host sov-brain-2 in ~/.ssh/config points at a dead pod (213.144.200.240:11982).
# Real one: fpowppss5ngtkw @ 194.26.196.156:17446, RTX 3090, /workspace mounted.
exec ssh -i ~/.runpod/ssh/runpodctl-ssh-key -p 17446 root@194.26.196.156 "$@"
