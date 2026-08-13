import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_local import init_db, get_db
from backend.auth_service import hash_password, verify_password, create_access_token, decode_access_token
from backend.weekly_sweep import run_weekly_sweep

def test_full_local_flow():
    print("[TEST] PROBANDO EL SISTEMA NATIVO LOCAL (SQLITE + JWT)...")
    
    # 1. Base de datos
    init_db()
    
    # 2. Test Auth Service
    pwd = "password123"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed), "Fallo verificación de contraseña"
    assert not verify_password("wrong", hashed), "Fallo protección contra contraseña errónea"
    
    token = create_access_token({"sub": "user-123", "username": "testuser", "email": "test@dorisk.com"})
    decoded = decode_access_token(token)
    assert decoded["sub"] == "user-123", "Fallo decodificación de token"
    print("[OK] Autenticación nativa y JWT funcionan correctamente.")
    
    # 3. Test Inserción de Playlist y Usuario
    with get_db() as conn:
        cursor = conn.cursor()
        u_id = str(uuid.uuid4())
        pl_id = str(uuid.uuid4())
        
        cursor.execute("INSERT OR REPLACE INTO users (id, email, username, password_hash, created_at) VALUES (?, ?, ?, ?, ?)",
                       (u_id, "admin@dorisk.com", "AdminTest", hashed, "2026-08-14T00:00:00Z"))
        cursor.execute("INSERT OR REPLACE INTO playlists (id, name, youtube_id, created_by, created_at) VALUES (?, ?, ?, ?, ?)",
                       (pl_id, "TEST PLAYLIST", "PL_TEST", u_id, "2026-08-14T00:00:00Z"))
        cursor.execute("INSERT OR REPLACE INTO playlist_users (playlist_id, user_id) VALUES (?, ?)",
                       (pl_id, u_id))
        
        s_id = str(uuid.uuid4())
        cursor.execute("INSERT OR REPLACE INTO songs (id, user_id, playlist_id, original_url, title, artist, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (s_id, u_id, pl_id, "https://youtube.com/watch?v=123", "Canción Test", "Artista Test", "2026-08-14T00:00:00Z"))
        
        cursor.execute("INSERT OR REPLACE INTO votes (song_id, user_id, score, created_at) VALUES (?, ?, ?, ?)",
                       (s_id, u_id, 7, "2026-08-14T00:00:00Z"))
        conn.commit()
        
    print("[OK] Inserciones en SQLite completadas.")
    
    # 4. Test Weekly Sweep
    success = run_weekly_sweep()
    assert success, "Fallo en sweep semanal"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weekly_winners WHERE playlist_id = ?", (pl_id,))
        winner = cursor.fetchone()
        assert winner is not None, "Ganador no fue guardado"
        print(f"[OK] Ganador semanal registrado con exito: {winner['track']} con puntuacion {winner['score']}")
        
    print("\n[SUCCESS] TODAS LAS PRUEBAS LOCALES PASARON AL 100%!")

if __name__ == "__main__":
    test_full_local_flow()
