"""Trial de 3 meses (pro3) - para testar validacao da conta."""
import sys, os, subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

serial = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1:16416'
script_dir = r'C:\Users\Wesley\Downloads\ultra_pro_extract\Google_AI_Ultra_Pro_一键下单'
script_path = r'C:\temp\ultra0_stack.py'

env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONUTF8'] = '1'

cmd = [
    sys.executable, '-u', script_path,
    '--account', 'current@device',
    '--no-add', '--force',
    '--plan', 'pro3',
    '--serial', serial,
]

print(f'=== TRIAL 3 MESES (pro3) em {serial} ===')
proc = subprocess.Popen(cmd, cwd=script_dir, env=env)
proc.wait(timeout=300)
print('Codigo:', proc.returncode)
