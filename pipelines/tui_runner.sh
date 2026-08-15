#!/bin/bash
# TUI Runner — Execute on each training site

SITE=$1
MODEL=$2

case $SITE in
    kaggle)
        echo "Running on Kaggle T4..."
        python3 pipelines/workflows/kaggle_workflow.py
        ;;
    colab)
        echo "Running on Colab T4..."
        python3 pipelines/workflows/colab_workflow.py
        ;;
    oracle)
        echo "Running on Oracle ARM..."
        python3 pipelines/workflows/oracle_workflow.py
        ;;
    huggingface)
        echo "Running on HuggingFace..."
        python3 pipelines/workflows/huggingface_workflow.py
        ;;
    github)
        echo "Running on GitHub..."
        python3 pipelines/workflows/github_workflow.py
        ;;
    papers-with-code)
        echo "Running on Papers With Code..."
        python3 pipelines/workflows/papers-with-code_workflow.py
        ;;
    lmarena)
        echo "Running on LMArena..."
        python3 pipelines/workflows/lmarena_workflow.py
        ;;
    aimo)
        echo "Running on AIMO..."
        python3 pipelines/workflows/aimo_workflow.py
        ;;
    *)
        echo "Unknown site: $SITE"
        ;;
esac
