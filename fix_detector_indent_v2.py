"""
fix_detector_indent_v2.py
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
* 重新格式化 ai_engine/detector.py 內 predict() 的 for-loop，
  修正縮排 & numpy float(conf) 轉型。
* 只改動 predict() 函式裡的區塊，其餘保持原狀。
"""
from pathlib import Path
import shutil, sys

SRC = Path("ai_engine/detector.py")
if not SRC.exists():
    sys.exit("❌  找不到 ai_engine/detector.py")

lines = SRC.read_text(encoding="utf-8").splitlines()

fixed, inside_predict, replaced = [], False, False
predict_indent = ""
for idx, ln in enumerate(lines):
    stripped = ln.lstrip()
    if stripped.startswith("def predict"):
        inside_predict = True
        predict_indent = ln[: len(ln) - len(stripped)]
        fixed.append(ln)
        continue

    if inside_predict:
        # 判斷迴圈開頭
        if stripped.startswith("for det in out:") and not replaced:
            loop_indent = predict_indent + " " * 4
            fixed.extend(
                [
                    f"{loop_indent}for det in out:",
                    f"{loop_indent}    conf = float(det[4])",
                    f"{loop_indent}    if conf < 0.25:",
                    f"{loop_indent}        continue",
                    f"{loop_indent}    cx, cy, w, h = det[:4]",
                    f"{loop_indent}    x1 = int((cx - w / 2) * iw)",
                    f"{loop_indent}    y1 = int((cy - h / 2) * ih)",
                    f"{loop_indent}    x2 = int((cx + w / 2) * iw)",
                    f"{loop_indent}    y2 = int((cy + h / 2) * ih)",
                    f"{loop_indent}    res.append((x1, y1, x2, y2, conf))",
                ]
            )
            replaced = True
            continue  # 跳過原本行
        # detect end of function
        if stripped.startswith("return res"):
            inside_predict = False
            fixed.append(predict_indent + "    return res")
            continue
        # 若已替換則略過舊 for-loop 內容
        if replaced:
            # 當下一個非縮排 (同層或更左) 就退出 replaced 狀態
            if not ln.startswith(loop_indent + " "):
                replaced = False
            else:
                continue  # 忽略舊行
    fixed.append(ln)

if not replaced:
    sys.exit("⚠️  沒偵測/替換到 for det in out 迴圈，檔案結構可能與預期不同。")

bak = SRC.with_suffix(".bak_indent_v2")
shutil.copy(SRC, bak)
SRC.write_text("\n".join(fixed) + "\n", encoding="utf-8")
print(f"✅ detector.py 縮排與 conf 轉型已修補；備份 → {bak}")
