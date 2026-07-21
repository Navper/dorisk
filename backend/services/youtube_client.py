import os
import json
import urllib.request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from backend.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, YOUTUBE_PLAYLIST_ID

TOKEN_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".youtube_tokens.json")
SCOPES = ["https://www.googleapis.com/auth/youtube"]

# Permitir HTTP local para el flujo OAuth de desarrollo
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def get_flow():
    redirect_uri = "http://localhost:8000/api/auth/youtube/callback"
    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri]
        }
    }
    return Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

def get_credentials() -> Credentials:
    """Carga y refresca las credenciales almacenadas si existen"""
    if not os.path.exists(TOKEN_PATH):
        return None
    
    try:
        with open(TOKEN_PATH, "r") as f:
            info = json.load(f)
        
        credentials = Credentials.from_authorized_user_info(info, SCOPES)
        
        # Refrescar el token si ha expirado
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            # Guardar el token refrescado
            save_credentials(credentials)
            
        return credentials
    except Exception as e:
        print(f"❌ Error al cargar credenciales de YouTube: {e}")
        return None

def save_credentials(credentials: Credentials):
    try:
        info = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }
        with open(TOKEN_PATH, "w") as f:
            json.dump(info, f)
    except Exception as e:
        print(f"❌ Error al guardar credenciales de YouTube: {e}")

def is_youtube_authorized() -> bool:
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return False
    creds = get_credentials()
    return creds is not None

def get_video_details(video_id: str) -> dict:
    """
    Obtiene el título crudo de un video de YouTube para pasárselo a Gemini.
    """
    creds = get_credentials()
    if not creds:
        # Fallback de prueba
        return {"raw_title": f"Video de YouTube {video_id}"}
        
    try:
        youtube = build("youtube", "v3", credentials=creds)
        res = youtube.videos().list(part="snippet", id=video_id).execute()
        items = res.get("items", [])
        if items:
            title = items[0]["snippet"]["title"]
            return {"raw_title": title}
        return {"raw_title": "Video Desconocido"}
    except Exception as e:
        print(f"❌ Error al obtener detalles del video {video_id}: {e}")
        return {"raw_title": f"Video {video_id}"}

def get_playlist_details(playlist_id: str) -> str:
    """
    Obtiene el nombre de una playlist de YouTube (intenta oEmbed público primero, luego API oficial).
    """
    # 1. Intentar via oEmbed (público, no requiere credenciales)
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/playlist?list={playlist_id}&format=json"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and "title" in data:
                return data["title"]
    except Exception as oe_err:
        print(f"⚠️ oEmbed falló al obtener playlist {playlist_id}: {oe_err}")

    # 2. Fallback a la API de YouTube oficial si está autorizada
    creds = get_credentials()
    if not creds:
        return "Nueva Playlist"
        
    try:
        youtube = build("youtube", "v3", credentials=creds)
        res = youtube.playlists().list(part="snippet", id=playlist_id).execute()
        items = res.get("items", [])
        if items:
            return items[0]["snippet"]["title"]
        return "Playlist Desconocida"
    except Exception as e:
        print(f"❌ Error al obtener detalles de la playlist {playlist_id} via API: {e}")
        return "Error al cargar nombre"

def add_video_to_playlist(video_id: str, youtube_playlist_id: str) -> bool:
    """
    Añade el ID de video directamente a la playlist específica de YouTube.
    """
    creds = get_credentials()
    if not creds:
        print("⚠️ [YouTube] No autorizado. Omitiendo inserción real.")
        return True
        
    try:
        youtube = build("youtube", "v3", credentials=creds)
        body = {
            "snippet": {
                "playlistId": youtube_playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
        youtube.playlistItems().insert(part="snippet", body=body).execute()
        return True
    except Exception as e:
        print(f"❌ Error al insertar video en la playlist de YouTube: {e}")
        return False


def remove_all_videos_from_playlist(youtube_playlist_id: str):
    """
    Vacía la playlist de YouTube para el cierre de semana.
    """
    if not youtube_playlist_id:
        return
    creds = get_credentials()
    if not creds:
        return
    try:
        youtube = build("youtube", "v3", credentials=creds)
        
        # Obtener los elementos de la playlist
        # Nota: recuperamos de 50 en 50 para evitar superar límites básicos
        items = []
        next_page_token = None
        
        while True:
            res = youtube.playlistItems().list(
                playlistId=youtube_playlist_id,
                part="id",
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            items.extend(res.get("items", []))
            next_page_token = res.get("nextPageToken")
            if not next_page_token:
                break
                
        # Eliminar cada uno
        for item in items:
            youtube.playlistItems().delete(id=item["id"]).execute()
            
        print(f"🟢 Playlist de YouTube ({youtube_playlist_id}) vaciada con éxito.")
    except Exception as e:
        print(f"❌ Error al vaciar la playlist de YouTube ({youtube_playlist_id}): {e}")
