import ssl
import pathlib
import urllib.request

import cv2
import numpy as np
import onnxruntime as ort

# Fallback tiny YOLOv8‑n model (≈6 MB) – downloaded automatically on first run
MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.onnx"


def _ensure_model(path: pathlib.Path) -> None:
    """Download the ONNX model if it does not yet exist."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        # Skip certificate verification – the GitHub asset uses HTTPS
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(MODEL_URL, path.as_posix())


class Detector:
    """Minimal ONNX‑YOLOv8 wrapper for CPUInference."""

    def __init__(self, model_path: str = "ai_engine/models/yolov8n.onnx") -> None:
        model_p = pathlib.Path(model_path)
        _ensure_model(model_p)

        # Build a single‑backend ONNX Runtime session (CPU only for portability)
        self.session = ort.InferenceSession(
            model_p.as_posix(), providers=["CPUExecutionProvider"]
        )
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, img: np.ndarray, conf_thres: float = 0.25):
        """Run YOLOv8 inference and return list of ``(x1, y1, x2, y2, conf)`` tuples.

        Parameters
        ----------
        img : np.ndarray
            BGR image read by OpenCV (H×W×3).
        conf_thres : float, optional
            Confidence threshold for filtering predictions, by default ``0.25``.
        """
        ih, iw = img.shape[:2]

        # --- Pre‑process -----------------------------------------------------
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (640, 640), swapRB=True)
        output = self.session.run(None, {self.input_name: blob})[0].squeeze()
        # ``output`` shape: (N, 84)  or  (84, N)  depending on export settings
        if output.shape[0] == 84:  # transpose once if channels first
            output = output.T

        scale_x, scale_y = iw / 640, ih / 640
        results = []

        for det in output:
            obj_conf = float(det[4])          # objectness score
            cls_conf = float(det[5:].max())   # best‑class probability
            conf = obj_conf * cls_conf        # final YOLO score
            if conf < conf_thres:
                continue

            cx, cy, w, h = det[:4]
            x1 = int((cx - w / 2) * scale_x)
            y1 = int((cy - h / 2) * scale_y)
            x2 = int((cx + w / 2) * scale_x)
            y2 = int((cy + h / 2) * scale_y)
            results.append((x1, y1, x2, y2, conf))

        return results
