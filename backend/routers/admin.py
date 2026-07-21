from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List

from backend.config import DEV_MODE, ADMIN_EMAIL
from backend.auth_deps import get_current_user, AppUser
from backend.db import admin_client
from backend.services.youtube_client import get_playlist_details
from backend.weekly_sweep import run_weekly_sweep

router = APIRouter(prefix="/api/admin", tags=["admin"])

class PlaylistCreate(BaseModel):
    youtube_id: str

class PlaylistAssign(BaseModel):
    user_ids: List[str]

def check_admin(user: AppUser):
    if not user.email or user.email != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Acceso denegado: esta acción requiere permisos de administrador.")

@router.get("/config")
async def get_config(user = Depends(get_current_user)):
    """Retorna la configuración actual."""
    try:
        check_admin(user)
    except HTTPException:
        return {"dev_mode": False}
        
    if not DEV_MODE:
        return {"dev_mode": False}
        
    return {
        "dev_mode": True
    }

@router.get("/playlists")
async def get_playlists(user = Depends(get_current_user)):
    check_admin(user)
    if not admin_client:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
    res = admin_client.table("playlists").select("*").order("created_at", desc=False).execute()
    return res.data

@router.post("/playlists")
async def create_playlist(data: PlaylistCreate, user = Depends(get_current_user)):
    check_admin(user)
    if not DEV_MODE:
        raise HTTPException(status_code=403, detail="Esta acción solo está permitida en DEV_MODE.")
    if not admin_client:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
    
    name = get_playlist_details(data.youtube_id)
    user_id = user.id
    
    new_pl = {
        "name": name,
        "youtube_id": data.youtube_id,
        "created_by": user_id
    }
    
    res = admin_client.table("playlists").insert(new_pl).execute()
    return res.data[0] if res.data else {"error": "No se pudo crear"}

@router.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: str, user = Depends(get_current_user)):
    check_admin(user)
    if not DEV_MODE:
        raise HTTPException(status_code=403, detail="Esta acción solo está permitida en DEV_MODE.")
    if not admin_client:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
    
    admin_client.table("playlists").delete().eq("id", playlist_id).execute()
    return {"message": "Playlist eliminada"}

@router.get("/playlists/{playlist_id}/users")
async def get_playlist_users(playlist_id: str, user = Depends(get_current_user)):
    check_admin(user)
    if not admin_client:
        raise HTTPException(status_code=500, detail="BD no configurada")
    
    res = admin_client.table("playlist_users").select("user_id").eq("playlist_id", playlist_id).execute()
    return [r["user_id"] for r in res.data]

@router.post("/playlists/{playlist_id}/users")
async def assign_playlist_users(playlist_id: str, data: PlaylistAssign, user = Depends(get_current_user)):
    check_admin(user)
    if not DEV_MODE:
        raise HTTPException(status_code=403, detail="Esta acción solo está permitida en DEV_MODE.")
    if not admin_client:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
    
    # Eliminar todos y recrear (estrategia simple)
    admin_client.table("playlist_users").delete().eq("playlist_id", playlist_id).execute()
    
    inserts = [{"playlist_id": playlist_id, "user_id": uid} for uid in data.user_ids]
    if inserts:
        admin_client.table("playlist_users").insert(inserts).execute()
        
    return {"message": "Usuarios actualizados"}

class ApproveUserRequest(BaseModel):
    approve: bool

@router.post("/users/{user_id}/approve")
async def approve_user(user_id: str, data: ApproveUserRequest, user = Depends(get_current_user)):
    check_admin(user)
    if not DEV_MODE:
        raise HTTPException(status_code=403, detail="Esta acción solo está permitida en DEV_MODE.")
    if not admin_client:
        raise HTTPException(status_code=500, detail="BD no configurada")
        
    if data.approve:
        admin_client.table("profiles").update({"is_approved": True}).eq("id", user_id).execute()
        return {"message": "Usuario aprobado con éxito."}
    else:
        # Rechazar: eliminar el perfil y eliminar el usuario del auth de Supabase
        admin_client.table("profiles").delete().eq("id", user_id).execute()
        try:
            admin_client.auth.admin.delete_user(user_id)
        except Exception as e:
            print(f"Error al eliminar usuario de auth: {e}")
        return {"message": "Usuario rechazado y eliminado con éxito."}

@router.get("/users")
async def get_all_users(user = Depends(get_current_user)):
    check_admin(user)
    if not DEV_MODE:
        raise HTTPException(status_code=403, detail="Esta acción solo está permitida en DEV_MODE.")
    if not admin_client:
        raise HTTPException(status_code=500, detail="BD no configurada")
    
    # Intentar desde profiles primero
    res = admin_client.table("profiles").select("id, username, email, is_approved").execute()
    if res.data:
        return res.data
    
    # Fallback: obtener directamente de auth.users via admin API
    try:
        auth_users = admin_client.auth.admin.list_users()
        users = []
        for u in auth_users:
            meta = getattr(u, 'user_metadata', {}) or {}
            users.append({
                "id": u.id,
                "username": meta.get("username", u.email.split("@")[0]),
                "email": u.email,
                "is_approved": True
            })
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

@router.post("/sweep")
async def force_weekly_sweep(user: AppUser = Depends(get_current_user)):
    check_admin(user)
    success = run_weekly_sweep()
    if success:
        return {"message": "Cierre semanal forzado con éxito. Playlists vaciadas y ganador guardado."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar el cierre semanal. Revisa los logs del servidor."
        )
