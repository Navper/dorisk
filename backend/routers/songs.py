from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from backend.db import supabase_client, admin_client
from backend.auth_deps import get_current_user, AppUser
from backend.pipeline import process_song_submission
from backend.config import DEV_MODE, ADMIN_EMAIL

router = APIRouter(prefix="/api/songs", tags=["songs"])

class SubmitSongRequest(BaseModel):
    url: str
    playlist_id: str

class VoteRequest(BaseModel):
    score: int

def get_cooldown_remaining(user_id: str, playlist_id: str) -> Optional[float]:
    """
    Retorna los segundos restantes antes de poder subir una canción (reinicio diario a medianoche UTC).
    """
    if not admin_client:
        return None
        
    try:
        res = admin_client.table("songs") \
            .select("created_at") \
            .eq("user_id", user_id) \
            .eq("playlist_id", playlist_id) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
            
        if res.data:
            last_date_str = res.data[0]["created_at"]
            last_date = datetime.fromisoformat(last_date_str.replace("Z", "+00:00")).astimezone(timezone.utc)
            now = datetime.now(timezone.utc)
            
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Si la última canción se subió en el día UTC actual, está en cooldown hasta la siguiente medianoche
            if last_date >= start_of_day:
                next_midnight = start_of_day + timedelta(days=1)
                return (next_midnight - now).total_seconds()
    except Exception as e:
        print(f"Error al verificar cooldown: {e}")
        
    return None

