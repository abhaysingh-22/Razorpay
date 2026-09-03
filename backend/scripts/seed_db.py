"""
Database Seeding CLI Tool for Razorpay RecoverAI.
Populates the Supabase database with realistic mock payment failures.

Usage:
    python -m scripts.seed_db --count 30 --wipe
"""

import argparse
import random
import sys

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

# Realistic distribution in Indian Fintech:
# 45% Insufficient Funds, 30% Expired Card, 20% Bank Timeout, 5% Fraud Flag
REASON_WEIGHTS = [0.45, 0.30, 0.20, 0.05]


def wipe_database() -> None:
    """Wipes all recovery attempts, transactions, and batch summaries."""
    print("🧹 Wiping existing database records...")
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
        print("✅ Database wiped clean.")
    except Exception as e:
        print(f"❌ Failed to wipe database: {e}", file=sys.stderr)
        raise


def generate_mock_transactions(count: int = 30) -> list[dict]:
    """Generates synthetic failed transactions with realistic Indian pricing tiers."""
    transactions = []
    for _ in range(count):
        reason = random.choices(FAILURE_REASONS, weights=REASON_WEIGHTS)[0]
        # Include high-ticket items occasionally for HITL demo
        amount = (
            round(random.uniform(11000, 25000), 2)
            if (reason == "fraud_flag" or random.random() < 0.1)
            else round(random.uniform(299, 4999), 2)
        )

        transactions.append(
            {
                "razorpay_payment_id": f"pay_{fake.uuid4()[:14]}",
                "amount": amount,
                "status": "failed",
                "failure_reason": reason,
                "customer_id": f"cust_{fake.uuid4()[:10]}",
            }
        )
    return transactions


def seed(count: int = 30, wipe: bool = False) -> None:
    """Seeds the Supabase database with mock transactions in batches."""
    if wipe:
        wipe_database()

    print(f"🌱 Generating and inserting {count} synthetic transactions...")
    data = generate_mock_transactions(count)

    # Insert in chunks of 50 to avoid payload size limits
    chunk_size = 50
    inserted_count = 0
    for i in range(0, len(data), chunk_size):
        chunk = data[i : i + chunk_size]
        res = supabase.table("transactions").insert(chunk).execute()
        inserted_count += len(res.data or [])

    print(f"✅ Successfully seeded {inserted_count} transactions into Supabase!")


def main():
    parser = argparse.ArgumentParser(
        description="Seed Supabase database with synthetic failed transactions."
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=30,
        help="Number of transactions to generate (default: 30)",
    )
    parser.add_argument(
        "--wipe", "-w", action="store_true", help="Wipe existing data before seeding"
    )
    args = parser.parse_args()

    seed(count=args.count, wipe=args.wipe)


if __name__ == "__main__":
    main()
