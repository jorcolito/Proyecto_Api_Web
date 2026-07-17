import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

@lru_cache(maxsize=1)
def get_supabase() -> Client:
    """Create the Supabase client only when an endpoint needs it."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Faltan SUPABASE_URL o SUPABASE_KEY en las variables de entorno."
        )

    return create_client(supabase_url, supabase_key)
