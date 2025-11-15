from pydantic import BaseModel, Field
from typing import Optional

class CompanyIn(BaseModel):
    company_id: str = Field(description="ID Company", min_length=1)
    name: Optional[str] = Field(description="Company name")
    name_first: Optional[str] = Field(description="First name")
    name_last: Optional[str] = Field(description="Last name")
    active: bool = Field(description="Is active")
    note: Optional[str] = Field(description="Note")
    type_person: int = Field(description="Type - 0 person, 1 company")
    address: Optional[str] = Field(description="Comapny address")
    type_relationship: int = Field(description="Relationship - 0 customer, 1 suplier, 2 customer + suplier")
    email: Optional[str] = Field(description="Email")
    phone_number: Optional[str] = Field(description="Phone number")
    alias: Optional[str] = Field(description="Nock name")
    foundation_id: Optional[str] = Field(description="ID base")
    ico: Optional[str] = Field(description="ICO")

class CompanyOut(BaseModel):
    company_id: str = Field(description="ID Company", min_length=1)
    name: Optional[str] = Field(description="Company name")
    name_first: Optional[str] = Field(description="First name")
    name_last: Optional[str] = Field(description="Last name")
    active: bool = Field(description="Is active")
    note: Optional[str] = Field(description="Note")
    type_person: int = Field(description="Type - 0 person, 1 company")
    created_at: str
    address: Optional[str] = Field(description="Comapny address")
    type_relationship: int = Field(description="Relationship - 0 customer, 1 suplier, 2 customer + suplier")
    email: Optional[str] = Field(description="Email")
    phone_number: Optional[str] = Field(description="Phone number")
    alias: Optional[str] = Field(description="Nock name")
    foundation_id: Optional[str] = Field(description="ID base")
    ico: Optional[str] = Field(description="ICO")
