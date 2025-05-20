#!/usr/bin/env python
"""
fix_detector_conf.py  (v2)
在 ai_engine/detector.py 的 for det in out 迴圈內
將 'conf = det[4]' 改為 'conf = float(det[4])'
"""

import pathlib, re, sys

fp = pathlib.Path("ai_engine/detector.py")
if not fp.exists():
    sys.exit("[FAIL] 找不到 ai_engine/detector.py")

src = fp.read_text(encoding="utf-8")

# pattern: conf=det[4] 或 conf = det[4]
pat  = re.compile(r"conf\s*=\s*det\[\s*4\s*]")
if not pat.search(src):
    print("[INFO] 未找到 'conf = det[4]'，可能已修補，未變更。")
    sys.exit(0)

dst = pat.sub("conf = float(det[4])", src)

bak = fp.with_suffix(".py.bak")
fp.rename(bak)
fp.write_text(dst, encoding="utf-8")
print(f"[OK] 已修補 detector.py，原檔備份為 {bak.name}")
