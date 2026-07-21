import re

def parse_link(url: str) -> dict:
    """
    Parsea una URL y determina si es de Spotify o YouTube, extrayendo el ID correspondiente.
    """
    url = url.strip()
    
    # Spotify Track: https://open.spotify.com/track/4PTG3Z6ehGkBFm6PuvY25D?si=...
    spotify_match = re.search(r"open\.spotify\.com/track/([a-zA-Z0-9]+)", url)
    if spotify_match:
        return {
            "platform": "spotify",
            "id": spotify_match.group(1)
        }
        
    # YouTube Video (incluye YouTube Music y enlaces móviles):
    youtube_match = re.search(
        r"(?:https?://)?(?:www\.|m\.|music\.)?(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})",
        url,
        re.IGNORECASE
    )
    if youtube_match:
        return {
            "platform": "youtube",
            "id": youtube_match.group(1)
        }
        
    return {
        "platform": "unknown",
        "id": None
    }
