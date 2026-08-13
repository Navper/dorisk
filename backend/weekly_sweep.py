import uuid
from datetime import datetime, timezone, timedelta
from backend.db_local import get_db

def run_weekly_sweep():
    """
    Realiza el cierre semanal automático de Dorisk:
    1. Para CADA playlist, calcula el ganador de la semana (1er puesto).
    2. Lo registra en la tabla `weekly_winners` con trofeo 🏆.
    3. Mantiene intactas las canciones en la web y en YouTube.
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Obtener todas las playlists activas
            cursor.execute("SELECT id, name, youtube_id FROM playlists")
            playlists = cursor.fetchall()
            
            if not playlists:
                print("[SWEEP] No hay playlists registradas.")
                return True
            
            today = datetime.now(timezone.utc)
            start_date = today - timedelta(days=7)
            week_label = f"SEMANA {start_date.strftime('%W')} ({start_date.strftime('%d %b').upper()} - {today.strftime('%d %b').upper()})"
            
            for pl in playlists:
                playlist_id = pl["id"]
                playlist_name = pl["name"]
                
                # Obtener canciones de esta playlist en los últimos 7 días
                cursor.execute("""
                    SELECT s.id, s.title, s.artist, s.art_url, u.username
                    FROM songs s
                    LEFT JOIN users u ON s.user_id = u.id
                    WHERE s.playlist_id = ? AND s.created_at >= ?
                """, (playlist_id, start_date.isoformat()))
                songs = cursor.fetchall()
                
                if not songs:
                    print(f"[SWEEP] Playlist '{playlist_name}': sin canciones esta semana.")
                    continue
                    
                leaderboard = []
                song_ids = [s["id"] for s in songs]
                placeholders = ",".join("?" * len(song_ids))
                
                cursor.execute(f"SELECT song_id, score FROM votes WHERE song_id IN ({placeholders})", song_ids)
                votes_rows = cursor.fetchall()
                
                votes_by_song = {sid: [] for sid in song_ids}
                for v in votes_rows:
                    votes_by_song[v["song_id"]].append(v["score"])
                
                for s in songs:
                    song_id = s["id"]
                    scores = votes_by_song[song_id]
                    avg = round(sum(scores) / len(scores), 1) if scores else 0.0
                    leaderboard.append({
                        "song": s,
                        "average": avg,
                        "votes_count": len(scores)
                    })
                    
                # Ordenar para obtener SOLO el 1er puesto (Ganador de la semana)
                leaderboard.sort(key=lambda x: (x["average"], x["votes_count"]), reverse=True)
                winner_entry = leaderboard[0]
                winner_song = winner_entry["song"]
                winner_avg = winner_entry["average"]
                
                username = winner_song["username"] or "Desconocido"
                winner_id = str(uuid.uuid4())
                now_iso = today.isoformat()
                
                # Registrar ganador en `weekly_winners`
                cursor.execute("""
                    INSERT INTO weekly_winners (id, playlist_id, week_label, track, artist, submitted_by, score, trophy, art_url, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    winner_id, playlist_id, f"{week_label} · {playlist_name}",
                    winner_song["title"], winner_song["artist"], f"@{username}",
                    winner_avg, "🏆", winner_song["art_url"], now_iso
                ))
                print(f"[WINNER] [{playlist_name}] Ganador guardado: {winner_song['title']} ({winner_avg})")
                
            conn.commit()
            
        print("[SWEEP] Cierre semanal completado. Ganadores registrados, canciones y playlists intactas.")
        return True
    except Exception as e:
        print(f"[ERROR] Error durante el cierre semanal: {e}")
        return False
