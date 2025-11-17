"""
Modelační třídy pro sklad
"""
from ast import literal_eval
from typing import Optional
from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    """
    Přijímací třída při dotazování sortimentu
    """
    item_id: str = Field(description="ID Item", min_length=1)
    name: str = Field(description="Item name", min_length=1)
    item_number: str = Field(description="Item number")
    description: Optional[str] = None
    price_purchase: float
    price_selling: float
    item_type: int
    active: bool
    note: str
    def get_json_attributes(self):
        """
        Vrací json atributy
        """
        attributes = [
            "item_id",
            "name",
            "item_number",
            "description",
            "price_purchase",
            "price_selling",
            "item_type",
            "active",
            "note",
        ]
        json = {}
        for attribute in attributes:
            json[attribute] = literal_eval("self."+attribute)
        return json

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
