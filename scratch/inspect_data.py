import sqlite3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from datetime import datetime, timezone, timedelta

conn = sqlite3.connect('data/dorisk.db')
conn.row_factory = sqlite3.Row

print("=== SONGS IN DATABASE ===")
songs = conn.execute("SELECT id, title, artist, playlist_id, created_at FROM songs ORDER BY created_at DESC").fetchall()
for s in songs:
    print(f"  {s['title']} by {s['artist']} | playlist: {s['playlist_id'][:8]}... | created: {s['created_at']}")

print(f"\nTotal songs: {len(songs)}")

# Check the 7-day filter
one_week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
recent = conn.execute("SELECT count(*) FROM songs WHERE created_at >= ?", (one_week_ago,)).fetchone()[0]
print(f"Songs in last 7 days: {recent}")
print(f"7-day cutoff: {one_week_ago}")

if songs:
    newest = songs[0]['created_at']
    oldest = songs[-1]['created_at']
    print(f"Newest song: {newest}")
    print(f"Oldest song: {oldest}")

print("\n=== WEEKLY WINNERS ===")
winners = conn.execute("SELECT * FROM weekly_winners ORDER BY created_at DESC").fetchall()
for w in winners:
    print(f"  {w['track']} by {w['artist']} | week: {w['week_label']} | trophy: {w['trophy']}")

print(f"\nTotal winners: {len(winners)}")
