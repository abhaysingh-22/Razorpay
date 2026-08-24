# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    groq_api_key: str
    razorpay_key_id: str
    razorpay_key_secret: str
    env: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()