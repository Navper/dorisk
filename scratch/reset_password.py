import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import admin_client

def reset_password():
    if not admin_client:
        print("❌ Error: admin_client no disponible (revisa las credenciales de Supabase)")
        return
    
    # 1. Buscar en profiles por username o email
    search_term = "erikasolarico"
    res = admin_client.table("profiles").select("*").ilike("username", f"%{search_term}%").execute()
    
    users = res.data or []
    if not users:
        # probar buscar por email
        res = admin_client.table("profiles").select("*").ilike("email", f"%{search_term}%").execute()
        users = res.data or []

    if not users:
        # buscar directamente en auth.users si es posible
        try:
            auth_users = admin_client.auth.admin.list_users()
            for u in auth_users:
                meta = getattr(u, 'user_metadata', {}) or {}
                if search_term.lower() in (u.email or "").lower() or search_term.lower() in (meta.get("username", "")).lower():
                    users.append({"id": u.id, "email": u.email, "username": meta.get("username", u.email)})
        except Exception as e:
            print(f"Error listando usuarios auth: {e}")

    if not users:
        print(f"❌ No se encontró ningún usuario con el nombre/correo '{search_term}'.")
        return

    for target in users:
        user_id = target["id"]
        email = target.get("email") or target.get("id")
        username = target.get("username")
        print(f"Encontrado usuario: {username} ({email}) - ID: {user_id}")
        
        try:
            admin_client.auth.admin.update_user_by_id(
                user_id,
                {"password": "123456"}
            )
            print(f"✅ Contraseña para {username} ({email}) actualizada con éxito a: 123456")
        except Exception as e:
            print(f"❌ Error actualizando contraseña para {user_id}: {e}")

if __name__ == "__main__":
    reset_password()
