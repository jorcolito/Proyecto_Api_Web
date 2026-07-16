import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Faltan SUPABASE_URL o SUPABASE_KEY en las variables de entorno.")

supabase: Client = create_client(supabase_url, supabase_key)


def get_supabase() -> Client:
    return supabase
