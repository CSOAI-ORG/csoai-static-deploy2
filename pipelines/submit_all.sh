#!/bin/bash
# SOV5v2 Submit All — One command to enter everything

echo "=== SOV5v2 E2E SUBMISSION ==="

# 1. Submit to Kaggle
echo "1. Submitting to Kaggle..."
export KAGGLE_API_TOKEN="KGAT_d72d5146a3b5622d24bac06eaf4004f2"
cd /Users/nicholas/clawd/csoai-static-deploy2/kaggle
kaggle competitions submit llm-classification-finetuning \
    -f submissions/llm_classification.csv \
    -m "SOV5v2 sovereign AI model" 2>&1 | tail -3

# 2. Publish to HuggingFace
echo ""
echo "2. Publishing to HuggingFace..."
cd /Users/nicholas/clawd/csoai-static-deploy2/pipelines/huggingface
python3 publish_to_hf.py

# 3. Run benchmark
echo ""
echo "3. Running benchmark..."
cd /Users/nicholas/clawd/csoai-static-deploy2
python3 benchmark-results/sov33_agent_loop.py --benchmark gaia --model sov5v2 2>&1 | tail -5

echo ""
echo "=== ALL SUBMISSIONS COMPLETE ==="
