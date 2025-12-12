"""
Modelační třídy pro sklad
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from Model.company import CompanyOut

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

class IssueDetailOut(BaseModel):
    """
    Odesílací třída při dotazování issue detail
    """
    issue_detail_id: str
    issue_id: str
    item_id: str
    amoung: float
    price_peice: float
    price_row: float
    note: Optional[str]
    item: Optional[ItemOut]
class IssueOut(BaseModel):
    """
    Odpovídací třída při dotazování issue
    """
    issue_id: str
    issue_number: str
    date_of_issue: date
    company_id: Optional[str]
    note: Optional[str]
    place: Optional[str]
    issue_price: float
    created_at: str
    company: Optional[CompanyOut]
    issueDetail: Optional[list[IssueDetailOut]]
class IssueOutEnvelope(BaseModel):
    status: str
    data: Optional[IssueOut]
class IssueDetailIn(BaseModel):
    """
    Přijímací třída při dotazování issue detail
    """
    issue_detail_id: str
    issue_id: str
    item_id: str
    amoung: float
    price_peice: float
    price_row: float
    note: Optional[str]
class IssueIn(BaseModel):
    """
    Přijímací třída při dotazování issue
    """
    issue_id: str
    issue_number: str
    date_of_issue: date
    company_id: Optional[str]
    note: Optional[str]
    place: Optional[str]
    issue_price: float
    issueDetail: Optional[list[IssueDetailIn]]
