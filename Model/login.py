"""
Modelační třídy pro přihlašování
"""
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    """
    Přijímací třída při přihlášení
    """
    email: EmailStr = Field(description="Email address", min_length=1)
    password: str = Field(description="Password", min_length=1)

class LoginResponse(BaseModel):
    """
    Odpovídací třída při přihlášení
    """
    access_token: str = Field(description="Access token to database", min_length=1)
    refresh_token: str = Field(description="Refresh token to database", min_length=1)
    token_type: str = "bearer"
    user: dict = Field(description="User information")

class RefreshResponce(BaseModel):
    """
    Odpovídací třída při refresh tokenu
    """
    access_token: str
    refresh_token: str
    token_type: str
    user: dict
