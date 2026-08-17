import sqlite3

conn = sqlite3.connect('data/dorisk.db')
conn.row_factory = sqlite3.Row

print("========================================")
print("  ESTADO DE LA BASE DE DATOS LOCAL (data/dorisk.db)")
print("========================================")

tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()]
for t in tables:
    count = conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    print(f"[-] Tabla '{t}': {count} filas")

print("\n--- USUARIOS GUARDADOS ---")
for u in conn.execute("SELECT username, email, is_admin, is_approved FROM users").fetchall():
    print(f"  * {u['username']} | {u['email']} | Admin: {u['is_admin']}")

print("\n--- PLAYLISTS GUARDADAS ---")
for p in conn.execute("SELECT name, id FROM playlists").fetchall():
    songs_in_pl = conn.execute("SELECT count(*) FROM songs WHERE playlist_id = ?", (p['id'],)).fetchone()[0]
    print(f"  * {p['name']} ({songs_in_pl} canciones)")

print("========================================")
