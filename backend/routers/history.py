from fastapi import APIRouter, HTTPException
from backend.db import supabase_client
from backend.config import DEV_MODE

router = APIRouter(prefix="/api/history", tags=["history"])

SIMULATED_WINNERS = [
    {
        "id": "h1",
        "week_label": "SEMANA 29 · TECHNO/ELECTRO",
        "track": "Strobe",
        "artist": "deadmau5",
        "submitted_by": "@capoeira",
        "score": 6.9,
        "trophy": "🏆"
    },
    {
        "id": "h2",
        "week_label": "SEMANA 28 · METAL",
        "track": "Master of Puppets",
        "artist": "Metallica",
        "submitted_by": "@alex",
        "score": 6.7,
        "trophy": "🏆"
    },
    {
        "id": "h3",
        "week_label": "SEMANA 27 · CULTURAS DEL MUNDO",
        "track": "Chan Chan",
        "artist": "Buena Vista Social Club",
        "submitted_by": "@mariana",
        "score": 6.8,
        "trophy": "🏆"
    },
    {
        "id": "h4",
        "week_label": "SEMANA 26 · TECHNO/ELECTRO",
        "track": "Around the World",
        "artist": "Daft Punk",
        "submitted_by": "@Elena",
        "score": 6.5,
        "trophy": "🥈"
    }
]

@router.get("")
async def get_weekly_winners_history():
    if not supabase_client:
        return SIMULATED_WINNERS
        
    try:
        res = supabase_client.table("weekly_winners") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()
            
        if res.data and len(res.data) > 0:
            return res.data
            
        # En produccion (DEV_MODE=False), devolver lista vacia si no hay ganadores en BD.
        # Solo mostrar simulacion si DEV_MODE es True (Local).
        if DEV_MODE:
            return SIMULATED_WINNERS
            
        return []
    except Exception as e:
        if DEV_MODE:
            return SIMULATED_WINNERS
        return []
