"""
Modelační třídy pro partnera
"""
from ast import literal_eval
from typing import Optional
from pydantic import BaseModel, Field

class CompanyIn(BaseModel):
    """
    Partner jako přijímaci parametr na API
    """
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

    def get_json_attributes(self):
        """
        Vrací json atributy
        """
        attributes = [
            "company_id",
            "name",
            "name_first",
            "name_last",
            "active",
            "note",
            "type_person",
            "address",
            "type_relationship",
            "email",
            "phone_number",
            "alias",
            "foundation_id",
            "ico"
        ]
        json = {}
        for attribute in attributes:
            json[attribute] = literal_eval("self."+attribute)
        return json

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
    address: Optional[str] = Field(description="Comapny address")
    type_relationship: int = Field(description="Relationship - 0 customer, 1 suplier, 2 customer + suplier")
    email: Optional[str] = Field(description="Email")
    phone_number: Optional[str] = Field(description="Phone number")
    alias: Optional[str] = Field(description="Nock name")
    foundation_id: Optional[str] = Field(description="ID base")
    ico: Optional[str] = Field(description="ICO")
