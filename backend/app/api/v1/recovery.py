from fastapi import APIRouter
from app.services.recovery_service import run_batch_recovery
from app.db.client import supabase

router = APIRouter(prefix="/recovery", tags=["recovery"])

@router.post("/run")
def trigger_batch_recovery():
    """Runs the recovery flow for every transaction currently due."""
    result = run_batch_recovery()
    return result

@router.get("/attempts")
def list_recovery_attempts(limit: int = 200):
    result = supabase.table("recovery_attempts") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute()
    return result.data