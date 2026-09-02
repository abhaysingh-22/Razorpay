from fastapi import APIRouter
from app.services.recovery_service import run_batch_recovery
from app.db.client import supabase

router = APIRouter(prefix="/recovery", tags=["recovery"])

@router.post("/run")
def trigger_batch_recovery():
    """Runs the recovery flow for every transaction currently due (UI / manual trigger)."""
    result = run_batch_recovery()
    return result

@router.post("/cron-batch")
@router.get("/cron-batch")
def trigger_cron_recovery():
    """
    Automated Cron Endpoint for cron-job.org or scheduled tasks.
    Supports both POST and GET for simple webhook pinging every 15 minutes.
    """
    result = run_batch_recovery()
    return {
        "status": "success",
        "message": f"Processed {result['processed']} transactions in cron cycle",
        "data": result
    }

@router.get("/attempts")
def list_recovery_attempts(limit: int = 200):
    result = supabase.table("recovery_attempts") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute()
    return result.data