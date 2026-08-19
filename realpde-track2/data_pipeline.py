"""
Track 2 data pipeline: h5 -> normalized streaming windows + TTT driver.

Mirrors the official stream layout:
  - raw fields 64x128, evaluated at 32x64 (2x spatial downsample)
  - windows: 20 input frames -> 20 target frames, stride 20
  - trajectory boundaries announced via reset_ttt_state()
  - normalization uses official train_real statistics (computed on the
    released train_real split, excluding 7575_0)
"""

import os
import glob
import time
import numpy as np
import h5py
import torch


def downsample_2x(field):
    """64x128 -> 32x64 via 2x2 average pooling."""
    f = field.astype(np.float64)
    return (f[:, 0::2, 0::2] + f[:, 0::2, 1::2] +
            f[:, 1::2, 0::2] + f[:, 1::2, 1::2]) / 4.0


def load_h5(path, channels=("u", "v"), add_p=False):
    """Load u,v (and optionally zero p) -> (T, 32, 64, C)."""
    out = []
    with h5py.File(path, "r") as f:
        for ch in channels:
            out.append(downsample_2x(f[ch][:]))
    x = np.stack(out, axis=-1)  # (T, 32, 64, C)
    if add_p:
        p = np.zeros((x.shape[0], x.shape[1], x.shape[2], 1), dtype=np.float64)
        x = np.concatenate([x, p], axis=-1)
    return x


def normalize(x, stats):
    """x: (T, H, W, C). Per-channel Gaussian normalization using train_real stats.
    p channel (index 2) is normalized with mean 0, std 1 (it is zero-filled)."""
    x = x.copy()
    x[..., 0] = (x[..., 0] - stats["mean_u"]) / stats["std_u"]
    x[..., 1] = (x[..., 1] - stats["mean_v"]) / stats["std_v"]
    if x.shape[-1] > 2:
        x[..., 2] = x[..., 2] / 1.0
    return x.astype(np.float32)


def make_windows(traj, in_step=20, out_step=20, stride=20):
    """Cut a trajectory (T,H,W,C) into (input, target) window pairs."""
    ins, outs = [], []
    T = traj.shape[0]
    i = 0
    while i + in_step + out_step <= T:
        ins.append(traj[i:i + in_step])
        outs.append(traj[i + in_step:i + in_step + out_step])
        i += stride
    if not ins:
        return np.zeros((0, in_step) + traj.shape[1:], dtype=np.float32), \
               np.zeros((0, out_step) + traj.shape[1:], dtype=np.float32)
    return np.stack(ins), np.stack(outs)


def load_trajectory_normed(path, stats, add_p=True):
    """Return normalized (T,32,64,3) trajectory."""
    x = load_h5(path, add_p=add_p)
    return normalize(x, stats)


def run_ttt_stream(model, windows_in, windows_out, device="cpu"):
    """Stream windows one by one through a TTT model.
    Returns preds, targets, step_times, adapt_losses, (lowers, uppers)."""
    preds, targets, step_times, adapt_losses = [], [], [], []
    lowers, uppers = [], []
    prev_target = None
    model.reset_ttt_state()
    for k, (win_in, win_out) in enumerate(zip(windows_in, windows_out)):
        inp = torch.from_numpy(win_in[None]).to(device)
        prev_t = (torch.from_numpy(prev_target[None]).to(device)
                  if prev_target is not None else None)
        t0 = time.perf_counter()
        pred, info = model.ttt_step(inp, prev_t)
        step_times.append(time.perf_counter() - t0)
        preds.append(pred.numpy() if isinstance(pred, torch.Tensor) else pred)
        targets.append(win_out[None])
        adapt_losses.append(info.get("adapt_loss"))
        if "lower" in info and "upper" in info:
            lo = info["lower"]
            hi = info["upper"]
            lowers.append(lo.numpy() if isinstance(lo, torch.Tensor) else lo)
            uppers.append(hi.numpy() if isinstance(hi, torch.Tensor) else hi)
        prev_target = win_out  # official stream: previous window's target revealed
    return preds, targets, step_times, adapt_losses, (lowers, uppers)


def main():
    import sys
    from local_eval import score_run

    stats = np.load("/root/realpde/train_real_stats.npz")
    stats = {k: float(v) for k, v in stats.items()}
    print("stats:", stats)

    data_root = "/root/realpde/data"
    # use a couple of train_real trajectories as a local validation stream
    real_files = sorted(glob.glob(os.path.join(data_root, "train_real", "*.h5")))
    real_files = [f for f in real_files if not f.endswith("7575_0.h5")]
    val_files = real_files[:2]  # fast local check; expand later
    print("val files:", [os.path.basename(f) for f in val_files])

    import submission
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = submission.get_ttt_model("/root/realpde/data/baseline_checkpoints/sim_real_ft",
                                     device)

    all_preds, all_targets, all_times, all_adapt = [], [], [], []
    all_lo, all_hi = [], []
    for f in val_files:
        traj = load_trajectory_normed(f, stats)
        wins_in, wins_out = make_windows(traj)
        print(f"{os.path.basename(f)}: {len(wins_in)} windows")
        preds, targets, times, adapt, (lo, hi) = run_ttt_stream(model, wins_in, wins_out, device)
        all_preds += preds
        all_targets += targets
        all_times += times
        all_adapt += adapt
        all_lo += lo
        all_hi += hi

    lo_arr = np.concatenate(all_lo) if all_lo else None
    hi_arr = np.concatenate(all_hi) if all_hi else None
    res = score_run(all_preds, all_targets, all_times, lo_arr, hi_arr, stats)
    for k, v in res.items():
        print(f"{k}: {v:.4f}")
    n_adapt = sum(1 for a in all_adapt if a is not None)
    print(f"adapt steps taken: {n_adapt}/{len(all_adapt)}")


if __name__ == "__main__":
    main()
