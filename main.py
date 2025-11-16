from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from Model.login import LoginRequest, LoginResponse, RefreshResponce
from Model.store import ItemIn, ItemOut
from Model.company import CompanyIn, CompanyOut
from supabase_client import supabase
from auth_dep import get_auth_ctx, AuthContext
from typing import List
from Endpoint.auth import login_endpoint, refresh_token_endpoint

app = FastAPI(title="Beruška API", version="0.1.0")

# Sem doplň adresu své Streamlit appky
origins = [
    "http://localhost:8501",                     # vývoj
    "https://jomipon-beruska-prototyp.streamlit.app",         # produkční Streamlit
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","PUT"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# ---------- AUTH ----------
@app.post("/auth/login", response_model=LoginResponse, tags=["Auth"])
async def login(payload: LoginRequest):
    """
    Přihlásí uživatele přes Supabase a vrátí access/refresh tokeny + základní info o userovi.
    Streamlit pošle email+password sem, ne přímo do Supabase.
    """
    return login_endpoint(supabase, payload)

@app.get("/auth/refresh", tags=["Auth"], response_model=RefreshResponce)
async def refresh_token(refresh_token: str):
    """
    Obnova session z refresh tokenu (když access token expiruje).
    Streamlit může zavolat, když dostane 401.
    """
    return refresh_token_endpoint(supabase, refresh_token)

# Functions
@app.get("/create_owner_id", tags=["Functions"])
async def get_create_owner_id(ctx: AuthContext = Depends(get_auth_ctx)):
    client = ctx.client
    try:
        resp = client.rpc("create_owner_id").execute()
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Function not found not found"
            )
    return {"status": "ok"}

# ---------- PROTECTED RESOURCES ----------
# ---------- Common ----------
@app.get("/companies", response_model=List[CompanyOut], tags=["Company"])
async def list_companies(ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací seznam partnerů
    """
    client = ctx.client
    try:
        resp = client.table("company").select("*").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    return resp.data

@app.get("/company/{id_company}", response_model=CompanyOut, tags=["Company"])
async def get_company(id_company, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací detail jednoho partnera
    """
    client = ctx.client
    try:
        resp = client.table("company").select("*").filter("company_id", "eq", str(id_company)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    if len(resp.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id '{id_company}' not found"
    )
    return resp.data[0]

# ---------- STORE ----------
@app.get("/items", response_model=List[ItemOut], tags=["Items"])
async def list_items(ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací seznam sortimentu
    """
    client = ctx.client
    try:
        resp = client.table("item").select("*").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    return resp.data


@app.post("/item", status_code=201, response_model=List[ItemOut], tags=["Items"])
async def create_item(item: ItemIn, ctx: AuthContext = Depends(get_auth_ctx)):
    client = ctx.client
    user = ctx.user

    # id uživatele – podle toho, co si v RLS používáš
    user_id = user.get("id") or user.get("sub")

    data = {
        "name": item.name,
        "description": item.description,
        "owner_id": user_id,   # pokud máš RLS na auth.uid() = owner_id
    }

    resp = client.table("items").insert(data).execute()
    if resp.error:
        raise HTTPException(status_code=500, detail=resp.error.message)
    return resp.data

