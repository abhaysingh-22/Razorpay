from app.agents.state import RecoveryState
from app.services.razorpay_service import retry_payment, send_card_update_link
from datetime import datetime, timedelta

def execute_retry_node(state: RecoveryState) -> RecoveryState:
    action = state["action"]

    if action == "retry_scheduled":
        result = retry_payment(state["transaction_id"], state["amount"])
        if result["success"]:
            state["outcome"] = "pending"   # order created, payment not confirmed yet
        else:
            state["outcome"] = "failed"

    elif action == "card_update_requested":
        result = send_card_update_link(state["customer_id"])
        state["outcome"] = "pending"

    elif action == "escalated":
        state["outcome"] = "pending"   # handed off to human, not resolved by agent

    elif action == "stopped":
        state["outcome"] = "failed"
        state["amount_recovered"] = 0

    if action in ("retry_scheduled", "card_update_requested"):
        state["next_retry_at"] = (datetime.utcnow() + timedelta(hours=24)).isoformat()

    return state

