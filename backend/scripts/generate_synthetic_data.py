# pyrefly: ignore [missing-import]
from faker import Faker
import random
from app.db.client import supabase

fake = Faker()

FAILURE_REASONS = [
    "insufficient_funds",
    "expired_card",
    "bank_timeout",
    "fraud_flag",
]

# realistic distribution — insufficient funds most common, fraud rare
REASON_WEIGHTS = [0.45, 0.30, 0.20, 0.05]

def generate_transactions(n=80):
    transactions = []
    for _ in range(n):
        reason = random.choices(FAILURE_REASONS, weights=REASON_WEIGHTS)[0]
        transactions.append({
            "razorpay_payment_id": f"pay_{fake.uuid4()[:14]}",
            "amount": round(random.uniform(199, 4999), 2),
            "status": "failed",
            "failure_reason": reason,
            "customer_id": f"cust_{fake.uuid4()[:10]}",
        })
    return transactions

def seed():
    data = generate_transactions(80)
    result = supabase.table("transactions").insert(data).execute()
    print(f"Inserted {len(result.data)} synthetic transactions")

if __name__ == "__main__":
    seed()