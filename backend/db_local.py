import sqlite3
import os
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

# Ubicación de la base de datos persistente
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "dorisk.db")
AVATARS_DIR = os.path.join(DATA_DIR, "avatars")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(AVATARS_DIR, exist_ok=True)

def get_db():
    """Retorna una conexión a SQLite optimizada para concurrencia (WAL mode)"""
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db():
    """Crea todas las tablas necesarias si no existen"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Tabla de Usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            avatar_url TEXT,
            is_approved INTEGER DEFAULT 1,
            is_admin INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        );
        """)
        
        # 2. Tabla de Playlists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            youtube_id TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL
        );
        """)
        
        # 3. Permisos de Usuarios por Playlist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist_users (
            playlist_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            PRIMARY KEY (playlist_id, user_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """)
        
        # 4. Canciones
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            playlist_id TEXT NOT NULL,
            original_url TEXT NOT NULL,
            source_platform TEXT DEFAULT 'youtube',
            artist TEXT,
            title TEXT,
            youtube_video_id TEXT,
            art_url TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE
        );
        """)
        
        # 5. Votaciones
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            song_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (song_id, user_id),
            FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """)
        
        # 6. Ganadores Históricos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_winners (
            id TEXT PRIMARY KEY,
            playlist_id TEXT,
            week_label TEXT NOT NULL,
            track TEXT NOT NULL,
            artist TEXT NOT NULL,
            submitted_by TEXT NOT NULL,
            score REAL NOT NULL,
            trophy TEXT NOT NULL,
            art_url TEXT,
            created_at TEXT NOT NULL
        );
        """)
        
        conn.commit()
        
        # Auto-poblar datos migrados si la base de datos esta vacia
        try:
            cursor.execute("SELECT count(*) FROM users")
            user_count = cursor.fetchone()[0]
            if user_count == 0:
                seed_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "initial_seed.sql")
                if os.path.exists(seed_file):
                    with open(seed_file, "r", encoding="utf-8") as f:
                        cursor.executescript(f.read())
                    conn.commit()
                    print("[SEED] Base de datos auto-poblada con exito desde initial_seed.sql")
        except Exception as e:
            print(f"[WARN] No se pudo auto-cargar initial_seed.sql: {e}")
        
        print("[OK] Base de datos local SQLite lista en:", DB_PATH)

# Inicializar automaticamente al importar
init_db()
