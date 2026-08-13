import os
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, EmailStr

from backend.db_local import get_db, AVATARS_DIR
from backend.auth_service import hash_password, verify_password, create_access_token
from backend.auth_deps import get_current_user, AppUser
from backend.config import ADMIN_EMAIL

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class ProfileUpdateRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

@router.post("/register")
async def register_user(data: RegisterRequest):
    username = data.username.strip()
    email = data.email.strip().lower()
    password = data.password.strip()

    if len(username) < 3:
        raise HTTPException(status_code=400, detail="El nombre de usuario debe tener al menos 3 caracteres")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")

    user_id = str(uuid.uuid4())
    pwd_hash = hash_password(password)
    avatar_url = f"https://api.dicebear.com/7.x/pixel-art/svg?seed={username}"
    is_approved = 1  # Auto-aprobado o administrado
    is_admin = 1 if email == ADMIN_EMAIL.lower() else 0
    now_iso = datetime.now(timezone.utc).isoformat()

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Verificar si ya existe usuario o email
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            existing = cursor.fetchone()
            if existing:
                raise HTTPException(status_code=400, detail="El nombre de usuario o correo ya está registrado")

            cursor.execute("""
                INSERT INTO users (id, email, username, password_hash, avatar_url, is_approved, is_admin, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, email, username, pwd_hash, avatar_url, is_approved, is_admin, now_iso))
            conn.commit()

        token = create_access_token({"sub": user_id, "username": username, "email": email})
        return {
            "message": "Registro completado con éxito",
            "token": token,
            "username": username
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en registro: {str(e)}")

@router.post("/login")
async def login_user(data: LoginRequest):
    login_input = data.username_or_email.strip()
    password = data.password.strip()

    with get_db() as conn:
        cursor = conn.cursor()
        if "@" in login_input:
            cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (login_input.lower(),))
        else:
            cursor.execute("SELECT * FROM users WHERE LOWER(username) = ?", (login_input.lower(),))
            
        user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    # Verificar aprobación si no es administrador
    if user["email"] != ADMIN_EMAIL and not user["is_approved"]:
        raise HTTPException(status_code=403, detail="Tu cuenta está pendiente de aprobación por el administrador.")

    token = create_access_token({
        "sub": user["id"],
        "username": user["username"],
        "email": user["email"]
    })

    return {
        "token": token,
        "username": user["username"]
    }

@router.get("/profile")
async def get_profile(user: AppUser = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, avatar_url, is_approved, is_admin, created_at FROM users WHERE id = ?", (user.id,))
        row = cursor.fetchone()
        
    if not row:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
        
    return dict(row)

@router.post("/profile/update")
async def update_profile(data: ProfileUpdateRequest, user: AppUser = Depends(get_current_user)):
    user_id = user.id

    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Si cambia el nombre de usuario
        if data.username:
            new_username = data.username.strip()
            if len(new_username) < 3:
                raise HTTPException(status_code=400, detail="El nombre de usuario debe tener al menos 3 caracteres")
                
            cursor.execute("SELECT id FROM users WHERE LOWER(username) = ? AND id != ?", (new_username.lower(), user_id))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
                
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            
        # 2. Si cambia la contraseña
        if data.password:
            new_password = data.password.strip()
            if len(new_password) < 6:
                raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
                
            new_pwd_hash = hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_pwd_hash, user_id))
            
        conn.commit()

    return {"message": "Perfil actualizado correctamente"}

@router.post("/profile/avatar")
async def upload_avatar(file: UploadFile = File(...), user: AppUser = Depends(get_current_user)):
    user_id = user.id

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    try:
        contents = await file.read()
        max_size = 60 * 1024 * 1024  # 60MB
        if len(contents) > max_size:
            raise HTTPException(status_code=400, detail="El archivo es demasiado grande. Máximo 60MB.")

        ext = file.filename.split(".")[-1] if "." in file.filename else "png"
        filename = f"{user_id}.{ext}"
        file_path = os.path.join(AVATARS_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        avatar_url = f"/static/avatars/{filename}"

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET avatar_url = ? WHERE id = ?", (avatar_url, user_id))
            conn.commit()

        return {"message": "Avatar actualizado correctamente", "avatar_url": avatar_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al subir avatar: {str(e)}")
