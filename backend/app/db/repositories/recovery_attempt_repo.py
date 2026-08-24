from app.db.client import supabase
from app.agents.state import RecoveryState

def save_recovery_attempt(state: RecoveryState) -> dict:
    record = {
        "transaction_id": state["transaction_id"],
        "attempt_number": state["attempt_number"],
        "action_taken": state["action"],
        "reasoning": state["reasoning"],
        "outcome": state["outcome"],
        "amount_recovered": state.get("amount_recovered", 0),
        "next_retry_at": state.get("next_retry_at"),
    }
    result = supabase.table("recovery_attempts").insert(record).execute()
    return result.data[0]

