# Oracle Cloud GPU Setup — $300 Free Credits

## Step 1: Sign Up for Oracle Cloud Free Tier

1. Go to https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Fill in your details:
   - Email
   - Name
   - Country
   - Credit/Debit card (for verification only, won't be charged)
4. Verify your email
5. Complete the sign-up process

## Step 2: Request GPU Quota

1. Sign in to Oracle Cloud Console: https://cloud.oracle.com
2. Click on the hamburger menu (top left)
3. Go to "Governance & Administration" > "Tenancy Details"
4. Click "Request Service Limit Increase"
5. Select "Compute" as the service
6. Select "GPU" as the resource
7. Request quota for:
   - VM.GPU.A10.1 (NVIDIA A10, 1 GPU, 24GB VRAM)
   - Or VM.GPU.A10.2 (NVIDIA A10, 2 GPUs, 48GB VRAM)
8. Submit the request

## Step 3: Launch GPU Instance

Once quota is approved:

### Using Console
1. Go to "Compute" > "Instances"
2. Click "Create Instance"
3. Select:
   - Name: "sov33-gpu-training"
   - Compartment: root
   - Availability Domain: AD-1
   - Image: NVIDIA GPU Cloud Machine Image
   - Shape: VM.GPU.A10.1
   - VCN: Create new or select existing
   - Subnet: Create new or select existing
   - SSH keys: Upload your public key
4. Click "Create"

### Using CLI
```bash
# Install OCI CLI
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"

# Configure OCI CLI
oci setup config

# Launch GPU instance
oci compute instance launch \
  --availability-domain "xxxxx" \
  --compartment-id "ocid1.tenancy.oc1..xxxxx" \
  --shape "VM.GPU.A10.1" \
  --image-id "ocid1.image.oc1..xxxxx" \
  --subnet-id "ocid1.subnet.oc1..xxxxx" \
  --ssh-authorized-keys-file ~/.ssh/id_rsa.pub \
  --display-name "sov33-gpu-training"
```

## Step 4: Set Up GPU Instance

SSH into the instance:
```bash
ssh opc@<instance-ip>
```

Install dependencies:
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker opc

# Install NVIDIA drivers
sudo apt-get install -y nvidia-driver-535
sudo reboot

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

## Step 5: Deploy SOV33 Training

```bash
# Pull Ollama with GPU support
docker run -d --gpus all \
  --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama

# Pull base model
docker exec ollama ollama pull qwen2.5:0.5b

# Create training script
cat > train_sov33.sh << 'EOF'
#!/bin/bash
set -e

# Create Modelfile
cat > Modelfile << 'MODELFILE'
FROM qwen2.5:0.5b
SYSTEM "You are SOV33-Ultimate-Sovereign, a sovereign AI with integrated governance, security, and defence."
PARAMETER temperature 0
PARAMETER num_predict 128
MODELFILE

# Create model
docker exec ollama ollama create sov33-ultimate-sovereign -f Modelfile

# Test model
docker exec ollama ollama run sov33-ultimate-sovereign "What is the EU AI Act Article 50?"
EOF

chmod +x train_sov33.sh
./train_sov33.sh
```

## Step 6: Continuous Training Pipeline

```bash
# Create training pipeline
cat > training_pipeline.sh << 'EOF'
#!/bin/bash
set -e

# Download training data from Oracle ARM
scp -r ubuntu@145.241.232.16:~/csoai-hub/training/ ./training/

# Train LoRA adapters
python3 train_lora.py \
  --model qwen2.5:0.5b \
  --data training/ \
  --output ./adapters/ \
  --epochs 3 \
  --batch-size 4

# Export quantized model
ollama create sov33-trained -f Modelfile.trained

# Upload to Oracle ARM
scp ./adapters/* ubuntu@145.241.232.16:~/csoai-hub/adapters/
EOF

chmod +x training_pipeline.sh
```

## Step 7: Set Up Cron for Continuous Training

```bash
# Add to crontab
crontab -e

# Add these lines:
# Train every 4 hours
0 */4 * * * /home/opc/training_pipeline.sh >> /home/opc/training.log 2>&1

# Backup to Oracle ARM every hour
0 * * * * rsync -avz /home/opc/training/ ubuntu@145.241.232.16:~/csoai-hub/training/ >> /home/opc/sync.log 2>&1
```

## Cost Analysis

### Oracle Free Tier
- $300 free credits for 30 days
- VM.GPU.A10.1: ~$3.50/hour
- 300 / 3.50 = ~85 hours of GPU training

### Always Free (After 30 days)
- ARM Ampere A1: 4 OCPU, 24GB RAM (Always Free)
- 200GB storage (Always Free)
- 10TB outbound transfer (Always Free)

### Strategy
1. Use $300 credits for initial GPU training (85 hours)
2. Export trained models to Oracle ARM (Always Free)
3. Run inference on Oracle ARM (Always Free)
4. Use Kaggle/Colab/Lightning for additional GPU needs

## Expected Results

### After GPU Training
- 12 OWEM specialists trained
- LoRA adapters for each specialist
- Quantized models for fast inference
- 2-3x performance improvement

### 24/7 Operation
- Oracle ARM: Always Free (inference)
- Kaggle T4: 30 hours/week (training)
- Colab T4: 12 hours/session (training)
- Lightning T4: 22 hours/month (training)

## Next Steps

1. [ ] Sign up for Oracle Cloud Free Tier
2. [ ] Request GPU quota
3. [ ] Launch GPU instance
4. [ ] Set up training pipeline
5. [ ] Train OWEM specialists
6. [ ] Deploy to Oracle ARM
7. [ ] Set up continuous training
