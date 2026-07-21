import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from backend.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_PLAYLIST_ID

# Ruta del token de caché de Spotify
TOKEN_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".spotify_tokens.json")

def get_oauth_manager():
    # El callback de redirección configurado en el panel de desarrolladores de Spotify
    redirect_uri = "http://localhost:8000/api/auth/spotify/callback"
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=redirect_uri,
        scope="playlist-modify-public playlist-modify-private",
        cache_path=TOKEN_PATH,
        open_browser=False
    )

def is_spotify_authorized() -> bool:
    """Retorna True si hay credenciales y el token de caché existe y es válido"""
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return False
    
    oauth = get_oauth_manager()
    token_info = oauth.get_cached_token()
    return token_info is not None

def get_track_details(track_id: str) -> dict:
    """
    Obtiene los detalles del track directamente desde Spotify por su ID.
    """
    if not is_spotify_authorized():
        return {
            "artist": "Artista Spotify",
            "song": f"Canción ID {track_id}",
            "art_url": "https://api.dicebear.com/7.x/pixel-art/svg?seed=spotify"
        }
        
    try:
        sp = spotipy.Spotify(auth_manager=get_oauth_manager())
        track = sp.track(track_id)
        artist = track["artists"][0]["name"]
        song = track["name"]
        images = track.get("album", {}).get("images", [])
        art_url = images[0]["url"] if images else "https://api.dicebear.com/7.x/pixel-art/svg?seed=spotify"
        return {
            "artist": artist,
            "song": song,
            "art_url": art_url
        }
    except Exception as e:
        print(f"❌ Error al obtener detalles de track {track_id}: {e}")
        return {
            "artist": "Desconocido",
            "song": "Canción Spotify",
            "art_url": "https://api.dicebear.com/7.x/pixel-art/svg?seed=error"
        }

def add_track_to_playlist(track_id: str) -> bool:
    """
    Añade un track ID directamente a la playlist colectiva de Spotify.
    """
    if not is_spotify_authorized():
        print("⚠️ [Spotify] No autorizado. Omitiendo inserción real.")
        return True
        
    try:
        sp = spotipy.Spotify(auth_manager=get_oauth_manager())
        sp.playlist_add_items(SPOTIFY_PLAYLIST_ID, [track_id])
        return True
    except Exception as e:
        print(f"❌ Error al añadir track a la playlist de Spotify: {e}")
        return False


def remove_all_tracks_from_playlist():
    """
    Vacía la playlist de Spotify para el cierre de semana.
    """
    if not is_spotify_authorized():
        return
    try:
        sp = spotipy.Spotify(auth_manager=get_oauth_manager())
        # Obtener los tracks de la playlist
        results = sp.playlist_items(SPOTIFY_PLAYLIST_ID, fields="items(track(id))")
        tracks = [item["track"]["id"] for item in results.get("items", []) if item.get("track", {}).get("id")]
        
        if tracks:
            sp.playlist_remove_all_occurrences_of_items(SPOTIFY_PLAYLIST_ID, tracks)
            print("🟢 Playlist de Spotify vaciada con éxito.")
    except Exception as e:
        print(f"❌ Error al vaciar la playlist de Spotify: {e}")
