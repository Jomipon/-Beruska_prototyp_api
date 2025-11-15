import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    # Vyhodíme chybu při startu – aspoň hned víš, že chybí proměnné
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_client(access_token: str) -> Client:
    """
    Vytvoří Supabase klienta, který se vůči DB prokazuje jako daný uživatel
    (přes jeho access token). RLS pak používá auth.uid() z tohoto tokenu.
    """
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    # tady je ten trik – přidáme token do PostgREST klienta
    client.postgrest.auth(access_token)
    return client
