from pydantic import BaseModel


class BatchSummaryOut(BaseModel):
    id: str
    total_transactions: int
    total_amount_at_risk: float
    total_amount_recovered: float
    recovery_rate: float
    breakdown_by_reason: dict
    key_highlights: list[str]
    exceptions: list[str]
    created_at: str


class RunBatchResponse(BaseModel):
    processed: int
    summary: BatchSummaryOut
