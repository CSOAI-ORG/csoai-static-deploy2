# SOVOS-MASTER — Fleet Wiring Config Bundle (all nodes → A100 :9000)
**Status:** READY-TO-APPLY. A100 is `machineId: None` (RunPod re-provision pending). All configs below are the exact one-liners to run on each node the moment `:9000` is reachable.

## Master endpoint (public, now in pod port config)
```
S3_ENDPOINT   = http://104.255.9.187:9000
ACCESS_KEY_3090 = gpu3090rw-11lvAw
SECRET_3090     = hZTqfLQnmWGWR6yx
ACCESS_KEY_A100 = a100rw-GDiniQ
SECRET_A100     = 7e6JL5UXbD5XD5tS
```
Health probe: `curl -s -o /dev/null -w "%{http_code}" http://104.255.9.187:9000/minio/health/live` → expect 200 when A100 is back.

## A. RunPod serverless endpoints (16) — client-side wiring
Serverless workers are stateless: they CALL OUT to the master to persist results. Pattern per endpoint's handler (Python example):
```python
import rclonepy  # or subprocess
# persist a run result to the master immediately after inference:
subprocess.run(["rclone","copyto","-","sovos:evidence/serverless/<endpoint-name>/<run-id>.json",
    "--s3-endpoint","http://104.255.9.187:9000",
    "--s3-access-key-id","a100rw-GDiniQ",
    "--s3-secret-access-key","7e6JL5UXbD5XD5tS"], input=json_bytes)
```
**Rule:** each endpoint writes to `evidence/serverless/<name>/` so results are corpus-fed and never lost on worker recycle.

## B. The 3090 pod (fpowppss5ngtkw, 194.26.196.156:17446)
```bash
rclone config create sovos s3 provider Minio env_auth false \
  access_key_id "gpu3090rw-11lvAw" secret_access_key "hZTqfLQnmWGWR6yx" \
  endpoint "http://104.255.9.187:9000" --non-interactive
rclone lsd sovos:   # verify
```

## C. Oracle Always-Free micros (public Ubuntu)
```bash
# on each Oracle micro (oracle-1, oracle-2)
curl -sL https://rclone.org/install.sh | sudo bash
rclone config create sovos s3 provider Minio env_auth false \
  access_key_id "a100rw-GDiniQ" secret_access_key "7e6JL5UXbD5XD5tS" \
  endpoint "http://104.255.9.187:9000" --non-interactive
rclone lsd sovos:
```

## D. Kaggle Kernels (each kernel run)
```python
# in-kernel (Python) — boto3, no creds on disk
import boto3
s3 = boto3.client("s3", endpoint_url="http://104.255.9.187:9000",
                  aws_access_key_id="a100rw-GDiniQ",
                  aws_secret_access_key="7e6JL5UXbD5XD5tS")
s3.upload_file("result.json", "evidence/kaggle/<kernel>/result.json", "result.json")
```

## E. Mac (already wired via tunnel — re-verify when A100 returns)
```bash
rclone lsd sovos:                                  # should list 6+ buckets
rclone copy sovos: ~/sovos-master-backup/          # full all-bucket backup (fixed coverage)
```

## F. Free GPU/CPU hosts (runpodctl, vast, any)
Same pattern as B: install rclone → `sovos:` remote → `http://104.255.9.187:9000` → lsd.

## Verification checklist (run once, in order, when A100 is back)
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://104.255.9.187:9000/minio/health/live   # 200
# on 3090
rclone lsd sovos: && rclone copy /tmp/test.txt sovos:evidence/fleet-wire-test.txt
# from an Oracle micro
rclone lsd sovos: && rclone ls sovos:evidence/ | head
# Mac
rclone lsd sovos: && tail -1 ~/sovos-master-backup/sovos-test.txt
```

## Buckets (created, per-pod users already provisioned)
models · merges · datasets · evidence · signed-cards · corpus · corpus-backup