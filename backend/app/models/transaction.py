from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionOut(BaseModel):
    id: str
    razorpay_payment_id: Optional[str]
    amount: float
    currency: str
    status: str
    failure_reason: str
    customer_id: str
    next_retry_at: Optional[datetime]
    created_at: datetime
