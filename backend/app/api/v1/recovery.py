# pyrefly: ignore [missing-import]
from fastapi import APIRouter, HTTPException

# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from app.services.recovery_service import run_batch_recovery, resolve_human_review
from app.db.client import supabase

router = APIRouter(prefix="/recovery", tags=["recovery"])


class ResolveReviewRequest(BaseModel):
    decision: str  # "approve" or "reject"
    notes: str | None = None


@router.post("/run")
def trigger_batch_recovery():
    """Runs the recovery flow for every transaction currently due (UI / manual trigger)."""
    result = run_batch_recovery()
    return result


# @router.post("/cron-batch")
# @router.get("/cron-batch")
# def trigger_cron_recovery():
#     """
#     Automated Cron Endpoint for cron-job.org or scheduled tasks.
#     Supports both POST and GET for simple webhook pinging every 15 minutes.
#     """
#     result = run_batch_recovery()
#     return {
#         "status": "success",
#         "message": f"Processed {result['processed']} transactions in cron cycle",
#         "data": result
#     }


@router.get("/review-queue")
def get_pending_review_queue():
    """Fetches transactions flagged for Human-in-the-Loop review."""
    result = (
        supabase.table("transactions")
        .select("*")
        .eq("status", "pending_human_review")
        .order("created_at", desc=True)
        .execute()
    )
    return result.data or []


@router.post("/review-queue/{transaction_id}/resolve")
def resolve_review_endpoint(transaction_id: str, payload: ResolveReviewRequest):
    """Submits human verdict ('approve' or 'reject') for a flagged payment."""
    if payload.decision not in ("approve", "reject"):
        raise HTTPException(
            status_code=400, detail="Decision must be 'approve' or 'reject'"
        )
    try:
        res = resolve_human_review(transaction_id, payload.decision, payload.notes)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/attempts")
def list_recovery_attempts(limit: int = 200):
    result = (
        supabase.table("recovery_attempts")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data
