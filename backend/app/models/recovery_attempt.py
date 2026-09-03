from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RecoveryAttemptOut(BaseModel):
    id: str
    transaction_id: str
    attempt_number: int
    action_taken: str
    reasoning: Optional[str]
    outcome: Optional[str]
    amount_recovered: float
    created_at: datetime
