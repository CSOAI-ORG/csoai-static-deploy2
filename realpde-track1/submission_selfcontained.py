"""Track 1 (Sim2Real) submission - NeurIPS 2026 RealPDE Competition.
Self-contained: FNO3d surrogate + internal normalization.
"""
import os
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

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
