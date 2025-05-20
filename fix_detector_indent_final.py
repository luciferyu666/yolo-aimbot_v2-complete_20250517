# fix_detector_indent_final.py
import pathlib, textwrap, sys, re

fp = pathlib.Path("ai_engine/detector.py")
code = fp.read_text(encoding="utf-8").splitlines(keepends=True)

out = []
fixed = False
i = 0
while i < len(code):
    line = code[i]
    out.append(line)
    if not fixed and re.match(r"\s*def\s+predict\(", line):
        i += 1
        # 如果下一行沒有縮排 (開頭不是空白或\t)，就補 4 空白
        while i < len(code) and code[i].strip() == '':
            out.append(code[i]); i += 1          # 跳過空白行
        if i < len(code) and not code[i].startswith((' ', '\t')):
            # 把函式體直到第一次遇到空白行前全部縮排
            while i < len(code) and code[i].strip():
                out.append('    ' + code[i])
                i += 1
            fixed = True
            continue
    i += 1

if not fixed:
    print("⚠️  檔案看起來已經修正（或結構和預期不同），未變更。")
    sys.exit(0)

bak = fp.with_suffix(".bak_indent")
fp.rename(bak)
fp.write_text(''.join(out), encoding="utf-8")
print(f"✅ Indentation 修正完成，備份存於 {bak.name}")
