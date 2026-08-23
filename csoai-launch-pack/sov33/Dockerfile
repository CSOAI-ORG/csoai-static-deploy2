FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

WORKDIR /workspace

# Install deps
RUN pip install --no-cache-dir \
    torch transformers accelerate bitsandbytes \
    peft trl datasets \
    safetensors sentencepiece protobuf \
    huggingface-hub kaggle \
    pyyaml requests rich

# Install sovereign dependencies
RUN pip install --no-cache-dir \
    numpy pandas matplotlib scipy \
    fastapi uvicorn

# Clone sovereign repo
RUN git clone https://github.com/CSOAI-ORG/csoai-sovereign.git || true

# Copy sovereign code
COPY . /workspace/sov33-master-takeover/
WORKDIR /workspace/sov33-master-takeover

# Make all modules executable
RUN chmod +x /workspace/sov33-master-takeover/sov33/*.py

# Default entrypoint: run govbench + emit sigils
CMD ["bash", "-c", "python3 sov33/govbench_takeover.py && python3 sov33/master_takeover.py"]
