from supabase import create_client, Client
from backend.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY

# Crear clientes globales de Supabase
supabase_client: Client = None
admin_client: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"❌ Error al iniciar el cliente de Supabase: {e}")
        
if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    try:
        admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception as e:
        print(f"❌ Error al iniciar el cliente admin de Supabase: {e}")
else:
    print("⚠️ Supabase no configurado completamente. Las consultas de insercion pueden fallar por RLS.")
