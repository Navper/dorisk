import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv("backend/.env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

if not url or not key:
    print("Faltan credenciales")
    exit(1)

client = create_client(url, key)

print("--- EXAMINANDO TABLAS DE SUPABASE ---")

for table in ["profiles", "playlists", "playlist_users", "songs", "votes", "weekly_winners"]:
    try:
        res = client.table(table).select("*").execute()
        print(f"Tabla '{table}': {len(res.data or [])} registros")
    except Exception as e:
        print(f"Error leyendo '{table}': {e}")

try:
    users = client.auth.admin.list_users()
    print(f"Usuarios en Auth: {len(users)}")
    for u in users:
        print(f" - ID: {u.id}, Email: {u.email}, Meta: {u.user_metadata}")
except Exception as e:
    print(f"Error leyendo Auth: {e}")
