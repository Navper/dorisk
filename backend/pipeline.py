from backend.services.link_parser import parse_link
from backend.services.gemini_client import clean_song_title
from backend.services import youtube_client
from backend.db import admin_client

def process_song_submission(url: str, user_id: str, playlist_id: str) -> dict:
    """
    Orquesta el flujo de envío exclusivo para YouTube (YouTube Music):
    1. Parsea el enlace.
    2. Valida que sea de YouTube.
    3. Obtiene metadatos de YouTube y los limpia con Gemini.
    4. Añade a la playlist de YouTube.
    5. Guarda el registro en Supabase.
    """
    parsed = parse_link(url)
    platform = parsed["platform"]
    item_id = parsed["id"]
    
    if platform != "youtube" or not item_id:
        raise ValueError("El enlace proporcionado debe ser un link válido de YouTube o YouTube Music.")
        
    artist = ""
    song_title = ""
    youtube_video_id = item_id
    art_url = f"https://img.youtube.com/vi/{item_id}/hqdefault.jpg" # Carátula nativa de YouTube en HQ!
    
    # 1. Obtener el título del video de YouTube
    yt_details = youtube_client.get_video_details(item_id)
    raw_title = yt_details["raw_title"]
    
    # 2. Limpiar con Gemini para extraer {artista, canción}
    cleaned = clean_song_title(raw_title)
    artist = cleaned["artist"]
    song_title = cleaned["song"]
    
    # 3. Obtener el youtube_id real de la playlist
    target_youtube_playlist_id = None
    if admin_client:
        pl_res = admin_client.table("playlists").select("youtube_id").eq("id", playlist_id).execute()
        if pl_res.data and pl_res.data[0].get("youtube_id"):
            target_youtube_playlist_id = pl_res.data[0]["youtube_id"]
            
    # 4. Añadir el video a la playlist de YouTube
    if target_youtube_playlist_id:
        youtube_client.add_video_to_playlist(item_id, target_youtube_playlist_id)
        
    # Guardar en base de datos
    song_record = {
        "user_id": user_id,
        "playlist_id": playlist_id,
        "original_url": url,
        "source_platform": "youtube",
        "artist": artist,
        "title": song_title,
        "spotify_track_id": None,
        "youtube_video_id": youtube_video_id,
        "art_url": art_url
    }
    
    if admin_client:
        try:
            res = admin_client.table("songs").insert(song_record).execute()
            if res.data:
                return res.data[0]
        except Exception as e:
            print(f"❌ Error al guardar la canción en Supabase: {e}")
            raise Exception("No se pudo guardar la canción en la base de datos.")
            
    # Fallback modo local/desarrollo
    song_record["id"] = "dev-song-id"
    song_record["created_at"] = "2026-07-09T00:00:00Z"
    return song_record
