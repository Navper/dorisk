import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from backend.config import DEV_MODE, ADMIN_EMAIL
from backend.auth_deps import get_current_user, AppUser
from backend.db_local import get_db
from backend.services.youtube_client import get_playlist_details
from backend.weekly_sweep import run_weekly_sweep

router = APIRouter(prefix="/api/admin", tags=["admin"])

class PlaylistCreate(BaseModel):
    youtube_id: str

class PlaylistAssign(BaseModel):
    user_ids: List[str]

class ApproveUserRequest(BaseModel):
    approve: bool

def check_admin(user: AppUser):
    if not user.email or user.email.lower() != ADMIN_EMAIL.lower():
        raise HTTPException(status_code=403, detail="Acceso denegado: esta acción requiere permisos de administrador.")

@router.get("/config")
async def get_config(user = Depends(get_current_user)):
    try:
        check_admin(user)
    except HTTPException:
        return {"dev_mode": False}
        
    return {"dev_mode": True}

@router.get("/playlists")
async def get_playlists(user = Depends(get_current_user)):
    check_admin(user)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM playlists ORDER BY created_at ASC")
        return [dict(row) for row in cursor.fetchall()]

@router.post("/playlists")
async def create_playlist(data: PlaylistCreate, user = Depends(get_current_user)):
    check_admin(user)
    name = get_playlist_details(data.youtube_id)
    new_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO playlists (id, name, youtube_id, created_by, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (new_id, name, data.youtube_id, user.id, now_iso))
        conn.commit()
        
        cursor.execute("SELECT * FROM playlists WHERE id = ?", (new_id,))
        return dict(cursor.fetchone())

@router.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: str, user = Depends(get_current_user)):
    check_admin(user)
    with get_db() as conn:
        cursor = conn.cursor()
        # 1. Limpiar votos asociados a canciones de esta playlist
        cursor.execute("DELETE FROM votes WHERE song_id IN (SELECT id FROM songs WHERE playlist_id = ?)", (playlist_id,))
        # 2. Limpiar canciones, accesos y playlist
        cursor.execute("DELETE FROM songs WHERE playlist_id = ?", (playlist_id,))
        cursor.execute("DELETE FROM playlist_users WHERE playlist_id = ?", (playlist_id,))
        cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
        conn.commit()
    
    return {"message": "Playlist eliminada de la app Dorisk (YouTube permanece intacto como archivo)"}

@router.get("/playlists/{playlist_id}/users")
async def get_playlist_users(playlist_id: str, user = Depends(get_current_user)):
    check_admin(user)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM playlist_users WHERE playlist_id = ?", (playlist_id,))
        return [r["user_id"] for r in cursor.fetchall()]

@router.post("/playlists/{playlist_id}/users")
async def assign_playlist_users(playlist_id: str, data: PlaylistAssign, user = Depends(get_current_user)):
    check_admin(user)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM playlist_users WHERE playlist_id = ?", (playlist_id,))
        for uid in data.user_ids:
            cursor.execute("INSERT INTO playlist_users (playlist_id, user_id) VALUES (?, ?)", (playlist_id, uid))
        conn.commit()
        
    return {"message": "Usuarios actualizados"}

@router.post("/users/{user_id}/approve")
async def approve_user(user_id: str, data: ApproveUserRequest, user = Depends(get_current_user)):
    check_admin(user)
    with get_db() as conn:
        cursor = conn.cursor()
        if data.approve:
            cursor.execute("UPDATE users SET is_approved = 1 WHERE id = ?", (user_id,))
            msg = "Usuario aprobado con éxito."
        else:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            msg = "Usuario rechazado y eliminado con éxito."
        conn.commit()
        
    return {"message": msg}

@router.get("/users")
async def get_all_users(user = Depends(get_current_user)):
    check_admin(user)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, is_approved FROM users ORDER BY created_at DESC")
        return [dict(r) for r in cursor.fetchall()]

@router.post("/sweep")
async def force_weekly_sweep(user: AppUser = Depends(get_current_user)):
    check_admin(user)
    success = run_weekly_sweep()
    if success:
        return {"message": "Cierre semanal forzado con éxito. Ganadores registrados y playlists intactas."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar el cierre semanal. Revisa los logs del servidor."
        )
