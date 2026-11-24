import sys, os, subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

script_dir = r'C:\Users\Wesley\Downloads\ultra_pro_extract\Google_AI_Ultra_Pro_一键下单'

env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONUTF8'] = '1'

cmd = [sys.executable, '-u', r'C:\temp\detailed_offers.py', '--list', '--no-add', '--force', '--serial', '127.0.0.1:16384']

log = r'C:\temp\offers_new.log'
with open(log, 'w', encoding='utf-8') as f:
    p = subprocess.Popen(cmd, cwd=script_dir, stdout=f, stderr=subprocess.STDOUT, env=env)
    p.wait(timeout=180)

with open(log, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()
for l in c.splitlines():
    if 'offer [' in l or '结果' in l:
        print(l[:180])
