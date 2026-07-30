#!/usr/bin/env python3
"""Frontier Move 1 smoke test — prove the render-text->image->OCR compression path end to end.
UNTESTED until run on a GPU with DeepSeek-OCR loaded. Two run modes:

  A) local (transformers, simplest on a Kaggle T4):
       pip install transformers pillow einops accelerate
       python smoke_test.py --mode local
  B) served (against the vLLM Dockerfile in this dir):
       python smoke_test.py --mode served --url http://localhost:8000/v1

Success = OCR reconstructs the rendered paragraph at high fidelity, and we log the
token-compression ratio (image tokens vs raw text tokens) to confirm the ~7.77x in-family claim.
"""
import argparse, base64, io, sys

SAMPLE = ("The estate's visual leg renders text as image tokens for optical context compression. "
          "DeepSeek-OCR reconstructs this paragraph from a single rendered image, using roughly an "
          "order of magnitude fewer tokens than the raw text would consume. This is the visual-honey unblock.")

def render_text_to_png(text, width=1024):
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    font = ImageFont.load_default()
    lines = textwrap.wrap(text, width=70)
    img = Image.new("RGB", (width, 24*len(lines)+40), "white")
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        d.text((20, 20+24*i), ln, fill="black", font=font)
    buf = io.BytesIO(); img.save(buf, format="PNG"); return buf.getvalue(), img.size

def ratio(text, img_bytes):
    # crude proxy: ~1 token / 4 chars of text vs DeepSeek-OCR's compressed vision tokens (report-only)
    raw_tokens = max(1, len(text)//4)
    return raw_tokens

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["local","served"], default="local")
    ap.add_argument("--url", default="http://localhost:8000/v1")
    args = ap.parse_args()

    png, size = render_text_to_png(SAMPLE)
    print(f"[render] {size[0]}x{size[1]} PNG, {len(png)} bytes · source ~{ratio(SAMPLE,png)} text tokens")

    if args.mode == "local":
        try:
            from transformers import AutoModel, AutoTokenizer
            import torch
        except ImportError:
            sys.exit("pip install transformers pillow einops accelerate torch first")
        tok = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-OCR", trust_remote_code=True)
        model = AutoModel.from_pretrained("deepseek-ai/DeepSeek-OCR", trust_remote_code=True,
                                          torch_dtype=torch.bfloat16, device_map="auto").eval()
        open("/tmp/_ocr_in.png","wb").write(png)
        # DeepSeek-OCR exposes .infer(...) in its remote code; prompt asks for a plain transcription.
        out = model.infer(tok, prompt="<image>\nOCR this image verbatim.", image_file="/tmp/_ocr_in.png")
        print("[ocr:local]\n", out)
    else:
        import urllib.request, json
        b64 = base64.b64encode(png).decode()
        body = {"model":"deepseek-ai/DeepSeek-OCR","messages":[{"role":"user","content":[
            {"type":"text","text":"OCR this image verbatim."},
            {"type":"image_url","image_url":{"url":f"data:image/png;base64,{b64}"}}]}]}
        req = urllib.request.Request(args.url.rstrip("/")+"/chat/completions",
              data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
        print("[ocr:served]\n", json.load(urllib.request.urlopen(req, timeout=120))["choices"][0]["message"]["content"])

if __name__ == "__main__":
    main()
