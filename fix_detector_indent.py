# fix_detector_indent.py
import re, pathlib, shutil, sys

fp = pathlib.Path("ai_engine/detector.py")
if not fp.exists():
    sys.exit("❌ 找不到 ai_engine/detector.py")

text = fp.read_text(encoding="utf-8")

pattern = re.compile(
    r"def predict\([^\n]+?\n)([ \t]+)for det in out:[\s\S]+?return res",
    re.MULTILINE,
)

m = pattern.search(text)
if not m:
    sys.exit("❌ 無法定位 predict() 迴圈，請人工檢查檔案結構。")

base_indent = " " * 8  # 兩層縮排（def → for）
fixed_block = f"""{base_indent}for det in out:
{base_indent}    conf = float(det[4])
{base_indent}    if conf < 0.25:
{base_indent}        continue
{base_indent}    cx, cy, w, h = det[:4]
{base_indent}    x1 = int((cx - w / 2) * iw)
{base_indent}    y1 = int((cy - h / 2) * ih)
{base_indent}    x2 = int((cx + w / 2) * iw)
{base_indent}    y2 = int((cy + h / 2) * ih)
{base_indent}    res.append((x1, y1, x2, y2, conf))
{base_indent}return res"""

new_text = pattern.sub(lambda _m: _m.group(1) + fixed_block, text)

# 備份 & 覆寫
bak = fp.with_suffix(".bak_indent")
shutil.copy(fp, bak)
fp.write_text(new_text, encoding="utf-8")

print("✅ detector.py 縮排已修補，備份於", bak)
