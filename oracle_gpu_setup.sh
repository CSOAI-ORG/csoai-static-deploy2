#!/bin/bash
# oracle_gpu_setup.sh — Set up Oracle GPU instance for SOV33 training
set -euo pipefail

echo "=== ORACLE GPU SETUP FOR SOV33 TRAINING ==="
echo ""

# Check if OCI CLI is installed
if ! command -v oci &> /dev/null; then
    echo "[1/5] Installing OCI CLI..."
    bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" --accept-all-defaults
    echo "  OK"
else
    echo "[1/5] OCI CLI already installed"
fi

# Check if configured
if [ ! -f ~/.oci/config ]; then
    echo "[2/5] Configuring OCI CLI..."
    echo "  Please run: oci setup config"
    echo "  Then run this script again"
    exit 1
else
    echo "[2/5] OCI CLI configured"
fi

# Get tenancy OCID
echo "[3/5] Getting tenancy info..."
TENANCY_ID=$(oci iam tenancy list --query 'data[0].id' --raw-output 2>/dev/null || echo "")
if [ -z "$TENANCY_ID" ]; then
    echo "  Error: Could not get tenancy ID"
    exit 1
fi
echo "  Tenancy: $TENANCY_ID"

# Get availability domain
echo "[4/5] Getting availability domain..."
AD=$(oci iam availability-domain list --query 'data[0].name' --raw-output 2>/dev/null || echo "")
if [ -z "$AD" ]; then
    echo "  Error: Could not get availability domain"
    exit 1
fi
echo "  AD: $AD"

# Check GPU quota
echo "[5/5] Checking GPU quota..."
GPU_QUOTA=$(oci limits resource-availability \
  --service-name compute \
  --limit-name vm-gpu-a1-count \
  --availability-domain "$AD" \
  --query 'available' \
  --raw-output 2>/dev/null || echo "0")

if [ "$GPU_QUOTA" = "0" ] || [ -z "$GPU_QUOTA" ]; then
    echo "  ⚠️  No GPU quota available"
    echo "  Please request GPU quota in Oracle Cloud Console:"
    echo "  1. Go to https://cloud.oracle.com"
    echo "  2. Menu > Governance & Administration > Tenancy Details"
    echo "  3. Click 'Request Service Limit Increase'"
    echo "  4. Select 'Compute' > 'GPU'"
    echo "  5. Request VM.GPU.A10.1"
    echo ""
    echo "  After quota is approved, run this script again"
    exit 1
fi

echo "  ✅ GPU quota available: $GPU_QUOTA"
echo ""

# Launch GPU instance
echo "=== LAUNCHING GPU INSTANCE ==="
echo "Shape: VM.GPU.A10.1"
echo "Image: NVIDIA GPU Cloud Machine Image"
echo ""

# Get VCN and subnet
VCN_ID=$(oci network vcn list \
  --compartment-id "$TENANCY_ID" \
  --query 'data[0].id' \
  --raw-output 2>/dev/null || echo "")

if [ -z "$VCN_ID" ]; then
    echo "Creating VCN..."
    VCN_ID=$(oci network vcn create \
      --compartment-id "$TENANCY_ID" \
      --cidr-blocks '["10.0.0.0/16"]' \
      --display-name "sov33-vcn" \
      --query 'data.id' \
      --raw-output 2>/dev/null || echo "")
fi

SUBNET_ID=$(oci network subnet list \
  --compartment-id "$TENANCY_ID" \
  --vcn-id "$VCN_ID" \
  --query 'data[0].id' \
  --raw-output 2>/dev/null || echo "")

if [ -z "$SUBNET_ID" ]; then
    echo "Creating subnet..."
    SUBNET_ID=$(oci network subnet create \
      --compartment-id "$TENANCY_ID" \
      --vcn-id "$VCN_ID" \
      --cidr-block "10.0.0.0/24" \
      --display-name "sov33-subnet" \
      --query 'data.id' \
      --raw-output 2>/dev/null || echo "")
fi

# Get GPU image OCID
IMAGE_ID=$(oci compute image list \
  --compartment-id "$TENANCY_ID" \
  --operating-system "NVIDIA GPU Cloud" \
  --query 'data[0].id' \
  --raw-output 2>/dev/null || echo "")

if [ -z "$IMAGE_ID" ]; then
    echo "Error: Could not find NVIDIA GPU Cloud image"
    echo "Please check: https://docs.oracle.com/en-us/iaas/Content/Compute/References/ngcimage.htm"
    exit 1
fi

echo "Launching instance..."
INSTANCE_ID=$(oci compute instance launch \
  --availability-domain "$AD" \
  --compartment-id "$TENANCY_ID" \
  --shape "VM.GPU.A10.1" \
  --image-id "$IMAGE_ID" \
  --subnet-id "$SUBNET_ID" \
  --ssh-authorized-keys-file ~/.ssh/id_rsa.pub \
  --display-name "sov33-gpu-training" \
  --query 'data.id' \
  --raw-output 2>/dev/null || echo "")

if [ -z "$INSTANCE_ID" ]; then
    echo "Error: Could not launch instance"
    exit 1
fi

echo "✅ Instance launched: $INSTANCE_ID"
echo ""

# Wait for instance to be running
echo "Waiting for instance to be running..."
while true; do
    STATE=$(oci compute instance get \
      --instance-id "$INSTANCE_ID" \
      --query 'data."lifecycle-state"' \
      --raw-output 2>/dev/null || echo "")
    
    if [ "$STATE" = "RUNNING" ]; then
        echo "✅ Instance is running"
        break
    elif [ "$STATE" = "PROVISIONING" ] || [ "$STATE" = "STARTING" ]; then
        echo "  Provisioning..."
        sleep 30
    else
        echo "  Error: Instance state is $STATE"
        exit 1
    fi
done

# Get public IP
PUBLIC_IP=$(oci compute instance list-vnics \
  --instance-id "$INSTANCE_ID" \
  --query 'data[0]."public-ip"' \
  --raw-output 2>/dev/null || echo "")

if [ -z "$PUBLIC_IP" ]; then
    echo "Error: Could not get public IP"
    exit 1
fi

echo ""
echo "=== GPU INSTANCE READY ==="
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo ""
echo "SSH into the instance:"
echo "  ssh opc@$PUBLIC_IP"
echo ""
echo "Then run the training setup:"
echo "  bash oracle_gpu_train.sh"
