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

    elif action == "escalated" or reason == "fraud_flag" or transaction["amount"] >= 10000:
        # Human-in-the-Loop Gate: Route suspicious or high-ticket payments for human verification
        result["outcome"] = "pending"
        result["amount_recovered"] = 0
        if reason == "fraud_flag":
            result["action"] = "flagged_for_human_review"
            result["reasoning"] = "Potential fraud pattern detected. Paused for Human-in-the-Loop Risk Officer verification."
        else:
            result["action"] = "high_ticket_human_review"
            result["reasoning"] = f"High-ticket transaction (₹{transaction['amount']:,.2f}) paused for risk safety review before retry."
        new_status = "pending_human_review"

    else:  # stopped
        result["outcome"] = "failed"
        result["amount_recovered"] = 0
        new_status = "exhausted"

    save_recovery_attempt(result)
    supabase.table("transactions").update({"status": new_status}).eq("id", transaction["id"]).execute()

    return result


def resolve_human_review(transaction_id: str, decision: str, notes: str | None = None) -> dict:
    """Handles Human-in-the-Loop (HITL) manual resolution for paused transactions."""
    tx_res = supabase.table("transactions").select("*").eq("id", transaction_id).execute()
    if not tx_res.data:
        raise ValueError(f"Transaction {transaction_id} not found.")

    transaction = tx_res.data[0]
    existing_attempts = supabase.table("recovery_attempts") \
        .select("attempt_number") \
        .eq("transaction_id", transaction_id) \
        .execute().data or []
    next_attempt = len(existing_attempts) + 1

    if decision == "approve":
        new_status = "recovered"
        attempt_record = {
            "transaction_id": transaction_id,
            "attempt_number": next_attempt,
            "action": "human_approved_retry",
            "reasoning": notes or "Risk Officer reviewed risk telemetry and approved recovery retry.",
            "outcome": "success",
            "amount_recovered": float(transaction["amount"]),
        }
    else:
        new_status = "escalated"
        attempt_record = {
            "transaction_id": transaction_id,
            "attempt_number": next_attempt,
            "action": "human_confirmed_block",
            "reasoning": notes or "Risk Officer confirmed fraud risk and permanently blocked auto-recovery.",
            "outcome": "failed",
            "amount_recovered": 0,
        }

    save_recovery_attempt(attempt_record)
    supabase.table("transactions").update({"status": new_status}).eq("id", transaction_id).execute()
    summary = generate_batch_summary()

    return {
        "status": "success",
        "transaction_id": transaction_id,
        "decision": decision,
        "new_status": new_status,
        "summary": summary
    }


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