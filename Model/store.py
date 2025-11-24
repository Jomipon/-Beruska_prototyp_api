"""
Modelační třídy pro sklad
"""
from typing import Optional
from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    """
    Přijímací třída při dotazování sortimentu
    """
    item_id: str = Field(description="ID Item", min_length=1)
    name: str = Field(description="Item name", min_length=1)
    item_number: str = Field(description="Item number")
    price_purchase: float
    price_selling: float
    item_type: int
    active: bool
    note: str

class ItemOut(BaseModel):
    """
    Odpovídací třída při dotazování sortimentu
    """
    item_id: str
    name: str
    item_number: Optional[str]
    price_purchase: float
    price_selling: float
    item_type: int
    active: bool
    note: str