@router.post("/submit")
async def submit_song(data: SubmitSongRequest, user: AppUser = Depends(get_current_user)):
    user_id = user.id
    email = user.email
    is_admin = email == ADMIN_EMAIL
    
    # 1. Validar cooldown de 24 horas para ESTA playlist (excepto admins)
    if not is_admin:
        seconds_left = get_cooldown_remaining(user_id, data.playlist_id)
        if seconds_left:
            hours = int(seconds_left // 3600)
            minutes = int((seconds_left % 3600) // 60)
            seconds = int(seconds_left % 60)
            raise HTTPException(
                status_code=400,
                detail=f"Debes esperar {hours:02d}:{minutes:02d}:{seconds:02d} antes de subir otra canción a esta playlist."
            )
        
    try:
        song = process_song_submission(data.url, user_id, data.playlist_id)
        return {"message": "¡Canción agregada con éxito!", "song": song}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feed")
async def get_today_feed(user: AppUser = Depends(get_current_user)):
    user_id = user.id
    
    if not admin_client:
        return []
        
    try:
        # 1. Obtener las playlists a las que el usuario tiene acceso
        pu_res = admin_client.table("playlist_users").select("playlist_id").eq("user_id", user_id).execute()
        playlist_ids = [p["playlist_id"] for p in pu_res.data]
        
        if not playlist_ids:
            return []
            
        # 2. Obtener los detalles de esas playlists
        pl_res = admin_client.table("playlists").select("*").in_("id", playlist_ids).execute()
        playlists_data = {p["id"]: p for p in pl_res.data}
        
        # 3. Obtener las canciones de estas playlists (últimos 7 días)
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        res = admin_client.table("songs") \
            .select("*, profiles(username, avatar_url)") \
            .in_("playlist_id", playlist_ids) \
            .gt("created_at", one_week_ago.isoformat()) \
            .order("created_at", desc=True) \
            .execute()
            
        songs = res.data or []
        
        # Estructurar la respuesta
        playlists_dict = {}
        for pid, pdata in playlists_data.items():
            playlists_dict[pid] = {
                "id": pid,
                "name": pdata["name"],
                "emoji": "🎧",
                "gradient": "linear-gradient(135deg,#3a2255,#7c5fa0)",
                "tracks": 0,
                "platforms": ["yt"] if pdata.get("youtube_id") else [],
                "songs": []
            }
        
        for s in songs:
            pid = s["playlist_id"]
            if pid not in playlists_dict:
                continue
                
            song_id = s["id"]
            owner_id = s["user_id"]
            username = s.get("profiles", {}).get("username", "Melómano")
            
            votes_res = admin_client.table("votes").select("user_id, score").eq("song_id", song_id).execute()
            votes_list = votes_res.data or []
            
            user_vote = None
            scores = []
            for v in votes_list:
                scores.append(v["score"])
                if v["user_id"] == user_id:
                    user_vote = v["score"]
                    
            avg = round(sum(scores) / len(scores), 1) if scores else 0.0
            
            created_at = datetime.fromisoformat(s["created_at"].replace("Z", "+00:00")).astimezone(timezone.utc)
            delta = datetime.now(timezone.utc) - created_at
            if delta.days > 0:
                ago = f"hace {delta.days}d"
            elif delta.seconds >= 3600:
                ago = f"hace {delta.seconds // 3600}h"
            elif delta.seconds >= 60:
                ago = f"hace {delta.seconds // 60}m"
            else:
                ago = "hace unos segundos"

            youtube_playlist_id = playlists_data.get(pid, {}).get("youtube_id")
            yt_id = s.get("youtube_video_id")
            song_url = f"https://www.youtube.com/watch?v={yt_id}&list={youtube_playlist_id}" if yt_id and youtube_playlist_id else s.get("original_url")

            playlists_dict[pid]["songs"].append({
                "id": song_id,
                "track": s["title"],
                "artist": s["artist"],
                "by": f"@{username}",
                "art": s["art_url"] or "🎵",
                "bg": "#1e1828,#2e2640",
                "isOwn": owner_id == user_id,
                "userVote": user_vote,
                "votes_count": len(scores),
                "average_score": avg,
                "votes": scores,
                "ago": ago,
                "song_url": song_url
            })
            playlists_dict[pid]["tracks"] += 1
            
        return list(playlists_dict.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el feed: {str(e)}")

@router.post("/{song_id}/vote")
async def vote_song(song_id: str, data: VoteRequest, user: AppUser = Depends(get_current_user)):
    user_id = user.id
    
    if data.score < 1 or data.score > 7:
        raise HTTPException(status_code=400, detail="La puntuación debe ser entre 1 y 7 estrellas.")
        
    if not admin_client:
        return {"message": "Voto registrado exitosamente (modo demo)"}
        
    try:
        # 1. Verificar que la canción exista y no sea del usuario propio
        song_res = admin_client.table("songs").select("user_id").eq("id", song_id).maybe_single().execute()
        if not song_res or not song_res.data:
            raise HTTPException(status_code=404, detail="La canción no existe.")
            
        song_owner = song_res.data["user_id"]
        if song_owner == user_id:
            raise HTTPException(status_code=400, detail="No puedes votar tu propia canción.")
            
        # 2. Registrar o actualizar voto (upsert)
        vote_data = {
            "song_id": song_id,
            "user_id": user_id,
            "score": data.score
        }
        admin_client.table("votes").upsert(vote_data, on_conflict="song_id,user_id").execute()
        return {"message": "Voto registrado correctamente."}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar voto: {str(e)}")

@router.get("/cooldown/{playlist_id}")
async def check_playlist_cooldown(playlist_id: str, user: AppUser = Depends(get_current_user)):
    user_id = user.id
    email = user.email
    
    if email == ADMIN_EMAIL:
        return {"cooldown": False, "seconds_left": 0}
        
    seconds_left = get_cooldown_remaining(user_id, playlist_id)
    if seconds_left:
        # Obtener los detalles de la canción subida hoy a esta playlist por este usuario
        song_data = None
        if admin_client:
            song_res = admin_client.table("songs") \
                .select("*") \
                .eq("user_id", user_id) \
                .eq("playlist_id", playlist_id) \
                .order("created_at", desc=True) \
                .limit(1) \
                .execute()
                
            if song_res.data:
                s = song_res.data[0]
                song_data = {
                    "title": s["title"],
                    "artist": s["artist"],
                    "art_url": s["art_url"] or "🎵",
                    "youtube_video_id": s["youtube_video_id"]
                }
        return {"cooldown": True, "seconds_left": seconds_left, "today_song": song_data}
        
    return {"cooldown": False, "seconds_left": 0}

@router.get("/leaderboard/{playlist_id}")
async def get_playlist_leaderboard(playlist_id: str, user = Depends(get_current_user)):
    if not admin_client:
        raise HTTPException(status_code=500, detail="BD no configurada")
        
    try:
        # 1. Obtener todos los IDs de usuario asociados a esta playlist
        pu_res = admin_client.table("playlist_users") \
            .select("user_id") \
            .eq("playlist_id", playlist_id) \
            .execute()
        users_in_playlist = pu_res.data or []
        user_ids = [u["user_id"] for u in users_in_playlist]
        
        if not user_ids:
            return []
            
        # 2. Obtener los perfiles correspondientes
        profiles_res = admin_client.table("profiles") \
            .select("id, username, email, avatar_url") \
            .in_("id", user_ids) \
            .execute()
        profiles = profiles_res.data or []
        
        # 3. Obtener todas las canciones subidas a esta playlist
        songs_res = admin_client.table("songs") \
            .select("id, user_id") \
            .eq("playlist_id", playlist_id) \
            .execute()
        songs = songs_res.data or []
        song_ids = [s["id"] for s in songs]
        
        # 4. Obtener todos los votos asociados a estas canciones
        votes = []
        if song_ids:
            votes_res = admin_client.table("votes") \
                .select("song_id, score") \
                .in_("song_id", song_ids) \
                .execute()
            votes = votes_res.data or []
            
        # 5. Calcular el puntaje para cada usuario
        song_to_user = {s["id"]: s["user_id"] for s in songs}
        user_scores = {uid: 0 for uid in user_ids}
        
        for v in votes:
            creator_id = song_to_user.get(v["song_id"])
            if creator_id in user_scores:
                user_scores[creator_id] += v["score"]
                
        # 6. Formatear la respuesta
        leaderboard = []
        for p in profiles:
            uid = p["id"]
            username = p.get("username", "Melómano")
            avatar_url = p.get("avatar_url")
            if not avatar_url:
                avatar_url = f"https://api.dicebear.com/7.x/pixel-art/svg?seed={username}"
                
            leaderboard.append({
                "username": username,
                "avatar_url": avatar_url,
                "score": user_scores.get(uid, 0)
            })
            
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        return leaderboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar leaderboard: {str(e)}")
