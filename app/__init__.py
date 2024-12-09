from supabase import create_client, Client
from app.config import Settings


def init_app():
    url: str = Settings.SUPABASE_URL
    key: str = Settings.SUPABASE_KEY
    supabase: Client = create_client(url, key)
    return supabase
