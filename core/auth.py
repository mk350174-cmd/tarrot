"""
The Spirit Gate — Supabase JWT verification.

Each request bears a JWT minted by Supabase Auth. We verify the signature,
extract the seeker's identity (`sub`), and forward the raw token so that
downstream Supabase calls run under the seeker's identity — letting RLS
guard the ancestral records.
"""
from dataclasses import dataclass

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import settings

_bearer = HTTPBearer(auto_error=True)


@dataclass
class AuthContext:
    user_id: str
    jwt_token: str  # raw token — pass to Supabase client for RLS


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> AuthContext:
    """Unveil the seeker behind the request — or turn them away at the gate."""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token — the gate remains closed.",
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token lacks a seeker identity.",
        )
    return AuthContext(user_id=str(user_id), jwt_token=token)
