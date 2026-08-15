# Frontier Move 1 — DeepSeek-OCR on vLLM (the visual-honey leg unblock)
# UNTESTED until run on a CUDA GPU (Kaggle T4 / HF Space / RunPod pod). This is the
# purpose-built image the 07-24 SOV4 synthesis said was the ONLY wall on the visual leg.
# DeepSeek-OCR ("Contexts Optical Compression"): render text -> vision tokens, ~10-20x fewer
# tokens at ~97% precision. Our measured 7.77x is in-family. Design is RIGHT; this image unblocks it.
FROM vllm/vllm-openai:v0.8.5

# DeepSeek-OCR support landed in vLLM 0.8.5+; pin transformers to a version that carries the modeling code.
RUN pip install --no-cache-dir \
    "transformers>=4.47" \
    "pillow" "einops" "accelerate" \
    "huggingface_hub[cli]"

ENV MODEL_ID=deepseek-ai/DeepSeek-OCR
ENV HF_HOME=/root/.cache/huggingface

# Serve an OpenAI-compatible endpoint; --trust-remote-code required for the OCR modeling code.
EXPOSE 8000
ENTRYPOINT ["python3","-m","vllm.entrypoints.openai.api_server", \
  "--model","deepseek-ai/DeepSeek-OCR","--trust-remote-code", \
  "--max-model-len","8192","--gpu-memory-utilization","0.90","--port","8000"]
