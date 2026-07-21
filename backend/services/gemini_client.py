import json
from google import genai
from google.genai import types
from backend.config import GEMINI_API_KEY

def clean_song_title(raw_title: str) -> dict:
    """
    Recibe un título sucio de una canción (por ejemplo, el título de un vídeo de YouTube
    o metadatos sin formatear) y devuelve un diccionario con {"artist": "...", "song": "..."}
    limpio gracias a Gemini 2.5 Flash.
    """
    if not GEMINI_API_KEY:
        print("⚠️ [Gemini] GEMINI_API_KEY no configurada. Usando fallback básico.")
        # Fallback local simple
        if " - " in raw_title:
            parts = raw_title.split(" - ", 1)
            return {"artist": parts[0].strip(), "song": parts[1].split("(")[0].split("[")[0].strip()}
        return {"artist": "Artista Desconocido", "song": raw_title}
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
        Actúa como un catálogo musical de alta precisión.
        Analiza este título de canción o metadatos de video: "{raw_title}"
        Limpia cualquier texto basura (como "Official Video", "HD", "1080p", "Video Oficial", "Lyrics", "Audio Latente", etc.).
        Identifica el artista principal (y colaboradores principales si los hay) y el título real de la canción.
        
        Devuelve estrictamente un objeto JSON con este formato exacto:
        {{
            "artist": "Nombre del artista",
            "song": "Título limpio de la canción"
        }}
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        data = json.loads(response.text)
        return {
            "artist": data.get("artist", "Artista Desconocido").strip(),
            "song": data.get("song", raw_title).strip()
        }
    except Exception as e:
        print(f"Error al invocar la API de Gemini: {e}")
        # Fallback de emergencia
        if " - " in raw_title:
            parts = raw_title.split(" - ", 1)
            return {"artist": parts[0].strip(), "song": parts[1].strip()}
        return {"artist": "Desconocido", "song": raw_title}
