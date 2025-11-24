"""
Modelační třídy pro nastavení
"""
from typing import Optional
from pydantic import BaseModel

class SettingsIn(BaseModel):
    """
    Přijímací třída při přihlášení
    """
    settings_id: str
    weather_enable: bool
    weather_place: Optional[str] = None
    weather_lat: Optional[float] = None
    weather_lon: Optional[float] = None
    quote_enable: bool

class SettingsOut(BaseModel):
    """
    Odpovídající třída při přihlášení
    """
    settings_id: str
    weather_enable: bool
    weather_place: Optional[str] = None
    weather_lat: Optional[float] = None
    weather_lon: Optional[float] = None
    quote_enable: bool
