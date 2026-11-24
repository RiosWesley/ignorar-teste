import subprocess, sqlite3, json, tempfile, os, time, datetime, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

serial = '127.0.0.1:16416'
remote = '/data/local/tmp/lib_resumo.db'
subprocess.run(['adb','-s',serial,'shell',f'cp /data/data/com.android.vending/databases/library.db {remote} 2>/dev/null; chmod 666 {remote}'], capture_output=True, timeout=30)
tmp = os.path.join(tempfile.gettempdir(),'lib_resumo.db')
if os.path.exists(tmp): os.remove(tmp)
subprocess.run(['adb','-s',serial,'pull',remote,tmp], capture_output=True, timeout=60)

now = int(time.time()*1000)
con = sqlite3.connect(tmp)
rows = con.execute('select account, subs_valid_until_time, inapp_purchase_data from ownership').fetchall()

# Agrupar por conta: pegar a assinatura valida mais longa
contas = {}
for acc, valid, data in rows:
    valid = int(valid or 0)
    if acc not in contas:
        contas[acc] = []
    contas[acc].append((valid, data))

print('=== ASSINATIVAS NO library.db (por conta) ===')
for acc in sorted(contas):
    vals = contas[acc]
    ativos = [(v,d) for v,d in vals if v > now]
    if ativos:
        v,d = max(ativos, key=lambda x: x[0])
        dt = datetime.datetime.fromtimestamp(v/1000)
        dias = (dt - datetime.datetime.now()).days
        tok = str(json.loads(d).get('purchaseToken',''))[:18] if d else ''
        print(f'  ATIVO  {acc:32} ate {dt.strftime("%Y-%m-%d")} ({dias}d) tok={tok}...')
    else:
        print(f'  vencido/sem trial  {acc}')
con.close()
