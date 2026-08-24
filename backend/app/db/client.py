# pyrefly: ignore [missing-import]
from supabase import create_client, Client
from app.config import settings

# Initialize the Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
