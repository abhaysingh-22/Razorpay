
# pyrefly: ignore [missing-import]
from supabase import Client
from app.db.client import supabase

def get_db() -> Client:
    """
    Get the Supabase client instance.
    """
    return supabase
