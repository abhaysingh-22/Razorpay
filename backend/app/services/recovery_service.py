import random
from app.db.client import supabase
from app.agents.graph import recovery_graph
from app.db.repositories.recovery_attempt_repo import save_recovery_attempt
from app.services.summary_service import generate_batch_summary


def run_recovery_for_transaction(transaction: dict) -> dict:
    # figure out how many attempts already happened for this transaction
    existing_attempts = supabase.table("recovery_attempts") \
        .select("attempt_number") \
        .eq("transaction_id", transaction["id"]) \
        .execute().data or []
    next_attempt_number = len(existing_attempts) + 1

    state = {
        "transaction_id": transaction["id"],
        "amount": float(transaction["amount"]),
        "failure_reason": transaction["failure_reason"],
        "customer_id": transaction["customer_id"],
        "attempt_number": next_attempt_number,
        "classified_reason": None,
        "action": None,
        "reasoning": None,
        "should_stop": False,
        "outcome": None,
        "amount_recovered": 0,
    }

    result = recovery_graph.invoke(state)
    action = result.get("action")
    attempt_num = result.get("attempt_number", 1)
    reason = result.get("classified_reason") or transaction.get("failure_reason")

    # Multi-Run Realistic Resolution Lifecycle
    if action == "retry_scheduled":
        if reason == "bank_timeout":
            # Bank timeouts: 85% recovered on attempt 1
            if random.random() < 0.85:
                result["outcome"] = "success"
                result["amount_recovered"] = result["amount"]
                new_status = "recovered"
            else:
                result["outcome"] = "pending"
                result["amount_recovered"] = 0
                new_status = "retry_scheduled"
        elif reason == "insufficient_funds":
            # Run 1: ~30% recovered, else schedule Attempt 2
            # Run 2: ~60% recovered (salary date), else schedule Attempt 3
            # Run 3: ~50% recovered, else exhausted
            if attempt_num == 1:
                if random.random() < 0.30:
                    result["outcome"] = "success"
                    result["amount_recovered"] = result["amount"]
                    new_status = "recovered"
                else:
                    result["outcome"] = "pending"
                    result["amount_recovered"] = 0
                    new_status = "retry_scheduled"
            elif attempt_num == 2:
                if random.random() < 0.60:
                    result["outcome"] = "success"
                    result["amount_recovered"] = result["amount"]
                    new_status = "recovered"
                else:
                    result["outcome"] = "pending"
                    result["amount_recovered"] = 0
                    new_status = "retry_scheduled"
            else:  # attempt 3+
                if random.random() < 0.50:
                    result["outcome"] = "success"
                    result["amount_recovered"] = result["amount"]
                    new_status = "recovered"
                else:
                    result["outcome"] = "failed"
                    result["amount_recovered"] = 0
                    result["action"] = "stopped"
                    result["reasoning"] = f"Exceeded maximum retries ({attempt_num}) for insufficient funds."
                    new_status = "exhausted"
        else:
            if random.random() < 0.50:
                result["outcome"] = "success"
                result["amount_recovered"] = result["amount"]
                new_status = "recovered"
            else:
                result["outcome"] = "pending"
                result["amount_recovered"] = 0
                new_status = "retry_scheduled"

    elif action == "card_update_requested":
        # Expired card: 
        # Attempt 1: notification sent -> awaiting_customer_action
        # Subsequent runs (attempts 2+): 55% chance customer updated card -> recovered!
        if attempt_num == 1:
            result["outcome"] = "pending"
            result["amount_recovered"] = 0
            new_status = "awaiting_customer_action"
        elif attempt_num <= 3:
            if random.random() < 0.55:
                result["outcome"] = "success"
                result["amount_recovered"] = result["amount"]
                result["action"] = "retry_scheduled"
                result["reasoning"] = "Customer updated payment method following notifications. Retry processed successfully."
                new_status = "recovered"
            else:
                if attempt_num >= 3:
                    result["outcome"] = "failed"
                    result["amount_recovered"] = 0
                    result["action"] = "stopped"
                    result["reasoning"] = "Customer did not update expired card after multiple reminders."
                    new_status = "exhausted"
                else:
                    result["outcome"] = "pending"
                    result["amount_recovered"] = 0
                    new_status = "awaiting_customer_action"
        else:
            result["outcome"] = "failed"
            result["amount_recovered"] = 0
            result["action"] = "stopped"
            new_status = "exhausted"

    elif action == "escalated":
        result["outcome"] = "failed"
        result["amount_recovered"] = 0
        new_status = "escalated"

    else:  # stopped
        result["outcome"] = "failed"
        result["amount_recovered"] = 0
        new_status = "exhausted"

    save_recovery_attempt(result)
    supabase.table("transactions").update({"status": new_status}).eq("id", transaction["id"]).execute()

    return result


def run_batch_recovery() -> dict:
    """Pulls all actionable transactions (failed, retry_scheduled, awaiting_customer_action) and runs recovery."""
    res_failed = supabase.table("transactions").select("*").eq("status", "failed").execute().data or []
    res_retry = supabase.table("transactions").select("*").eq("status", "retry_scheduled").execute().data or []
    res_awaiting = supabase.table("transactions").select("*").eq("status", "awaiting_customer_action").execute().data or []

    all_tx_map = {tx["id"]: tx for tx in (res_failed + res_retry + res_awaiting)}
    transactions = list(all_tx_map.values())

    results = []
    for tx in transactions:
        try:
            result = run_recovery_for_transaction(tx)
            results.append(result)
        except Exception as e:
            print(f"Failed to process transaction {tx['id']}: {e}")

    summary = generate_batch_summary(results if results else None)
    return {"processed": len(results), "summary": summary}