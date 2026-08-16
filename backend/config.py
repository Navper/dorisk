import os
from dotenv import load_dotenv

# Cargar variables del entorno desde el archivo .env si existe
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")
load_dotenv(env_path)

DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

JWT_SECRET = os.getenv("JWT_SECRET", "dorisk-super-secret-key-truenas-2026-production")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "navpercris@gmail.com")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID", "7cqzYeMb9k7XYgX0SthiyC")

YOUTUBE_PLAYLIST_ID = os.getenv("YOUTUBE_PLAYLIST_ID", "PLWKiSrhIgZYI")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

# Validar configuraciones críticas en el arranque
def validate_config():
    missing = []
    if not JWT_SECRET:
        missing.append("JWT_SECRET")
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    
    if missing:
        print(f"[WARNING] Faltan variables de entorno criticas: {', '.join(missing)}")
        print("Asegurate de configurar las variables de entorno en el panel.")
