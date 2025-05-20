"""
fix_detector_rewrite.py
完全重寫 ai_engine/detector.py 中的 predict() 以修復縮排和 NumPy 轉型問題
"""
from pathlib import Path
import re, shutil, sys

SRC = Path("ai_engine/detector.py")
if not SRC.exists():
    sys.exit("❌ 找不到 ai_engine/detector.py")

code = SRC.read_text(encoding="utf-8").splitlines()

out = []
i = 0
rewritten = False
while i < len(code):
    line = code[i]
    if re.match(r"\s*def\s+predict\s*\(", line):
        indent = re.match(r"(\s*)", line).group(1)
        # ── 塞入新的 predict 實作 ────────────────────────────
        out.append(f"{indent}def predict(self, img):")
        out.append(f"{indent}    ih, iw = img.shape[:2]")
        out.append(f"{indent}    blob = cv2.dnn.blobFromImage(img, 1/255, (640, 640), swapRB=True)")
        out.append(f"{indent}    out = self.sess.run(None, {{self.input: blob}})[0]")
        out.append(f"{indent}    res = []")
        out.append(f"{indent}    for det in out:")
        out.append(f"{indent}        conf = float(det[4])")
        out.append(f"{indent}        if conf < 0.25:")
        out.append(f"{indent}            continue")
        out.append(f"{indent}        cx, cy, w, h = det[:4]")
        out.append(f"{indent}        x1 = int((cx - w/2) * iw)")
        out.append(f"{indent}        y1 = int((cy - h/2) * ih)")
        out.append(f"{indent}        x2 = int((cx + w/2) * iw)")
        out.append(f"{indent}        y2 = int((cy + h/2) * ih)")
        out.append(f"{indent}        res.append((x1, y1, x2, y2, conf))")
        out.append(f"{indent}    return res")
        # ────────────────────────────────────────────────────
        # 跳過舊 predict() 內容直到下一個 def 或 EOF
        i += 1
        while i < len(code) and not re.match(r"\s*def\s+\w+", code[i]):
            i += 1
        rewritten = True
        continue
    out.append(line)
    i += 1

if not rewritten:
    sys.exit("⚠️  未找到 predict()，檔案結構異常，請人工檢查。")

bak = SRC.with_suffix(".bak_rewrite")
shutil.copy(SRC, bak)
SRC.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"✅ predict() 已重寫完成，備份存於 {bak}")
