from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

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
    from app.api.v1.transactions import reset_database_endpoint
    return reset_database_endpoint()

