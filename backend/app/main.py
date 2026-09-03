# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.api.v1.transactions import reset_database_endpoint
from app.api.v1.metrics import export_recovery_pdf

app = FastAPI(title="AI Revenue Recovery")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this to your frontend URL before final submission
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "ai-revenue-recovery"}

@app.get("/reset")
@app.post("/reset")
def root_reset():
    return reset_database_endpoint()

@app.get("/export-pdf")
def root_export_pdf():
    return export_recovery_pdf()

