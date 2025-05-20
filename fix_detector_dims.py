# fix_detector_dims.py
import re, pathlib, textwrap, sys

fp = pathlib.Path("ai_engine/detector.py")
src = fp.read_text(encoding="utf-8")

new_body = textwrap.dedent("""\
    def predict(self, img, conf_thres: float = 0.25):
        \"\"\"Run ONNX-YOLOv8 inference and return [(x1,y1,x2,y2,conf), …].\"\"\"
        ih, iw = img.shape[:2]                       # 原始影像尺寸
        blob = cv2.dnn.blobFromImage(img, 1/255, (640, 640), swapRB=True)
        out = self.sess.run(None, {self.input: blob})[0]   # (1,84,8400) or (8400,84)
        out = out.squeeze()                         # -> (84,8400) or (8400,84)

        # 若第一維只有 84 個元素就代表還沒轉置，先轉置成 (N,84)
        if out.shape[0] == 84:
            out = out.T

        results = []
        for det in out:
            obj_conf = float(det[4])                # 物件置信度 (scalar)
            cls_conf = float(det[5:].max())         # 最高類別分數
            conf = obj_conf * cls_conf             # YOLOv8 常用的綜合置信度
            if conf < conf_thres:
                continue

            cx, cy, w, h = det[:4]                  # 模型輸出座標以 640 為基準
            scale_x, scale_y = iw / 640, ih / 640
            x1 = int((cx - w / 2) * scale_x)
            y1 = int((cy - h / 2) * scale_y)
            x2 = int((cx + w / 2) * scale_x)
            y2 = int((cy + h / 2) * scale_y)
            results.append((x1, y1, x2, y2, conf))

        return results
""")

pattern = r"def\s+predict\([^)]*\)[\s\S]+?return\s+[^\n]+\n"
if re.search(pattern, src):
    bak = fp.with_suffix(".bak_dims")
    fp.rename(bak)
    fp.write_text(re.sub(pattern, new_body, src), encoding="utf-8")
    print(f"[OK] predict() 已重寫，備份存於 {bak.name}")
else:
    print("⚠️  沒找到原本的 predict()，請手動確認檔案結構。")
    sys.exit(1)
