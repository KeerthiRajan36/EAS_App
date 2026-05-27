from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssignAssetSchema(BaseModel):
    asset_id: int
    employee_id: int


class ReturnAssetsSchema(BaseModel):
    allocation_id: int


class AllocationResponse(BaseModel):

    id: int
    asset_id: int
    employee_id: int
    assigned_date: datetime
    returned_date: Optional[datetime]

 
