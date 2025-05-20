#!/usr/bin/env python
"""
fix_detector_numpy_cast_v2.py
支援以下各種寫法：
    conf = det[4]
    conf=det[4];
    if conf<0.25: continue
    if conf < 0.25:
"""
import pathlib, re, sys

fp = pathlib.Path("ai_engine/detector.py")
if not fp.exists():
    sys.exit("[FAIL] 找不到 ai_engine/detector.py")

txt = fp.read_text(encoding="utf-8")

pat = re.compile(
    r"(conf\s*=\s*det\[\s*4\s*]\s*;?\s*\n?)"
    r"(\s*if\s+conf\s*<\s*0\.25\s*:?\s*(?:continue)?)",
    flags=re.MULTILINE,
)

def repl(m):
    assign, cond = m.groups()
    assign_fixed = re.sub(
        r"conf\s*=\s*det\[\s*4\s*]",
        'conf = float(__import__("numpy").asarray(det[4]).flat[0])',
        assign,
    )
    # 讓 if/continue 變成獨立一行（可保留語意）
    cond_fixed = "\n" + re.sub(r"\s*continue$", "\n    continue", cond)
    return assign_fixed + cond_fixed

new_txt, n = pat.subn(repl, txt, count=1)
if n == 0:
    print("[INFO] 仍未匹配；請手動修改或貼出原始區段讓我檢查。")
    sys.exit()

bak = fp.with_suffix(".py.bak")
fp.rename(bak)
fp.write_text(new_txt, encoding="utf-8")
print(f"[OK] 已修補 detector.py (備份 {bak.name})")
