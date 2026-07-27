#!/usr/bin/env python3
"""
SOV33-Ultimate-Sovereign — HuggingFace Spaces App
Provides GPU-accelerated inference for the sovereign AI model.
"""
import gradio as gr
import json
import subprocess
import time
from datetime import datetime, timezone

MODEL_NAME = "sov33-ultimate-sovereign"

def chat(message, history):
    """Chat with the model."""
    try:
        # Try Ollama first
        payload = json.dumps({
            "model": MODEL_NAME,
            "prompt": message,
            "stream": False,
            "options": {"temperature": 0, "num_predict": 256}
        })
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/generate", "-H", "Content-Type: application/json", "-d", payload],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("response", "No response from model")
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_status():
    """Get model status."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if MODEL_NAME in result.stdout:
            return f"✅ Model {MODEL_NAME} loaded"
        else:
            return f"⚠️ Model {MODEL_NAME} not found"
    except:
        return "❌ Ollama not available"

# Create Gradio interface
with gr.Blocks(title="SOV33-Ultimate-Sovereign", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🦁 SOV33-Ultimate-Sovereign
    
    **World-class sovereign AI with integrated governance, security, and defence.**
    
    - **Arena Composite**: 72.5%
    - **Perfect Scores**: 100% safety_red_team, 100% code_generation
    - **Capabilities**: EU AI Act, GDPR, ISO 42001, NIST AI RMF, BFT-33, DEFONEOS, AUKUS
    """)
    
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(height=400)
            msg = gr.Textbox(label="Message", placeholder="Ask about EU AI Act, GDPR, BFT-33, DEFONEOS...")
            submit = gr.Button("Submit", variant="primary")
            
            def respond(message, history):
                response = chat(message, history)
                history.append((message, response))
                return "", history
            
            submit.click(respond, [msg, chatbot], [msg, chatbot])
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
        
        with gr.Column():
            status = gr.Markdown(get_status())
            
            gr.Markdown("""
            ### Example Questions
            
            - What is the EU AI Act Article 50?
            - What is GDPR Article 33?
            - What is ISO 42001?
            - What is NIST AI RMF?
            - What is BFT-33 quorum?
            - What is DEFONEOS?
            - Write Python binary search
            - What is 7 factorial?
            """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
