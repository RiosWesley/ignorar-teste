import subprocess, sqlite3, json, tempfile, os, time, datetime, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

serial = '127.0.0.1:16416'
remote = '/data/local/tmp/lib_v.db'
subprocess.run(['adb','-s',serial,'shell',f'cp /data/data/com.android.vending/databases/library.db {remote} 2>/dev/null; chmod 666 {remote}'], capture_output=True, timeout=30)
tmp = os.path.join(tempfile.gettempdir(),'lib_v.db')
if os.path.exists(tmp): os.remove(tmp)
subprocess.run(['adb','-s',serial,'pull',remote,tmp], capture_output=True, timeout=60)

con = sqlite3.connect(tmp)
rows = con.execute('select account, subs_valid_until_time, inapp_purchase_data from ownership').fetchall()
now = int(time.time()*1000)
for acc, valid, data in rows:
    if int(valid or 0) > now:
        dt = datetime.datetime.fromtimestamp(int(valid)/1000)
        tok = str(json.loads(data).get('purchaseToken',''))[:25] if data else ''
        print(f'ATIVO: {acc}')
        print(f'  Valido ate: {dt.strftime("%Y-%m-%d %H:%M")}')
        print(f'  Dias restantes: {(dt-datetime.datetime.now()).days}')
        print(f'  Token: {tok}...')
con.close()
