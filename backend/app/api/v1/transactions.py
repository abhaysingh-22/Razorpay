# pyrefly: ignore [missing-import]
from fastapi import APIRouter, HTTPException
import random

# pyrefly: ignore [missing-import]
from faker import Faker
from app.db.client import supabase

fake = Faker()
FAILURE_REASONS = [
    "insufficient_funds",
    "expired_card",
    "bank_timeout",
    "fraud_flag",
]
REASON_WEIGHTS = [0.45, 0.30, 0.20, 0.05]

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/generate")
def generate_transactions_endpoint(count: int = 10):
    """Generates and injects synthetic failed transactions into the database."""
    transactions = []
    for _ in range(count):
        reason = random.choices(FAILURE_REASONS, weights=REASON_WEIGHTS)[0]
        transactions.append(
            {
                "razorpay_payment_id": f"pay_{fake.uuid4()[:14]}",
                "amount": round(random.uniform(299, 4999), 2),
                "status": "failed",
                "failure_reason": reason,
                "customer_id": f"cust_{fake.uuid4()[:10]}",
            }
        )
    result = supabase.table("transactions").insert(transactions).execute()
    return {
        "status": "success",
        "inserted": len(result.data or []),
        "transactions": result.data or [],
    }


@router.post("/reset")
@router.get("/reset")
def reset_database_endpoint():
    """Wipes all transactions, recovery attempts, and batch summaries to start fresh."""
    try:
        supabase.table("recovery_attempts").delete().neq(
            "id", "00000000-0000-0000-0000-000000000000"
        ).execute()
        supabase.table("transactions").delete().neq(
            "id", "00000000-0000-0000-0000-000000000000"
        ).execute()
        supabase.table("batch_summaries").delete().neq(
            "id", "00000000-0000-0000-0000-000000000000"
        ).execute()
        return {
            "status": "success",
            "message": "Database wiped clean. Ready for fresh test runs.",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to reset database: {str(e)}"
        )


@router.get("/")
def list_transactions(status: str | None = None, limit: int = 100):
    query = (
        supabase.table("transactions")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
    )
    if status:
        query = query.eq("status", status)
    result = query.execute()
    return result.data


@router.get("/{transaction_id}")
def get_transaction(transaction_id: str):
    result = (
        supabase.table("transactions").select("*").eq("id", transaction_id).execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Transaction not found")

    attempts = (
        supabase.table("recovery_attempts")
        .select("*")
        .eq("transaction_id", transaction_id)
        .order("attempt_number")
        .execute()
    )

    return {
        "transaction": result.data[0],
        "recovery_attempts": attempts.data,
    }
