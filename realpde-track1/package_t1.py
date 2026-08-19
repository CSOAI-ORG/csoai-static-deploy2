import zipfile
import os

t1_code = open("/root/realpde/submission_model.py").read()
wrapper = """

from submission_model import SubmissionModel as _SM
_model = None
def predict(input_array, metadata=None):
    global _model
    if _model is None:
        import torch
        _model = _SM(device="cuda" if torch.cuda.is_available() else "cpu")
    return _model.predict(input_array, metadata)
"""
with zipfile.ZipFile("/root/realpde/submission_t1_v1.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("submission.py", t1_code + wrapper)
    zf.write("/root/realpde/trained_v1/model.pth", "model.pth")
    zf.write("/root/realpde/trained_v1/stats_real.npz", "stats.npz")
print("t1 zip size MB:", os.path.getsize("/root/realpde/submission_t1_v1.zip") / 1e6)
