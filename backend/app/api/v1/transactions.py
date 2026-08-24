from fastapi import APIRouter, HTTPException
from app.db.client import supabase

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/")
def list_transactions(status: str | None = None, limit: int = 100):
    query = supabase.table("transactions").select("*").order("created_at", desc=True).limit(limit)
    if status:
        query = query.eq("status", status)
    result = query.execute()
    return result.data

@router.get("/{transaction_id}")
def get_transaction(transaction_id: str):
    result = supabase.table("transactions").select("*").eq("id", transaction_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Transaction not found")

    attempts = supabase.table("recovery_attempts") \
        .select("*") \
        .eq("transaction_id", transaction_id) \
        .order("attempt_number") \
        .execute()

    return {
        "transaction": result.data[0],
        "recovery_attempts": attempts.data,
    }