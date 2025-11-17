"""
Authentifikace uživatele a přihlášení na supabase
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from supabase_client import supabase, get_user_client

bearer_scheme = HTTPBearer(auto_error=False)

class AuthContext:
    """
    Info o uživateli a Supabase klienta, který běží pro přihlášeného uživatele
    """
    def __init__(self, user: dict, client):
        self.user = user
        self.client = client

async def get_auth_ctx(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> AuthContext:
    """
    Ověří Bearer token
    Vrátí user info + supabase klienta, který běží pod tímto uživatelem (RLS)
    """
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    access_token = creds.credentials

    try:
        # ověření tokenu u Supabase Auth
        user_resp = supabase.auth.get_user(access_token)
        if not user_resp or not user_resp.user:
            raise HTTPException(status_code=401, detail="Invalid token")

        # klient s nastaveným JWT – bude triggerovat RLS jako tento user
        user_client = get_user_client(access_token)

        # supabase-py user může být objekt; převedeme ho na dict
        user_dict = user_resp.user.__dict__

        return AuthContext(user=user_dict, client=user_client)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from e
