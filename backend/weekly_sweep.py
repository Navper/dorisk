from datetime import datetime, timezone, timedelta
from backend.db import admin_client

def run_weekly_sweep():
    """
    Realiza el cierre semanal automático de Dorisk:
    1. Para CADA playlist, calcula el ganador de la semana.
    2. Lo registra en la tabla `weekly_winners`.
    3. Limpia las canciones y votos de la semana.
    """
    if not admin_client:
        print("⚠️ [Cierre Semanal] Supabase no está configurado. Operación omitida.")
        return False
        
    try:
        # Obtener todas las playlists activas
        pl_res = admin_client.table("playlists").select("id, name, youtube_id").execute()
        playlists = pl_res.data or []
        
        if not playlists:
            print("🟢 [Cierre Semanal] No hay playlists registradas.")
            return True
        
        today = datetime.now(timezone.utc)
        start_date = today - timedelta(days=7)
        week_label = f"SEMANA {start_date.strftime('%W')} ({start_date.strftime('%d %b').upper()} - {today.strftime('%d %b').upper()})"
        
        for pl in playlists:
            playlist_id = pl["id"]
            playlist_name = pl["name"]
            
            # Obtener canciones de esta playlist
            songs_res = admin_client.table("songs") \
                .select("*, profiles(username)") \
                .eq("playlist_id", playlist_id) \
                .execute()
            songs = songs_res.data or []
            
            if not songs:
                print(f"🟢 [Cierre Semanal] Playlist '{playlist_name}': sin canciones esta semana.")
                continue
                
            leaderboard = []
            
            song_ids = [s["id"] for s in songs]
            votes_res = admin_client.table("votes").select("song_id, score").in_("song_id", song_ids).execute()
            votes = votes_res.data or []
            
            votes_by_song = {sid: [] for sid in song_ids}
            for v in votes:
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
                
            leaderboard.sort(key=lambda x: (x["average"], x["votes_count"]), reverse=True)
            winner_entry = leaderboard[0]
            winner_song = winner_entry["song"]
            winner_avg = winner_entry["average"]
            
            # Contar ganadores anteriores de esta playlist para el trofeo
            history_count = admin_client.table("weekly_winners") \
                .select("id", count="exact") \
                .eq("playlist_id", playlist_id) \
                .execute()
            count = history_count.count or 0
            trophy = "🏆" if count == 0 else ("🥈" if count == 1 else "🥉")
            
            username = winner_song.get("profiles", {}).get("username", "Desconocido") if winner_song.get("profiles") else "Desconocido"
            
            winner_data = {
                "playlist_id": playlist_id,
                "week_label": f"{week_label} · {playlist_name}",
                "track": winner_song["title"],
                "artist": winner_song["artist"],
                "submitted_by": f"@{username}",
                "score": winner_avg,
                "trophy": trophy,
                "art_url": winner_song["art_url"]
            }
            
            # 1. Registrar ganador en la tabla `weekly_winners`
            admin_client.table("weekly_winners").insert(winner_data).execute()
            print(f"🏆 [{playlist_name}] Ganador: {winner_song['title']} de {winner_song['artist']} con {winner_avg}★")
            
            # 2. Eliminar la playlist finalizada de Dorisk (la playlist original en YouTube NUNCA se borra ni vacía)
            song_ids = [s["id"] for s in songs]
            if song_ids:
                admin_client.table("votes").delete().in_("song_id", song_ids).execute()
            admin_client.table("songs").delete().eq("playlist_id", playlist_id).execute()
            admin_client.table("playlist_users").delete().eq("playlist_id", playlist_id).execute()
            admin_client.table("playlists").delete().eq("id", playlist_id).execute()
            print(f"📦 [{playlist_name}] Season finalizada. Playlist archivada intacta en YouTube.")
            
        print("🧹 Cierre de temporada completado para todas las playlists.")
        return True
    except Exception as e:
        print(f"❌ Error durante el cierre semanal: {e}")
        return False

