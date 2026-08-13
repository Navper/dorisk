from fastapi import Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.auth_service import decode_access_token
from backend.db_local import get_db
from backend.config import ADMIN_EMAIL

class AppUser(BaseModel):
    id: str
    email: str
    username: str

async def get_current_user(authorization: str = Header(None)) -> AppUser:
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autorización faltante")
    
    try:
        parts = authorization.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Formato de token inválido. Usar 'Bearer <token>'")
        
        token = parts[1]
        
        # Validar y decodificar el token JWT nativo
        payload = decode_access_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        
        user_id = payload["sub"]
        
        # Buscar usuario en la base de datos local SQLite
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, username, is_approved FROM users WHERE id = ?", (user_id,))
            user_row = cursor.fetchone()
            
            if not user_row:
                raise HTTPException(status_code=401, detail="Usuario no encontrado")
            
            email = user_row["email"]
            username = user_row["username"]
            is_approved = user_row["is_approved"]
            
            # Verificar aprobación si no es administrador
            if email != ADMIN_EMAIL and not is_approved:
                raise HTTPException(
                    status_code=403,
                    detail="Tu cuenta está pendiente de aprobación por el administrador."
                )
            
            return AppUser(id=user_id, email=email, username=username)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error de autenticación: {str(e)}")
