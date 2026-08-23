from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import sys
import platform
from datetime import datetime

app = FastAPI(
    title="Razorpay Recovery & Risk Manager API",
    description="Backend API for Razorpay Agentic AI System",
    version="1.0.0",
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

START_TIME = time.time()

@app.get("/")
def read_root():
    return {
        "service": "Razorpay Agentic AI Backend",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "docs_url": "/docs",
    }

@app.get("/api/health")
def health_check():
    uptime_seconds = round(time.time() - START_TIME, 2)
    return {
        "status": "healthy",
        "uptime_seconds": uptime_seconds,
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "modules": {
            "fastapi": "0.115.0",
            "langgraph": "0.2.45",
            "groq": "available",
            "supabase": "configured",
            "razorpay": "ready"
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

@app.get("/api/ping")
def ping():
    return {
        "message": "pong",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
