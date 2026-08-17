from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from backend.db_local import get_db
from backend.auth_deps import get_current_user, AppUser
from backend.pipeline import process_song_submission
from backend.config import ADMIN_EMAIL

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
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT created_at FROM songs 
            WHERE user_id = ? AND playlist_id = ? 
            ORDER BY created_at DESC LIMIT 1
        """, (user_id, playlist_id))
        row = cursor.fetchone()

        if row and row["created_at"]:
            try:
                last_date = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")).astimezone(timezone.utc)
                now = datetime.now(timezone.utc)
                start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
                
                if last_date >= start_of_day:
                    next_midnight = start_of_day + timedelta(days=1)
                    return (next_midnight - now).total_seconds()
            except Exception as e:
                print(f"Error parseando fecha de cooldown: {e}")

    return None

@router.post("/submit")
async def submit_song(data: SubmitSongRequest, user: AppUser = Depends(get_current_user)):
    user_id = user.id
    email = user.email
    is_admin = email.lower() == ADMIN_EMAIL.lower()
    
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
    
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # 1. Obtener playlists a las que el usuario tiene acceso
            cursor.execute("""
                SELECT p.id, p.name, p.youtube_id 
                FROM playlists p
                INNER JOIN playlist_users pu ON p.id = pu.playlist_id
                WHERE pu.user_id = ?
            """, (user_id,))
            playlists = cursor.fetchall()
            
            if not playlists:
                return []
                
            playlist_ids = [p["id"] for p in playlists]
            playlists_dict = {}
            for p in playlists:
                pid = p["id"]
                playlists_dict[pid] = {
                    "id": pid,
                    "name": p["name"],
                    "emoji": "🎧",
                    "gradient": "linear-gradient(135deg,#3a2255,#7c5fa0)",
                    "tracks": 0,
                    "platforms": ["yt"] if p["youtube_id"] else [],
                    "songs": []
                }
                
            # 2. Obtener TODAS las canciones de estas playlists (sin filtro temporal)
            placeholders = ",".join("?" * len(playlist_ids))
            
            cursor.execute(f"""
                SELECT s.*, u.username, u.avatar_url
                FROM songs s
                LEFT JOIN users u ON s.user_id = u.id
                WHERE s.playlist_id IN ({placeholders})
                ORDER BY s.created_at DESC
            """, playlist_ids)
            songs = cursor.fetchall()
            
            # 3. Obtener todos los votos de estas canciones
            song_ids = [s["id"] for s in songs]
            votes_by_song = {}
            if song_ids:
                v_placeholders = ",".join("?" * len(song_ids))
                cursor.execute(f"SELECT song_id, user_id, score FROM votes WHERE song_id IN ({v_placeholders})", song_ids)
                for v in cursor.fetchall():
                    sid = v["song_id"]
                    if sid not in votes_by_song:
                        votes_by_song[sid] = []
                    votes_by_song[sid].append(dict(v))

            now_utc = datetime.now(timezone.utc)
            for s in songs:
                pid = s["playlist_id"]
                if pid not in playlists_dict:
                    continue
                    
                song_id = s["id"]
                owner_id = s["user_id"]
                username = s["username"] or "Melómano"
                
                song_votes = votes_by_song.get(song_id, [])
                scores = [v["score"] for v in song_votes]
                user_vote = next((v["score"] for v in song_votes if v["user_id"] == user_id), None)
                avg = round(sum(scores) / len(scores), 1) if scores else 0.0
                
                try:
                    created_at = datetime.fromisoformat(s["created_at"].replace("Z", "+00:00")).astimezone(timezone.utc)
                    delta = now_utc - created_at
                    if delta.days > 0:
                        ago = f"hace {delta.days}d"
                    elif delta.seconds >= 3600:
                        ago = f"hace {delta.seconds // 3600}h"
                    elif delta.seconds >= 60:
                        ago = f"hace {delta.seconds // 60}m"
                    else:
                        ago = "hace unos segundos"
                except Exception:
                    ago = "reciente"

                youtube_playlist_id = next((p["youtube_id"] for p in playlists if p["id"] == pid), None)
                yt_id = s["youtube_video_id"]
                song_url = f"https://www.youtube.com/watch?v={yt_id}&list={youtube_playlist_id}" if yt_id and youtube_playlist_id else s["original_url"]

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
        
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT user_id FROM songs WHERE id = ?", (song_id,))
            song = cursor.fetchone()
            if not song:
                raise HTTPException(status_code=404, detail="La canción no existe.")
                
            if song["user_id"] == user_id:
                raise HTTPException(status_code=400, detail="No puedes votar tu propia canción.")
                
            now_iso = datetime.now(timezone.utc).isoformat()
            cursor.execute("""
                INSERT INTO votes (song_id, user_id, score, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(song_id, user_id) DO UPDATE SET score = excluded.score, created_at = excluded.created_at
            """, (song_id, user_id, data.score, now_iso))
            conn.commit()

        return {"message": "Voto registrado correctamente."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar voto: {str(e)}")

@router.get("/cooldown/{playlist_id}")
async def check_playlist_cooldown(playlist_id: str, user: AppUser = Depends(get_current_user)):
    user_id = user.id
    email = user.email
    
    if email.lower() == ADMIN_EMAIL.lower():
        return {"cooldown": False, "seconds_left": 0}
        
    seconds_left = get_cooldown_remaining(user_id, playlist_id)
    if seconds_left:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title, artist, art_url, youtube_video_id 
                FROM songs WHERE user_id = ? AND playlist_id = ? 
                ORDER BY created_at DESC LIMIT 1
            """, (user_id, playlist_id))
            row = cursor.fetchone()
            song_data = dict(row) if row else None
            
        return {"cooldown": True, "seconds_left": seconds_left, "today_song": song_data}
        
    return {"cooldown": False, "seconds_left": 0}

@router.get("/leaderboard/{playlist_id}")
async def get_playlist_leaderboard(playlist_id: str, user = Depends(get_current_user)):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Obtener usuarios de la playlist y sus puntos
            cursor.execute("""
                SELECT u.id, u.username, u.avatar_url,
                       COALESCE(SUM(v.score), 0) as total_score
                FROM playlist_users pu
                INNER JOIN users u ON pu.user_id = u.id
                LEFT JOIN songs s ON s.user_id = u.id AND s.playlist_id = pu.playlist_id
                LEFT JOIN votes v ON v.song_id = s.id
                WHERE pu.playlist_id = ?
                GROUP BY u.id, u.username, u.avatar_url
                ORDER BY total_score DESC
            """, (playlist_id,))
            
            rows = cursor.fetchall()
            leaderboard = []
            for r in rows:
                username = r["username"] or "Melómano"
                avatar_url = r["avatar_url"] or f"https://api.dicebear.com/7.x/pixel-art/svg?seed={username}"
                leaderboard.append({
                    "username": username,
                    "avatar_url": avatar_url,
                    "score": r["total_score"]
                })
                
            return leaderboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar leaderboard: {str(e)}")
