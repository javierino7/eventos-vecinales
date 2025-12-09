import os, pymysql
from pathlib import Path

# Cargar .env y limpiar comillas
env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        k, _, v = line.partition('=')
        v = v.strip().strip("'").strip('"')
        os.environ[k.strip()] = v

conn = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=int(os.getenv('DB_PORT','3306')),
    ssl={'ssl_mode':'REQUIRED'}
)
with conn.cursor() as c:
    c.execute("CREATE DATABASE IF NOT EXISTS eventos_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("DB creada/verificada: eventos_db")
conn.commit(); conn.close()
