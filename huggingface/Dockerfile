FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    "torch==2.4.1" \
    "transformers==4.45.2" \
    "datasets==2.21.0" \
    "accelerate==0.34.2" \
    "gradio==4.42.0" \
    "huggingface_hub==0.25.2" \
    "bitsandbytes==0.43.3"

COPY app.py /app/app.py
COPY sov33_benchmark_general.py /app/sov33_benchmark_general.py
COPY sov33_benchmark_agentic.py /app/sov33_benchmark_agentic.py
COPY harness_loader.py /app/harness_loader.py

ENV PYTHONUNBUFFERED=1 \
    SOV33_OUT_DIR=/data/bench-results \
    HF_HOME=/data/hf_cache \
    TRANSFORMERS_CACHE=/data/hf_cache \
    HF_DATASETS_CACHE=/data/hf_cache/datasets

RUN mkdir -p /data/bench-results /data/hf_cache

EXPOSE 7860

CMD ["python", "app.py"]