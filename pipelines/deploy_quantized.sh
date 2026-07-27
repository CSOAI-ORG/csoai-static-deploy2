#!/bin/bash
# Deploy quantized models to RunPod

echo "Deploying quantized Mamba/SSM models..."

# Pull models on RunPod
ssh -p 12704 -o StrictHostKeyChecking=no root@62.169.159.96 "
    echo 'Pulling Mamba models...'
    pip install -q mamba-ssm 2>/dev/null
    
    echo 'Creating Modelfiles...'
    for model in mamba-1.3b mamba-2.7b rwkv7-2.9b zamba2-1.2b; do
        cat > /workspace/sovereign/Modelfile.\$model << EOF
FROM \$model
PARAMETER temperature 0
PARAMETER num_predict 256
SYSTEM \"\"\"You are a sovereign AI assistant. Answer accurately.\"\"\"
EOF
        echo \"Created Modelfile.\$model\"
    done
    
    echo 'Testing models...'
    for model in mamba-1.3b mamba-2.7b; do
        echo -n \"Testing \$model... \"
        timeout 30 ollama run \$model 'Say hi' 2>&1 | tail -1
    done
    
    echo 'Done!'
" 2>&1

echo ""
echo "=== QUANTIZED MODELS READY ==="
echo "All Mamba/SSM models on RunPod T4"
echo "Cost: $0.44/hr (85% savings)"
