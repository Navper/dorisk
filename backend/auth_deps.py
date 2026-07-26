from fastapi import Header, HTTPException
from backend.db import supabase_client
from pydantic import BaseModel

class AppUser(BaseModel):
    id: str
    email: str
    username: str

async def get_current_user(authorization: str = Header(None)) -> AppUser:
    if not supabase_client:
        return AppUser(id="00000000-0000-0000-0000-000000000000", email="dev@dorisk.com", username="Developer")
        
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autorización faltante")
    
    try:
        parts = authorization.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Formato de token inválido. Usar 'Bearer <token>'")
        
        token = parts[1]
        # Validar el token con Supabase
        res = supabase_client.auth.get_user(token)
        if not res or not res.user:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        # Verificar aprobación
        from backend.db import admin_client
        from backend.config import ADMIN_EMAIL
        if admin_client:
            if res.user.email != ADMIN_EMAIL:
                profile_res = admin_client.table("profiles").select("is_approved").eq("id", res.user.id).maybe_single().execute()
                if profile_res and profile_res.data:
                    if not profile_res.data.get("is_approved", False):
                        raise HTTPException(
                            status_code=403,
                            detail="Tu cuenta está pendiente de aprobación por el administrador."
                        )
        meta = getattr(res.user, "user_metadata", {}) or {}
        username = meta.get("username", res.user.email.split("@")[0])
        return AppUser(id=res.user.id, email=res.user.email, username=username)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error de autenticación: {str(e)}")
