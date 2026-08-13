import uuid
from datetime import datetime, timezone
from backend.services.link_parser import parse_link
from backend.services.gemini_client import clean_song_title
from backend.services import youtube_client
from backend.db_local import get_db

def process_song_submission(url: str, user_id: str, playlist_id: str) -> dict:
    """
    Orquesta el flujo de envío exclusivo para YouTube (YouTube Music):
    1. Parsea el enlace.
    2. Valida que sea de YouTube.
    3. Obtiene metadatos de YouTube y los limpia con Gemini.
    4. Añade a la playlist de YouTube.
    5. Guarda el registro en la base de datos local SQLite.
    """
    parsed = parse_link(url)
    platform = parsed["platform"]
    item_id = parsed["id"]
    
    if platform != "youtube" or not item_id:
        raise ValueError("El enlace proporcionado debe ser un link válido de YouTube o YouTube Music.")
        
    youtube_video_id = item_id
    art_url = f"https://img.youtube.com/vi/{item_id}/hqdefault.jpg"
    
    # 1. Obtener el título del video de YouTube
    yt_details = youtube_client.get_video_details(item_id)
    raw_title = yt_details["raw_title"]
    
    # 2. Limpiar con Gemini para extraer {artista, canción}
    cleaned = clean_song_title(raw_title)
    artist = cleaned["artist"]
    song_title = cleaned["song"]
    
    # 3. Obtener el youtube_id real de la playlist desde SQLite
    target_youtube_playlist_id = None
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT youtube_id FROM playlists WHERE id = ?", (playlist_id,))
        row = cursor.fetchone()
        if row and row["youtube_id"]:
            target_youtube_playlist_id = row["youtube_id"]
            
    # 4. Añadir el video a la playlist de YouTube si existe
    if target_youtube_playlist_id:
        try:
            youtube_client.add_video_to_playlist(item_id, target_youtube_playlist_id)
        except Exception as yt_err:
            print(f"⚠️ Error añadiendo a YouTube: {yt_err}")
        
    # 5. Guardar en base de datos local SQLite
    song_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO songs (id, user_id, playlist_id, original_url, source_platform, artist, title, youtube_video_id, art_url, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (song_id, user_id, playlist_id, url, "youtube", artist, song_title, youtube_video_id, art_url, now_iso))
        conn.commit()
        
        cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        return dict(cursor.fetchone())
