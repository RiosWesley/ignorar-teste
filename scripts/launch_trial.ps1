# Ativar trial. Uso: .\launch_trial.ps1 pro12
# Opcoes: pro12 (12 meses), pro6 (6 meses), pro3 (3 meses)
param(
    [Parameter(Position=0)]
    [string]$Plan = "pro12",
    [string]$Serial = "127.0.0.1:7555"
)

chcp 65001 > $null
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

Write-Host "=== Ativando trial: $Plan ===" -ForegroundColor Green
Write-Host "Use ultra0_pt.py para nao clicar automaticamente (voce finaliza)" -ForegroundColor Yellow

python ultra0_pt.py --account "current@device" --no-add --force --plan $Plan --serial $Serial
