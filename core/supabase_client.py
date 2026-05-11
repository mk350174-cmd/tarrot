"""
The Ancestral Path — Supabase client factory.

All database access flows through this module. We never use the service-role
key in user-facing paths; the user's own JWT is forwarded so PostgreSQL
Row-Level Security enforces privacy at the database layer.
"""
from supabase import Client, create_client

from core.config import settings


def get_user_supabase(jwt_token: str) -> Client:
    """
    Return a Supabase client scoped to the seeker's identity.

    The anon key is sent as apikey, the user's JWT as the Authorization
    bearer. RLS policies then evaluate `auth.uid()` against `user_id`.
    """
    client: Client = create_client(settings.supabase_url, settings.supabase_anon_key)
    client.postgrest.auth(jwt_token)
    return client
