
# YOLO Aimbot v2 – Fast‑UI Patch 1

此版本在 FUI 交付基礎上補齊缺口：

* **ByteTrack**：採用簡化版 IOU‑Based ByteTrack，支援 ID 保持
* **Coverage ≥ 80 %**：新增單元與整合測試
* **HUD**：前端顯示 FPS、延遲(ms)、控制模式切換 (NET/Serial)
* **OBS Lua**：可解析 UDP bounding box 並畫框 / HUD
* **其他**：腳本、CI 門檻更新

執行 `docker compose up` 即可。
