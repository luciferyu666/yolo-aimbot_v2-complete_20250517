# fix_detector_indent_ultimate.py
import pathlib, re, sys

fp = pathlib.Path("ai_engine/detector.py")
txt = fp.read_text(encoding="utf-8").splitlines(keepends=False)

new = []
fixed = False
i = 0
while i < len(txt):
    line = txt[i]
    new.append(line)
    if re.match(r"\s*def\s+predict\(", line):
        i += 1
        # 收集直到第一行真正程式碼(非空白)結束
        while i < len(txt) and txt[i].strip() == "":
            new.append(txt[i]); i += 1
        # 若 docstring 行未縮排 ── > 補 4 空白
        if i < len(txt) and not txt[i].startswith((" ", "\t")):
            while i < len(txt) and txt[i].strip() != "":
                new.append("    " + txt[i])
                i += 1
            fixed = True
            continue        # 繼續跑 while 迴圈
    i += 1

if fixed:
    bak = fp.with_suffix(".bak_indentfix")
    fp.rename(bak)
    fp.write_text("\n".join(new) + "\n", encoding="utf-8")
    print(f"✅ 已修正縮排，備份存於 {bak.name}")
else:
    print("⚠️  未偵測到需要修正的區塊。（可能已經手動修好或結構不同）")
    sys.exit(1)
