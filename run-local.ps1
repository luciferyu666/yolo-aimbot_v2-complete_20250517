<#
  run-local.ps1 ─ YOLO Aimbot v2-Complete
  前提：已在專案根目錄，且安裝 Git / Python / Node.js
#>

#------------------ 參數 ------------------#
$Root      = "C:\Users\vince\Downloads\yolo-aimbot_v2-complete_20250517"
$PyVenv    = ".venv"
$ModelURL  = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.onnx"
$ModelPath = "$Root\ai_engine\models\yolov8n.onnx"
$BackHost  = "127.0.0.1"; $BackPort = 8000
$UiPort    = 3000
#-----------------------------------------#

function Info { param($m) ; Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Fail { param($m) ; Write-Host "[FAIL] $m" -ForegroundColor Red ; exit 1 }

cd $Root  # 進入專案根

# 1. Python venv & 套件
if (!(Test-Path $PyVenv)) {
  Info "Creating venv ..."
  python -m venv $PyVenv
}
& "$PyVenv\Scripts\Activate.ps1"
Info "Installing Python dependencies ..."
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) { Fail "pip install failed" }

# 2. 下載模型 (若不存在)
if (!(Test-Path $ModelPath)) {
  Info "Downloading YOLO model ..."
  Invoke-WebRequest $ModelURL -OutFile $ModelPath -UseBasicParsing
  if ($LASTEXITCODE -ne 0) { Fail "Model download failed" }
}

# 3. 測試覆蓋率
Info "Running pytest ..."
pytest --cov=. --cov-fail-under=80
if ($LASTEXITCODE -ne 0) { Fail "Tests failed or coverage < 80%" }

# 4. 背景啟動 FastAPI
Info "Starting backend (http://$BackHost`:$BackPort) ..."
$cmdBackend = "`"$env:Path='$env:Path'; cd $Root; & `"$PyVenv\Scripts\Activate.ps1`"; uvicorn api.app:app --host $BackHost --port $BackPort`""
Start-Process powershell "-NoLogo -NoExit -Command $cmdBackend"

# 5. 背景啟動 Tauri + React
Info "Starting UI (http://localhost:$UiPort) ..."
$cmdUI = "`"$env:Path='$env:Path'; cd $Root\ui; npm install --omit=dev; npm run tauri dev`""
Start-Process powershell "-NoLogo -NoExit -Command $cmdUI"

# 6. 等待後端啟動 & 發送偵測
Start-Sleep 10
Info "Calling /detect with sample image ..."
$resp = Invoke-WebRequest -Method POST `
        -Uri "http://$BackHost`:$BackPort/detect" `
        -Form @{ file = Get-Item "$Root\examples\sample_frame.jpg" } |
        Select-Object -ExpandProperty Content

$resp = Invoke-WebRequest -Method POST `
        -Uri "http://$BackHost`:$BackPort/detect" `
        -Form @{ file = Get-Item "$Root\examples\sample_frame.jpg" } |
        Select-Object -ExpandProperty Content
Write-Host "`n--- API Response ---`n$resp"

$uiUrl = "http://localhost:$UiPort"
Info ("All done! Open $uiUrl  and watch FPS/Latency in the browser.")
