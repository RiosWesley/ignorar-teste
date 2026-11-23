# Verificacao de ambiente
chcp 65001 > $null
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

Write-Host "=== Verificando ambiente ===" -ForegroundColor Green
python -c "import frida; print('Frida:', frida.__version__)"
adb devices
Write-Host ""
Write-Host "Conecte o MuMu: adb connect 127.0.0.1:7555" -ForegroundColor Yellow
Write-Host "Depois: adb -s 127.0.0.1:7555 root" -ForegroundColor Yellow
