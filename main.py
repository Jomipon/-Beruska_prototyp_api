"""
Hlavní metoda pro start aplikace
"""
from typing import List
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from Model.login import LoginIn, LoginOut, RefreshOut
from Model.store import ItemIn, ItemOut, IssueOut, IssueIn, IssueOutEnvelope
from Model.company import CompanyIn, CompanyOut
from Model.setting import SettingsIn, SettingsOut
from Model.weather import WeatherOut
from supabase_client import supabase
from auth_dep import get_auth_ctx, AuthContext
from Endpoint.auth_endpoint import login_endpoint, refresh_token_endpoint
from Endpoint.issue_endpoint import create_issue_endpoint
from Endpoint.weather_endpoint import get_weather_place_by_name_endpoint

app = FastAPI(title="Beruška API", version="0.1.0")

load_dotenv()

api_access_url = os.environ.get("API_ACCESS_URL")

origins = api_access_url

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Test běhu api
    """
    return {"status": "ok"}
@app.post("/auth/login", response_model=LoginOut, tags=["Auth"])
async def login(payload: LoginIn):
    """
    Přihlásí uživatele přes Supabase a vrátí access/refresh tokeny + základní info o uživateli.
    """
    return login_endpoint(supabase, payload)
@app.get("/auth/refresh", tags=["Auth"], response_model=RefreshOut)
async def refresh_token(refresh_token: str):
    """
    Obnova session z refresh tokenu (když access token expiruje).
    """
    return refresh_token_endpoint(supabase, refresh_token)
@app.get("/create_owner_id", tags=["Functions"])
async def get_create_owner_id(ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Zavolá funkci create_owner_id v Supabase, aby se připravila tabulka accounts
    """
    client = ctx.client
    try:
        client.rpc("create_owner_id").execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Function not found not found"
            ) from e
    return {"status": "ok"}

