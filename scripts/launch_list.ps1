# Listar todos os offers disponiveis (ZERO RISCO - nao clica em nada)
chcp 65001 > $null
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

python ultra0.py --list --no-add --force --serial 127.0.0.1:7555
