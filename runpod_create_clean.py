#!/usr/bin/env python3
"""runpod_create_clean.py — Create a fresh RunPod pod with proper env
for LoRA training. Uses runpod/pytorch image with CUDA 12.4 (matches H100).
"""
import json, os, subprocess, sys, time
from pathlib import Path

KEY_FILE = Path.home() / ".runpod" / "api_key"
API_BASE = "https://api.runpod.io/graphql"


def load_key():
    return KEY_FILE.read_text().strip()


def graphql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = subprocess.run([
        "curl", "-s", API_BASE,
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {load_key()}",
        "-d", json.dumps(payload)
    ], capture_output=True, text=True, timeout=30)
    return json.loads(r.stdout)


def create_pod(name="sov4-train", gpu="NVIDIA A40", image="runpod/pytorch:2.4.0-py3.10-cuda12.4.0-devel-ubuntu22.04"):
    """Create a pod with PyTorch + CUDA 12.4 + Jupyter + SSH."""
    print(f"=== Creating pod: {name} ===")
    print(f"  GPU: {gpu}")
    print(f"  Image: {image}")
    mutation = """
    mutation CreatePod($input: PodFindAndDeployOnDemandInput!) {
        podFindAndDeployOnDemand(input: $input) {
            id
            desiredStatus
        }
    }
    """
    variables = {
        "input": {
            "name": name,
            "imageName": image,
            "gpuTypeId": gpu,
            "gpuCount": 1,
            "containerDiskInGb": 50,
            "volumeInGb": 200,
            "ports": "22/tcp,8888/http,11434/http",
        }
    }
    result = graphql(mutation, variables)
    pod = result.get("data", {}).get("podFindAndDeployOnDemand", {})
    if pod.get("id"):
        print(f"  Pod created: {pod['id']}")
        return pod["id"]
    print(f"  FAILED: {result}")
    return None


def wait_for_pod(pod_id, timeout=300):
    """Wait for pod to be RUNNING with SSH port."""
    import socket
    print(f"Waiting for {pod_id}...")
    start = time.time()
    while time.time() - start < timeout:
        r = graphql("{ pod(input: {id: \"%s\"}) { id desiredStatus machine { gpuTypeId } runtime { uptimeSeconds } } }" % pod_id)
        pod = r.get("data", {}).get("pod", {})
        if not pod:
            time.sleep(5)
            continue
        status = pod.get("desiredStatus")
        print(f"  status={status} uptime={pod.get('runtime', {}).get('uptimeSeconds', 0)}s")
        if status == "RUNNING":
            # check SSH
            public_ip = pod.get("machine", {}).get("publicIp")  # not always present
            time.sleep(5)
            return pod
        time.sleep(10)
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        gpu = sys.argv[2] if len(sys.argv) > 2 else "NVIDIA A40"
        pod_id = create_pod(gpu=gpu)
        if pod_id:
            wait_for_pod(pod_id)
    else:
        print("usage: python3 runpod_create_clean.py create [GPU_TYPE]")
        print("  GPU types: NVIDIA A40, NVIDIA H100 PCIe, NVIDIA GeForce RTX 3090")
