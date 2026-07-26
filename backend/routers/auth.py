from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, EmailStr
from backend.db import supabase_client, admin_client
from backend.auth_deps import get_current_user, AppUser
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

@router.post("/register")
async def register_user(data: RegisterRequest):
    if not supabase_client:
        return {"message": "Modo desarrollo: Registro de demostración exitoso", "token": "dummy-dev-token", "username": data.username}
    
    try:
        # Registrar en el auth de Supabase
        res = supabase_client.auth.sign_up({
            "email": data.email,
            "password": data.password,
            "options": {
                "data": {
                    "username": data.username
                }
            }
        })
        
        # Insertar perfil publico usando el service_role (bypass RLS)
        if res.user:
            try:
                if admin_client:
                    profile_data = {
                        "id": res.user.id,
                        "username": data.username,
                        "email": data.email,
                        "avatar_url": f"https://api.dicebear.com/7.x/pixel-art/svg?seed={data.username}"
                    }
                    admin_client.table("profiles").upsert(profile_data).execute()
                    print(f"Perfil creado exitosamente para {data.username}")
                else:
                    print("admin_client no configurado, perfil no creado")
            except Exception as pe:
                print(f"Nota: Error al crear perfil: {pe}")
        
        token = res.session.access_token if res.session else "token-pending-email-confirm"
        return {
            "message": "Registro completado",
            "token": token,
            "username": data.username
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en registro: {str(e)}")

@router.post("/login")
async def login_user(data: LoginRequest):
    if not supabase_client:
        return {"token": "dummy-dev-token", "username": data.username_or_email or "Developer"}

    email = data.username_or_email
    
    # Si ingreso el username en lugar del email, buscamos el email en profiles
    if "@" not in data.username_or_email:
        try:
            if admin_client:
                profile = admin_client.table("profiles").select("email").eq("username", data.username_or_email).maybe_single().execute()
                if profile and profile.data and profile.data.get("email"):
                    email = profile.data["email"]
                else:
                    raise HTTPException(status_code=400, detail="Usuario no encontrado. Prueba con tu email.")
            else:
                raise HTTPException(status_code=400, detail="Configuracion incompleta del servidor.")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error buscando usuario: {str(e)}")

    try:
        res = supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": data.password
        })
        
        username = res.user.user_metadata.get("username", "Melomano")
        return {
            "token": res.session.access_token,
            "username": username
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

class ResetPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/reset-password-request")
async def request_password_reset(data: ResetPasswordRequest):
    if not supabase_client:
        return {"message": "Modo desarrollo: link de reseteo falso enviado."}
        
    try:
        # Supabase enviará un correo con un link que apunta al SITE_URL con #access_token=...&type=recovery
        supabase_client.auth.reset_password_for_email(data.email)
        return {"message": "Si el correo está registrado, recibirás un enlace de recuperación."}
    except Exception as e:
        # Por seguridad no revelamos si el correo existe o no
        return {"message": "Si el correo está registrado, recibirás un enlace de recuperación."}

class ProfileUpdateRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

@router.post("/profile/update")
async def update_profile(data: ProfileUpdateRequest, user: AppUser = Depends(get_current_user)):
    user_id = user.id
    
    if not admin_client:
        raise HTTPException(status_code=500, detail="BD no configurada")
        
    try:
        # 1. Si se cambia el nombre de usuario, validar y actualizar
        if data.username:
            new_username = data.username.strip()
            if len(new_username) < 3:
                raise HTTPException(status_code=400, detail="El nombre de usuario debe tener al menos 3 caracteres")
                
            # Verificar si ya existe en profiles
            existing = admin_client.table("profiles").select("id").eq("username", new_username).neq("id", user_id).execute()
            if existing.data:
                raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
                
            admin_client.table("profiles").update({"username": new_username}).eq("id", user_id).execute()
            
        # 2. Si se cambia la contraseña, actualizarla en Supabase Auth usando admin client
        if data.password:
            new_password = data.password.strip()
            if len(new_password) < 6:
                raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
            
            admin_client.auth.admin.update_user_by_id(
                user_id,
                attributes={"password": new_password}
            )
            
        return {"message": "Perfil actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar perfil: {str(e)}")

@router.post("/profile/avatar")
async def upload_avatar(file: UploadFile = File(...), user: AppUser = Depends(get_current_user)):
    user_id = user.id
    
    if not admin_client:
        raise HTTPException(status_code=500, detail="BD no configurada")
        
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
    try:
        contents = await file.read()
        
        # Limitar tamaño a 60MB
        max_size = 60 * 1024 * 1024  # 60MB en bytes
        if len(contents) > max_size:
            raise HTTPException(status_code=400, detail="El archivo es demasiado grande. Máximo 60MB.")
        
        file_path = f"{user_id}_avatar.png"
        
        # Subir con override
        try:
            admin_client.storage.from_("avatars").upload(
                path=file_path,
                file=contents,
                file_options={"content-type": file.content_type, "x-upsert": "true"}
            )
        except Exception as upload_err:
            try:
                admin_client.storage.from_("avatars").remove([file_path])
            except:
                pass
            admin_client.storage.from_("avatars").upload(
                path=file_path,
                file=contents,
                file_options={"content-type": file.content_type}
            )
            
        avatar_url = admin_client.storage.from_("avatars").get_public_url(file_path)
        
        admin_client.table("profiles").update({"avatar_url": avatar_url}).eq("id", user_id).execute()
        
        return {"message": "Avatar actualizado correctamente", "avatar_url": avatar_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al subir avatar: {str(e)}")

@router.get("/profile")
async def get_profile(user: AppUser = Depends(get_current_user)):
    user_id = user.id
    if not admin_client or user_id == "00000000-0000-0000-0000-000000000000":
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar_url": f"https://api.dicebear.com/7.x/pixel-art/svg?seed={user.username}"
        }
        
    res = admin_client.table("profiles").select("*").eq("id", user_id).maybe_single().execute()
    if not res.data:
        email = user.email
        username = user.username
        avatar_url = f"https://api.dicebear.com/7.x/pixel-art/svg?seed={username}"
        profile_data = {
            "id": user_id,
            "username": username,
            "email": email,
            "avatar_url": avatar_url
        }
        admin_client.table("profiles").insert(profile_data).execute()
        return profile_data
        
    return res.data

