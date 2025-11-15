from pydantic import BaseModel, Field
from typing import Optional


class ItemIn(BaseModel):
    item_id: str = Field(description="ID Item", min_length=1)
    name: str = Field(description="Item name", min_length=1)
    item_number: str = Field(description="Item number")
    description: Optional[str] = None
    price_purchase: float
    price_selling: float
    item_type: int
    active: bool
    note: str

class ItemOut(BaseModel):
    item_id: str
    name: str
    item_number: Optional[str]
    price_purchase: float
    price_selling: float
    item_type: int
    active: bool
    note: str
