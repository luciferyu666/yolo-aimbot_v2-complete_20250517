#!/usr/bin/env python
"""
fix_detector_numpy_cast.py
--------------------------
將 ai_engine/detector.py 內的

    conf = det[4]
    if conf < 0.25:

改成

    conf = float(np.asarray(det[4]).flat[0])
    if conf < 0.25:
"""
import pathlib, re, sys, textwrap

fp = pathlib.Path("ai_engine/detector.py")
if not fp.exists():
    sys.exit("[FAIL] 找不到 ai_engine/detector.py")

code = fp.read_text(encoding="utf-8")

pat = re.compile(
    r"conf\s*=\s*det\[\s*4\s*]\s*\n\s*if\s+conf\s*<\s*0\.25", re.MULTILINE
)

if not pat.search(code):
    print("[INFO] 未找到原始片段，可能結構不同或已手動修正，請人工檢查。")
    sys.exit(0)

fixed = pat.sub(
    textwrap.dedent(
        """\
        conf = float(__import__("numpy").asarray(det[4]).flat[0])
        if conf < 0.25"""
    ),
    code,
)

bak = fp.with_suffix(".py.bak")
fp.rename(bak)
fp.write_text(fixed, encoding="utf-8")
print(f"[OK] detector.py 已修補；原檔備份為 {bak.name}")
