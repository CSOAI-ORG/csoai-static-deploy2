"""
Build Track 2 (LTTTA) submission archive: submission.py + fp16-packed model.

Usage:
    python package_submission.py --model model.pth --out submission.zip
        [--stats stats_real.npz] [--pack-fp16]

Rules:
  - archive < 256 MB after extraction (checkpoint included)
  - submission.py must expose get_ttt_model(submission_dir, device)
  - model weights named model.pth in the archive root
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile


def pack_fp16(src, dst):
    """Complex-safe fp16 pack (mirrors the official pack_ckpt_fp16.py)."""
    import torch
    ckpt = torch.load(src, map_location="cpu", weights_only=False)
    sd = ckpt["model_state_dict"] if isinstance(ckpt, dict) and "model_state_dict" in ckpt else ckpt
    packed, complex_keys = {}, []
    for k, v in sd.items():
        if torch.is_tensor(v) and v.is_complex():
            packed[k] = torch.view_as_real(v).half()
            complex_keys.append(k)
        elif torch.is_tensor(v) and torch.is_floating_point(v):
            packed[k] = v.half()
        else:
            packed[k] = v
    torch.save({"state_fp16": packed, "complex_keys": complex_keys}, dst)
    print(f"packed {src} -> {dst}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stats", default="")
    ap.add_argument("--pack-fp16", action="store_true")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as td:
        # submission.py from the track2 package (self-contained FNO + controller)
        shutil.copy("/root/realpde/submission.py", os.path.join(td, "submission.py"))
        if args.pack_fp16:
            pack_fp16(args.model, os.path.join(td, "model.pth"))
        else:
            shutil.copy(args.model, os.path.join(td, "model.pth"))
        if args.stats and os.path.exists(args.stats):
            shutil.copy(args.stats, os.path.join(td, "stats.npz"))
        # zip it
        with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in os.listdir(td):
                zf.write(os.path.join(td, f), f)
        size_mb = os.path.getsize(args.out) / 1e6
        print(f"archive: {args.out} ({size_mb:.1f} MB)")
        if size_mb > 256:
            print("WARNING: exceeds 256 MB submission cap!")
        else:
            print("OK: under 256 MB cap")


if __name__ == "__main__":
    main()
