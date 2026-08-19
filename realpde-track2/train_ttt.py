"""
Track 2 training pipeline — sim pretrain → real finetune for the LTTTA
streaming surrogate.

Design notes:
  - Data: train_sim (pretrain) + train_real (finetune) from the official HF
    release; windowed 20→20, stride 20, 32x64 via 2x strided subsampling
    (matches RealPDEBench Foil sub_s=2 convention).
  - Normalization: per-channel z-score with stats fit on the training split
    (fit on train_real for the finetune stage; the official evaluator applies
    its own normalization, so the exact stats will be swapped from the
    starting kit when available — the pipeline takes a stats npz path).
  - Excludes train_real/7575_0.h5 per the official announcement.
  - Output: model.pth + stats.npz + train log; fp16 pack step for the
    256MB submission budget.
"""

import argparse
import glob
import json
import os
import re
import time

import h5py
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

from submission import FNO3d, load_state_dict_any


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def keyf(fn):
    m = re.match(r"(\d+)_(\d+)\.h5", os.path.basename(fn))
    return (float(m.group(1)), float(m.group(2)))


def down_stride(x):
    return x[:, ::2, ::2]


class FoilStream(Dataset):
    def __init__(self, root, split, in_step=20, out_step=20, stride=20,
                 stats_path=None, fit_stats=True, channels=("u", "v"),
                 add_p=True, exclude_bad=True):
        self.root = root
        self.in_step = in_step
        self.out_step = out_step
        self.stride = stride
        self.channels = list(channels)
        self.add_p = add_p
        files = sorted(glob.glob(os.path.join(root, split, "*.h5")), key=keyf)
        if exclude_bad:
            files = [f for f in files if not f.endswith("7575_0.h5")]
        self.files = files
        self.records = []  # (file_idx, t0)
        for fi, f in enumerate(files):
            with h5py.File(f, "r") as h:
                T = h["u"].shape[0]
            for t0 in range(0, T - (in_step + out_step) + 1, stride):
                self.records.append((fi, t0))
        # stats
        if stats_path and os.path.exists(stats_path):
            st = np.load(stats_path)
            self.mean = st["mean"].astype(np.float32)
            self.std = st["std"].astype(np.float32)
            self.std = np.where(self.std == 0, 1.0, self.std)
            self.fitted = False
        else:
            self.mean, self.std = self._fit_stats()
            self.fitted = True

    def _fit_stats(self):
        n = 0
        s = np.zeros(3 if self.add_p else len(self.channels), dtype=np.float64)
        s2 = np.zeros_like(s)
        for f in self.files:
            with h5py.File(f, "r") as h:
                cols = []
                for ch in self.channels:
                    cols.append(down_stride(h[ch][:].astype(np.float64)))
                arr = np.stack(cols, axis=-1)
                if self.add_p:
                    p = np.zeros(arr.shape[:-1] + (1,), dtype=np.float64)
                    arr = np.concatenate([arr, p], axis=-1)
            flat = arr.reshape(-1, arr.shape[-1])
            n += flat.shape[0]
            s += flat.sum(0)
            s2 += (flat ** 2).sum(0)
        mean = s / n
        std = np.sqrt(s2 / n - mean ** 2)
        std = np.where(std == 0, 1.0, std)
        return mean.astype(np.float32), std.astype(np.float32)

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        fi, t0 = self.records[idx]
        with h5py.File(self.files[fi], "r") as h:
            cols = []
            for ch in self.channels:
                cols.append(down_stride(h[ch][t0:t0 + self.in_step + self.out_step]
                                        .astype(np.float32)))
            data = np.stack(cols, axis=-1)
            if self.add_p:
                p = np.zeros(data.shape[:-1] + (1,), dtype=np.float32)
                data = np.concatenate([data, p], axis=-1)
        data = (data - self.mean) / self.std
        inp = torch.from_numpy(data[:self.in_step].copy())
        tgt = torch.from_numpy(data[self.in_step:].copy())
        return inp, tgt


