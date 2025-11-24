"""
Endpoint pro autentifikaci uživatele
"""

from fastapi import HTTPException
from Model.login import LoginOut, RefreshOut

def login_endpoint(supabase, payload):
    """
    Přihlášení uživatele pomocí emailu a hesla
    """
    try:
        res = supabase.auth.sign_in_with_password({"email": payload.email, "password": payload.password})
        if not res or not res.session:
            print(f"{res=}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session = res.session
        return LoginOut(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            user=vars(res.user) if res.user else {},
        )
    except Exception as e:
        # schválně neprozrazujeme detail (pro bezpečnost)
        raise HTTPException(status_code=401, detail="Invalid email or password") from e

def refresh_token_endpoint(supabase, refresh_token):
    """
    Obnova session z refresh tokenu
    """
    try:
        refreshed = supabase.auth.refresh_session(refresh_token)
        if not refreshed or not refreshed.session:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return RefreshOut(
            access_token = refreshed.session.access_token,
            refresh_token = refreshed.session.refresh_token,
            token_type = "bearer",
            user = vars(refreshed.user) if refreshed.user else {},
            )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from e
