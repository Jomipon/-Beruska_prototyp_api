from Model.login import LoginResponse, RefreshResponce
from fastapi import HTTPException

def login_endpoint(supabase, payload):
    try:
        res = supabase.auth.sign_in_with_password({"email": payload.email, "password": payload.password})
        if not res or not res.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session = res.session
        return LoginResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            user=vars(res.user) if res.user else {},
        )
    except Exception as e:
        # schválně neprozrazujeme detail (pro bezpečnost)
        raise HTTPException(status_code=401, detail="Invalid email or password")

def refresh_token_endpoint(supabase, refresh_token):
    try:
        refreshed = supabase.auth.refresh_session(refresh_token)
        if not refreshed or not refreshed.session:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return RefreshResponce(
            access_token = refreshed.session.access_token,
            refresh_token = refreshed.session.refresh_token,
            token_type = "bearer",
            user = vars(refreshed.user) if refreshed.user else {},
            )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
