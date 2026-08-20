"""
Track 2 (LTTTA) submission — NeurIPS 2026 RealPDE Competition.

Interface contract (from the official Submission page):
    get_ttt_model(submission_dir, device) -> object with:
        reset_ttt_state(self) -> None
        ttt_step(self, input_norm, prev_target_norm=None) -> (pred_norm, info)

    input_norm       : (1, 20, 32, 64, 3) normalized input window
    prev_target_norm : (1, 20, 32, 64, 3) ground truth of previous step (or None)
    pred_norm        : (1, 20, 32, 64, 3) prediction
    info             : dict with "adapt_loss" (float or None) and optional
                       "lower"/"upper" normalized bounds of same shape as pred.

Architecture: OOWM-style agentic test-time adaptation controller on top of a
base FNO3d surrogate (official baseline architecture, width 64, 4 layers,
modes 4/12/16). The controller decides, per step, whether to adapt (gradient
steps on the revealed previous window) and how many steps to take, balancing
accuracy against the per-step time budget (t_numerical = 0.72896 s).
"""

import os
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# Model: FNO3d (matches official baseline sim_real_fno.pth state dict)
# ---------------------------------------------------------------------------
class SpectralConv3d(nn.Module):
    def __init__(self, in_channels, out_channels, modes1, modes2, modes3):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.modes1 = modes1
        self.modes2 = modes2
        self.modes3 = modes3
        self.scale = 1 / (in_channels * out_channels)
        self.weights1 = nn.Parameter(self.scale * torch.rand(in_channels, out_channels, modes1, modes2, modes3, dtype=torch.cfloat))
        self.weights2 = nn.Parameter(self.scale * torch.rand(in_channels, out_channels, modes1, modes2, modes3, dtype=torch.cfloat))
        self.weights3 = nn.Parameter(self.scale * torch.rand(in_channels, out_channels, modes1, modes2, modes3, dtype=torch.cfloat))
        self.weights4 = nn.Parameter(self.scale * torch.rand(in_channels, out_channels, modes1, modes2, modes3, dtype=torch.cfloat))

    def compl_mul3d(self, inp, weights):
        return torch.einsum("bixyz,ioxyz->boxyz", inp, weights)

    def forward(self, x):
        batchsize = x.shape[0]
        x_ft = torch.fft.rfftn(x, dim=[-3, -2, -1])
        out_ft = torch.zeros(batchsize, self.out_channels, x.size(-3), x.size(-2), x.size(-1) // 2 + 1, dtype=torch.cfloat, device=x.device)
        out_ft[:, :, :self.modes1, :self.modes2, :self.modes3] = self.compl_mul3d(
            x_ft[:, :, :self.modes1, :self.modes2, :self.modes3], self.weights1)
        out_ft[:, :, -self.modes1:, :self.modes2, :self.modes3] = self.compl_mul3d(
            x_ft[:, :, -self.modes1:, :self.modes2, :self.modes3], self.weights2)
        out_ft[:, :, :self.modes1, -self.modes2:, :self.modes3] = self.compl_mul3d(
            x_ft[:, :, :self.modes1, -self.modes2:, :self.modes3], self.weights3)
        out_ft[:, :, -self.modes1:, -self.modes2:, :self.modes3] = self.compl_mul3d(
            x_ft[:, :, -self.modes1:, -self.modes2:, :self.modes3], self.weights4)
        return torch.fft.irfftn(out_ft, s=(x.size(-3), x.size(-2), x.size(-1)))


class FNO3d(nn.Module):
    def __init__(self, modes1=4, modes2=12, modes3=16, n_layers=4, width=64,
                 shape_in=(1, 20, 32, 64, 3), shape_out=(1, 20, 32, 64, 3)):
        super().__init__()
        self.modes1 = modes1
        self.modes2 = modes2
        self.modes3 = modes3
        self.width = width
        self.shape_in = shape_in
        self.shape_out = shape_out
        self.dim_in = shape_in[-1]
        self.dim_out = shape_out[-1] * shape_out[0] // shape_in[0]
        self.padding = 6
        self.fc0 = nn.Linear(self.dim_in + 3, self.width)
        self.n_layers = n_layers
        self.spectral_convs = nn.ModuleList()
        self.convs = nn.ModuleList()
        self.bns = nn.ModuleList()
        for _ in range(n_layers):
            self.spectral_convs.append(SpectralConv3d(self.width, self.width, modes1, modes2, modes3))
            self.convs.append(nn.Conv3d(self.width, self.width, 1))
            self.bns.append(nn.BatchNorm3d(self.width))
        self.fc1 = nn.Linear(self.width, 128)
        self.fc2 = nn.Linear(128, self.dim_out)

    def get_grid(self, shape, device):
        # Official RealPDEBench order: grid channels are (t, y, x) — dims
        # size_x=T, size_y=H, size_z=W in the official get_grid.
        b, t, h, w, c = shape
        gridt = torch.tensor(np.linspace(0, 1, t), dtype=torch.float, device=device)
        gridt = gridt.reshape(1, t, 1, 1, 1).repeat([b, 1, h, w, 1])
        gridy = torch.tensor(np.linspace(0, 1, h), dtype=torch.float, device=device)
        gridy = gridy.reshape(1, 1, h, 1, 1).repeat([b, t, 1, w, 1])
        gridx = torch.tensor(np.linspace(0, 1, w), dtype=torch.float, device=device)
        gridx = gridx.reshape(1, 1, 1, w, 1).repeat([b, t, h, 1, 1])
        return torch.cat((gridt, gridy, gridx), dim=-1)

    def forward(self, x):
        grid = self.get_grid(x.shape, x.device)
        x = torch.cat((x, grid), dim=-1)
        x = self.fc0(x)
        x = x.permute(0, 4, 1, 2, 3)
        x = F.pad(x, [0, self.padding, 0, self.padding, 0, self.padding])
        for i in range(self.n_layers):
            x1 = self.spectral_convs[i](x)
            x2 = self.convs[i](x)
            x = x1 + x2
            x = self.bns[i](x)
            if i < self.n_layers - 1:
                x = F.gelu(x)
        x = x[..., :-self.padding, :-self.padding, :-self.padding]
        x = x.permute(0, 2, 3, 4, 1)
        x = self.fc1(x)
        x = F.gelu(x)
        x = self.fc2(x)
        return x


# ---------------------------------------------------------------------------
# Agentic TTT controller
# ---------------------------------------------------------------------------
class LTTTAController:
    """Bounded agent deciding when and how much to adapt, per step.

    State: base weights snapshot + running error estimate + calibrated
    residual scale. Adaptation = a few gradient steps of the surrogate on the
    revealed previous window, with LR/step count chosen by the controller
    (OOWM clan-supervisor pattern: a supervisor routes between 'predict frozen'
    and 'adapt now' based on observed drift, never using the current step's
    ground truth to build the current prediction).

    SPS: returns calibrated lower/upper bounds (all-or-nothing across the
    run). The residual scale is estimated from the *revealed previous window*
    (legitimate adaptation signal), EMA-smoothed, then used to build a
    z-multiplier band around the prediction.
    """

    def __init__(self, model, device, max_adapt_steps=2, base_lr=1e-4,
                 adapt_every=3, drift_threshold=0.35, ema_alpha=0.3,
                 z_mult=1.2, min_band=0.02, return_bounds=True):
        self.model = model
        self.device = device
        self.max_adapt_steps = max_adapt_steps
        self.base_lr = base_lr
        self.adapt_every = adapt_every
        self.drift_threshold = drift_threshold
        self.ema_alpha = ema_alpha
        self.z_mult = z_mult
        self.min_band = min_band
        self.return_bounds = return_bounds
        self.base_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        self.step_count = 0
        self.ema_err = None
        self.resid_std = None   # EMA per-channel residual std (normalized space)
        self.cached_input = None

    def reset_ttt_state(self):
        """Restore checkpoint weights and clear adaptation state."""
        self.model.load_state_dict(self.base_state)
        self.step_count = 0
        self.ema_err = None
        self.resid_std = None
        self.cached_input = None

    def _relative_l2(self, pred, target, eps=1e-8):
        flat = pred.reshape(pred.shape[0], -1)
        tflat = target.reshape(target.shape[0], -1)
        return (torch.norm(flat - tflat, dim=1) / torch.clamp(torch.norm(tflat, dim=1), min=eps)).mean()

    def adapt(self, input_win, target_win):
        """A few gradient steps on the revealed previous window."""
        inp = input_win.to(self.device)
        tgt = target_win.to(self.device)
        self.model.train()
        params = [p for p in self.model.parameters() if p.requires_grad]
        steps = self.max_adapt_steps
        # Drift-aware step count: adapt more when error is high.
        if self.ema_err is not None:
            steps = min(self.max_adapt_steps, 1 + int(2 * self.ema_err / self.drift_threshold))
        for _ in range(steps):
            self.model.zero_grad()
            pred = self.model(inp)
            loss = F.mse_loss(pred, tgt)
            loss.backward()
            for p in params:
                p.data -= self.base_lr * p.grad
        self.model.eval()
        return loss.item()

    def _calibrate(self, prev_pred, prev_target):
        """Estimate per-channel residual std from the revealed previous window."""
        r = (prev_pred - prev_target)  # (1, T, H, W, C)
        s = r.std(dim=(0, 1, 2, 3))   # per-channel (C,)
        if self.resid_std is None:
            self.resid_std = s.detach()
        else:
            self.resid_std = self.ema_alpha * s.detach() + (1 - self.ema_alpha) * self.resid_std
        return self.resid_std

    def ttt_step(self, input_norm, prev_target_norm=None):
        # 1) Adapt if ground truth of the previous window was revealed.
        adapt_loss = None
        if prev_target_norm is not None and self.cached_input is not None:
            prev_t = prev_target_norm.to(self.device)
            with torch.no_grad():
                prev_pred = self.model(self.cached_input.to(self.device))
                err = self._relative_l2(prev_pred, prev_t).item()
            if self.ema_err is None:
                self.ema_err = err
            else:
                self.ema_err = self.ema_alpha * err + (1 - self.ema_alpha) * self.ema_err
            self._calibrate(prev_pred, prev_t)
            # The controller decides: adapt on cadence when drift is high.
            if (self.step_count % self.adapt_every == 0) and (
                    self.ema_err > self.drift_threshold or self.step_count < 2):
                adapt_loss = self.adapt(self.cached_input, prev_target_norm)

        # 2) Predict the current window.
        self.model.eval()
        with torch.no_grad():
            pred = self.model(input_norm.to(self.device))

        # 3) Build calibrated bounds (all-or-nothing across the run).
        # Per-channel band in normalized space: z * resid_std(channel).
        # The evaluator denormalizes bounds, so the physical width is
        # 2*z*resid_std_physical — sigma_global ≈ u-channel std, so z≈1.2
        # gives a tight-but-covering band (coverage ~ 80-90%).
        info = {"adapt_loss": adapt_loss}
        if self.return_bounds:
            if self.resid_std is not None:
                band = torch.clamp(self.z_mult * self.resid_std, min=self.min_band)
                band = band.view(1, 1, 1, 1, -1).to(pred.device)
            else:
                band = torch.full((1, 1, 1, 1, pred.shape[-1]), self.min_band,
                                  device=pred.device)
            info["lower"] = (pred - band).cpu()
            info["upper"] = (pred + band).cpu()

        # 4) Cache current input for the next step.
        self.cached_input = input_norm.detach().clone()
        self.step_count += 1
        return pred.cpu(), info


# ---------------------------------------------------------------------------
# Checkpoint loading (fp32 native, fp16 packed, raw state_dict)
# ---------------------------------------------------------------------------
def unpack_fp16(path):
    raw = torch.load(path, map_location="cpu", weights_only=False)
    complex_keys = set(raw["complex_keys"])
    sd = {}
    for k, v in raw["state_fp16"].items():
        if k in complex_keys:
            sd[k] = torch.view_as_complex(v.float())
        elif torch.is_tensor(v) and v.dtype == torch.float16:
            sd[k] = v.float()
        else:
            sd[k] = v
    return sd


def load_state_dict_any(model, path):
    raw = torch.load(path, map_location="cpu", weights_only=False)
    if isinstance(raw, dict) and "state_fp16" in raw:
        sd = unpack_fp16(path)
    elif isinstance(raw, dict) and "model_state_dict" in raw:
        sd = raw["model_state_dict"]
    elif isinstance(raw, dict) and "state_dict" in raw:
        sd = raw["state_dict"]
    else:
        sd = raw
    if all(k.startswith("module.") for k in sd):
        sd = {k[len("module."):]: v for k, v in sd.items()}
    # Only load keys that exist (robust to minor arch drift)
    model_sd = model.state_dict()
    filtered = {k: v for k, v in sd.items() if k in model_sd and model_sd[k].shape == v.shape}
    missing = [k for k in model_sd if k not in filtered]
    model.load_state_dict(filtered, strict=False)
    return missing


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def get_ttt_model(submission_dir, device="cpu"):
    model = FNO3d()
    ckpt_path = os.path.join(submission_dir, "model.pth")
    missing = []
    if os.path.exists(ckpt_path):
        missing = load_state_dict_any(model, ckpt_path)
    model.to(device)
    model.eval()
    return LTTTAController(model, device)
