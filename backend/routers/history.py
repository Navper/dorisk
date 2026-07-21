from fastapi import APIRouter, HTTPException
from backend.db import supabase_client

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("")
async def get_weekly_winners_history():
    if not supabase_client:
        # Fallback local para demo
        return [
            {
                "id": "h1",
                "week_label": "SEMANA 27 (01 JUL - 07 JUL)",
                "track": "Bohemian Rhapsody",
                "artist": "Queen",
                "submitted_by": "@Carlos",
                "score": 6.9,
                "trophy": "🏆",
                "art_url": "https://api.dicebear.com/7.x/pixel-art/svg?seed=bohemian"
            },
            {
                "id": "h2",
                "week_label": "SEMANA 26 (24 JUN - 30 JUN)",
                "track": "Blinding Lights",
                "artist": "The Weeknd",
                "submitted_by": "@Ana",
                "score": 6.5,
                "trophy": "🥈",
                "art_url": "https://api.dicebear.com/7.x/pixel-art/svg?seed=blinding"
            }
        ]
        
    try:
        res = supabase_client.table("weekly_winners") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()
        return res.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el histórico: {str(e)}")
