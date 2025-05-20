import pathlib, re, textwrap

p = pathlib.Path("ai_engine/detector.py")
src = p.read_text(encoding="utf-8").splitlines()

out, inside = [], False
for line in src:
    if re.match(r"\s*def\s+predict\(", line):
        inside = True
        out.append(line)
        continue
    if inside:
        if line.strip() == "":
            out.append("    ")          # 空行仍保持縮排
            continue
        if not line.startswith((" ", "\t")):
            line = "    " + line        # 若缺縮排就補 4 空白
        elif not line.startswith("    "):
            # 把不足 4 空白的行補滿
            line = "    " + line.lstrip()
        if re.match(r"\s*def\s+\w", line):
            inside = False              # 意外遇到下一個 def，跳出
    out.append(line)

bak = p.with_suffix(".bak_forceindent")
p.rename(bak)
p.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"✅ 強制縮排完成；備份：{bak.name}")
