from fastapi import APIRouter
from backend.db import supabase_client

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("")
async def get_weekly_winners_history():
    if not supabase_client:
        return []
        
    try:
        res = supabase_client.table("weekly_winners") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()
        return res.data or []
    except Exception as e:
        return []