@app.get("/create_issue_from_pre", tags=["Functions"])
async def get_create_issue_from_pre(id_pre: str, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Zavolá funkci create_issue_from_pre v Supabase, která překlopí data z pre tabulky
    """
    client = ctx.client
    try:
        client.rpc("create_issue_from_pre", params={"p_id_pre": id_pre}).execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Function create_issue_from_pre not found"
            ) from e
    return {"status": "ok"}

@app.get("/companies", tags=["Company"]) #response_model=List[CompanyOut]
async def list_companies(ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací seznam partnerů
    """
    client = ctx.client
    try:
        resp = client.from_("company_fullname").select("*").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
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
        resp = client.from_("company_fullname").select("*").filter("company_id", "eq", str(id_company)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    if len(resp.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id '{id_company}' not found"
    )
    return resp.data[0]
@app.post("/company", response_model=CompanyOut, tags=["Company"])
async def create_company(company: CompanyIn, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vloží nového partnera
    """
    client = ctx.client
    try:
        id_company = company.company_id
        resp = client.from_("company").select("*").filter("company_id", "eq", str(id_company)).execute()
        if len(resp.data) > 0:
            raise HTTPException(status_code=500, detail="Company is exists")
        client.from_("company").insert(company.model_dump()).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    try:
        resp = client.from_("company").select("*").filter("company_id", "eq", str(id_company)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    if len(resp.data) == 0:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Company with id '{id_company}' not found"
        )
    return resp.data[0]
@app.put("/company/{id_company}", response_model=CompanyOut, tags=["Company"])
async def update_company(company: CompanyIn, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Upraví uloženého partnera
    """
    client = ctx.client
    id_company = company.company_id
    #print(f"{company.model_dump()=}")
    client.from_("company").update(company.model_dump()).eq("company_id", id_company).execute()
    try:
        resp = client.from_("company_fullname").select("*").filter("company_id", "eq", str(id_company)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    if len(resp.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id '{id_company}' not found"
    )
    return resp.data[0]
@app.delete("/company/{id_company}", tags=["Company"])
async def delete_company(id_company, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací detail jednoho partnera
    """
    client = ctx.client
    try:
        resp = client.from_("company").select("*").filter("company_id", "eq", str(id_company)).execute()
        if len(resp.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"Company with id '{id_company}' not found")
        resp = client.from_("company").delete().filter("company_id", "eq", str(id_company)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    
    return {"status": "ok"}
@app.get("/items", response_model=List[ItemOut], tags=["Items"])
async def list_items(ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací seznam sortimentu
    """
    client = ctx.client
    try:
        resp = client.from_("item").select("*").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    return resp.data
@app.get("/item/{id_item}", response_model=ItemOut, tags=["Item"])
async def get_item(id_item, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací detail jednoho sortimentu
    """
    client = ctx.client
    try:
        resp = client.from_("item").select("*").filter("item_id", "eq", str(id_item)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    if len(resp.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{id_item}' not found"
    )
    return resp.data[0]
@app.post("/item", status_code=201, response_model=ItemOut, tags=["Items"])
async def create_item(item: ItemIn, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vytvoří nový sortiment
    """
    client = ctx.client
    try:
        id_item = item.item_id
        resp = client.from_("item").select("*").filter("item_id", "eq", str(id_item)).execute()
        if len(resp.data) > 0:
            raise HTTPException(status_code=500, detail="Item is exists")
        print(f"{item=}")
        client.from_("item").insert(item.model_dump()).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    try:
        resp = client.from_("item").select("*").filter("item_id", "eq", str(id_item)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    if len(resp.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{id_item}' not found"
    )
    return resp.data[0]
@app.put("/item/{id_item}", response_model=ItemOut, tags=["Item"])
async def update_item(item: ItemIn, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Upraví uloženého partnera
    """
    client = ctx.client
    #try:
    id_item = item.item_id
    print(f"{item.model_dump()=}")
    client.from_("item").update(item.model_dump()).eq("item_id", id_item).execute()
#except Exception as e:
    #    raise HTTPException(status_code=500, detail=e) from e
    try:
        resp = client.from_("item").select("*").filter("item_id", "eq", str(id_item)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    if len(resp.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{id_item}' not found"
    )
    return resp.data[0]
@app.delete("/item/{id_item}", tags=["Item"])
async def delete_item(id_item, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací detail jednoho partnera
    """
    client = ctx.client
    try:
        resp = client.from_("item").select("*").filter("item_id", "eq", str(id_item)).execute()
        if len(resp.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"Item with id '{id_item}' not found")
        resp = client.from_("item").delete().filter("item_id", "eq", str(id_item)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    
    return {"status": "ok"}
@app.get("/settings", response_model=SettingsOut, tags=["Settings"])
async def get_settings(ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací nastavení uživatele
    """
    client = ctx.client
    try:
        resp = client.from_("settings").select("*").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    if len(resp.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settings not found"
    )
    return resp.data[0]
@app.put("/settings", response_model=SettingsOut, tags=["Settings"])
async def update_settings(settings: SettingsIn, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Upraví uložené nastavení uživatele
    """
    client = ctx.client
    try:
        settings_id = settings.settings_id
        client.from_("settings").update(settings.model_dump()).filter("settings_id", "eq", settings_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    try:
        resp = client.from_("settings").select("*").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    if len(resp.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settings not found"
        )
    print(resp)
    return resp.data[0]
@app.get("/weather_place/{place_name}", response_model=WeatherOut, tags=["Weather"])
async def get_weather_place_by_name(place_name, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací GPS souřadnice pro zadanou lokalitu
    """
    client = ctx.client
    try:
        weather_place = get_weather_place_by_name_endpoint(client, place_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    return weather_place
@app.get("/issues", tags=["Issue"]) #response_model=List[IssueOut]
async def get_issues(ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací seznam všech výdejek (pouze hlavičky)
    """
    client = ctx.client
    try:
        #resp = client.from_("issue_head").select("*").execute()
        #resp = client.from_("issue_detail").select("*, issue_head(*)").execute()
        #resp = client.from_("issue_detail").select("*, issue_head(*)").execute()
        #resp = client.from_("issue_head").select("""  *,  start_scan:scans!scan_id_start (    id,    user_id,    badge_scan_time  ),  end_scan:scans!scan_id_end (    id,    user_id,    badge_scan_time  )""").execute()
        #resp = client.from_("issue_head").select("*, company(*)").execute()
        resp = client.from_("issue_head").select("*").execute()
        for issue in resp.data:
            if issue["company_id"]:
                company_detail = client.from_("company_fullname").select("*").filter("company_id", "eq", issue["company_id"]).execute()
                if company_detail.data:
                    issue["company_fullname"] = company_detail.data[0]["name_full"]
                else:
                    issue["company_fullname"] = ""
    except Exception as e:
        print(f"{e=}")
        raise HTTPException(status_code=500, detail=e) from e
    #return resp.data
    return {"row_count": len(resp.data), "data": resp.data}
#@app.get("/issue/{id_item}", tags=["Issue"]) # response_model=IssueOut
@app.get("/issue/{issue_id}", response_model=IssueOutEnvelope, tags=["Issue"]) # response_model=IssueOut
async def get_issue(issue_id, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vrací detail jedné výdejky (hlavičku i detail)
    """
    client = ctx.client
    try:
        resp = client.from_("issue_head").select("*").filter("issue_id", "eq", str(issue_id)).execute()
        if len(resp.data) == 0:
            return {"status": "NO_HEAD_DATA", "data": None}
        detail = client.from_("issue_detail").select("*, item(*)").filter("issue_id", "eq", str(issue_id)).execute()
        if len(detail.data) == 0:
            return {"status": "NO_DETAIL_DATA", "data": None}
        rows_detail = []
        for row_detail in detail.data:
            if row_detail["item_id"]:
                item_row = client.from_("item").select("*").filter("item_id", "eq", row_detail["item_id"]).execute()
                rows_detail.append(item_row)
        resp.data[0]["issueDetail"] = detail.data
        company = client.from_("company_fullname").select("*").filter("company_id", "eq", resp.data[0]["company_id"]).execute()
        if company.data:
            resp.data[0]["company"] = company.data[0]
        else:
            resp.data[0]["company"] = None

    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    return {"status": "OK", "data": resp.data[0]}
@app.post("/issue", status_code=201, tags=["Issue"]) #response_model=IssueOut
async def create_issue(issue: IssueIn, ctx: AuthContext = Depends(get_auth_ctx)):
    """
    Vždy vyžaduje platný Bearer token.
    ctx.client má nastavený access_token, takže RLS běží jako konkrétní uživatel.
    Vytvoří novou výdejku
    """
    client = ctx.client
    try:
        issue_insert = create_issue_endpoint(client, issue)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
    print(f"{issue_insert=}")
    return issue_insert
@app.get("/test", tags=["Test"])
async def get_test():
    """
    Test GET metody
    """
    return {"status": "ok"}
@app.post("/test", tags=["Test"])
async def post_test(post_data: dict):
    """
    Test POST metody
    """
    return post_data
@app.put("/test", tags=["Test"])
async def put_test(post_data: dict):
    """
    Test PUT metody
    """
    return post_data
@app.delete("/test", tags=["Test"])
async def delete_test(post_data: dict):
    """
    Test DELETE metody
    """
    return post_data


@app.get("/movies", tags=["Test"])
async def get_test_references(ctx: AuthContext = Depends(get_auth_ctx)):
    client = ctx.client
    #resp = client.from_("performances").select("knu:id, *").execute()
    #resp = client.from_("performances").select("*, actors(*)").execute()
    resp = client.from_("performances").select("knu:id, act:actors(actor_id:id, *), movies(*)").execute()

    return resp
