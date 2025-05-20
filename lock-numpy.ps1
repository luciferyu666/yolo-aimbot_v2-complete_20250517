# ★ 在專案根執行：  .\lock-numpy.ps1

$Venv   = ".venv"
$Target = "1.26.4"

function Info($m){Write-Host "[INFO] $m" -f Cyan}

# 1) venv
if (!(Test-Path $Venv)){ Info "Creating venv ..."; python -m venv $Venv }
& "$Venv\Scripts\Activate.ps1"

# 2) 安裝目標 NumPy
Info "Force-install NumPy $Target ..."
pip uninstall -y numpy  | Out-Null
pip install -q  "numpy==$Target"

# 3) 測試
python -c "import numpy, sys, importlib.util as iu; 
print('✅ NumPy', numpy.__version__, 'import OK');
print('➜  onnxruntime import …', end=' ');
try:
    import onnxruntime as ort; print('OK', ort.__version__)
except Exception as e:
    print('FAIL', e); sys.exit(1)"