def make_loader(root, split, batch_size, num_workers=4, **kw):
    ds = FoilStream(root, split, **kw)
    return ds, DataLoader(ds, batch_size=batch_size, shuffle=True,
                          num_workers=num_workers, pin_memory=True,
                          drop_last=True)


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def train_stage(model, loader, device, steps, lr, log_path, val_loader=None,
                val_every=250, clip=1.0, affine_aug=0.15):
    """Train with optional per-channel affine augmentation: each batch gets a
    random scale ~ N(1, affine_aug) and shift ~ N(0, affine_aug) applied per
    channel. Makes the model robust to the unknown official normalizer shift
    (the evaluator normalizes with its own train_real statistics)."""
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-5)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    log = []
    model.train()
    it = iter(loader)
    t0 = time.time()
    for step in range(1, steps + 1):
        try:
            inp, tgt = next(it)
        except StopIteration:
            it = iter(loader)
            inp, tgt = next(it)
        inp, tgt = inp.to(device), tgt.to(device)
        if affine_aug > 0:
            # random per-channel affine on both input and target (keeps the
            # prediction target consistent with the augmented input space)
            c = inp.shape[-1]
            scale = 1 + affine_aug * torch.randn(c, device=device)
            shift = affine_aug * torch.randn(c, device=device)
            inp = inp * scale.view(1, 1, 1, 1, c) + shift.view(1, 1, 1, 1, c)
            tgt = tgt * scale.view(1, 1, 1, 1, c) + shift.view(1, 1, 1, 1, c)
        opt.zero_grad()
        pred = model(inp)
        loss = F.mse_loss(pred, tgt)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), clip)
        opt.step()
        sched.step()
        if step % 50 == 0:
            el = time.time() - t0
            msg = (f"[{time.strftime('%H:%M:%S')}] step {step}/{steps} "
                   f"loss {loss.item():.6f} lr {sched.get_last_lr()[0]:.2e} "
                   f"({el:.0f}s)")
            print(msg, flush=True)
            log.append({"step": step, "loss": float(loss.item())})
            with open(log_path, "a") as f:
                f.write(msg + "\n")
        if val_loader is not None and step % val_every == 0:
            vloss = evaluate(model, val_loader, device)
            print(f"  val mse: {vloss:.6f}", flush=True)
            with open(log_path, "a") as f:
                f.write(f"  val mse: {vloss:.6f}\n")
    return log


def evaluate(model, loader, device):
    model.eval()
    tot, n = 0.0, 0
    with torch.no_grad():
        for inp, tgt in loader:
            inp, tgt = inp.to(device), tgt.to(device)
            pred = model(inp)
            tot += F.mse_loss(pred, tgt).item() * inp.size(0)
            n += inp.size(0)
            if n > 2000:
                break
    model.train()
    return tot / max(n, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/root/realpde/data")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--sim-steps", type=int, default=3000)
    ap.add_argument("--real-steps", type=int, default=3000)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--lr-sim", type=float, default=3e-4)
    ap.add_argument("--lr-real", type=float, default=1e-4)
    ap.add_argument("--init", default="", help="pretrained ckpt to start from")
    ap.add_argument("--out", default="/root/realpde/trained")
    ap.add_argument("--real-stats", default="", help="stats npz for real finetune")
    ap.add_argument("--affine", type=float, default=0.15, help="per-channel affine augmentation scale")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    print("device:", device, flush=True)

    model = FNO3d().to(device)
    if args.init:
        load_state_dict_any(model, args.init)
        print("initialized from", args.init, flush=True)

    # ---- stage 1: sim pretrain ----
    print("=== stage 1: sim pretrain ===", flush=True)
    sim_ds, sim_loader = make_loader(args.root, "train_sim", args.batch,
                                     stats_path=os.path.join(args.out, "stats_sim.npz"))
    if sim_ds.fitted:
        np.savez(os.path.join(args.out, "stats_sim.npz"),
                 mean=sim_ds.mean, std=sim_ds.std)
    train_stage(model, sim_loader, device, args.sim_steps, args.lr_sim,
                os.path.join(args.out, "train_sim.log"), affine_aug=args.affine)
    torch.save({"model_state_dict": model.state_dict()},
               os.path.join(args.out, "model_sim.pth"))

    # ---- stage 2: real finetune ----
    print("=== stage 2: real finetune ===", flush=True)
    real_ds, real_loader = make_loader(args.root, "train_real", args.batch,
                                       stats_path=args.real_stats or
                                       os.path.join(args.out, "stats_real.npz"))
    if real_ds.fitted:
        np.savez(os.path.join(args.out, "stats_real.npz"),
                 mean=real_ds.mean, std=real_ds.std)
    print("real stats mean:", real_ds.mean, "std:", real_ds.std, flush=True)
    train_stage(model, real_loader, device, args.real_steps, args.lr_real,
                os.path.join(args.out, "train_real.log"), affine_aug=args.affine)
    torch.save({"model_state_dict": model.state_dict()},
               os.path.join(args.out, "model.pth"))
    print("DONE ->", os.path.join(args.out, "model.pth"), flush=True)


if __name__ == "__main__":
    main()
