# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.api.v1 import transactions, recovery, metrics

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(transactions.router)
api_router.include_router(recovery.router)
api_router.include_router(metrics.router)