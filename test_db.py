import os, pymysql
from pathlib import Path

# Cargar .env y LIMPIAR comillas
env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        k, _, v = line.partition('=')
        v = v.strip().strip("'").strip('"')  # <-- sin escapes
        os.environ[k.strip()] = v

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
pwd  = os.getenv('DB_PASSWORD')
dbname = os.getenv('DB_NAME') or None
port = int(os.getenv('DB_PORT','3306'))

print('Host:', host)
print('User (env):', repr(user))
print('Pass len:', len(pwd) if pwd else 0)

# Probar 'administrador' y 'administrador@ev-mysql-vecinal'
candidates = [user, f"{user}@{host.split('.')[0]}"]

last_err = None
for u in candidates:
    try:
        print('\nProbando usuario:', repr(u))
        conn = pymysql.connect(
            host=host, user=u, password=pwd, db=dbname, port=port,
            ssl={'ssl_mode':'REQUIRED'}
        )
        with conn.cursor() as c:
            c.execute('SELECT CURRENT_USER(), VERSION()')
            cu, ver = c.fetchone()
            print('Conectado como:', cu, '| MySQL:', ver)
        conn.close()
        print('OK')
        break
    except Exception as e:
        last_err = e
        print('FALLÓ:', type(e).__name__, e)
else:
    raise last_err
