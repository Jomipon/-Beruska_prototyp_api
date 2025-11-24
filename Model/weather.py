"""
Modelační třídy pro počasí
"""
from pydantic import BaseModel
class WeatherOut(BaseModel):
    """
    Odesílací třída pro GPS lokaci
    """
    id: str
    place_name: str
    place_lat: float
    place_lon: float
    created_at: str
