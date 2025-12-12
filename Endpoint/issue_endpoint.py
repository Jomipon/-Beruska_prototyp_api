"""
Endpoint pro výdejku
"""
from ast import literal_eval
import uuid
from typing import Optional
from fastapi import HTTPException
from Model.store import IssueIn, IssueDetailIn
def create_issue_endpoint(client, issue):
    """
    Vytváří dýdejku hlavičku i detail
    
    :param client: připojení do databáze
    :param issue: Výdejka
    """
    issue_id = issue.issue_id
    issue_number = issue.issue_number

    resp = client.table("issue_head").select("*").filter("issue_id", "eq", str(issue_id)).execute()
    if len(resp.data) > 0:
        raise HTTPException(status_code=500, detail="Issue ID is exists")
    resp = client.table("issue_head").select("*").filter("issue_number", "eq", str(issue_number)).execute()
    if len(resp.data) > 0:
        raise HTTPException(status_code=500, detail="Issue number is exists")
    #print(f"{issue.model_fields=}") #IssueIn.model_fields()
    #print(f"{issue.model_fields.items()=}") #IssueIn.model_fields()
    columns_head = []
    for column_name, column_type in issue.model_fields.items():
        print(f"{column_name} - {column_type} - {column_type.annotation}")
        if column_type.annotation in (str,int,float,Optional[str],Optional[int],Optional[float]):
            columns_head.append(column_name)
    print(f"{columns_head=}")
    issue_head_insert = {}
    for column_head in columns_head:
        print(f"{column_head=}")
        #issue_head_insert[column_head] = literal_eval(f"issue.{column_head}")
    print(f"{issue_head_insert=}")
    pre_id_tran = str(uuid.uuid4())
    issue_head_insert["pre_id"] = pre_id_tran
    issue_head_insert["issue_id"] = issue.issue_id
    issue_head_insert["issue_number"] = issue.issue_number
    issue_head_insert["date_of_issue"] = issue.date_of_issue.isoformat()
    issue_head_insert["company_id"] = issue.company_id
    issue_head_insert["note"] = issue.note
    issue_head_insert["place"] = issue.place
    issue_head_insert["issue_price"] = issue.issue_price
    
    issue_detail_insert = {}
    issue_detail_insert["pre_id"] = pre_id_tran
    issue_detail_insert["issue_id"] = issue.issue_id
    issue_detail_insert["item_id"] = issue.issueDetail[0].item_id
    issue_detail_insert["amoung"] = issue.issueDetail[0].amoung
    issue_detail_insert["price_peice"] = issue.issueDetail[0].price_peice
    issue_detail_insert["price_row"] = issue.issueDetail[0].price_row
    issue_detail_insert["note"] = issue.issueDetail[0].note
    
    client.from_("issue_head_pre").insert(issue_head_insert).execute()
    client.from_("issue_detail_pre").insert(issue_detail_insert).execute()
    #client.rpc("create_issue_from_pre").execute()
    #client.from_("issue_head").insert(issue.model_dump()).execute()
    #client.from_("issue_head").insert(issue_head_insert).then().from_("issue_detail").insert(issue_detail_insert).execute()

    #resp = client.table("issue_head").select("*").filter("issue_id", "eq", str(issue_id)).execute()
    #return resp.data[0]
    return issue_head_insert


