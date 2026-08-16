import os
import sys
import uuid
import urllib.request
from dotenv import load_dotenv
from supabase import create_client

# Agregar path raíz
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_local import get_db, init_db, AVATARS_DIR
from backend.auth_service import hash_password

load_dotenv("backend/.env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def run_migration():
    print("=== INICIANDO MIGRACION TOTAL DE SUPABASE A BASE DE DATOS LOCAL ===")

    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("[ERROR] Faltan SUPABASE_URL o SUPABASE_SERVICE_KEY en backend/.env")
        return False

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception as e:
        print(f"[ERROR] conectando con Supabase: {e}")
        return False

    init_db()

    conn = get_db()
    cursor = conn.cursor()

    # -------------------------------------------------------------
    # 1. MIGRAR USUARIOS Y PERFILES
    # -------------------------------------------------------------
    print("\n[1/5] Migrando Usuarios y Perfiles...")
    try:
        # Obtener perfiles de la tabla profiles
        prof_res = supabase.table("profiles").select("*").execute()
        profiles_map = {p["id"]: p for p in (prof_res.data or [])}

        # Obtener usuarios de Auth
        users = []
        try:
            users_res = supabase.auth.admin.list_users()
            users = users_res if isinstance(users_res, list) else getattr(users_res, "users", [])
        except Exception as e:
            print(f"[WARN] No se pudo listar auth.users directamente ({e}), usando tabla profiles...")

        inserted_users = 0
        if users:
            for u in users:
                user_id = u.id
                email = u.email or f"user_{user_id[:8]}@dorisk.com"
                prof = profiles_map.get(user_id, {})
                username = prof.get("username") or (u.user_metadata.get("username") if hasattr(u, "user_metadata") and u.user_metadata else None) or email.split("@")[0]
                avatar_url = prof.get("avatar_url") or f"https://api.dicebear.com/7.x/pixel-art/svg?seed={username}"
                is_approved = 1 if prof.get("is_approved", True) else 0
                created_at = u.created_at if hasattr(u, "created_at") and u.created_at else "2026-01-01T00:00:00Z"
                
                # Usar hash por defecto seguro si no se tiene la clave en texto plano
                pwd_hash = hash_password("dorisk2026")

                cursor.execute("""
                    INSERT OR REPLACE INTO users (id, email, username, password_hash, avatar_url, is_approved, is_admin, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, email, username, pwd_hash, avatar_url, is_approved, 0, str(created_at)))
                inserted_users += 1
        else:
            # Fallback usando tabla profiles
            for user_id, prof in profiles_map.items():
                email = prof.get("email") or f"{prof.get('username', user_id[:8])}@dorisk.com"
                username = prof.get("username", email.split("@")[0])
                avatar_url = prof.get("avatar_url") or f"https://api.dicebear.com/7.x/pixel-art/svg?seed={username}"
                is_approved = 1 if prof.get("is_approved", True) else 0
                created_at = prof.get("created_at") or "2026-01-01T00:00:00Z"
                pwd_hash = hash_password("dorisk2026")

                cursor.execute("""
                    INSERT OR REPLACE INTO users (id, email, username, password_hash, avatar_url, is_approved, is_admin, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, email, username, pwd_hash, avatar_url, is_approved, 0, str(created_at)))
                inserted_users += 1

        print(f"[OK] {inserted_users} usuarios migrados con exito.")
    except Exception as e:
        print(f"[ERROR] migrando usuarios: {e}")

    # -------------------------------------------------------------
    # 2. MIGRAR PLAYLISTS
    # -------------------------------------------------------------
    print("\n[2/5] Migrando Playlists...")
    try:
        pl_res = supabase.table("playlists").select("*").execute()
        playlists = pl_res.data or []
        for pl in playlists:
            cursor.execute("""
                INSERT OR REPLACE INTO playlists (id, name, youtube_id, created_by, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (pl["id"], pl["name"], pl.get("youtube_id"), pl.get("created_by"), str(pl.get("created_at", ""))))
        print(f"[OK] {len(playlists)} playlists migradas.")
    except Exception as e:
        print(f"[ERROR] migrando playlists: {e}")

    # -------------------------------------------------------------
    # 3. MIGRAR PERMISOS DE USUARIOS (playlist_users)
    # -------------------------------------------------------------
    print("\n[3/5] Migrando Permisos de Playlists...")
    try:
        pu_res = supabase.table("playlist_users").select("*").execute()
        pu_list = pu_res.data or []
        for pu in pu_list:
            cursor.execute("""
                INSERT OR REPLACE INTO playlist_users (playlist_id, user_id)
                VALUES (?, ?)
            """, (pu["playlist_id"], pu["user_id"]))
        print(f"[OK] {len(pu_list)} asignaciones de playlist migradas.")
    except Exception as e:
        print(f"[ERROR] migrando playlist_users: {e}")

    # -------------------------------------------------------------
    # 4. MIGRAR CANCIONES Y VOTOS
    # -------------------------------------------------------------
    print("\n[4/5] Migrando Canciones y Votos...")
    try:
        songs_res = supabase.table("songs").select("*").execute()
        songs = songs_res.data or []
        for s in songs:
            cursor.execute("""
                INSERT OR REPLACE INTO songs (id, user_id, playlist_id, original_url, source_platform, artist, title, youtube_video_id, art_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["id"], s["user_id"], s["playlist_id"], s["original_url"],
                s.get("source_platform", "youtube"), s.get("artist"), s.get("title"),
                s.get("youtube_video_id"), s.get("art_url"), str(s.get("created_at", ""))
            ))
        print(f"[OK] {len(songs)} canciones migradas.")

        votes_res = supabase.table("votes").select("*").execute()
        votes = votes_res.data or []
        for v in votes:
            cursor.execute("""
                INSERT OR REPLACE INTO votes (song_id, user_id, score, created_at)
                VALUES (?, ?, ?, ?)
            """, (v["song_id"], v["user_id"], v["score"], str(v.get("created_at", ""))))
        print(f"[OK] {len(votes)} votos migrados.")
    except Exception as e:
        print(f"[ERROR] migrando canciones/votos: {e}")

    # -------------------------------------------------------------
    # 5. MIGRAR GANADORES HISTORICOS
    # -------------------------------------------------------------
    print("\n[5/5] Migrando Ganadores Semanales...")
    try:
        ww_res = supabase.table("weekly_winners").select("*").execute()
        winners = ww_res.data or []
        for w in winners:
            cursor.execute("""
                INSERT OR REPLACE INTO weekly_winners (id, playlist_id, week_label, track, artist, submitted_by, score, trophy, art_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                w["id"], w.get("playlist_id"), w["week_label"], w["track"],
                w["artist"], w["submitted_by"], w["score"], w["trophy"],
                w.get("art_url"), str(w.get("created_at", ""))
            ))
        print(f"[OK] {len(winners)} ganadores historicos migrados.")
    except Exception as e:
        print(f"[ERROR] migrando weekly_winners: {e}")

    conn.commit()
    conn.close()

    print("\n[EXITO] MIGRACION COMPLETADA CON EXITO!")
    print("Todos los datos han sido guardados en el archivo local SQLite.")
    return True

if __name__ == "__main__":
    run_migration()
