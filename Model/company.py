"""
Modelační třídy pro partnera
"""
from typing import Optional
from pydantic import BaseModel, Field

class CompanyIn(BaseModel):
    """
    Partner jako přijímaci parametr na API
    """
    company_id: str = Field(description="ID Company", min_length=1)
    name: Optional[str] = Field(description="Company name", default=None)
    name_first: Optional[str] = Field(description="First name", default=None)
    name_last: Optional[str] = Field(description="Last name", default=None)
    active: bool = Field(description="Is active", default=True)
    note: Optional[str] = Field(description="Note", default=None)
    type_person: int = Field(description="Type - 0 person, 1 company", default=0)
    address: Optional[str] = Field(description="Company address", default=None)
    type_relationship: int = Field(description="Relationship - 0 customer, 1 suplier, 2 customer + suplier", default=2)
    email: Optional[str] = Field(description="Email", default=None)
    phone_number: Optional[str] = Field(description="Phone number", default=None)
    alias: Optional[str] = Field(description="Nock name", default=None)
    foundation_id: Optional[str] = Field(description="ID base", default=None)
    ico: Optional[str] = Field(description="ICO", default=None)

class CompanyOut(BaseModel):
    """
    Partner jako odesílací parametr na API
    """
    company_id: str = Field(description="ID Company", min_length=1)
    name: Optional[str] = Field(description="Company name")
    name_first: Optional[str] = Field(description="First name")
    name_last: Optional[str] = Field(description="Last name")
    active: bool = Field(description="Is active")
    note: Optional[str] = Field(description="Note")
    type_person: int = Field(description="Type - 0 person, 1 company")
    created_at: str
    address: Optional[str] = Field(description="Company address")
    type_relationship: int = Field(description="Relationship - 0 customer, 1 suplier, 2 customer + suplier")
    email: Optional[str] = Field(description="Email")
    phone_number: Optional[str] = Field(description="Phone number")
    alias: Optional[str] = Field(description="Nock name")
    foundation_id: Optional[str] = Field(description="ID base")
    ico: Optional[str] = Field(description="ICO")
