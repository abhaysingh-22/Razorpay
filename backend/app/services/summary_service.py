from app.db.client import supabase

def generate_batch_summary(results: list[dict] | None = None) -> dict:
    if results is None:
        transactions = supabase.table("transactions").select("*").execute().data
        attempts = (
            supabase.table("recovery_attempts")
            .select("*")
            .order("created_at", desc=True)
            .execute()
            .data
        )
        latest_attempts = {}
        for attempt in attempts:
            latest_attempts.setdefault(attempt["transaction_id"], attempt)
        attempts = list(latest_attempts.values())

        total_transactions = len(transactions)
        total_amount_at_risk = sum(t["amount"] for t in transactions)
        total_recovered = sum(a["amount_recovered"] or 0 for a in attempts)

        breakdown = {}
        for t in transactions:
            reason = t["failure_reason"]
            breakdown.setdefault(reason, {"count": 0, "recovered": 0})
            breakdown[reason]["count"] += 1
        for a in attempts:
            tx = next((t for t in transactions if t["id"] == a["transaction_id"]), None)
            if tx and a["outcome"] == "success":
                breakdown[tx["failure_reason"]]["recovered"] += a["amount_recovered"] or 0

    else:
        # results already carry everything we need per-transaction — no matching required
        attempts = [
            {
                "transaction_id": r["transaction_id"],
                "action_taken": r["action"],
                "reasoning": r["reasoning"],
                "outcome": r["outcome"],
                "amount_recovered": r.get("amount_recovered", 0),
                "attempt_number": r["attempt_number"],
            }
            for r in results
        ]

        total_transactions = len(results)
        total_amount_at_risk = sum(r["amount"] for r in results)
        total_recovered = sum(r.get("amount_recovered", 0) or 0 for r in results)

        breakdown = {}
        for r in results:
            reason = r["failure_reason"]
            breakdown.setdefault(reason, {"count": 0, "recovered": 0})
            breakdown[reason]["count"] += 1
            if r["outcome"] == "success":
                breakdown[reason]["recovered"] += r.get("amount_recovered", 0) or 0

    recovery_rate = round((total_recovered / total_amount_at_risk) * 100, 1) if total_amount_at_risk else 0

    highlights = [
        f"₹{total_recovered:,.0f} recovered out of ₹{total_amount_at_risk:,.0f} at risk ({recovery_rate}%)",
        f"{total_transactions} failed transactions processed",
        f"{sum(1 for a in attempts if a['action_taken'] == 'escalated')} cases escalated for fraud review — zero auto-retries attempted on these",
        f"{sum(1 for a in attempts if a['action_taken'] == 'stopped')} cases stopped after exceeding retry limit",
    ]

    exceptions = [
        f"Transaction {a['transaction_id']}: stopped after {a['attempt_number']} attempts, reason: {a['reasoning']}"
        for a in attempts if a["action_taken"] == "stopped"
    ]

    summary = {
        "total_transactions": total_transactions,
        "total_amount_at_risk": total_amount_at_risk,
        "total_amount_recovered": total_recovered,
        "recovery_rate": recovery_rate,
        "breakdown_by_reason": breakdown,
        "key_highlights": highlights,
        "exceptions": exceptions,
    }

    supabase.table("batch_summaries").insert(summary).execute()
    return summary
