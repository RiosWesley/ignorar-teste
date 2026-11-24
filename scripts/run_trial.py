"""Launcher direto: abre o trial de 12 meses e para na tela para você finalizar.
Uso: python C:\temp\run_trial.py [porta]
"""
import sys, os, subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

serial = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1:16416'
script_dir = r'C:\Users\Wesley\Downloads\ultra_pro_extract\Google_AI_Ultra_Pro_一键下单'
script_path = r'C:\temp\ultra0_pt.py'

env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONUTF8'] = '1'

# Direto no trial de 12 meses — SEM --list
cmd = [
    sys.executable, '-u', script_path,
    '--account', 'current@device',
    '--no-add', '--force',
    '--plan', 'pro12',
    '--serial', serial,
]

print(f'Rodando trial 12 meses em {serial}...')
proc = subprocess.Popen(cmd, cwd=script_dir, env=env)
proc.wait(timeout=300)
print('Finalizado. Codigo:', proc.returncode)
