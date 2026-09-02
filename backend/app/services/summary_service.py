from app.db.client import supabase

def generate_batch_summary(results: list[dict] | None = None) -> dict:
    transactions = supabase.table("transactions").select("*").execute().data or []
    attempts = (
        supabase.table("recovery_attempts")
        .select("*")
        .order("created_at", desc=True)
        .execute()
        .data or []
    )

    latest_attempts = {}
    for attempt in attempts:
        latest_attempts.setdefault(attempt["transaction_id"], attempt)

    total_transactions = len(transactions)
    total_amount_at_risk = sum(t["amount"] for t in transactions)
    total_recovered = sum(
        t["amount"] for t in transactions if t["status"] == "recovered"
    )

    breakdown = {}
    for t in transactions:
        reason = t["failure_reason"]
        breakdown.setdefault(reason, {"count": 0, "recovered": 0})
        breakdown[reason]["count"] += 1
        if t["status"] == "recovered":
            breakdown[reason]["recovered"] += t["amount"]

    recovery_rate = round((total_recovered / total_amount_at_risk) * 100, 1) if total_amount_at_risk else 0

    recovered_count = sum(1 for t in transactions if t["status"] == "recovered")
    escalated_count = sum(1 for t in transactions if t["status"] == "escalated")
    exhausted_count = sum(1 for t in transactions if t["status"] == "exhausted")
    pending_count = sum(1 for t in transactions if t["status"] in ("retry_scheduled", "awaiting_customer_action", "failed"))

    highlights = [
        f"₹{total_recovered:,.0f} recovered out of ₹{total_amount_at_risk:,.0f} at risk ({recovery_rate}%)",
        f"{total_transactions} total transactions managed ({recovered_count} recovered, {pending_count} in-flight)",
        f"{escalated_count} cases escalated for fraud review — zero auto-retries attempted on these",
        f"{exhausted_count} cases stopped after exceeding maximum retry limit",
    ]

    exceptions = [
        f"Transaction {a['transaction_id'][:8]}: stopped after {a['attempt_number']} attempts, reason: {a['reasoning']}"
        for a in latest_attempts.values() if a.get("action_taken") == "stopped" or a.get("action_taken") == "escalated"
    ]

    summary = {
        "total_transactions": total_transactions,
        "total_amount_at_risk": total_amount_at_risk,
        "total_amount_recovered": total_recovered,
        "recovery_rate": recovery_rate,
        "breakdown_by_reason": breakdown,
        "key_highlights": highlights,
        "exceptions": exceptions[:10],
    }

    supabase.table("batch_summaries").insert(summary).execute()
    return summary
