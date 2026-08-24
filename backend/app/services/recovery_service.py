from app.db.client import supabase
from app.agents.graph import recovery_graph
from app.db.repositories.recovery_attempt_repo import save_recovery_attempt
from app.services.summary_service import generate_batch_summary


def run_recovery_for_transaction(transaction: dict) -> dict:
    # figure out how many attempts already happened for this transaction
    existing_attempts = supabase.table("recovery_attempts") \
        .select("attempt_number") \
        .eq("transaction_id", transaction["id"]) \
        .execute().data
    next_attempt_number = len(existing_attempts) + 1

    state = {
        "transaction_id": transaction["id"],
        "amount": transaction["amount"],
        "failure_reason": transaction["failure_reason"],
        "customer_id": transaction["customer_id"],
        "attempt_number": next_attempt_number,   # was hardcoded to 1 before — bug
        "classified_reason": None,
        "action": None,
        "reasoning": None,
        "should_stop": False,
        "outcome": None,
        "amount_recovered": 0,
    }

    result = recovery_graph.invoke(state)

    if result["action"] == "retry_scheduled" and result["outcome"] == "pending":
        result["outcome"] = "success"
        result["amount_recovered"] = result["amount"]
        new_status = "recovered"
    elif result["action"] == "card_update_requested":
        result["outcome"] = "pending"
        result["amount_recovered"] = 0
        new_status = "awaiting_customer_action"   # NOT "failed" anymore — key fix
    elif result["action"] == "escalated":
        new_status = "escalated"
    else:  # stopped
        new_status = "exhausted"

    save_recovery_attempt(result)
    supabase.table("transactions").update({"status": new_status}).eq("id", transaction["id"]).execute()

    return result


def run_batch_recovery() -> dict:
    """Pulls all failed transactions and runs the full recovery flow on each."""
    transactions = supabase.table("transactions").select("*").eq("status", "failed").execute().data

    results = []
    for tx in transactions:
        try:
            result = run_recovery_for_transaction(tx)
            results.append(result)
        except Exception as e:
            print(f"Failed to process transaction {tx['id']}: {e}")

    summary = generate_batch_summary(results)
    return {"processed": len(results), "summary": summary}