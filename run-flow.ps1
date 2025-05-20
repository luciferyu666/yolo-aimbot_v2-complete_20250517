<#
  run-flow.ps1
  YOLO Aimbot v2 ▸ 功能驗證 & 本地部署（覆蓋率不設門檻）
  - 請放在專案根目錄執行，或自行調整 $Root 變數
#>

#--------------- 基本參數 ---------------#
$Root      = "C:\Users\vince\Downloads\yolo-aimbot_v2-complete_20250517"  # 專案根
$PyVenv    = ".venv"
$ModelPath = "$Root\ai_engine\models\yolov8n.onnx"    # 必須先準備好
$BackHost  = "127.0.0.1"; $BackPort = 8000
$UiPort    = 3000
#----------------------------------------#

function Info { param($m) ; Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Fail { param($m) ; Write-Host "[FAIL] $m" -ForegroundColor Red ; exit 1 }

# -- 0. 進入專案根 ----------------------------------------------------------------
cd $Root

# -- 1. 建立 / 啟用 venv -----------------------------------------------------------
if (!(Test-Path $PyVenv)) {
  Info "Creating Python venv ..."
  python -m venv $PyVenv
}
& "$PyVenv\Scripts\Activate.ps1"

# -- 2. 安裝依賴 ------------------------------------------------------------------
Info "Installing requirements ..."
pip install -q -r requirements.txt
# 確保專案可 import
pip install -q -e .        # 安裝成 editable package

# -- 3. 確認模型 -------------------------------------------------------------------
if (!(Test-Path $ModelPath)) { Fail "Model file not found: $ModelPath" }

# -- 4. 執行測試（無覆蓋率門檻） ---------------------------------------------------
$env:PYTHONPATH = "$Root"
Info "Running pytest ..."
pytest --cov=.          # 僅報 coverage，不做 fail-under
if ($LASTEXITCODE -ne 0) { Fail "Some tests failed" }

# -- 5. 背景啟動 FastAPI -----------------------------------------------------------
Info "Starting backend on $BackPort ..."
$cmdBackend = "`"$env:Path='$env:Path'; cd $Root; & `"$PyVenv\Scripts\Activate.ps1`"; uvicorn api.app:app --host $BackHost --port $BackPort`""
Start-Process powershell "-NoLogo -NoExit -Command $cmdBackend"

# -- 6. 背景啟動 Tauri + React -----------------------------------------------------
Info "Starting UI on $UiPort ..."
$cmdUI = "`"$env:Path='$env:Path'; cd $Root\ui; npm install --omit=dev; npm run tauri dev`""
Start-Process powershell "-NoLogo -NoExit -Command $cmdUI"


# -- 7. 等待後端就緒 & 發送範例偵測 ---------------------------------------------
Start-Sleep 10
Info "Calling /detect API ..."

if ($PSVersionTable.PSVersion.Major -ge 7) {
    # PowerShell 7+ 支援 -Form
    $resp = Invoke-WebRequest -Method POST `
            -Uri "http://$BackHost`:$BackPort/detect" `
            -Form @{ file = Get-Item "$Root\examples\sample_frame.jpg" } |
            Select-Object -ExpandProperty Content
}
else {
    # Windows PowerShell 5.1 Fallback：使用內建 curl.exe
    $resp = curl.exe -s -F "file=@$Root\examples\sample_frame.jpg" `
            "http://$BackHost`:$BackPort/detect"
}

Write-Host "`n--- API Response ---`n$resp"

$uiUrl = "http://localhost:$UiPort"

Info ("All done! Open $uiUrl   to watch FPS / Latency")
