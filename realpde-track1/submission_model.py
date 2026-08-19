"""
Track 1 (Sim2Real) submission — NeurIPS 2026 RealPDE Competition.

Interface (from the official Submission page):
    class SubmissionModel:
        def __init__(self, submission_dir=None, device="cpu"): ...
        def predict(self, input_array, metadata=None):
            -> np.ndarray (N, T_out=20, H=32, W=64, C=3)
            or dict {"prediction": pred, "lower": lo, "upper": hi}

    Optional load_checkpoint(path, device) called when model.pth exists.

Same FNO3d surrogate as Track 2 (single model serves both tracks); the
predict() path is batch inference without adaptation. Optional calibrated
uncertainty bounds (lower/upper) for the SPS subscore.
"""

import os
import numpy as np
import torch
import torch.nn.functional as F

from submission import FNO3d, load_state_dict_any

# Default stats (fit on the official train_real release, excluding 7575_0,
# at 32x64 via 2x strided subsampling). Updated by training pipeline output
# stats_real.npz — see bake_stats() below.
DEFAULT_MEAN = np.array([0.15401423, -0.00055775, 0.0], dtype=np.float32)
DEFAULT_STD = np.array([0.11456379, 0.015575, 1.0], dtype=np.float32)


class SubmissionModel:
    def __init__(self, submission_dir=None, device="cpu"):
        self.device = device
        self.model = FNO3d().to(device)
        self.submission_dir = submission_dir
        self.mean = DEFAULT_MEAN.copy()
        self.std = DEFAULT_STD.copy()
        if submission_dir:
            ckpt = os.path.join(submission_dir, "model.pth")
            if os.path.exists(ckpt):
                self.load_checkpoint(ckpt, device)
            st = os.path.join(submission_dir, "stats.npz")
            if os.path.exists(st):
                s = np.load(st)
                self.mean = s["mean"].astype(np.float32)
                self.std = s["std"].astype(np.float32)
                self.std = np.where(self.std == 0, 1.0, self.std)
        self.model.eval()
        self._mc_dropout = False  # set True to return calibrated bounds

    def load_checkpoint(self, path, device="cpu"):
        load_state_dict_any(self.model, path)
        self.model.to(device).eval()

    def predict(self, input_array, metadata=None):
        x = torch.from_numpy(np.asarray(input_array, dtype=np.float32)).to(self.device)
        # Normalize to the model's training space (raw inputs on Track 1).
        m = torch.from_numpy(self.mean).to(self.device)
        s = torch.from_numpy(self.std).to(self.device)
        x = (x - m) / s
        with torch.no_grad():
            if self._mc_dropout:
                self._enable_dropout()
                preds = torch.stack([self.model(x) for _ in range(8)], dim=0)
                pred = preds.mean(0)
                std = preds.std(0)
                self.model.eval()
                # denormalize bounds back to raw space
                lower = pred * s + m - 1.96 * std * s
                upper = pred * s + m + 1.96 * std * s
                pred = pred * s + m
                return {
                    "prediction": pred.cpu().numpy(),
                    "lower": lower.cpu().numpy(),
                    "upper": upper.cpu().numpy(),
                }
            pred = self.model(x) * s + m
        return pred.cpu().numpy()

    def _enable_dropout(self):
        for m in self.model.modules():
            if m.__class__.__name__.startswith("Dropout"):
                m.train()
