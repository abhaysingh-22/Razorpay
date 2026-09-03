from typing import TypedDict, Optional
from datetime import datetime


class RecoveryState(TypedDict):
    # input
    transaction_id: str
    amount: float
    failure_reason: str
    customer_id: str
    attempt_number: int

    # filled in by nodes as it flows through the graph
    classified_reason: Optional[str]  # normalized/confirmed reason
    action: Optional[
        str
    ]  # 'retry_scheduled' | 'card_update_requested' | 'escalated' | 'stopped'
    reasoning: Optional[str]  # LLM's explanation — this becomes your audit trail
    should_stop: bool
    outcome: Optional[str]  # 'success' | 'failed' | 'pending'
    amount_recovered: float
    next_retry_at: Optional[datetime]  # when the next retry is scheduled, if applicable
