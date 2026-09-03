"""
Synthetic Transaction Generator Module & CLI Tool.
Generates realistic payment failure payloads for testing and benchmarks.

Usage:
    python -m scripts.generate_synthetic_data --count 20 --json
"""

import argparse
import json
import random
from typing import List, Dict, Any
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


def generate_transactions(count: int = 50) -> List[Dict[str, Any]]:
    """
    Generates a list of synthetic failed payment payloads.
    
    Args:
        count: Number of transactions to create.
        
    Returns:
        List of transaction dictionaries.
    """
    transactions = []
    for _ in range(count):
        reason = random.choices(FAILURE_REASONS, weights=REASON_WEIGHTS)[0]
        amount = round(random.uniform(10500, 24000), 2) if (reason == "fraud_flag" or random.random() < 0.1) else round(random.uniform(299, 4999), 2)
        transactions.append({
            "razorpay_payment_id": f"pay_{fake.uuid4()[:14]}",
            "amount": amount,
            "status": "failed",
            "failure_reason": reason,
            "customer_id": f"cust_{fake.uuid4()[:10]}",
        })
    return transactions


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic payment failure dataset.")
    parser.add_argument("--count", "-n", type=int, default=20, help="Number of records to generate (default: 20)")
    parser.add_argument("--insert", "-i", action="store_true", help="Directly insert generated records into Supabase")
    parser.add_argument("--json", "-j", action="store_true", help="Print output as formatted JSON")
    args = parser.parse_args()

    data = generate_transactions(args.count)

    if args.insert:
        res = supabase.table("transactions").insert(data).execute()
        print(f"✅ Inserted {len(res.data or [])} synthetic transactions into Supabase.")
    elif args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"⚡ Generated {len(data)} synthetic transactions (Sample 1st item: {data[0] if data else 'None'})")


if __name__ == "__main__":
    main()