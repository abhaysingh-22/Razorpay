from fastapi import APIRouter
from app.db.client import supabase

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/summary")
def get_latest_summary():
    """Returns the most recent batch summary — the dashboard headline numbers."""
    result = supabase.table("batch_summaries") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()
    return result.data[0] if result.data else None

@router.get("/history")
def get_summary_history(limit: int = 20):
    """All batch summaries over time — this powers your 'recovery maturing over runs' chart."""
    result = supabase.table("batch_summaries") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute()
    return result.data