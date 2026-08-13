from fastapi import APIRouter
from backend.db_local import get_db

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("")
async def get_weekly_winners_history():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM weekly_winners ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error cargando histórico de ganadores: {e}")
        return []
