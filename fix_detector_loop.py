#!/usr/bin/env python
"""
fix_detector_loop.py
--------------------
* 把 ai_engine/detector.py 的 predict() 迴圈修正為正確的列迭代 *
"""
import pathlib, re, sys, textwrap

fp = pathlib.Path("ai_engine/detector.py")
if not fp.exists():
    sys.exit("[FAIL] 找不到 ai_engine/detector.py")

src = fp.read_text(encoding="utf-8")

# --- 1. 確保已 import numpy as np ---
if "import numpy as np" not in src:
    src = src.replace("import onnxruntime as ort, cv2,", "import onnxruntime as ort, cv2, numpy as np,")

# --- 2. 置換 predict 內部迴圈 ---
pat = re.compile(
    r"(out\s*=\s*self\.sess\.run[^\n]+\n)([\s\S]*?for\s+det\s+in\s+out:\s*\n\s*conf[^\n]+\n)",
    re.MULTILINE,
)

def patch(m):
    header = m.group(1)
    # 新的處理區塊
    body = textwrap.dedent(
        """\
        # YOLOv8 ONNX 輸出 (1, 84, 8400) -> (8400, 84)
        out = np.squeeze(out).T
        res = []
        for det in out:
            conf = float(det[4])
            if conf < 0.25:
                continue
            cx, cy, w, h = det[:4]
            x1 = int((cx - w / 2) * iw)
            y1 = int((cy - h / 2) * ih)
            x2 = int((cx + w / 2) * iw)
            y2 = int((cy + h / 2) * ih)
            res.append((x1, y1, x2, y2, conf))
        return res
        """
    )
    return header + body

new_src, n = pat.subn(patch, src, count=1)
if n == 0:
    print("[INFO] 未匹配到舊迴圈，請手動檢查。")
    sys.exit()

bak = fp.with_suffix(".py.bak")
fp.rename(bak)
fp.write_text(new_src, encoding="utf-8")
print(f"[OK] detector.py 已修補；原檔備份為 {bak.name}")
