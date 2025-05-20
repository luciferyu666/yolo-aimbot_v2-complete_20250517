#!/usr/bin/env python
import pathlib, re, sys, textwrap, itertools

fp = pathlib.Path("ai_engine/detector.py")
if not fp.exists():
    sys.exit("[FAIL] detector.py 不存在")

src = fp.read_text(encoding="utf-8")
if "import numpy as np" not in src:
    src = src.replace("import onnxruntime as ort, cv2,", "import onnxruntime as ort, cv2, numpy as np,")

pat = re.compile(
    r"(out\s*=\s*self\.sess\.run[^\n]+\n)([\s\S]*?for\s+det\s+in\s+out:\s*\n\s*conf[^\n]+\n)",
    re.MULTILINE,
)

def patch(m):
    header = m.group(1)
    body = textwrap.dedent(
        """\
        out = np.squeeze(out).T  # (8400, 84)
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
    print("[INFO] 沒找到舊迴圈，請手動檢查。")
    sys.exit()

# 產生不重複的 .bakX 檔名
for idx in itertools.count(1):
    bak = fp.with_suffix(f".py.bak{idx}")
    if not bak.exists():
        break

fp.replace(bak)
fp.write_text(new_src, encoding="utf-8")
print(f"[OK] 已修補 detector.py；備份存於 {bak.name}")
